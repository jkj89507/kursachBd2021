from flask import *
from work_withBD import *
import datetime
import time

user = Control("main", "db_creator", "12345Q", "localhost", 5432)
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
		global __nameUser, __mailUser, __b_dateUser, __b_placeUser, __mailUser, __passwordUser, __idUser, __total, __role, now, user
		__mailUser = request.form.get("email")
		__passwordUser = request.form.get("pass")
		answer = user.printCurrEl("data_login WHERE email={} AND password={}".format(addKav(__mailUser), addKav(__passwordUser)))
		if  (len(answer) != 0):
			__idUser = answer[0][2]
			answer = user.printCurrEl("info_user WHERE id_user={}".format(__idUser))[0]
			__nameUser = answer[1]
			__b_placeUser= answer[2]
			__b_dateUser = answer[3]
			__role = answer[4]
			answer = user.printCurrEl("bank_info WHERE id_user={}".format(__idUser))[0]
			__total = answer[2]
			now = getTime()
			mt = dictMounth[str(now.month)]
			day = dictDay[str(now.weekday())]


			user.createElTable("log", (__mailUser, now.strftime("{} {} %d %Y %H:%M:%S").format(day, mt)))
			if __role == "owner": 
				user = Control("main", "head", "123456W", "localhost", 5432)
			return redirect(url_for('indexer'))
		else: return redirect(url_for('login'))
	
@app.route('/add', methods=["POST"])
def add():
	answer = user.printCurrEl("bank_info WHERE id_user={}".format(__idUser))[0][1][-4:]
	cardNum = "**** **** **** "+ str(answer) 
	answer = user.printCurrEl("info_user RIGHT JOIN info_work ON (info_user.name=info_work.name) WHERE info_user.id_user={}".format(__idUser),
		"info_user.id_user, info_user.name, info_work.phone")
	phone = answer[0][2]
	return render_template("addbalance.html", name=__nameUser, 
							login=__mailUser, b_date=__b_dateUser, 
							b_place=__b_placeUser, money=__total, 
							card=cardNum, phone=phone)

@app.route('/up', methods=["POST"])
def up():
	global __total
	addbalance = request.form.get("add")
	__total = __total + int(addbalance)
	user.updateElTable("bank_info", "id_user={}".format(__idUser), 
									amount=str(__total))
	user.deleteElTable("curr_service", "curr_service IS NULL AND curr_time IS NULL")
	return redirect(url_for('indexer'))


@app.route('/account', methods=["POST"])
def account():
	if __role == "owner":
		dictServ = [] 
		answer = user.printCurrEl("data_login RIGHT JOIN info_user ON (data_login.id_user=info_user.id_user) RIGHT JOIN info_work ON (info_work.name = info_user.name)",
						"data_login.id_user, info_user.name, info_work.phone, data_login.email, data_login.password", "id_user")
		for i in answer:
			helpDict = {}
			helpDict["id_user"] = int(i[0])
			helpDict["name"] = i[1]
			helpDict["phone"] = i[2]
			helpDict["email"] = i[3]
			helpDict["password"] = i[4]
			dictServ.append(helpDict)

		return render_template('users.html', nname=__nameUser, login=__mailUser,
							 b_date=__b_dateUser, b_place=__b_placeUser, 
							 dict=dictServ, money=__total)

	else: return render_template("account.html", name=__nameUser, 
							login=__mailUser, b_date=__b_dateUser, 
							b_place=__b_placeUser, password=__passwordUser, 
							money=__total)

@app.route('/order/<ordID>/<ordName>/<int:ordCost>', methods=["POST"])
def order(ordID, ordName,ordCost):
	answer = user.printCurrEl("bank_info WHERE id_user={}".format(__idUser))[0][1][-4:]
	cardNum = "**** **** **** "+ str(answer) 
	answer = user.printCurrEl("info_user RIGHT JOIN info_work ON (info_user.name=info_work.name) WHERE info_user.id_user={}".format(__idUser),
		"info_user.id_user, info_user.name, info_work.phone")
	phone = answer[0][2]
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
	user.updateElTable("bank_info", "id_user={}".format(__idUser), 
									amount=str(__total))
	now = getTime()
	mt = dictMounth[str(now.month)]
	day = dictDay[str(now.weekday())]
	user.updateElTable("curr_service", "id_user={} AND curr_service IS NULL AND curr_time IS NULL".format(__idUser), 
						curr_service=addKav(ordName), curr_time=addKav(now.strftime("{} {} %d %Y %H:%M:%S").format(day, mt)))
	return redirect(url_for('indexer'))

@app.route('/status', methods=["POST"])
def status():
	dictServ = []
	for i in (i for i in user.printCurrEl("curr_service WHERE id_user={}".format(__idUser), "*", "curr_time DESC")):
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

@app.route('/cancel/<ordName>/<ordDate>', methods=["POST"])
def  cancel(ordName, ordDate):
	global __total
	answer = user.printCurrEl("curr_service RIGHT JOIN service ON (curr_service = service.serv_name) WHERE id_user = {} AND curr_time = {} AND curr_service = {}".format(__idUser, addKav(ordDate), addKav(ordName)),
		"curr_service, curr_time, service.cost")[0]
	__total += answer[2]
	user.deleteElTable("curr_service", "id_user={} AND curr_time={} AND curr_service={}".format(__idUser, addKav(ordDate), addKav(ordName)))
	user.updateElTable("bank_info", "id_user={}".format(__idUser), amount=str(__total))
	user.deleteElTable("curr_service", "curr_service IS NULL AND curr_time IS NULL")
	return redirect(url_for('indexer'))

@app.route('/about', methods=["POST"])
def about():
	return render_template("about.html", name=__nameUser, 
							login=__mailUser, b_date=__b_dateUser, 
							b_place=__b_placeUser, money=__total)

@app.route('/service', methods=["POST"])
def service():
	dictServ = []
	for i in (i for i in user.printEl("service")):
		if __total >= int(i[2]):
			helpDict = {}
			helpDict["id"] = int (i[0])
			helpDict["name"] = i[1]
			helpDict["cost"] = int(i[2])
			dictServ.append(helpDict)

	return render_template("service.html", name=__nameUser, login=__mailUser,
							 b_date=__b_dateUser, b_place=__b_placeUser, 
							 dict=dictServ, money=__total)


@app.route('/change', methods=["POST"])
def change():
	global __nameUser, __mailUser, __b_dateUser, __b_placeUser, __mailUser, __passwordUser, __idUser
	__nameUser = request.form.get("name")
	__mailUser = request.form.get("login")
	__b_dateUser = "Mon" + " " + dictMounth[request.form.get("mounth")] + " " + request.form.get("day") + " " + request.form.get("year") + " " + "21:04:37"
	__b_placeUser = request.form.get("ncity")
	__passwordUser = request.form.get("pass")
	user.updateElTable("data_login", "id_user="+str(__idUser), 
						email=addKav(__mailUser), password=addKav(__passwordUser))
	user.updateElTable("info_user", "id_user="+str(__idUser), 
						name=addKav(__nameUser), home_place=addKav(__b_placeUser), 
						b_date=addKav(__b_dateUser))
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