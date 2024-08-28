# ========== LIBRARIES ==========

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_session import Session
import pandas as pd
from datetime import timedelta, datetime, date
from dateutil.relativedelta import relativedelta
import sqlite3 as sql
from hashlib import sha256

# ========== APP PARAMETERS ==========
app = Flask(__name__)
app.config["SECRET_KEY"] = 'H0sp!taIB!ll!ngSyst3m'
app.config["SESSION_TYPE"] = 'filesystem'
DATABASE = 'docbill.sqlite3.db'
Session(app)

# ========== LOGIN / SESSION MANAGEMENT ==========

@app.before_request
def before_request():
	session.permanent = True
	app.permanent_session_lifetime = timedelta(minutes=10)

@app.route("/login")
def login():
	con = sql.connect(DATABASE)
	cur = con.cursor()
	loginlogo = cur.execute("SELECT logo FROM hospital ORDER BY id DESC").fetchone()[0]
	return render_template("login.html", loginlogo = loginlogo)

@app.route("/logout")
def logout():
	session.clear()
	flash('Logged out successfully.', 'info')
	return redirect(url_for("login"))

@app.route("/login", methods = ["POST"])
def post_login():
	username = request.form.get("username")
	password = request.form.get("password")
	password = sha256(password.encode('utf-8')).hexdigest()
	remember = True if request.form.get("remember") else False
	con = sql.connect(DATABASE)
	cur = con.cursor()
	cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
	if not cur.fetchall():
		flash('Wrong Username or Password. Try Again !!!', 'danger')
		return redirect(url_for("login"))
	session['logged_in'] = True
	flash("Welcome", 'success')
	return redirect(url_for("dashboard"))

@app.route("/", methods=["GET", "POST"])
def home():
	if ('logged_in' not in session) or (session['logged_in'] != True):
		return redirect(url_for("login"))
	return redirect(url_for('dashboard'))

# ========== SETUP ==========

# Route - Setup
@app.route("/setup")
@app.route("/hospital", methods=["GET", "POST"])
def hospital():
	if ('logged_in' not in session) or (session['logged_in'] != True):
		flash('Session timeout. Please login again', 'info')
		return redirect(url_for("login"))
	conn = sql.connect(DATABASE)
	cur = conn.cursor()
	hosp = cur.execute("SELECT * FROM hospital ORDER BY id DESC").fetchone()
	hdata = [hosp[1],hosp[2],hosp[3],hosp[4],hosp[5],hosp[6]]
	if request.method == "POST":
		hosp = request.form.to_dict()
		logo = request.files['logo']
		filename = logo.filename
		specs = ",".join(request.form.getlist('specs'))
		conn = sql.connect(DATABASE)
		cur = conn.cursor()
		logo.save("static/images/logo/"+filename)
		vals = (hosp['name'],filename,hosp['address'],hosp['phone'],hosp['email'],specs)
		cur.execute("INSERT INTO hospital (name,logo,address,phone,email,specs) VALUES (?,?,?,?,?,?)",(hosp['name'],filename,hosp['address'],hosp['phone'],hosp['email'],specs))
		conn.commit()
		return redirect(url_for('dashboard'))
	return render_template("hospital.html", hdata = hdata, title = 'Hospital')

# ========== DASHBOARD ==========

