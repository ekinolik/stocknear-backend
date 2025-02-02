from urllib.parse import urlparse
import os
import json
import re

# Directory to store sample responses
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MOCK_RESPONSES_DIR = os.path.join(BASE_DIR, "mock_responses")

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

async def mock_fetch_data(url, _headers=None):
    """Fetch mock data from JSON files based on the URL."""

    # Parse URL to extract hostname and path
    parsed_url = urlparse(url)
    service_name = parsed_url.netloc.replace(".", "_")  # Convert dots to underscores
    path = parsed_url.path + ("?" + parsed_url.query if parsed_url.query else "")


    # Determine the mock file based on service name
    mock_file_path = os.path.join(MOCK_RESPONSES_DIR, f"{service_name}.json")

    # Check if the mock file exists
    if not os.path.exists(mock_file_path):
        raise FileNotFoundError(f"Mock file not found: {mock_file_path}")

    # Load the JSON mock data
    with open(mock_file_path, "r") as file:
        mock_data = json.load(file)

    # Find all matching paths (substrings within the requested path or matching the regex)
    matching_paths = [key for key in mock_data.keys() if re.compile(key).fullmatch(path) is not None or path.startswith(key)]
    if not matching_paths:
        raise ValueError(f"No mock response found for path: {path}")

    # Find the longest matching path
    longest_match = max(matching_paths, key=len)

    # Ensure there's no duplicate longest match
    if matching_paths.count(longest_match) > 1:
        raise ValueError(f"Multiple longest matching paths found for: {path}")

    return mock_data[longest_match]

async def mock_fetch_data_json(url, _headers=None):
    return await mock_fetch_data(url, _headers)


async def mock_fetch_data_response(url, _headers=None):
    res = await mock_fetch_data(url, _headers)
    return MockResponse(res, 200)
