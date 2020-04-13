from flask import Flask,render_template,request
import requests
import configparser

app = Flask(__name__)

@app.route('/weather')
def hello():
	return render_template('combine.html',metadata="Check your city...")

@app.route('/weather/city', methods=['POST'])
def handle_data():

	city = str(request.form['city'])
	#read config file
	Config = configparser.ConfigParser()
	Config.read("config.ini")

	#weather api
	secret = Config.get('Key','WEATHER_KEY')
	url = 'http://api.openweathermap.org/data/2.5/weather'
	params = {'q': city, 'units': 'metric', 'appid': secret}
	response = requests.get(url = url, params = params)

	temp = str(response.json()['main']['temp'])
	feels_like = str(response.json()['main']['feels_like'])
	description = ""#str(response.json()['weather'][0]['description'])
	temp_int = int(float(temp))

	#cases 'Hot','warm','cool','chilly','cold','freezing'
	if temp_int >= 28:
		description = "Hot"
	elif 16 <= temp_int < 28:
		description = "Warm"
	elif 10 <= temp_int < 16:
		description = "Cool"
	elif 6 <= temp_int < 10:
		description = "Chilly"
	elif 0 <= temp_int < 6:
		description = "Cold"
	else:
		description = "Freezing"

	#giphy api
	secret_giphy = Config.get('Key','GIPHY_KEY')
	url_giphy = 'http://api.giphy.com/v1/gifs/translate'
	params_giphy = {'s': description, 'api_key': secret_giphy}
	response_giphy = requests.get(url = url_giphy, params = params_giphy)

	url_giphy = str(response_giphy.json()['data']['images']['original']['url'])

	#return ('Temperature in ' + city + ' is: ' + temp + " " +
	#		"<img src="+url_giphy+"/> ")
	#return render_template('weather.html',city = city ,temp = temp, url=url_giphy, feel=feels_like,des=description)		
	return render_template('combine.html',show=1,metadata="Check anoter city...",city = city ,temp = temp, url=url_giphy, feel=feels_like,des=description) 

@app.errorhandler(500)
def page_not_found(e):
    return render_template('combine.html',metadata="City Not Found!")


if __name__ == "__main__":
	app.run(debug = False) 
