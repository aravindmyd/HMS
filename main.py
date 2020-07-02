from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from datetime import datetime

now = datetime.now()
app = Flask(__name__)
# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'sdfasdfasdbasfbhadsbfjasdnfjasdufh asdkfn'
# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'testpassword'
app.config['MYSQL_DB'] = 'HMS'
# Initialize MySQL
mysql = MySQL(app)


# http://localhost:5000/login/ - this will be the login page, we need to use both GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        option = request.form['holder']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f'SELECT * FROM {option} WHERE username = %s AND password = %s', (username, password,))
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            cursor.execute(f"UPDATE {option} SET timestamp = '{str(date_time)}' WHERE id={account['id']} ")
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            if option == "admission":
                return render_template('admissionHomePage.html')
            elif option == "pharmacist":
                return render_template('pharmacistHomePage.html')
            elif option == "diagnostic":
                return "diagnostic"

        else:
            # Account doesnt exist or username/password incorrect
            flash(msg)
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)


@app.route("/admissionOption", methods=['GET', 'POST'])
def admission():
    if request.method == 'POST':
        optionData = request.form['admission']
        print(optionData)
        if optionData == 'Delete':
            return render_template('deletePatient.html')
        elif optionData == 'Create':
            return render_template('patientRegistration.html')
        elif optionData == "Update":
            return render_template('updatePatient.html')
        elif optionData == 'View':
            return render_template('viewPatient.html')
        elif optionData == 'Billing':
            return render_template('patientBilling.html')


@app.route("/patientRegistration", methods=['POST'])
def registerpatient():
    if request.method == "POST":
        ssnId = (request.form['ssnId'])
        patientName = (request.form['name'])
        patientAge = (request.form['age'])
        DOJ = (request.form['birthDate'])
        TOB = (request.form['typeOfBed'])
        address = (request.form['address'])
        state = (request.form['state'])
        city = (request.form['city'])
        status = "active"
        conn = mysql.connect
        cur = conn.cursor()
        cur.execute(
            f"Insert into patients(ssnId,patientName,patientAge,DOJ,TOB,address,city,state,status) values('{ssnId}','{patientName}','{patientAge}','{DOJ}','{TOB}','{address}','{city}','{state}','{status}');")
        # insert into patients(ssnId,patientName,patientAge,DOJ,TOB,address,city,state,status) values(4545,"naveen",45,45/05/1998,"semi","adsfasdfadsfadsf fadsfasd fasdf ","chennai","tamilcadu","active");
        conn.commit()
        flash("Inserted")
        return render_template('admissionHomePage.html')

    return "Registered"


@app.route('/getData', methods=['POST'])
def getData():
    if request.method == "POST":
        ssnId = request.form['ssnId']
        conn = mysql.connect
        cur = conn.cursor()
        cur.execute(f'select * from patients where ssnId = {ssnId}')
        patient = cur.fetchone()
        # (550, '123456789', 'AV', '22', '2019-10-30', 'Single room', 'Thiruvalluvar Nagar', 'Chennai', 'TamilNadu', 'active')
    return render_template('updatePatient.html', ssnId=patient[1], name=patient[2], age=patient[3], doj=patient[4],
                           tob=patient[5], address=patient[6])


@app.route('/putData/<ssnId>', methods=['POST'])
def putData(ssnId):
    print("In put data")
    if request.method == 'POST':
        patientName = (request.form['name'])
        patientAge = (request.form['age'])
        DOJ = (request.form['birthDate'])
        TOB = (request.form['typeOfBed'])
        address = (request.form['address'])
        state = (request.form['state'])
        city = (request.form['city'])
        conn = mysql.connect
        cur = conn.cursor()
        cur.execute(
            f"UPDATE patients SET patientName='{patientName}',patientAge='{patientAge}',DOJ='{DOJ}',TOB='{TOB}',address='{address}',city='{city}',state='{state}' where ssnId='{ssnId}'")
        conn.commit()
        flash("Updated Succesfully")
        return render_template('admissionHomePage.html')
    return "Updated"


