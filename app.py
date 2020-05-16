from flask import Flask, render_template, request,redirect, url_for
import string
import os
from scripts import creds
import requests

filepath = os.path.dirname(__file__)


app = Flask(__name__)

app.debug=True
apiurl = 'http://192.168.1.29:7878/'

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return '404'
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return '500'
    return render_template('404.html'), 404



@app.route('/kill/<player>')
def kill(player):
    url = apiurl+'v2/players/kill?token=%s&player=%s' % (creds.token,player)
    print(url)
    data = requests.get(url)
    return redirect(url_for('home'))



@app.route('/')
def home():
    url = apiurl+'v2/server/status'
    data = requests.get(url)
    data = data.json()
    users = apiurl+'v2/players/list?token=%s' % creds.token
    users = requests.get(users)
    users = users.json()
    users = users['players']
    return render_template('home.html', data=data, users=users)

@app.route('/meteor')
def meteor():
    url = apiurl+'world/meteor?token=%s' % (creds.token)
    data = requests.get(url)
    return redirect(url_for('home'))

@app.route('/detail<player>')
def detail(player):
    url = apiurl+'v3/players/read?token=%s&player=%s' % (creds.token,player)
    playerdata = requests.get(url)
    playerdata = playerdata.json()
    return render_template('player.html', data=playerdata)



@app.route('/bcast', methods=['GET','POST'])
def bcast():
    if request.method == 'POST':
        postdata = request.values
        postdata = postdata.to_dict()
        message = postdata['bcast']


        url = apiurl+'v2/server/broadcast?token=%s&msg=%s' % (creds.token,message)
        print(url)
        data = requests.get(url)
        data = data.json()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
