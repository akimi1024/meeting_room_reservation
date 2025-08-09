import streamlit as st
from utils import api_client

def login_form():
    with st.form("login_form"):
        username = st.text_input("ユーザー名")
        # password = st.text_input("パスワード", type="password")
        submitted = st.form_submit_button("ログイン")

        if submitted:
            # res = api_client.post("login", {"username": username, "password": password})
            res = api_client.post("login", {"username": username})
            st.write(res)
            if res["status_code"] == 200:
                # st.session_state["token"] = res["data"]["token"]
                st.session_state["token"] = True  # 仮ログイン状態
                st.session_state["is_admin"] = res["data"].get("is_admin", False)
                st.session_state["username"] = res["data"].get("username")
                st.rerun()
            else:
                st.error("ログイン失敗")
