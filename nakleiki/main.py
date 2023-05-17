from database import database
from nakleiki import ozon_methods
from nakleiki import service_methods

def prepare_document():
    service_methods.clear_cache()
    codes = ozon_methods.get_codes()
    divided_codes = []
    for index, code in enumerate(codes['result']['postings']):
        if index % 20 == 0:
            divided_codes.append([])
        divided_codes[-1].append(code['posting_number'])

    for index, code in enumerate(divided_codes):
        ozon_methods.get_pdf(code, index)
    service_methods.concatenate_documents()

    for index, code in enumerate(codes['result']['postings']):
        offer_id = code['products'][0]['offer_id']
        count = code['products'][0]['quantity']
        image = ozon_methods.get_image(offer_id)
        service_methods.download_image(image)
        service_methods.create_image(f"Количество: {count}", f"Упаковка: {database.get_pack_type_by_article(offer_id)}")  # TODO: DO IN FUTURE
        service_methods.update_pdf(index)
