import json
import requests
from bs4 import BeautifulSoup
import os


def extract_data_from_dawn():
    url = "https://www.dawn.com/"
    result_data = []
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract titles and descriptions from articles
        articles = soup.find_all('article', class_='story')
        for article in articles:
            title_element = article.find('h2', class_='story__title')
            title_link = title_element.find('a') if title_element else None
            title = title_link.text.strip() if title_link else "No title available"
            
            description_element = article.find('div', class_='story__excerpt')
            description = description_element.text.strip() if description_element else "No description available"
            link = title_link['href'] if title_link else "No link available"
            
            result_data.append({'title': title, 'link': link, 'description': description})
        
        return result_data
    except requests.RequestException as e:
        print(f"An error occurred while fetching data from {url}: {e}")
        return []


def extract_data_from_bbc():
    url = "https://www.bbc.com/"
    result_data = []
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract headlines and descriptions
        cards = soup.find_all('a', {'data-testid': 'internal-link'})
        for card in cards:
            headline = card.find('h2', {'data-testid': 'card-headline'})
            if headline:
                title = headline.text.strip()
                link = f"https://www.bbc.com{card['href']}" if card.has_attr('href') else "No link available"
                description = card.find('p', {'data-testid': 'card-description'})
                desc_text = description.text.strip() if description else "No description available"
                
                result_data.append({'title': title, 'link': link, 'description': desc_text})
        
        return result_data
    except requests.RequestException as e:
        print(f"An error occurred while fetching data from {url}: {e}")
        return []


def main():
    print("Current Working Directory:", os.getcwd())
    # Extract data from BBC and Dawn
    bbc_data = extract_data_from_bbc()
    dawn_data = extract_data_from_dawn()

    # Combine all data into one list
    all_data = bbc_data + dawn_data

    # # Write data to JSON file
    with open('.\\data\\extracted_data.json', 'w', encoding='utf-8') as file:
        json.dump(all_data, file, ensure_ascii=False, indent=4)

    print("Data has been written to 'extracted_data.json'")


main()
