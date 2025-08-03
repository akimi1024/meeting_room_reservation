import streamlit as st
import datetime
import pandas as pd
from utils import api_client

def build_user_dict(users):
    return {user['username']: user['user_id'] for user in users}

def build_room_dict(rooms):
    return {room['room_name']: {'room_id': room['room_id'], 'capacity': room['capacity']} for room in rooms}

def format_datetime(iso_str):
    return datetime.datetime.fromisoformat(iso_str).strftime('%Y/%m/%d %H:%M')

def booking_df_transform(bookings, users, rooms):
    """予約データをUI表示用に変換"""
    df = pd.DataFrame(bookings)

    users_id = {u['user_id']: u['username'] for u in users}
    rooms_id = {r['room_id']: {'room_name': r['room_name'], 'capacity': r['capacity']} for r in rooms}

    df['user_id'] = df['user_id'].map(lambda x: users_id[x])
    df['room_id'] = df['room_id'].map(lambda x: rooms_id[x]['room_name'])
    df['start_datetime'] = df['start_datetime'].map(format_datetime)
    df['end_datetime'] = df['end_datetime'].map(format_datetime)

    return df.rename(columns={
        'user_id': '予約者名',
        'room_id': '会議室名',
        'booked_num': '予約人数',
        'start_datetime': '開始日時',
        'end_datetime': '終了日時',
        'booking_id': '予約ID'
    })

def fetch_list(endpoint):
    if endpoint == "users":
        not_found_msg = "登録されているユーザー情報がありません"
        error_msg = "ユーザー一覧の取得に失敗しました"
    elif endpoint == "rooms":
        not_found_msg = "登録されている会議室がありません"
        error_msg = "会議室一覧の取得に失敗しました"
    elif endpoint == "booking":
        not_found_msg = "登録されている予約がありません"
        error_msg = "予約一覧の取得に失敗しました"

    """一覧データ取得の共通処理"""
    res = api_client.get(endpoint)
    if res["status_code"] == 200:
        if res["data"]:
            return res["data"]
        else:
            st.info(not_found_msg)
            return []
    elif res["status_code"] == 404:
        st.info(not_found_msg)
        return []
    else:
        st.error(f"{error_msg}: {res['error']}")
        return []