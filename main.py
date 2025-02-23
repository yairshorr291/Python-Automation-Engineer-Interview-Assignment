from api_handler import fetch_characters, verify_locations
from automation_handler import process_characters

def main():
    """
    תהליך שלם: שליפת דמויות מה-API, יצירת קובץ הכרות, וביצוע אוטומציה על הדמויות.
    """
    # שלב 1: שליפת דמויות מה-API
    character_data = fetch_characters()

    if not character_data:
        print("No characters fetched from API.")
        return

    # שלב 2: ביצוע אוטומציה על הדמויות
    results = process_characters(character_data)
    for result in results:
        print(f"{result['character_name']}: {result['status']}")

    # בדיקת המיקומים של הדמויות
    verify_locations(character_data)


if __name__ == "__main__":
    main()
