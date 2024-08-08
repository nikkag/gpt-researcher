# Brave Search Retriever

# libraries
import os
import requests


class BraveSearch():
    """
    Brave Search Retriever
    """
    def __init__(self, query):
        """
        Initializes the BraveSearch object
        Args:
            query:
        """
        self.query = query
        self.api_key = self.get_api_key()

    def get_api_key(self):
        """
        Gets the Brave API key
        Returns:

        """
        try:
            api_key = os.environ["BRAVE_API_KEY"]
        except KeyError:
            raise Exception("Brave API key not found. Please set the BRAVE_API_KEY environment variable.")
        return api_key

    def search(self, max_results=7):
        """
        Searches the query
        Returns:

        """
        if len(self.query) > 400:
            print(f"The query length of {len(self.query)} exceeds the maximum query length is 400")
            return []

        print("Searching with query {0}...".format(self.query))
        """Useful for general internet search queries using the Brave API."""

        # Search the query
        url = "https://api.search.brave.com/res/v1/web/search"

        headers = {
            'X-Subscription-Token': self.api_key,
            # 'Content-Type': 'application/json'
        }
        params = {
            "q": self.query,
        }

        resp = requests.get(url, headers=headers, params=params)

        # Preprocess the results
        if resp is None:
            return []
        try:
            search_results = resp.json()
        except Exception:
            return []
        if search_results is None:
            return []
        if 'error' in search_results:
            print(f'error in these results: {search_results}')
            raise Exception('Brave rate limited the request')

        results = search_results["web"]["results"]
        search_results = []

        # Normalize the results to match the format of the other search APIs
        for result in results:
            # skip youtube results
            if "youtube.com" in result["url"]:
                continue
            search_result = {
                "title": result["title"],
                "href": result["url"],
                "body": result["description"],
            }
            search_results.append(search_result)

        return search_results
