import requests
from bs4 import BeautifulSoup
import json
import time


def valid_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return True
    except:
        return False

url = input("Enter the URL: ")

while not valid_url(url):
    print("Invalid URL. Please enter a valid URL.")
    url = input("Enter the URL: ")

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")


print("What would you like to extract?")
print("1. Links")
print("2. Whole HTML")
print("3. Text content")
print("4. Metadata")
print("5. Social media data")
choices = input("Enter your choices (comma-separated, e.g. '1,2,3'): ").split(",")

#links
filter_links = False
if "1" in choices:
    filter_links_input = input("Do you want to filter out links that don't start with http? (y/n) ")
    if filter_links_input.lower() == "y":
        filter_links = True

    if "1" in choices:
        links = [link.get("href") for link in soup.find_all("a")]

        if filter_links:
            links = [link for link in links if link and link.startswith("http")]
        
        with open("links.txt", "w") as file:
            for link in links:
                if link:
                    file.write(link + "\n")
        print("Links extracted and saved to links.txt")

#html
if "2" in choices:
    html = response.content
    with open("html.html", "wb") as file:
        file.write(html)
    print("Whole HTML extracted and saved to html.html")

#text
if "3" in choices:
    text = soup.get_text()
    with open("text.txt", "w", encoding="utf-8") as file:
        file.write(text)
    print("Text content extracted and saved to text.txt")

#metadata
if "4" in choices:
    metadata = {}
    for meta in soup.find_all("meta"):
        if meta.get("name"):
            metadata[meta.get("name")] = meta.get("content")
    with open("metadata.json", "w") as file:
        json.dump(metadata, file, indent=4)
    print("Metadata extracted and saved to metadata.json")

#social media
if "5" in choices:

    social_data = {}

    fb_likes_elem = soup.select_one('div[id^="fb"] span')
    if fb_likes_elem:
        fb_likes = fb_likes_elem.get_text()
        social_data['facebook_likes'] = fb_likes
    
    fb_shares_elem = soup.select_one('a[href^="https://www.facebook.com/sharer.php"] span')
    if fb_shares_elem:
        fb_shares = fb_shares_elem.get_text()
        social_data['facebook_shares'] = fb_shares

    twt_tweets_elem = soup.select_one('a[href^="https://twitter.com/share"] span')
    if twt_tweets_elem:
        twt_tweets = twt_tweets_elem.get_text()
        social_data['twitter_tweets'] = twt_tweets

    twt_likes_elem = soup.select_one('a[href^="https://twitter.com/intent/like"] span')
    if twt_likes_elem:
        twt_likes = twt_likes_elem.get_text()
        social_data['twitter_likes'] = twt_likes

    with open("social_media_data.json", "w") as file:
        json.dump(social_data, file, indent=4)
    print("Social media data extracted and saved to social_media_data.json")
time.sleep(10)
if not any(c in choices for c in ["1", "2", "3", "4", "5"]):
    print("Invalid choice. Please enter a comma-separated list of numbers between 1 and 5.")
