import streamlit as st
import requests
import json
import datetime
import pandas as pd

page = st.sidebar.selectbox(
    'menu',
    ('user', 'rooms', 'bookings')
)

if page == 'user':
    st.title('ユーザー登録画面')
    with st.form(key='user'):
        # user_id = random.randint(1, 10)
        username = st.text_input('ユーザー名', max_chars=12)
        user_data = {
            # 'user_id': user_id,
            'username': username
        }

        submit_button = st.form_submit_button(label='送信')

        if submit_button:
            st.write('## 送信データ')
            st.write('## レスポンス')
            url = 'http://127.0.0.1:8000/api/users'

            res = requests.post(
                url,
                data=json.dumps(user_data),
            )

            if res.status_code == 200:
                st.write('### ユーザー登録成功')
                st.success('ユーザー登録成功')
            else:
                st.write('### ユーザー登録失敗')

            st.write('## レスポンス')
            st.write(res.status_code)
            st.write("生レスポンス:", res.text)
            st.write('### 送信データ')
            st.json(user_data)

            st.json(res.json())

elif page == 'rooms':
    st.title('APIテスト画面（ルーム）')
    with st.form(key='rooms'):
        # room_id = random.randint(1, 10)
        room_name = st.text_input('ルーム名', max_chars=12)
        capacity = st.number_input('収容人数', step=1)
        room_data = {
            # 'room_id': room_id,
            'room_name': room_name,
            'capacity': capacity
        }

        submit_button = st.form_submit_button(label='送信')

        if submit_button:
            url = 'http://127.0.0.1:8000/api/rooms'

            res = requests.post(
                url,
                data=json.dumps(room_data),
            )

            st.write('### ステータスコード')
            st.write(res.status_code)

            if res.status_code == 200:
                st.write('### ルーム登録成功')
                st.success('ルーム登録成功')
            else:
                st.write('### ルーム登録失敗')
            st.json(res.json())

elif page == 'bookings':
    st.title('会議室予約画面')
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
                st.write('## 送信データ')
                st.json(booking_data)
                st.write('## レスポンス')
                url = 'http://127.0.0.1:8000/api/bookings'

                res = requests.post(
                    url,
                    data=json.dumps(booking_data),
                )

                if res.status_code == 200:
                    st.write('### 予約登録成功')
                    st.success('予約登録成功')
                elif res.status_code == 404:
                    st.write('### 予約登録失敗')
                    st.error('指定された時間に会議室はすでに予約されています。')
                else:
                    st.write('### 予約登録失敗')
                st.write('### レスポンス')
                st.json(res.json())