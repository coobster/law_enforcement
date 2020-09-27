from flask import Flask,request,g
import hashlib as hasher
import sqlite3,time
from os.path import exists

app = Flask(__name__)

DATABASE = 'test.db'

#database loading function
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db
    
# database query function
def query_db(query,args=(),one=False):
    cursor = get_db().execute(query,args)
    row_value = cursor.fetchall()
    cursor.close()
    return (row_value[0] if row_value else None) if one else row_value

@app.route('/',methods = ['GET','POST'])
def index():
    page = "<h1><font color='#0000e0'>USA Police department Military Supply Spending</font></h1><p>"
    for x in [x[0] for x in query_db('select distinct state from all_states order by state')]:
        page += "<a href=\"/s/{}\">{}</a><br>\n".format(x,x) 
    return page

@app.route('/s/<data>')
def state(data):
    page = "<h1><font color='#0000e0'>USA Police department Military Supply Spending</font></h1><p>"
    page += "<h1><font color='#00e000'>{}</font></h1><p>".format(data)
    total = [float(i[0]) for i in query_db('select Acquisition_Value from all_states where state=?',(data,))]
    page += "<h1>Total: ${}</h1><p>".format(round(sum(total),2))
    for x in [x[0] for x in query_db('select distinct station_name from all_states where state=?',(data,))]:
        page += "<a href=\"/d/{}\">{}</a><br>\n".format(x,x)
    return page

@app.route('/d/<data>')
def department(data):
    page = "<h1><font color='#0000e0'>USA Police department Military Supply Spending</font></h1><p>"
    page += "<h1><font color='#00e000'>{}</font></h1><p>".format(data)
    total = [float(i[0]) for i in query_db('select Acquisition_Value from all_states where station_name=?',(data,))]
    page += "<h1>Total: ${}</h1><p>".format(round(sum(total),2)) 
    page += "<table><tr><td><b>Item Name</b></td><td><b>Cost</b></td><td><b>Quantity</b></td></tr>"
    for x in query_db('select Item_Name,Quantity,Acquisition_Value from all_states where station_name=?',(data,)):
        page += "<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(x[0],x[2],x[1])
    return page

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    # if the database is not present load the database from the military servers.
    if not exists(DATABASE):
        print('DATABASE NOT FOUND: downloading database...')
        import populate_database
    # Run the web application at localhost:4321
    app.run(host='0.0.0.0', port=4321, threaded=True)
