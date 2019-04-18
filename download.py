#!/usr/bin/env python
# coding: utf8

import praw
import urllib, mimetypes, urllib2
import os
import time
import sys
from pymongo import MongoClient

DATA_DIR = 'subreddit'

Submission = None

def is_url_image(url):    
    mimetype,encoding = mimetypes.guess_type(url)
    return (mimetype and mimetype.startswith('image'))
	
def exists_in_db(id):
	return Submission.find_one({ '_id': id }) != None
	
def insert_submission_to_db(submission):
	return Submission.insert_one(submission).inserted_id
	
def construct_submission(id, name, url, image_name, subreddit_id):
	return { \
		'_id': id, \
		'name': name, \
		'url': url, \
		'image_name': image_name, \
		'subreddit_id': subreddit_id \
	}
	
if __name__ == '__main__':
	
	try:
		arg_client_id = sys.argv[1]
		arg_client_secret = sys.argv[2]
		arg_subreddit = sys.argv[3]
		arg_limit = None
		if len(sys.argv) == 5:
			arg_limit = int(sys.argv[4])
	except:
		print "Invalid Arguments - Usage: download.py client_id client_secret subreddit <limit>"
		sys.exit()

	# setup mongodb
	db_client = MongoClient('localhost', 27017)
	db = db_client['LetsGetThisBread']
	Submission = db['Submission']
	
	# init reddit API
	reddit = praw.Reddit(client_id=arg_client_id,
					client_secret=arg_client_secret,
					user_agent='python:LetsGetThisBread:v1.0.0 (by /u/seanarwa)')
	
	if not os.path.exists(DATA_DIR + '/' + arg_subreddit):
		os.makedirs(DATA_DIR + '/' + arg_subreddit)
					
	download_count = 0
	subreddit = reddit.subreddit(arg_subreddit)
	for submission in subreddit.new(limit=None):
			
		if exists_in_db(submission.id) or download_count == arg_limit:
			break
		
		url = submission.url.encode('utf-8')
		if is_url_image(url):
			image_name = url.rsplit('/', 1)[-1]
			try:
				urllib.urlretrieve(url, DATA_DIR + '/' + arg_subreddit + '/' + image_name)
				submission_obj = construct_submission(submission.id, submission.name, url, image_name, subreddit.id)
				insert_submission_to_db(submission_obj)
				print 'Downloaded ' + url
				download_count += 1
			except:
				print "Unexpected error:", sys.exc_info()[1]
		
	print 'Download Complete.'
	sys.exit()
