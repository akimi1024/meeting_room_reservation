import streamlit as st
import requests
import json

def user_registration_render():
    st.title('ユーザー登録')
    with st.form(key='user'):
        # user_id = random.randint(1, 10)
        username = st.text_input('ユーザー名', max_chars=12)
        user_data = {
            # 'user_id': user_id,
            'username': username
        }

        submit_button = st.form_submit_button(label='送信')

        if submit_button:
            url = 'http://127.0.0.1:8000/api/users'

            res = requests.post(
                url,
                data=json.dumps(user_data),
            )

            if res.status_code == 200:
                st.success('ユーザー登録成功')
            else:
                st.error('ユーザー登録失敗')

def user_info_update_render():
    st.title("ユーザー編集")
    # ユーザー一覧を取得
    url_users = 'http://127.0.0.1:8000/api/users'
    res_user = requests.get(url_users)
    res_users = res_user.json()
    user_dict = {user['username']: user['user_id'] for user in res_users}

    # 選択ボックスでユーザーを選択
    selected_username = st.selectbox("編集するユーザーを選択してください", options=list(user_dict.keys()))
    selected_user_id = user_dict[selected_username]

    # 選択ユーザーの現在の情報
    current_username = selected_username

    # 編集フォーム
    with st.form(key="edit_user_form"):
        new_username = st.text_input("ユーザー名", value=current_username)
        submit_button = st.form_submit_button("更新")

    # 削除フォーム
    with st.form(key="delete_user_form"):
        st.write("ユーザーを削除する場合は以下のボタンを押してください")
        delete_button = st.form_submit_button("ユーザー削除")

        if submit_button:
            if new_username.strip() == "":
                st.error("ユーザー名を入力してください")
            else:
                update_data = {
                    "username": new_username
                }
                url_update = f'http://127.0.0.1:8000/api/users/{selected_user_id}'
                res_update = requests.put(
                    url_update,
                    data=json.dumps(update_data)
                )

                if res_update.status_code == 200:
                    st.success("ユーザー情報が更新されました")
                else:
                    st.error(f"ユーザー情報の更新に失敗しました: {res_update.text}")
                    st.write("レスポンスコード:", res_update.status_code)

        elif delete_button:
            url_delete = f'http://127.0.0.1:8000/api/users/{selected_user_id}'
            res_delete = requests.delete(url_delete)

            if res_delete.status_code == 200:
                message = res_delete.json().get("message")
                st.success(message)
            else:
                st.error(f"ユーザーの削除に失敗しました: {res_delete.text}")
                st.write("レスポンスコード:", res_delete.status_code)