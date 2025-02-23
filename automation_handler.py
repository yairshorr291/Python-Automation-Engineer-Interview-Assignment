from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import io
from datetime import datetime
import time


def init_driver():
    """
    Initializes a Chrome browser in maximized window mode.

    :return: A WebDriver instance for Chrome
    """
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Open browser in maximized mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    print("Chrome browser initialized successfully.")
    return driver


def set_language_to_english(driver):
    """
    Sets the Google homepage language to English if not already set.

    :param driver: The WebDriver instance controlling the browser
    """
    try:
        language_button = driver.find_element(By.XPATH, '//a[contains(@href, "hl=en")]')
        language_button.click()
        print("Page language set to English.")
    except Exception as e:
        print(f"Error clicking the language button or language already set to English: {e}")


def go_to_google_images(driver):
    """
    Navigates to Google Images using the "Images" button on the homepage.

    :param driver: The WebDriver instance controlling the browser
    """
    try:
        images_button = driver.find_element(By.XPATH, '//a[text()="Images"]')
        images_button.click()
        print("Successfully navigated to Google Images.")
    except Exception as e:
        print(f"Error clicking the Images button: {e}")


def verify_images_page(driver):
    """
    Verifies that the browser is on the Google Images page by checking the URL.

    :param driver: The WebDriver instance controlling the browser
    :raises AssertionError: If the current URL does not indicate the Google Images page
    """
    try:
        assert "imghp" in driver.current_url, "Not on Google Images page."
        print("Successfully reached Google Images page.")
    except AssertionError as e:
        print(f"Error: {e}")
        raise


def search_character_image(driver, character_name):
    """
    Searches for a given character on Google Images.

    :param driver: The WebDriver instance controlling the browser
    :param character_name: The name of the character to search for
    :raises Exception: If the search fails
    """
    try:
        # Locate the search box and clear it
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.clear()

        # Input the character name and submit the search
        search_box.send_keys(f"Rick and Morty {character_name}")
        search_box.submit()

        # Wait for image results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-q] img"))
        )
        print(f"Search completed for: {character_name}")
    except Exception as e:
        raise Exception(f"Failed to complete search for {character_name}.") from e


def calculate_image_position(character_id):
    """
    Calculates the image position in the result grid based on the character ID.

    :param character_id: The ID of the character
    :return: The calculated position in the grid
    """
    if character_id >= 100:
        hundreds = character_id // 100
        ones = character_id % 10
        return hundreds + ones
    elif character_id >= 10:
        tens = (character_id // 10) % 10
        ones = character_id % 10
        return tens + ones
    else:
        return character_id


def wait_for_image_load(image_element, max_retries=10, wait_time=3):
    """
    Waits for an image to fully load by checking its width and height.

    :param image_element: The WebElement representing the image
    :param max_retries: Maximum number of retries (default: 10)
    :param wait_time: Time to wait between retries in seconds (default: 3)
    :return: True if the image loads successfully, False otherwise
    """
    retries = 0
    while retries < max_retries:
        width = image_element.size['width']
        height = image_element.size['height']
        if width > 0 and height > 0:
            return True
        retries += 1
        time.sleep(wait_time)
    return False


def save_image_with_timestamp(image, character_name, character_id):
    """
    Saves an image with a human-readable timestamp.

    :param image: The PIL Image object to save
    :param character_name: The name of the character
    :param character_id: The ID of the character
    :return: The path of the saved image
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    image_path = f"{character_name}_{character_id}-{timestamp}.jpg"
    image.save(image_path, format="JPEG")
    return image_path


def capture_and_save_image(driver, image_position, character_name, character_id, wait_time=10, max_retries=10):
    """
    Captures and saves an image from the specified position in the search results.

    :param driver: The WebDriver instance controlling the browser
    :param image_position: The position of the image in the result grid
    :param character_name: The name of the character
    :param character_id: The ID of the character
    :param wait_time: Time to wait between retries in seconds (default: 10)
    :param max_retries: Maximum number of retries (default: 10)
    :return: A message indicating the status of the operation
    """
    image_divs = driver.find_elements(By.CSS_SELECTOR, "div[data-q] img")
    assert len(image_divs) > 0, f"No images found on Google Images page for {character_name}"

    if len(image_divs) <= image_position:
        return f"No image found at position {image_position} for {character_name}"

    selected_image = image_divs[image_position]

    if not wait_for_image_load(selected_image, max_retries=max_retries, wait_time=wait_time):
        return f"Image not loaded after {max_retries} retries for {character_name}"

    time.sleep(2)
    screenshot_as_bytes = selected_image.screenshot_as_png
    image = Image.open(io.BytesIO(screenshot_as_bytes))
    image_path = save_image_with_timestamp(image, character_name, character_id)
    return f"Screenshot saved as {image_path}"


def process_characters(character_data, wait_time=1, max_retries=10):
    """
    Automates the process for a list of characters: searching, capturing, and saving images.

    :param character_data: A list of dictionaries containing character details
    :param wait_time: Time to wait between retries in seconds (default: 1)
    :param max_retries: Maximum number of retries (default: 10)
    :return: A list of results, including status messages for each character
    """
    driver = init_driver()
    driver.get("https://www.google.com")
    set_language_to_english(driver)
    go_to_google_images(driver)
    verify_images_page(driver)

    results = []

    try:
        for character in character_data:
            character_name = character["name"]
            character_id = character["id"]

            try:
                search_character_image(driver, character_name)
                image_position = calculate_image_position(character_id)
                result = capture_and_save_image(driver, image_position, character_name, character_id, wait_time,
                                                max_retries)
                results.append({"character_name": character_name, "status": result})

            except Exception as e:
                error_message = f"Error processing {character_name}: {str(e)}"
                results.append({"character_name": character_name, "status": error_message})
                print(error_message)

    finally:
        driver.quit()

    return results
