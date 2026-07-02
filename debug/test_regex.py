import re

# Your squished data
test_data = """Child Item SummaryCategoryItemsQuantityBMC6868CPU6868MEMORY70274POWER_STRIPS22SERVER6868STORAGE_ARRAY1717SWITCH11Serial Number"""

print("=== TESTING CURRENT REGEX ===")
# Current regex
pattern = r"CPU\s*(\d+)\s*(\d*)"
match = re.search(pattern, test_data, re.IGNORECASE)

if match:
    print(f"Match found: {match.group(0)}")
    print(f"Group 1: {match.group(1)}")
    print(f"Group 2: {match.group(2)}")
    
    # Current logic
    qty_str = match.group(2) if match.group(2) else match.group(1)
    print(f"Result quantity: {qty_str}")
else:
    print("No match found")

print("\n=== TESTING FIXED REGEX ===")
# Fixed pattern - limit digit groups to 2-3 digits (reasonable for quantities)
pattern_fixed = r"CPU\s*(\d{1,3})\s*(\d{1,3})"
match_fixed = re.search(pattern_fixed, test_data, re.IGNORECASE)

if match_fixed:
    print(f"Match found: {match_fixed.group(0)}")
    print(f"Group 1: {match_fixed.group(1)}")
    print(f"Group 2: {match_fixed.group(2)}")
    qty_str = match_fixed.group(2) if match_fixed.group(2) else match_fixed.group(1)
    print(f"Result quantity: {qty_str}")
else:
    print("No match found")
