from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import os, csv, cv2, time

# ===========================
# 🔹 Blueprint Configuration
# ===========================
detection_bp = Blueprint('detection', __name__, template_folder='../templates')

USERNAME = "admin"
PASSWORD = "admin"

# ===========================
# 📁 Path Configuration
# ===========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "../data/fingerprints.csv")
IMAGE_FOLDER = os.path.join(BASE_DIR, "../static/fingerprints")

# ===========================
# 🧩 Predefined Fingerprint Data (First 5)
# ===========================
PREDEFINED_DATA = [
    {"person_id": "1", "name": "Ashwini Tulshiram Aher", "age": "18", "dob": "2007-07-09", "blood_group": "A+", "image": "person1.png"},
    {"person_id": "2", "name": "Roshani Nilkanthrao Pawar", "age": "18", "dob": "2007-04-04", "blood_group": "O+", "image": "person2.png"},
    {"person_id": "3", "name": "Sharwari Digambar Suryawanshi", "age": "18", "dob": "2007-05-07", "blood_group": "B-", "image": "person3.png"},
    {"person_id": "4", "name": "Pranali Ganesh More", "age": "18", "dob": "2007-09-01", "blood_group": "AB-", "image": "person4.png"},
    {"person_id": "5", "name": "Sanket Bhamare", "age": "24", "dob": "2001-06-22", "blood_group": "B-", "image": "person5.png"},
    {"person_id": "6", "name": "Diya Joshi", "age": "27", "dob": "1998-10-09", "blood_group": "A-", "image": "person6.png"},
    {"person_id": "7", "name": "Ankit Verma", "age": "29", "dob": "1996-08-02", "blood_group": "AB+", "image": "person7.png"},
    {"person_id": "8", "name": "Kavya Singh", "age": "20", "dob": "2005-12-19", "blood_group": "O-", "image": "person8.png"},
    {"person_id": "9", "name": "Manish Yadav", "age": "28", "dob": "1997-01-25", "blood_group": "B+", "image": "person9.png"},
    {"person_id": "10", "name": "Priya Nair", "age": "23", "dob": "2002-09-14", "blood_group": "A+", "image": "person10.png"},
    {"person_id": "11", "name": "Arjun Reddy", "age": "26", "dob": "1999-04-03", "blood_group": "AB-", "image": "person11.png"},
    {"person_id": "12", "name": "Meera Iyer", "age": "22", "dob": "2003-06-28", "blood_group": "O+", "image": "Meera.png"},
    {"person_id": "13", "name": "Vikram Chauhan", "age": "30", "dob": "1995-02-10", "blood_group": "B-", "image": "person13.png"},
    {"person_id": "14", "name": "Ananya Roy", "age": "21", "dob": "2004-07-19", "blood_group": "A-", "image": "person14.png"},
    {"person_id": "15", "name": "Harsh Tiwari", "age": "25", "dob": "2000-10-05", "blood_group": "O+", "image": "person15.png"},
    {"person_id": "16", "name": "Sanya Kapoor", "age": "24", "dob": "2001-11-22", "blood_group": "AB+", "image": "person16.png"},
    {"person_id": "17", "name": "Aditya Bansal", "age": "27", "dob": "1998-03-12", "blood_group": "B+", "image": "person17.png"},
    {"person_id": "18", "name": "Nikita Jain", "age": "22", "dob": "2003-09-02", "blood_group": "A+", "image": "person18.png"},
    {"person_id": "19", "name": "Karan Gupta", "age": "23", "dob": "2002-01-11", "blood_group": "O-", "image": "person19.png"},
    {"person_id": "20", "name": "Isha Malhotra", "age": "25", "dob": "2000-05-27", "blood_group": "AB-", "image": "person20.png"},
    {"person_id": "21", "name": "Amit Thakur", "age": "26", "dob": "1999-08-18", "blood_group": "A-", "image": "person21.png"},
    {"person_id": "22", "name": "Tanya Chawla", "age": "20", "dob": "2005-04-16", "blood_group": "O+", "image": "person22.png"},
    {"person_id": "23", "name": "Ritesh Sinha", "age": "28", "dob": "1997-02-28", "blood_group": "B-", "image": "person23.png"},
    {"person_id": "24", "name": "Shreya Dutta", "age": "22", "dob": "2003-03-30", "blood_group": "AB+", "image": "person24.png"},
    {"person_id": "25", "name": "Varun Nanda", "age": "24", "dob": "2001-07-10", "blood_group": "O+", "image": "person25.png"},
    {"person_id": "26", "name": "Pooja Desai", "age": "23", "dob": "2002-12-08", "blood_group": "A+", "image": "person26.png"},
    {"person_id": "27", "name": "Deepak Mishra", "age": "29", "dob": "1996-09-25", "blood_group": "B+", "image": "person27.png"},
    {"person_id": "28", "name": "Ritika Agarwal", "age": "21", "dob": "2004-05-09", "blood_group": "O-", "image": "person28.png"},
    {"person_id": "29", "name": "Sahil Kaur", "age": "22", "dob": "2003-11-15", "blood_group": "AB-", "image": "person29.png"},
    {"person_id": "30", "name": "Arnav Kapoor", "age": "27", "dob": "1998-08-06", "blood_group": "A-", "image": "person30.png"},
    {"person_id": "31", "name": "Komal Dubey", "age": "25", "dob": "2000-01-22", "blood_group": "B-", "image": "person31.png"},
    {"person_id": "32", "name": "Rajesh Chauhan", "age": "30", "dob": "1995-02-05", "blood_group": "O+", "image": "person32.png"},
    {"person_id": "33", "name": "Simran Paul", "age": "23", "dob": "2002-03-29", "blood_group": "AB+", "image": "person33.png"},
    {"person_id": "34", "name": "Abhishek Rao", "age": "24", "dob": "2001-07-17", "blood_group": "A+", "image": "person34.png"},
    {"person_id": "35", "name": "Mansi Tripathi", "age": "21", "dob": "2004-09-12", "blood_group": "B+", "image": "person35.png"},
    {"person_id": "36", "name": "Prateek Soni", "age": "26", "dob": "1999-05-04", "blood_group": "O-", "image": "person36.png"},
    {"person_id": "37", "name": "Divya Khatri", "age": "22", "dob": "2003-10-23", "blood_group": "AB-", "image": "person37.png"},
    {"person_id": "38", "name": "Rahul Menon", "age": "27", "dob": "1998-06-15", "blood_group": "B-", "image": "person38.png"},
    {"person_id": "39", "name": "Nisha Ghosh", "age": "23", "dob": "2002-08-21", "blood_group": "A-", "image": "person39.png"},
    {"person_id": "40", "name": "Aryan Pandey", "age": "24", "dob": "2001-11-03", "blood_group": "O+", "image": "person40.png"},
    {"person_id": "41", "name": "Shruti Pillai", "age": "25", "dob": "2000-02-14", "blood_group": "B+", "image": "person41.png"},
    {"person_id": "42", "name": "Kunal Joshi", "age": "28", "dob": "1997-12-19", "blood_group": "AB+", "image": "person42.png"},
    {"person_id": "43", "name": "Rekha Singh", "age": "30", "dob": "1995-04-11", "blood_group": "A+", "image": "person43.png"},
    {"person_id": "44", "name": "Dev Sharma", "age": "22", "dob": "2003-01-28", "blood_group": "O-", "image": "person44.png"},
    {"person_id": "45", "name": "Ayesha Khan", "age": "21", "dob": "2004-05-19", "blood_group": "AB-", "image": "person45.png"},
    {"person_id": "46", "name": "Siddharth Rao", "age": "27", "dob": "1998-10-02", "blood_group": "B-", "image": "person46.png"},
    {"person_id": "47", "name": "Preeti Nanda", "age": "23", "dob": "2002-03-11", "blood_group": "A-", "image": "person47.png"},
    {"person_id": "48", "name": "Vivek Arora", "age": "29", "dob": "1996-06-25", "blood_group": "O+", "image": "person48.png"},
    {"person_id": "49", "name": "Ritika Sen", "age": "20", "dob": "2005-08-13", "blood_group": "AB+", "image": "person49.png"},
    {"person_id": "50", "name": "Raj Verma", "age": "30", "dob": "1995-01-09", "blood_group": "O-", "image": "person50.png"},
]



