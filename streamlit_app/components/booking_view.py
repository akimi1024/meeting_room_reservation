import streamlit as st
import requests
import json
import datetime
import pandas as pd


def booking_render():
    st.title('会議室予約')
    # ユーザー一覧を取得
    url_users = 'http://127.0.0.1:8000/api/users'
    res_user = requests.get(url_users)
    res_users = res_user.json()
    user_dict = {user['username']: user['user_id'] for user in res_users}

    # 会議室一覧を取得
    url_rooms = 'http://127.0.0.1:8000/api/rooms'
    res_room = requests.get(url_rooms)
    res_rooms = res_room.json()
    room_dict = {room['room_name']: {'room_id': room['room_id'], 'capacity': room['capacity']} for room in res_rooms}

    st.write('### 会議室一覧')
    df_rooms = pd.DataFrame(res_rooms)
    df_rooms.columns = ['会議室名', '定員', 'ID']
    st.table(df_rooms)

    url_booking = 'http://127.0.0.1:8000/api/bookings'
    res_booking = requests.get(url_booking)
    res_bookings = res_booking.json()
    if not res_bookings:
        st.info("予約データがありません")
    else:
      df_bookings = pd.DataFrame(res_bookings)

      users_id = {}
      for user in res_users:
          users_id[user['user_id']] = user['username']
      rooms_id = {}
      for room in res_rooms:
          rooms_id[room['room_id']] = {'room_name': room['room_name'], 'capacity': room['capacity']}


      to_username = lambda x: users_id[x]
      to_roomname = lambda x: rooms_id[x]['room_name']
      to_datetime = lambda x: datetime.datetime.fromisoformat(x).strftime('%Y/%m/%d %H:%M')

      df_bookings['user_id'] = df_bookings['user_id'].map(to_username)
      df_bookings['room_id'] = df_bookings['room_id'].map(to_roomname)
      df_bookings['start_datetime'] = df_bookings['start_datetime'].map(to_datetime)
      df_bookings['end_datetime'] = df_bookings['end_datetime'].map(to_datetime)

      df_bookings = df_bookings.rename(columns={
          'user_id': '予約者名',
          'room_id': '会議室名',
          'booked_num': '予約人数',
          'start_datetime': '開始日時',
          'end_datetime': '終了日時',
          'booking_id': '予約ID'
      })

      st.write('### 予約一覧')
      st.table(df_bookings)

      with st.form(key='bookings'):
          user_name = st.selectbox('予約者名', options=list(user_dict.keys()))
          room_name = st.selectbox('会議室名', options=list(room_dict.keys()))
          booked_num = st.number_input('予約人数', step=1, min_value=1)
          date = st.date_input('予約日', min_value=datetime.date.today())
          start_time = st.time_input('開始時間', value=datetime.time(9, 0))
          end_time = st.time_input('終了時間', value=datetime.time(20, 0))

          submit_button = st.form_submit_button(label='送信')

          if submit_button:
              user_id = user_dict[user_name]
              room_id = room_dict[room_name]['room_id']
              capacity = room_dict[room_name]['capacity']
              booking_data = {
                  'user_id': user_id,
                  'room_id': room_id,
                  'booked_num': booked_num,
                  'start_datetime': datetime.datetime.combine(date, start_time).isoformat(),
                  'end_datetime': datetime.datetime.combine(date, end_time).isoformat()
              }

              if booked_num > capacity:
                  st.error(f'予約人数が会議室の定員({capacity})を超えています。')
              elif start_time >= end_time:
                  st.error('終了時間は開始時間より後でなければなりません。')
              elif start_time < datetime.time(9, 0) or end_time > datetime.time(20, 0):
                  st.error('予約時間は9:00から20:00の間でなければなりません。')
              else:
                  url = 'http://127.0.0.1:8000/api/bookings'

                  res = requests.post(
                      url,
                      data=json.dumps(booking_data),
                  )

                  if res.status_code == 200:
                      st.success('予約登録成功')
                  elif res.status_code == 404:
                      st.error('指定された時間に会議室はすでに予約されています。')
                  else:
                      st.error(f'予約登録失敗: {res.text}')

def booking_info_update_render():
    st.title("予約編集")

    # 予約一覧取得
    url_booking = 'http://127.0.0.1:8000/api/bookings'
    res_booking = requests.get(url_booking)
    res_bookings = res_booking.json()

    # ユーザー一覧取得
    url_users = 'http://127.0.0.1:8000/api/users'
    res_user = requests.get(url_users)
    res_users = res_user.json()
    user_dict = {user['username']: user['user_id'] for user in res_users}

    # 会議室一覧取得
    url_rooms = 'http://127.0.0.1:8000/api/rooms'
    res_room = requests.get(url_rooms)
    res_rooms = res_room.json()
    room_dict = {room['room_name']: {'room_id': room['room_id'], 'capacity': room['capacity']} for room in res_rooms}

    if not res_bookings:
        st.info("登録されている予約がありません。")
    else:
        # booking_idと表示用の組み合わせを作成
        booking_options = {
            f"{booking['booking_id']}: {booking['user_id']} - {booking['room_id']} - {booking['start_datetime']}":
            booking['booking_id']
            for booking in res_bookings
        }

        # 編集する予約選択
        selected_booking_label = st.selectbox("編集する予約を選択", list(booking_options.keys()))
        selected_booking_id = booking_options[selected_booking_label]

        # 選択した予約データを取得
        current_booking = next(b for b in res_bookings if b["booking_id"] == selected_booking_id)

        # 現在のデータをフォームにセット
        current_user = next(user["username"] for user in res_users if user["user_id"] == current_booking["user_id"])
        current_room = next(room["room_name"] for room in res_rooms if room["room_id"] == current_booking["room_id"])
        current_start = datetime.datetime.fromisoformat(current_booking["start_datetime"])
        current_end = datetime.datetime.fromisoformat(current_booking["end_datetime"])

        with st.form(key="edit_booking_form"):
            new_user_name = st.selectbox("予約者", options=list(user_dict.keys()), index=list(user_dict.keys()).index(current_user))
            new_room_name = st.selectbox("会議室", options=list(room_dict.keys()), index=list(room_dict.keys()).index(current_room))
            new_booked_num = st.number_input("予約人数", value=current_booking["booked_num"], step=1, min_value=1)
            new_date = st.date_input("予約日", value=current_start.date())
            new_start_time = st.time_input("開始時間", value=current_start.time())
            new_end_time = st.time_input("終了時間", value=current_end.time())

            col1, col2 = st.columns(2)
            with col1:
                update_button = st.form_submit_button("更新")
            with col2:
                delete_button = st.form_submit_button("削除")

        # 更新処理
        if update_button:
            user_id = user_dict[new_user_name]
            room_id = room_dict[new_room_name]["room_id"]
            capacity = room_dict[new_room_name]["capacity"]

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
                url_update = f"http://127.0.0.1:8000/api/bookings/{selected_booking_id}"
                res_update = requests.put(url_update, data=json.dumps(update_data))

                if res_update.status_code == 200:
                    st.success("予約情報を更新しました")
                elif res_update.status_code == 404:
                    st.error("指定された時間に会議室はすでに予約されています。")
                else:
                    st.error(f"予約の更新に失敗しました: {res_update.text}")

        # 削除処理
        if delete_button:
            url_delete = f"http://127.0.0.1:8000/api/bookings/{selected_booking_id}"
            res_delete = requests.delete(url_delete)

            if res_delete.status_code == 200:
                message = res_delete.json().get("message", "予約を削除しました")
                st.success(message)
            else:
                st.error(f"予約の削除に失敗しました: {res_delete.text}")
