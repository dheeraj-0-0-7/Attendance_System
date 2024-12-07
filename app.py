from flask import Flask, render_template, request, session, flash, redirect, url_for
from datetime import timedelta, datetime
import logging
import psycopg2, os, cv2, face_recognition

app = Flask(__name__)
app.secret_key = "thisissecretkey"
app.permanent_session_lifetime = timedelta(minutes=15)

url = 'postgresql://postgres.wfndeugctludkryndzme:dbforstudentsattendance@aws-0-us-east-1.pooler.supabase.com:6543/postgres'
conn = psycopg2.connect(url)
 

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods = ["POST","GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        cur = conn.cursor()
        cur.execute('''SELECT student_id,"password" FROM "Registrations" WHERE username = %s''', (username,))
        user_details = cur.fetchone()  
        if user_details:
            student_id,db_password = user_details 
            if(db_password == password):
                   session["user"] = username
                   return redirect(url_for("user",id=student_id))
            else:
                flash("Incorrect password.")
                return redirect(url_for("login"))
        else:
            flash("Username not found.")
            return redirect(url_for("login"))
    else:
        if "user" in session:
            return redirect(url_for("user"))        
        return render_template("login.html")
    
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/register", methods = ["POST","GET"])
def register():
    if request.method == "POST":
        id = request.form["student-id"]
        name = request.form["full-name"]
        username = request.form["username"]
        password = request.form["password"]
        dob = request.form["dob"]
        course = request.form["course-id"]
        cur = conn.cursor()
        cur.execute('''INSERT INTO "Registrations" 
                    (created_at, student_id, "Name", username, "password", date_of_birth, course_id) 
                    VALUES(now(), %s, %s, %s, %s, %s, %s)''',
                    (id, name, username, password, dob, course))
        conn.commit()
        return redirect({url_for("user")})
    else:
        return render_template("register.html")

@app.route("/student/id=<id>", methods = ["POST","GET"])
def user(id):
    if "user" in session:
        cur = conn.cursor()
        cur.execute('''SELECT s.name , s.student_id,s2."name" as subject, e.subject_id, p.name as professor
                        FROM public."Enrollment" e
                        left join public."Student" s on e.student_id = s.student_id 
                        left join public."Subjects" s2 on s2.subject_id = e.subject_id 
                        left join public."Professors" p on p.professor_id = e.professor_id 
                        where e.student_id = %s''', (id,))
        student_info = cur.fetchall()
        cur.close()
        return render_template("user.html", student_enrollment_info= student_info)
    else:
        return redirect(url_for("login"))
    
@app.route("/student/id=<id>/subject/<subject_id>", methods=["GET", "POST"])
def subject(id, subject_id):
    if "user" in session:
        cur = conn.cursor()
        cur.execute('''SELECT s.name, s.student_id, s2."name" as subject, e.subject_id, p.name as professor,
                            COUNT(a.status) AS total_classes,
                            COUNT(CASE WHEN a.status = 'Present' THEN 1 END) AS total_present,
                            COUNT(CASE WHEN a.status = 'Absent' THEN 1 END) AS total_absent,
                            ROUND(
                                (COUNT(CASE WHEN a.status = 'Present' THEN 1 END)::decimal / NULLIF(COUNT(a.status), 0)) * 100, 
                                2
                            ) AS attendance_percentage
                        FROM public."Enrollment" e
                        LEFT JOIN public."Student" s ON e.student_id = s.student_id 
                        LEFT JOIN public."Subjects" s2 ON s2.subject_id = e.subject_id 
                        LEFT JOIN public."Professors" p ON p.professor_id = e.professor_id
                        LEFT JOIN public."attendance" a ON e.student_id = a.student_id AND e.subject_id = a.subject_id 
                        WHERE e.student_id = %s AND s2.subject_id = %s
                        GROUP BY s.name, s.student_id, s2.name, e.subject_id, p.name''', (id, subject_id))
        subject_info = cur.fetchone()
        cur.close()
        return render_template("subject.html", student_subject_info=subject_info)
    else:
        return redirect(url_for("login"))

@app.route("/student/id=<id>/subject/<subject_id>/upload_image", methods=["POST"])
def upload_image(id, subject_id):
    if "user" in session:
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM public."attendance"
            WHERE student_id = %s AND subject_id = %s AND attendance_date = %s''',(id,subject_id,datetime.today().date()))
        existing_attendance = cursor.fetchone()
        cursor.close()

        if existing_attendance:
            flash('Attendance has already been marked for today.', 'error')
            return redirect(url_for('subject_page', id=id, subject_id=subject_id))
        else:
            cur = conn.cursor()
            cur.execute('''SELECT professor_id
                            FROM public."Enrollment" 
                            where student_id =%s and subject_id = %s''', (id,subject_id))
            prof_id = cur.fetchone()
            if 'professor-image' not in request.files:
                flash('No file uploaded')
                return redirect(request.url)
            file = request.files['professor-image']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file:
                current_date = datetime.now().strftime("%m%d%Y")
                new_filename = f"student_{id}_subject_{subject_id}_professor_{prof_id[0]}_{current_date}.jpg"
                file.save(os.path.join('images/students', new_filename))

                uploaded_image = face_recognition.load_image_file(f'images/students/{new_filename}')
                reference_image_path = f'images/employees/professor_{prof_id[0]}_{current_date}.jpg'
                reference_image = face_recognition.load_image_file(reference_image_path)

                # Detect faces and compute face encodings
                uploaded_face_encodings = face_recognition.face_encodings(uploaded_image)
                reference_face_encodings = face_recognition.face_encodings(reference_image)

                if len(uploaded_face_encodings) > 0 and len(reference_face_encodings) > 0:
                    uploaded_face_encoding = uploaded_face_encodings[0]
                    reference_face_encoding = reference_face_encodings[0]

                    # Compare faces
                    match_results = face_recognition.compare_faces([reference_face_encoding], uploaded_face_encoding)

                    if match_results[0]:
                        attendance_status = 'Present'
                        cur.execute('''INSERT INTO Attendance (student_id, subject_id, attendance_date, status)
                            VALUES (%s, %s, CURRENT_DATE, %s)''',
                            (id, subject_id, attendance_status))
                        flash('Attendance marked successfully!', 'success')
                        conn.commit()
                        cur.close()
                    else:
                        flash('Image does not match. Please try again.','error')
                else:
                    flash('No face detected in the image. Please try again.','error') 
        return subject(id, subject_id)
    else:
        return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True, port=8000)