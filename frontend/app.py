import streamlit as st
from components import login, header, booking_view, user_view, room_view

def main():
    if "token" not in st.session_state:
        login.login_or_signup_form()
    else:
        # 共通メニュー
        menu = ["予約登録", "予約管理"]

        # 管理者だけ追加
        if st.session_state.get("is_admin", False):
            menu.extend(["ユーザー登録", "会議室登録", "ユーザー管理", "会議室管理"])

        menu.append("ログアウト")

        page = st.sidebar.selectbox("ページ選択", menu)

        if page == "ログアウト":
            st.session_state.clear()
            st.rerun()

        # 選択ページをヘッダーに表示
        header.show_header(page)

        # ページごとの処理
        if page == "予約登録":
            booking_view.booking_render()
        elif page == "ユーザー登録":
            user_view.user_registration_render()
        elif page == "会議室登録":
            room_view.room_registration_render()
        elif page == "予約管理":
            booking_view.booking_info_update_render()
        elif page == "ユーザー管理":
            user_view.user_info_update_render()
        elif page == "会議室管理":
            room_view.room_info_update_render()

if __name__ == "__main__":
    main()