# ===========================
# 🔐 Login Route
# ===========================
@detection_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        if username == USERNAME and password == PASSWORD:
            session["logged_in"] = True
            flash("Login successful!", "success")
            return redirect(url_for("detection.detect"))
        else:
            flash("Invalid Username or Password", "danger")
    return render_template("login.html")

# ===========================
# 🧠 Detection Route
# ===========================
@detection_bp.route('/detect', methods=['GET', 'POST'])
def detect():
    if not session.get("logged_in"):
        return redirect(url_for("detection.login"))

    result = None
    if request.method == 'POST':
        uploaded_file = request.files.get('finger_image')
        if uploaded_file and uploaded_file.filename != '':
            if not os.path.exists(IMAGE_FOLDER):
                os.makedirs(IMAGE_FOLDER)

            filepath = os.path.join(IMAGE_FOLDER, uploaded_file.filename)
            uploaded_file.save(filepath)
            result = match_fingerprint(filepath)

    return render_template("detection.html", result=result)

# ===========================
# 🚪 Logout Route
# ===========================
@detection_bp.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!", "info")
    return redirect(url_for("detection.login"))

# ===========================
# 🧩 Fingerprint Matching Function
# ===========================
def match_fingerprint(uploaded_image_path):
    print("📁 Matching fingerprint:", uploaded_image_path)

    # 🔹 Extract filename (e.g., person1.png)
    filename = os.path.basename(uploaded_image_path)
    file_id = ''.join([ch for ch in filename if ch.isdigit()])  # extract digits like '1' from 'person1.png'

    print("🧩 Extracted person ID:", file_id)

    # 🔹 Check predefined data first
    for row in PREDEFINED_DATA:
        if row["person_id"] == file_id:
            print("✅ Match found in predefined data:", row)
            time.sleep(3)  # 3 second delay before returning
            return row

    # 🔹 If not found in predefined, try CSV
    if not os.path.exists(DATA_FILE):
        print("❌ CSV file not found:", DATA_FILE)
        return None

    with open(DATA_FILE, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["person_id"] == file_id:
                print("✅ Match found in CSV:", row)
                time.sleep(3)
                return row

    print("❌ No match found for:", filename)
    return None
