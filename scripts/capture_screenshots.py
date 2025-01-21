import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image

def setup_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def capture_screenshot(driver, url, element_id, filename, wait_time=10):
    try:
        driver.get(url)
        time.sleep(wait_time)  # Wait for dashboard to load completely
        
        # Wait for specific element to be visible
        element = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.ID, element_id))
        )
        
        # Take screenshot
        screenshot_path = os.path.join("docs", "screenshots", filename)
        driver.save_screenshot(screenshot_path)
        
        # Optimize image
        img = Image.open(screenshot_path)
        img.save(screenshot_path, optimize=True, quality=85)
        
        print(f"Screenshot saved: {filename}")
        return True
    except Exception as e:
        print(f"Error capturing {filename}: {str(e)}")
        return False

def main():
    # Create screenshots directory if it doesn't exist
    os.makedirs(os.path.join("docs", "screenshots"), exist_ok=True)
    
    # Setup driver
    driver = setup_chrome_driver()
    
    try:
        # Dashboard URL
        dashboard_url = "http://localhost:8050"
        
        # List of screenshots to capture
        screenshots = [
            ("dashboard-overview", "main-content"),
            ("team-comparison", "team-comparison-chart"),
            ("demand-distribution", "demand-distribution-chart"),
            ("daily-metrics", "daily-metrics-table")
        ]
        
        # Capture each screenshot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        for name, element_id in screenshots:
            filename = f"{name}_{timestamp}.png"
            capture_screenshot(driver, dashboard_url, element_id, filename)
            
        # Capture full page
        filename = f"full-dashboard_{timestamp}.png"
        driver.get(dashboard_url)
        time.sleep(10)  # Wait for everything to load
        driver.save_screenshot(os.path.join("docs", "screenshots", filename))
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
