# Libraries
import os
from playwright.sync_api import sync_playwright

def run_resy_bot():
	print("Starting Resy bot...")
	email = os.getenv("RESY_USERNAME")
	password = os.getenv("RESY_PASSWORD")
	maxtimeout=1000

	with sync_playwright() as p:
		browser = p.chromium.launch(headless=False)  # Set headless=True for silent mode
		page = browser.new_page()
		page.goto("https://resy.com")

		# Click login button
		page.click("text=Log In")

		# Go through username & password
		try:
			page.click("text=Use Email and Password instead", timeout=maxtimeout)
		except:
			pass

		# Log in credentials
		page.fill("input[name='email']", email) # Fill in credentials
		page.fill("input[name='password']", password)
		page.click("button[type='submit']")
		page.wait_for_selector("input.react-autosuggest__input")

		# Finds search field
		search_input = page.locator("input.react-autosuggest__input")
		search_input.wait_for(state="visible")
		search_input.wait_for(state="attached")
		search_input.wait_for(state="enabled")
		search_input.fill("TESTINGFORLUKE")

		# Pause for inspection
		input("Press Enter to close the browser...")
		browser.close()
		
		# # For targetting & debug
		# print(page.content())

		# print("Logged in successfully.")
		# browser.close()

	return "Login complete."