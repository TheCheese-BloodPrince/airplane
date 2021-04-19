from flask import Flask
from threading import Thread
app = Flask('')
@app.route('/')
def home():
  return "This is the web server for the airplane bot. airplane is a Discord moderation bot with a build in economy."
def run():
  app.run(host='0.0.0.0',port=8080)
def keep_alive():
  t=Thread(target=run)
  t.start()
