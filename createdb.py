import sqlite3 as sql
from hashlib import sha256

# Connect to SQLite or create a new SQLite DB if not exists
con = sql.connect('docbill.sqlite3.db')

# Create a connection
cur = con.cursor()

# Drop 'hospital' table if already exsists
cur.execute("DROP TABLE IF EXISTS hospital")

# Create 'hospital' table
hospital = '''CREATE TABLE hospital (
	"id" INTEGER PRIMARY KEY AUTOINCREMENT,
	"name"	TEXT,
	"logo"	TEXT,
	"address"	TEXT,
	"phone"	TEXT,
	"email" TEXT,
	"specs" TEXT )'''
cur.execute(hospital)

# Drop 'users' table if already exsists
cur.execute("DROP TABLE IF EXISTS users")

# Create 'users' table
users = '''CREATE TABLE users (
	"userid"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"username"	TEXT,
	"password"	TEXT )'''
cur.execute(users)

# Drop 'doctors' table if already exsists
cur.execute("DROP TABLE IF EXISTS doctors")

# Create 'doctors' table
doctors = '''CREATE TABLE doctors (
	"docsl"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"docid"	TEXT,
	"docfullname"	TEXT,
	"docdob"	TEXT,
	"docgender"	TEXT,
	"docemail"	TEXT,
	"docphone"	TEXT,
	"docqual"	TEXT,
	"docexp"	TEXT,
	"docspec"	TEXT,
	"docaltphone"	TEXT,
	"docaddress"	TEXT,
	"entrydate" DATETIME DEFAULT (DATETIME('now', 'localtime')) )'''
con.execute(doctors)

# Drop 'patients' table if already exsists
cur.execute("DROP TABLE IF EXISTS patients")

# Create 'patients' table
patients = '''CREATE TABLE patients (
	"patsl" INTEGER PRIMARY KEY AUTOINCREMENT,
	"patid"	TEXT,
	"patfullname"	TEXT,
	"patdob"	TEXT,
	"patgender"	TEXT,
	"patemail"	TEXT,
	"patphone"	TEXT,
	"pataddress"	TEXT,
	"pataltcontact"	TEXT,
	"patrelation"	TEXT,
	"entrydate" DATETIME DEFAULT (DATETIME('now', 'localtime')) )'''
con.execute(patients)

# Drop 'bills' table if already exsists
cur.execute("DROP TABLE IF EXISTS bills")

# Create 'bills' table
bills = '''CREATE TABLE bills (
	"billsl" INTEGER PRIMARY KEY AUTOINCREMENT,
	"billnumber"	TEXT,
	"billdate"	TEXT,
	"billdoctor"	TEXT,
	"billpatdetails"	TEXT,
	"billitem1"	TEXT,
	"billqty1"	INTEGER,
	"billitemrate1"	INTEGER,
	"billitemtotal1"	INTEGER,
	"billitem2"	TEXT,
	"billqty2"	INTEGER,
	"billitemrate2"	INTEGER,
	"billitemtotal2"	INTEGER,
	"billitem3"	TEXT,
	"billqty3"	INTEGER,
	"billitemrate3"	INTEGER,
	"billitemtotal3"	INTEGER,
	"billtotal"	INTEGER,
	"billstatus"	TEXT,
	"billmode"	TEXT,
	"entrydate" DATETIME DEFAULT (DATETIME('now', 'localtime')) )'''
con.execute(bills)

# Add hospital details
# addhospital = '''INSERT INTO hospital (id,name,logo,address,phone,email,specs) VALUES
#				('1','My Hospital','/static/images/logo.png','Address 1, Address 2, Address 3, State, Pincode','+91-900099009','hospital@docbill.com','Pulmonology,Gynecology,General Medicine')'''
# cur.execute(addhospital)

# Create one user
cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",('clinic', sha256('clinic'.encode('utf-8')).hexdigest()))


# Add dummy doctors
adddoctors = '''INSERT INTO doctors (docsl,docid,docfullname,docdob,docgender,docemail,docphone,docqual,docexp,docspec,docaltphone,docaddress) VALUES
				('1','D01','Dr. Sailesh','1990-04-03','Male','sailesh@doc.com','9090909090','MD, MBBS','15 Years','Pulmonology','9990099900','Haryana'),
				('2','D02','Dr. Kiran','1993-08-01','Female','kiran@doc.com','9900990099','MS, MBBS','10 Years','Gynecology','9009009009','Rajasthan'),
				('3','D03','Dr. Kumar','1996-10-05','Male','kumar@doc.com','9099099090','DNB, MBBS','8 Years','General Medicine','9090090090','Telangana')'''
cur.execute(adddoctors)

