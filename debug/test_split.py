import re

test_data = "CategoryItemsQuantityBMC6868CPU6868MEMORY70274POWER_STRIPS22SERVER6868STORAGE_ARRAY1717SWITCH11"

print("=== PARSING WITH SPLIT LOGIC ===\n")

target_cats = ["BMC", "CPU", "MEMORY", "POWER_STRIPS", "SERVER", "STORAGE_ARRAY", "SWITCH"]

# Find positions
category_positions = []
for cat in target_cats:
    match = re.search(cat, test_data, re.IGNORECASE)
    if match:
        category_positions.append((match.start(), match.end(), cat))

category_positions.sort()

summary_data = {}
for i, (start, end, cat) in enumerate(category_positions):
    data_start = end
    if i + 1 < len(category_positions):
        data_end = category_positions[i+1][0]
    else:
        data_end = len(test_data)
    
    data_range = test_data[data_start:data_end]
    print(f"{cat:15s}: data_range = {repr(data_range):30s}", end="")
    
    # Extract all numbers
    all_numbers = re.findall(r"\d+", data_range)
    
    if len(all_numbers) == 1:
        # Single number - check if it could be split
        num_str = all_numbers[0]
        if len(num_str) == 4:
            # Likely format: XXYY (Items=XX, Quantity=YY)
            items = int(num_str[:2])
            qty = int(num_str[2:])
            print(f"-> Split '{num_str}' into Items={items}, Qty={qty}")
            summary_data[cat] = qty
        elif len(num_str) == 5:
            # Could be: XXYY or XXYYZ or XYYZZ
            # Heuristic: if even, split in half. If odd, last number is Qty
            mid = len(num_str) // 2
            items = int(num_str[:mid])
            qty = int(num_str[mid:])
            print(f"-> Split '{num_str}' (len={len(num_str)}) into Items={items}, Qty={qty}")
            summary_data[cat] = qty
        else:
            # Use last number as Quantity
            qty = int(num_str)
            print(f"-> Using as Qty: {qty}")
            summary_data[cat] = qty
    elif len(all_numbers) >= 2:
        # Multiple numbers - use last as Quantity
        qty = int(all_numbers[-1])
        print(f"-> Multiple numbers {all_numbers}, using last: {qty}")
        summary_data[cat] = qty
    else:
        print("-> NO DATA")

print(f"\n*** RESULT ***")
print(f"Summary: {summary_data}")
print()
print(f"Expected: {{'BMC': 68, 'CPU': 68, 'MEMORY': 274, 'POWER_STRIPS': 2, 'SERVER': 68, 'STORAGE_ARRAY': 17, 'SWITCH': 1}}")
print(f"\nMatches:")
expected = {'BMC': 68, 'CPU': 68, 'MEMORY': 274, 'POWER_STRIPS': 2, 'SERVER': 68, 'STORAGE_ARRAY': 17, 'SWITCH': 1}
for cat, exp_qty in expected.items():
    got_qty = summary_data.get(cat)
    match = "✓" if got_qty == exp_qty else "✗"
    print(f"  {match} {cat:15s}: expected {exp_qty:3d}, got {got_qty}")
