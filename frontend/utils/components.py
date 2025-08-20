import streamlit as st

def select_user(users, label="ユーザーを選択"):
    """ユーザー選択セレクトボックス"""
    user_dict = {user['username']: user for user in users}
    selected = st.selectbox(label, options=list(user_dict.keys()))
    return user_dict[selected]

def select_room(rooms, label="会議室を選択"):
    """会議室選択セレクトボックス"""
    room_dict = {room['room_name']: room for room in rooms}
    selected = st.selectbox(label, options=list(room_dict.keys()))
    return room_dict[selected]

def select_booking(bookings, users, rooms, label="編集する予約を選択"):
    if not bookings:
        return None

    def format_label(b):
        user = next((u["username"] for u in users if u["user_id"] == b["user_id"]), "不明なユーザー")
        room = next((r["room_name"] for r in rooms if r["room_id"] == b["room_id"]), "不明な会議室")
        return f"{b['booking_id']}: {user} - {room} - {b['start_datetime']}"

    booking_dict = {format_label(b): b for b in bookings}
    options = list(booking_dict.keys())

    if not options:
        st.warning("選択肢が存在しません。")
        return None

    selected = st.selectbox(label, options)
    return booking_dict.get(selected)  # ← get()で安全に取得


def api_result_message(res, success_msg="成功しました", fail_msg="失敗しました"):
    """API結果に応じたメッセージ"""
    if res["status_code"] == 200:
        st.success(success_msg)
        # st.rerun()
    else:
        detail_msg = res["data"].get("detail", "不明なエラー")
        st.error(f"{fail_msg}: {detail_msg}")