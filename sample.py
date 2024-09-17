from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!!'

#プログラム起動
app.run(host="localhost",port=5000,debug=True)