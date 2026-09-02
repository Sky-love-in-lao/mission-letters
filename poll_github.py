import time
import urllib.request
import urllib.parse
import json

client_id = "178c6fc778ccc68e1d6a"
device_code = "c6220a7034bef373325efced79c90f6ba2b9e0f0"

print("Polling for GitHub token...")
data_bytes = urllib.parse.urlencode({
    "client_id": client_id,
    "device_code": device_code,
    "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
}).encode("utf-8")

req = urllib.request.Request("https://github.com/login/oauth/access_token", data=data_bytes)
req.add_header("Accept", "application/json")

while True:
    try:
        with urllib.request.urlopen(req) as response:
            resp_data = json.loads(response.read().decode())
            if "access_token" in resp_data:
                print(f"\nSUCCESS! Token: {resp_data['access_token']}")
                with open("github_token.txt", "w") as f:
                    f.write(resp_data["access_token"])
                break
            elif resp_data.get("error") == "authorization_pending":
                print(".", end="", flush=True)
                time.sleep(5)
            else:
                print(f"\nError: {resp_data}")
                break
    except Exception as e:
        print(f"\nRequest failed: {e}")
        time.sleep(5)
