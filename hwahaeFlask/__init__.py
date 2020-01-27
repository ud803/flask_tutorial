from flask import Flask, g, request, Response, make_response, jsonify
import sqlite3

app = Flask(__name__)
app.debug = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
    
@app.route('/products', methods=['GET'])
def products():
    query_parameters = request.args
    
    skin_type = query_parameters.get('skin_type')
    category = query_parameters.get('category')
    page = query_parameters.get('page')
    exclude_ingredient = query_parameters.get('exclude_ingredient')
    include_ingredient = query_parameters.get('include_ingredient')
    
    query = "SELECT id, imageId, name, price, ingredients, monthlySales FROM item WHERE "
    to_filter = []
    
    #category
    if category:
        query += "category=? AND"
        to_filter.append(category)
    
    #include_ingredient
    if include_ingredient:
        for ingredient in include_ingredient.split(','):
            query += "ingredients LIKE ? AND"
            to_filter.append(ingredient)
    
    #exclude_ingredient
    if exclude_ingredient:
        for ingredient in exclude_ingredient.split(','):
            query += "ingredients NOT LIKE ? AND"
            to_filter.append(ingredient)
    
    query = query[:-4] + ';'

    conn = sqlite3.connect('hwahaeFlask/static/data/hwahae.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    for result in results:
        query = "SELECT * FROM ingredient WHERE"
        to_filter = []

        for ingredient in result['ingredients'].split(','):
            query += " name LIKE ? OR"
            to_filter.append(ingredient)
        query = query[:-3] + ';'
        ing = cur.execute(query, to_filter).fetchall()

        score = 0
        for _ in ing:
            if(_[skin_type] == "O"):
                score += 1
            elif(_[skin_type] == "X"):
                score -= 1
            else:
                continue
        result['score'] = score
        
    results = sorted(results, key= lambda x: x['score'], reverse = True)

    #page
    if page:
        results = results[(int(page)-1)*50:int(page)*50]
    
    return jsonify(results)
    

@app.route('/product/<pid>', methods=['GET'])
def product(pid):  
    final_results = [] 
    skin_type = request.args.get('skin_type')

    query = "SELECT * FROM item WHERE id = ?"

    conn = sqlite3.connect('hwahaeFlask/static/data/hwahae.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    target = cur.execute(query, [pid]).fetchall()[0]
    final_results.append(target)

    query = "SELECT id, imageId, category, ingredients, name, price FROM item WHERE category = ?"
    results = cur.execute(query, [target["category"]]).fetchall()

    for result in results:
        query = "SELECT * FROM ingredient WHERE"
        to_filter = []

        for ingredient in result['ingredients'].split(','):
            query += " name LIKE ? OR"
            to_filter.append(ingredient)
        query = query[:-3] + ';'
        ing = cur.execute(query, to_filter).fetchall()

        score = 0
        for _ in ing:
            if(_[skin_type] == "O"):
                score += 1
            elif(_[skin_type] == "X"):
                score -= 1
            else:
                continue
        result['score'] = score
        
    results = sorted(results, key= lambda x: x['score'], reverse = True)
    
    for result in results[:3]:
        result = {k:v for k, v in result.items() if k in ['id', 'imageId', 'name', 'price']}
        print(result)
        final_results.append(result)
        
    return jsonify(final_results)