from pyquery import PyQuery as pq
import requests
import json

json_source = "https://collegedunia.com/college/4417-shri-ram-college-of-commerce-srcc-new-delhi"

def get_pq(html):
    return pq(html)

def getSource(url):
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Couldn't get any response!")
        return None

    return response.text

if __name__ == "__main__":
    base_source = getSource(json_source)

    if base_source:
        doc = get_pq(base_source)
        json_script = doc('script#__NEXT_DATA__').text()

        try:
            data = json.loads(json_script)
            print(json.dumps(data, indent=2))  # pretty-print JSON
        except json.JSONDecodeError:
            print("Couldn't parse JSON from the script tag.")
