# Libraries
import os
from datetime import datetime
from playwright.sync_api import sync_playwright

# Functions
from dotenv import load_dotenv
from src.wait import wait, wait_for_selector

# Load environment variables
load_dotenv()

# Handles opening popup
def avoid_popup(page):
  wait(page)
  try: 
    if page.is_visible("[data-test-id='announcement-button-secondary']"):
      print("(W) check_availability -> avoid_popup -> Pop-up Detected. Avoiding.")
      page.click("[data-test-id='announcement-button-secondary']")
      wait(page)
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
  wait_for_selector(page, "text=New York")

  # Step 3: Click on "New York"
  page.click("text=New York")
  return

# Navigates resy page
def check_availability(page, location, restaurant, date, time_window, party_size):
  print(f"(Msg) check_availability -> Checking availability for {restaurant} on {date} at {time_window} for {party_size} people...")
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
    wait(page, 8000)

    # Update location
    set_location(page)

    # Wait for location update
    wait(page)

    # Search
    page.fill("input.react-autosuggest__input", restaurant)
    wait(page)

    # Click the input again to avoid hover suggestions
    page.click("input.react-autosuggest__input")

    # Enter search
    page.keyboard.press("Enter") # Press enter key

    # Click first link
    wait_for_selector(page, "[data-test-id='search-result-link-details']", 6000)

    # Click the first result
    page.click("[data-test-id='search-result-link-details']")

    # Update party size
    page.select_option("[data-test-id='dropdown-group-party-size']", value=str(party_size))

    # Update date
    page.click("#DropdownGroup__selector--date--selection")

    # Need to convert input date to this format
    wait_for_selector(page, f"button[data-test-id='ResyCalendar-day-data'][aria-label='{date}.']")
    page.click(f"button[data-test-id='ResyCalendar-day-data'][aria-label='{date}.']")

    # Checks availability on the time_window
    st = datetime.strptime(time_window[0], "%I:%M %p")
    et = datetime.strptime(time_window[1], "%I:%M %p")
    # Get all reservation options
    buttons = page.query_selector_all("button[data-testid^='reservation-button-rgs://']")
    for button in buttons:
      time_text = button.query_selector(".ReservationButton__time").inner_text().strip() # Get time
      button_time = datetime.strptime(time_text, "%I:%M %p") # reformat
      if st <= button_time <= et:
        print(f"(Msg): check_availability -> Found availability: {button_time}")
        return page, button
    return page, None # No reservation found

  except Exception as e:
    print(f"check_availability -> error when opening page: \n {e}")
    page.pause()
    return