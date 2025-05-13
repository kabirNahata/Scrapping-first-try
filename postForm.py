from pyquery import PyQuery
import requests

base_url = "https://httpbin.org"

def getSource(base_url):
    response = requests.get(base_url)
    if response.status_code != 200:
        print("Couldnt get any response!")
        return None

    return response.text

def get_pq(source):
    return PyQuery(source)

def enter_page():
    url_page = get_pq(getSource(base_url)) 
    url = url_page('div.swagger-ui li a').attr('href')
    return url

def next_page():
    form_page = base_url + enter_page()
    forms = get_pq(getSource(form_page))
    action = forms.find("form").attr('action')
    name = forms.find("form p:first input").attr('name')
    tel = forms("form p").eq(1).find("input").attr("name")
    email = forms("form p").eq(2).find("input").attr("name")
    


    return action, name, tel, email

# def filling_page():
#     cust_name = pq()
#     return cust_name

def main():
    action , name , tel , email = next_page()
    print(action)
    print(name)
    print(tel)
    print(email)



if __name__ == "__main__":
    main()
    