# Route - Dashboard
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
	if ('logged_in' not in session) or (session['logged_in'] != True):
		flash('Session timeout. Please login again', 'info')
		return redirect(url_for("login"))
	conn = sql.connect(DATABASE)
	cur = conn.cursor()
	ndocs = cur.execute("SELECT COUNT(docid) FROM doctors").fetchone()[0]
	npats = cur.execute("SELECT COUNT(patid) FROM patients").fetchone()[0]
	billtable = cur.execute("SELECT * FROM bills").fetchall()
	columns = [colname[0] for colname in cur.description]
	df = pd.DataFrame(billtable, columns = columns)
	end = date.today()
	start = end - relativedelta(days=180)
	if request.method == "POST":
		start = request.form['startdate']
		end = request.form['enddate']
	filterdf = df[(df.billdate >= str(start)) & (df.billdate <= str(end))]
	chartdf = filterdf.groupby('billdate').sum().reset_index()
	nbills = len(filterdf.index)
	income = chartdf.billtotal.sum()
	hosp = cur.execute("SELECT * FROM hospital ORDER BY id DESC").fetchone()
	hdata = [hosp[1],hosp[2],hosp[3],hosp[4],hosp[5],hosp[6]]
	return render_template("dashboard.html", dashdata = [income, nbills, npats, ndocs, start, end], chartdata = [list(chartdf.billdate), list(chartdf.billtotal)], hdata = hdata, title = 'Dashboard')

# ========== BILLS ==========

# Route - All Bills
@app.route("/bills", methods=["GET", "POST"])
def bills():
	if ('logged_in' not in session) or (session['logged_in'] != True):
		flash('Session timeout. Please login again', 'info')
		return redirect(url_for("login"))
	conn = sql.connect(DATABASE)
	conn.row_factory = sql.Row
	cur = conn.cursor()
	cur.execute("SELECT * FROM bills ORDER BY billdate DESC")
	content = cur.fetchall()
	mindate = cur.execute("SELECT billdate from bills ORDER BY billdate ASC").fetchone()[0]
	maxdate = cur.execute("SELECT billdate from bills ORDER BY billdate DESC").fetchone()[0]
	hosp = cur.execute("SELECT * FROM hospital ORDER BY id DESC").fetchone()
	hdata = [hosp['name'],hosp['logo'],hosp['address'],hosp['phone'],hosp['email'],hosp['specs']]
	return render_template("bills.html", bills = content, mindate = mindate, maxdate = maxdate, hdata = hdata, title = 'All Bills')

# Route - Add Bill
@app.route("/addbill", methods=["GET", "POST"])
def addbill():
	if ('logged_in' not in session) or (session['logged_in'] != True):
		flash('Session timeout. Please login again', 'info')
		return redirect(url_for("login"))
	conn = sql.connect(DATABASE)
	conn.row_factory = sql.Row
	cur = conn.cursor()
	nextbillid = datetime.now().strftime("%y%m%d%H%M")
	patients = cur.execute("SELECT patfullname, patid, patphone from patients").fetchall()
	doctors = cur.execute("SELECT docfullname FROM doctors").fetchall()
	hosp = cur.execute("SELECT * FROM hospital ORDER BY id DESC").fetchone()
	hdata = [hosp['name'],hosp['logo'],hosp['address'],hosp['phone'],hosp['email'],hosp['specs']]
	if request.method == "POST":
		content = request.form.to_dict()
		cur.execute("INSERT INTO bills ({}) VALUES ({})".format(','.join(content.keys()), ', '.join(['?']*len(content))), tuple(content.values()))
		conn.commit()
		flash('Bill Details Added Successfully', 'success')
		return redirect(url_for('addbill'))
	return render_template("addbill.html", nextbillid = nextbillid, doctors = doctors, patients = patients, hdata = hdata, title = 'Add Bill')

# Route - Edit Bill
@app.route("/editbill/<string:uid>", methods=["GET", "POST"])
def editbill(uid):
	if ('logged_in' not in session) or (session['logged_in'] != True):
		flash('Session timeout. Please login again', 'info')
		return redirect(url_for("login"))
	conn = sql.connect(DATABASE)
	cur = conn.cursor()
	doctors = cur.execute("SELECT docfullname FROM doctors").fetchall()
	patients = cur.execute("SELECT patfullname, patid, patphone from patients").fetchall()
	billdata = cur.execute("SELECT * FROM bills WHERE billnumber = ?", (uid,)).fetchone()
	hosp = cur.execute("SELECT * FROM hospital ORDER BY id DESC").fetchone()
	hdata = [hosp[1],hosp[2],hosp[3],hosp[4],hosp[5],hosp[6]]
	if request.method == "POST":
		content = request.form.to_dict()
		billno = content['billnumber']
		vals = list(content.values()).copy()
		keys = list(content.keys()).copy()
		keys.append('entrydate')
		date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		vals.extend([date,billno])
		cur.execute("UPDATE bills SET {}=? WHERE billnumber=?".format('=?,'.join(keys)), tuple(vals))
		conn.commit()
		flash('Bill# '+billno+' Details Updated Successfully', 'warning')
		return redirect(url_for('bills'))
	return render_template("editbill.html", doctors = doctors, patients = patients, billdata = billdata, hdata = hdata, title = 'Edit Bill')

