# Functions 
from src.wait import wait, wait_for_selector

def make_reservation(page, button):
  button.click() # Make res
  print("(Msg): make_reservation -> Clicked reservation button")
  
  # Pause
  page.pause()
  return