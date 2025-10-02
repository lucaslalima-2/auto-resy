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

# Sets location
def set_location(page):
  # Step 1: Click the location selector
  page.click("button[aria-label^='Location']")  # Matches "Location Jersey City"

  # Step 2: Wait for the location list to appear
  page.wait_for_selector("text=New York", timeout=5000)

  # Step 3: Click on "New York"
  page.click("text=New York")
  return

# Navigates resy page
def check_availability(location, restaurant, date, time, party_size):
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
      add_credentials(page)

      # Wait for login to complete
      page.wait_for_timeout(8000) # Give 8 seconds

      # Update location
      set_location(page)

      # Wait for location update
      page.wait_for_timeout(4000) # Give 4 seconds

      # Search
      page.fill("input.react-autosuggest__input", restaurant)
      page.wait_for_timeout(4000) # Give 4 seconds
      page.keyboard.press("Enter") # Press enter key

      # Need to follow this first href:
      # <a class="Link SearchResult__container-link" href="cities/new-york-ny/venues/sawa?date=2025-10-02&amp;seats=2" data-test-id="search-result-link-details" tabindex="0"><h3 class="SearchResult__venue-name">Sawa</h3></a>

      # Pause
      page.pause()
    except Exception as e:
      print(f"check_availability -> error when opening page: \n {e}")
      page.pause()
      return