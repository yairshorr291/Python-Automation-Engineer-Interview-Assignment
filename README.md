# Interview Assignment


_**Task Overview**:_
In this assignment, you will demonstrate your skills in API interaction, automation testing with
Selenium, and test organization using Pytest. You are expected to interact with the Rick and Morty
API, perform web automation using Selenium WebDriver, and follow the given instructions to
complete the task.
Delivery Date – as agreed in the mail/phone call.

**Assignment Steps**:

**1. API Interaction**
1. Get the base URL of the Rick and Morty API and assign it to a variable called 'base_url'.
2. Fetch all episodes using the 'base_url'.
3. Randomly choose one episode from the list where the number of characters exceeds or
equals 30.
4. Print the name of the selected episode and the number of characters in it.
5. Randomly select two characters from the chosen episode and store them as Character
objects (each object should include attributes like id, name, status, species, location, etc.).
o Bonus: Fetch both characters simultaneously.
6. For each character, write a friendly introduction to a text file named
characters_introduction.txt:
o Format: "Hi! I'm CHARACTER_NAME, My ID is CHARACTER_ID, I'm from
LOCATION_NAME, etc."

**2. UI Automation (Selenium)**
Wrap the following steps in a Pytest test.
1. Open Chrome Browser:
   o Ensure the window is maximized.
   o Navigate to Google.com, and use English as the browser's language.
2. Navigate to Google Images:
   o Bonus: Access the "Images" section using the link button in the top-right corner of
   the Google homepage.
3. Search for the First Character:
   o Search for 'Rick and Morty FIRST_CHARACTER_NAME'.
4. Click on the Correct Image:

   o Using the first character's ID, calculate the correct image position using the
   hundreds/tens digit plus the ones digit. (e.g. ID = 123 => position = 1+3)
   ▪ If the character’s ID has fewer than 3 digits, use the tens and ones digits for
   grid calculation.

   o Ensure the selected image is under a Div element with the attribute data-q.
5. Take a Screenshot:

   o Capture the selected image in a screenshot and save it as FIRST_CHARACTER_NAME-
   ID-TIMESTAMP.jpg.
   o The TIMESTAMP must be human-readable, containing the screenshot's date and
time.

6. Navigate to the Second Character's Image:
   o Retrieve the URL of the second character’s image and repeat the screenshot process.
   o Bonus: Capture only the specific image without background elements.
7. Close the Browser.

**3. Verification and Assertion:**
1. Verify that the locations of the two selected characters are the same – using Python assert.
2. Assertions:
   o If the locations differ, print:
   "FIRST_CHARACTER_NAME from FIRST_CHARACTER_LOCATION and
   SECOND_CHARACTER_NAME from SECOND_CHARACTER_LOCATION."
   o If the locations match, print:
   "Both characters are from LOCATION_NAME."

**Additional Guidelines:**
1. Pytest: Ensure the UI automation portion is wrapped in Pytest functions.
   o Bonus: Use Page Object Model (POM) design to structure your Selenium code.
2. Code Quality:
   o Your code should be clean, maintainable, and well-commented.
   o Ensure the usage of functions or classes wherever appropriate.
   o Avoid hardcoding values unless necessary.
3. Requirements:
   o Use the requests library for API interaction.
   o Use selenium for web automation, with Chrome WebDriver.


_**In my words:**_

The project integrates API handling and browser automation. The API Handler retrieves data from the Rick and Morty API—fetching episodes, filtering them by a minimum character count, randomly selecting an episode, retrieving details for two characters, writing a character introduction file, and verifying that both characters are from the same location. The Automation Handler uses Selenium to control a Chrome browser: it opens the browser in fullscreen, sets the language to English, navigates to Google Images, searches for character images, calculates the correct image position based on the character ID, waits for images to load fully, and captures screenshots that are saved with timestamped filenames using Pillow and datetime. The Main Application orchestrates these components, while testing is managed with Pytest.

Key libraries and tools include:

**Requests** (for HTTP API calls)
**Random** (for random selection)
**Selenium** with webdriver-manager (for browser automation)
**Pillow** (PIL) (for image processing)
**Datetime** (for timestamping)
**Pytest** (for testing)
This modular design ensures maintainability, ease of testing, and the flexibility to extend the project further.


**📁 Final Code Architecture**
*main.py*
*Orchestrates the overall flow of the project.*
-Calls fetch_characters() to retrieve character data from the Rick and Morty API.
-Passes the characters to process_characters() to handle automation tasks.
-Prints the results (success or failure for each character).
-Verifies if the two characters originate from the same location after automation (to ensure the process is not interrupted).

*api_handler.py*
*Handles all logic related to data fetching and processing from the Rick and Morty API.*
Functions:
-fetch_episodes, filter_episodes_with_characters, select_random_episode
-fetch_character_details: retrieves full character data from their URLs
-write_character_introduction: creates a text file introducing the characters
-verify_locations: checks if both characters are from the same location
-fetch_characters: manages the entire data fetching pipeline
*Why it's separate: Makes it easier to test, mock, and debug API calls independently from the automation logic.*

*automation_handler.py*
*Handles browser automation using Selenium to search and capture character images from Google Images.*
Functions:
-init_driver: initializes Chrome in fullscreen
-set_language_to_english: ensures Google is in English
-go_to_google_images: navigates via the top-right “Images” button
-verify_images_page: confirms that the browser is on Google Images
-search_character_image: clears and searches the character
-calculate_image_position: calculates index in the image grid
-wait_for_image_load: checks that image is visible and loaded
-capture_and_save_image: takes a screenshot of the image and saves it
-process_characters: full automation loop over all selected characters
*Why it's separate: It keeps the automation process clean, modular, and testable on its own.*

*test_automation.py*
*Contains all the Pytest-based unit and integration tests.*
-Uses fixtures to set up and tear down the browser driver.
-Every custom function is covered: from driver initialization to image capture and full process execution.
-Allows simulation of success/failure cases.
*Why it's separate: Keeps testing logic out of the main codebase. Supports test automation and CI/CD.*

**💡 Why This Architecture?**
-Separation of concerns: Each module has a single responsibility.
-Maintainability: Easy to isolate and fix bugs.
-Testability: Modules can be tested independently or as a whole.
-Extensibility: Easy to add new features like multilingual support, advanced filtering, or machine learning models.
-Clean code: Follows best practices for readability and reuse.

