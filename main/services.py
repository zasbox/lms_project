import os

import requests
from django.conf import settings


def make_payment(course_name, amount):
    apikey = settings.API_KEY
    main_url = settings.MAIN_URL

    headers = {'Authorization': f'Bearer {apikey}'}
    params = {'name': course_name}
    response = requests.post(f'https://api.stripe.com/v1/products', headers=headers, params=params)
    data = response.json()
    product_id = data['id']

    params = {"unit_amount": amount * 100, 'currency': 'RUB', 'product': product_id}
    response = requests.post(f'https://api.stripe.com/v1/prices', headers=headers, params=params)
    data = response.json()
    price_id = data['id']

    params = {'line_items[][price]': f'{price_id}', 'line_items[][quantity]': 1,
              'success_url': f"{main_url}/courses/payment/realized/{{CHECKOUT_SESSION_ID}}", 'mode': "payment"}
    response = requests.post(f'https://api.stripe.com/v1/checkout/sessions', headers=headers, params=params)
    data = response.json()

    return {'session': data['id'], 'url': data['url']}


def get_status_payment(session):
    apikey = settings.API_KEY
    headers = {'Authorization': f'Bearer {apikey}'}
    response = requests.get(f'https://api.stripe.com/v1/checkout/sessions/{session}', headers=headers)
    data = response.json()
    return data['payment_status']
