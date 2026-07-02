import re

# Your actual data
test_data = """Child Item SummaryCategoryItemsQuantityBMC6868CPU6868MEMORY70274POWER_STRIPS22SERVER6868STORAGE_ARRAY1717SWITCH11Serial Number"""

print("=== APPROACH: Parse by finding category positions ===")
summary_section = test_data[test_data.find("Child Item Summary")+len("Child Item Summary"):test_data.find("Serial Number")]

print(f"Summary section: {repr(summary_section)}\n")

valid_categories = ["CHASSIS", "HBA", "MEMORY", "MODULES", "SSD", "SWITCH", "UPS", "SCRAP",
    "CPU", "CPU_COOLER", "FAN", "POWER_SUPPLY", "PDU", "NIC", "RAID_CONTROLLER",
    "STORAGE_DRIVE", "HDD", "NVME", "GPU", "TPU", "FPGA", "KVM", "BATTERY",
    "BATTERY_MODULE", "CONTROLLER", "NETWORK_SWITCH", "TRANSCEIVER", "SFP", "QSFP",
    "CABLES", "RAILS", "MOUNTING_KIT", "FAN_MODULE", "BLADE", "BLADE_SERVER",
    "RACK_UNIT", "PATCH_PANEL", "BMC", "MANAGEMENT_MODULE", "CONSOLE_SERVER",
    "TAPE_LIBRARY", "TAPE_LIB", "JBOD", "EXPANSION_CARD", "OPTICAL_TRANSCEIVER"]

# Find all category positions
category_matches = []
for cat in valid_categories:
    pattern = rf"{cat}"  # No word boundaries - just match the text
    for match in re.finditer(pattern, summary_section, re.IGNORECASE):
        category_matches.append((match.start(), match.end(), cat))

# Sort by position
category_matches.sort()

print(f"Found categories at positions: {category_matches}\n")

# Extract data between categories
summary_data = {}
for i, (start, end, cat) in enumerate(category_matches):
    # Find the end of data for this category (start of next category or end of text)
    if i + 1 < len(category_matches):
        data_end = category_matches[i+1][0]
    else:
        data_end = len(summary_section)
    
    # Extract digit data between this category name and next category
    data_range = summary_section[end:data_end]
    print(f"{cat}: data_range = {repr(data_range)}")
    
    # Find all numbers in this range
    all_numbers = re.findall(r"\d+", data_range)
    if all_numbers:
        qty = int(all_numbers[-1])  # Take last number
        summary_data[cat] = qty
        print(f"  -> Taking last number: {qty}\n")

print(f"\nFinal summary: {summary_data}")
