import requests

BASE_URL = "http://127.0.0.1:8000/api"

def _request(method, endpoint, data=None):
    """共通HTTPリクエスト関数"""
    url = f"{BASE_URL}/{endpoint}"
    try:
        if method == "GET":
            res = requests.get(url)
        elif method == "POST":
            print(data)
            res = requests.post(url, json=data)
        elif method == "PUT":
            res = requests.put(url, json=data)
        elif method == "DELETE":
            res = requests.delete(url)
        else:
            return {"status_code": 400, "data": {"error": "Invalid HTTP method"}}

        try:
            body = res.json()  # JSONが返る場合
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
    return _request("POST", endpoint, data)

def put(endpoint, data, resource_id=None):
    """PUTメソッド (IDありでもOK)"""
    url = f"{endpoint}/{resource_id}" if resource_id else endpoint
    return _request("PUT", url, data)

def delete(endpoint, resource_id=None):
    """DELETEメソッド (IDありでもOK)"""
    url = f"{endpoint}/{resource_id}" if resource_id else endpoint
    return _request("DELETE", url)
