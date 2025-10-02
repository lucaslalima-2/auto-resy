# Functions 
from src.wait import wait, wait_for_selector

def make_reservation(page, button):
  # Select time
  button.click()
  print("(Msg): make_reservation -> Clicked time-slot button")
  
  # Wait for new window (iFrame)
  wait_for_selector(page, "iframe[title='Resy - Book Now']")
  iframe_element = page.query_selector("iframe[title='Resy - Book Now']")
  frame = iframe_element.content_frame()

  # Click reserve
  reserve_button = frame.locator("button:has-text('Reserve Now')")
  reserve_button.wait_for(state="visible", timeout=10000)
  reserve_button.click()
  print("(Msg): make_reservation -> Clicked 'Reserve Now'")

  # Click Confirm
  try:
    confirm_button = frame.locator("button:has-text('Confirm')")
    reserve_button.scroll_into_view_if_needed()
    confirm_button.wait_for(state="visible", timeout=5000)
    confirm_button.click() # can try reserve_button.click(force=True)
    print("(Msg): make_reservation -> Clicked 'Confirm'")
  except Exception as e:
    print(f"(E): Confirm button not found -> {e}")
    page.screenshot(path="reserve_button_error.png") 

  # Pause
  page.pause()
  return