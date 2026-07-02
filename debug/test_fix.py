import re

# Your actual data
test_data = """DetailsAttributesAdditional Serial/AssetHistoryJobAttachmentsTerawareFamily TreeCommentsDBD Count: 498Child Item SummaryCategoryItemsQuantityBMC6868CPU6868MEMORY70274POWER_STRIPS22SERVER6868STORAGE_ARRAY1717SWITCH11Serial NumberItem IdCategoryModelAsset TagStatusQuanity6012271-A64490016RACKV2 OPEN RACK6012271RECYCLED1"""

print("=== NEW FIXED APPROACH ===")
summary_section_match = re.search(r"Child Item Summary(.*?)(?:Serial Number|$)", test_data, re.IGNORECASE | re.DOTALL)

if summary_section_match:
    summary_block = summary_section_match.group(1)
    print(f"Summary block extracted:\n{repr(summary_block[:100])}")
    
    # Test CPU extraction
    target = "CPU"
    
    # Try pattern with whitespace first
    cat_match = re.search(rf"{target}\s+(\d+)\s+(\d+)", summary_block, re.IGNORECASE)
    if cat_match:
        print(f"\nWhitespace pattern matched: {cat_match.group(0)}")
        print(f"Group 1: {cat_match.group(1)}, Group 2: {cat_match.group(2)}")
    else:
        print(f"\nWhitespace pattern didn't match, trying squished format...")
        # Try squished pattern
        cat_match = re.search(rf"{target}(\d{{1,3}})(\d{{1,3}})", summary_block, re.IGNORECASE)
        if cat_match:
            print(f"Squished pattern matched: {cat_match.group(0)}")
            print(f"Group 1: {cat_match.group(1)}, Group 2: {cat_match.group(2)}")
            qty_str = cat_match.group(2) if cat_match.group(2) else cat_match.group(1)
            print(f"Final quantity: {qty_str}")
else:
    print("Summary section not found!")

print("\n=== TESTING ALL CATEGORIES ===")
valid_categories = ["BMC", "CPU", "MEMORY", "POWER_STRIPS", "SERVER", "STORAGE_ARRAY", "SWITCH"]

if summary_section_match:
    summary_block = summary_section_match.group(1)
    summary_data = {}
    
    for target in valid_categories:
        # Try pattern with whitespace first
        cat_match = re.search(rf"{target}\s+(\d+)\s+(\d+)", summary_block, re.IGNORECASE)
        
        if not cat_match:
            # Try squished pattern
            cat_match = re.search(rf"{target}(\d{{1,3}})(\d{{1,3}})", summary_block, re.IGNORECASE)
        
        if cat_match:
            qty_str = cat_match.group(2) if cat_match.group(2) else cat_match.group(1)
            summary_data[target] = int(qty_str)
            print(f"{target}: {qty_str}")
    
    print(f"\nFinal summary: {summary_data}")
