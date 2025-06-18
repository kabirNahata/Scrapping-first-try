from pyquery import PyQuery
import requests
import json

json_source = "https://www.collegedunia.com/college/4417-shri-ram-college-of-commerce-srcc-new-delhi"

def get_pq(source):
    return PyQuery(source)

def getSource(url):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print("Couldnt get any response!")
        return None

    return response.text

def main():
    # print(json_source)
    base_source = getSource(json_source)
    # print(base_source)
    pq = get_pq(base_source)
    json_code = pq("script#__NEXT_DATA__")
    # print(json_code.text())
    output = json_code.text()
    with open("data.json", "w") as f:
        json.dump(output, f)

    



if __name__ == "__main__":
    main()