import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
db = SQLAlchemy(app)

class Weather(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    city = db.Column(db.String(200), nullable = False)
    temp = db.Column(db.Integer, nullable = False)
    desc = db.Column(db.String(200), nullable = False)
    icon = db.Column(db.Text(100), nullable = False)

    def __repr__(self):
        return 'City ' + str(id)


@app.route('/')

def index():
    return render_template('index.html')


@app.route('/temp', methods = ['GET', "POST"])

def weather():

    if request.method == 'POST':

        key = '0d95232681c289eb67495f74d23bf6d8'
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + key
        

        try:
            city = request.form['city']
            resp = requests.get(url.format(city)).json()

            weather_info = {
                'city' : city,
                'temp' : resp['main']['temp'],
                'desc' : resp['weather'][0]['description'],
                'icon' : resp['weather'][0]['icon']
            }

            current_weather = Weather(city = weather_info['city'], temp = weather_info['temp'], desc = weather_info['desc'], icon = weather_info['icon'])
            db.session.add(current_weather)


            return render_template('temp.html', weather = current_weather)

        except:
            return render_template('index.html')

    else:
        return redirect('index.html')


if __name__ == '__main__':
    app.run(debug = True)