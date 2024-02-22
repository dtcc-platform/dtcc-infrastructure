# Copyright(C) 2023 Vasilis Naserentin
# Licensed under the MIT License


# Bibliometric fetching utilities for Scopus and Google Scholar -
# Regarding Google Scholar check https://stackoverflow.com/questions/62938110/does-google-scholar-have-an-api-available-that-we-can-use-in-our-research-applic


import requests, pandas as pd
import time



#The function fetch_scopus_id_from_orcid is not working at the moment, due to the Elsevier API.
def fetch_scopus_id_from_orcid(orcid, api_key):
    """
    Fetches the Scopus Author ID for a given ORCID.

    Parameters:
    - orcid (str): The ORCID of the author.
    - api_key (str): Your Scopus API key.

    Returns:
    - str: The Scopus Author ID, or None if not found.
    """
    base_url = "https://api.elsevier.com/content/search/author"
    base_url = "https://api.elsevier.com/content/ author/orcid/{orcid}"
    #query = f'ORCID({orcid})'
    headers = {
        'X-ELS-APIKey': api_key,
        'Accept': 'application/json'
    }

    try:
        response = requests.get(f"{base_url}?query={query}", headers=headers)
        response.raise_for_status()  # Raises an exception for HTTP errors
        
        # Assuming the first result is the correct author, adjust as necessary
        data = response.json()
        scopus_id = data.get('search-results', {}).get('entry', [{}])[0].get('dc:identifier')
        
        return scopus_id

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Scopus ID for ORCID {orcid}: {e}")
        return None


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
api_key = '15dc1f98cfe0f0dd91f339dd2320ab97'
# Data for ORCIDs and names

# 0000-0002-1547-4773 13411014700 Anders Logg
# 0000-0001-6671-2578 55105387900 J. Gil
# 0000-0002-3485-9329 57211082959 Vasilis Naserentin
# 0000-0002-5401-5721 8517200800 Minna Kastrunen
# 0000-0001-8493-9231 6506205281 57196467108 Beata Wastberg #second Scopus ID seems more correct
# 0000-0002-9031-4323 14323749200 Liane Thuvander 
# 0000-0002-1674-6785 29068142600 Leonardo Rosado 
# 0000-0002-9756-2362 57140631100 Alexander Hollberg
# 0000-0002-2193-6639 50162059900 Lars Marcus
# 0000-0002-4000-9064 57142025000 Meta Berghauser Pont  
# 0000-0002-0067-1985 6701469399 Monica Billger 
# 0000-0003-2375-1328 57972443500 Franziska Hunger  
# 0000-0001-8561-1588 57222349653 Sanjay Somanath 
# 0000-0003-4330-6133 57218887730 Alex G.  
# 0000-0001-8713-0083 56383888200 Malgorzata Zboinska
# 0000-0002-3706-8485 10041142400 Mattias Ruppe 
# 0000-0002-8630-8262 56568263500 Dag Wastberg 
# 0000-0001-6552-4276 57207795648 Jonas Runberger 
# 0000-0001-7723-2801 57211528948 Mikael Johansson 
# 0000-0003-1263-4062 57195324485 Amardeep Amavasai 
# 0000-0003-3252-1495 56396851400 Lars Harrie
#                     7101892857  Graham Kemp
# UniSalento
#                     57209449951 Antonella Longo
####Keep out for now 0000-0002-8277-9390  24484232300 Marco Salvatore Zappatore
#0000-0002-1082-7293  56070325200 Angelo Martella
#                     58618232000 Amro Issam Hamed Attia Ramadan
# 0000-0001-9751-9367 58618232100 Cristian Martella 
# GATE
#57939562600 Radostin Mitkov
#35932460300 Dessislava Petrova
#57219490991 Mariya Pantusheva
#57193733342 Peter Hristov
#57467223200 Evgeny Shirinyan

import pandas as pd

# Complete data including ORCIDs (where available), Scopus IDs, and names
data = [
    ("0000-0002-1547-4773", "13411014700", "Anders Logg"),
    ("0000-0001-6671-2578", "55105387900", "Jorge Gil"),
    ("0000-0002-3485-9329", "57211082959", "Vasilis Naserentin"),
    ("0000-0002-5401-5721", "8517200800", "Minna Kastrunen"),
    ("0000-0001-8493-9231", "57196467108", "Beata Wastberg"),
    ("0000-0002-9031-4323", "14323749200", "Liane Thuvander"),
    ("0000-0002-1674-6785", "29068142600", "Leonardo Rosado"),
    ("0000-0002-9756-2362", "57140631100", "Alexander Hollberg"),
    ("0000-0002-2193-6639", "50162059900", "Lars Marcus"),
    ("0000-0002-4000-9064", "57142025000", "Meta Berghauser Pont"),
    ("0000-0002-0067-1985", "6701469399", "Monica Billger"),
    ("0000-0003-2375-1328", "57972443500", "Franziska Hunger"),
    ("0000-0001-8561-1588", "57222349653", "Sanjay Somanath"),
    ("0000-0003-4330-6133", "57218887730", "Alex Gonzalez Caceres"),
    ("0000-0001-8713-0083", "56383888200", "Malgorzata Zboinska"),
    ("0000-0002-3706-8485", "10041142400", "Mattias Ruppe"),
    ("0000-0002-8630-8262", "56568263500", "Dag Wastberg"),
    ("0000-0001-6552-4276", "57207795648", "Jonas Runberger"),
    ("0000-0001-7723-2801", "57211528948", "Mikael Johansson"),
    ("0000-0003-1263-4062", "57195324485", "Amardeep Amavasai"),
    ("0000-0003-3252-1495", "56396851400", "Lars Harrie"),
    (None, "7101892857", "Graham Kemp"),
    (None, "57209449951", "Antonella Longo"),
    ("0000-0002-1082-7293", "56070325200", "Angelo Martella"),
    (None, "58618232000", "Amro Issam Hamed Attia Ramadan"),
    ("0000-0001-9751-9367", "58618232100", "Cristian Martella"),
    (None, "57939562600", "Radostin Mitkov"),
    (None, "35932460300", "Dessislava Petrova"),
    (None, "57219490991", "Mariya Pantusheva"),
    (None, "57193733342", "Peter Hristov"),
    (None, "57467223200", "Evgeny Shirinyan")
]

# Creating the DataFrame
df = pd.DataFrame(data, columns=["ORCID", "Scopus ID", "Name"])

# Displaying the DataFrame to verify
print(df)

# Optionally, you might want to save this DataFrame to a CSV file for future use
df.to_csv("orcid_scopus_names.csv", index=False)


year = 2024   # Optional
max_results = 50  # Example: increase if you need more

#for element in df['Scopus ID']:
#    print(element,df['Name'])
    #publications = get_publications_by_author_and_year(api_key, element, year, max_results)
    #for i, (title, journal_name) in enumerate(publications, start=1):
    #    print(f"{i}. {title} - {journal_name}")

for index, row in df.iterrows():
    orcid = row.iloc[0]  
    scopusid = row.iloc[1]  
    name = row.iloc[2]  
    print(orcid,scopusid,name)
    print("-----\n")
    publications = get_publications_by_author_and_year(api_key, scopusid, year, max_results)
    #print(publications)
    for i, (title, journal_name) in enumerate(publications, start=1):
       print(f"{i}. {title} - {journal_name}")
    # Adding a small timeout to not get blocked by the API
    time.sleep(1)
    print('\n')


##for i, (title, journal_name) in enumerate(publications, start=1):
#    print(f"{i}. {title} - {journal_name}")

