def wait(page, wait_time=2000):
  page.wait_for_timeout(wait_time) # Give 4 seconds
  return

def wait_for_selector(page, selector, timeout=5000):
  page.wait_for_selector(selector, timeout=timeout)
  return