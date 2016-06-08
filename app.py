from flask import Flask

from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123321'
app.config['MYSQL_DATABASE_DB'] = 'pedagogia'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/")
def main():
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT * from usuario")
	data = cursor.fetchone()
	print data
	if data is None:
		return "deu merda"
	else:
		return "deu certo"

if __name__ == '__main__':
	app.run()