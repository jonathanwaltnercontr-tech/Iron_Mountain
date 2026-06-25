import tkinter as tk
from tkinter import messagebox
import pandas as pd
from io import StringIO
import re
import os
import webbrowser
import plotly.express as px
import gspread
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# --- AUTOMATED AUTHENTICATION STRUCTURE ---
TARGET_FOLDER_ID = "1QPpHmq24nmASYgQb9TY6hcMLbi9jMJPe"

# Tokens extracted directly from your Playground session
ACCESS_TOKEN = "ya29.a0AT3oNZ_-lthgbFYhQQwytUPG9wTaRxxTtSPaRYJLom4D7s9F6D4mw9ZyzFUgbW2KxLzrHCnYvs9tpipHOOh7CF__GsI3UEycpZVglA3z1zf-yJM2vQiICOORRcL6Pm1xUxj0YnjKTNIL350kw8Y5TdvOU18BeAdCtHCTOR5gvD-CIbPNIts76LP7Z05dHTZJ2GpWpvAaCgYKAcsSARYSFQHGX2MiIMtpfP2VmkKlYJat3JiGBA0206"
REFRESH_TOKEN = "1//04N29cKvdJV9XCgYIARAAGAQSNwF-L9IrnAx4kbIOEbaT10GkXQJ2D2s6suuxCW118xe7DVCzCJ_BNx-azMxKjzDP-96kbeYLzeM"
CLIENT_ID = "407408718192.apps.googleusercontent.com"

class IronMountainUltimateApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw() 
        
        # Setup Floating UI Panel
        self.floating_win = tk.Toplevel(self.root)
        self.floating_win.title("IM Auto-Upload")
        self.floating_win.attributes("-topmost", True)
        self.floating_win.geometry("180x60+40+40") 
        
        self.btn = tk.Button(self.floating_win, text="🚀 Send Straight to Folder", 
                             bg="#007ACC", fg="white", font=("Arial", 10, "bold"),
                             command=self.process_and_upload)
        
        self.btn.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.floating_win.withdraw()
        
        self.current_data = ""
        self.monitor_clipboard()
        
    def monitor_clipboard(self):
        try:
            data = self.root.clipboard_get()
            if "Child Item Summary" in data and "Category" in data:
                if data != self.current_data:
                    self.current_data = data
                    self.floating_win.deiconify() 
            else:
                self.floating_win.withdraw()
        except tk.TclError:
            pass 
        self.root.after(1000, self.monitor_clipboard)

    def process_and_upload(self):
        try:
            raw_text = self.current_data.strip()
            
            # 1. PARSE RACK MODEL NAME
            rack_model = "Unknown Rack Model"
            for line in raw_text.split('\n'):
                if "RACK" in line:
                    parts = re.split(r'\t|\s{2,}', line.strip())
                    if len(parts) >= 4:
                        rack_model = parts[3]
                        break

            # 2. PARSE CHILD ITEM SUMMARY TABLE
            summary_pattern = re.search(r"Child Item Summary\n(.*?)\nSerial Number", raw_text, re.DOTALL)
            if not summary_pattern:
                raise Exception("Could not isolate the Child Item Summary section.")
                
            summary_block = summary_pattern.group(1).strip()
            
            summary_rows = []
            for line in summary_block.split('\n'):
                parts = [p.strip() for p in re.split(r'\t|\s{2,}', line.strip()) if p.strip()]
                if parts:
                    summary_rows.append(parts)
            
            summary_df = pd.DataFrame(summary_rows[1:], columns=summary_rows[0])
            summary_df['Quantity'] = pd.to_numeric(summary_df['Quantity'])
            
            # 3. GENERATE INTERACTIVE GRAPH VIEW
            fig = px.bar(summary_df, x='Category', y='Quantity', 
                         title=f"Components Structure Inside Rack ({rack_model})",
                         text='Quantity', color='Quantity',
                         color_continuous_scale=px.colors.sequential.Plotly3,
                         template="plotly_white")
            fig.update_traces(textposition='outside')
            
            chart_html = f"Rack_Graph_{rack_model.replace(' ', '_')}.html"
            fig.write_html(chart_html)
            webbrowser.open('file://' + os.path.realpath(chart_html))

            # 4. TOKEN REFRESH AUTHENTICATION
            creds = Credentials(
                token=ACCESS_TOKEN,
                refresh_token=REFRESH_TOKEN,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=CLIENT_ID
            )
            
            if not creds.valid:
                creds.refresh(Request())
                
            gc = gspread.authorize(creds)
            sheet_title = f"Rack Summary - {rack_model}"
            
            # Create the sheet inside your target folder
            spreadsheet = gc.create(sheet_title, folder_id=TARGET_FOLDER_ID)
            worksheet = spreadsheet.sheet1
            worksheet.title = "Summary Overview"
            
            # --- GUARANTEED DATA BLOCK FORMATION ---
            headers = [str(c) for c in summary_df.columns.tolist()]
            rows = [[str(item) for item in row] for row in summary_df.values.tolist()]
            
            full_matrix = [
                [f"Rack Profile Model: {rack_model}"],
                [], 
                headers
            ] + rows
            
            # Use strict update_values() which forces Google to accept the matrix array data
            worksheet.update_values('A1', full_matrix)
            
            messagebox.showinfo("Success!", f"Successfully processed {rack_model}!\n\n1. Graph opened in Chrome.\n2. Google Sheet data successfully populated in your folder.")
            self.floating_win.withdraw()
            self.current_data = ""

        except Exception as e:
            messagebox.showerror("Error", f"Execution Failed: {str(e)}")

if __name__ == "__main__":
    print("Background listener engine running safely... Go copy your summary pages!")
    app = IronMountainUltimateApp()
    app.root.mainloop()