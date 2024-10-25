import sys
import mysql.connector
import streamlit as st
from admin import AdminPage

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

class QuestionsPage:
    def __init__(self, username, admin_id, subject):
        self.connection = establish_connection()
        self.cursor = self.connection.cursor(dictionary=True)
        self.username = username
        self.admin_id = admin_id
        self.subject = subject

    def fetch_questions(self):
        try:
            if self.subject is not None:
                table_name = f"{self.subject}"
                query = f"SELECT * FROM {table_name}"
                self.cursor.execute(query)
                questions = self.cursor.fetchall()
                return questions
            else:
                st.warning("Please select a subject before fetching questions.")
                return None
        except mysql.connector.Error as err:
            st.error(f"Error retrieving questions: {err}")
            return None

    def add_question_to_db(self, question_text, options, correct_answer, duration):
        if self.subject is None:
            st.error("Subject not selected. Please select a subject first.")
            return

        add_question_query = f"INSERT INTO {self.subject.lower()} (question_text, options, correct_answer, duration) VALUES (%s, %s, %s, %s)"

        data = (question_text, options, correct_answer, duration)

        try:
            self.cursor.execute(add_question_query, data)
            self.connection.commit()
            st.success("Question added successfully!")
        except mysql.connector.Error as err:
            st.error(f"Error adding question: {err}")

    def add_questions_ui(self):
        st.title("📝 Add Questions")
        with st.form(key="question_form"):
            question_text = st.text_input("Question")
            options = st.text_input("Options (comma-separated)")
            correct_answer = st.text_input("Correct Answer")
            duration = st.number_input("Time Duration (seconds)", min_value=10, max_value=300, step=10)
            submit_question = st.form_submit_button("Add Question")

            if submit_question:
                self.add_question_to_db(question_text, options, correct_answer, duration)

    
    def view_questions(self):
        try:
            st.title("🔍 View Questions")
            if self.subject is not None:
                view_questions_query = f"SELECT * FROM {self.subject}"
                self.cursor.execute(view_questions_query)
                questions = self.cursor.fetchall()
                for q in questions:
                    with st.expander(f"Question ID: {q['id']}"):
                        st.write(f"*Question:* {q['question_text']}")
                        st.write(f"*Options:* {q['options']}")
                        st.write(f"*Correct Answer:* {q['correct_answer']}")
                        st.write(f"*Duration:* {q['duration']} seconds")
            else:
                st.warning("Please select a subject before viewing questions.")
        except mysql.connector.Error as err:
            st.error(f"Error retrieving questions: {err}")
      

    def display_questions(self):
        st.title(f"{self.subject.capitalize()} Questions")

        # Fetch questions from the database based on the subject
        questions = self.fetch_questions()

        if not questions:
            st.warning(f"No questions available for {self.subject.capitalize()}.")
            return

        # Display each question
        for question in questions:
            st.write(f"Question ID: {question['id']}")
            st.write(f"Question Text: {question['question_text']}")
            st.write(f"Options: {question['options']}")
            st.write(f"Correct Answer: {question['correct_answer']}")
            st.write(f"Duration: {question['duration']} seconds")
            st.write("---")
    def delete_question_from_db(self, subject, question_id_to_delete):
        if self.subject is None:
            st.error("Subject not selected. Please select a subject first.")
            return

        delete_question_query = f"DELETE FROM {self.subject} WHERE id = %s"

        try:
            self.cursor.execute(delete_question_query, (question_id_to_delete,))
            self.connection.commit()
            st.success("Question deleted successfully!")
        except mysql.connector.Error as err:
            st.error(f"Error deleting question: {err}")

    
    def get_session_state(self):
        session_state = st.session_state
        if not hasattr(session_state, "questions"):
            session_state.questions = QuestionsPage("", 0, "")  # Default values, you may need to adjust
        return session_state
    

def main():
    username_index = sys.argv.index("username") + 1
    admin_id_index = sys.argv.index("admin_id") + 1
    subject_index = sys.argv.index("subject") + 1
    username = sys.argv[username_index]
    admin_id = int(sys.argv[admin_id_index])
    subject = sys.argv[subject_index]

    admin = AdminPage(username, admin_id)
    qp = QuestionsPage(username, admin_id, subject)

    questions_page = QuestionsPage(username, admin_id, subject)
    st.sidebar.title("🛠 Admin Panel")
    app_mode = st.sidebar.selectbox("Choose the option",
                                    ["Add Questions", "View Questions", "Delete Questions"])
    if app_mode == "Add Questions":
        qp.add_questions_ui()
    elif app_mode == "View Questions":
        qp.view_questions()
    elif app_mode == "Delete Questions":
        st.title("❌ Delete Questions")
        question_id_to_delete = st.text_input("Enter Question ID to delete:")
        if st.button("Delete Question"):
            qp.delete_question_from_db(subject,question_id_to_delete)

if __name__ == "__main__":
    main()