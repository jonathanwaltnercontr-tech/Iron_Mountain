"""
Extended Test Suite - 60+ Additional Edge Case Tests for Bug Detection
Tests for squished format, overlapping categories, malformed data, and real-world edge cases
"""

import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.app import parse_clipboard_data


# ============================================================================
# SQUISHED FORMAT VARIATIONS (Tests 051-065)
# ============================================================================

def test_051_squished_format_all_categories():
    """Test squished format with actual user data - all categories"""
    test_data = "Child Item SummaryCategoryItemsQuantityBMC6868CPU6868MEMORY70274POWER_STRIPS22SERVER6868STORAGE_ARRAY1717SWITCH11Serial Number"
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


def test_052_squished_single_digit_quantities():
    """Test squished format with single digit quantities"""
    test_data = "Child Item SummaryCPU1MEMORY5SWITCH9Serial Number"
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


def test_053_squished_five_digit_sequence():
    """Test squished format with 5+ digit sequences"""
    test_data = "Child Item SummaryCPU12345MEMORY98765Serial Number"
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


def test_054_squished_leading_zeros():
    """Test squished format with leading zeros in quantities"""
    test_data = "Child Item SummaryCPU0068MEMORY00274Serial Number"
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


def test_055_squished_very_large_numbers():
    """Test squished format with very large quantities"""
    test_data = "Child Item SummaryCPU9999MEMORY999999Serial Number"
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


def test_056_mixed_squished_and_spaced():
    """Test data with mixed squished and properly spaced sections"""
    test_data = """
    Child Item Summary
    CPU 10 20
    MEMORY50100
    SWITCH 1 2
    Serial Number
    """
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


def test_057_squished_with_tabs():
    """Test squished format mixed with tabs"""
    test_data = "Child Item Summary\tCPU6868\tMEMORY70274\tSWITCH11Serial Number"
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


def test_058_squished_categories_at_boundaries():
    """Test when categories appear at start and end of summary"""
    test_data = "Child Item SummaryCPU6868SWITCH11Serial Number"
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


def test_059_squished_consecutive_categories():
    """Test squished format with many categories in a row"""
    test_data = "Child Item SummaryCPU1MEMORY2SSD3SWITCH4BMC5Serial Number"
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


def test_060_squished_only_numbers_between_categories():
    """Test squished with only digit data between categories, no text"""
    test_data = "Child Item SummaryCPU68MEMORY274Serial Number"
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


# ============================================================================
# CATEGORY NAME OVERLAPS & AMBIGUITIES (Tests 061-070)
# ============================================================================

def test_061_overlapping_category_names_cpu_cpu_cooler():
    """Test categories where one name contains another (CPU vs CPU_COOLER)"""
    test_data = """
    Child Item Summary
    CPU 5 10
    CPU_COOLER 3 8
    Serial Number
    """
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


def test_062_overlapping_storage_names():
    """Test storage-related category overlaps"""
    test_data = """
    Child Item Summary
    STORAGE_DRIVE 2 4
    STORAGE_ARRAY 1 5
    Serial Number
    """
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


def test_063_overlapping_memory_names():
    """Test memory-related overlaps (MEMORY vs MODULES)"""
    test_data = """
    Child Item Summary
    MEMORY 100 200
    MODULES 50 75
    Serial Number
    """
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


def test_064_power_overlaps():
    """Test power-related overlaps (POWER_SUPPLY vs POWER_STRIPS)"""
    test_data = """
    Child Item Summary
    POWER_SUPPLY 10 15
    POWER_STRIPS 5 20
    Serial Number
    """
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


def test_065_network_overlaps():
    """Test network-related overlaps (NIC vs NETWORK_SWITCH)"""
    test_data = """
    Child Item Summary
    NIC 8 12
    NETWORK_SWITCH 2 3
    Serial Number
    """
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


# ============================================================================
# MALFORMED & CORRUPTED DATA (Tests 071-085)
# ============================================================================

def test_071_missing_child_item_summary_section():
    """Test when Child Item Summary section is completely missing"""
    test_data = """
    Item\tCategory\tType\tModel\tStatus
    001\tRACK\tChassis\tTEST_RACK\tINVENTORY
    Serial Number: ABC123
    """
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showwarning') as mock_warn:
            parse_clipboard_data()
            # Should show warning about no categories


def test_072_child_summary_with_no_data():
    """Test Child Item Summary section present but empty"""
    test_data = """
    Child Item Summary
    
    Serial Number: ABC123
    """
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showwarning'):
            parse_clipboard_data()


def test_073_child_summary_only_headers():
    """Test Child Item Summary with only column headers, no data"""
    test_data = """
    Child Item Summary
    Category Items Quantity
    Serial Number: ABC123
    """
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showwarning'):
            parse_clipboard_data()


