from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app, 'friendsdb')
@app.route('/')
def index():
	query = "SELECT * FROM friends"
	friends = mysql.query_db(query)
	return render_template('index.html', friends= friends)

@app.route('/add')
def add():
	return render_template('add.html')

@app.route('/create', methods=['POST'])
def create():
	query = "INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES (:first_name, :last_name, :occupation, NOW(), NOW())"
	data = {
	'first_name': request.form['first_name'],
	'last_name': request.form['last_name'],
	'occupation': request.form['occupation']
	}
	mysql.query_db(query, data)
	return redirect('/')

@app.route('/show/<id>')
def show(id):
	query = "SELECT * FROM `friendsdb`.`friends` WHERE id= :id"
	data = {
	'id': id
	}
	user = mysql.query_db(query, data)
	return render_template('friend.html', id= id, user = user)

@app.route('/update/<id>', methods=['POST'])
def update(id):
	query = "UPDATE `friendsdb`.`friends` SET `first_name`=:first_name, `last_name`=:last_name , `occupation`= :occupation WHERE `id`=:id"
	data = {
	'id': id,
	'first_name': request.form['first_name'],
	'last_name': request.form['last_name'],
	'occupation': request.form['occupation']
	}
	mysql.query_db(query, data)
	return redirect('/')

@app.route('/edit/<id>')
def edit(id):
	return render_template('edit.html',id=id)

@app.route('/friends/<id>/delete')
def delete(id):
	query = "DELETE FROM `friendsdb`.`friends` WHERE id = :id"
	data = {'id': id}
	mysql.query_db(query, data)
	return redirect('/')


app.run(debug=True)