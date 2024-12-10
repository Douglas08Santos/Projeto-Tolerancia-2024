import requests

latest_usd_exchange_rate = 1.0

def ft_seek_product(product_id):
    # Request para Store, via get
    response = requests.get('http://store:5001/product', params={'product': product_id})

    #Verificação se o produto foi encontrado
    if response.status_code == 200: #OK
        return response.json()
    else:
        return None
    
def ft_get_exchange():
    try:
        response = requests.get('http://exchange:5002/exchange') # colocar num try-catch

        if response.status_code == 200:
            data = response.json()
            latest_usd_exchange_rate = data['exchange_rate']
            return latest_usd_exchange_rate
        else:
            return latest_usd_exchange_rate
        # implementar um catch para tratar a exceção (log)
    finally:
            return latest_usd_exchange_rate

def ft_make_purchase(product_id):
    response = requests.post('http://store:5001/sell', json={'product': product_id})

    if response.status_code == 200:
        return response.json()['transaction_id']
    else: 
        return None
    
def ft_send_bonus(user_id, bonus):
    response = requests.post('http://fidelity:5003/bonus', json={"user": user_id, "bonus":bonus})
    if response.status_code == 200:
        return response.json()['bonus']
    else: 
        return None