from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def main():
  return "https://discord.com/api/oauth2/authorize?client_id=927945361471995925&permissions=8&scope=bot"

def run():
  app.run(host="0.0.0.0", port=8000)

def keep_alive():
  server = Thread(target=run)
  server.start()
