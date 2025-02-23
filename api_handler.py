import requests
import random

# Constants
NumOfCharactersInEp = 30  # Minimum number of characters in an episode
NumOfCharactersToStore = 2  # Number of characters to store from the selected episode
PageFound = 200  # Status code indicating a successful API request


def fetch_episodes(base_url):
    """
    Fetches all episodes from the API.

    :param base_url: The base URL of the API
    :return: A list of episodes retrieved from the API
    :raises Exception: If the API request fails
    """
    response = requests.get(f"{base_url}/episode")
    if response.status_code != PageFound:
        raise Exception("Failed to fetch episodes")
    return response.json()["results"]


def filter_episodes_with_characters(episodes, min_characters):
    """
    Filters episodes to include only those with at least a specified number of characters.

    :param episodes: A list of episodes
    :param min_characters: The minimum number of characters required per episode
    :return: A list of episodes that meet the minimum character requirement
    """
    return [ep for ep in episodes if len(ep["characters"]) >= min_characters]


def select_random_episode(episodes):
    """
    Selects a random episode from the provided list.

    :param episodes: A list of episodes
    :return: A randomly selected episode
    """
    return random.choice(episodes)


def fetch_character_details(character_urls, num_characters_to_store):
    """
    Fetches character details from a list of character URLs.

    :param character_urls: A list of character URLs
    :param num_characters_to_store: The number of characters to retrieve details for
    :return: A list of character details
    :raises Exception: If fetching character data fails
    """
    selected_characters = random.sample(character_urls, num_characters_to_store)
    character_data = []
    for char_url in selected_characters:
        response = requests.get(char_url)
        if response.status_code == PageFound:
            character_data.append(response.json())
        else:
            raise Exception(f"Failed to fetch character data from {char_url}")
    return character_data


def write_character_introduction(character_data, file_name="characters_introduction.txt"):
    """
    Writes character introductions to a text file.

    :param character_data: A list of character details
    :param file_name: The name of the file to write to (default is 'characters_introduction.txt')
    :return: None
    """
    with open(file_name, "w") as file:
        for char in character_data:
            introduction = (
                f"Hi! I'm {char['name']}, My ID is {char['id']}, "
                f"I'm from {char['location']['name']}, "
                f"My status is {char['status']}, and I'm a {char['species']}.\n"
            )
            file.write(introduction)
    print(f"Character introductions written to '{file_name}'")


def verify_locations(character_data):
    """
    Verifies if the locations of two characters are the same and prints the result.

    :param character_data: A list of character details (expected to include exactly two characters)
    :return: None
    :raises AssertionError: If the locations of the two characters are different
    """
    first_character = character_data[0]
    second_character = character_data[1]

    first_name = first_character["name"]
    second_name = second_character["name"]

    first_location = first_character["location"]["name"]
    second_location = second_character["location"]["name"]

    if first_location == second_location:
        print(f"Both characters are from {first_location}.")
    else:
        print(f"{first_name} from {first_location} and {second_name} from {second_location}.")

    assert first_location == second_location, \
        f"{first_name} from {first_location} and {second_name} from {second_location}."


def fetch_characters():
    """
    Orchestrates the full process: fetching characters, creating an introduction file,
    and verifying their locations.

    :return: A list of character details
    :raises Exception: If no valid episodes are found
    """
    base_url = "https://rickandmortyapi.com/api"

    # Step 1: Fetch all episodes
    episodes = fetch_episodes(base_url)

    # Step 2: Filter episodes with at least NumOfCharactersInEp characters
    valid_episodes = filter_episodes_with_characters(episodes, NumOfCharactersInEp)
    if not valid_episodes:
        raise Exception(f"No episode with at least {NumOfCharactersInEp} characters found.")

    # Step 3: Select a random episode
    selected_episode = select_random_episode(valid_episodes)
    print(f"Selected Episode: {selected_episode['name']}, Characters: {len(selected_episode['characters'])}")

    # Step 4: Fetch character details
    character_data = fetch_character_details(selected_episode["characters"], NumOfCharactersToStore)

    # Step 5: Write character introductions to a file
    write_character_introduction(character_data)

    return character_data
