import tkinter as tk
from tkinter import messagebox
import re
import pyperclip
import urllib.parse
import webbrowser
import json
import os
from dotenv import load_dotenv

# ==============================================================================
# CONFIGURATION
# ==============================================================================
load_dotenv()

WEB_APP_URL = os.getenv(
    "WEB_APP_URL", 
    "https://script.google.com/a/macros/ironmountain.com/s/AKfycbxFWwKznWRIyLEHOmEosRLSUoU-66Sta35HESHcZUzjDEe4PJVvy3ZTIOC6sh3qB6tb/exec"
)

MY_ACCESS_TOKEN = os.getenv("MY_ACCESS_TOKEN", "")
SECRET_KEY = os.getenv("SECRET_KEY", "IronMountainSecureToken2026")

def upload_to_google_sheets(summary_data, rack_model):
    """Packages data parameters and routes it securely through your browser's SSO profile."""
    payload = {
        "secret_key": SECRET_KEY,
        "rack_model": rack_model,
        "summary_data": summary_data
    }
    
    try:
        # Convert data dictionary to a clean, URL-safe JSON string
        json_string = urllib.parse.quote(json.dumps(payload))
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
    """Extracts target matrix terms strictly from the Child Item Summary block 
    and captures ONLY the exact Rack model from the itemized table layout."""
    try:
        raw_text = pyperclip.paste()
    except Exception as e:
        messagebox.showerror("Clipboard Error", f"Failed to read clipboard:\n{e}")
        return
    
    if not raw_text or not raw_text.strip():
        messagebox.showwarning("Empty Clipboard", "Clipboard is empty. Please copy data first.")
        return
    
    summary_data = {}
    rack_model = "Unknown Rack"
    
    # 1. ISOLATE THE CHILD ITEM SUMMARY SECTION
    summary_section_match = re.search(r"Child Item Summary(.*?)(?:Serial Number|$)", raw_text, re.IGNORECASE | re.DOTALL)
    
    if summary_section_match:
        summary_block = summary_section_match.group(1)
        valid_categories = {
            "CHASSIS", "HBA", "MEMORY", "MODULES", "SSD", "SWITCH", "UPS", "SCRAP",
            "CPU", "CPU_COOLER", "FAN", "POWER_SUPPLY", "PDU", "NIC", "RAID_CONTROLLER",
            "STORAGE_DRIVE", "HDD", "NVME", "GPU", "TPU", "FPGA", "KVM", "BATTERY",
            "BATTERY_MODULE", "CONTROLLER", "NETWORK_SWITCH", "TRANSCEIVER", "SFP", "QSFP",
            "CABLES", "RAILS", "MOUNTING_KIT", "FAN_MODULE", "BLADE", "BLADE_SERVER",
            "RACK_UNIT", "PATCH_PANEL", "BMC", "MANAGEMENT_MODULE", "CONSOLE_SERVER",
            "TAPE_LIBRARY", "TAPE_LIB", "JBOD", "EXPANSION_CARD", "OPTICAL_TRANSCEIVER"
        }
        
        for target in valid_categories:
            cat_match = re.search(rf"{target}\s*(\d+)\s*(\d*)", summary_block, re.IGNORECASE)
            if cat_match:
                # Use group(2) if it exists and is not empty, otherwise use group(1)
                qty_str = cat_match.group(2) if cat_match.group(2) else cat_match.group(1)
                summary_data[target] = int(qty_str)
                
    if not summary_data:
        valid_categories = {
            "MEMORY", "MODULES", "OPTICAL_TRANSCEIVER", "SCRAP", "SSD", "STORAGE_ARRAY",
            "SWITCH", "UPS", "CHASSIS", "CPU", "FAN", "POWER_SUPPLY", "PDU", "NIC",
            "RAID_CONTROLLER", "HDD", "NVME", "GPU", "BLADE", "PATCH_PANEL", "CABLES",
            "TRANSCEIVER", "SFP", "QSFP", "JBOD", "EXPANSION_CARD"
        }
        for line in raw_text.split('\n'):
            for target in valid_categories:
                if target in line.upper():
                    nums = re.findall(r"\d+", line)
                    if nums:
                        summary_data[target] = int(nums[-1])

    if not summary_data:
        messagebox.showwarning("Empty Target Matrix", "No valid child item summary categories detected on your clipboard.")
        return

    # 2. EXACT MODEL EXTRACTOR FROM THE ITEMIZED GRAPH
    # Strategy A: Clean column-based extraction using tabs or spaces
    for line in raw_text.split('\n'):
        # Split by tabs first, then fall back to multi-spaces
        columns = [col.strip() for col in line.split('\t') if col.strip()]
        if len(columns) < 3:
            columns = [col.strip() for col in re.split(r'\s{2,}', line) if col.strip()]
            
        # If 'RACK' is found in the Category column, the next column is explicitly the Model
        if len(columns) >= 4 and "RACK" == columns[2].upper():
            rack_model = columns[3]
            break

    # Strategy B: Fallback if the string arrives completely squished without any spacing
    if rack_model == "Unknown Rack":
        # Finds 'RACK', captures the model characters, ignores the 7-digit Asset Tag right before the Status
        squished_match = re.search(r"RACK\s*([A-Za-z0-9_\-]+?)(\d{7})(?:SOLD|RECYCLED|DESTROYED|INVENTORY)", raw_text, re.IGNORECASE)
        if squished_match:
            rack_model = squished_match.group(1).strip()

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