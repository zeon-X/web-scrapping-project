from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)


# ...

def scrape_bikroy(query):
    base_url = f"https://bikroy.com/en/ads?query={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Send an HTTP GET request to the URL
    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the script containing window.initialData
        script_tag = soup.find(
            "script", text=lambda x: "window.initialData" in str(x))

        if script_tag:
            # Extract the JSON data from the script
            json_data = json.loads(
                script_tag.string.split("window.initialData = ")[1])

            # Access the 'ads' array
            ads_array = json_data['serp']['ads']['data']['ads']

            # You can now work with the 'ads_array' as needed
            for idx, ad in enumerate(ads_array, start=1):
                print(f"Ad {idx}:")
                print(f"Title: {ad['title']}")
                print(f"Location: {ad['location']}")
                print(f"Price: {ad['price']}")
                print(f"Link: https://bikroy.com/en/ad/{ad['slug']}")
                print("\n")

            print(f"Total {len(ads_array)} ads found.")

        else:
            print("No window.initialData script found.")

    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

    return None

# ...


# def scrape_bikroy(query):
#     base_url = f"https://bikroy.com/en/ads?query={query}"
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
#     }

#     response = requests.get(base_url, headers=headers)

#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')
#         product_containers = soup.find_all(
#             "a", class_="card-link--3ssYv gtm-ad-item")

#         scraped_data = []

#         for product in product_containers:
#             # Use try-except to handle cases where elements are not found
#             try:
#                 product_title = product.find(
#                     "h2", class_="heading--2eONR title--3yncE").text.strip()
#                 product_location = product.find(
#                     "div", class_="description--2-ez3").text.strip()
#                 product_price = product.find(
#                     "div", class_="price--3SnqI").text.strip()
#                 product_link = "https://bikroy.com" + product.get("href")
#                 updated_time = product.find(
#                     "div", class_="updated-time--1DbCk").text.strip()

#                 product_info = {
#                     "title": product_title,
#                     "location": product_location,
#                     "price": product_price,
#                     "link": product_link,
#                     "updated_time": updated_time,
#                 }

#                 scraped_data.append(product_info)
#             except AttributeError:
#                 # Handle cases where an element is not found
#                 continue

#         return scraped_data
#     else:
#         return None


# def scrape_bikroy(query):
#     base_url = f"https://bikroy.com/en/ads?query={query}"
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
#     }

#     # Send an HTTP GET request to the URL
#     response = requests.get(base_url, headers=headers)

#     if response.status_code == 200:
#         # Print the HTML content to the console
#         print(response.text)
#     else:
#         print(f"Failed to retrieve data. Status code: {response.status_code}")

#     return None


# def scrape_bikroy(query):
#     base_url = f"https://bikroy.com/en/ads?query={query}"
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
#     }

#     # Send an HTTP GET request to the URL
#     response = requests.get(base_url, headers=headers)

#     if response.status_code == 200:
#         # Save the HTML content to an HTML file
#         with open('bikroy.html', 'w', encoding='utf-8') as file:
#             file.write(response.text)
#         print("HTML content saved to bikroy.html")
#     else:
#         print(f"Failed to retrieve data. Status code: {response.status_code}")

#     return None


@app.route('/')
def index():
    return render_template('index.html', results=None)


@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    results = scrape_bikroy(query)
    return render_template('index.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)
