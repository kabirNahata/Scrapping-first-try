from pyquery import PyQuery
import requests

base_url = "https://duckduckgo.com"

def getSource(base_url):
    response = requests.get(base_url)
    if response.status_code != 200:
        print("Couldnt get any response!")
        return None

    return response.text

def get_pq(source):
    return PyQuery(source)

def main():

    query = "bikash nahata, nepal"
    payload= "/?t=h_&q="
    print(payload)

    r = requests.get(base_url + payload + query)
    print(r.text)

if __name__ == "__main__":
    main()
 