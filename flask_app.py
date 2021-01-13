from flask import *
import psycopg2
from pullinfo import cipher, salt
import hashlib
import datetime
import time

user = psycopg2.connect(database="main", user="db_creator", password="12345Q", host="localhost",port= 5432)
cursor = user.cursor()
app = Flask(__name__)
__nameUser = ""
__b_dateUser = ""
__b_placeUser= ""
__mailUser = ""
__passwordUser = ""
__role = ""
__idUser = 0
__total = 0
now = 0
curr_pg_user = 0
curr_pg_st = 0
i_counter = 1

'''def checkLogin(login):
	if login == "":
		redirect(url_for('login'))'''

def addKav(help:str):
	return "'"+help+"'"

dictMounth = {"1": "Jan", "2": "Feb", "3":"Mar", "4":"Apr",
					"5": "May", "6": "Jun", "7": "Jul", "8":"Aug",
					"9": "Sep", "10": "Oct", "11":"Nov", "12":"Dec"}

dictDay = {"0": "Mon", "1": "Tue", "2": "Wed", "3": "Thu",
			"4": "Fri", "5": "Sat", "6": "Sun"}

def getTime():
	while True:
		return datetime.datetime.now()
		

@app.route('/')
@app.route('/login')
def login():
	return render_template('reg.html')
	
@app.route('/validate', methods=["POST"])
def validate():
	if request.method == "POST":
		global __nameUser, __mailUser, __b_dateUser, __b_placeUser, __mailUser, __passwordUser
		global __idUser, __total, __role, now, user, i_counter

		__mailUser = request.form.get("email")
		__passwordUser = hashlib.pbkdf2_hmac('sha256', request.form.get("pass").encode(), salt, 100000).hex()

		cursor.execute("""SELECT * 
							FROM data_login 
							WHERE email=%s AND password=%s """, (__mailUser, __passwordUser))
		answer = cursor.fetchall()

		if  (len(answer) != 0):
			__idUser = answer[0][2]

			cursor.execute("""SELECT * 
								FROM info_user 
								WHERE id_user= %s""", 
								([__idUser]))
			answer = cursor.fetchall()[0]

			__nameUser = answer[1]
			__b_placeUser= answer[2]
			__b_dateUser = answer[3]
			__role = answer[4]

			cursor.execute("""SELECT * 
								FROM bank_info WHERE id_user= %s""", 
								([__idUser]))
			answer = cursor.fetchall()[0]

			__total = answer[2]
			now = getTime()
			mt = dictMounth[str(now.month)]
			day = dictDay[str(now.weekday())]

			cursor.execute("""INSERT INTO log (email, date_log)
								VALUES (%s, %s)""", 
								(__mailUser, now.strftime("{} {} %d %Y %H:%M:%S").format(day, mt)))
			user.commit()
			if __role == "owner": 
				user = psycopg2.connect(database="main", user="head", password="123456W", host="localhost",port=5432)
			return redirect(url_for('indexer'))
		else: return redirect(url_for('login'))
	
@app.route('/add', methods=["POST"])
def add():
	user = psycopg2.connect(database="main", user="db_creator", password="12345Q", host="localhost",port= 5432)
	cursor = user.cursor()
	cursor.execute("""SELECT card_number
						FROM bank_info 
						WHERE id_user= %s""", 
						([__idUser]))
	answer = cursor.fetchall()[0]

	answer = cipher.decrypt(answer[0].encode('utf-8')).decode('utf-8')
	cardNum = "**** **** **** "+ str(answer)[-4:]

	cursor.execute("""SELECT info_user.id_user, info_user.name, info_work.phone 
						FROM info_user RIGHT JOIN  info_work ON (info_user.name=info_work.name) 
						WHERE info_user.id_user= %s""", 
						([__idUser]))
	answer = cursor.fetchall()[0] 
	
	phone = answer[2]
	return render_template("addbalance.html", name=__nameUser, 
							login=__mailUser, b_date=__b_dateUser, 
							b_place=__b_placeUser, money=__total, 
							card=cardNum, phone=phone)

