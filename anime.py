from crypt import methods
from flask import Flask, render_template, request, redirect

import requests

import random


# CONSTANTS
url = 'https://api.jikan.moe/v4/top/anime?page='

data = {
	'title': '',
	'rank': 0,
	'image': ''
}
prevData = {
	'title': '',
	'rank': 0,
	'image': ''
}

score = 0


app = Flask(__name__)

@app.route('/', methods=['GET'])
def main():
	global score

	updateData()
	updateData()

	score = 0

	return render()

@app.route('/', methods=['POST'])
def onButtonClick():
	if 'higher' not in request.form and 'lower' not in request.form:
		return render()

	global data, prevData, score

	if 'higher' in request.form:
		if data['rank'] <= prevData['rank']:
			updateData()

			score += 1
			return render()
	if 'lower' in request.form:
		if data['rank'] >= prevData['rank']:
			updateData()

			score += 1
			return render()
	
	return redirect('/gameover/')



@app.route('/gameover/')
def gameover():
	gif = getGif()

	quoteData = getQuote()

	return render_template('gameover.html', gif=gif, score=score, quoteData=quoteData)


def render():
	global data, prevData, score

	return render_template('index.html', data=data, prevData=prevData, score=score)

def updateData():
	global prevData, data

	prevData = data

	success = False
	while not success:
		success = True

		data = getData()

		if data['rank'] == 0 or data['image'] == 'https://cdn.myanimelist.net/img/sp/icon/apple-touch-icon-256.png':
			data = getData()
			success = False

			continue

		for i in data:
			if data[i] == None:
				data = getData()
				success = False

				break

def getData():
	maxPage = 40

	page = random.randrange(0, maxPage)

	newData = {}

	resp = requests.get(url + str(page))

	json = resp.json()

	jsonData = json['data']

	i = random.randrange(0, len(jsonData))

	jsonData = jsonData[i]

	newData['title'] = jsonData['title'];
	newData['rank'] = jsonData['rank'];
	newData['image'] = jsonData['images']['jpg']['large_image_url'];

	return newData

def getGif():
	resp = requests.get('https://api.catboys.com/baka')

	json = resp.json()

	url = json['url']

	return url

def getQuote():
	quoteData = getQuoteData()

	while len(quoteData['quote']) > 250:
		quoteData = getQuoteData()

	return quoteData

def getQuoteData():
	quoteData = {}

	resp = requests.get('https://animechan.vercel.app/api/random')

	json = resp.json()

	quoteData['quote'] = json['quote']
	quoteData['anime'] = json['anime']
	quoteData['character'] = json['character']

	return quoteData


if __name__ == '__main__':
	app.run()