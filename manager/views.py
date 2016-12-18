#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import sys
import time
import telepot
import requests
import pafy

VERIFY_TOKEN = 'youtube-download-karega'
PAGE_ACCESS_TOKEN = 'EAAO5LXdwYSwBAFNtQwyXBAgswtxV9wVMQMoUO887BT4dE8qFykRoyqEftoe2GHJe35HuLHL8ZAPmWWoW4evqBTO6cYUdFO7CYqKtyBLXvMrIxApNQe5iZBRmC3S6g0HEZBKOwzZAG0OXSrcZBGMcBlEHtKO57ownY3cDvAYMevwZDZD'

def post_facebook_message(fbid, message_text):
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
	response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":message_text}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
	print status.json()

class MyChatBotView(generic.View):
	def get (self, request, *args, **kwargs):
		if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
			return HttpResponse(self.request.GET['hub.challenge'])
		else:
			return HttpResponse('Invalid token.')

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return generic.View.dispatch(self, request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		incoming_message= json.loads(self.request.body.decode('utf-8'))
		print incoming_message

		for entry in incoming_message['entry']:
			for message in entry['messaging']:
				print message
				try:
					sender_id = message['sender']['id']
					message_text = message['message']['text']
					
					words = message_text.split(' ')
					flag_URL = 0
					flag_VIDEO = 0
					title = '_'
					url = '_'

					for text in words:
						if text.startswith('https://') or text.startswith('www.') or text.startswith('youtu'):
							url = text
							flag_URL = 1
						elif text.lower().startswith('video'):
							flag_VIDEO = 1
					
					if flag_URL == 0:
						message_text = 'Please enter a video link to download.'

					'''else:
						video = pafy.new(url)
						best = video.getbest()
						message_text = video.title + '\t(' + video.duration + ')'
						post_facebook_message(sender_id,message_text)
						
						if flag_VIDEO == 1:
						    r = requests.get('http://tinyurl.com/api-create.php?url=' + best.url)
						    message_text = 'Download Video: ' + str(r.text)
						    post_facebook_message(sender_id,message_text)

						else :
							bestaudio = video.getbestaudio(preftype="m4a")
							r = requests.get('http://tinyurl.com/api-create.php?url=' + bestaudio.url)
							message_text = 'Download Audio: ' + str(r.text)
							post_facebook_message(sender_id,message_text)
							message_text = 'IMPORTANT: After downloading, rename the file to (anyname).m4a.\nNOTE: You could also save in .mp3 extension, but m4a provides better quality!'
							post_facebook_message(sender_id,message_text)'''
						    
				except Exception as e:
					print e
					pass

		return HttpResponse()

def index(request):
	return HttpResponse('Building Youtube Downloader Bot!')