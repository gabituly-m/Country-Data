import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
app = Flask(__name__)
app.app_context().push()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)
API_KEY = 'YOUR_API_KEY'

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    countryName = db.Column(db.Text, unique=True, nullable=False)
    offName = db.Column(db.Text, unique=True, nullable=False)
    nativeName = db.Column(db.Text, unique=True, nullable=False)
    currency = db.Column(db.Text, nullable=False)
    curSymbol = db.Column(db.Text, nullable=False)
    capital = db.Column(db.Text, unique=True, nullable=False)
    region = db.Column(db.Text, nullable=False)
    subregion = db.Column(db.Text, nullable=False)
    language = db.Column(db.String, nullable=False)
    population = db.Column(db.Text, nullable=False)
    area = db.Column(db.Text, nullable=False)
    flag = db.Column(db.Text, nullable=False)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    print(request.form)
    user_input = request.form['country']
    countryName = user_input

    if Data.query.filter_by(countryName = user_input).first() is None:
        url = 'https://restcountries.com/v3.1/name/' + user_input
        r = requests.get(url)
        if r.status_code == 404:
            return '<h1>Oops You have to go back and type again country name</h1>' \
                   '<input type="button" value="Go Back" onclick="history.back(-1)"/>'
        countData = r.json()[0]
        offName = countData['name']['official']
        for k, item in countData['name']['nativeName'].items():
            nativeName = item['official']
            break
        capital = countData['capital'][0]
        flag = countData['flags']['png']
        for k, item in countData['currencies'].items():
            currency =  item['name']
            curSymbol = item['symbol']
        language = ', '.join(list(countData['languages'].values()))
        region = countData['region']
        subregion = countData['subregion']
        population = countData['population']
        area = float(countData['area'])
        i = Data(countryName=countryName, offName=offName, currency=currency,
                     curSymbol=curSymbol, nativeName=nativeName, capital=capital,
                     region=region, subregion=subregion, language=language, population=population,
                        area=area, flag=flag)
        db.session.add(i)
        db.session.commit()
    else:
        c = Data.query.filter_by(countryName = user_input).first()
        offName = c.offName
        nativeName = c.nativeName
        currency = c.currency
        curSymbol = c.curSymbol
        region = c.region
        subregion = c.subregion
        flag = c.flag
        capital = c.capital
        language = c.language
        area = c.area
        population = c.population
    url2 = 'https://api.openweathermap.org/data/2.5/weather?q=' + capital + '&units=metric' + '&appid=' + API_KEY
    r2 = requests.get(url2)
    temp = r2.json()['main']['temp']
    icon = r2.json()['weather'][0]['icon']
    return render_template('result.html', countryName=countryName, offName=offName, nativeName=nativeName, temp=temp,
                           icon=icon, currency=currency, curSymbol=curSymbol, capital=capital,
                         region=region, subregion=subregion, language=language, population=population,
                        area=area, flag=flag
                            )

with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)