# Route - View Bill
@app.route("/viewbill/<string:uid>", methods=["GET", "POST"])
def viewbill(uid):
	if ('logged_in' not in session) or (session['logged_in'] != True):
		flash('Session timeout. Please login again', 'info')
		return redirect(url_for("login"))
	conn = sql.connect(DATABASE)
	cur = conn.cursor()
	billdata = cur.execute("SELECT * FROM bills WHERE billnumber = ?", (uid,)).fetchone()
	hosp = cur.execute("SELECT * FROM hospital ORDER BY id DESC").fetchone()
	hdata = [hosp[1],hosp[2],hosp[3],hosp[4],hosp[5],hosp[6]]
	return render_template("viewbill.html", billdata = billdata, hdata = hdata, title = 'View Bill')

# Route - Delete Bill
@app.route("/deletebill/<string:uid>", methods=['GET', 'POST'])
def deletebill(uid):
	if ('logged_in' not in session) or (session['logged_in'] != True):
		flash('Session timeout. Please login again', 'info')
		return redirect(url_for("login"))
	con = sql.connect(DATABASE)
	cur = con.cursor()
	cur.execute("DELETE FROM bills WHERE billnumber = ?", (uid,))
	con.commit()
	flash('Bill# '+uid+' Deleted Successfully','danger')
	return redirect(url_for("bills"))

# ========== PATIENTS ==========

# Route - All Patients
@app.route("/patients", methods=["GET", "POST"])
def patients():
	if ('logged_in' not in session) or (session['logged_in'] != True):
		flash('Session timeout. Please login again', 'info')
		return redirect(url_for("login"))
	conn = sql.connect(DATABASE)
	conn.row_factory = sql.Row
	cur = conn.cursor()
	cur.execute("SELECT * FROM patients ORDER BY entrydate DESC")
	content = cur.fetchall()
	hosp = cur.execute("SELECT * FROM hospital ORDER BY id DESC").fetchone()
	hdata = [hosp['name'],hosp['logo'],hosp['address'],hosp['phone'],hosp['email'],hosp['specs']]
	return render_template("patients.html", patients = content, hdata = hdata, title = 'All Patients')

# Route - Add Patient
@app.route("/addpatient", methods=["GET", "POST"])
def addpatient():
	if ('logged_in' not in session) or (session['logged_in'] != True):
		flash('Session timeout. Please login again', 'info')
		return redirect(url_for("login"))
	conn = sql.connect(DATABASE)
	cur = conn.cursor()
	hosp = cur.execute("SELECT * FROM hospital ORDER BY id DESC").fetchone()
	hdata = [hosp[1],hosp[2],hosp[3],hosp[4],hosp[5],hosp[6]]
	lastsl = cur.execute("SELECT patsl FROM patients ORDER BY patsl DESC").fetchone()
	lastsl = 0 if lastsl == None else lastsl[0]
	nextpatid = str(datetime.now().strftime("%y%m%d"))+f"{lastsl+1:02}"
	if request.method == "POST":
		content = request.form.to_dict()
		cur.execute("INSERT INTO patients ({}) VALUES ({})".format(','.join(content.keys()), ', '.join(['?']*len(content))), tuple(content.values()))
		conn.commit()
		flash('Patient Details Added Successfully', 'success')
		return redirect(url_for('addpatient'))
	return render_template("addpatient.html", nextpatid = nextpatid, hdata = hdata, title = 'Add Patient')

