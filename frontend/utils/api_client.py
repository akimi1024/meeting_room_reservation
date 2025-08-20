import requests
from streamlit import session_state

BASE_URL = "http://backend:8000/api"

def _headers():
    h = {"Content-Type": "application/json"}
    token = session_state.get("token")
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h

def _request(method, endpoint, data=None):
    url = f"{BASE_URL}/{endpoint}"
    try:
        if method == "GET":
            res = requests.get(url, headers=_headers())
        elif method == "POST":
            res = requests.post(url, json=data, headers=_headers())
        elif method == "PUT":
            res = requests.put(url, json=data, headers=_headers())
        elif method == "DELETE":
            res = requests.delete(url, headers=_headers())
        else:
            return {"status_code": 400, "data": {"error": "Invalid HTTP method"}}

        # 共通エラーハンドリング（期限切れなど）
        if res.status_code == 401:
            session_state.clear()
            return {"status_code": 401, "data": {"detail": "認証切れ"}}

        try:
            body = res.json()
        except ValueError:
            body = {}

        return {
            "status_code": res.status_code,
            "data": body
        }

    except requests.RequestException as e:
        return {
            "status_code": 500,
            "data": {"error": f"リクエスト失敗: {str(e)}"}
        }


def get(endpoint):
    return _request("GET", endpoint)

def post(endpoint, data):
    print(f"requestUrl: {endpoint}")
    return _request("POST", endpoint, data)

def put(endpoint, data, resource_id=None):
    """PUTメソッド (IDありでもOK)"""
    url = f"{endpoint}/{resource_id}" if resource_id else endpoint
    return _request("PUT", url, data)

def delete(endpoint, resource_id=None):
    """DELETEメソッド (IDありでもOK)"""
    url = f"{endpoint}/{resource_id}" if resource_id else endpoint
    return _request("DELETE", url)