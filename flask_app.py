from flask import *
from work_withBD import *

admin = Control("main", "db_creator", "12345Q", "localhost", 5432)
testUsl = [{"name": "Suspendisse", "cost": 3000},
			{"name": "Curabitur", "cost": 2500},
			{"name": "Consectetur", "cost": 1200},
			{"name": "Phasellus"  ,"cost": 7000},
			{"name": "Nullam", "cost": 1000}
			]


app = Flask(__name__)

@app.route('/')
@app.route('/login')
def login():
	return render_template('reg.html')
	
@app.route('/validate', methods=["POST"])
def validate():
	if request.method == "POST":
		global loginLog
		loginLog = request.form["email"]
		passwordLog = request.form["pass"] # Gavin_Wuckert77@gmail.com ,  47IIKTVQku9zdZf
		for i in (i for i in admin.printUsers("users")):
			if loginLog == i[1] and passwordLog == i[2]:
 				return redirect(url_for('indexer')) 
		abort(401)
	

@app.route('/account', methods=["POST"])
def account():
	if request.method == "POST":
		return render_template("account.html", name="Cristobal Conroy", login=loginLog,
							 b_date="Apr-25-1933", b_place="Dominica Enolachester 69010 Lubowitz Tunnel White Field Apt. 520")

@app.route('/about', methods=["POST"])
def about():
	if request.method == "POST":
		return render_template("about.html", name="Cristobal Conroy", login=loginLog,
							 b_date="Apr-25-1933", b_place="Dominica Enolachester 69010 Lubowitz Tunnel White Field Apt. 520")

@app.route('/service', methods=["POST"])
def service():
	if request.method == "POST":
		return render_template("service.html", name="Cristobal Conroy", login=loginLog,
							 b_date="Apr-25-1933", b_place="Dominica Enolachester 69010 Lubowitz Tunnel White Field Apt. 520", dict=testUsl)

@app.route('/main')
def indexer():
	return render_template('index.html', name="Cristobal Conroy", login=loginLog,
							 b_date="Apr-25-1933", b_place="Dominica Enolachester 69010 Lubowitz Tunnel White Field Apt. 520")
	


if __name__ == '__main__':
	app.run(debug=True)