@app.route('/deletePatient', methods=['POST'])
def deletePatient():
    if request.method == 'POST':
        ssnId = request.form['ssnId']
        conn = mysql.connect
        cur = conn.cursor()
        cur.execute(f'DELETE from patients where ssnId = {ssnId}')
        conn.commit()
        flash("Patient Record deleted Succesfully!")
    return render_template('admissionHomePage.html')


@app.route('/viewPatient', methods=['POST'])
def viewPatient():
    if request.method == 'POST':
        ssnId = request.form['ssnId']
        conn = mysql.connect
        cur = conn.cursor()
        cur.execute('select * from patients')
        patients = cur.fetchall()
        print(patients)
        modified_ls = []
        no_need = [0, 7, 8, 9]
        for i in patients:
            ls = []
            for j in range(len(i)):
                if j not in no_need:
                    ls.append(i[j])

            modified_ls.append(ls)
            print(modified_ls)
    return render_template('patientTable.html', data=modified_ls, leng=len(modified_ls))


@app.route('/admissionHome', methods=['POST'])
def admissionHome():
    return render_template('admissionHomePage.html')


@app.route('/billingPatient', methods=['POST'])
def billingPatient():
    if request.method == 'POST':
        ssnId = request.form['ssnId']
        conn = mysql.connect
        cur = conn.cursor()
        cur.execute(f'select * from patients where ssnId = {ssnId}')
        data = cur.fetchone()
        mod_data = []
        for i in range(len(data)):
            if i not in [0, 7, 8, 9]:
                mod_data.append(data[i])
        print(mod_data)
        return render_template("billingTable.html", pat_data=mod_data)
    return render_template('admissionHomePage.html')


@app.route('/payBill', methods=['POST'])
def payBill():
    return render_template('admissionHomePage.html')

#PHARMIST FUNCTIONS
@app.route("/pharmacistOption", methods=['GET', 'POST'])
def pharmacistOption():
    if request.method == 'POST':
        optionData = request.form['pharmacist']
        print(optionData)
        if optionData == 'IssueMedicine':
            return render_template('pharmacistIssue.html')
        elif optionData == 'GetPatientDetails':
            return render_template('pharmacistPatient.html')

@app.route('/pharmacistIssue',methods = ['POST'])
def pharmacistIssue():
    if request.method == 'POST':
        ssnId = request.form['ssnId']
        conn = mysql.connect
        cur = conn.cursor()
        cur.execute(f'select * from patients where ssnId = {ssnId}')
        patient_data = cur.fetchone()
        mod_data = []
        for i in range(len(patient_data)):
            if i not in [0, 7, 8, 9]:
                mod_data.append(patient_data[i])
        medicine_data = ["Paracetomol","100","Rs45","Rs4500"]
        return render_template('pharmaIssueTable.html',patient_data = mod_data,leng=len(mod_data),medicine_issued=medicine_data)
    return "Pharmacist Issue"

@app.route('/issueMedicine',methods = ['POST'])
def issueMedicine():
    conn = mysql.connect
    cur = conn.cursor()
    cur.execute(f'select medicineName from medicineMaster')
    medi = cur.fetchall()
    medicines = []
    for row in medi:
        medicines.append(row[0])
    print(medicines)
    return render_template('issueMedicine.html',medicines = medicines)
@app.route('/getQuantity',methods = ['POST'])
def getQuantity():
    if request.method == 'POST':
        qty = request.form['qty']
        medicine = request.form['srch']
        conn = mysql.connect
        cur = conn.cursor()
        print(medicine)
        cur.execute(f'select qty,medicineName from medicineMaster where medicineName = "{medicine}"')
        available_qty = cur.fetchone()[0]
        if qty<=available_qty:
           return render_template("")
    return "available"

if __name__ == '__main__':
    app.run(debug=True)
