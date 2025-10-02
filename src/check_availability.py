# Libraries
import os
from playwright.sync_api import sync_playwright

# Functions
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Handles opening popup
def avoid_popup(page):
  page.wait_for_timeout(2000) # wait 2s for pop up
  try: 
    if page.is_visible("[data-test-id='announcement-button-secondary']"):
      print("(W) check_availability -> avoid_popup -> Pop-up Detected. Avoiding.")
      page.click("[data-test-id='announcement-button-secondary']")
      page.wait_for_timeout(1000) # wait 2s for closing
  except Exception as e:
    print(f"check_availability -> avoid_popup -> No popup found. Handling: {e}.")
    return

# Adds credentials to login
def add_credentials(page):
  email = os.getenv("RESY_USERNAME")
  password = os.getenv("RESY_PASSWORD")
  page.fill("input[name='email']", email)
  page.fill("input[name='password']", password)
  page.click("button[type='submit']")
  return

# Navigates resy page
def check_availability(restaurant, date, time, party_size):
  print(f"Checking availability for {restaurant} on {date} at {time} for {party_size} people...")

  with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=300)  # Set headless=False for debugging
    context = browser.new_context()
    page = context.new_page()
    # Go through username & password
    try:
      # Open page
      page.goto("https://resy.com")
      avoid_popup(page)

      # Click login
      page.click("[data-test-id='menu_container-button-log_in']") # click login button
      page.click("button.SmsViewSignInButton") # clicks sign-in option

      # Credentials
      # page.wait_for_selector("input[name='email']", timeout=5000)
      add_credentials(page)

      # Pause
      page.pause()
    except Exception as e:
      print(f"check_availability -> error when opening page: \n {e}")
      page.pause()
      return
      