import requests
import csv
from xml.etree import ElementTree as ET # or from bs4 import BeautifulSoup

def rss_to_csv(rss_url, output_filename='output.csv'):
    try:
        response = requests.get(rss_url)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

        # Parse the XML content
        root = ET.fromstring(response.content)
        # If using BeautifulSoup:
        # soup = BeautifulSoup(response.content, 'xml')
        # items = soup.find_all('item') # Or whatever the item tag is in your RSS feed

        # Define CSV headers
        fieldnames = ['title', 'link', 'description', 'pubDate', 'author']

        with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for item in root.findall('.//item'): # Adjust XPath as needed for your RSS structure
                title = item.find('title').text if item.find('title') is not None else ''
                link = item.find('link').text if item.find('link') is not None else ''
                description = item.find('description').text if item.find('description') is not None else ''
                pubDate = item.find('pubDate').text if item.find('pubDate') is not None else ''
                author = item.find('author').text if item.find('author') is not None else ''

                writer.writerow({
                    'title': title,
                    'link': link,
                    'description': description,
                    'pubDate': pubDate,
                    'author': author
                })
        print(f"Successfully converted RSS feed to {output_filename}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching RSS feed: {e}")
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    rss_feed_url = 'http://rss.cnn.com/rss/cnn_topstories.rss' # Example CNN Top Stories RSS feed
    rss_to_csv(rss_feed_url)
