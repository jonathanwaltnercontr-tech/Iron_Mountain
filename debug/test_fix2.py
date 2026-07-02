import re

# Your actual data
test_data = """DetailsAttributesAdditional Serial/AssetHistoryJobAttachmentsTerawareFamily TreeCommentsDBD Count: 498Child Item SummaryCategoryItemsQuantityBMC6868CPU6868MEMORY70274POWER_STRIPS22SERVER6868STORAGE_ARRAY1717SWITCH11Serial NumberItem IdCategoryModelAsset TagStatusQuanity6012271-A64490016RACKV2 OPEN RACK6012271RECYCLED1"""

print("=== FIXED PATTERN WITH LOOKAHEAD ===")
summary_section_match = re.search(r"Child Item Summary(.*?)(?:Serial Number|$)", test_data, re.IGNORECASE | re.DOTALL)

if summary_section_match:
    summary_block = summary_section_match.group(1)
    print(f"Summary block:\n{repr(summary_block[:100])}\n")
    
    valid_categories = ["CHASSIS", "HBA", "MEMORY", "MODULES", "SSD", "SWITCH", "UPS", "SCRAP",
        "CPU", "CPU_COOLER", "FAN", "POWER_SUPPLY", "PDU", "NIC", "RAID_CONTROLLER",
        "STORAGE_DRIVE", "HDD", "NVME", "GPU", "TPU", "FPGA", "KVM", "BATTERY",
        "BATTERY_MODULE", "CONTROLLER", "NETWORK_SWITCH", "TRANSCEIVER", "SFP", "QSFP",
        "CABLES", "RAILS", "MOUNTING_KIT", "FAN_MODULE", "BLADE", "BLADE_SERVER",
        "RACK_UNIT", "PATCH_PANEL", "BMC", "MANAGEMENT_MODULE", "CONSOLE_SERVER",
        "TAPE_LIBRARY", "TAPE_LIB", "JBOD", "EXPANSION_CARD", "OPTICAL_TRANSCEIVER"]
    
    summary_data = {}
    sorted_cats = sorted(valid_categories, key=len, reverse=True)
    
    for target in ["BMC", "CPU", "MEMORY", "POWER_STRIPS", "SERVER", "STORAGE_ARRAY", "SWITCH"]:
        qty_str = None
        
        # Strategy 1: Normal whitespace pattern
        cat_match = re.search(rf"{target}\s+(\d+)\s+(\d+)", summary_block, re.IGNORECASE)
        if cat_match:
            qty_str = cat_match.group(2)
            print(f"{target}: Found with whitespace pattern, qty={qty_str}")
        else:
            # Strategy 2: Squished pattern with non-greedy and lookahead
            cat_pattern = rf"{target}([0-9]+?)(?=(?:{'|'.join(re.escape(c) for c in sorted_cats if c != target)})|\Z)"
            cat_match = re.search(cat_pattern, summary_block, re.IGNORECASE)
            
            if cat_match:
                digit_sequence = cat_match.group(1)
                print(f"{target}: Found squished, digit_sequence='{digit_sequence}'")
                all_numbers = re.findall(r"\d+", digit_sequence)
                print(f"  All numbers in sequence: {all_numbers}")
                if all_numbers:
                    qty_str = all_numbers[-1]
                    print(f"  Taking last: {qty_str}")
        
        if qty_str:
            summary_data[target] = int(qty_str)
    
    print(f"\nFinal summary: {summary_data}")
else:
    print("Summary section not found!")
