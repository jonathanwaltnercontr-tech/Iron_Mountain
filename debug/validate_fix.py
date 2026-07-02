"""
Validation test for the squished data format parsing fix.
This test uses the exact data provided by the user.
"""
import sys
sys.path.insert(0, r'C:\Users\jwaltner.ctr\Documents\GitHub\Iron_Mountain')

from src.scripts.app import parse_clipboard_data
from unittest.mock import patch
import json

# User's actual data
user_data = """DetailsAttributesAdditional Serial/AssetHistoryJobAttachmentsTerawareFamily TreeCommentsDBD Count: 498Child Item SummaryCategoryItemsQuantityBMC6868CPU6868MEMORY70274POWER_STRIPS22SERVER6868STORAGE_ARRAY1717SWITCH11Serial NumberItem IdCategoryModelAsset TagStatusQuanity6012271-A64490016RACKV2 OPEN RACK6012271RECYCLED1"""

print("=" * 70)
print("VALIDATION TEST: Squished Data Format Parsing")
print("=" * 70)
print()
print("Input Data (Child Item Summary section):")
print("CategoryItemsQuantityBMC6868CPU6868MEMORY70274POWER_STRIPS22SERVER6868STORAGE_ARRAY1717SWITCH11")
print()
print("Expected Results:")
expected = {
    'BMC': 68,
    'CPU': 68,
    'MEMORY': 274,
    'POWER_STRIPS': 2,
    'SERVER': 68,
    'STORAGE_ARRAY': 17,
    'SWITCH': 1
}
for cat, qty in expected.items():
    print(f"  {cat:20s}: {qty}")

print()
print("-" * 70)
print()

# Mock the clipboard and capture results
captured_data = {}

def mock_upload(summary_data, rack_model):
    """Mock to capture the parsed data"""
    captured_data['summary'] = summary_data
    captured_data['rack_model'] = rack_model

with patch('pyperclip.paste', return_value=user_data):
    with patch('src.scripts.app.upload_to_google_sheets', side_effect=mock_upload):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()

print("RESULTS:")
print()
print(f"Rack Model: {captured_data.get('rack_model', 'NOT CAPTURED')}")
print()
print("Parsed Categories:")

all_correct = True
for cat, expected_qty in expected.items():
    actual_qty = captured_data.get('summary', {}).get(cat)
    status = "✓ PASS" if actual_qty == expected_qty else "✗ FAIL"
    
    if actual_qty != expected_qty:
        all_correct = False
        
    print(f"  {status} {cat:20s}: expected {expected_qty:3d}, got {actual_qty}")

print()
print("=" * 70)
if all_correct:
    print("✓ ALL TESTS PASSED - Squished data parsing is working correctly!")
    print("  CPU quantity correctly captured as 68 (not 6868)")
else:
    print("✗ SOME TESTS FAILED - Check parsing logic")
print("=" * 70)
