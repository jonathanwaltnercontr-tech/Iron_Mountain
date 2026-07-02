import re

test_data = "CategoryItemsQuantityBMC6868CPU6868MEMORY70274POWER_STRIPS22SERVER6868STORAGE_ARRAY1717SWITCH11"

# Print each character position  
for i, c in enumerate(test_data):
    print(f"{i:3d}: {c}", end="  ")
    if (i+1) % 15 == 0:
        print()

print("\n")

# Check specific positions
print(f"Position 21-24: {test_data[21:24]}")  # BMC
print(f"Position 28-31: {test_data[28:31]}")  # CPU
print(f"Position 35-41: {test_data[35:41]}")  # MEMORY
print(f"Position 41-52: {test_data[41:52]}")  # Should be POWER_STRIPS?
print(f"Position 42-54: {test_data[42:54]}")  # POWER_STRIPS
print(f"Position 55-61: {test_data[55:61]}")  # SERVER
print(f"Position 62-76: {test_data[62:76]}")  # STORAGE_ARRAY
print(f"Position 78-84: {test_data[78:84]}")  # SWITCH

# Now try finding them
print("\n=== Finding categories ===")
for cat in ["BMC", "CPU", "MEMORY", "POWER_STRIPS", "SERVER", "STORAGE_ARRAY", "SWITCH"]:
    matches = list(re.finditer(cat, test_data, re.IGNORECASE))
    print(f"{cat:15s}: {matches}")
    if matches:
        for m in matches:
            print(f"   Position {m.start()}-{m.end()}: {repr(test_data[m.start():m.end()])}")
