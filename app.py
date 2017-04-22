from flask import Flask, send_from_directory, jsonify, abort, make_response, url_for
import requests, os, json

app = Flask(__name__)

pokemonData = None

# Open pokemon database file.
with open('database/pokemon.json', 'r', encoding='utf8') as file:
    pokemonData = json.load(file)
    file.close()

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/error')
def error():
    return app.send_static_file('error.html')

# Handle 404 as json or else Flash will use html as default.
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

# Spreadsheet file
@app.route('/spreadsheet')
def spreadSheet():
    return app.send_static_file('spreadsheet.html')

@app.route('/spreadsheet/<string:key>/<string:sheet>/<int:row>', methods=['GET'])
def generateJsonClipboard(key,sheet,row):
    website = "https://script.google.com/macros/s/AKfycbxOLElujQcy1-ZUer1KgEvK16gkTLUqYftApjNCM_IRTL3HSuDk/exec?id=" + key + "&sheet=" + sheet
    r = requests.get(website)

    errorPage = app.send_static_file('error.html')

    try:
        jsonResult = r.json()[sheet][row - 1]
    except Exception:
        return errorPage

    # information
    nickname = jsonResult['Name']
    species = jsonResult['Species']
    gender = jsonResult['Gender']
    item = jsonResult['Item']
    nature = jsonResult['Nature']
    shiny = jsonResult['Shiny']

    # check gender
    if("f" in gender.lower()):
        gender = "f"
    elif("m" in gender.lower()):
        gender = "m"
    else:
        abort(404)

    # check shiny
    if ("y" in shiny.lower()):
        shiny = "Yes"
    elif("n" in shiny.lower()):
        shiny = "No"
    else:
        abort(404)

    # Moves
    move1 = str(jsonResult['Move_1'])
    move2 = str(jsonResult['Move_2'])
    move3 = str(jsonResult['Move_3'])
    move4 = str(jsonResult['Move_4'])

    # IV
    iv_hp = jsonResult['IV_HP']
    iv_atk = jsonResult['IV_Atk']
    iv_def = jsonResult['IV_Def']
    iv_spA = jsonResult['IV_SpA']
    iv_spD = jsonResult['IV_SpD']
    iv_spe = jsonResult['IV_Spe']

    # EV
    ev_hp = jsonResult['EV_HP']
    ev_atk = jsonResult['EV_Atk']
    ev_def = jsonResult['EV_Def']
    ev_spA = jsonResult['EV_SpA']
    ev_spD = jsonResult['EV_SpD']
    ev_spe = jsonResult['EV_Spe']

    # Hidden power Type
    try:
        hiddenPowerType = (((jsonResult['IV_HP'] % 2) + ((jsonResult['IV_Atk'] % 2) * 2) + (
        (jsonResult['IV_Def'] % 2) * 4) + ((jsonResult['IV_Spe'] % 2) * 8) + ((jsonResult['IV_SpA'] % 2) * 16) + (
                            (jsonResult['IV_SpD'] % 2) * 32)) * 15) // 63
    except Exception:
        return abort(404)

    # Ability
    ability = str(jsonResult['Ability'])

    # Level
    level = str(jsonResult['Level'])

    # Image
    image = ""
    for pokemon in pokemonData['pokemon']:
        if (pokemon["species"] == species):
            if(shiny.lower() == "yes"):
                image = pokemon["image"]["shiny"]
            else:
                image = pokemon["image"]["regular"]

    pokemon = {}
    # Append all the stuff into the pokemon json and return it.
    pokemon.update({"species": species})
    pokemon.update({"nickname": nickname})
    pokemon.update({"gender": gender.upper()})
    pokemon.update({"item": item.title()})
    pokemon.update({"nature": nature.title()})
    pokemon.update({"shiny": shiny.title()})
    pokemon.update({"level": int(level)})
    pokemon.update({"ability": ability.title()})
    pokemon.update({"hiddenPower": int(hiddenPowerType)})
    pokemon.update({"image": image})
    pokemon.update({"iv": {}})
    pokemon['iv'].update({"hp": int(iv_hp)})
    pokemon['iv'].update({"atk": int(iv_atk)})
    pokemon['iv'].update({"def": int(iv_def)})
    pokemon['iv'].update({"spA": int(iv_spA)})
    pokemon['iv'].update({"spD": int(iv_spD)})
    pokemon['iv'].update({"spe": int(iv_spe)})
    pokemon.update({"ev": {}})
    pokemon['ev'].update({"hp": int(ev_hp)})
    pokemon['ev'].update({"atk": int(ev_atk)})
    pokemon['ev'].update({"def": int(ev_def)})
    pokemon['ev'].update({"spA": int(ev_spA)})
    pokemon['ev'].update({"spD": int(ev_spD)})
    pokemon['ev'].update({"spe": int(ev_spe)})
    pokemon.update({"move": {}})
    pokemon['move'].update({"move1": move1.title()})
    pokemon['move'].update({"move2": move2.title()})
    pokemon['move'].update({"move3": move3.title()})
    pokemon['move'].update({"move4": move4.title()})

    response = jsonify({'pokemon': pokemon})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Get pokmon by species
