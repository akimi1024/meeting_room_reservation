import streamlit as st

def show_header(page_title: str):
    st.markdown(f"### {page_title} - ログインユーザー: {st.session_state.get('username')}")