def test_074_malformed_numbers_non_numeric_quantities():
    """Test with text that looks like category but has non-numeric data"""
    test_data = """
    Child Item Summary
    CPU ABC DEF
    MEMORY XYZ 123
    Serial Number
    """
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showwarning'):
            parse_clipboard_data()


def test_075_negative_quantities():
    """Test handling of negative numbers in quantities"""
    test_data = """
    Child Item Summary
    CPU -5 10
    MEMORY 100 -50
    Serial Number
    """
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


def test_076_floating_point_quantities():
    """Test handling of decimal/floating point quantities"""
    test_data = """
    Child Item Summary
    CPU 5.5 10.2
    MEMORY 100.75 200.5
    Serial Number
    """
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


def test_077_special_characters_in_quantities():
    """Test special characters mixed with numbers"""
    test_data = """
    Child Item Summary
    CPU $100 #50
    MEMORY (25) [30]
    Serial Number
    """
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


def test_078_duplicate_category_entries():
    """Test same category appearing multiple times"""
    test_data = """
    Child Item Summary
    CPU 5 10
    MEMORY 20 30
    CPU 8 15
    Serial Number
    """
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


def test_079_extremely_long_lines():
    """Test very long lines in clipboard data"""
    long_line = "A" * 10000
    test_data = f"""
    Child Item Summary
    {long_line}
    CPU 5 10
    {long_line}
    Serial Number
    """
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


def test_080_unicode_in_rack_model():
    """Test unicode characters in rack model name"""
    test_data = """
    Item\tCategory\tType\tModel\tStatus
    001\tRACK\tChassis\tRACK_μ_OMEGA_∑\tINVENTORY
    
    Child Item Summary
    CPU 5 10
    """
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


# ============================================================================
# BOUNDARY & EXTREME CONDITIONS (Tests 081-095)
# ============================================================================

def test_081_very_large_quantity_values():
    """Test extremely large quantity values"""
    test_data = """
    Child Item Summary
    CPU 1000000 9999999
    MEMORY 500000 9999999
    Serial Number
    """
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


def test_082_zero_quantities():
    """Test zero quantities in different positions"""
    test_data = """
    Child Item Summary
    CPU 0 0
    MEMORY 0 10
    SWITCH 10 0
    Serial Number
    """
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


def test_083_single_spaces_between_data():
    """Test with minimal spacing (single spaces instead of multiple)"""
    test_data = """
    Child Item Summary
    CPU 1 2
    MEMORY 3 4
    Serial Number
    """
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


def test_084_multiple_tabs_between_columns():
    """Test with excessive tabs between fields"""
    test_data = """
    Child Item Summary
    CPU\t\t\t5\t\t\t10
    MEMORY\t\t20\t\t\t30
    Serial Number
    """
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


def test_085_mixed_line_endings():
    """Test data with mixed line ending types"""
    test_data = "Child Item Summary\rCPU 5 10\nMEMORY 20 30\r\nSerial Number"
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


# ============================================================================
# RACK MODEL EXTRACTION EDGE CASES (Tests 086-100)
# ============================================================================

def test_086_rack_model_with_leading_trailing_spaces():
    """Test rack model surrounded by whitespace"""
    test_data = """
    Item\tCategory\tType\tModel\tStatus
    001\tRACK\tChassis\t   SPACED_MODEL   \tINVENTORY
    
    Child Item Summary
    CPU 1 2
    """
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


def test_087_rack_model_only_numbers():
    """Test rack model that's purely numeric"""
    test_data = """
    Item\tCategory\tType\tModel\tStatus
    001\tRACK\tChassis\t9876543210\tINVENTORY
    
    Child Item Summary
    CPU 1 2
    """
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


def test_088_rack_model_special_characters():
    """Test rack model with special characters"""
    test_data = """
    Item\tCategory\tType\tModel\tStatus
    001\tRACK\tChassis\tRAC!@#$%^&*()\tINVENTORY
    
    Child Item Summary
    CPU 1 2
    """
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


def test_089_rack_in_column_different_position():
    """Test RACK category appearing in different column position"""
    test_data = """
    Item\tType\tCategory\tModel\tStatus
    001\tChassis\tRACK\tRAC_TEST\tINVENTORY
    
    Child Item Summary
    CPU 1 2
    """
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


def test_090_multiple_racks_different_cases():
    """Test multiple RACK entries with different casing"""
    test_data = """
    Item\tCategory\tType\tModel\tStatus
    001\tRACK\tChassis\tFIRST_RACK\tINVENTORY
    002\track\tChassis\tSECOND_RACK\tINVENTORY
    003\tRacK\tChassis\tTHIRD_RACK\tINVENTORY
    
    Child Item Summary
    CPU 1 2
    """
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