# Route - Edit Patient
@app.route("/editpatient/<string:uid>", methods=["GET", "POST"])
def editpatient(uid):
	if ('logged_in' not in session) or (session['logged_in'] != True):
		flash('Session timeout. Please login again', 'info')
		return redirect(url_for("login"))
	conn = sql.connect(DATABASE)
	cur = conn.cursor()
	patdata = cur.execute("SELECT * FROM patients WHERE patid = ?", (uid,)).fetchone()
	hosp = cur.execute("SELECT * FROM hospital ORDER BY id DESC").fetchone()
	hdata = [hosp[1],hosp[2],hosp[3],hosp[4],hosp[5],hosp[6]]
	if request.method == "POST":
		content = request.form.to_dict()
		patno = content['patid']
		vals = list(content.values()).copy()
		keys = list(content.keys()).copy()
		keys.append('entrydate')
		date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		vals.extend([date,patno])
		cur.execute("UPDATE patients SET {}=? WHERE patid=?".format('=?,'.join(keys)), tuple(vals))
		conn.commit()
		flash('Patient# '+patno+' Details Updated Successfully', 'warning')
		return redirect(url_for('patients'))
	return render_template("editpatient.html", patdata = patdata, hdata = hdata, title = 'Edit Patient')

# Route - View Patient
@app.route("/viewpatient/<string:uid>", methods=["GET", "POST"])
def viewpatient(uid):
	if ('logged_in' not in session) or (session['logged_in'] != True):
		flash('Session timeout. Please login again', 'info')
		return redirect(url_for("login"))
	conn = sql.connect(DATABASE)
	cur = conn.cursor()
	patdata = cur.execute("SELECT * FROM patients WHERE patid = ?", (uid,)).fetchone()
	hosp = cur.execute("SELECT * FROM hospital ORDER BY id DESC").fetchone()
	hdata = [hosp[1],hosp[2],hosp[3],hosp[4],hosp[5],hosp[6]]
	return render_template("viewpatient.html", patdata = patdata, hdata = hdata, title = 'View Patient')

# Route - Delete Patient
@app.route("/deletepatient/<string:uid>", methods=['GET', 'POST'])
def deletepatient(uid):
	if ('logged_in' not in session) or (session['logged_in'] != True):
		flash('Session timeout. Please login again', 'info')
		return redirect(url_for("login"))
	con = sql.connect(DATABASE)
	cur = con.cursor()
	cur.execute("DELETE FROM patients WHERE patid = ?", (uid,))
	con.commit()
	flash('Patient# '+uid+' Deleted Successfully','danger')
	return redirect(url_for("patients"))

# ========== DOCTORS ==========

# Route - All Doctors
@app.route("/doctors", methods=["GET", "POST"])
def doctors():
	if ('logged_in' not in session) or (session['logged_in'] != True):
		flash('Session timeout. Please login again', 'info')
		return redirect(url_for("login"))
	conn = sql.connect(DATABASE)
	conn.row_factory = sql.Row
	cur = conn.cursor()
	content = cur.execute("SELECT * FROM doctors ORDER BY docsl").fetchall()
	hosp = cur.execute("SELECT * FROM hospital ORDER BY id DESC").fetchone()
	hdata = [hosp['name'],hosp['logo'],hosp['address'],hosp['phone'],hosp['email'],hosp['specs']]
	return render_template("doctors.html", doctors = content, hdata = hdata, title = 'All Doctors')

