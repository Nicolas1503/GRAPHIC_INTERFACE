from flask import Flask,render_template,request,redirect,url_for
import random
app = Flask(__name__)

@app.route("/")
def index_html():
    with open('log.txt','r') as f:
        for line in f:
            pass
        last_line = line
    velocidad = last_line.split(';')[0]
    periodo = last_line.split(';')[1]
    n_helices = last_line.split(';')[2]
    return render_template('index.html', vel = velocidad, per = periodo, n_helices = n_helices)


if __name__ == '__main__':
    app.run()