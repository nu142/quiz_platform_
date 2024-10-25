import streamlit as st
import subprocess

def select_subject():
        st.title("Select Subject")

        # Button to select 'mathematics'
        if st.button("mathematics"):
            load_questions("mathematics")

        # Button to select 'Python'
        if st.button("Python"):
            load_questions("python")

def load_questions(subject):
    
        subprocess.run(["streamlit", "run", "strt.py", "selected_subject", "subject",str(subject)])
        st.experimental_rerun()
def main():
    st.title("Subject Selection")

    st.write("Please select your subjects from the options below:")
    select_subject()
    

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