@app.route('/api/v1/pokemon/<string:species>', methods=['GET'])
def pokemon(species):
    pokemon = [pkmn for pkmn in pokemonData['pokemon'] if pkmn['species'].lower() == species.lower()]
    # Detect Farfetch'd weird name.
    if ("farfetch" in species.lower()):
        pokemon = [pkmn for pkmn in pokemonData['pokemon'] if pkmn['species'] == "Farfetch'd"]

    # Detect Flabébé name to normal english
    if (species.lower() == "flabebe"):
        species = species.replace("e", "é")

    # For pokemon with spaces in name and check again.
    if len(pokemon) == 0:
        species = species.replace("-", " ")
        pokemon = [pkmn for pkmn in pokemonData['pokemon'] if pkmn['species'].lower() == species.lower()]

    if len(pokemon) == 0:
        abort(404)

    response = jsonify({'pokemon': pokemon})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Get pokemon by dex number
@app.route('/api/v1/pokemon/<int:dex>', methods=['GET'])
def pokemondex(dex):
    pokemon = [pkmn for pkmn in pokemonData['pokemon'] if pkmn['id'] == dex]
    if len(pokemon) == 0:
        abort(404)
    response = jsonify({'pokemon': pokemon})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Get pokemon by hidden ability
@app.route('/api/v1/pokemon/hiddenability/<string:ability>', methods=['GET'])
def pokemonhiddenability(ability):
    pokemon = [make_url_data(pkmn) for pkmn in pokemonData['pokemon'] if pkmn['abilities']['hidden_ability'] == ability.lower()]
    if len(pokemon) == 0:
        abort(404)
    response = jsonify({'pokemon': pokemon})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Get pokemon by ability
@app.route('/api/v1/pokemon/ability/<string:ability>', methods=['GET'])
def pokemonability(ability):
    pkmn = [make_url_data(pkmn) for pkmn in pokemonData['pokemon'] if (pkmn['abilities']['ability1'] == ability or pkmn['abilities']['ability2'] == ability.lower()) ]
    if len(pkmn) == 0:
        abort(404)
    response = jsonify({'pokemon': pokemon})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Get pokemon by type
@app.route('/api/v1/pokemon/type/<string:type>', methods=['GET'])
def pokemontype(type):
    pokemon = [make_url_data(pkmn) for pkmn in pokemonData['pokemon'] if (pkmn['types']['type1'] == type.lower() or pkmn['types']['type2'] == type.lower()) ]
    if len(pokemon) == 0:
        abort(404)
    response = jsonify({'pokemon': pokemon})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Get pokemon by gender
@app.route('/api/v1/pokemon/gender/<string:gender>', methods=['GET'])
def pokemongender(gender):
    pokemon = [make_url_data(pkmn) for pkmn in pokemonData['pokemon'] if pkmn['gender'][gender.lower()] == "true" ]
    if len(pokemon) == 0:
        abort(404)
    response = jsonify({'pokemon': pokemon})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Make uri data for pokemon
def make_url_data(pkmn):
    pkmn.update({'url':(url_for('pokemondex', dex=pkmn['id'], _external=True))})
    return pkmn

if __name__ == "__main__":
    app.run(debug=True)