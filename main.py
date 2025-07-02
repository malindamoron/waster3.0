import time 
import random 
from playwright.sync_api import sync_playwright 
from getpass import getpass

--- UserCredentials ---

EMAIL = "shashisunil3333@gmail.com" 
PASSWORD = "WWW.YOUTUBE.COM"  # Fill manually below

--- Command Variants ---

COMMANDS = [ 
    "generate copilot news today", 
    "what if news", 
    "future releases of movies and series", 
    "today’s trending news" 
]

--- Delay Config ---

REFRESH_INTERVAL = 210  # seconds = 3.5 minutes

--- Main Function ---

def run_waster(): global PASSWORD if not PASSWORD: PASSWORD = getpass("Enter your Microsoft password: ")

with sync_playwright() as p:
    print("[WASTER] Launching browser...")
    browser = p.chromium.launch(headless=False, args=[
        "--disable-blink-features=AutomationControlled",
        "--start-maximized"
    ])
    context = browser.new_context()
    page = context.new_page()

    print("[WASTER] Navigating to Copilot...")
    page.goto("https://copilot.microsoft.com")

    # Click sign in if needed
    try:
        page.click("text=Sign in", timeout=10000)
        print("[WASTER] Sign-in page detected.")
    except:
        print("[WASTER] Already signed in or no sign-in button found.")

    # Login flow
    try:
        page.fill('input[type="email"]', EMAIL)
        page.click('input[type="submit"]')
        page.wait_for_timeout(2000)

        page.fill('input[type="password"]', PASSWORD)
        page.click('input[type="submit"]')
        page.wait_for_timeout(3000)

        # Stay signed in?
        try:
            page.click("input[id='idBtn_Back']", timeout=5000)
        except:
            pass

        print("[WASTER] Logged in successfully.")
    except Exception as e:
        print("[WASTER] Login failed: ", e)

    # Start command loop
    while True:
        try:
            command = random.choice(COMMANDS)
            print(f"\n[WASTER] Sending command: {command}")

            # Locate text box and enter command
            page.wait_for_selector("textarea", timeout=15000)
            page.fill("textarea", command)
            page.keyboard.press("Enter")

            # Wait for response to generate
            page.wait_for_selector(".cib-serp-main", timeout=25000)
            time.sleep(8)  # Wait for full reply

            # Extract text content
            containers = page.query_selector_all(".cib-serp-main")
            for i, block in enumerate(containers):
                text = block.inner_text()
                print(f"[RESPONSE {i+1}]\n{text}\n")

        except Exception as err:
            print("[WASTER] Error during interaction:", err)

        print(f"[WASTER] Waiting {REFRESH_INTERVAL/60:.1f} minutes before next round...\n")
        time.sleep(REFRESH_INTERVAL)

--- Entry Point ---

if name == "main": run_waster()

