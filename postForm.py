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
    size = forms("form fieldset p label").find("input").attr("name")
    topping = forms("form fieldset").eq(1).find("p label input").attr("name")
    delivery_time = forms("form p").eq(10).find("label input").attr("name")
    delivery_instruction = forms("form p").eq(11).find("label textarea").attr("name")
    payload=f"{name}=kabir&{tel}=98079&{email}=kbr2gmia.com&{size}=large&{topping}=bacon&{topping}=cheese&{topping}=onion&{topping}=mushroom&{delivery_time}=11:00&{delivery_instruction}=hello fast food"
    return payload , action 

def main():
    payload, action = next_page() 
    r = requests.post(base_url + action, data=payload)
    print(r.json())
    print(r.headers)
   




if __name__ == "__main__":
    main()
    