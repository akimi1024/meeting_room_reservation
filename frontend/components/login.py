import streamlit as st
from utils import api_client

def login_or_signup_form():
    # セッションでページ種別を保持（初期はログイン）
    if "auth_mode" not in st.session_state:
        st.session_state["auth_mode"] = "login"

    # タイトル切り替え
    if st.session_state["auth_mode"] == "login":
        st.subheader("ログイン")
    else:
        st.subheader("サインアップ")

    with st.form("auth_form"):
        username = st.text_input("ユーザー名")
        password = st.text_input("パスワード", type="password")

        # サインアップの場合だけ管理者フラグ追加（任意）
        is_admin = False
        # if st.session_state["auth_mode"] == "signup":
            # is_admin = st.checkbox("管理者として登録する", value=False)

        submitted = st.form_submit_button(
            "ログイン" if st.session_state["auth_mode"] == "login" else "サインアップ"
        )

        if submitted:
            if st.session_state["auth_mode"] == "login":
                res = api_client.post("login", {"username": username, "password": password})
            else:
                res = api_client.post("signup", {"username": username, "password": password, "is_admin": is_admin})

            if res["status_code"] == 200:
                # ログイン時・サインアップ時の共通処理
                token = res["data"]["access_token"]
                st.session_state["token"] = token
                st.session_state["is_admin"] = res["data"]["user"]["is_admin"]
                st.session_state["username"] = res["data"]["user"]["username"]
                st.rerun()
            else:
                # エラー詳細がある場合は表示
                detail = res["data"].get("detail")
                if isinstance(detail, list):
                    # Pydanticバリデーションエラーの形式
                    for err in detail:
                        st.error(f"{err.get('loc', [''])[1]}: {err.get('msg')}")
                elif isinstance(detail, str):
                    # 普通のエラーメッセージ形式
                    st.error(detail)
                else:
                    st.error("処理失敗")


    # 切り替えリンク
    if st.session_state["auth_mode"] == "login":
        if st.button("アカウントを作成する"):
            st.session_state["auth_mode"] = "signup"
            st.rerun()
    else:
        if st.button("既にアカウントをお持ちの方はこちら"):
            st.session_state["auth_mode"] = "login"
            st.rerun()
