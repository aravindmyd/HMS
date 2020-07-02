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
                return render_template('diagnosticHomePage.html')

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
        modified_ls = []
        no_need = [0, 7, 8, 9]
        for i in patients:
            ls = []
            for j in range(len(i)):
                if j not in no_need:
                    ls.append(i[j])

            modified_ls.append(ls)
    return render_template('patientTable.html', data=modified_ls, leng=len(modified_ls))


@app.route('/admissionHome', methods=['POST'])
def admissionHome():
    return render_template('admissionHomePage.html')

@app.route('/pharmacistHome', methods=['POST'])
def pharmacistHome():
    return render_template('pharmacistHomePage.html')

@app.route('/diagnosticHome', methods=['POST'])
def diagnosticHome():
    return render_template('diagnosticHomePage.html')
@app.route('/billingPatient', methods=['POST'])
def billingPatient():
    if request.method == 'POST':
        #PATIENT DATA
        ssnId = request.form['ssnId']
        conn = mysql.connect
        cur = conn.cursor()
        cur.execute(f'select * from patients where ssnId = {ssnId}')
        data = cur.fetchone()
        doj = data[4]
        tob = data[5]
        mod_data = []
        for i in range(len(data)):
            if i not in [0, 7, 8, 9]:
                mod_data.append(data[i])

        #MEDICINE DATA
        total_medicine_amount = 0
        cur.execute(f'select * from patients where ssnId = {ssnId}')
        patient_data = cur.fetchone()
        mod_data_med = []
        for i in range(len(patient_data)):
            if i not in [0, 7, 8, 9]:
                mod_data_med.append(patient_data[i])
        # medicine_data = ["Paracetomol","100","Rs45","Rs4500"]
        cur.execute(f'select * from medicinePatient where patientId = {ssnId}')
        pat = cur.fetchall()
        no_need = [0, 1]
        medicine_data_med = []
        for record in pat:
            ls = []
            for item in range(len(record)):
                if item not in no_need:
                    if item == 4:
                        ls.append(f"RS.{float(record[4]) / float(record[3])}")
                    ls.append(record[item])
            medicine_data_med.append(ls)
        for i in medicine_data_med:
            total_medicine_amount += float(i[3])
        #DIAGNOSTIC DATA
        total_diagnositc_amount = 0
        cur.execute(f'select * from patients where ssnId = {ssnId}')
        patient_data = cur.fetchone()
        mod_data_diag = []
        for i in range(len(patient_data)):
            if i not in [0, 7, 8, 9]:
                mod_data_diag.append(patient_data[i])
        cur.execute(f'select testName from diagnosticPatient where patientId = {ssnId}')
        pat = cur.fetchall()
        medicine_data = []
        for i in pat:
            cur.execute(f'select charge from diagnosticMaster where testName ="{i[0]}"')
            charge = cur.fetchone()
            medicine_data.append([i[0], charge[0]])
        for i in medicine_data:
            total_diagnositc_amount += float(i[1])
        #Calcuation for total charge

        #Calculation for total number of days
        import datetime
        data = doj.split('-')
        today = datetime.date.today()
        someday = datetime.date(int(data[0]), int(data[1]), int(data[2]))
        diff = someday - today
        total_days = abs(diff.days)
        total_days+=1
        #Calculation of rent
        room_rent = 0
        print(total_days)
        if tob== 'General ward':
            room_rent = total_days * 2000
        elif tob== 'Semi sharing':
            room_rent = total_days * 4000
        elif tob== 'Single Room':
            room_rent = total_days * 8000
        room_rent = abs(room_rent)
        print(room_rent,"room rent")
        print(total_medicine_amount,"pharmacy amount")
        print(total_diagnositc_amount,"diagnostic amount")
        total_charge = room_rent + total_diagnositc_amount + total_medicine_amount
        return render_template("billingTable.html", patient_data=mod_data,diagnostic_conducted=medicine_data,medicine_issued = medicine_data_med,total_charge = total_charge)


@app.route('/payBill', methods=['POST'])
def payBill():
    if request.method == 'POST':
        conn = mysql.connect
        cur = conn.cursor()
        ssnId = request.form['ssnId']
        cur.execute(f'update patients set status = "discharged" where ssnId={ssnId}')
        conn.commit()
        flash("Patient Discharged")
    return render_template('admissionHomePage.html')

#PHARMIST FUNCTIONS
@app.route("/pharmacistOption", methods=['GET', 'POST'])
def pharmacistOption():
    if request.method == 'POST':
        optionData = request.form['pharmacist']
        if optionData == 'IssueMedicine':
            return render_template('pharmacistIssue.html')
        elif optionData == 'GetPatientDetails':
            return render_template('getPatientDetails.html')

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
        #medicine_data = ["Paracetomol","100","Rs45","Rs4500"]
        cur.execute(f'select * from medicinePatient where patientId = {ssnId}')
        pat = cur.fetchall()
        no_need = [0, 1]
        medicine_data = []
        for record in pat:
            ls = []
            for item in range(len(record)):
                if item not in no_need:
                    if item == 4:
                        ls.append(f"RS.{float(record[4]) / float(record[3])}")
                    ls.append(record[item])
            medicine_data.append(ls)

        return render_template('pharmaIssueTable.html',patient_data = mod_data,leng=len(mod_data),medicine_issued=medicine_data)
    return "Pharmacist Issue"

