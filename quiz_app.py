import streamlit as st
import subprocess

def show_quiz():
    st.write("Quiz will start here!")

def load_admin_page():
    subprocess.run(["streamlit", "run", "loginstream.py"])
    st.experimental_rerun()

def main():
    st.title('Quiz Application')
    st.header('Welcome to the Quiz!')
    st.write('''
    This is a simple quiz application built using Streamlit. The quiz covers a variety of topics, 
    including general knowledge, science, history, and more. Test your knowledge and have fun!
    ''')

    # Adding custom CSS for the floating GIF background
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(" https://i.gifer.com/HKVW.gif");
              background-attachment: local;
             background-size: 50%;
              background-position: center;
               background-origin: content-box;
             
        }}      
        
        </style>
        """,
        unsafe_allow_html=True
    )

    # Instructions section
    st.subheader("Instructions:")
    st.write("Please read the following instructions carefully before you begin the quiz:")

    # Instruction list (you can add more as per your quiz rules)
    st.write("- Make sure to answer all questions.")
    st.write("- Good luck and have fun!")

    # Start quiz button
    if st.button('Login here ;)'):
        load_admin_page()

if __name__ == '__main__':
    main()