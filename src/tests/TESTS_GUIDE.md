# Test Suite Documentation

## Overview
✅ **50 comprehensive test cases created and all PASSED**

The test suite validates the Iron Mountain app's core functionality:
- Clipboard data parsing
- Error handling
- Rack model extraction
- Data serialization

## Test Results Location

All test execution files are saved to: **`src/tests/tests_execution/`**

### Generated Files

1. **`upload_data_*.json`** (Multiple files)
   - Individual captures from each test that performs an upload
   - Shows parsed data sent to Google Sheets (without actual upload)
   - Contains: timestamp, rack_model, summary_data, status

   Example:
   ```json
   {
     "timestamp": "2026-07-02T07:44:41.818001",
     "rack_model": "Unknown Rack",
     "summary_data": {
       "MEMORY": 15
     },
     "status": "captured_from_test"
   }
   ```

2. **`all_uploads.log`**
   - Summary log of all captured uploads
   - Format: `[timestamp] | Rack: [model] | Items: [count]`
   - Quick overview of all data captured during tests

3. **`test_results.log`**
   - Individual test results with pass/fail status
   - Format: `[timestamp] | [test_name] | [PASSED/FAILED]`
   - Track which tests executed and their outcomes

4. **`ui_messages.log`**
   - All UI messages (warnings, errors, info) triggered during tests
   - Logged with: [INFO], [WARNING], [ERROR] tags
   - Prevents GUI popups during automated testing

5. **`browser_urls.log`**
   - URLs that would be opened in the browser
   - Prevents actual browser launches during testing

## Test Coverage (50 Tests)

### GROUP 1: Valid Input Parsing (Tests 1-8)
- Single & multiple category parsing
- Rack model extraction (columns & squished text)
- All valid hardware categories
- Quantity extraction accuracy
- Ignoring non-summary sections
- Case-insensitive matching

### GROUP 2: Error Handling (Tests 9-16)
- Empty clipboard detection
- Whitespace-only clipboard
- Missing Child Item Summary
- Clipboard read exceptions
- Invalid category handling
- Malformed quantity entries
- Large number handling
- Zero quantity acceptance

### GROUP 3: Rack Model Extraction (Tests 17-24)
- Basic rack model extraction
- Underscores & hyphens in names
- Space-separated columns
- Multiple rack entries
- Case-insensitive RACK matching
- Numeric characters in names
- Unknown Rack default fallback

### GROUP 4: Data Serialization (Tests 25-32)
- JSON payload structure validation
- Special character URL encoding
- JSON serialization accuracy
- Unicode character support
- Large number serialization
- Apostrophe handling
- Empty summary data handling

### GROUP 5: Integration & Workflow (Tests 33-40)
- Complete workflow validation
- Fallback parsing activation
- Multiple separate uploads
- Console logging verification
- Summary output format
- Rack model output format
- Mixed case consistency
- Regex pattern stability

### GROUP 6: Edge Cases (Tests 41-50)
- Very long rack model names
- Large clipboard data handling
- Single digit quantities
- Leading/trailing whitespace
- Tab vs space delimiters
- Duplicate category entries
- Special characters in names
- Numeric-only categories
- Partial summary sections
- Cumulative parsing accuracy (final comprehensive test)

## Running the Tests

### Run all tests:
```bash
cd c:\Users\jwaltner.ctr\Documents\GitHub\Iron_Mountain
.\.venv\Scripts\pytest src/tests/test_app.py -v
```

### Run specific test:
```bash
.\.venv\Scripts\pytest src/tests/test_app.py::test_001_parse_single_category -v
```

### Run with detailed output:
```bash
.\.venv\Scripts\pytest src/tests/test_app.py -vv --tb=long
```

### Generate HTML report:
```bash
.\.venv\Scripts\pytest src/tests/test_app.py --html=report.html
```

## Test Results Summary

```
============================= 50 passed in 0.94s ==============================
```

✅ All 50 tests passed successfully
✅ No Google Sheets uploads occurred
✅ All data captured to local JSON files
✅ All errors/warnings logged to files
✅ No browser windows opened
✅ Complete audit trail available in tests_execution/

## Key Features of Test Setup

1. **No External Calls**
   - ✅ Google Sheets API not called
   - ✅ Browser not opened
   - ✅ GUI not displayed

2. **Complete Audit Trail**
   - ✅ Every test action logged
   - ✅ All data captured to JSON
   - ✅ UI messages preserved
   - ✅ Browser URLs captured

3. **Test Isolation**
   - ✅ Each test is independent
   - ✅ No test interference
   - ✅ Fixtures provide clean state

4. **Error Capture**
   - ✅ Exceptions logged
   - ✅ UI warnings/errors recorded
   - ✅ Easy debugging

## Reviewing Test Data

To inspect what data was captured:

```bash
# View latest upload data
Get-Content src/tests/tests_execution/upload_data_*.json -Head 20

# View all uploads summary
Get-Content src/tests/tests_execution/all_uploads.log

# View test results
Get-Content src/tests/tests_execution/test_results.log

# View UI messages
Get-Content src/tests/tests_execution/ui_messages.log
```

## Files Modified/Created

- ✅ `src/tests/test_app.py` - 50 test cases
- ✅ `src/tests/conftest.py` - pytest configuration & mocking
- ✅ `src/tests/tests_execution/` - test execution results

## Next Steps

1. View test execution files in VS Code's file explorer
2. Review JSON files to verify data parsing
3. Check logs for any issues
4. Modify tests as needed
5. Re-run tests to verify fixes

---

**Note**: All tests are designed to verify that goals were achieved without modifying any actual data sources or external systems.
