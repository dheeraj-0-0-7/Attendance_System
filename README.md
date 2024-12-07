# Student Attendance Management System

A comprehensive web application for marking, managing student attendance, and analyzing attendance statistics. Built with Flask, PostgreSQL, and HTML/CSS, this project integrates a facial recognition system to simplify attendance tracking while providing meaningful insights.

---

## Features

- **Facial Recognition Attendance**  
  Leverages facial recognition technology to mark student attendance efficiently and securely.

- **Student Dashboard**  
  Displays personal details and subject-wise attendance statistics.

- **Subject Details**  
  View detailed statistics for a specific subject, including total classes, present/absent counts, and attendance percentages.

- **Authentication**  
  Secure user login system with session-based authentication.

- **Responsive UI**  
  A user-friendly and mobile-responsive interface for ease of access.

---

## Technology Stack

- **Backend:** Flask (Python), SQLAlchemy  
- **Frontend:** HTML, CSS, JavaScript, Bootstrap  
- **Database:** PostgreSQL  
- **Facial Recognition:** OpenCV, Dlib  
- **Hosting/Deployment:** Flask built-in development server (or Docker if extended)

---

## Installation and Setup

1. Clone the repository:  
   ```bash
   git clone https://github.com/yourusername/student-attendance-management.git
   cd student-attendance-management
   ```

2. Set up a Python virtual environment:  
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

4. Install OpenCV and Dlib for facial recognition:  
   ```bash
   pip install opencv-python dlib
   ```

5. Configure the database:  
   - Create a PostgreSQL database named `attendance_management`.  
   - Update the `config.py` file with your database credentials.

6. Initialize the database:  
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

7. Run the application:  
   ```bash
   flask run
   ```

8. Access the application in your browser at `http://localhost:5000`.


---

## Usage

1. **Log in** using your assigned credentials.  
2. Navigate to your dashboard to view attendance statistics.  
3. Click on a subject to view detailed attendance reports.  
4. Upload image to mark attendance securely and efficiently.  
5. Log out securely when done.

---

## Folder Structure

```plaintext
student-attendance-management/
├── app/
│   ├── templates/         # HTML templates
│   ├── static/            # CSS, JS, and images
│   ├── routes/            # Application routes
│   ├── models.py          # Database models
│   ├── train_faces.py     # Facial recognition training
│   ├── mark_attendance.py # Facial recognition attendance marking
│   └── __init__.py        # App initialization
├── faces/                 # Stored images of students for facial recognition
├── migrations/            # Database migration files
├── config.py              # Application configuration
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgments

- Flask for the web framework.  
- PostgreSQL for database management.  
- OpenCV and Dlib for facial recognition technology.  
- Bootstrap for responsive UI components.

---

### Author

**Dheeraj Reddy Ravula**  
Feel free to connect on [LinkedIn](https://linkedin.com/in/dheeraj-reddy-ravula-5586271a3/) for queries or collaborations.
```

Save this content as `README.md` in the root directory of your project. Let me know if you need further adjustments!
