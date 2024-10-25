# # import streamlit as st
# # from dbsetup import Question, Session

# # def load_questions_from_db():
# #     session = Session()
# #     questions = session.query(Question).all()
# #     session.close()  # Close the session when done
# #     return questions

# # def display_question(question, question_number, total_questions):
# #     # Display the current question and its options
# #     st.title(f"Quiz: Question {question_number} of {total_questions}")
# #     st.write(question.question_text)  # Display the question text
    
# #     # Show progress
# #     progress_bar = st.progress(question_number / total_questions)
    
# #     options = question.options.split(',')
# #     user_answer = st.radio("Choose one option:", options, key=question.id)
    
# #     # Determine if it's the last question to change the button text accordingly
# #     if question_number == total_questions:
# #         button_label = "Submit Quiz"
# #     else:
# #         button_label = "Next"

# #     if st.button(button_label):
# #         return {"Question": question.question_text, "User Answer": user_answer, "Correct Answer": question.correct_answer}
# #     return None

# # def display_leaderboard(user_responses):
# #     st.title("Quiz Completed!")
# #     if user_responses:
# #         correct_responses = sum(1 for response in user_responses if response['User Answer'] == response['Correct Answer'])
# #         total_questions = len(user_responses)
# #         score = correct_responses / total_questions * 100
# #         st.success(f"Your total score is: {correct_responses}/{total_questions} - {score:.2f}%")

# # def main():
# #     st.session_state.setdefault('current_question', 0)
# #     st.session_state.setdefault('user_responses', [])
# #     st.session_state.setdefault('quiz_finished', False)

# #     if not st.session_state['quiz_finished']:
# #         questions = load_questions_from_db()
# #         total_questions = len(questions)
        
# #         if st.session_state['current_question'] < total_questions:
# #             current_question_num = st.session_state['current_question'] + 1
# #             response = display_question(questions[st.session_state['current_question']], current_question_num, total_questions)
# #             if response:
# #                 st.session_state.user_responses.append(response)
# #                 if current_question_num == total_questions:
# #                     st.session_state['quiz_finished'] = True
# #                     st.experimental_rerun()
# #                 else:
# #                     st.session_state.current_question += 1
# #                     st.experimental_rerun()
# #         else:
# #             st.session_state['quiz_finished'] = True
# #             st.experimental_rerun()
    
# #     if st.session_state['quiz_finished']:
# #         display_leaderboard(st.session_state.user_responses)
# #         # Optionally, you can add a button or mechanism to reset the quiz here if needed.

# # if __name__ == "__main__":
# #     main()
# import streamlit as st
# import mysql.connector

# # Function to establish connection to MySQL database
# def establish_connection():
#     db_config = {
#         "host": "localhost",
#         "user": "root",
#         "password": "root",
#         "database": "loginconn",
#         "port": 3306,
#     }
#     try:
#         connection = mysql.connector.connect(**db_config)
#         return connection
#     except mysql.connector.Error as e:
#         st.error(f"Error connecting to MySQL database: {e}")
#         return None

# # Function to fetch user information
# def fetch_user_info(connection):
#     user_info_query = "SELECT id, urname FROM users LIMIT 1"
#     cursor = connection.cursor(dictionary=True)
#     try:
#         cursor.execute(user_info_query)
#         user_info = cursor.fetchone()
#         return user_info
#     except mysql.connector.Error as e:
#         st.error(f"Error fetching user information: {e}")
#         return None
#     finally:
#         cursor.close()


# def close_connection(connection):
#     if connection.is_connected():
#         connection.close()


# def fetch_questions(connection, table_name):
#     fetch_query = f"SELECT * FROM {table_name}"
#     cursor = connection.cursor(dictionary=True)
#     try:
#         cursor.execute(fetch_query)
#         questions = cursor.fetchall()
#         return questions
#     except mysql.connector.Error as e:
#         st.error(f"Error fetching questions from table {table_name}: {e}")
#         return None
#     finally:
#         cursor.close()


# # Function to display the quiz page for a selected subject
# def display_quiz(subject, username, user_id):
#     st.title(f"Quiz for {subject}")
#     st.write(f"Welcome {username} (ID: {user_id}) to the {subject} quiz!")
#     st.write("Here you can attend the quiz for the selected subject.")

#     # Establish connection to the database
#     connection = establish_connection()
#     if connection:
#         # Fetch questions from the corresponding table based on the subject
#         table_name = subject.lower()  # Assuming table names are lowercase and correspond to subject names
#         questions = fetch_questions(connection, table_name)
#         if questions:
#             # Initialize session state for each question
#             for q in questions:
#                 if f"question_{q['id']}" not in st.session_state:
#                     st.session_state[f"question_{q['id']}"] = None

#             question_index = st.session_state.get("question_index", 0)  # Get the question index from session state
#             num_questions = len(questions)
#             score = st.session_state.get("score", 0)  # Get the current score from session state

#             if question_index < num_questions:
#                 q = questions[question_index]

#                 # Displaying the question and options as MCQ
#                 options = q['options'].split(',')
#                 user_answer = st.radio(
#                     label=q['question_text'],
#                     options=options,
#                     key=f"question_{q['id']}"  # Use question ID as part of the key
#                 )

#                 # Add a button to navigate to the next question
#                 if st.button("Next"):
#                     # Check if the user's answer is correct and update the score accordingly
#                     if user_answer == q['correct_answer']:
#                         score += 1
#                         st.session_state["score"] = score  # Update the score in session state
#                     question_index += 1  # Move to the next question
#                     st.session_state["question_index"] = question_index  # Update the question index in session state
#                     st.experimental_rerun()  # Rerun the script to display the next question

#             else:
#                 # Show submit button after answering all questions
#                 if st.button("Submit"):
#                     st.write(f"Your score: {score}/{num_questions}")

#         else:
#             st.error(f"No questions found for {subject}.")
        
#         # Close the database connection
#         close_connection(connection)
#     else:
#         st.error("Connection to database failed.")


# # Function to calculate the score
# def calculate_score(questions):
#     score = 0
#     for q in questions:
#         user_answer = st.session_state[f"question_{q['id']}"]
#         if user_answer == q['correct_answer']:
#             score += 1
#     return score

# # Main function
# def main():
#     # Establish connection to the database
#     connection = establish_connection()
#     if connection:
#         # Fetch user information
#         user_info = fetch_user_info(connection)
#         if user_info:
#             username = user_info['urname']
#             user_id = user_info['id']
#             # Display the sidebar with username and ID
#             st.sidebar.title("User Information")
#             st.sidebar.write(f"Username: {username}")
#             st.sidebar.write(f"User ID: {user_id}")

#             # Display different subjects in the sidebar
#             st.sidebar.title("Select Subject")
#             subjects = ["Mathematics", "Python"]
#             selected_subject = st.sidebar.selectbox("Choose the subject", subjects)

#             # Reset session state when a new subject is selected
#             if st.session_state.get("selected_subject") != selected_subject:
#                 st.session_state["selected_subject"] = selected_subject
#                 st.session_state["question_index"] = 0
#                 st.session_state["score"] = 0

#             # Check if the user has selected a subject
#             if selected_subject:
#                 display_quiz(selected_subject, username, user_id)  # Display the quiz page for the selected subject

#         else:
#             st.error("User information not found.")
        
#         # Close the database connection
#         close_connection(connection)
#     else:
#         st.error("Connection to database failed.")


# if __name__ == "__main__":
#     main()