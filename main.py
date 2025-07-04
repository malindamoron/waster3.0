import os
import time
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError

EMAIL = "shashisunil3333@gmail.com"
PASSWORD = "WWW.YOUTUBE.COM"  # Replace with actual password

COMMANDS = ["today's news", "what if news", "future releases"]
SAVE_FOLDER = "hippo"  # Don't use absolute like /hippo unless necessary

# Ensure folder exists
Path(SAVE_FOLDER).mkdir(parents=True, exist_ok=True)

def save_response(title, text):
    safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "_")).rstrip()
    date = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = os.path.join(SAVE_FOLDER, f"{safe_title}_{date}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)

def login_to_copilot(page):
    try:
        page.goto("https://copilot.microsoft.com/", timeout=60000)

        if "sign in" in page.content().lower():
            print("[WASTER] Sign-in page detected.")
            page.click("text=Sign in")
            page.wait_for_selector('input[type="email"]', timeout=15000)
            page.fill('input[type="email"]', EMAIL)
            page.click('input[type="submit"]')

            page.wait_for_selector('input[type="password"]', timeout=15000)
            page.fill('input[type="password"]', PASSWORD)
            page.click('input[type="submit"]')

            try:
                page.wait_for_selector('input[type="submit"]', timeout=5000)
                page.click('input[type="submit"]')  # Stay signed in
            except:
                pass

            print("[WASTER] Login successful.")
        else:
            print("[WASTER] Already logged in or no login prompt found.")
    except Exception as e:
        print(f"[WASTER] Login failed: {e}")

def ask_question(page, question):
    try:
        textarea = page.get_by_test_id("composer-input")
        textarea.wait_for(state="visible", timeout=20000)
        textarea.fill(question)
        textarea.press("Enter")
        print(f"[WASTER] Sent: {question}")

        page.wait_for_selector(".cib-serp-main", timeout=30000)
        response = page.locator(".cib-serp-main").inner_text()
        return response
    except TimeoutError:
        print("[WASTER] Timeout waiting for Copilot response.")
        return "[ERROR] Copilot did not respond."

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--no-sandbox",
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--disable-software-rasterizer",
                "--single-process",
                "--start-maximized"
            ]
        )
        context = browser.new_context()
        page = context.new_page()

        login_to_copilot(page)

        while True:
            for command in COMMANDS:
                print(f"[WASTER] Asking: {command}")
                response = ask_question(page, command)
                save_response(command, response)
                print(f"[WASTER] Response for '{command}' saved.")
                time.sleep(10)

            print("[WASTER] Sleeping 3.5 minutes...\n")
            time.sleep(210)

if __name__ == "__main__":
    main()
