import streamlit as st
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

    selected_room = components.select_room(rooms, label="編集する会議室を選択")

    with st.form(key="edit_room_form"):
        new_room_name = st.text_input("会議室名", value=selected_room["room_name"])
        new_capacity = st.number_input("定員", value=selected_room["capacity"], step=1, min_value=1)
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
        res_update = api_client.put("rooms", update_data, selected_room["room_id"])
        components.api_result_message(res_update, success_msg=f"{new_room_name} に更新しました", fail_msg="更新に失敗しました")


    # 削除処理
    if delete_button:
        res_delete = api_client.delete("rooms", selected_room["room_id"])
        components.api_result_message(res_delete, success_msg="削除しました", fail_msg="削除に失敗しました")
