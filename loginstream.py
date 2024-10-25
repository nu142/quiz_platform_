import streamlit as st
import mysql.connector
import re
import subprocess

class LoginPage:

    def __init__(self):
        self.admin_id = None
        self.user_id =None
        self.username = None
        self.urname = None
        self.admin_name = None

    def display_login(self):
        st.title("Login Page")
        self.username = st.text_input("Username:")
        self.password = st.text_input("Password:", type="password")
        self.login_type = st.radio("Login as:", ["User", "Admin"])

        login_button = st.button("Login")
        if login_button:
            self.login()

    def validate_password(self):
        if not re.search(r'[a-z]', self.password):
            st.error("Password must contain at least one lowercase letter.")
            return False
        if not re.search(r'[A-Z]', self.password):
            st.error("Password must contain at least one uppercase letter.")
            return False     
        if not re.search(r'\d', self.password):
            st.error("Password must contain at least one digit.")
            return False
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', self.password):
            st.error("Password must contain at least one special character.")
            return False
        if len(self.password) < 8:
            st.error("Password must be at least 8 characters long.")
            return False
        return True
    
    def load_admin_page(self):
        subprocess.run(["streamlit", "run", "admin.py", "username", self.username, "admin_id", str(self.admin_id)])
        st.experimental_rerun()

    def load_user_page(self):
        subprocess.run(["streamlit", "run", "usdemo.py", "username", self.username, "user_id", str(self.user_id)])
        st.experimental_rerun()

    def login(self):
        username = self.username
        password = self.password
        if self.validate_password():
            login_type = "user" if self.login_type == "User" else "admin"

            try:
                db_config = {
                    "host": "localhost",
                    "user": "root",
                    "password": "root",
                    "database": "loginconn",
                    "port": 3306,
                }

                connection = mysql.connector.connect(**db_config)
                cursor = connection.cursor()

                if login_type == 'user':
                    user_info = self.fetch_user_info(username)
                    if user_info is not None:
                        self.user_id, self.urname = user_info
                        st.success(f"User Login Successful! Welcome, {username} !")
                        self.load_user_page()
                    else:
                        st.error("User Login Failed. Admin information not retrieved.")

                elif login_type == 'admin':
                    admin_info = self.fetch_admin_info(username)
                    if admin_info is not None:
                        self.admin_id, self.admin_name = admin_info
                        st.success(f"Admin Login Successful! Welcome, {username} !")
                        self.load_admin_page()
                    else:
                        st.error("Admin Login Failed. Admin information not retrieved.")

            except mysql.connector.Error as err:
                st.error(f"Error: {err}")

            finally:
                if 'cursor' in locals():
                    cursor.close()
                if 'connection' in locals():
                    connection.close()
            self.perform_database_operations(username, password, login_type)
    
    def fetch_admin_info(self, admin_name):
        try:
            db_config = {
                "host": "localhost",
                "user": "root",
                "password": "root",
                "database": "loginconn",
                "port": 3306,
            }

            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor(dictionary=True)

            query = "SELECT id, username FROM admin WHERE username = %s"
            cursor.execute(query, (admin_name,))
            admin_info = cursor.fetchone()

            if admin_info:
                return admin_info['id'], admin_info['username']
            else:
                st.error("Admin not found in the database.")
                return None

        except mysql.connector.Error as err:
            st.error(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()
    def fetch_user_info(self, user_name):
        try:
            db_config = {
                "host": "localhost",
                "user": "root",
                "password": "root",
                "database": "loginconn",
                "port": 3306,
            }

            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor(dictionary=True)

            query = "SELECT id, urname FROM users WHERE urname = %s"
            cursor.execute(query, (user_name,))
            user_info = cursor.fetchone()

            if user_info:
                return user_info['id'], user_info['urname']
            else:
                st.error("User not found in the database.")
                return None

        except mysql.connector.Error as err:
            st.error(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()
    def perform_database_operations(self, username, password, login_type):
        db_config = {
            "host": "localhost",
            "user": "root",
            "password": "root",
            "database": "loginconn",
            "port": 3306,
        }

        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            if login_type == "user":
                # user exists in the database
                query = "SELECT  id, urname FROM users WHERE urname = %s AND urpassword = %s"
                cursor.execute(query, (username, password))
                result = cursor.fetchone()
            else:
                # admin exists in the database
                query = "SELECT id, username FROM admin WHERE username = %s AND password = %s"
                cursor.execute(query, (username, password))
                result = cursor.fetchone()
                #st.write("admin id:", result[0])  
                #st.write("admin name:", result[1]) 

        except mysql.connector.Error as err:
            st.error(f"Error: {err}")

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()

def main():
    login_page = LoginPage()
    login_page.display_login()
if __name__ == "__main__":
    main()