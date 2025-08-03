import streamlit as st
import requests
import json
import datetime
import pandas as pd
from utils import api_client, helpers, components


def booking_render():
    st.title('会議室予約')
    # ユーザー一覧を取得
    users = api_client.get("users")
    # 会議室一覧を取得
    rooms = api_client.get("rooms")
    # 予約一覧を取得
    bookings = api_client.get("bookings")


    # 会議室一覧表示
    st.write('### 会議室一覧')
    if rooms["status_code"] == 200:
        rooms_data = rooms["data"]
        df_rooms = pd.DataFrame(rooms_data)
        df_rooms.columns = ['会議室名', '定員', 'ID']
        st.table(df_rooms)
    else:
        st.error("会議室一覧の取得に失敗しました")

    # 予約一覧表示
    if bookings["status_code"] == 200:
        df_bookings = helpers.booking_df_transform(bookings["data"], users["data"], rooms["data"])
        st.table(df_bookings)
    else:
        st.info("予約データがありません")

    # 予約フォーム
    with st.form(key='bookings'):
        user = components.select_user(users["data"], "予約者名")
        room = components.select_room(rooms["data"], "会議室名")
        booked_num = st.number_input('予約人数', step=1, min_value=1)
        date = st.date_input('予約日', min_value=datetime.date.today())
        start_time = st.time_input('開始時間', value=datetime.time(9, 0))
        end_time = st.time_input('終了時間', value=datetime.time(20, 0))

        submit_button = st.form_submit_button(label='送信')

        if submit_button:
            if booked_num > room['capacity']:
                st.error(f'予約人数が会議室の定員({room["capacity"]})を超えています。')
            elif start_time >= end_time:
                st.error('終了時間は開始時間より後でなければなりません。')
            else:
                booking_data = {
                    'user_id': user,
                    'room_id': room['room_id'],
                    'booked_num': booked_num,
                    'start_datetime': datetime.datetime.combine(date, start_time).isoformat(),
                    'end_datetime': datetime.datetime.combine(date, end_time).isoformat()
                }
                res = api_client.post("bookings", booking_data)
                components.api_result_message(res, "予約登録成功", "予約登録失敗")


def booking_info_update_render():
    st.title("予約編集")

    # --- API からデータ取得 ---
    bookings = api_client.get("bookings")
    users = api_client.get("users")
    rooms = api_client.get("rooms")

    if bookings["status_code"] != 200:
        st.info("登録されている予約がありません。")
        return

    # --- 辞書化 ---
    user_dict = {user['username']: user['user_id'] for user in users["data"]}
    room_dict = {room['room_name']: room['room_id'] for room in rooms["data"]}

    # --- booking_idと表示用テキストをマッピング ---
    booking_options = {
        f"{b['booking_id']}: {b['user_id']} - {b['room_id']} - {b['start_datetime']}": b['booking_id']
        for b in bookings["data"]
    }

    # --- 編集対象の予約を選択 ---
    selected_booking_label = st.selectbox("編集する予約を選択", list(booking_options.keys()))
    selected_booking_id = booking_options[selected_booking_label]
    current_booking = next(b for b in bookings["data"] if b["booking_id"] == selected_booking_id)

    # --- 現在の予約情報を展開 ---
    current_user = next(u["username"] for u in users["data"] if u["user_id"] == current_booking["user_id"])
    current_room = next(r["room_name"] for r in rooms["data"] if r["room_id"] == current_booking["room_id"])
    current_start = datetime.datetime.fromisoformat(current_booking["start_datetime"])
    current_end = datetime.datetime.fromisoformat(current_booking["end_datetime"])

    # --- 編集フォーム ---
    with st.form(key="edit_booking_form"):
        new_user_name = st.selectbox(
            "予約者",
            options=list(user_dict.keys()),
            index=list(user_dict.keys()).index(current_user)
        )
        new_room_name = st.selectbox(
            "会議室",
            options=list(room_dict.keys()),
            index=list(room_dict.keys()).index(current_room)
        )
        new_booked_num = st.number_input("予約人数", value=current_booking["booked_num"], step=1, min_value=1)
        new_date = st.date_input("予約日", value=current_start.date())
        new_start_time = st.time_input("開始時間", value=current_start.time())
        new_end_time = st.time_input("終了時間", value=current_end.time())

        col1, col2 = st.columns(2)
        with col1:
            update_button = st.form_submit_button("更新")
        with col2:
            delete_button = st.form_submit_button("削除")

    # --- 更新処理 ---
    if update_button:
        user_id = user_dict[new_user_name]
        room_id = room_dict[new_room_name]
        capacity = next(r["capacity"] for r in rooms["data"] if r["room_id"] == room_id)

        if new_booked_num > capacity:
            st.error(f'予約人数が会議室の定員({capacity})を超えています。')
        elif new_start_time >= new_end_time:
            st.error('終了時間は開始時間より後でなければなりません。')
        elif new_start_time < datetime.time(9, 0) or new_end_time > datetime.time(20, 0):
            st.error('予約時間は9:00から20:00の間でなければなりません。')
        else:
            update_data = {
                "user_id": user_id,
                "room_id": room_id,
                "booked_num": new_booked_num,
                "start_datetime": datetime.datetime.combine(new_date, new_start_time).isoformat(),
                "end_datetime": datetime.datetime.combine(new_date, new_end_time).isoformat()
            }
            response = api_client.put(f"bookings/{selected_booking_id}", update_data)

            if response:
                st.success("予約情報を更新しました")
            else:
                st.error("予約の更新に失敗しました")

    # --- 削除処理 ---
    if delete_button:
        response = api_client.delete(f"bookings/{selected_booking_id}")
        if response:
            message = response.get("message", "予約を削除しました")
            st.success(message)
        else:
            st.error("予約の削除に失敗しました")