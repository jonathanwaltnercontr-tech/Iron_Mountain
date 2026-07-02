"""
Pytest configuration for Iron Mountain tests
Handles mocking, fixtures, and file output instead of Google Sheets uploads
"""

import pytest
import json
import os
from pathlib import Path
from datetime import datetime

# Get the tests_execution directory
TESTS_EXECUTION_DIR = Path(__file__).parent / "tests_execution"
TESTS_EXECUTION_DIR.mkdir(exist_ok=True)


@pytest.fixture(autouse=True)
def mock_google_sheets_upload(monkeypatch):
    """
    Automatically mock upload_to_google_sheets for all tests
    Saves data to JSON files instead of uploading to Google Sheets
    """
    
    def mock_upload(summary_data, rack_model):
        """
        Mock upload function that saves to file instead of uploading
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        output_file = TESTS_EXECUTION_DIR / f"upload_data_{timestamp}.json"
        
        output_data = {
            "timestamp": datetime.now().isoformat(),
            "rack_model": rack_model,
            "summary_data": summary_data,
            "status": "captured_from_test"
        }
        
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        # Also append to a comprehensive log
        log_file = TESTS_EXECUTION_DIR / "all_uploads.log"
        with open(log_file, 'a') as f:
            f.write(f"\n{datetime.now().isoformat()} | Rack: {rack_model} | Items: {len(summary_data)}\n")
    
    # Import here to avoid circular imports
    from scripts import app
    monkeypatch.setattr(app, "upload_to_google_sheets", mock_upload)


@pytest.fixture(autouse=True)
def mock_tkinter_messagebox(monkeypatch):
    """
    Mock tkinter messagebox to prevent GUI popups during testing
    Saves messages to log file
    """
    from unittest.mock import MagicMock
    
    messages_log = TESTS_EXECUTION_DIR / "ui_messages.log"
    
    def log_showinfo(title, message):
        with open(messages_log, 'a') as f:
            f.write(f"\n[INFO] {title}\n{message}\n")
    
    def log_showwarning(title, message):
        with open(messages_log, 'a') as f:
            f.write(f"\n[WARNING] {title}\n{message}\n")
    
    def log_showerror(title, message):
        with open(messages_log, 'a') as f:
            f.write(f"\n[ERROR] {title}\n{message}\n")
    
    import tkinter.messagebox
    monkeypatch.setattr(tkinter.messagebox, "showinfo", log_showinfo)
    monkeypatch.setattr(tkinter.messagebox, "showwarning", log_showwarning)
    monkeypatch.setattr(tkinter.messagebox, "showerror", log_showerror)


@pytest.fixture(autouse=True)
def mock_webbrowser(monkeypatch):
    """
    Mock webbrowser.open to prevent opening browser during tests
    Logs the URLs that would have been opened
    """
    urls_log = TESTS_EXECUTION_DIR / "browser_urls.log"
    
    def log_webbrowser_open(url, new=0, autoraise=True):
        with open(urls_log, 'a') as f:
            f.write(f"\n{datetime.now().isoformat()} | URL: {url[:100]}...\n")
    
    import webbrowser
    monkeypatch.setattr(webbrowser, "open", log_webbrowser_open)


@pytest.fixture(autouse=True)
def create_test_report(request):
    """
    Create a test report file for each test
    """
    yield
    
    # After test execution
    report_file = TESTS_EXECUTION_DIR / "test_results.log"
    test_name = request.node.name
    test_outcome = "PASSED" if request.node.rep_call.passed else "FAILED" if hasattr(request.node, 'rep_call') else "PASSED"
    
    with open(report_file, 'a') as f:
        f.write(f"\n{datetime.now().isoformat()} | {test_name} | {test_outcome}\n")


# Hook to capture test outcomes
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture test results"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