# Add dummy patients
addpatients = '''INSERT INTO patients (patsl,patid,patfullname,patdob,patgender,patemail,patphone,pataddress,pataltcontact,patrelation) VALUES
				('1','P24020101','Dhruv Choudhury','1980-01-01','Male','pat1@doc.com','9079190914','Haryana','9188989169','Wife'),
				('2','P24030506','Aarav Mistry','1982-02-02','Male','pat2@doc.com','9039064515','Rajasthan','9075945698','Brother'),
				('3','P24041002','Raina Malhotra','1983-04-03','Female','pat3@doc.com','9527443335','Punjab','9847894538','Husband'),
				('4','P24051112','Rajveer Patel','1985-01-04','Male','pat4@doc.com','9383743007','Gujarat','9224256310','Father'),
				('5','P24062203','Yuvraj Kumar','1989-06-05','Male','pat5@doc.com','9725204431','Delhi','9691753219','Son'),
				('6','P24071112','Varun Ghosh','1984-08-06','Male','pat6@doc.com','9249168072','West Bengal','9559490363','Wife'),
				('7','P24081601','Shilpa Kaushik','1986-10-07','Female','pat7@doc.com','9528129122','Uttar Pradesh','9777398365','Husband'),
				('8','P24092811','Sumitra Lakshman','1987-12-08','Female','pat8@doc.com','9339213552','Tamil Nadu','9443657022','Sister'),
				('9','P24101104','Hemant Mishra','1981-05-09','Male','pat9@doc.com','9940491231','Madhya Pradesh','9342103232','Daughter'),
				('10','P24113008','Divya Kumari','1988-11-10','Female','pat10@doc.com','9777930924','Andhra Pradesh','9756361631','Son')'''
cur.execute(addpatients)