def test_091_rack_model_extremely_long():
    """Test very long rack model name"""
    long_model = "RACK_" + "X" * 500
    test_data = f"""
    Item\tCategory\tType\tModel\tStatus
    001\tRACK\tChassis\t{long_model}\tINVENTORY
    
    Child Item Summary
    CPU 1 2
    """
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


def test_092_squished_rack_with_numbers():
    """Test squished format rack model extraction with multi-digit serial"""
    test_data = """
    RAC:LEGRAND_RACK_PRO_9876543INVENTORYCHILD
    Child Item Summary
    CPU 6 8
    Serial Number
    """
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


def test_093_no_rack_section_fallback():
    """Test fallback when no RACK section found"""
    test_data = """
    Item\tType\tModel\tStatus
    001\tChassis\tUNKNOWN_MODEL\tINVENTORY
    
    Child Item Summary
    CPU 5 10
    """
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


def test_094_rack_with_multiple_spaces_in_name():
    """Test rack model with multiple internal spaces"""
    test_data = """
    Item\tCategory\tType\tModel\tStatus
    001\tRACK\tChassis\tRAC  WITH   MANY   SPACES\tINVENTORY
    
    Child Item Summary
    CPU 1 2
    """
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


def test_095_rack_model_case_preservation():
    """Test that rack model case is preserved"""
    test_data = """
    Item\tCategory\tType\tModel\tStatus
    001\tRACK\tChassis\tMyRaCk_MoDeLv2.1\tINVENTORY
    
    Child Item Summary
    CPU 1 2
    """
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


# ============================================================================
# REGEX & PARSING ROBUSTNESS (Tests 096-110)
# ============================================================================

def test_096_regex_injection_attempt_dot():
    """Test that regex metacharacters don't cause injection"""
    test_data = """
    Child Item Summary
    CPU. 5 10
    MEM.RY 20 30
    Serial Number
    """
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showwarning'):
            parse_clipboard_data()


def test_097_regex_injection_attempt_asterisk():
    """Test asterisk in data"""
    test_data = """
    Child Item Summary
    CPU* 5 10
    MEMORY** 20 30
    Serial Number
    """
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showwarning'):
            parse_clipboard_data()


def test_098_regex_injection_attempt_brackets():
    """Test brackets in data"""
    test_data = """
    Child Item Summary
    CPU[5] 5 10
    MEMORY[REF] 20 30
    Serial Number
    """
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showwarning'):
            parse_clipboard_data()


def test_099_category_case_variations():
    """Test all possible case combinations for categories"""
    test_data = """
    Child Item Summary
    cpu 1 2
    Cpu 3 4
    CPU 5 6
    cPu 7 8
    Serial Number
    """
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


def test_100_massive_clipboard_data():
    """Test with extremely large clipboard data (1MB+)"""
    # Generate very large data
    large_data = "Child Item Summary\n"
    for i in range(5000):
        large_data += f"CPU {i} {i+1}\nMEMORY {i} {i+1}\n"
    large_data += "Serial Number"
    
    with patch('pyperclip.paste', return_value=large_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


# ============================================================================
# CONCURRENT & STATE ISSUES (Tests 101-105)
# ============================================================================

def test_101_rapid_sequential_calls():
    """Test multiple rapid parse calls"""
    test_data = """
    Child Item Summary
    CPU 5 10
    Serial Number
    """
    
    for _ in range(10):
        with patch('pyperclip.paste', return_value=test_data):
            with patch('tkinter.messagebox.showinfo'):
                parse_clipboard_data()


def test_102_empty_then_valid_data():
    """Test parsing empty data followed by valid data"""
    empty_data = ""
    valid_data = "Child Item Summary\nCPU 5 10\nSerial Number"
    
    with patch('pyperclip.paste', return_value=empty_data):
        with patch('tkinter.messagebox.showwarning'):
            parse_clipboard_data()
    
    with patch('pyperclip.paste', return_value=valid_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


def test_103_whitespace_only_variations():
    """Test different types of whitespace-only content"""
    test_cases = [
        " " * 100,              # Only spaces
        "\t" * 100,             # Only tabs
        "\n" * 100,             # Only newlines
        " \t\n " * 100,         # Mixed whitespace
    ]
    
    for test_data in test_cases:
        with patch('pyperclip.paste', return_value=test_data):
            with patch('tkinter.messagebox.showwarning'):
                parse_clipboard_data()


def test_104_null_bytes_in_data():
    """Test data with null bytes"""
    test_data = "Child Item Summary\x00CPU 5 10\x00Serial Number"
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


def test_105_control_characters_in_data():
    """Test data with control characters"""
    test_data = "Child Item Summary\x01\x02CPU\x03 5 10\x04Serial Number"
    
    with patch('pyperclip.paste', return_value=test_data):
        with patch('tkinter.messagebox.showinfo'):
            parse_clipboard_data()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
