import time

from flask import Flask, render_template, request

from database import database

app = Flask(__name__)
db = database.Database()

@app.route('/storage')
def storage():
    print(request.args)
    try:
        page_number = int(request.args.get('page', default=1))
    except:
        return render_template('404.html', server_speed=0)
    time_start = time.time()
    data = [{
        'name': 'Это тестовое название',
        'price': 500,
        'count': 1,
        'real_count': 6,
        'is_active': True,
        'questions': False,
        'links': ['ozon', 'yandex']
    }]
    items_max = len(data)
    pages_count = items_max // 25
    if items_max % 25 != 0:
        pages_count += 1

    items_current = page_number * 25
    if items_current > items_max:
        items_current = items_max

    if page_number > pages_count or page_number <= 0:
        return render_template('404.html', server_speed=0)

    server_speed_answer = round(time.time() - time_start, 2)
    return render_template('storage.html', server_speed=server_speed_answer, data=data, page_number=page_number,
                           items_max=items_max, pages_count=pages_count, items_current=items_current)


@app.route('/search-stats')
def search_stats():
    start_time = time.time()
    print(request.args)
    labels = ['January', 'February', 'March', 'April', 'May', 'June']
    data = [0, 10, 15, 8, 22, 18, 25]
    server_speed_answer = round(time.time() - start_time, 2)
    return render_template('item-stats.html', data=data, server_speed=server_speed_answer, labels=labels)

@app.route('/strategies')
def strategies():
    return render_template('strategies/strategies.html')


@app.route('/sources')
def sources():
    return render_template('sources/sources.html')


@app.route('/shops', methods=["GET", "POST"])
def shops():
    print(request.method, request.form)
    if request.method == 'POST':
        form_data = request.form.to_dict()
        shop_name = form_data['shop_name']
        client_id = form_data['client-id']
        api_key = form_data['api-key']
        # db.add_shop()
    shops = ''
    return render_template('shops/shops.html', shops=shops)


@app.route('/add-item', methods=['POST'])
def add_item():
    data = request.get_json()


@app.route('/')
def index():
    created_count = db.get_count('Created')
    source_parsed_count = db.get_count('Source parsed')
    target_parsed_count = db.get_count('Target parsed')
    suggested_count = db.get_count('Suggested')
    return render_template('index.html', created_count=created_count, source_parsed_count=source_parsed_count, target_parsed_count=target_parsed_count, suggested_count=suggested_count)


app.run(debug=True, port=8080)
