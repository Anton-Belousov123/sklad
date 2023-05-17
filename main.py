import random
import time

from flask import Flask, render_template, request, send_file

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
    if page_number == 0:
        return render_template('404.html', server_speed=0)
    time_start = time.time()
    items = db.get_items((page_number - 1) * 25)
    data = []
    print(len(items))
    for i in items:
        data.append({
        'name': i[1],
        'price': 500,
        'count': 1,
        'real_count': 6,
        'is_active': random.randint(0, 1),
        'questions': random.randint(0, 1),
        'links': ['ozon', 'yandex']
    })
    items_max = int(db.get_count('Suggested'))
    pages_count = items_max // 25
    if items_max % 25 != 0:
        pages_count += 1

    items_current = page_number * 25
    if items_current > items_max:
        items_current = items_max
    print(f"{pages_count=}")
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
    return render_template('graphic.html', data=data, server_speed=server_speed_answer, labels=labels)

@app.route('/strategies')
def strategies():
    return render_template('strategies/strategies.html')


@app.route('/sources')
def sources():
    return render_template('sources/sources.html')


@app.route('/adding/stats')
def addingstats():
    elements = db.get_suggestion_stats()
    print(elements)
    data = [
        {'label': 'Line 1', 'data': [10, 20, 30, 40, 50]},
        {'label': 'Line 2', 'data': [5, 15, 25, 35, 45]},
        {'label': 'Line 3', 'data': [20, 10, 30, 50, 40]}
    ]
    labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
    legends = ['Legend 1', 'Legend 2', 'Legend 3']
    return render_template('adding/stats.html', today=[], data=data, legends=legends, labels=labels, title='Ежедневная статистика добавлений')


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


@app.route('/nakleiki-download', methods=["POST"])
def nakleiki_download_post():
    from nakleiki import main as nk
    nk.prepare_document()
    return send_file('cache/result.pdf', as_attachment=True)

@app.route('/nakleiki', methods=['POST'])
def nakleiki_post():
    v, id = request.json['value'], request.json['id']
    db.update_nakleiki(id, v)
    return 'ok'


@app.route('/nakleiki', methods=["GET"])
def nakleiki():
    print(request.args)
    try:
        page_number = int(request.args.get('page', default=1))
    except:
        return render_template('404.html', server_speed=0)
    if page_number == 0:
        return render_template('404.html', server_speed=0)
    time_start = time.time()
    items = db.get_nakleiki((page_number - 1) * 25)
    data = []
    print(len(items))
    for i in items:
        data.append({
            'number': i[0],
            'photo': i[1],
            'name': i[2],
            'pack_type': i[3]
        })
    items_max = int(db.get_count_nakleiki())
    pages_count = items_max // 25
    if items_max % 25 != 0:
        pages_count += 1

    items_current = page_number * 25
    if items_current > items_max:
        items_current = items_max
    print(f"{pages_count=}")
    if page_number > pages_count or page_number <= 0:
        return render_template('404.html', server_speed=0)

    server_speed_answer = round(time.time() - time_start, 2)
    return render_template('nakleiki.html', server_speed=server_speed_answer, data=data, page_number=page_number,
                           items_max=items_max, pages_count=pages_count, items_current=items_current)


@app.route('/')
def index():
    created_count = db.get_count('Created')
    source_parsed_count = db.get_count('Source parsed')
    target_parsed_count = db.get_count('Target parsed')
    suggested_count = db.get_count('Suggested')
    target_error = db.get_count('Suggested')
    source_error = db.get_count('Suggested')
    return render_template('index.html', created_count=created_count, source_parsed_count=source_parsed_count, target_parsed_count=target_parsed_count, suggested_count=suggested_count,
                           target_error=target_error, source_error=source_error)


app.run(debug=True, host='0.0.0.0', port=8080)
