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

            # print(f"Total {len(ads_array)} ads found.")
            return ads_array

        else:
            print("No window.initialData script found.")

    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

    return None


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
