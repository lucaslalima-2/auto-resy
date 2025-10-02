# Libaries
from playwright.sync_api import sync_playwright
from datetime import datetime

# Functions
from src.check_availability import check_availability
from src.make_reservation import make_reservation

# Global variables
location = "New York"
restuarant = "Convivium Osteria"
date = "October 31, 2025"
time_window = ["9:35:00 PM", "10:00 PM"]
party_size = 4

# Function
with sync_playwright() as p:
  # Start session
  browser = p.chromium.launch(headless=False, slow_mo=300)  # Set headless=False for debugging
  context = browser.new_context()
  page = context.new_page()

  # Fetch availability
  page, resbutton = check_availability(page, location, restuarant, date, time_window, party_size)

  # Button click
  if resbutton:
      print(f"(Debugger): Found reservation button → {resbutton}")
      make_reservation(page, resbutton)
  else:
      print("(Debugger): No reservation found in time window.")
      page.pause()