import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys
from urllib.parse import urlparse

# --- Configuration ---
# The URL of the page you want to scrape
TARGET_URL = "https://www.k5learning.com/free-math-worksheets/fifth-grade-5"
# ---------------------

def fetch_and_scrape_links(url):
    """
    Fetches the content of a URL and scrapes it for all unique hyperlinks.

    Args:
        url (str): The URL of the webpage to scrape.

    Returns:
        list: A sorted list of unique, absolute URLs found on the page.
    """
    print(f"[*] Fetching links from: {url}")
    
    # Use a set to automatically handle duplicate links
    unique_links = set()

    try:
        # Use a session object for better performance and to set headers
        session = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = session.get(url, headers=headers, timeout=15)
        
        # This will raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print(f"[!!!] FAILED to retrieve the webpage. Error: {e}", file=sys.stderr)
        return []

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all anchor tags <a> that have an 'href' attribute
    for a_tag in soup.find_all('a', href=True):
        link = a_tag['href']
        
        # Ignore empty or javascript links
        if not link or link.startswith('#') or link.startswith('javascript:'):
            continue
            
        # Convert relative URLs (like '/about-us') to absolute URLs
        absolute_link = urljoin(url, link)
        unique_links.add(absolute_link)

    # Return a sorted list for consistent output
    return sorted(list(unique_links))


def get_pdf_links(url):
    """
    Fetches a URL and scrapes it for all unique links pointing to PDF files.
    """
    print(f"[*] Scanning {url} for PDF links...")
    pdf_links = set() # Use a set to avoid duplicates

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Check for errors like 404

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all link <a> tags with an 'href' attribute
        for a_tag in soup.find_all('a', href=True):
            link = a_tag['href']
            
            # Check if the link is for a PDF
            if link.lower().endswith('.pdf'):
                # Convert relative links (like "/docs/file.pdf") to absolute links
                full_link = urljoin(url, link)
                pdf_links.add(full_link)

    except requests.exceptions.RequestException as e:
        print(f"[!] Error fetching the URL: {e}")
        return []

    return sorted(list(pdf_links)) # Return a sorted list

def download_pdf(pdf_url, output_folder="downloaded_pdfs"):
    """
    Downloads a PDF file from a given URL.
    """
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get the filename from the URL
    filename = os.path.join(output_folder, os.path.basename(pdf_url))

    print(f"[*] Downloading {pdf_url} to {filename}...")

    try:
        response = requests.get(pdf_url, stream=True, timeout=20)
        response.raise_for_status() # Check for errors

        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"[+] Downloaded successfully: {filename}")

    except requests.exceptions.RequestException as e:
        print(f"[!] Error downloading {pdf_url}: {e}")
    except IOError as e:
        print(f"[!] Error saving file {filename}: {e}")