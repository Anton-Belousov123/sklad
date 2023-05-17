import json

import requests

from nakleiki import db_methods

headers = {
    'Client-Id': '667260',
    'Api-Key': '3e8b0e18-c341-4d6e-8706-d479388e666e'
}


def get_codes():
    url = 'https://api-seller.ozon.ru/v3/posting/fbs/unfulfilled/list'
    data = {
        "dir": "ASC",
        "filter": {
            "status": "awaiting_deliver",
            "cutoff_from": "2021-08-24T14:15:22Z",
            "cutoff_to": "2100-08-31T14:15:22Z"
        },
        "limit": 1000,
        "offset": 0,
        "with": {
            "analytics_data": True,
            "barcodes": True,
            "financial_data": True,
            "translit": True
        }
    }
    r = requests.post(url, headers=headers, data=json.dumps(data))
    return r.json()


def get_image(offer_id):
    url = 'https://api-seller.ozon.ru/v2/product/info'
    data = {
        "offer_id": offer_id,
        "product_id": 0,
        "sku": 0
    }
    resp = requests.post(url, data=json.dumps(data), headers=headers).json()
    import qrcode
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    link = f"https://ozon.ru/context/detail/id/{resp['result']['id']}"
    qr.add_data(link)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")
    qr_image.save("cache/qrcode.png")
    from PIL import Image
    image = Image.open('cache/qrcode.png')
    flipped_image = image.rotate(180)
    flipped_image.save('cache/qrcode.png')
    return resp['result']['primary_image']


def get_pdf(codes, index):
    url = 'https://api-seller.ozon.ru/v2/posting/fbs/package-label'
    data = {
        'posting_number': codes
    }
    resp = requests.post(url, data=json.dumps(data), headers=headers)
    with open(f'cache/{index}.pdf', 'wb') as f:
        f.write(resp.content)
    f.close()


def get_items_list(last_id=None, arr=[]):
    url = 'https://api-seller.ozon.ru/v2/product/list'
    data = {
        'limit': 1000
    }
    if last_id:
        data['last_id'] = last_id
    resp = requests.post(url, data=json.dumps(data), headers=headers).json()['result']
    for item in resp['items']:
        if item['product_id'] in arr:
            return arr
        arr.append(item['product_id'])
    return get_items_list(resp['last_id'], arr)


def get_item_info(product_id):
    url = 'https://api-seller.ozon.ru/v2/product/info'
    data = {
        "offer_id": "",
        "product_id": product_id,
        "sku": 0
    }
    resp = requests.post(url, data=json.dumps(data), headers=headers).json()['result']
    image = resp['primary_image']
    name = resp['name']
    db_methods.insert_item(product_id, name, image)

