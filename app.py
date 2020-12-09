from flask import Flask, jsonify, request, url_for, redirect, session, render_template, g
import sqlite3 

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'Thisisasecret'

def connect_db():
    sql = sqlite3.connect('data.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g,'sqlite3'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g,'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def index():
    session.pop('name',None)
    return '<h1>HELLO</h1>'


@app.route('/home',methods = ['GET','POST'],defaults = {'name':'Satyadev'})
@app.route('/home/<name>',methods = ['POST','GET'])
def home(name):
    session['name'] = name
    db = get_db()
    curs = db.execute('select id,name,location from users')
    results = curs.fetchall()
    return render_template('home.html',name = name,display = False,mylist = ['one','two','three','four'],results = results)


@app.route('/render')
def render():
    return render_template('tt.html')


@app.route('/json')
def json():
    if 'name' in session:
        name = session['name']
    else:
        name = 'Not in Session!'
    return jsonify({'key' : 'value','key2' : [1,2,3], 'name':name})


@app.route('/query')
def query():
    name = request.args.get('name')
    loc = request.args.get('location')
    return '<h1> You are on the query page {} {}</h1>'.format(name,loc)


@app.route('/theform',methods = ['GET','POST'])
def theform():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        name = request.form['name']
        loc = request.form['location']
        
        db = get_db()
        db.execute('insert into users (name,location) values (?,?)',[name,loc])
        db.commit()
        return redirect(url_for('home',name = name))


@app.route('/processjson',methods = ['POST'])
def processjson():
    
    data = request.get_json()
    name = data['name']
    loc = data['location']
    array = data['randomlist']

    return jsonify({'result' : 'Success!','name':name,'location':loc,'list':array[2]})


@app.route('/viewresults')
def viewresults():
    db = get_db()
    curs = db.execute('select id,name,location from users')
    results = curs.fetchall()
    return 'The id is {}, name is {}, location is {}'.format(results[1]['id'],results[1]['name'],results[1]['location'])


if __name__ == '__main__':
    app.run()