from flask import *
import json
from signup import manage_database
from signup import send_email

app = Flask(__name__)
mana_sql = manage_database.sql_manager("root", "Gzm20125")
@app.route("/signup", methods = ["GET", "POST"])
def signup():
	if request.method == "GET":
		return render_template("signup.html")
	elif request.method == "POST":
		email = request.form["email"]
		username = request.form["username"]
		password = request.form["password"]
		comfirmpassword = request.form["comfirmpassword"]
		print(username, password, comfirmpassword)
		if password != comfirmpassword:
			return jsonify(comfirmpassword = "password and comfirmpassword is not the same")

		check_r_user = mana_sql._search_r_user(email = email, username = username)
		if check_r_user != {}:
			return jsonify(warn = "these info have been signup and not been vertified, please go to email to vertify")
			

		check_user_email = mana_sql._search_user(email = email)
		check_user_username = mana_sql._search_user(username = username)
		if check_user_email != {}:
			return jsonify(email = "email have been signup")
		if check_user_username != {}:
			return jsonify(username = "username have been signup")		

		vertifycode = send_email.send_vertify_email(email)
		print("vertifycode", vertifycode)
		if mana_sql._insert_r_user(email, username, password, vertifycode) == 0:
			return jsonify(warn = "we have sent a message to your email, please go to your email and click the url in email to vertify your account")
		else:
			return jsonify(warn = "sign up failed")

@app.route("/vertify")
def vertify():
	vertifycode = request.args.get('vertifycode')
	result = mana_sql._search_r_user(vertifycode = vertifycode)
	print("result", result)
	print("emial", result["email"])
	print("username", result["username"])
	print("password", result["password"])
	if result != {}:
		if mana_sql._insert_user(email = result["email"], username = result["username"], password = result["password"]):
			session['username'] = result["username"]
			return redirect(url_for('detail', username = result["username"]))
		else:
			return "vertify err"	

@app.route("/login", methods = ["GET", "POST"])
def login():
	if request.method == "GET":
		return render_template("login.html")
	elif request.method == "POST":
		print("this is post")
		email = request.form["email"]
		password = request.form["password"]
		print("email:", email)
		print("password:", password)
		result = mana_sql._search_user(email = email)
		print(result)
		if result == {}:
			return jsonify(username = "no such a account!")
		elif result != {} and result["password"] != password:
			return jsonify(password = "password is wrong")
		elif result != {} and result["password"] == password:
			session['username'] = result["username"]
			return redirect(url_for('detail', username = result["username"]))


@app.route("/detail")
def detail():
	username = request.args.get('username')
	if "username" in session and username == session["username"]:
		email = mana_sql._search_user(username = username)["email"]
		return render_template("detail.html", email = email, username = username)
	abort(401)


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


if __name__ == "__main__":
	app.run(host = "0.0.0.0", port = 8888, debug = True)