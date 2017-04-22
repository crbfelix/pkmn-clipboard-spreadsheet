# Pokemon's Google Spreadsheet Clipboard Generator

![Heroku](http://heroku-badge.herokuapp.com/?app=pkmnclipboard&style=flat&svg=1) 
[![ghit.me](https://ghit.me/badge.svg?repo=N3evin/pkmn-clipboard-spreadsheet)](https://ghit.me/repo/N3evin/pkmn-clipboard-spreadsheet)


A simple website that generate pkhex/pokemon showdown clipboard from google spreadsheet informations.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

### Features
- Keep track of your battle ready team for [pokemon showdown](http://pokemonshowdown.com/) easily.
- Generate PKHEX clipboard from google request form.
- Allow others to copy your battle ready pokemon from google spreadsheet.
- Much more...


### Template
You can use this [Google Spreadsheet](https://docs.google.com/spreadsheets/d/1UhGUFz6vRir5NFJ8kf0-siQF7JFvStX5ZvMYCHihlA4/edit?usp=sharing) to configure your spreadsheet information into the `config` sheet and you are good to go.


### Usage
Get the `ID` of your spreadsheet, your `sheet name` and `row number`. Paste it at the end if `https://pkmnclipboard.herokuapp.com/spreadsheet?id={ID}&name={sheet-name}&row={row-number}` without the parenthesis.

Json output: `https://pkmnclipboard.herokuapp.com/spreadsheet/{ID}/{sheet-name}/{row-number}`

Example: [https://pkmnclipboard.herokuapp.com/spreadsheet?id=1UhGUFz6vRir5NFJ8kf0-siQF7JFvStX5ZvMYCHihlA4&name=Sheet1&row=1](https://pkmnclipboard.herokuapp.com/spreadsheet?id=1UhGUFz6vRir5NFJ8kf0-siQF7JFvStX5ZvMYCHihlA4&name=Sheet1&row=1)

Example Json output: [https://pkmnclipboard.herokuapp.com/spreadsheet/1UhGUFz6vRir5NFJ8kf0-siQF7JFvStX5ZvMYCHihlA4/Sheet1/1](https://pkmnclipboard.herokuapp.com/spreadsheet/1UhGUFz6vRir5NFJ8kf0-siQF7JFvStX5ZvMYCHihlA4/Sheet1/1)

Your done! Now you can pass on the site to someone else! It's even easier if you make a copy of the google spreadsheet template above.

More APIs can be found here: [https://pkmnclipboard.herokuapp.com](https://pkmnclipboard.herokuapp.com) 

### Requirements (if you want to host)
- Python 2.X or 3.X
- [Flask](http://flask.pocoo.org/)

### Manually Setup (if you want to host)
1. Run `app.py` to start the webservice.
2. Put in the information required in the spreadsheet boxes.

### Heroku Setup (if you want to host)
Click on the `Deploy to Heroku` button and you are good to go!

### Credit
- [JSON script source](https://script.google.com/d/143u0RLuppsmYJ0B3wzo6i0jZYSfIFV2NLJMHPM-Sqczpr9bLwdffc-Wx/edit?usp=sharing)

### Credits
- Database Maintainer: [crbfelix](https://github.com/crbfelix)
- Designed by: [Randolph](#)