import time

from flask import Flask, render_template, request

app = Flask(__name__)


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

    if page_number > pages_count or page_number < 0:
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


@app.route('/add-item', methods=['POST'])
def add_item():
    data = request.get_json()
    database.save_data()


@app.route('/')
def index():
    return render_template('index.html', server_speed=0)




app.run(debug=True)
