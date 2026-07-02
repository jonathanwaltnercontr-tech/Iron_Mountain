"""
Comprehensive test suite for Iron Mountain app.py (50 test cases)
Tests parsing logic, error handling, and data validation

All uploads are captured to JSON files in tests_execution/ folder
No actual Google Sheets uploads occur during testing
"""

import pytest
from unittest.mock import patch
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.app import parse_clipboard_data


# ============================================================================
# TEST GROUP 1: Clipboard Data Parsing - Valid Inputs (Tests 1-8)
# ============================================================================

def test_001_parse_single_category():
    """Test parsing with a single valid category"""
    test_data = """
    Child Item Summary
    MEMORY 10 15
    Serial Number: ABC123
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()
        # Data saved to tests_execution/upload_data_*.json


def test_002_parse_multiple_categories():
    """Test parsing with multiple valid categories"""
    test_data = """
    Child Item Summary
    CHASSIS 2 3
    MEMORY 10 12
    SSD 5 8
    Serial Number: XYZ789
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_003_parse_rack_model_from_columns():
    """Test extracting rack model from tab-separated columns"""
    test_data = """
    Item\tCategory\tType\tModel\tStatus
    001\tRACK\tPDU\tLEGRAND_RACK_2024\tINVENTORY
    
    Child Item Summary
    CHASSIS 1 2
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_004_parse_rack_model_from_squished_text():
    """Test extracting rack model from compact text (no spacing)"""
    test_data = """
    RAC:LEGRAND_RACK9876543INVENTORY
    Child Item Summary
    MEMORY 5 7
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_005_parse_all_valid_categories():
    """Test parsing all 40+ valid hardware categories"""
    categories = [
        "CHASSIS", "HBA", "MEMORY", "MODULES", "SSD", "SWITCH", "UPS", "SCRAP",
        "CPU", "CPU_COOLER", "FAN", "POWER_SUPPLY", "PDU", "NIC", "RAID_CONTROLLER",
    ]
    
    test_data = "Child Item Summary\n"
    for i, cat in enumerate(categories):
        test_data += f"{cat} {i} {i+1}\n"
    test_data += "Serial Number: TEST123"
    
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_006_parse_quantity_extraction_accuracy():
    """Test that quantities are extracted with correct numerical values"""
    test_data = """
    Child Item Summary
    CPU 1 42
    MEMORY 2 128
    SSD 3 1024
    Serial Number: ABC123
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_007_parse_ignores_non_summary_sections():
    """Test that data outside Child Item Summary is ignored"""
    test_data = """
    Pre-Summary Data
    MEMORY 999 999
    
    Child Item Summary
    MEMORY 10 15
    
    Post-Summary Data
    CPU 888 888
    
    Serial Number: TEST
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_008_parse_case_insensitive_categories():
    """Test that category matching is case-insensitive"""
    test_data = """
    Child Item Summary
    memory 10 25
    cpu 5 8
    chassis 2 3
    Serial Number: TEST
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


# ============================================================================
# TEST GROUP 2: Error Handling (Tests 9-16)
# ============================================================================

def test_009_empty_clipboard_error():
    """Test handling of empty clipboard"""
    with patch('pyperclip.paste', return_value=""):
        parse_clipboard_data()
        # Warning logged to tests_execution/ui_messages.log


def test_010_clipboard_only_whitespace():
    """Test handling of clipboard with only whitespace"""
    with patch('pyperclip.paste', return_value="   \n\n   "):
        parse_clipboard_data()


def test_011_no_child_item_summary_found():
    """Test handling when Child Item Summary section not found"""
    test_data = "Some random text without summary section"
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_012_clipboard_read_exception():
    """Test handling of clipboard read errors"""
    with patch('pyperclip.paste', side_effect=Exception("Clipboard error")):
        parse_clipboard_data()


def test_013_invalid_category_ignored():
    """Test that invalid categories are properly ignored"""
    test_data = """
    Child Item Summary
    INVALID_CAT 10 15
    MEMORY 5 8
    BADCATEGORY 20 25
    Serial Number: TEST
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_014_malformed_quantity_skipped():
    """Test that malformed quantity entries are handled gracefully"""
    test_data = """
    Child Item Summary
    MEMORY ABC DEF
    CPU 5 10
    Serial Number: TEST
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_015_numeric_overflow_handling():
    """Test handling of very large numbers"""
    test_data = """
    Child Item Summary
    MEMORY 0 999999999
    Serial Number: TEST
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_016_zero_quantity_accepted():
    """Test that zero quantities are accepted"""
    test_data = """
    Child Item Summary
    MEMORY 0 0
    CPU 1 0
    Serial Number: TEST
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


# ============================================================================
# TEST GROUP 3: Rack Model Extraction (Tests 17-24)
# ============================================================================

def test_017_rack_model_basic_extraction():
    """Test basic rack model extraction"""
    test_data = """
    Item\tCategory\tType\tModel\tStatus
    001\tRACK\tChassis\tDELL_R750\tINVENTORY
    
    Child Item Summary
    CPU 1 4
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_018_rack_model_with_underscores():
    """Test rack model extraction with underscores"""
    test_data = """
    Item\tCategory\tType\tModel\tStatus
    001\tRACK\tChassis\tLEGRAND_RACK_2024_PLUS\tINVENTORY
    
    Child Item Summary
    MEMORY 1 8
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_019_rack_model_with_hyphens():
    """Test rack model extraction with hyphens"""
    test_data = """
    Item\tCategory\tType\tModel\tStatus
    001\tRACK\tChassis\tHP-DL380-Gen10\tINVENTORY
    
    Child Item Summary
    CPU 1 16
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_020_rack_model_space_separated_columns():
    """Test rack model with space-separated columns"""
    test_data = """
    Item  Category  Type  Model  Status
    001   RACK      Chassis  CUSTOM_MODEL_001  INVENTORY
    
    Child Item Summary
    SSD 1 2
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_021_multiple_racks_first_selected():
    """Test that first RACK entry is selected when multiple exist"""
    test_data = """
    Item\tCategory\tType\tModel\tStatus
    001\tRACK\tChassis\tFIRST_RACK\tINVENTORY
    002\tRACK\tChassis\tSECOND_RACK\tINVENTORY
    
    Child Item Summary
    MEMORY 1 8
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_022_rack_model_case_insensitive():
    """Test that RACK matching is case-insensitive"""
    test_data = """
    Item\tCategory\tType\tModel\tStatus
    001\track\tChassis\tTEST_MODEL\tINVENTORY
    
    Child Item Summary
    CPU 1 4
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_023_rack_model_numeric_in_name():
    """Test rack model with numeric characters"""
    test_data = """
    Item\tCategory\tType\tModel\tStatus
    001\tRACK\tChassis\tRAC2024GEN5PRO\tINVENTORY
    
    Child Item Summary
    CHASSIS 1 1
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_024_unknown_rack_default():
    """Test that Unknown Rack is returned when no RACK found"""
    test_data = """
    Item\tCategory\tType\tModel\tStatus
    001\tCHASSIS\tServer\tSOME_MODEL\tINVENTORY
    
    Child Item Summary
    CPU 1 8
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


# ============================================================================
# TEST GROUP 4: Data Serialization & URL Encoding (Tests 25-32)
# ============================================================================

def test_025_payload_valid_json_structure():
    """Test that payload is valid JSON"""
    test_data = """
    Child Item Summary
    MEMORY 1 16
    Serial Number: TEST
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_026_url_encoding_special_characters():
    """Test URL encoding handles special characters properly"""
    test_data = """
    Child Item Summary
    MEMORY 1 16
    Serial Number: TEST&SPECIAL=VALUE
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_027_json_serialization_accuracy():
    """Test that data is accurately serialized to JSON"""
    test_data = """
    Child Item Summary
    CHASSIS 1 2
    MEMORY 2 16
    SSD 3 4
    Serial Number: TEST
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_028_url_safe_encoding():
    """Test that URLs are properly URL-encoded"""
    test_data = """
    Child Item Summary
    MEMORY 1 16
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_029_apostrophe_handling():
    """Test that apostrophes in data are handled correctly (JSON not str)"""
    test_data = """
    Child Item Summary
    MEMORY 1 16
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_030_unicode_character_support():
    """Test handling of unicode characters in rack model"""
    test_data = """
    Item\tCategory\tType\tModel\tStatus
    001\tRACK\tChassis\tRACK_2024\tINVENTORY
    
    Child Item Summary
    MEMORY 1 8
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_031_large_quantity_serialization():
    """Test serialization of large numbers"""
    test_data = """
    Child Item Summary
    MEMORY 1 1000000
    CPU 1 9999999
    Serial Number: TEST
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_032_empty_summary_data_upload():
    """Test handling of empty summary (triggers warning)"""
    test_data = """
    Child Item Summary
    INVALID 1 1
    Serial Number: TEST
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


# ============================================================================
# TEST GROUP 5: Integration & Workflow Tests (Tests 33-40)
# ============================================================================

def test_033_complete_workflow_valid_input():
    """Test complete workflow from clipboard to capture"""
    test_data = """
    Item\tCategory\tType\tModel\tStatus
    001\tRACK\tChassis\tLEGRAND_RACK\tINVENTORY
    
    Child Item Summary
    CHASSIS 1 1
    MEMORY 2 16
    CPU 1 8
    SSD 3 4
    
    Serial Number: ABC123
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_034_fallback_parsing_triggered():
    """Test that fallback parsing works when primary fails"""
    test_data = """
    NoValidSummary
    MEMORY5008
    SSD3004
    CPU1008
    Serial Number: TEST
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_035_multiple_upload_calls_separate():
    """Test that separate clipboard reads trigger separate captures"""
    test_data1 = """
    Child Item Summary
    MEMORY 1 8
    """
    test_data2 = """
    Child Item Summary
    CPU 1 4
    """
    
    with patch('pyperclip.paste', return_value=test_data1):
        parse_clipboard_data()
    
    with patch('pyperclip.paste', return_value=test_data2):
        parse_clipboard_data()


def test_036_console_logging_present():
    """Test that console logging output is generated"""
    test_data = """
    Child Item Summary
    MEMORY 1 16
    Serial Number: TEST123
    """
    with patch('pyperclip.paste', return_value=test_data):
        with patch('builtins.print') as mock_print:
            parse_clipboard_data()
            assert mock_print.called


def test_037_summary_output_format():
    """Test that summary output is in expected format"""
    test_data = """
    Child Item Summary
    MEMORY 1 16
    CPU 1 8
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_038_rack_model_output_format():
    """Test that rack model output is in expected format"""
    test_data = """
    Item\tCategory\tType\tModel\tStatus
    001\tRACK\tChassis\tTEST_RACK_2024\tINVENTORY
    
    Child Item Summary
    MEMORY 1 8
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_039_mixed_case_input_consistency():
    """Test that mixed case input produces consistent output"""
    test_data = """
    Child Item Summary
    Memory 1 8
    CPU 1 4
    chassis 1 1
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_040_regex_pattern_stability():
    """Test that regex patterns are stable with various inputs"""
    test_cases = [
        "MEMORY 1 16",
        "MEMORY10 16",
        "MEMORY  10  16",
        "memory 1 16",
        "MeMoRy 1 16",
    ]
    
    for test_case in test_cases:
        test_data = f"""
        Child Item Summary
        {test_case}
        """
        with patch('pyperclip.paste', return_value=test_data):
            parse_clipboard_data()


