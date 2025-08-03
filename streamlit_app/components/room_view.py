import streamlit as st
import requests
import json
from utils import api_client, helpers, components


def room_registration_render():
    st.title('会議室登録')
    with st.form(key='rooms'):
        room_name = st.text_input('ルーム名', max_chars=12)
        capacity = st.number_input('収容人数', step=1)
        room_data = {
            'room_name': room_name,
            'capacity': capacity
        }

        submit_button = st.form_submit_button(label='送信')

        if submit_button:
            room_res = api_client.post("rooms", room_data)

            if room_res["status_code"] == 200:
                st.success('ルーム登録成功')
            else:
                st.write('### ルーム登録失敗')

def room_info_update_render():
    st.title("会議室編集")

    # 会議室一覧を取得
    rooms = helpers.fetch_list("rooms")

    room_dict = helpers.build_room_dict(rooms)

    selected_room_name = st.selectbox("編集する会議室を選択", list(room_dict.keys()))
    selected_room_id = room_dict[selected_room_name]["room_id"]
    current_room = next(room for room in rooms if room["room_id"] == selected_room_id)

    with st.form(key="edit_room_form"):
        new_room_name = st.text_input("会議室名", value=current_room["room_name"])
        new_capacity = st.number_input("定員", value=current_room["capacity"], step=1, min_value=1)
        col1, col2 = st.columns(2)

        with col1:
            update_button = st.form_submit_button("更新")

        with col2:
            delete_button = st.form_submit_button("削除")

    # 更新処理
    if update_button:
        update_data = {
            "room_name": new_room_name,
            "capacity": new_capacity
        }
        res_update = api_client.put("rooms", update_data, selected_room_id)

        if res_update["status_code"] == 200:
            st.success(f"{new_room_name} に更新しました")
        else:
            st.error("更新に失敗しました")

    # 削除処理
    if delete_button:
        res_delete = api_client.delete("rooms", selected_room_id)

        if res_delete["status_code"] == 200:
            st.success(res_delete["data"].get("message", "削除完了"))
        else:
            st.error(f"削除に失敗しました: {res_delete['data']}")