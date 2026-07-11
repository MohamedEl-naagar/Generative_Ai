import streamlit as st

from sqlalchemy import Column,String,Integer,create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
st.header("hello world")
st.button("click me")
st.write("hello naggaro make sure you have a great day!")
name =st.text_input("Enter your name")
st.write("Your name is ",name)

st_option=st.radio("choose the option",[
    "opt1","opt2","opt3"
])

st.write(st_option)

check_option=st.checkbox("choose")

st.write(check_option)