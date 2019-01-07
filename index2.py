import os
from flask import Flask, request
import requests
import traceback
import json

token = os.environ.get ('FB_ACCESS_TOKEN')


app = Flask(__name__)

@app.route ('/', methods = ['GET', 'POST'])


def webhook() :

	if request.method == 'POST':
		try:
			data = json.loads(request.data.decode())
			print(data)
			text = data['entry'][0]['messaging'][0]['message']['text']
			sender = data['entry'][0]['messaging'][0]['sender']['id']
			
			payload = location_quick_reply(sender)

			r= requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token, json=payload)
		except Exception as e:
				print(traceback.format_exc())
			

	elif request.method == 'GET':
		if request.args.get('hub.verify_token') == os.environ.get('FB_VERIFY_TOKEN'):
			return request.args.get('hub.challenge')
		return "Wrong Verify Token"
	return "Nothing"


def location_quick_reply(sender):
	return{
		"recipient":{
			"id":sender
		},
		"message":{
			"text":"Share your location:",
			"quick_replies":[
				{
					"content_type":"location",
				}			
			]
		}
	}






if __name__ == '__main__':
		app.run(debug=True)






