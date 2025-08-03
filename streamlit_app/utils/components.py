import streamlit as st

def select_user(users, label="ユーザーを選択"):
    """ユーザー選択セレクトボックス"""
    user_dict = {user['username']: user['user_id'] for user in users}
    selected = st.selectbox(label, options=list(user_dict.keys()))
    return user_dict[selected]

def select_room(rooms, label="会議室を選択"):
    """会議室選択セレクトボックス"""
    room_dict = {room['room_name']: room for room in rooms}
    selected = st.selectbox(label, options=list(room_dict.keys()))
    return room_dict[selected]

def confirm_delete(message="削除してもいいですか？"):
    """削除ボタン"""
    with st.form(key="delete_form"):
        st.write(message)
        delete_button = st.form_submit_button("削除")
    return delete_button

def api_result_message(res, success_msg="成功しました", fail_msg="失敗しました"):
    """API結果に応じたメッセージ"""
    if res["status_code"] == 200:
        st.success(success_msg)
    else:
        detail_msg = res["data"].get("detail", "不明なエラー")
        st.error(f"{fail_msg}: {detail_msg}")