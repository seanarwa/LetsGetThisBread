import os
import sys
import praw

if __name__ == '__main__':

	with open('subreddits.txt', 'r') as file:
		subreddits = file.read().splitlines()
	
	try:
		with open('credentials.txt', 'r') as file:
			credentials = file.read().splitlines()
			
		reddit = praw.Reddit(client_id=credentials[0],
				client_secret=credentials[1],
				user_agent='python:LetsGetThisBread:v1.0.0 (by /u/seanarwa)')
	except:
		print('Missing or Invalid Credentials')
		sys.exit()

	client_id = credentials[0]
	client_secret = credentials[1]

	for subreddit in subreddits:
		print('Downloading r/' + subreddit + ' ...')
		os.system('download.py ' + client_id + ' ' + client_secret +  ' ' + subreddit)
