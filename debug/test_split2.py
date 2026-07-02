import re

test_data = "CategoryItemsQuantityBMC6868CPU6868MEMORY70274POWER_STRIPS22SERVER6868STORAGE_ARRAY1717SWITCH11"

print("=== REFINED SPLIT LOGIC ===\n")

target_cats = ["BMC", "CPU", "MEMORY", "POWER_STRIPS", "SERVER", "STORAGE_ARRAY", "SWITCH"]

# Find positions
category_positions = []
for cat in target_cats:
    match = re.search(cat, test_data, re.IGNORECASE)
    if match:
        category_positions.append((match.start(), match.end(), cat))

category_positions.sort()

def parse_quantity(digit_string):
    """Extract quantity from digit string.
    
    Assumes format: <ITEMS><QUANTITY>
    Where ITEMS is 1-2 digits, QUANTITY is the rest.
    """
    if len(digit_string) <= 2:
        # For 1-2 digits: split in half (or just 1 digit for quantity if len=1)
        split = len(digit_string) // 2
        if split == 0:
            return int(digit_string)
        else:
            return int(digit_string[split:])
    else:
        # For 3+ digits: items get 2 digits max, rest is quantity
        # But try to balance - if 4 digits, split 50/50; if 5, split 2/3
        # Simple rule: Items get min(2, ceil(len/2)) digits
        split = min(2, (len(digit_string) + 1) // 2)
        return int(digit_string[split:])

summary_data = {}
for i, (start, end, cat) in enumerate(category_positions):
    data_start = end
    if i + 1 < len(category_positions):
        data_end = category_positions[i+1][0]
    else:
        data_end = len(test_data)
    
    data_range = test_data[data_start:data_end]
    all_numbers = re.findall(r"\d+", data_range)
    
    print(f"{cat:15s}: data_range = {repr(data_range):30s}", end="")
    
    if all_numbers:
        num_str = all_numbers[0]  # Use first (and usually only) number
        qty = parse_quantity(num_str)
        print(f"-> parse_quantity('{num_str}') = {qty}")
        summary_data[cat] = qty
    else:
        print("-> NO DATA")

print(f"\n*** RESULT ***")
print(f"Summary: {summary_data}")
print()
print(f"Expected: {{'BMC': 68, 'CPU': 68, 'MEMORY': 274, 'POWER_STRIPS': 2, 'SERVER': 68, 'STORAGE_ARRAY': 17, 'SWITCH': 1}}")
print(f"\nMatches:")
expected = {'BMC': 68, 'CPU': 68, 'MEMORY': 274, 'POWER_STRIPS': 2, 'SERVER': 68, 'STORAGE_ARRAY': 17, 'SWITCH': 1}
all_match = True
for cat in target_cats:
    exp_qty = expected.get(cat)
    got_qty = summary_data.get(cat)
    match = "✓" if got_qty == exp_qty else "✗"
    if got_qty != exp_qty:
        all_match = False
    print(f"  {match} {cat:15s}: expected {exp_qty}, got {got_qty}")

print(f"\nAll correct? {all_match}")
