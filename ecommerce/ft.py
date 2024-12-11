from flask import jsonify
import requests

latest_usd_exchange_rate = 1.0

def ft_seek_product(product_id):
    try:
        # Request para Store, via get
        response = requests.get('http://store:5001/product', params={'product': product_id})

        #Verificação se o produto foi encontrado
        if response.status_code == 200: #OK
            return response.json()
        else:
            return None
    except requests.exceptions.RequestException:
        pass
    
def ft_get_exchange():
    global latest_usd_exchange_rate
    # tentando em exchange1
    try:
        response = requests.get('http://exchange1:5011/exchange')
        if response.status_code == 200:
            data = response.json()
            latest_usd_exchange_rate = data['exchange_rate']
            return latest_usd_exchange_rate
        # implementar um catch para tratar a exceção (log)
    except requests.exceptions.RequestException:
        pass

    # se exchange1 falhar, o exchange2 será solicitado
    try:
        response = requests.get('http://exchange2:5012/exchange')
        if response.status_code == 200:
            data = response.json()
            latest_usd_exchange_rate = data['exchange_rate']
            return latest_usd_exchange_rate
        # implementar um catch para tratar a exceção (log)
    except requests.exceptions.RequestException:
        pass

    #Se ambos falharem, será enviado o ultimo valor salvo
    return latest_usd_exchange_rate

def ft_make_purchase(product_id):
    try:
        response = requests.post('http://store:5001/sell', json={'product': product_id})

        if response.status_code == 200:
            return response.json()['transaction_id']
        else: 
            return None
    except requests.exceptions.RequestException:
        pass
   
    
def ft_send_bonus(user_id, bonus):
    try:
        response = requests.post('http://fidelity:5003/bonus', json={"user": user_id, "bonus":bonus})
        if response.status_code == 200:
            return response.json()['bonus']
        else: 
            return None
    except requests.exceptions.RequestException:
        pass
    