@app.route('/up', methods=["POST"])
def up():
	global __total
	addbalance = request.form.get("add")
	__total = __total + int(addbalance)

	user = psycopg2.connect(database="main", user="db_creator", password="12345Q", host="localhost",port= 5432)
	cursor = user.cursor()

	cursor.execute("""UPDATE bank_info 
						SET amount=%s 
						WHERE id_user= %s""", 
						(__total ,__idUser))
	user.commit()

	user = psycopg2.connect(database="main", user="db_creator", password="12345Q", host="localhost",port=5432)
	cursor = user.cursor()

	cursor.execute("""DELETE FROM curr_service WHERE (curr_service IS NULL) AND (curr_time IS NULL)""")
	user.commit()
	return redirect(url_for('indexer'))


@app.route('/last', methods=["POST"])
def last():
	global curr_pg_user
	curr_pg_user -= 5
	return redirect(url_for('account'))


@app.route('/next', methods=["POST"])
def next():
	global curr_pg_user
	curr_pg_user += 5
	return redirect(url_for('account'))
	


@app.route('/account', methods=["POST", "GET"])
def account():
	if __role == "owner":
		dictServ = []
		user = psycopg2.connect(database="main", user="head", password="123456W", host="localhost",port=5432)
		cursor = user.cursor()

		cursor.execute("""SELECT data_login.id_user, info_user.name, info_work.phone, data_login.email, data_login.password
							FROM data_login 
							RIGHT JOIN info_user ON (data_login.id_user=info_user.id_user) 
							RIGHT JOIN info_work ON (info_work.name = info_user.name)
							ORDER BY id_user
							LIMIT 5
							OFFSET %s
						""", ([curr_pg_user]))
		answer = cursor.fetchall()
		for i in answer:
			helpDict = {}
			helpDict["id_user"] = int(i[0])
			helpDict["name"] = i[1]
			helpDict["phone"] = i[2]
			helpDict["email"] = i[3]
			helpDict["password"] = i[4]
			dictServ.append(helpDict)

		return render_template('users.html', name=__nameUser, 
							login=__mailUser, b_date=__b_dateUser, 
							b_place=__b_placeUser, dict=dictServ, 
							money=__total, cpg=int(curr_pg_user/5)+1)

	else: return render_template("account.html", name=__nameUser, 
							login=__mailUser, b_date=__b_dateUser, 
							b_place=__b_placeUser, password=__passwordUser, 
							money=__total)

@app.route('/edit/<id_user>', methods=["POST"])
def edit(id_user):
	user = psycopg2.connect(database="main", user="db_creator", password="12345Q", host="localhost",port= 5432)
	cursor = user.cursor()

	cursor.execute("""SELECT data_login.id_user, info_user.name, info_work.phone, data_login.email, data_login.password
						FROM data_login 
						RIGHT JOIN info_user ON (data_login.id_user=info_user.id_user) 
						RIGHT JOIN info_work ON (info_work.name = info_user.name)
						WHERE data_login.id_user=%s""",
						([id_user]))
	answer = cursor.fetchall()[0]
	helpDict = {}
	helpDict["id_user"] = int(answer[0])
	helpDict["name"] = answer[1]
	helpDict["phone"] = answer[2]
	helpDict["email"] = answer[3]
	helpDict["password"] = answer[4]
	return render_template("adccount.html", dict=helpDict,
							name=__nameUser, login=__mailUser,
							b_date=__b_dateUser, b_place=__b_placeUser)

@app.route('/order/<ordID>/<ordName>/<int:ordCost>', methods=["POST"])
def order(ordID, ordName,ordCost):
	user = psycopg2.connect(database="main", user="db_creator", password="12345Q", host="localhost",port= 5432)
	cursor = user.cursor()

	cursor.execute("""SELECT card_number
						FROM bank_info
						WHERE id_user = %s""",
						([__idUser]))
	answer = cursor.fetchall()[0]
	answer = cipher.decrypt(answer[0].encode('utf-8')).decode('utf-8')
	cardNum = "**** **** **** "+ str(answer)[-4:]

	cursor.execute("""SELECT info_user.id_user, info_user.name, info_work.phone
						FROM info_user 
						RIGHT JOIN info_work ON (info_user.name=info_work.name) 
						WHERE info_user.id_user=%s""",
						([__idUser]))  
	answer = cursor.fetchall()[0]
	phone = answer[2]
	return render_template("order.html", name=__nameUser, 
							login=__mailUser, b_date=__b_dateUser, 
							b_place=__b_placeUser, order=ordName, 
							cost=ordCost, money=__total, card=cardNum,
							phone=phone)
	#return redirect(url_for('about'))

