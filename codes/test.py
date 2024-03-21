from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time
import os
import requests
driver = webdriver.Chrome()

# Navigate to the webpage containing the link to the PDF
driver.get("https://www.nissan.in/vehicles/brochures.html")
pdf_links = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href$=".pdf"]'))
)
download_folder = "downloaded_pdfs"
os.makedirs(download_folder, exist_ok=True)

# Loop through the PDF links and download each PDF
for index, pdf_link in enumerate(pdf_links):
    # Get the PDF URL
    pdf_url = pdf_link.get_attribute('href')

    # Use requests to download the PDF
    response = requests.get(pdf_url)

    # Save the PDF to a local file with a unique name
    pdf_filename = os.path.join(download_folder, f"downloaded_file_{index + 1}.pdf")
    with open(pdf_filename, 'wb') as pdf_file:
        pdf_file.write(response.content)

# Wait for some time to allow the download to complete
time.sleep(5)  # You may adjust the duration based on the expected download time

# Close the browser
driver.quit()
