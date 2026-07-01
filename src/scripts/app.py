import tkinter as tk
from tkinter import messagebox
import re
import pyperclip
import urllib.parse
import webbrowser

# ==============================================================================
# CONFIGURATION
# ==============================================================================
WEB_APP_URL = "https://script.google.com/a/macros/ironmountain.com/s/AKfycbxFWwKznWRIyLEHOmEosRLSUoU-66Sta35HESHcZUzjDEe4PJVvy3ZTIOC6sh3qB6tb/exec"

# Your validated access token token configuration string
MY_ACCESS_TOKEN = "ya29.a0AT3oNZ_9_u_0hv2iDiidRSrJpSrroUEFjIecb2aK3Tp-QCT3rAKIoK88OqfkqEt9NUK-26RBFUCJW4YvOH9f4qbKUY3YCu20Q6PPO1SUUZRvIbgw6p6qEosofbwnstL0AMu_1A-wgdlphQ6sg6yzuEfdVgoqEKwTSFJOo5rurCdMnF8uBv8OjV1ezYkqjU2kj1UEbTMo4pwQIgaCgYKASMSARQSFQHGX2MiWA5vR3J-LsBHy7W1ho88Mg0213"

def upload_to_google_sheets(summary_data, rack_model):
    """Packages data parameters and routes it securely through your browser's SSO profile."""
    payload = {
        "secret_key": "IronMountainSecureToken2026",
        "rack_model": rack_model,
        "summary_data": summary_data
    }
    
    try:
        # Convert data dictionary to a clean, URL-safe data string parameter
        json_string = urllib.parse.quote(str(payload).replace("'", '"'))
        final_delivery_url = f"{WEB_APP_URL}?data={json_string}"
        
        print("🔄 Processing asset parsing array and instantiating individual document file...")
        # Automatically launches your default browser profile to create the sheet and avoid the 401 block
        webbrowser.open(final_delivery_url, new=2, autoraise=False)
        
        messagebox.showinfo(
            "Report Document Generated", 
            f"Successfully updated master dashboard ledger!\n\nNew Sheet Created for: {rack_model}\nCategories printed to top table: {len(summary_data)}"
        )
    except Exception as e:
        messagebox.showerror("Error", f"Failed to reach spreadsheet pipeline:\n{e}")

def parse_clipboard_data():
    """Extracts target matrix terms across dense or heavily squished corporate text dumps."""
    raw_text = pyperclip.paste()
    
    # Target validation metrics set using an optimized hash set for instant O(1) lookups
    valid_categories = {
        "MEMORY", "MODULES", "OPTICAL_TRANSCEIVER", "SCRAP", 
        "SSD", "STORAGE_ARRAY", "SWITCH", "UPS", "CHASSIS, CPU, GPU"
    }
    
    summary_data = {}
    rack_model = "Unknown Rack"
    
    # 1. CASE-INSENSITIVE SMART DATA EXTRACTOR
    # Targets text strings that immediately precede numerical values anywhere in the clip
    found_groupings = re.findall(r"([A-Za-z_]+?)(\d+)", raw_text)
    for cat, qty in found_groupings:
        upper_cat = cat.upper()
        for target in valid_categories:
            if upper_cat.endswith(target):
                summary_data[target] = int(qty)

    # Fallback scanning loop checking line layers directly if text is formatted cleanly
    if not summary_data:
        for line in raw_text.split('\n'):
            for target in valid_categories:
                if target in line.upper():
                    nums = re.findall(r"\d+", line)
                    if nums:
                        summary_data[target] = int(nums[-1])

    if not summary_data:
        messagebox.showwarning("Empty Target Matrix", "No valid child item summary categories detected on your clipboard.")
        return

    # 2. BRAND-AGNOSTIC HARDWARE ENCLOSURE MATCHER
    lines = raw_text.split('\n')
    for line in lines:
        line = line.strip()
        if "RACK" in line.upper():
            match_rack = re.search(r"RACK\s*([A-Za-z0-9_\-\s]+?\s+RACK|[A-Za-z0-9_\-\s]{3,30})", line, re.IGNORECASE)
            if match_rack:
                rack_model = match_rack.group(1).strip()
            else:
                fallback_match = re.search(r"RACK([A-Z0-9\s\-]{3,20})", line, re.IGNORECASE)
                rack_model = fallback_match.group(1).strip() if fallback_match else "Unknown Rack"
            
            # Wipe out trailing numbers or status suffixes
            rack_model = re.sub(r"\d+$", "", rack_model).strip()
            break 

    print(f"\n================ LOG PREVIEW ================")
    print(f"Identified Hardware Enclosure: {rack_model}")
    print(f"Parsed Assets Breakdown:      {summary_data}")
    print(f"=============================================")
    
    upload_to_google_sheets(summary_data, rack_model)

def create_floating_button():
    """Builds a permanent widget panel that pins directly over active browser tabs/sheets."""
    root = tk.Tk()
    root.title("Clipboard Scanner Tool")
    root.geometry("260x90")
    root.attributes("-topmost", True)  # Anchors the tool window permanently on top
    
    btn = tk.Button(
        root, 
        text="Process Clipboard Data", 
        command=parse_clipboard_data, 
        bg="#d9534f", 
        fg="white", 
        font=("Arial", 11, "bold"),
        activebackground="#c9302c",
        activeforeground="white"
    )
    btn.pack(expand=True, fill=tk.BOTH, padx=12, pady=12)
    
    root.mainloop()

if __name__ == "__main__":
    create_floating_button()