@app.route('/pay/<ordName>/<int:ordCost>', methods=["POST"])
def pay(ordCost, ordName):
	global __total, now
	__total = __total - ordCost

	user = psycopg2.connect(database="main", user="db_creator", password="12345Q", host="localhost",port= 5432)
	cursor = user.cursor()
	cursor.execute("""UPDATE bank_info 
						SET amount=%s
						WHERE id_user=%s""",
						(__total, __idUser))
	user.commit()

	now = getTime()
	mt = dictMounth[str(now.month)]
	day = dictDay[str(now.weekday())]

	user = psycopg2.connect(database="main", user="db_creator", password="12345Q", host="localhost",port= 5432)
	cursor = user.cursor()
	cursor.execute("""UPDATE curr_service 
						SET curr_service=%s,curr_time=%s
						WHERE id_user=%s AND curr_service IS NULL AND curr_time IS NULL""",
						(ordName, now.strftime("{} {} %d %Y %H:%M:%S").format(day, mt),(__idUser)))
	user.commit()
	return redirect(url_for('indexer'))

@app.route('/status', methods=["POST", "GET"])
def status():
	dictServ = []

	user = psycopg2.connect(database="main", user="db_creator", password="12345Q", host="localhost",port= 5432)
	cursor = user.cursor()
	cursor.execute("""SELECT *
						FROM curr_service
						WHERE id_user=%s
						ORDER BY curr_time DESC""",
						([__idUser]))

	answer = cursor.fetchall()
	for i in (i for i in answer):
		helpDict = {}
		helpDict["id_user"] = int (i[1])
		helpDict["curr_service"] = i[2]
		helpDict["curr_time"] = i[3]
		helpDict["status"] = i[4]
		if helpDict["status"] == False: helpDict["status"] = "In process"
		else: helpDict["status"] = "Ready"
		dictServ.append(helpDict)
	return render_template("status.html", name=__nameUser, login=__mailUser,
							 b_date=__b_dateUser, b_place=__b_placeUser, 
							 dict=dictServ, money=__total)

@app.route('/done/<idUser>/<ordName>/<ordDate>', methods=["POST"])
def  done (idUser, ordName, ordDate):
	global __total
	if __role == "owner":
		user = psycopg2.connect(database="main", user="head", password="123456W", host="localhost",port=5432)
		cursor = user.cursor()
		cursor.execute("""SELECT curr_service, curr_time, service.cost
							FROM curr_service 
							RIGHT JOIN service ON (curr_service.curr_service = service.serv_name) 
							WHERE id_user = %s AND curr_time LIKE %s AND curr_service LIKE %s""",
							(idUser, ordDate, ordName))
		answer = cursor.fetchall()[0]
		plus = answer[2]

		cursor.execute("""UPDATE curr_service
							SET status=%s
							WHERE id_user=%s AND curr_time LIKE %s AND curr_service LIKE %s""",
							(True, idUser, ordDate,ordName))
		user.commit()
		__total += plus
		user = psycopg2.connect(database="main", user="head", password="123456W", host="localhost",port=5432)
		cursor = user.cursor()
		cursor.execute("""UPDATE bank_info
							SET amount=%s
							WHERE id_user=%s""",
							(__total, __idUser))
		user.commit()

		user = psycopg2.connect(database="main", user="head", password="123456W", host="localhost",port=5432)
		cursor = user.cursor()
		cursor.execute("""DELETE FROM curr_service
							WHERE curr_service IS NULL AND curr_time IS NULL""")
		user.commit()

		return redirect(url_for('service'))