@app.route('/issueMedicine',methods = ['POST'])
def issueMedicine():
    conn = mysql.connect
    cur = conn.cursor()
    patient_data = request.form['ssnId']
    cur.execute(f'select medicineName from medicineMaster')
    medi = cur.fetchall()
    medicines = []
    for row in medi:
        medicines.append(row[0])
    return render_template('issueMedicine.html',medicines = medicines,patient = patient_data)

@app.route('/getQuantity',methods = ['POST'])
def getQuantity():
    if request.method == 'POST':
        qty = request.form['qty']
        medicine = request.form['srch']
        ssnId = request.form['ssnId']
        conn = mysql.connect
        cur = conn.cursor()
        cur.execute(f'select qty,medicineName,medicineId,rate from medicineMaster where medicineName = "{medicine}"')
        data = cur.fetchone()
        available_qty,medicine_name,medicine_id,rate = data
        if qty<=available_qty:
            flash("Item added to Patient's db")
            #Reduce the qty in master file.
            cur.execute(f'update medicineMaster set qty = "{int(available_qty) - int(qty)}" where medicineName = "{medicine}"')
            conn.commit()
            #update the patient file.
            cur.execute(f'Insert into medicinePatient values({medicine_id},"{ssnId}","{medicine_name}","{qty}","{float(rate)*int(qty)}");')
            conn.commit()
            flash("Master DB and patient DB Updated")
        else:
            flash(f"No stock available. Only {available_qty} quantity available")
        return render_template('pharmacistHomePage.html')
@app.route('/getPatientDetails',methods = ['POST'])
def getPatientDetails():
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
        #medicine_data = ["Paracetomol","100","Rs45","Rs4500"]
        cur.execute(f'select * from medicinePatient where patientId = {ssnId}')
        pat = cur.fetchall()
        no_need = [0, 1]
        medicine_data = []
        for record in pat:
            ls = []
            for item in range(len(record)):
                if item not in no_need:
                    if item == 4:
                        ls.append(f"RS.{float(record[4]) / float(record[3])}")
                    ls.append(record[item])
            medicine_data.append(ls)
        return render_template('patientViewTable.html',patient_data = mod_data,leng=len(mod_data),medicine_issued=medicine_data)
    return "Pharmacist Issue"

# DIAGNOSTIC FUNCTIONS
@app.route("/diagnosticOption", methods=['GET', 'POST'])
def diagnosticOption():
    if request.method == 'POST':
        optionData = request.form['diagnostic']
        if optionData == 'Add Diagnostic':
            return render_template('diagnosticIssue.html')
        elif optionData == 'GetPatientDetails':
            return render_template('getDiagnosticDetails.html')

@app.route('/diagnosticIssue',methods = ['POST'])
def diagnosticIssue():
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
        #medicine_data = ["Paracetomol","100","Rs45","Rs4500"]
        cur.execute(f'select testName from diagnosticPatient where patientId = {ssnId}')
        pat = cur.fetchall()
        medicine_data = []
        for i in pat:
            cur.execute(f'select charge from diagnosticMaster where testName ="{i[0]}"')
            charge = cur.fetchone()
            medicine_data.append([i[0],charge[0]])
        return render_template('diagnosticIssueTable.html',patient_data = mod_data,diagnostic_conducted=medicine_data)
    return "Diagnostic Issue"

@app.route('/issueDiagnostic',methods = ['POST'])
def issueDiagnostic():
    conn = mysql.connect
    cur = conn.cursor()
    patient_data = request.form['ssnId']
    cur.execute(f'select testName from diagnosticMaster')
    medi = cur.fetchall()
    tests = []
    for row in medi:
        tests.append(row[0])
    return render_template('issueDiagnostic.html',tests = tests,patient = patient_data)

@app.route('/getDiagnostic',methods = ['POST'])
def getDiagnostic():
    if request.method == 'POST':
        testName = request.form['srch']
        ssnId = request.form['ssnId']
        conn = mysql.connect
        cur = conn.cursor()
        cur.execute(f'select testName,testId,charge from diagnosticMaster where testName = "{testName}"')
        data = cur.fetchone()
        test_name,test_id,charges = data
        #update the patient file.
        cur.execute(f'Insert into diagnosticPatient values({test_id},"{ssnId}","{test_name}");')
        conn.commit()
        flash("Master DB and patient DB Updated")
        return render_template('diagnosticHomePage.html')

@app.route('/getDiagnosticDetails',methods = ['POST'])
def getDiagnosticDetails():
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
        cur.execute(f'select testName from diagnosticPatient where patientId = {ssnId}')
        pat = cur.fetchall()
        medicine_data = []
        for i in pat:
            cur.execute(f'select charge from diagnosticMaster where testName ="{i[0]}"')
            charge = cur.fetchone()
            medicine_data.append([i[0],charge[0]])

        return render_template('diagnosticViewTable.html',patient_data = mod_data,leng=len(mod_data),diagnostic_conducted=medicine_data)
    return "Diagnostic Issue"

if __name__ == '__main__':
    app.run(debug=True)
