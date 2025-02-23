import pytest
import random
import requests
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from automation_handler import (
    init_driver,
    set_language_to_english,
    go_to_google_images,
    verify_images_page,
    search_character_image,
    calculate_image_position,
    wait_for_image_load,
    save_image_with_timestamp,
    capture_and_save_image,
    process_characters
)

@pytest.fixture
def driver():
    """
    אתחול דפדפן עבור הבדיקות וסגירתו בסיום.
    """
    driver = init_driver()
    yield driver
    driver.quit()


def test_init_driver():
    """
    בדיקה לפונקציה init_driver.
    """
    driver = init_driver()
    assert driver is not None, "הדפדפן לא אותחל כראוי."
    driver.quit()


def test_set_language_to_english(driver):
    """
    בדיקה לפונקציה set_language_to_english.
    """
    driver.get("https://www.google.com")
    try:
        set_language_to_english(driver)
    except NoSuchElementException:
        pytest.fail("כפתור השפה לא נמצא או שלא בוצע שינוי לשפה האנגלית.")


def test_go_to_google_images(driver):
    """
    בדיקה לפונקציה go_to_google_images.
    """
    driver.get("https://www.google.com")
    set_language_to_english(driver)
    try:
        go_to_google_images(driver)
    except NoSuchElementException:
        pytest.fail("כפתור Images לא נמצא או שלא בוצעה מעבר לדף התמונות.")


def test_verify_images_page(driver):
    """
    בדיקה לפונקציה verify_images_page.
    """
    driver.get("https://www.google.com")
    set_language_to_english(driver)
    go_to_google_images(driver)
    try:
        verify_images_page(driver)
    except AssertionError as e:
        pytest.fail(f"לא הצלחנו לאמת את דף התמונות: {e}")


def test_search_character_image(driver):
    """
    בדיקה לפונקציה search_character_image.
    """
    driver.get("https://www.google.com")
    set_language_to_english(driver)
    go_to_google_images(driver)
    verify_images_page(driver)
    try:
        search_character_image(driver, "Rick Sanchez")
    except Exception as e:
        pytest.fail(f"חיפוש הדמות נכשל: {e}")


def test_calculate_image_position():
    """
    בדיקה לפונקציה calculate_image_position.
    """
    assert calculate_image_position(123) == 4, "חישוב המיקום עבור ID 123 נכשל."
    assert calculate_image_position(45) == 9, "חישוב המיקום עבור ID 45 נכשל."
    assert calculate_image_position(7) == 7, "חישוב המיקום עבור ID 7 נכשל."


def test_wait_for_image_load(driver):
    """
    בדיקה לפונקציה wait_for_image_load.
    """
    driver.get("https://www.google.com")
    set_language_to_english(driver)
    go_to_google_images(driver)
    verify_images_page(driver)
    search_character_image(driver, "Rick Sanchez")

    images = driver.find_elements(By.CSS_SELECTOR, "div[data-q] img")
    assert len(images) > 0, "לא נמצאו תמונות בתוצאות החיפוש."

    loaded = wait_for_image_load(images[0])
    assert loaded, "התמונה לא נטענה בהצלחה."


def test_save_image_with_timestamp():
    """
    בדיקה לפונקציה save_image_with_timestamp.
    """
    from PIL import Image

    # יצירת תמונה ריקה לבדיקות
    img = Image.new('RGB', (100, 100), color='red')
    image_path = save_image_with_timestamp(img, "Rick Sanchez", 123)
    assert "Rick Sanchez_123" in image_path, "שם הקובץ שנשמר אינו תואם."
    assert image_path.endswith(".jpg"), "הקובץ שנשמר אינו בפורמט JPG."


@pytest.mark.parametrize("character_name, character_id", [
    ("Rick Sanchez", 123),
    ("Morty Smith", 45),
    ("Summer Smith", 78),
    ("Jerry Smith", 90),
    ("Beth Smith", 33),
])
def test_capture_and_save_image(driver, character_name, character_id):
    """
    בדיקה לפונקציה capture_and_save_image עבור דמות נתונה.
    """
    driver.get("https://www.google.com")
    set_language_to_english(driver)
    go_to_google_images(driver)
    verify_images_page(driver)
    search_character_image(driver, character_name)

    images = driver.find_elements(By.CSS_SELECTOR, "div[data-q] img")
    assert len(images) > 0, f"לא נמצאו תמונות בתוצאות החיפוש עבור {character_name}."

    result = capture_and_save_image(driver, 0, character_name, character_id)
    assert "Screenshot saved" in result, f"התמונה לא נשמרה בהצלחה עבור {character_name}."



@pytest.mark.parametrize("num_characters", [5])
def test_process_characters(driver, num_characters):
    """
    בדיקה לפונקציה process_characters.
    """
    character_data = [
        {"name": "Rick Sanchez", "id": 123},
        {"name": "Morty Smith", "id": 45},
        {"name": "Summer Smith", "id": 78},
        {"name": "Jerry Smith", "id": 90},
        {"name": "Beth Smith", "id": 33},
    ]
    results = process_characters(character_data, wait_time=1, max_retries=10)
    assert len(results) == len(character_data), "לא כל הדמויות עובדו בהצלחה."
    for result in results:
        assert "Screenshot saved" in result["status"] or "Error" in result["status"], f"בעיה עם הדמות: {result}"
