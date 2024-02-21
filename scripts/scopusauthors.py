import requests

def get_publications_by_author_and_year(api_key, author_id, year=None, max_results=100):
    """
    Retrieves publication titles for a given author from Scopus, optionally filtered by year, handling pagination.

    Parameters:
    - api_key (str): Your Scopus API key.
    - author_id (str): The Scopus Author ID for the author.
    - year (int, optional): The publication year to filter by. If None, retrieves all publications.
    - max_results (int): Maximum number of results to retrieve.

    Returns:
    - list: A list of publication titles associated with the author, filtered by year if specified.
    """
    publications = []
    start = 0
    count = 25  # Adjust based on the API's maximum allowed value or your preference

    while True:
        # Constructing the query
        query = f'AU-ID({author_id})'
        if year:
            query += f' AND PUBYEAR IS {year}'

        # Setting up the URL and headers for the request
        url = f'https://api.elsevier.com/content/search/scopus?query={query}&start={start}&count={count}'
        headers = {
            'X-ELS-APIKey': api_key,
            'Accept': 'application/json'
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raises an exception for HTTP errors

            data = response.json()
            entries = data.get('search-results', {}).get('entry', [])

            if not entries:
                break  # Break the loop if no more results are found

            #for item in entries:
            #    title = item.get('dc:title', 'No title available')
            #    publications.append(title)
            
            for item in data.get('search-results', {}).get('entry', []):
                title = item.get('dc:title', 'No title available')
                journal_name = item.get('prism:publicationName', 'No journal name available')
                publications.append((title, journal_name))

            start += count  # Increment 'start' to fetch the next page of results

            # Check if we've reached the maximum number of desired results
            if len(publications) >= max_results or len(entries) < count:
                break  # Exit if we have enough results or fewer results were returned than requested

        except requests.exceptions.RequestException as e:
            print(f'Failed to retrieve data: {e}')
            break  # Exit the loop in case of HTTP errors

    return publications[:max_results]  # Return up to the maximum number of results requested

# Example usage:

# Prompt the user for the Scopus API key
api_key = input("Please enter your Scopus API key: ")

author_id = '55105387900' #J. Gil as an example
year = 2022  # Optional
max_results = 50  # Example: increase if you need more
publications = get_publications_by_author_and_year(api_key, author_id, year, max_results)
#for title in publications:
#    print(title)

#for i, title in enumerate(publications, start=1):  # start=1 if you want the counter to start from 1
#    print(str(i) + " " + title)

for i, (title, journal_name) in enumerate(publications, start=1):
    print(f"{i}. {title} - {journal_name}")
