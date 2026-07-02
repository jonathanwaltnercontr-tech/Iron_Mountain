"""
Debug version that shows exactly what's being matched
"""
import sys
sys.path.insert(0, r'C:\Users\jwaltner.ctr\Documents\GitHub\Iron_Mountain')

import re

# Exact code from app.py
user_data = """DetailsAttributesAdditional Serial/AssetHistoryJobAttachmentsTerawareFamily TreeCommentsDBD Count: 498Child Item SummaryCategoryItemsQuantityBMC6868CPU6868MEMORY70274POWER_STRIPS22SERVER6868STORAGE_ARRAY1717SWITCH11Serial NumberItem IdCategoryModelAsset TagStatusQuanity6012271-A64490016RACKV2 OPEN RACK6012271RECYCLED1"""

valid_categories = {
    "CHASSIS", "HBA", "MEMORY", "MODULES", "SSD", "SWITCH", "UPS", "SCRAP",
    "CPU", "CPU_COOLER", "FAN", "POWER_SUPPLY", "PDU", "NIC", "RAID_CONTROLLER",
    "STORAGE_DRIVE", "HDD", "NVME", "GPU", "TPU", "FPGA", "KVM", "BATTERY",
    "BATTERY_MODULE", "CONTROLLER", "NETWORK_SWITCH", "TRANSCEIVER", "SFP", "QSFP",
    "CABLES", "RAILS", "MOUNTING_KIT", "FAN_MODULE", "BLADE", "BLADE_SERVER",
    "RACK_UNIT", "PATCH_PANEL", "BMC", "MANAGEMENT_MODULE", "CONSOLE_SERVER",
    "TAPE_LIBRARY", "TAPE_LIB", "JBOD", "EXPANSION_CARD", "OPTICAL_TRANSCEIVER",
    "POWER_STRIPS", "SERVER", "STORAGE_ARRAY"  # Make sure these are in the set
}

summary_section_match = re.search(r"Child Item Summary(.*?)(?:Serial Number|$)", user_data, re.IGNORECASE | re.DOTALL)
summary_block = summary_section_match.group(1)

print(f"Summary block:\n{repr(summary_block)}\n")

# Find all category positions (exact code from app.py)
category_positions = []
for cat in valid_categories:
    for match in re.finditer(cat, summary_block, re.IGNORECASE):
        category_positions.append((match.start(), match.end(), cat))

# Sort by start position
category_positions.sort()

print(f"Found {len(category_positions)} matches:")
for start, end, cat in sorted(category_positions):
    print(f"  {start:2d}-{end:2d}: {cat:20s}")

print("\n\nExpected categories in data:")
for cat in ["BMC", "CPU", "MEMORY", "POWER_STRIPS", "SERVER", "STORAGE_ARRAY", "SWITCH"]:
    if any(c == cat for _, _, c in category_positions):
        print(f"  ✓ {cat}")
    else:
        print(f"  ✗ {cat} MISSING!")
