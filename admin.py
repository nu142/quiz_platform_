import sys
import mysql.connector
import streamlit as st
import subprocess

def establish_connection():
    # Establish connection to MySQL database
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "root",
        "database": "loginconn",
        "port": 3306,
    }

    connection = mysql.connector.connect(**db_config)
    return connection

def close_connection(connection):
    if connection.is_connected():
        connection.close()

class AdminPage:
    def __init__(self, username, admin_id):
        self.connection = establish_connection()
        self.cursor = self.connection.cursor(dictionary=True)
        self.username = username
        self.admin_id = admin_id
        self.authenticate_admin() 
        self.subject = None

    def authenticate_admin(self):
        query = "SELECT * FROM admin WHERE username = %s AND id = %s"
        self.cursor.execute(query, (self.username, self.admin_id))
        result = self.cursor.fetchone()

        if result and 'admin_name' in result:
            self.admin_name = result['admin_name']

    def select_subject(self):
        st.title("Select Subject")

        # Button to select 'mathematics'
        if st.button("mathematics"):
            self.load_questions("mathematics")

        # Button to select 'Python'
        if st.button("Python"):
            self.load_questions("python")

    def load_questions(self, subject):
        subprocess.run(["streamlit", "run", "questions.py", "username", str(self.username), "admin_id", str(self.admin_id),"subject",str(subject)])
        st.experimental_rerun()

def get_session_state():
    session_state = st.session_state
    if not hasattr(session_state, "admin"):
        session_state.admin = AdminPage("", 0)  # Default values, you may need to adjust
    return session_state

def main():
    # Retrieve username and admin_id from command-line arguments
    username_index = sys.argv.index("username") + 1
    admin_id_index = sys.argv.index("admin_id") + 1

    username = sys.argv[username_index]
    admin_id = int(sys.argv[admin_id_index])

    admin = AdminPage(username, admin_id)
    st.title("Admin Access")
    admin.authenticate_admin()
    admin.select_subject()

if __name__ == "__main__":
    main()
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("https://techcrunch.com/wp-content/uploads/2019/04/bulb-on-off1.gif?w=730&crop=1");
        background-position: left;
        backgroung-size:100%;
    }}
    </style>
    """,
    unsafe_allow_html=True
)