# Add dummy bills
addbills = '''INSERT INTO bills (billsl,billnumber,billdate,billdoctor,billpatdetails,billitem1,billqty1,billitemrate1,billitemtotal1,billitem2,billqty2,billitemrate2,billitemtotal2,billitem3,billqty3,billitemrate3,billitemtotal3,billtotal,billstatus,billmode) VALUES 
			('1','INV2310131352','2023-10-13','Dr. Sailesh','Name: Dhruv Choudhury | ID: P24020101 | Phone: 9079190914','Consultation','1','350','350','','','','','','','','','350','Paid','Cash'),
			('2','INV2404041329','2024-04-04','Dr. Kiran','Name: Aarav Mistry | ID: P24030506 | Phone: 9039064515','Injection','1','250','250','','','','','','','','','250','Paid','UPI'),
			('3','INV2407170939','2024-07-17','Dr. Kumar','Name: Raina Malhotra | ID: P24041002 | Phone: 9527443335','Procedure','1','500','500','','','','','','','','','500','Paid','Card'),
			('4','INV2404021645','2024-04-02','Dr. Sailesh','Name: Rajveer Patel | ID: P24051112 | Phone: 9383743007','Consultation','1','350','350','','','','','','','','','350','Paid','UPI'),
			('5','INV2304071616','2023-04-07','Dr. Kiran','Name: Yuvraj Kumar | ID: P24062203 | Phone: 9725204431','Injection','1','250','250','','','','','','','','','250','Paid','Cash'),
			('6','INV2407031541','2024-07-03','Dr. Kumar','Name: Varun Ghosh | ID: P24071112 | Phone: 9249168072','Procedure','1','500','500','','','','','','','','','500','Paid','Cash'),
			('7','INV2308180913','2023-08-18','Dr. Sailesh','Name: Shilpa Kaushik | ID: P24081601 | Phone: 9528129122','Consultation','1','350','350','','','','','','','','','350','Paid','Card'),
			('8','INV2402010909','2024-02-01','Dr. Kiran','Name: Sumitra Lakshman | ID: P24092811 | Phone: 9339213552','Injection','1','250','250','','','','','','','','','250','Paid','UPI'),
			('9','INV2308030916','2023-08-03','Dr. Kumar','Name: Hemant Mishra | ID: P24101104 | Phone: 9940491231','Procedure','1','500','500','','','','','','','','','500','Paid','Cash'),
			('10','INV2309301216','2023-09-30','Dr. Sailesh','Name: Divya Kumari | ID: P24113008 | Phone: 9777930924','Consultation','1','350','350','','','','','','','','','350','Paid','UPI'),
			('11','INV2404141517','2024-04-14','Dr. Kiran','Name: Dhruv Choudhury | ID: P24020101 | Phone: 9079190914','Injection','1','250','250','','','','','','','','','250','Paid','Card'),
			('12','INV2303061144','2023-03-06','Dr. Kumar','Name: Aarav Mistry | ID: P24030506 | Phone: 9039064515','Procedure','1','500','500','','','','','','','','','500','Paid','UPI'),
			('13','INV2406190925','2024-06-19','Dr. Sailesh','Name: Raina Malhotra | ID: P24041002 | Phone: 9527443335','Consultation','1','350','350','','','','','','','','','350','Paid','Cash'),
			('14','INV2311141352','2023-11-14','Dr. Kiran','Name: Rajveer Patel | ID: P24051112 | Phone: 9383743007','Injection','1','250','250','','','','','','','','','250','Paid','Cash'),
			('15','INV2405151231','2024-05-15','Dr. Kumar','Name: Yuvraj Kumar | ID: P24062203 | Phone: 9725204431','Procedure','1','500','500','','','','','','','','','500','Paid','Card'),
			('16','INV2308070946','2023-08-07','Dr. Sailesh','Name: Varun Ghosh | ID: P24071112 | Phone: 9249168072','Consultation','1','350','350','','','','','','','','','350','Paid','UPI'),
			('17','INV2306141009','2023-06-14','Dr. Kiran','Name: Shilpa Kaushik | ID: P24081601 | Phone: 9528129122','Injection','1','250','250','','','','','','','','','250','Paid','Cash'),
			('18','INV2401011649','2024-01-01','Dr. Kumar','Name: Sumitra Lakshman | ID: P24092811 | Phone: 9339213552','Procedure','1','500','500','','','','','','','','','500','Paid','UPI'),
			('19','INV2405301659','2024-05-30','Dr. Sailesh','Name: Hemant Mishra | ID: P24101104 | Phone: 9940491231','Consultation','1','350','350','','','','','','','','','350','Paid','Card'),
			('20','INV2304291327','2023-04-29','Dr. Kiran','Name: Divya Kumari | ID: P24113008 | Phone: 9777930924','Injection','1','250','250','','','','','','','','','250','Paid','UPI'),
			('21','INV2305091419','2023-05-09','Dr. Kumar','Name: Dhruv Choudhury | ID: P24020101 | Phone: 9079190914','Procedure','1','500','500','','','','','','','','','500','Paid','Cash'),
			('22','INV2311240910','2023-11-24','Dr. Sailesh','Name: Aarav Mistry | ID: P24030506 | Phone: 9039064515','Consultation','1','350','350','','','','','','','','','350','Paid','Cash'),
			('23','INV2407141439','2024-07-14','Dr. Kiran','Name: Raina Malhotra | ID: P24041002 | Phone: 9527443335','Injection','1','250','250','','','','','','','','','250','Paid','Card'),
			('24','INV2303131205','2023-03-13','Dr. Kumar','Name: Rajveer Patel | ID: P24051112 | Phone: 9383743007','Procedure','1','500','500','','','','','','','','','500','Paid','UPI'),
			('25','INV2307281022','2023-07-28','Dr. Sailesh','Name: Yuvraj Kumar | ID: P24062203 | Phone: 9725204431','Consultation','1','350','350','','','','','','','','','350','Paid','Cash'),
			('26','INV2403071609','2024-03-07','Dr. Kiran','Name: Varun Ghosh | ID: P24071112 | Phone: 9249168072','Injection','1','250','250','','','','','','','','','250','Paid','UPI'),
			('27','INV2303281513','2023-03-28','Dr. Kumar','Name: Shilpa Kaushik | ID: P24081601 | Phone: 9528129122','Procedure','1','500','500','','','','','','','','','500','Paid','Card'),
			('28','INV2302141114','2023-02-14','Dr. Sailesh','Name: Sumitra Lakshman | ID: P24092811 | Phone: 9339213552','Consultation','1','350','350','','','','','','','','','350','Paid','UPI'),
			('29','INV2403061337','2024-03-06','Dr. Kiran','Name: Hemant Mishra | ID: P24101104 | Phone: 9940491231','Injection','1','250','250','','','','','','','','','250','Paid','Cash'),
			('30','INV2406180925','2024-06-18','Dr. Kumar','Name: Divya Kumari | ID: P24113008 | Phone: 9777930924','Procedure','1','500','500','','','','','','','','','500','Paid','Cash'),
			('31','INV2404281057','2024-04-28','Dr. Sailesh','Name: Dhruv Choudhury | ID: P24020101 | Phone: 9079190914','Consultation','1','350','350','','','','','','','','','350','Paid','Card'),
			('32','INV2307161432','2023-07-16','Dr. Kiran','Name: Aarav Mistry | ID: P24030506 | Phone: 9039064515','Injection','1','250','250','','','','','','','','','250','Paid','UPI'),
			('33','INV2305101537','2023-05-10','Dr. Kumar','Name: Raina Malhotra | ID: P24041002 | Phone: 9527443335','Procedure','1','500','500','','','','','','','','','500','Paid','Cash'),
			('34','INV2304281206','2023-04-28','Dr. Sailesh','Name: Rajveer Patel | ID: P24051112 | Phone: 9383743007','Consultation','1','350','350','','','','','','','','','350','Paid','UPI'),
			('35','INV2312241240','2023-12-24','Dr. Kiran','Name: Yuvraj Kumar | ID: P24062203 | Phone: 9725204431','Injection','1','250','250','','','','','','','','','250','Paid','Card'),
			('36','INV2407091413','2024-07-09','Dr. Kumar','Name: Varun Ghosh | ID: P24071112 | Phone: 9249168072','Procedure','1','500','500','','','','','','','','','500','Paid','UPI'),
			('37','INV2402020909','2024-02-02','Dr. Sailesh','Name: Shilpa Kaushik | ID: P24081601 | Phone: 9528129122','Consultation','1','350','350','','','','','','','','','350','Paid','Cash'),
			('38','INV2308210926','2023-08-21','Dr. Kiran','Name: Sumitra Lakshman | ID: P24092811 | Phone: 9339213552','Injection','1','250','250','','','','','','','','','250','Paid','Cash'),
			('39','INV2304090951','2023-04-09','Dr. Kumar','Name: Hemant Mishra | ID: P24101104 | Phone: 9940491231','Procedure','1','500','500','','','','','','','','','500','Paid','Card'),
			('40','INV2303311609','2023-03-31','Dr. Sailesh','Name: Divya Kumari | ID: P24113008 | Phone: 9777930924','Consultation','1','350','350','','','','','','','','','350','Paid','UPI'),
			('41','INV2310100936','2023-10-10','Dr. Kiran','Name: Dhruv Choudhury | ID: P24020101 | Phone: 9079190914','Injection','1','250','250','','','','','','','','','250','Paid','Cash'),
			('42','INV2306221152','2023-06-22','Dr. Kumar','Name: Aarav Mistry | ID: P24030506 | Phone: 9039064515','Procedure','1','500','500','','','','','','','','','500','Paid','UPI'),
			('43','INV2310090912','2023-10-09','Dr. Sailesh','Name: Raina Malhotra | ID: P24041002 | Phone: 9527443335','Consultation','1','350','350','','','','','','','','','350','Paid','Card'),
			('44','INV2308111423','2023-08-11','Dr. Kiran','Name: Rajveer Patel | ID: P24051112 | Phone: 9383743007','Injection','1','250','250','','','','','','','','','250','Paid','UPI'),
			('45','INV2302271250','2023-02-27','Dr. Kumar','Name: Yuvraj Kumar | ID: P24062203 | Phone: 9725204431','Procedure','1','500','500','','','','','','','','','500','Paid','Cash'),
			('46','INV2407111037','2024-07-11','Dr. Sailesh','Name: Varun Ghosh | ID: P24071112 | Phone: 9249168072','Consultation','1','350','350','','','','','','','','','350','Paid','Cash'),
			('47','INV2402281227','2024-02-28','Dr. Kiran','Name: Shilpa Kaushik | ID: P24081601 | Phone: 9528129122','Injection','1','250','250','','','','','','','','','250','Paid','Card'),
			('48','INV2311121428','2023-11-12','Dr. Kumar','Name: Sumitra Lakshman | ID: P24092811 | Phone: 9339213552','Procedure','1','500','500','','','','','','','','','500','Paid','UPI'),
			('49','INV2307161549','2023-07-16','Dr. Sailesh','Name: Hemant Mishra | ID: P24101104 | Phone: 9940491231','Consultation','1','350','350','','','','','','','','','350','Paid','Cash'),
			('50','INV2402271657','2024-02-27','Dr. Kiran','Name: Divya Kumari | ID: P24113008 | Phone: 9777930924','Injection','1','250','250','','','','','','','','','250','Paid','UPI'),
			('51','INV2308151559','2023-08-15','Dr. Kumar','Name: Dhruv Choudhury | ID: P24020101 | Phone: 9079190914','Procedure','1','500','500','','','','','','','','','500','Paid','Card'),
			('52','INV2312181156','2023-12-18','Dr. Sailesh','Name: Aarav Mistry | ID: P24030506 | Phone: 9039064515','Consultation','1','350','350','','','','','','','','','350','Paid','UPI'),
			('53','INV2309091037','2023-09-09','Dr. Kiran','Name: Raina Malhotra | ID: P24041002 | Phone: 9527443335','Injection','1','250','250','','','','','','','','','250','Paid','Cash'),
			('54','INV2305311619','2023-05-31','Dr. Kumar','Name: Rajveer Patel | ID: P24051112 | Phone: 9383743007','Procedure','1','500','500','','','','','','','','','500','Paid','Cash'),
			('55','INV2401311123','2024-01-31','Dr. Sailesh','Name: Yuvraj Kumar | ID: P24062203 | Phone: 9725204431','Consultation','1','350','350','','','','','','','','','350','Paid','Card'),
			('56','INV2306071110','2023-06-07','Dr. Kiran','Name: Varun Ghosh | ID: P24071112 | Phone: 9249168072','Injection','1','250','250','','','','','','','','','250','Paid','UPI'),
			('57','INV2403071247','2024-03-07','Dr. Kumar','Name: Shilpa Kaushik | ID: P24081601 | Phone: 9528129122','Procedure','1','500','500','','','','','','','','','500','Paid','Cash'),
			('58','INV2401221141','2024-01-22','Dr. Sailesh','Name: Sumitra Lakshman | ID: P24092811 | Phone: 9339213552','Consultation','1','350','350','','','','','','','','','350','Paid','UPI'),
			('59','INV2404211558','2024-04-21','Dr. Kiran','Name: Hemant Mishra | ID: P24101104 | Phone: 9940491231','Injection','1','250','250','','','','','','','','','250','Paid','Card'),
			('60','INV2405241515','2024-05-24','Dr. Kumar','Name: Divya Kumari | ID: P24113008 | Phone: 9777930924','Procedure','1','500','500','','','','','','','','','500','Paid','UPI'),
			('61','INV2309111058','2023-09-11','Dr. Sailesh','Name: Dhruv Choudhury | ID: P24020101 | Phone: 9079190914','Consultation','1','350','350','','','','','','','','','350','Paid','Cash'),
			('62','INV2307151035','2023-07-15','Dr. Kiran','Name: Aarav Mistry | ID: P24030506 | Phone: 9039064515','Injection','1','250','250','','','','','','','','','250','Paid','Cash'),
			('63','INV2405311115','2024-05-31','Dr. Kumar','Name: Raina Malhotra | ID: P24041002 | Phone: 9527443335','Procedure','1','500','500','','','','','','','','','500','Paid','Card'),
			('64','INV2307151640','2023-07-15','Dr. Sailesh','Name: Rajveer Patel | ID: P24051112 | Phone: 9383743007','Consultation','1','350','350','','','','','','','','','350','Paid','UPI'),
			('65','INV2311161153','2023-11-16','Dr. Kiran','Name: Yuvraj Kumar | ID: P24062203 | Phone: 9725204431','Injection','1','250','250','','','','','','','','','250','Paid','Cash'),
			('66','INV2308041624','2023-08-04','Dr. Kumar','Name: Varun Ghosh | ID: P24071112 | Phone: 9249168072','Procedure','1','500','500','','','','','','','','','500','Paid','UPI'),
			('67','INV2312081250','2023-12-08','Dr. Sailesh','Name: Shilpa Kaushik | ID: P24081601 | Phone: 9528129122','Consultation','1','350','350','','','','','','','','','350','Paid','Card'),
			('68','INV2307091338','2023-07-09','Dr. Kiran','Name: Sumitra Lakshman | ID: P24092811 | Phone: 9339213552','Injection','1','250','250','','','','','','','','','250','Paid','UPI'),
			('69','INV2304261316','2023-04-26','Dr. Kumar','Name: Hemant Mishra | ID: P24101104 | Phone: 9940491231','Procedure','1','500','500','','','','','','','','','500','Paid','Cash'),
			('70','INV2307151628','2023-07-15','Dr. Sailesh','Name: Divya Kumari | ID: P24113008 | Phone: 9777930924','Consultation','1','350','350','','','','','','','','','350','Paid','Cash'),
			('71','INV2404091629','2024-04-09','Dr. Kiran','Name: Dhruv Choudhury | ID: P24020101 | Phone: 9079190914','Injection','1','250','250','','','','','','','','','250','Paid','Card'),
			('72','INV2406270913','2024-06-27','Dr. Kumar','Name: Aarav Mistry | ID: P24030506 | Phone: 9039064515','Procedure','1','500','500','','','','','','','','','500','Paid','UPI'),
			('73','INV2308071322','2023-08-07','Dr. Sailesh','Name: Raina Malhotra | ID: P24041002 | Phone: 9527443335','Consultation','1','350','350','','','','','','','','','350','Paid','Cash'),
			('74','INV2307201057','2023-07-20','Dr. Kiran','Name: Rajveer Patel | ID: P24051112 | Phone: 9383743007','Injection','1','250','250','','','','','','','','','250','Paid','UPI'),
			('75','INV2402101135','2024-02-10','Dr. Kumar','Name: Yuvraj Kumar | ID: P24062203 | Phone: 9725204431','Procedure','1','500','500','','','','','','','','','500','Paid','Card'),
			('76','INV2311211449','2023-11-21','Dr. Sailesh','Name: Varun Ghosh | ID: P24071112 | Phone: 9249168072','Consultation','1','350','350','','','','','','','','','350','Paid','UPI'),
			('77','INV2302121009','2023-02-12','Dr. Kiran','Name: Shilpa Kaushik | ID: P24081601 | Phone: 9528129122','Injection','1','250','250','','','','','','','','','250','Paid','Cash'),
			('78','INV2304191616','2023-04-19','Dr. Kumar','Name: Sumitra Lakshman | ID: P24092811 | Phone: 9339213552','Procedure','1','500','500','','','','','','','','','500','Paid','Cash'),
			('79','INV2406050933','2024-06-05','Dr. Sailesh','Name: Hemant Mishra | ID: P24101104 | Phone: 9940491231','Consultation','1','350','350','','','','','','','','','350','Paid','Card'),
			('80','INV2401051337','2024-01-05','Dr. Kiran','Name: Divya Kumari | ID: P24113008 | Phone: 9777930924','Injection','1','250','250','','','','','','','','','250','Paid','UPI'),
			('81','INV2309031059','2023-09-03','Dr. Kumar','Name: Dhruv Choudhury | ID: P24020101 | Phone: 9079190914','Procedure','1','500','500','','','','','','','','','500','Paid','Cash'),
			('82','INV2308171646','2023-08-17','Dr. Sailesh','Name: Aarav Mistry | ID: P24030506 | Phone: 9039064515','Consultation','1','350','350','','','','','','','','','350','Paid','UPI'),
			('83','INV2405270904','2024-05-27','Dr. Kiran','Name: Raina Malhotra | ID: P24041002 | Phone: 9527443335','Injection','1','250','250','','','','','','','','','250','Paid','Card'),
			('84','INV2401221117','2024-01-22','Dr. Kumar','Name: Rajveer Patel | ID: P24051112 | Phone: 9383743007','Procedure','1','500','500','','','','','','','','','500','Paid','UPI'),
			('85','INV2309181437','2023-09-18','Dr. Sailesh','Name: Yuvraj Kumar | ID: P24062203 | Phone: 9725204431','Consultation','1','350','350','','','','','','','','','350','Paid','Cash'),
			('86','INV2406211246','2024-06-21','Dr. Kiran','Name: Varun Ghosh | ID: P24071112 | Phone: 9249168072','Injection','1','250','250','','','','','','','','','250','Paid','Cash'),
			('87','INV2407121032','2024-07-12','Dr. Kumar','Name: Shilpa Kaushik | ID: P24081601 | Phone: 9528129122','Procedure','1','500','500','','','','','','','','','500','Paid','Card'),
			('88','INV2304201225','2023-04-20','Dr. Sailesh','Name: Sumitra Lakshman | ID: P24092811 | Phone: 9339213552','Consultation','1','350','350','','','','','','','','','350','Paid','UPI'),
			('89','INV2306061149','2023-06-06','Dr. Kiran','Name: Hemant Mishra | ID: P24101104 | Phone: 9940491231','Injection','1','250','250','','','','','','','','','250','Paid','Cash'),
			('90','INV2405081152','2024-05-08','Dr. Kumar','Name: Divya Kumari | ID: P24113008 | Phone: 9777930924','Procedure','1','500','500','','','','','','','','','500','Paid','UPI'),
			('91','INV2306041247','2023-06-04','Dr. Sailesh','Name: Dhruv Choudhury | ID: P24020101 | Phone: 9079190914','Consultation','1','350','350','','','','','','','','','350','Paid','Card'),
			('92','INV2304241112','2023-04-24','Dr. Kiran','Name: Aarav Mistry | ID: P24030506 | Phone: 9039064515','Injection','1','250','250','','','','','','','','','250','Paid','UPI'),
			('93','INV2403121234','2024-03-12','Dr. Kumar','Name: Raina Malhotra | ID: P24041002 | Phone: 9527443335','Procedure','1','500','500','','','','','','','','','500','Paid','Cash'),
			('94','INV2310311245','2023-10-31','Dr. Sailesh','Name: Rajveer Patel | ID: P24051112 | Phone: 9383743007','Consultation','1','350','350','','','','','','','','','350','Paid','Cash'),
			('95','INV2405061122','2024-05-06','Dr. Kiran','Name: Yuvraj Kumar | ID: P24062203 | Phone: 9725204431','Injection','1','250','250','','','','','','','','','250','Paid','Card'),
			('96','INV2310191112','2023-10-19','Dr. Kumar','Name: Varun Ghosh | ID: P24071112 | Phone: 9249168072','Procedure','1','500','500','','','','','','','','','500','Paid','UPI'),
			('97','INV2305291504','2023-05-29','Dr. Sailesh','Name: Shilpa Kaushik | ID: P24081601 | Phone: 9528129122','Consultation','1','350','350','','','','','','','','','350','Paid','Cash'),
			('98','INV2308191425','2023-08-19','Dr. Kiran','Name: Sumitra Lakshman | ID: P24092811 | Phone: 9339213552','Injection','1','250','250','','','','','','','','','250','Paid','UPI'),
			('99','INV2307201536','2023-07-20','Dr. Kumar','Name: Hemant Mishra | ID: P24101104 | Phone: 9940491231','Procedure','1','500','500','','','','','','','','','500','Paid','Card'),
			('100','INV2302211632','2023-02-21','Dr. Sailesh','Name: Divya Kumari | ID: P24113008 | Phone: 9777930924','Consultation','1','350','350','','','','','','','','','350','Paid','UPI'),
			('101','INV2311130900','2023-11-13','Dr. Kiran','Name: Dhruv Choudhury | ID: P24020101 | Phone: 9079190914','Injection','1','250','250','','','','','','','','','250','Paid','Cash'),
			('102','INV2311011432','2023-11-01','Dr. Kumar','Name: Aarav Mistry | ID: P24030506 | Phone: 9039064515','Procedure','1','500','500','','','','','','','','','500','Paid','Cash'),
			('103','INV2303031046','2023-03-03','Dr. Sailesh','Name: Raina Malhotra | ID: P24041002 | Phone: 9527443335','Consultation','1','350','350','','','','','','','','','350','Paid','Card'),
			('104','INV2301190949','2023-01-19','Dr. Kiran','Name: Rajveer Patel | ID: P24051112 | Phone: 9383743007','Injection','1','250','250','','','','','','','','','250','Paid','UPI'),
			('105','INV2403261336','2024-03-26','Dr. Kumar','Name: Yuvraj Kumar | ID: P24062203 | Phone: 9725204431','Procedure','1','500','500','','','','','','','','','500','Paid','Cash'),
			('106','INV2301201112','2023-01-20','Dr. Sailesh','Name: Varun Ghosh | ID: P24071112 | Phone: 9249168072','Consultation','1','350','350','','','','','','','','','350','Paid','UPI'),
			('107','INV2308031445','2023-08-03','Dr. Kiran','Name: Shilpa Kaushik | ID: P24081601 | Phone: 9528129122','Injection','1','250','250','','','','','','','','','250','Paid','Card'),
			('108','INV2303221403','2023-03-22','Dr. Kumar','Name: Sumitra Lakshman | ID: P24092811 | Phone: 9339213552','Procedure','1','500','500','','','','','','','','','500','Paid','UPI'),
			('109','INV2304051627','2023-04-05','Dr. Sailesh','Name: Hemant Mishra | ID: P24101104 | Phone: 9940491231','Consultation','1','350','350','','','','','','','','','350','Paid','Cash'),
			('110','INV2310101124','2023-10-10','Dr. Kiran','Name: Divya Kumari | ID: P24113008 | Phone: 9777930924','Injection','1','250','250','','','','','','','','','250','Paid','Cash'),
			('111','INV2312310929','2023-12-31','Dr. Kumar','Name: Dhruv Choudhury | ID: P24020101 | Phone: 9079190914','Procedure','1','500','500','','','','','','','','','500','Paid','Card'),
			('112','INV2404151314','2024-04-15','Dr. Sailesh','Name: Aarav Mistry | ID: P24030506 | Phone: 9039064515','Consultation','1','350','350','','','','','','','','','350','Paid','UPI'),
			('113','INV2407101651','2024-07-10','Dr. Kiran','Name: Raina Malhotra | ID: P24041002 | Phone: 9527443335','Injection','1','250','250','','','','','','','','','250','Paid','Cash'),
			('114','INV2312041342','2023-12-04','Dr. Kumar','Name: Rajveer Patel | ID: P24051112 | Phone: 9383743007','Procedure','1','500','500','','','','','','','','','500','Paid','UPI'),
			('115','INV2311141247','2023-11-14','Dr. Sailesh','Name: Yuvraj Kumar | ID: P24062203 | Phone: 9725204431','Consultation','1','350','350','','','','','','','','','350','Paid','Card'),
			('116','INV2312221110','2023-12-22','Dr. Kiran','Name: Varun Ghosh | ID: P24071112 | Phone: 9249168072','Injection','1','250','250','','','','','','','','','250','Paid','UPI'),
			('117','INV2310061055','2023-10-06','Dr. Kumar','Name: Shilpa Kaushik | ID: P24081601 | Phone: 9528129122','Procedure','1','500','500','','','','','','','','','500','Paid','Cash'),
			('118','INV2405301404','2024-05-30','Dr. Sailesh','Name: Sumitra Lakshman | ID: P24092811 | Phone: 9339213552','Consultation','1','350','350','','','','','','','','','350','Paid','Cash'),
			('119','INV2407201617','2024-07-20','Dr. Kiran','Name: Hemant Mishra | ID: P24101104 | Phone: 9940491231','Injection','1','250','250','','','','','','','','','250','Paid','Card'),
			('120','INV2310141209','2023-10-14','Dr. Kumar','Name: Divya Kumari | ID: P24113008 | Phone: 9777930924','Procedure','1','500','500','','','','','','','','','500','Paid','UPI'),
			('121','INV2303221514','2023-03-22','Dr. Sailesh','Name: Dhruv Choudhury | ID: P24020101 | Phone: 9079190914','Consultation','1','350','350','','','','','','','','','350','Paid','Cash'),
			('122','INV2301181147','2023-01-18','Dr. Kiran','Name: Aarav Mistry | ID: P24030506 | Phone: 9039064515','Injection','1','250','250','','','','','','','','','250','Paid','UPI'),
			('123','INV2404300930','2024-04-30','Dr. Kumar','Name: Raina Malhotra | ID: P24041002 | Phone: 9527443335','Procedure','1','500','500','','','','','','','','','500','Paid','Card'),
			('124','INV2308081223','2023-08-08','Dr. Sailesh','Name: Rajveer Patel | ID: P24051112 | Phone: 9383743007','Consultation','1','350','350','','','','','','','','','350','Paid','UPI'),
			('125','INV2304041108','2023-04-04','Dr. Kiran','Name: Yuvraj Kumar | ID: P24062203 | Phone: 9725204431','Injection','1','250','250','','','','','','','','','250','Paid','Cash'),
			('126','INV2308121053','2023-08-12','Dr. Kumar','Name: Varun Ghosh | ID: P24071112 | Phone: 9249168072','Procedure','1','500','500','','','','','','','','','500','Paid','Cash'),
			('127','INV2307061205','2023-07-06','Dr. Sailesh','Name: Shilpa Kaushik | ID: P24081601 | Phone: 9528129122','Consultation','1','350','350','','','','','','','','','350','Paid','Card'),
			('128','INV2304061607','2023-04-06','Dr. Kiran','Name: Sumitra Lakshman | ID: P24092811 | Phone: 9339213552','Injection','1','250','250','','','','','','','','','250','Paid','UPI'),
			('129','INV2306271105','2023-06-27','Dr. Kumar','Name: Hemant Mishra | ID: P24101104 | Phone: 9940491231','Procedure','1','500','500','','','','','','','','','500','Paid','Cash'),
			('130','INV2306191042','2023-06-19','Dr. Sailesh','Name: Divya Kumari | ID: P24113008 | Phone: 9777930924','Consultation','1','350','350','','','','','','','','','350','Paid','UPI'),
			('131','INV2305061542','2023-05-06','Dr. Kiran','Name: Dhruv Choudhury | ID: P24020101 | Phone: 9079190914','Injection','1','250','250','','','','','','','','','250','Paid','Card'),
			('132','INV2311041141','2023-11-04','Dr. Kumar','Name: Aarav Mistry | ID: P24030506 | Phone: 9039064515','Procedure','1','500','500','','','','','','','','','500','Paid','UPI'),
			('133','INV2304261552','2023-04-26','Dr. Sailesh','Name: Raina Malhotra | ID: P24041002 | Phone: 9527443335','Consultation','1','350','350','','','','','','','','','350','Paid','Cash'),
			('134','INV2401201543','2024-01-20','Dr. Kiran','Name: Rajveer Patel | ID: P24051112 | Phone: 9383743007','Injection','1','250','250','','','','','','','','','250','Paid','Cash'),
			('135','INV2303131336','2023-03-13','Dr. Kumar','Name: Yuvraj Kumar | ID: P24062203 | Phone: 9725204431','Procedure','1','500','500','','','','','','','','','500','Paid','Card'),
			('136','INV2404101430','2024-04-10','Dr. Sailesh','Name: Varun Ghosh | ID: P24071112 | Phone: 9249168072','Consultation','1','350','350','','','','','','','','','350','Paid','UPI'),
			('137','INV2306031156','2023-06-03','Dr. Kiran','Name: Shilpa Kaushik | ID: P24081601 | Phone: 9528129122','Injection','1','250','250','','','','','','','','','250','Paid','Cash'),
			('138','INV2310121646','2023-10-12','Dr. Kumar','Name: Sumitra Lakshman | ID: P24092811 | Phone: 9339213552','Procedure','1','500','500','','','','','','','','','500','Paid','UPI'),
			('139','INV2301271510','2023-01-27','Dr. Sailesh','Name: Hemant Mishra | ID: P24101104 | Phone: 9940491231','Consultation','1','350','350','','','','','','','','','350','Paid','Card'),
			('140','INV2407191119','2024-07-19','Dr. Kiran','Name: Divya Kumari | ID: P24113008 | Phone: 9777930924','Injection','1','250','250','','','','','','','','','250','Paid','UPI'),
			('141','INV2405271251','2024-05-27','Dr. Kumar','Name: Dhruv Choudhury | ID: P24020101 | Phone: 9079190914','Procedure','1','500','500','','','','','','','','','500','Paid','Cash'),
			('142','INV2305281005','2023-05-28','Dr. Sailesh','Name: Aarav Mistry | ID: P24030506 | Phone: 9039064515','Consultation','1','350','350','','','','','','','','','350','Paid','Cash'),
			('143','INV2302081436','2023-02-08','Dr. Kiran','Name: Raina Malhotra | ID: P24041002 | Phone: 9527443335','Injection','1','250','250','','','','','','','','','250','Paid','Card'),
			('144','INV2312041613','2023-12-04','Dr. Kumar','Name: Rajveer Patel | ID: P24051112 | Phone: 9383743007','Procedure','1','500','500','','','','','','','','','500','Paid','UPI'),
			('145','INV2405140906','2024-05-14','Dr. Sailesh','Name: Yuvraj Kumar | ID: P24062203 | Phone: 9725204431','Consultation','1','350','350','','','','','','','','','350','Paid','Cash'),
			('146','INV2407101417','2024-07-10','Dr. Kiran','Name: Varun Ghosh | ID: P24071112 | Phone: 9249168072','Injection','1','250','250','','','','','','','','','250','Paid','UPI'),
			('147','INV2301101320','2023-01-10','Dr. Kumar','Name: Shilpa Kaushik | ID: P24081601 | Phone: 9528129122','Procedure','1','500','500','','','','','','','','','500','Paid','Card'),
			('148','INV2406151442','2024-06-15','Dr. Sailesh','Name: Sumitra Lakshman | ID: P24092811 | Phone: 9339213552','Consultation','1','350','350','','','','','','','','','350','Paid','UPI'),
			('149','INV2305061402','2023-05-06','Dr. Kiran','Name: Hemant Mishra | ID: P24101104 | Phone: 9940491231','Injection','1','250','250','','','','','','','','','250','Paid','Cash'),
			('150','INV2407311519','2024-07-31','Dr. Kumar','Name: Divya Kumari | ID: P24113008 | Phone: 9777930924','Procedure','1','500','500','','','','','','','','','500','Paid','Cash')'''
cur.execute(addbills)

#commit changes
con.commit()

#close the connection
con.close()