# Route - Add Doctor
@app.route("/adddoctor", methods=["GET", "POST"])
def adddoctor():
	if ('logged_in' not in session) or (session['logged_in'] != True):
		flash('Session timeout. Please login again', 'info')
		return redirect(url_for("login"))
	conn = sql.connect(DATABASE)
	conn.row_factory = sql.Row
	cur = conn.cursor()
	hosp = cur.execute("SELECT * FROM hospital ORDER BY id DESC").fetchone()
	hdata = [hosp['name'],hosp['logo'],hosp['address'],hosp['phone'],hosp['email'],hosp['specs']]
	specs = hosp['specs'].split(",")
	lastsl = cur.execute("SELECT docsl FROM doctors ORDER BY docsl DESC").fetchone()
	lastsl = 0 if lastsl == None else lastsl[0]
	nextdocid = f"{lastsl+1:02}"
	if request.method == "POST":
		content = request.form.to_dict()
		cur.execute("INSERT INTO doctors ({}) VALUES ({})".format(','.join(content.keys()), ', '.join(['?']*len(content))), tuple(content.values()))
		conn.commit()
		flash('Doctor Details Added Successfully', 'success')
		return redirect(url_for('adddoctor'))
	return render_template("adddoctor.html", nextdocid = nextdocid, specs = specs, hdata = hdata, title = 'Add Doctor')

# Route - Edit Doctor
@app.route("/editdoctor/<string:uid>", methods=["GET", "POST"])
def editdoctor(uid):
	if ('logged_in' not in session) or (session['logged_in'] != True):
		flash('Session timeout. Please login again', 'info')
		return redirect(url_for("login"))
	conn = sql.connect(DATABASE)
	cur = conn.cursor()
	hosp = cur.execute("SELECT * FROM hospital ORDER BY id DESC").fetchone()
	hdata = [hosp[1],hosp[2],hosp[3],hosp[4],hosp[5],hosp[6]]
	specs = hosp[6].split(",")
	docdata = cur.execute("SELECT * FROM doctors WHERE docid = ?", (uid,)).fetchone()
	if request.method == "POST":
		content = request.form.to_dict()
		docno = content['docid']
		vals = list(content.values()).copy()
		keys = list(content.keys()).copy()
		keys.append('entrydate')
		date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		vals.extend([date,docno])
		cur.execute("UPDATE doctors SET {}=? WHERE docid=?".format('=?,'.join(keys)), tuple(vals))
		conn.commit()
		flash('Doctor# '+docno+' Details Updated Successfully', 'warning')
		return redirect(url_for('doctors'))
	return render_template("editdoctor.html", specs = specs, docdata = docdata, hdata = hdata, title = 'Edit Doctor')

# Route - View Doctor
@app.route("/viewdoctor/<string:uid>", methods=["GET", "POST"])
def viewdoctor(uid):
	if ('logged_in' not in session) or (session['logged_in'] != True):
		flash('Session timeout. Please login again', 'info')
		return redirect(url_for("login"))
	conn = sql.connect(DATABASE)
	cur = conn.cursor()
	docdata = cur.execute("SELECT * FROM doctors WHERE docid = ?", (uid,)).fetchone()
	hosp = cur.execute("SELECT * FROM hospital ORDER BY id DESC").fetchone()
	hdata = [hosp[1],hosp[2],hosp[3],hosp[4],hosp[5],hosp[6]]
	return render_template("viewdoctor.html", docdata = docdata, hdata = hdata, title = 'View Doctor')

# Route - Delete Doctor
@app.route("/deletedoctor/<string:uid>", methods=["GET", "POST"])
def deletedoctor(uid):
	if ('logged_in' not in session) or (session['logged_in'] != True):
		flash('Session timeout. Please login again', 'info')
		return redirect(url_for("login"))
	con = sql.connect(DATABASE)
	cur = con.cursor()
	cur.execute("DELETE FROM doctors WHERE docid = ?", (uid,))
	con.commit()
	flash('Doctor# '+uid+' Deleted Successfully','danger')
	return redirect(url_for("doctors"))

# ========== APP RUN ==========

if __name__ == '__main__':
	app.run(debug = True, host='0.0.0.0')
