from flask import *
from work_withBD import *

user = Control("main", "db_creator", "12345Q", "localhost", 5432)
app = Flask(__name__)
nameUser = ""
b_dateUser = ""
b_placeUser= ""
mailUser = ""
passwordUser = ""
idUser = 0

@app.route('/')
@app.route('/login')
def login():
	return render_template('reg.html')
	
@app.route('/validate', methods=["POST"])
def validate():
	if request.method == "POST":
		global nameUser, mailUser, b_dateUser, b_placeUser, mailUser, passwordUser, idUser
		mailUser = request.form.get("email")
		passwordUser = request.form.get("pass") 
		for i in (i for i in user.printEl("data_login")):
			if mailUser == i[0] and  passwordUser == i[1]:
				for j in (j for j in user.printEl("info_user")):
					idUser = i[2]
					nameUser = j[1]
					b_dateUser = j[3]
					b_placeUser= j[2]
					if j[0] == i[2]: return redirect(url_for('indexer'))
		abort(401)
	

@app.route('/account', methods=["POST"])
def account():
	return render_template("account.html", name=nameUser, login=mailUser,
							 b_date=b_dateUser, b_place=b_placeUser, password=passwordUser)

@app.route('/about', methods=["POST"])
def about():
	return render_template("about.html", name=nameUser, login=mailUser,
							 b_date=b_dateUser, b_place=b_placeUser)

@app.route('/service', methods=["POST"])
def service():
	dictServ = []
	for i in (i for i in user.printEl("service")):
		helpDict = {}
		helpDict["id"] = int (i[0])
		helpDict["name"] = i[1]
		helpDict["cost"] = int(i[2])
		dictServ.append(helpDict)
	return render_template("service.html", name=nameUser, login=mailUser,
							 b_date=b_dateUser, b_place=b_placeUser, dict=dictServ)

@app.route('/change', methods=["POST"])
def change():
	dictMounth = {"1": "Jan", "2": "Feb", "3":"Mar", "4":"Apr",
					"5": "May", "6": "Jun", "7": "Jul", "8":"Aug",
					"9": "Sep", "10": "Oct", "11":"Nov", "12":"Dec"}
	global nameUser, mailUser, b_dateUser, b_placeUser, mailUser, passwordUser, idUser
	nameUser = request.form.get("name")
	mailUser = request.form.get("login")
	b_dateUser = "Mon" + " " + dictMounth[request.form.get("mounth")] + " " + request.form.get("day") + " " + request.form.get("year") + " " + "21:04:37"
	b_placeUser = request.form.get("ncity")
	passwordUser = request.form.get("pass")
	user.updateElTable("data_login", "id_user="+str(idUser), email="'"+mailUser+"'", password="'"+passwordUser+"'")
	user.updateElTable("info_user", "id_user="+str(idUser), name="'"+nameUser+"'", home_place="'"+b_placeUser+"'", b_date="'"+b_dateUser+"'")
	return redirect(url_for('indexer'))


@app.route('/main')
def indexer():
	return render_template('index.html', name=nameUser, login=mailUser,
							 b_date=b_dateUser, b_place=b_placeUser)
	

if __name__ == '__main__':
	app.run(debug=True)