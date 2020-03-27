from flask import Flask 
  
app = Flask(__name__) 
  
@app.route("/")
def route():
    return "<h1>Welcome to Chatbot</h1>"
