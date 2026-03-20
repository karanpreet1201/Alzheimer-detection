import urllib.request
import urllib.error

req = urllib.request.Request("http://localhost:8000/register", data=b'{"username":"testuserxyz123","email":"test1234xyz@example.com","password":"testpass"}', headers={"Content-Type": "application/json"})
try:
    resp = urllib.request.urlopen(req)
    print("Success:", resp.read().decode())
except urllib.error.HTTPError as e:
    print('HTTPError:', e.code)
    try:
        print("Body:", e.read().decode())
    except Exception as ex:
        print("Could not read body:", ex)
except Exception as e:
    print("Other Error:", e)
