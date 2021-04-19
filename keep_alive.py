from flask import Flask
from threading import Thread
app = Flask('')
@app.route('/')
def home():
  return "This is the web server for the nyooom bot."
def run():
  app.run(host='0.0.0.0',port=8080)
def keep_alive():
  t=Thread(target=run)
  t.start()