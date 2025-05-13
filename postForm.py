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
    pizza_size_small = forms("form fieldset p label").find("input").attr("value")
    pizza_size_medium = forms("form fieldset p").eq(1).find("label input").attr("value")
    pizza_size_large = forms("form fieldset p").eq(2).find("label input").attr("value")
    pizza_topping_bacon = forms("form fieldset").eq(1).find("p label input").attr("value")
    pizza_topping_cheese = forms("form fieldset").eq(1).find("p").eq(1).find("label input").attr("value")
    pizza_topping_onion = forms("form fieldset").eq(1).find("p").eq(2).find("label input").attr("value")
    pizza_topping_mushroom = forms("form fieldset").eq(1).find("p").eq(3).find("label input").attr("value")
    # delivery_time = forms("form p").eq(3).find("label input").attr("name")
    # delivery_instruction = forms("form p").eq(4).find("label input").attr("name")
    # submit = forms("forms p").eq(5).find("button").text()


    return action, name, tel, email, pizza_size_small, pizza_size_medium, pizza_size_large , pizza_topping_bacon, pizza_topping_cheese,pizza_topping_onion, pizza_topping_mushroom #, delivery_time, delivery_instruction, submit


# def filling_page():
#     cust_name = pq()
#     return cust_name

def main():
    action, name, tel, email, pizza_size_small, pizza_size_medium, pizza_size_large , pizza_topping_bacon, pizza_topping_cheese,pizza_topping_onion , pizza_topping_mushroom  = next_page() #, delivery_time, delivery_instruction, submit
    print(action)
    print(name)
    print(tel)
    print(email)
    print(pizza_size_small)
    print(pizza_size_medium)
    print(pizza_size_large)
    print(pizza_topping_bacon)
    print(pizza_topping_cheese)
    print(pizza_topping_onion)
    print(pizza_topping_mushroom)   
    # print(delivery_time)
    # print(delivery_instruction)
    # print(submit)
if __name__ == "__main__":
    main()
    