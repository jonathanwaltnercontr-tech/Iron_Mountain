import re

summary_block = "CategoryItemsQuantityBMC6868CPU6868MEMORY70274POWER_STRIPS22SERVER6868STORAGE_ARRAY1717SWITCH11"

print(f"Full summary block ({len(summary_block)} chars):")
print(f"{repr(summary_block)}\n")

print("Character positions:")
for i in range(0, len(summary_block), 10):
    print(f"  {i:2d}-{i+10:2d}: {repr(summary_block[i:i+10])}")

print("\n\nSearching for specific categories:")
target_cats = ["POWER_STRIPS", "SERVER", "STORAGE_ARRAY", "POWER_SUPPLY", "STORAGE_DRIVE"]

for cat in target_cats:
    matches = list(re.finditer(cat, summary_block, re.IGNORECASE))
    if matches:
        for m in matches:
            print(f"{cat:20s} found at {m.start():2d}-{m.end():2d}: {repr(summary_block[m.start():m.end()])}")
    else:
        print(f"{cat:20s} NOT FOUND")
