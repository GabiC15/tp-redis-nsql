from flask import Flask, jsonify, request, render_template
from redis import Redis
from datetime import datetime
import json

### Que guarda cada registro?
# episode_*: lista de personajes de un episodio
# state_*: estado de un episodio (disponible, reservado, alquilado)
# title_*: titulo de un episodio
# price_*: precio de un episodio

app = Flask(__name__, template_folder='')

def connect_db():
    conexion = Redis(host='db-redis', port=6379, decode_responses=True, )
    if(conexion.ping()):
        print("conectado a redis")
    else:
        print("error de conexion con redis")

    return conexion

def init_db():
    con = connect_db()
    if con.get('init'):
        return
    f = open('chapters.json')
    chapters = json.load(f)
    for i in range(len(chapters)):
        chapter = chapters[i]
        con.set(f'title_{chapter['key']}', chapter['title'])
        con.set(f'price_{chapter['key']}', chapter['price'])
        for chr in chapter['characters']:
            con.lpush(f'episode_{chapter['key']}', chr)
    con.set('init', 1)

def get_list(db, nombre_lista):
    lista = db.lrange(nombre_lista, 0, -1)
    return lista

@app.route('/', methods=['GET'])
def index():
    """Retorna la pagina index."""
    return render_template('home.html')

###############  PARTE 2 ###############
@app.route('/load_character', methods=['GET'])
def load_character():
    if(request.method == 'GET'):
        con = connect_db()
        episode = request.args.get("episode")
        character_name = request.args.get("name")
        con.lpush(f'episode_{episode}', character_name)

    return "OK"

@app.route('/remove_character', methods=['GET'])
def remove_character():
    if(request.method == 'GET'):
        con = connect_db()
        episode = request.args.get("episode")
        character_name = request.args.get("name")
        con.lrem(f'episode_{episode}', 0, character_name)

    return "OK"

@app.route('/list_charapters_episode', methods=['GET'])
def lista_characters_by_episode():
    lista = None
    if(request.method == 'GET'):
        con = connect_db()
        episode = request.args.get("episode")
        lista = get_list(con, f'episode_{episode}')
    return jsonify(lista)

@app.route('/list_episodes', methods=['GET'])
def lista_episodes():
    json = {}
    if(request.method == 'GET'):
        con = connect_db()
        keys = list(map(lambda k: k.split("_")[-1], con.keys('episode_*')))
        state_keys = [f'state_{k}' for k in keys]
        price_keys = [f'price_{k}' for k in keys]
        titles_keys = [f'title_{k}' for k in keys]
        episodes = con.mget(state_keys)
        titles = con.mget(titles_keys)
        prices = con.mget(price_keys)
        for key in range(len(state_keys)):
            state = episodes[key] if episodes[key] else 'available'
            details = {'state': state, 'title': titles[key], 'price': prices[key]}
            json[keys[key]] = details
    return jsonify(json)

###############  PARTE 3 ###############
@app.route('/rent_episode', methods=['GET'])
def rent_episode():
    if(request.method == 'GET'):
        con = connect_db()
        episode = request.args.get("episode")
        con.set(f'state_{episode}', "reserved", ex=240)
    return "OK"

@app.route('/confirm_pay', methods=['GET'])
def confirm_pay():
    if(request.method == 'GET'):
        con = connect_db()
        episode = request.args.get("episode")
        passedPrice = request.args.get("price")
        state = con.get(f'state_{episode}')
        price = con.get(f'price_{episode}')

        if price != passedPrice:
            return 'ERROR: El monto que ingresó no corresponde con el precio del capitulo', 400
        if state == 'available':
            return 'ERROR: El episodio debe estar previamente reservado', 400
        elif state == 'rented':
            return 'ERROR: El episodio ya está alquilado', 400
        
        con.set(f'state_{episode}', "rented", ex=86400)
        con.set(f'pay_{episode}_{datetime.now()}', passedPrice)
    return "OK"



if __name__ == '__main__':
    init_db()
    
    app.run(host='web-api-flask', port='5000', debug=True)

