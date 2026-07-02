import re

test_data = "CategoryItemsQuantityBMC6868CPU6868MEMORY70274POWER_STRIPS22SERVER6868STORAGE_ARRAY1717SWITCH11"

print("=== CORRECT PARSING BY CATEGORY BOUNDARIES ===\n")

# Categories to search for (just the ones mentioned)
target_cats = ["BMC", "CPU", "MEMORY", "POWER_STRIPS", "SERVER", "STORAGE_ARRAY", "SWITCH"]

# Find positions of all categories
category_positions = []
for cat in target_cats:
    match = re.search(cat, test_data, re.IGNORECASE)
    if match:
        category_positions.append((match.start(), match.end(), cat))

# Sort by start position
category_positions.sort()

print(f"Categories found in order:")
for start, end, cat in category_positions:
    print(f"  {cat:15s} at position {start:2d}-{end:2d}")

print()

# Parse data between categories
summary_data = {}
for i, (start, end, cat) in enumerate(category_positions):
    # Data starts after the category name
    data_start = end
    
    # Data ends at the start of the next category name (or end of string)
    if i + 1 < len(category_positions):
        data_end = category_positions[i+1][0]
    else:
        data_end = len(test_data)
    
    data_range = test_data[data_start:data_end]
    print(f"{cat:15s}: data_range = {repr(data_range):30s}", end="")
    
    # Extract all numbers
    all_numbers = re.findall(r"\d+", data_range)
    if all_numbers:
        qty = int(all_numbers[-1])  # Last number is quantity
        summary_data[cat] = qty
        print(f"-> {qty}")
    else:
        print("-> NO DATA")

print(f"\n*** RESULT ***")
print(f"Summary: {summary_data}")
print()
print(f"Expected: {{'BMC': 68, 'CPU': 68, 'MEMORY': 274, 'POWER_STRIPS': 22, 'SERVER': 68, 'STORAGE_ARRAY': 17, 'SWITCH': 11}}")
print(f"Got correct CPU? {summary_data.get('CPU') == 68}")
