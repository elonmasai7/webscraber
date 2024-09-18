import os
import sqlite3

try:
    import requests
except ImportError:
    print("Requests is not installed. Please install it using 'pip install requests'")
    exit(1)

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("BeautifulSoup is not installed. Please install it using 'pip install beautifulsoup4'")
    exit(1)

try:
    import pandas as pd
except ImportError:
    print("Pandas is not installed. Please install it using 'pip install pandas'")
    exit(1)

def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.title.string, response.cookies

def get_firefox_history(profile_path):
    history_path = os.path.join(profile_path, 'places.sqlite')
    con = sqlite3.connect(history_path)
    cursor = con.cursor()
    cursor.execute("""
        SELECT url, title, visit_count, last_visit_date
        FROM moz_places
    """)
    results = cursor.fetchall()
    con.close()
    return pd.DataFrame(results, columns=['url', 'title', 'visit_count', 'last_visit_date'])

def get_firefox_cookies(profile_path):
    cookies_path = os.path.join(profile_path, 'cookies.sqlite')
    con = sqlite3.connect(cookies_path)
    cursor = con.cursor()
    cursor.execute("""
        SELECT host, name, value, creationTime, lastAccessed, expiry
        FROM moz_cookies
    """)
    results = cursor.fetchall()
    con.close()
    return pd.DataFrame(results, columns=['host', 'name', 'value', 'creationTime', 'lastAccessed', 'expiry'])

def find_firefox_profile():
    # Assuming a default profile path for Linux
    profile_base_path = os.path.expanduser('~/.mozilla/firefox/')
    profiles = os.listdir(profile_base_path)
    # Assuming the first profile is the one we want, adjust if necessary
    profile_path = os.path.join(profile_base_path, profiles[0])
    return profile_path

# Example usage
if __name__ == "__main__":
    # Scrape website
    url = 'https://www.example.com'
    title, cookies = scrape_website(url)
    print(f"Title: {title}")
    print(f"Cookies: {cookies}")

    # Get Firefox profile path
    firefox_profile_path = find_firefox_profile()

    # Get browser history
    history_df = get_firefox_history(firefox_profile_path)
    print("Browser History:")
    print(history_df.head())

    # Get browser cookies
    cookies_df = get_firefox_cookies(firefox_profile_path)
    print("Browser Cookies:")
    print(cookies_df.head())
