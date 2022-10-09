from flask import Flask,render_template,redirect,request,jsonify
from cryptography.fernet import Fernet
import json,sqlite3
app = Flask(__name__)
app.config['SECRET_KEY'] = "H-SyCHWobEf9pLs0nBpyEUbFNMnP7034jLmMM07SB1E"
# key
key=b'ajEUJHFsGFPs3TKMeaPad2nXZ9ibe7WSlxmHaM9D7BA='
f = Fernet(key)
csrf = 'null'
# home page
@app.route("/")
def home():
	conn = sqlite3.connect('db.db')
	con = conn.cursor()
	res = conn.execute("SELECT * FROM data")
	global csrf
	csrf = Fernet.generate_key().decode()
	print(csrf,"home")
	return render_template("index.html",data=res,f=f,csrf=csrf)

#password generated
@app.route("/password")
def password():
	password = Fernet.generate_key()
	print(csrf,"password")
	return jsonify({"password":str(password)[5:-6]})

#save password
@app.route("/data",methods=['GET','POST'])
def save_password():
	if(request.method =='POST'):
		password = json.loads(request.data.decode())['password']
		name = json.loads(request.data.decode())['name']
		csrf_token = json.loads(request.data.decode())['csrf']
		print(csrf,"save")
		print(csrf_token,"::",csrf)
		if(csrf_token== csrf):
			conn = sqlite3.connect('db.db')
			con = conn.cursor()
			try:
				conn.execute("CREATE TABLE if not exists data(sno integer primary key,name text not null,password text not null,browser text not null) ")
				res = conn.execute(f"select * from data where name='{name}' or password='{password}' ")
				if(res.fetchall()):
					con.close()
					return jsonify({"return":"Already Data EXIST"})
				else:
					password = f.encrypt(password.encode()).decode()
					conn.execute(f"""INSERT INTO data(name,password,browser) values('{name}',"{password}",'{request.user_agent}') """)
					conn.commit()
					con.close()
					return jsonify({'return':"Successfully Save"})
			except Exception as error:
				con.close()
				return jsonify({'return':error})
		else:
			return jsonify({"return":"CSRF_Token Invalid"})
		

# delete 

if(__name__ == "__main__"):
	app.run(debug=True)