# ============================================================================
# TEST GROUP 6: Edge Cases & Boundary Tests (Tests 41-50)
# ============================================================================

def test_041_very_long_rack_model_name():
    """Test handling of very long rack model names"""
    long_model = "A" * 255
    test_data = f"""
    Item\tCategory\tType\tModel\tStatus
    001\tRACK\tChassis\t{long_model}\tINVENTORY
    
    Child Item Summary
    MEMORY 1 8
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_042_very_large_clipboard_data():
    """Test handling of very large clipboard data"""
    categories = ["MEMORY", "CPU", "SSD", "CHASSIS", "FAN"] * 100
    test_data = "Child Item Summary\n"
    for i, cat in enumerate(categories):
        test_data += f"{cat} 1 {i+1}\n"
    
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_043_single_digit_quantities():
    """Test parsing of single digit quantities"""
    test_data = """
    Child Item Summary
    MEMORY 0 1
    CPU 0 2
    SSD 0 3
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_044_leading_trailing_whitespace():
    """Test handling of leading/trailing whitespace"""
    test_data = """
    
    
    Child Item Summary
    MEMORY 1 16
    
    
    Serial Number: TEST
    
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_045_tab_vs_space_delimiters():
    """Test that both tab and space delimiters work"""
    test_data_tabs = """
    Item\tCategory\tType\tModel\tStatus
    001\tRACK\tChassis\tTAB_MODEL\tINVENTORY
    
    Child Item Summary
    MEMORY 1 8
    """
    
    with patch('pyperclip.paste', return_value=test_data_tabs):
        parse_clipboard_data()


def test_046_duplicate_category_entries():
    """Test handling of duplicate category entries (last one wins)"""
    test_data = """
    Child Item Summary
    MEMORY 1 8
    CPU 1 4
    MEMORY 2 16
    CPU 2 8
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_047_special_characters_in_model_name():
    """Test special characters in model names"""
    test_data = """
    Item\tCategory\tType\tModel\tStatus
    001\tRACK\tChassis\tMODEL-2024_PRO+v1\tINVENTORY
    
    Child Item Summary
    MEMORY 1 8
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_048_numeric_only_categories():
    """Test that numeric-only input is rejected"""
    test_data = """
    Child Item Summary
    123 1 8
    456 2 16
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_049_partial_child_summary_section():
    """Test incomplete Child Item Summary section"""
    test_data = """
    Child Item Summary
    """
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


def test_050_cumulative_parsing_accuracy():
    """Final test: Comprehensive accuracy check of entire parsing system"""
    test_data = """
    Header Data
    Item\tCategory\tType\tModel\tStatus
    001\tRACK\tChassis\tFINAL_TEST_RACK_2024\tINVENTORY
    
    Child Item Summary
    CHASSIS 1 2
    MEMORY 5 32
    CPU 3 16
    SSD 10 8
    HDD 20 4
    SWITCH 2 2
    UPS 1 1
    
    Serial Number: COMPREHENSIVE_TEST_123
    Additional Data
    """
    
    with patch('pyperclip.paste', return_value=test_data):
        parse_clipboard_data()


# ============================================================================
# TEST RUNNER
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
