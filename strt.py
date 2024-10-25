import streamlit as st
import mysql.connector
import sys
import subprocess
import time
from datetime import datetime, timedelta
import threading


def establish_connection():
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "root",
        "database": "loginconn",
        "port": 3306,
    }
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as e:
        st.error(f"Error connecting to MySQL database: {e}")
        return None
def close_connection(connection):
    if connection.is_connected():
        connection.close()
def fetch_questions(connection, table_name):
    fetch_query = f"SELECT * FROM {table_name}"
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(fetch_query)
        questions = cursor.fetchall()
        return questions
    except mysql.connector.Error as e:
        st.error(f"Error fetching questions from table {table_name}: {e}")
        return None
    finally:
        cursor.close()

def fetch_user_info(connection):
    user_info_query = "SELECT id, urname FROM users LIMIT 1"
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(user_info_query)
        user_info = cursor.fetchone()
        return user_info
    except mysql.connector.Error as e:
        st.error(f"Error fetching user information: {e}")
        return None
    finally:
        cursor.close()
 
def countdown_timer(duration, timer_placeholder):
    total_seconds = duration

    while total_seconds > 0:
        timer = timedelta(seconds=total_seconds)
        timer_placeholder.write(f"Time Left: {timer}")

        # Updating elapsed time
        elapsed_time = (datetime.now() - st.session_state["start_time"]).total_seconds()
        remaining_time = max(int(duration - elapsed_time), 0)

        if remaining_time <= 0:
            timer_placeholder.empty()
            session_state.timer_expired = True
            st.experimental_rerun()
            return

        total_seconds -= 1

    timer_placeholder.empty()
    session_state.timer_expired = True
    st.experimental_rerun()

def display_quiz(subject):
    st.title(f"Quiz on {subject.capitalize()}")
    connection = establish_connection()
    if connection:
        table_name = subject.lower()
        questions = fetch_questions(connection, table_name)
        if questions:
            if "start_time" not in st.session_state or "question_index" not in st.session_state:
                st.session_state["question_index"] = 0
                st.session_state["start_time"] = datetime.now()
                st.session_state["score"] = 0

            question_index = st.session_state["question_index"]
            num_questions = len(questions)
            score = st.session_state["score"]

            # if question_index < num_questions:
            #     q = questions[question_index]
            #     time_limit = q['duration']  # Assuming this is in seconds
            #     elapsed_time = (datetime.now() - st.session_state["start_time"]).total_seconds()
            #     remaining_time = max(int(time_limit - elapsed_time), 0)

            #     with st.sidebar:
            #         st.write(f"Time Left: {remaining_time} seconds")

            #     if remaining_time <= 0:
            #         st.session_state["question_index"] += 1
            #         if st.session_state["question_index"] < num_questions:
            #             st.session_state["start_time"] = datetime.now()
            #             st.experimental_rerun()
            #         else:
            #             display_score(score, num_questions)
            #             return
            if question_index < num_questions:
                q = questions[question_index]
                time_limit = q['duration']  # Assuming this is in seconds
                elapsed_time = (datetime.now() - st.session_state["start_time"]).total_seconds()
                remaining_time = max(int(time_limit - elapsed_time), 0)

                with st.sidebar:
                    st.write(f"Time Left: {remaining_time} seconds")

                if remaining_time <= 0:
                    st.session_state["question_index"] += 1
                    if st.session_state["question_index"] < num_questions:
                        st.session_state["start_time"] = datetime.now()
                        st.experimental_rerun()
                    else:
                        display_score(score, num_questions, subject)
                        return

                st.markdown(f"### Question {question_index + 1} of {num_questions}")
                options = q['options'].split(',')

                with st.form("quiz_form", clear_on_submit=True):
                    st.markdown(f"#### {q['question_text']}")
                    user_answer = st.radio("Select one option:", options, key=f"question_{q['id']}")
                    submit_button = st.form_submit_button("Next")

                if submit_button:
                    if user_answer == q['correct_answer']:
                        st.session_state["score"] += 1

                    st.session_state["question_index"] += 1
                    if st.session_state["question_index"] < num_questions:
                        st.session_state["start_time"] = datetime.now()
                        st.experimental_rerun()
            else:
                display_score(score, num_questions,subject)
                if st.button("Restart Quiz"):
                    restart_quiz()

        else:
            st.error(f"No questions found for {subject}.")
        close_connection(connection)
    else:
        st.error("Connection to database failed.")

def display_score(score, num_questions,subject):
    st.success(f"🎉 Congratulations! You've completed the quiz on {subject}.")
    st.metric(label="Your Score", value=f"{score}/{num_questions}")

def restart_quiz():
    st.session_state["question_index"] = 0
    st.session_state["start_time"] = datetime.now()
    st.session_state["score"] = 0
    subprocess.run(["streamlit","run","usdemo.py"])
    st.experimental_rerun()

def main():
    subject_index = sys.argv.index("subject") + 1 if "subject" in sys.argv else 0
    subject = sys.argv[subject_index] if subject_index else "default_subject"
    # Display the quiz page for the selected subject
    display_quiz(subject)


if __name__ == "__main__":
    main()