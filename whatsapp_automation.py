"""
WHATSAPP AUTOMATION - SIMPLE & RELIABLE
"""

import json
import os
import sys
import time
import traceback
from datetime import datetime
import re
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd

print("=" * 70)
print("WHATSAPP AUTOMATION")
print("=" * 70)
print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)


class WhatsAppAutomation:
    def __init__(self, config):
        self.config = config
        self.driver = None
        self.failed_messages = []
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.log_file = os.path.join(script_dir, "failed_messages.log")
        
    def setup_driver(self):
        """Setup Chrome - Simple & Clean"""
        print("\n[1/4] SETTING UP CHROME")
        print("-" * 40)
        
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        
        try:
            print("Opening Chrome...")
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.maximize_window()
            print("✓ Chrome ready")
            return True
        except Exception as e:
            print(f"✗ Chrome error: {str(e)[:200]}")
            return False
    
    def wait_for_login(self):
        """Wait for QR scan - FIXED 60 SECOND WAIT"""
        print(f"\n[2/4] WHATSAPP WEB")
        print("-" * 40)
        
        try:
            print("Loading WhatsApp Web...")
            self.driver.get("https://web.whatsapp.com/")
            time.sleep(5)  # Initial wait for page load
            
            print("\n" + "=" * 70)
            print("SCAN QR CODE")
            print("=" * 70)
            print("1. Look at Chrome window")
            print("2. Scan QR code with your phone")
            print("3. You have 60 seconds to scan")
            print("=" * 70)
            
            # FIXED: Always wait 60 seconds for QR scan
            wait_time = 60
            print(f"\n⏳ Waiting {wait_time} seconds for QR scan...")
            
            start_time = time.time()
            qr_scanned = False
            
            while time.time() - start_time < wait_time:
                try:
                    # Check if already logged in (chat list exists)
                    chat_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                        "div[role='list'], div[data-testid='chat-list'], div[class*='chat']")
                    
                    if chat_elements:
                        print("✓ WhatsApp loaded successfully!")
                        qr_scanned = True
                        break
                    
                    # Check if QR code is still present
                    qr_elements = self.driver.find_elements(By.CSS_SELECTOR, "canvas")
                    if not qr_elements:
                        print("✓ QR code disappeared (scanned)")
                        qr_scanned = True
                        break
                        
                except:
                    pass
                
                # Show progress every 15 seconds
                elapsed = int(time.time() - start_time)
                if elapsed % 15 == 0:
                    print(f"  {elapsed}/{wait_time} seconds...")
                
                time.sleep(2)  # Check every 2 seconds
            
            if qr_scanned:
                print("✓ QR scanned successfully!")
                time.sleep(5)  # Extra wait for WhatsApp to fully load
                return True
            else:
                print(f"⚠️ {wait_time} seconds elapsed - QR not detected")
                print("⚠️ Continuing anyway - please ensure WhatsApp is loaded")
                time.sleep(10)  # Extra wait
                return True  # Continue anyway
                
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            print("⚠️ Continuing anyway...")
            time.sleep(10)
            return True  # Continue anyway
    
    def format_phone(self, phone):
        """Format phone number"""
        phone = str(phone).strip()
        phone = re.sub(r'[^\d+]', '', phone)
        country_code = self.config.get('country_code', '+92')
        
        if not phone.startswith(country_code):
            if phone.startswith('0'):
                phone = phone[1:]
            phone = country_code + phone
        return phone
    
    def send_message(self, phone, message):
        """Send message - FIXED to type in message box, not search box"""
        try:
            print(f"\nSending to: {phone}")
            
            whatsapp_url = f"https://web.whatsapp.com/send?phone={phone}"
            self.driver.get(whatsapp_url)
            time.sleep(5)
            
            # FIX: Wait for chat to fully load and find the CORRECT message box
            print("Looking for message input box...")
            
            # Method 1: Try to find message box by data-tab attribute
            try:
                # WhatsApp Web uses data-tab='10' for message input
                message_box = WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 
                        "div[contenteditable='true'][data-tab='10'], "
                        "div[contenteditable='true'][data-tab='9'], "
                        "footer div[contenteditable='true']"))
                )
                print("✓ Found message box (data-tab selector)")
            except:
                # Method 2: Try to find by position (footer area)
                try:
                    message_box = WebDriverWait(self.driver, 15).until(
                        EC.presence_of_element_located((By.XPATH, 
                            "//footer//div[@contenteditable='true']"))
                    )
                    print("✓ Found message box (footer selector)")
                except:
                    # Method 3: Try your exact XPath
                    try:
                        message_box = WebDriverWait(self.driver, 15).until(
                            EC.presence_of_element_located((By.XPATH, 
                                "/html/body/div[1]/div/div/div[3]/div/div[4]/div/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div[1]/p"))
                        )
                        print("✓ Found message box (your XPath)")
                    except:
                        # Method 4: Last resort - find ALL contenteditable divs and use the last one
                        all_editables = self.driver.find_elements(By.CSS_SELECTOR, "div[contenteditable='true']")
                        if len(all_editables) >= 2:
                            # Usually: [0] = search box, [1] = message box
                            message_box = all_editables[1]
                            print(f"✓ Found message box (index {1} of {len(all_editables)})")
                        else:
                            raise Exception("Could not find message input box")
            
            # Click and focus on the message box
            print("Focusing on message box...")
            message_box.click()
            time.sleep(2)
            
            # Clear any existing text (Ctrl+A, Delete)
            message_box.send_keys(Keys.CONTROL + "a")
            message_box.send_keys(Keys.DELETE)
            time.sleep(1)
            
            # Send message line by line
            print("Typing message...")
            lines = message.split("\n")
            for i, line in enumerate(lines):
                message_box.send_keys(line)
                if i < len(lines) - 1:
                    message_box.send_keys(Keys.SHIFT + Keys.ENTER)
                    time.sleep(0.1)
            
            # Send the message
            message_box.send_keys(Keys.ENTER)
            time.sleep(4)
            
            print(f"✓ Message sent to {phone}")
            return True
            
        except Exception as e:
            print(f"✗ Failed to send: {str(e)[:100]}")
            
            # Take screenshot for debugging
            try:
                safe_phone = re.sub(r'[^\d]', '', phone)[-4:]  # Last 4 digits
                screenshot_path = os.path.join(os.path.dirname(__file__), f"error_send_{safe_phone}.png")
                self.driver.save_screenshot(screenshot_path)
                print(f"  Screenshot saved: {screenshot_path}")
            except:
                pass
                
            return False
    
    def run(self):
        """Main execution - MUST HAVE THIS METHOD"""
        try:
            if not self.setup_driver():
                return False, "Chrome failed"
            
            if not self.wait_for_login():
                return False, "Login failed"
            
            print(f"\n[3/4] READING DATA")
            print("-" * 40)
            
            file_path = self.config['file_path']
            if not os.path.exists(file_path):
                return False, f"File not found: {file_path}"
            
            df = pd.read_excel(file_path)
            phone_column = self.config['phone_column']
            
            if phone_column not in df.columns:
                return False, f"Column '{phone_column}' not found"
            
            total = len(df)
            success = 0
            
            print(f"✓ Found {total} contacts")
            
            print(f"\n[4/4] SENDING MESSAGES")
            print("-" * 40)
            
            for i, row in df.iterrows():
                contact_num = i + 1
                print(f"\n{contact_num}/{total}:")
                
                raw_phone = row[phone_column]
                if pd.isna(raw_phone):
                    print("  ✗ Empty phone")
                    continue
                
                phone = self.format_phone(raw_phone)
                print(f"  Phone: {phone}")
                
                message = self.config['message_template']
                selected_vars = self.config.get('selected_vars', [])
                
                for var in selected_vars:
                    if var in df.columns and var != phone_column:
                        value = str(row[var]) if not pd.isna(row[var]) else ""
                        message = message.replace(f"{{{var}}}", value)
                
                message = message.replace(f"{{{phone_column}}}", str(raw_phone))
                
                # Send with retry
                for attempt in range(3):
                    if self.send_message(phone, message):
                        success += 1
                        print(f"  ✓ Sent")
                        break
                    elif attempt < 2:
                        print(f"  ↻ Retry {attempt+1}/3")
                        time.sleep(5)
                    else:
                        print(f"  ✗ Failed")
                
                if contact_num < total:
                    delay = random.randint(10, 25)
                    print(f"  ⏳ Waiting {delay}s...")
                    time.sleep(delay)
            
            self.driver.quit()
            
            print("\n" + "=" * 70)
            print("COMPLETE")
            print("=" * 70)
            print(f"Total: {total}")
            print(f"Success: {success}")
            print(f"Failed: {total - success}")
            
            return True, f"Sent {success}/{total}"
            
        except Exception as e:
            print(f"\n✗ Error: {str(e)}")
            traceback.print_exc()
            
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
            
            return False, str(e)


def main():
    if len(sys.argv) < 2:
        print("Usage: python whatsapp_automation.py <config_file>")
        input("\nPress Enter to exit...")
        return
    
    config_file = sys.argv[1]
    
    try:
        print(f"Loading config...")
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        # Show config details
        print(f"\nConfiguration:")
        print(f"- File: {config.get('file_path')}")
        print(f"- Phone column: {config.get('phone_column')}")
        print(f"- Country code: {config.get('country_code', '+92')}")
        print(f"- Variables: {len(config.get('selected_vars', []))} selected")
        print(f"\n⚠️ Note: You have 60 seconds to scan QR code")
        
        automation = WhatsAppAutomation(config)
        success, message = automation.run()  # This calls the run() method
        
        print("\n" + "=" * 70)
        print("RESULT")
        print("=" * 70)
        print(message)
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        traceback.print_exc()
    
    print("\n" + "=" * 70)
    input("Press Enter to close...")


if __name__ == "__main__":
    main()