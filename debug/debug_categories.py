import re

summary_block = "CategoryItemsQuantityBMC6868CPU6868MEMORY70274POWER_STRIPS22SERVER6868STORAGE_ARRAY1717SWITCH11"

valid_categories = {
    "CHASSIS", "HBA", "MEMORY", "MODULES", "SSD", "SWITCH", "UPS", "SCRAP",
    "CPU", "CPU_COOLER", "FAN", "POWER_SUPPLY", "PDU", "NIC", "RAID_CONTROLLER",
    "STORAGE_DRIVE", "HDD", "NVME", "GPU", "TPU", "FPGA", "KVM", "BATTERY",
    "BATTERY_MODULE", "CONTROLLER", "NETWORK_SWITCH", "TRANSCEIVER", "SFP", "QSFP",
    "CABLES", "RAILS", "MOUNTING_KIT", "FAN_MODULE", "BLADE", "BLADE_SERVER",
    "RACK_UNIT", "PATCH_PANEL", "BMC", "MANAGEMENT_MODULE", "CONSOLE_SERVER",
    "TAPE_LIBRARY", "TAPE_LIB", "JBOD", "EXPANSION_CARD", "OPTICAL_TRANSCEIVER"
}

# Find all category positions
category_positions = []
for cat in valid_categories:
    for match in re.finditer(cat, summary_block, re.IGNORECASE):
        category_positions.append((match.start(), match.end(), cat))

# Sort by start position
category_positions.sort()

print(f"Found {len(category_positions)} category matches:")
for start, end, cat in category_positions:
    print(f"  {start:2d}-{end:2d}: {cat:20s} -> data after: {repr(summary_block[end:end+10])}")
