import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_wikipedia(query):
    url = f"https://en.wikipedia.org/w/index.php?search={query}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Cherche les titres et les résumés des résultats de recherche
            titles = soup.find_all('div', class_='mw-search-result-heading')
            summaries = soup.find_all('div', class_='searchresult')

            results = pd.DataFrame({
                'Title': [title.get_text().strip() for title in titles],
                'Summary': [summary.get_text().strip() for summary in summaries]
            })

            return results
        else:
            print("Erreur de réponse HTTP :", response.status_code)
            return pd.DataFrame()
    except Exception as e:
        print("Une erreur s'est produite :", e)
        return pd.DataFrame()

# Exemple d'utilisation
query = "Python Programming"
results = scrape_wikipedia(query)
print(results.head())