# Libaries
from playwright.sync_api import sync_playwright
from datetime import datetime

# Functions
from src.check_availability import check_availability

# Global variables
location = "New York"
restuarant = "Sawa"
date = "October 30, 2025"
time_window = ["7:00 PM", "9:00 PM"]
party_size = 3

# Function
with sync_playwright() as p:
  # Start session
  browser = p.chromium.launch(headless=False, slow_mo=300)  # Set headless=False for debugging
  context = browser.new_context()
  page = context.new_page()

  # Fetch availability
  page, res_button = check_availability(page, location, restuarant, date, time_window, party_size)

  # Optional: pause for inspection
  if res_button:
      print(f"(Debugger): Found reservation button → {res_button}")
      page.pause()
  else:
      print("(Debugger): No reservation found in time window.")