import streamlit as st
from utils import api_client, helpers, components

def user_registration_render():
    with st.form(key='user'):
        username = st.text_input('ユーザー名', max_chars=12)
        password = st.text_input("パスワード", type="password")
        admin_button = st.checkbox(label='管理者ユーザー')
        user_data = {
            'username': username,
            'password_hash': password,
            'is_admin': admin_button
        }

        submit_button = st.form_submit_button(label='送信')

        if submit_button:
            res = api_client.post("users", user_data)

            if res["status_code"] == 200:
                st.success('ユーザー登録成功')
            else:
                st.error('ユーザー登録失敗')

def user_info_update_render():
    # ユーザー一覧を取得
    res_users = helpers.fetch_list("users")

    if not res_users:
        return

    # 選択ボックスでユーザーを選択
    selected_user = components.select_user(res_users)

    # 編集フォーム
    with st.form(key="edit_user_form"):
        new_username = st.text_input("ユーザー名", value=selected_user["username"])
        new_password = st.text_input("新しいパスワード（変更する場合のみ）", type="password")
        admin_button = st.checkbox(label='管理者ユーザー', value=selected_user["is_admin"])

        col1, col2 = st.columns(2)
        with col1:
            update_button = st.form_submit_button("更新")
        with col2:
            delete_button = st.form_submit_button("削除")

        # 更新処理
        if update_button:
            if new_username.strip() == "":
                st.error("ユーザー名を入力してください")
            else:
                update_data = {
                    'username': new_username,
                    'is_admin': admin_button
                }
                # パスワードが入力されていれば追加
                if new_password.strip():
                    update_data["password_hash"] = new_password
                else:
                    update_data["password_hash"] = selected_user["password_hash"]

                res_update = api_client.put("users", update_data, selected_user["user_id"])
                components.api_result_message(
                    res_update,
                    f"{selected_user['username']}に更新しました",
                    "更新に失敗しました"
                )

        # 削除処理
        if delete_button:
            res_delete = api_client.delete("users", selected_user["user_id"])
            components.api_result_message(res_delete, success_msg="削除しました", fail_msg="削除に失敗しました")