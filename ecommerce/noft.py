import requests

def noft_seek_product(product_id):
    # Request para Store, via get
    response = requests.get('http://store:5001/product', params={'product': product_id})
    return response.json()

def noft_get_exchange():
    response = requests.get('http://exchange1:5011/exchange') # colocar num try-catch
    data = response.json()
    return data['exchange_rate']

def noft_make_purchase(product_id):
    response = requests.post('http://store:5001/sell', json={'product': product_id})
    return response.json()['transaction_id']
    
def noft_send_bonus(user_id, bonus):
    response = requests.post('http://fidelity:5003/bonus', json={"user": user_id, "bonus":bonus})
    return response.json()['bonus']