@app.route('/cancel/<idUser>/<ordName>/<ordDate>', methods=["POST"])
def  canceler (idUser, ordName, ordDate):
	global __total
	if __role == "owner":
		user = psycopg2.connect(database="main", user="head", password="123456W", host="localhost",port=5432)
		cursor = user.cursor()
		cursor.execute("""SELECT curr_service, curr_time, service.cost
							FROM curr_service 
							RIGHT JOIN service ON (curr_service.curr_service = service.serv_name) 
							WHERE id_user = %s AND curr_time LIKE %s AND curr_service LIKE %s""",
							(idUser, ordDate, ordName))
		answer = cursor.fetchall()[0]
		minus = answer[2]

		user = psycopg2.connect(database="main", user="head", password="123456W", host="localhost",port=5432)
		cursor = user.cursor()
		cursor.execute("""DELETE FROM curr_service
							WHERE id_user=%s AND curr_time LIKE %s AND curr_service LIKE %s""",
							(idUser, ordDate, ordName))
		user.commit()

		user = psycopg2.connect(database="main", user="head", password="123456W", host="localhost",port=5432)
		cursor = user.cursor()
		cursor.execute("""SELECT *
							FROM bank_info
							WHERE id_user=%s""",
							([idUser]))
		answer = cursor.fetchall()[0]
	
		summ = answer[2] + minus

		cursor.execute("""UPDATE bank_info
							SET amount=%s
							WHERE id_user=%s""",
							(summ, idUser))
		user.commit()

		cursor.execute("""DELETE FROM curr_service
							WHERE curr_service IS NULL AND curr_time IS NULL""")
		user.commit()

		return redirect(url_for('service'))

@app.route('/cancel/<ordName>/<ordDate>', methods=["POST"])
def  cancel(ordName, ordDate):
	global __total
	user = psycopg2.connect(database="main", user="db_creator", password="12345Q", host="localhost",port= 5432)
	cursor = user.cursor()
	cursor.execute("""SELECT curr_service, curr_time, service.cost
						FROM curr_service 
						RIGHT JOIN service ON (curr_service.curr_service = service.serv_name)
						WHERE id_user = %s AND curr_time LIKE %s AND curr_service LIKE %s""",
						(__idUser, ordDate, ordName))
	answer = cursor.fetchall()[0]
	__total += answer[2]
	cursor.execute("""DELETE FROM curr_service
							WHERE id_user=%s AND curr_time LIKE %s AND curr_service LIKE %s""",
							(__idUser, ordDate, ordName))

	user.commit()
	cursor.execute("""UPDATE bank_info
							SET amount=%s
							WHERE id_user=%s""",
							(__total, __idUser))
	user.commit()

	cursor.execute("""DELETE FROM curr_service
							WHERE curr_service IS NULL AND curr_time IS NULL""")
	user.commit()

	return redirect(url_for('service'))

@app.route('/about', methods=["POST"])
def about():
	return render_template("about.html", name=__nameUser, 
							login=__mailUser, b_date=__b_dateUser, 
							b_place=__b_placeUser, money=__total)

@app.route('/lastPg', methods=["POST"])
def lastPg():
	global curr_pg_st
	curr_pg_st -= 5
	return redirect(url_for('service'))


@app.route('/nextPg', methods=["POST"])
def nextPg():
	global curr_pg_st
	curr_pg_st += 5
	return redirect(url_for('service'))

