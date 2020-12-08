from flask import Flask, jsonify, request, url_for, redirect, session, render_template

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'Thisisasecret'

@app.route('/')
def index():
    session.pop('name',None)
    return '<h1>HELLO</h1>'

@app.route('/home',methods = ['GET','POST'],defaults = {'name':'Satyadev'})
@app.route('/home/<name>',methods = ['POST','GET'])
def home(name):
    session['name'] = name
    return render_template('home.html',name = name,display = False,mylist = ['one','two','three','four'])

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
       # loc = request.form['location']

       # return '<h1>{} {}</h1>'.format(name,loc)
        return redirect(url_for('home',name = name))

'''@app.route('/theform',methods = ['POST'])
def process():
    name = request.form['name']
    loc = request.form['location']

    return '<h1>{} {}</h1>'.format(name,loc)'''

@app.route('/processjson',methods = ['POST'])
def processjson():
    
    data = request.get_json()
    name = data['name']
    loc = data['location']
    array = data['randomlist']

    return jsonify({'result' : 'Success!','name':name,'location':loc,'list':array[2]})


if __name__ == '__main__':
    app.run()