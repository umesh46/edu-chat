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

# --- Main execution block ---

if __name__ == "__main__":


  TARGET_URL = "https://www.k5learning.com/free-math-worksheets/fifth-grade-5"
  link_contains = "https://www.k5learning.com/free-math-worksheets/fifth-grade-5/"
  g_drive_link = "/content/drive/MyDrive/Jiya/DoTheMath"

  parent_f = urlparse(TARGET_URL).path.strip('/').split('/')[-1]

  all_links = fetch_and_scrape_links(TARGET_URL)
  # prompt: select links from all_links if it contains "free-math-worksheets/fifth-grade-5"

  fifth_grade_links = [link for link in all_links if link_contains in link]

  fifth_grade_links = fifth_grade_links

  if fifth_grade_links:
      print(f"\n[+] Found {len(fifth_grade_links)} unique links on the page:")
      for i, link in enumerate(fifth_grade_links, 1):
          print(f"  {i:3}. {link}")
          clink_contains =  link +"/"
          # print(clink_contains)
          child_links = fetch_and_scrape_links(link)
          child_links = [link for link in child_links if clink_contains in link]

          child_links = child_links

          for j, clink in enumerate(child_links, 1):
            print(f"---------------  {j:3}. {clink}")

            child_f = urlparse(clink).path.strip('/').split('/')[-1]

            print("folder location: ----- ",parent_f+"/"+child_f)
            save_folder = g_drive_link+"/"+parent_f+"/"+child_f

            pdf_links = get_pdf_links(clink)
            for k, pd_link in enumerate(pdf_links, 1):

              print(f"---------------****************  {k:3}. {pd_link}")
              download_pdf(pd_link,save_folder)
            

  else:
      print("\n[-] No links were found or the page could not be accessed.")

