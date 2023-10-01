import flask
from flask import jsonify
from flask import request

from sql import create_connection
from sql import execute_read_query
from sql import execute_query

import creds


#setting up an application name
app = flask.Flask(__name__)
app.config["DEBUG"] = True #allow to show errors in browser



#  API's for DATABASE access
#  Reference : From Our class CIS 3368
#create a endpoint to get user from DB : 

@app.route('/', methods=['GET'])
def home():
    return "<h1> Welcome to my API's</h1>" # http://127.0.0.1:5000
#get all users 
@app.route('/api/zoo/all', methods=['GET']) #http://127.0.0.1:5000/api/zoo/all
def api_users_all():
    myCreds = creds.Creds()
    conn = create_connection(myCreds.connectionstring, myCreds.username, myCreds.passwd, myCreds.dataBase)
    sql ="select * from zoo"
    zoo = execute_read_query(conn, sql)
    print(jsonify(zoo))
    return jsonify(zoo)





#add a user as POST method
# Reference : From Our class CIS 3368

@app.route('/api/zoo', methods=['POST']) # http://127.0.0.1:5000/api/zoo
def api_add_zoo():
 def api_add_zoo():
    request_data = request.get_json()
    newid = request_data['id']
    newdomain = request_data['domain']
    newkingdom = request_data['kingdom']
    newclass = request_data['class']
    newspecies = request_data['species']
    newage = request_data['age']
    newanimalname = request_data['animalname']
    newalive = request_data['alive']

    myCreds = creds.Creds()
    conn = create_connection(myCreds.connectionstring, myCreds.username, myCreds.passwd, myCreds.dataBase)
    sql = "insert into zoo(id, domain, kingdom, class, species, age, animalname, alive) values ('%s','%s','%s','%s','%s','%s','%s','%s')" % (newid, newdomain, newkingdom, newclass, newspecies, newage, newanimalname, newalive)

    execute_query(conn, sql)
    return 'Add user request successful!'
# update a user as PUT method
# Reference : https://restfulapi.net/http-methods/
@app.route('/api/zoo/<int:id>', methods=['PUT'])
def api_update_zoo(id):
    try:
        request_data = request.get_json()
        updatedomain = request_data['domain']
        updatekingdom = request_data['kingdom']
        updateclass = request_data['class']
        updatespecies = request_data['species']
        updateage = request_data['age']
        updateanimalname = request_data['animalname']
        updatealive = request_data['alive']

        myCreds = creds.Creds()
        conn = create_connection(myCreds.connectionstring, myCreds.username, myCreds.passwd, myCreds.dataBase)
        sql = "UPDATE zoo SET domain = %s, kingdom = %s, class = %s, species = %s, age = %s, animalname = %s, alive = %s WHERE id = %s"
        cursor = conn.cursor()
        cursor.execute(sql, (updatedomain, updatekingdom, updateclass, updatespecies, updateage, updateanimalname, updatealive, id))
        conn.commit()
        cursor.close()
        conn.close()
        return 'Update animal request successful!'
    except Exception as e:
        return str(e), 400


# Reference : https://www.w3schools.com/python/ref_requests_delete.asp
# Delete a user with DELETE method http://127.0.0.1:5000/api/zoo/1
@app.route('/api/zoo/<int:id>', methods=['DELETE'])
def api_delete_zoo_by_id(id):
    try:
        myCreds = creds.Creds()
        conn = create_connection(myCreds.connectionstring, myCreds.username, myCreds.passwd, myCreds.dataBase)
        sql = "DELETE FROM zoo WHERE id = %s"
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return "Delete request successful!"  # Respond status for success delete
    except Exception as e:
        return str(e), 500  # Respond with an error message and 500 status for internal server error

if __name__ == '__main__':
    app.run()