@app.route('/service', methods=["POST", "GET"])
def service():
	dictServ = []
	if __role == "owner":
		user = psycopg2.connect(database="main", user="head", password="123456W", host="localhost",port=5432)
		cursor = user.cursor()
		cursor.execute("""SELECT curr_service.id_user, info_user.name ,curr_service.curr_service, 
								curr_service.curr_time, service.cost, curr_service.status
							FROM curr_service 
							RIGHT JOIN info_user ON (curr_service.id_user = info_user.id_user) 
							RIGHT JOIN service ON (curr_service.curr_service = service.serv_name) 
							WHERE curr_service.curr_service IS NOT NULL
							ORDER BY curr_service.curr_time DESC
							LIMIT 5
							OFFSET %s""",
							([curr_pg_st]))
		answer = cursor.fetchall()
		for i in (i for i in answer):	
			helpDict = {}
			helpDict["id_user"] = int(i[0])
			helpDict["name"] = i[1]
			helpDict["curr_service"] = i[2]
			helpDict["curr_time"] = i[3]
			helpDict["cost"] = i[4]
			helpDict["status"] = i[5]
			if helpDict["status"] == False: helpDict["status"] = "In process"
			else: helpDict["status"] = "Ready"
			dictServ.append(helpDict)
		return render_template("adstatus.html", name=__nameUser, login=__mailUser,
								 b_date=__b_dateUser, b_place=__b_placeUser, 
								 dict=dictServ, money=__total, cpg=int(curr_pg_st/5)+1)
	else:
		user = psycopg2.connect(database="main", user="db_creator", password="12345Q", host="localhost",port= 5432)
		cursor = user.cursor()
		cursor.execute("""SELECT *
							FROM service""")
		answer = cursor.fetchall()
		for i in (i for i in answer):
			if __total >= int(i[2]):
				helpDict = {}
				helpDict["id"] = int (i[0])
				helpDict["name"] = i[1]
				helpDict["cost"] = int(i[2])
				dictServ.append(helpDict)

		return render_template("service.html", name=__nameUser, login=__mailUser,
								 b_date=__b_dateUser, b_place=__b_placeUser, 
								 dict=dictServ, money=__total)

@app.route('/change/<id_user>', methods=["POST"])
def changeByAdmin(id_user):
	if __role == "owner":
		nameUser = request.form.get("name")
		mailUser = request.form.get("login")
		phone = request.form.get("phone")
		passwordUser = hashlib.pbkdf2_hmac('sha256', request.form.get("pass").encode(), salt, 100000).hex()

		user = psycopg2.connect(database="main", user="head", password="123456W", host="localhost",port=5432)
		cursor = user.cursor()
		cursor.execute("""UPDATE data_login
							SET email=%s, password=%s
							WHERE id_user=%s""",
							(mailUser, passwordUser, id_user))
		user.commit()

		user = psycopg2.connect(database="main", user="head", password="123456W", host="localhost",port=5432)
		cursor = user.cursor()
		cursor.execute("""UPDATE info_user
							SET name=%s
							WHERE id_user=%s""",
							(nameUser, id_user))
		user.commit()

		user = psycopg2.connect(database="main", user="head", password="123456W", host="localhost",port=5432)
		cursor = user.cursor()
		cursor.execute("""UPDATE info_work
							SET phone=%s
							WHERE name=%s""",
							(nameUser, id_user))
		user.commit()
		return redirect(url_for('indexer'))

@app.route('/change', methods=["POST"])
def change():
	global __nameUser, __mailUser, __b_dateUser, __b_placeUser, __mailUser, __passwordUser, __idUser
	__nameUser = request.form.get("name")
	__mailUser = request.form.get("login")
	__b_dateUser = "Mon" + " " + dictMounth[request.form.get("mounth")] + " " + request.form.get("day") + " " + request.form.get("year") + " " + "21:04:37"
	__b_placeUser = request.form.get("ncity")
	__passwordUser = hashlib.pbkdf2_hmac('sha256', request.form.get("pass").encode(), salt, 100000).hex()

	user = psycopg2.connect(database="main", user="db_creator", password="12345Q", host="localhost",port= 5432)
	cursor = user.cursor()
	cursor.execute("""UPDATE data_login
						SET email=%s, password=%s
						WHERE id_user = %s""",
						(__mailUser, __passwordUser, __idUser))
	user.commit()

	user = psycopg2.connect(database="main", user="db_creator", password="12345Q", host="localhost",port= 5432)
	cursor = user.cursor()
	cursor.execute("""UPDATE info_user
						SET name=%s, home_place=%s, b_date=%s
						WHERE id_user = %s""",
						(__nameUser, __b_placeUser, __b_dateUser, __idUser))
	user.commit()

	return redirect(url_for('indexer'))


@app.route('/main')
def indexer():
	if __role == "owner": return render_template('adindex.html', name=__nameUser, 
							login=__mailUser, b_date=__b_dateUser, 
							b_place=__b_placeUser, money=__total)

	else: return render_template('index.html', name=__nameUser, 
							login=__mailUser, b_date=__b_dateUser, 
							b_place=__b_placeUser, money=__total)
	

if __name__ == '__main__':
	app.run(debug=True)