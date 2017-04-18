from flask import Flask, send_from_directory
import requests, os

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
    return "<link rel=\"shortcut icon\" href=\"/favicon.ico\"><title>PKHEX Generator</title><style>footer{font-family: \"Helvetica Neue\", Arial, sans-serif;position: absolute; left:0; right: 0; padding: 1rem; bottom: 0;background-color: #efefef;text-align: center;}</style><h1>Welcome to PKHEX clipboard generator by <a href=\"https://github.com/N3evin\">N3evin</a></h1><div><fieldset><legend>Generate PKHEX clipboard format data</legend><p><h2>/spreadsheet/{spreadsheet id}/{sheet name}/{row}</h2></p><ul><li><b>spreadsheet id:</b> id from spreadsheet url.</li><li><b>sheetname:</b> sheet name from spreadsheet to read from.</li><li><b>row:</b> which row of spreadsheet to retrieve information from.</li></ul></fieldset></div><footer>Copyright &copy; <script>new Date().getFullYear()>2010&&document.write(new Date().getFullYear());</script>, <a href=\"https://github.com/N3evin/pkhex-spreadsheet\">N3evin</a></footer>"

@app.route('/spreadsheet/<string:key>/<string:sheet>/<int:row>', methods=['GET'])
def generateClipboard(key,sheet,row):
    website = "https://script.google.com/macros/s/AKfycbxOLElujQcy1-ZUer1KgEvK16gkTLUqYftApjNCM_IRTL3HSuDk/exec?id=" + key + "&sheet="+sheet
    r = requests.get(website)

    errorPage = "<link rel=\"shortcut icon\" href=\"/favicon.ico\"><title>PKHEX Generator</title><style>footer{font-family: \"Helvetica Neue\", Arial, sans-serif;position: absolute; left:0; right: 0; padding: 1rem; bottom: 0;background-color: #efefef;text-align: center;}</style><h2 align=\"center\">No pokemon found!</h2><footer>Copyright &copy; <script>new Date().getFullYear()>2010&&document.write(new Date().getFullYear());</script>, <a href=\"https://github.com/N3evin/pkhex-spreadsheet\">N3evin</a></footer>"


    try:
        jsonResult = r.json()[sheet][row-1]
    except Exception:
        return errorPage

    # information
    nickname = jsonResult['Nickname']
    species = jsonResult['Species'].capitalize()
    gender = jsonResult['Gender']
    item = " @ " + jsonResult['Item']
    nature = jsonResult['Nature'] + " Nature"
    shiny = jsonResult['Shiny']

    # Check for item.
    if(jsonResult['Item'] == "None" or jsonResult['Item'] == ""):
        item = ""

    # Check for gender
    genderImage = "https://www.transparenttextures.com/patterns/asfalt-light.png"
    if(gender.lower()=="male" or gender.lower()=="m"):
        gender = " (M)"
        genderImage = "http://cdn.mysitemyway.com/icons-watermarks/simple-black/classica/classica_mars-symbol/classica_mars-symbol_simple-black_256x256.png"
    elif(gender.lower()=="female" or gender.lower()=="f"):
        gender=" (F)"
        genderImage = "http://cdn.mysitemyway.com/icons-watermarks/simple-black/classica/classica_female-symbol/classica_female-symbol_simple-black_256x256.png"
    else:
        gender = ""

    # Special character for unknown and alola
    speciesImage = species;
    if ("-a" in species.lower()):                       # Alola form
        speciesImage = speciesImage.rsplit('-', 1)[0] + "-alola"
    elif ("-!" in species.lower()):                     # Unknown-!
        speciesImage = speciesImage.rsplit('-', 1)[0] + "-exclamation"
    elif ("-?" in species.lower()):                     # Unknown-?
        speciesImage = speciesImage.rsplit('-', 1)[0] + "-question"
    elif ("\u2640" in species.lower()):                 # with female sign
        speciesImage = "female/" + speciesImage[:-2]
        species = species[:-2]
    elif ("\u2642" in species.lower()):                 # with male sign
        speciesImage = speciesImage[:-2]
        species = species[:-2]
    elif(species.lower() == "farfetch'd"):              # farfetch'd have a special name.
        speciesImage = "farfetchd"
    elif('\u2019' in species and "oricorio" in species):# oricorio-pa’u have a special name.
        speciesImage = "oricorio-pa-u"
    elif("." in species.lower()):                       # For Mr. Mine and Mime Jr.
        species = species.title()
        speciesImage = species.replace(".","")
        speciesImage = speciesImage.replace(" ","-")

    # IV
    iv_hp = str(jsonResult['IV_HP'])
    iv_atk = str(jsonResult['IV_Atk'])
    iv_def = str(jsonResult['IV_Def'])
    iv_spA = str(jsonResult['IV_SpA'])
    iv_spD = str(jsonResult['IV_SpD'])
    iv_spE = str(jsonResult['IV_Spe'])

    # EV
    ev_hp = str(jsonResult['EV_HP'])
    ev_atk = str(jsonResult['EV_Atk'])
    ev_def = str(jsonResult['EV_Def'])
    ev_spA = str(jsonResult['EV_SpA'])
    ev_spD = str(jsonResult['EV_SpD'])
    ev_spE = str(jsonResult['EV_Spe'])

    #Hidden power Type
    try:
        hiddenPowerType = (((jsonResult['IV_HP']%2)+((jsonResult['IV_Atk']%2)*2) +((jsonResult['IV_Def']%2)*4) +((jsonResult['IV_Spe']%2)*8) +((jsonResult['IV_SpA']%2)*16)+((jsonResult['IV_SpD']%2)*32)) * 15)//63
    except Exception:
        return errorPage

    # Ability
    ability = str(jsonResult['Ability'])

    # Level
    level = str(jsonResult['Level'])

    # Moves
    moves = ""
    if(str(jsonResult['Move_1']) != ""):
        moves += "- " + str(jsonResult['Move_1']) + '\n'
    if(str(jsonResult['Move_2']) != ""):
        moves += "- " + str(jsonResult['Move_2']) + '\n'
    if(str(jsonResult['Move_3']) != ""):
        moves += "- " + str(jsonResult['Move_3']) + '\n'
    if(str(jsonResult['Move_4']) != ""):
        moves += "- " + str(jsonResult['Move_4'])

    # HTML information
    info = nickname + " (" + species + ")" + gender + item + "\nShiny: " + shiny + "\n" + nature
    ivInfo = "IVs: " + iv_hp + " HP / " + iv_atk + " Atk / " + iv_def + " Def / " + iv_spA + " SpA / " + iv_spD + " SpD / " + iv_spE + " Spe"
    evInfo = "EVs: " + ev_hp + " HP / " + ev_atk + " Atk / " + ev_def + " Def / " + ev_spA + " SpA / " + ev_spD + " SpD / " + ev_spE + " Spe"
    abilityInfo = "Ability: " + ability
    levelInfo = "Level: " + level

    result = info + "\n" + ivInfo + "\n" + evInfo + "\n" + abilityInfo + "\n" + levelInfo + "\n" + moves
    resultHtml = result.replace("\n","</br>")


    # Check if shiny set shiny image
    pokemonImage = "https://raw.githubusercontent.com/msikma/pokesprite/master/icons/pokemon/regular/"+ speciesImage.lower() +".png"
    if(shiny.lower() == "y" or shiny.lower() == "yes"):
        pokemonImage ="https://raw.githubusercontent.com/msikma/pokesprite/master/icons/pokemon/shiny/"+ speciesImage.lower() +".png"

    # Hidden power images
    hiddenPowerImage = ["http://www.serebii.net/pokedex-bw/type/fighting.gif", "http://i.imgur.com/dQbTg50.gif", "http://i.imgur.com/ph8kmn3.gif", "http://i.imgur.com/DVkKfTL.gif", "http://i.imgur.com/PGuzYhv.gif", "http://i.imgur.com/PRd5TLc.gif", "http://i.imgur.com/wslKUmD.gif", "http://i.imgur.com/R14BN7m.gif", "http://i.imgur.com/1Rzd3v5.gif", "http://i.imgur.com/MEh0HBX.gif", "http://i.imgur.com/AaHMBic.gif", "http://i.imgur.com/kgsfJi9.gif", "http://i.imgur.com/hcgblEH.gif", "http://i.imgur.com/StPY3Ym.gif", "http://i.imgur.com/vuIrzDM.gif", "http://i.imgur.com/7jFeWqg.gif", "http://i.imgur.com/4GvaM2N.gif", "http://i.imgur.com/hwZMniI.gif", "http://i.imgur.com/qXQcUfg.png"]

    webPage = "<link rel=\"shortcut icon\" href=\"/favicon.ico\"><title>PKHEX Generator</title><style>header { text-align: center;}footer { font-family: \"Helvetica Neue\", Arial, sans-serif; position: absolute; left: 0; right: 0; padding: 1rem; bottom: 0; background-color: #efefef; text-align: center;}table{border: 1px solid black; margin-left: auto; margin-right: auto;}.tableHeader{font-family: \"Lucida Console\", Monaco, monospace}.btnWrapper { text-align: center;}script { display: none;}.data { border-style: inset; width: 600px; margin: auto;}.popup { position: relative; display: inline-block; cursor: pointer;}.popup .popuptext { visibility: hidden; width: 160px; background-color: #555; color: #fff; text-align: center; border-radius: 6px; padding: 8px 0; position: absolute; z-index: 1; bottom: -225%; left: 50%; margin-left: -80px;}.popup .popuptext::after { content: ""; position: absolute; bottom: 100%; left: 50%; margin-left: -5px; border-width: 5px; border-style: solid; border-color: transparent transparent #555 transparent;}.popup .show { visibility: visible; -webkit-animation: fadeIn 1s; animation: fadeIn 1s}@-webkit-keyframes fadeIn { from { opacity: 0; } to { opacity: 1; }}@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; }}</style><script src=\"https://cdn.rawgit.com/zenorocha/clipboard.js/v1.6.0/dist/clipboard.min.js\"></script><header> <h1>"+ species +"\'s Clipboard information</h1></header><div class=\"data\"> "+ resultHtml +"</div></br><table width=\"auto\"> <tr> <td width=\"190\" class=\"tableHeader\">"+ species + " <img src=\"" + genderImage +"\" width=\"15px\"></img></td> <td class=\"tableHeader\" width=\"150\" style=\"padding-left:10px; padding-right:20px;\">Level:</td> <td width=\"186\">"+ level +"</td> <td width=\"150\" class=\"tableHeader\">Moves:</td> <td width=\"40\">Hp</td> <td width=\"40\">Atk</td> <td width=\"40\">Def</td> <td width=\"40\">SpA</td> <td width=\"40\">SpD</td> <td width=\"40\">Spe</td> </tr> <tr> <td rowspan=\"4\" align=\"middle\" background=\"http://orig09.deviantart.net/fd1f/f/2014/323/2/0/x_and_y_menu_background_1_by_phoenixoflight92-d86y3jj.png\"><img src =\""+ pokemonImage +"\" width=\"80px\"></img></td> <td class=\"tableHeader\" style=\"padding-left:10px; padding-right:20px;\">Ability:</td> <td>"+ ability +"</td> <td>" + str(jsonResult['Move_1']) + "</td> <td>" + iv_hp +"</td> <td>" + iv_atk + "</td> <td>" + iv_def + "</td> <td>" + iv_spA + "</td> <td>" + iv_spD + "</td> <td>" + iv_spE + "</td> </tr> <tr> <td class=\"tableHeader\" style=\"padding-left:10px; padding-right:20px;\">Nature:</td> <td>"+ nature[:5] +"</td> <td>" + str(jsonResult['Move_2']) + "</td> <td>&nbsp;</td> <td>&nbsp;</td> <td>&nbsp;</td> <td>&nbsp;</td> <td>&nbsp;</td> <td>&nbsp;</td> </tr> <tr> <td class=\"tableHeader\" style=\"padding-left:10px; padding-right:20px;\">Item Held:</td> <td>"+ item[2:] + "</td> <td>" + str(jsonResult['Move_3']) + "</td> <td>Hp</td> <td>Atk</td> <td>Def</td> <td>SpA</td> <td>SpD</td> <td>Spe</td> </tr> <tr> <td class=\"tableHeader\" style=\"padding-left:10px; padding-right:20px;\">Hidden Power:</td> <td><img src=\"" + hiddenPowerImage[hiddenPowerType] + "\"></img></td> <td>"+ str(jsonResult['Move_4']) +" <td>" + ev_hp + "</td> <td>" + ev_atk + "</td> <td>" + ev_def + "</td> <td>" + ev_spA + "</td> <td>" + ev_spD + "</td> <td>" + ev_spE + "</td> </tr></table></br><div class=\"btnWrapper\"> <button class=\"popup\" onclick=\"myFunction()\" data-clipboard-text=\"" + result + "\">Copy to clipboard <span class=\"popuptext\" id=\"myPopup\">Copied!</span></button></div><script type = \"text/javascript\" > var clip = new Clipboard('.popup');function myFunction() {var popup = document.getElementById(\"myPopup\");popup.classList.toggle(\"show\");} </script><footer>Copyright &copy; <script>new Date().getFullYear()>2010&&document.write(new Date().getFullYear());</script>, <a href=\"https://github.com/N3evin/pkhex-spreadsheet\">N3evin</a></footer>"

    return webPage

if __name__ == "__main__":
	app.run(debug=True)
