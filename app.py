from flask import Flask
import requests


app = Flask(__name__)

@app.route('/')
def index():
    return "<title>PKHEX Generator</title><h1>Welcome to PKHEX clipboard generator by <a href=\"https://github.com/N3evin\">N3evin</a></h1><div><fieldset><legend>Generate PKHEX clipboard format data</legend><p><h2>/api/pkhex/{spreadsheet id}/{sheet name}/{row}</h2></p><ul><li><b>spreadsheet id:</b> id from spreadsheet url.</li><li><b>sheetname:</b> sheet name from spreadsheet to read from.</li><li><b>row:</b> which row of spreadsheet to retrieve information from.</li></ul></fieldset></div>"

@app.route('/api/pkhex/<string:key>/<string:sheet>/<int:row>', methods=['GET'])
def generateClipboard(key,sheet,row):
    website = "https://script.google.com/macros/s/AKfycbxOLElujQcy1-ZUer1KgEvK16gkTLUqYftApjNCM_IRTL3HSuDk/exec?id=" + key + "&sheet="+sheet
    r = requests.get(website)
    jsonResult = r.json()[sheet][row-1]

    # information
    nickname = jsonResult['Nickname']
    species = jsonResult['Species']
    gender = jsonResult['Gender']
    item = " @ " + jsonResult['Item']
    natural = jsonResult['Nature'] + " Nature"
    shiny = jsonResult['Shiny']

    # Check for item.
    if(jsonResult['Item'] == "None" or jsonResult['Item'] == ""):
        item = ""

    # Check for gender
    if(gender.lower()=="male" or gender.lower()=="m"):
        gender = " (M)"
    elif(gender.lower()=="female" or gender.lower()=="f"):
        gender=" (F)"
    else:
        gender = ""



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

    info = nickname + " (" + species + ")" + gender + item + "\nShiny: " + shiny + "\n" + natural
    ivInfo = "IVs: " + iv_hp + " HP / " + iv_atk + " Atk / " + iv_def + " Def / " + iv_spA + " SpA / " + iv_spD + " SpD / " + iv_spE + " Spe"
    evInfo = "EVs: " + ev_hp + " HP / " + ev_atk + " Atk / " + ev_def + " Def / " + ev_spA + " SpA / " + ev_spD + " SpD / " + ev_spE + " Spe"
    abilityInfo = "Ability: " + ability
    levelInfo = "Level: " + level

    result = info + "\n" + ivInfo + "\n" + evInfo + "\n" + abilityInfo + "\n" + levelInfo + "\n" + moves
    resultHtml = result.replace("\n","</br>")

    webPage = "<title>PKHEX Generator</title><style>header{text-align: center;}footer{font-family: \"Helvetica Neue\", Arial, sans-serif;position: absolute; left:0; right: 0; padding: 1rem; bottom: 0;background-color: #efefef;text-align: center;}.btnWrapper{text-align: center;}script{display: none;}.data {border-style: inset; width: 600px; margin: auto;}.popup {position: relative;display: inline-block;cursor: pointer;}.popup .popuptext {visibility: hidden;width: 160px;background-color: #555;color: #fff;text-align: center;	border-radius: 6px;	padding: 8px 0;	position: absolute;z-index: 1;	bottom: -225%;left: 50%;margin-left: -80px;	} .popup .popuptext::after {content: "";position: absolute;bottom: 100%;left: 50%;margin-left: -155px;border-width: 5px;border-style: solid; border-color: transparent transparent #555 transparent;}.popup .show {visibility: visible;-webkit-animation: fadeIn 1s;animation: fadeIn 1s}@-webkit-keyframes fadeIn {from {opacity: 0;}to {opacity: 1;}}@keyframes fadeIn {from {opacity: 0;}to {opacity:1 ;}}</style><script src=\"https://cdn.rawgit.com/zenorocha/clipboard.js/v1.6.0/dist/clipboard.min.js\"></script><header><h1>"+ species  +" \'s Clipboard information</h1></header><div class=\"data\"> "+ resultHtml +"</div></br><div class=\"btnWrapper\"><button class=\"popup\" onclick=\"myFunction()\" data-clipboard-text=\""+ result +"\">Copy to clipboard <span class=\"popuptext\" id=\"myPopup\">Copied!</span></button></div><script type=\"text/javascript\">var clip = new Clipboard('.popup'); function myFunction() {var popup = document.getElementById(\"myPopup\");popup.classList.toggle(\"show\");}</script><footer>Copyright &copy; <script>new Date().getFullYear()>2010&&document.write(new Date().getFullYear());</script>, <a href=\"https://github.com/N3evin/\">N3evin</a></footer>"

    return webPage

if __name__ == "__main__":
	app.run()