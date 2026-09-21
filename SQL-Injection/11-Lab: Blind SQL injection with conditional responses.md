# 📝 Lab: Blind SQL injection with conditional responses

- **Vulnerability:** SQL Injection.
- **Difficulty:** PRACTITIONER.
- **Objective:** log in as the administrator user.
- **Description:** This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.
The results of the SQL query are not returned, and no error messages are displayed. But the application includes a Welcome back message in the page if the query returns any rows.
The database contains a different table called users, with columns called username and password. You need to exploit the blind SQL injection vulnerability to find out the password of the administrator user.
To solve the lab, log in as the administrator user.

---

## 🛠️ Tools Used
- Browser (FoxyProxy)
- Burp Suite
- Python

---

## 🐾 Steps to Reproduce
1. Pergi ke halaman utama, buka *Burpsuite -> Proxy -> HTTP History -> Ctrl+R -> Repeater*.
2. Di *Repeater*. Cookie adalah tempat kita injeksi payload. Coba injeksi dengan payload `' AND '1'='1` di samping value variable **TrackingId**
dan pastikan respon memberikan tanda *Welcome back!*. Coba juga menngunakan `' AND '1'='2` dan periksa respone. Dengan hal ini kita dapat memastikan bahwa ada kerentanan **Blind SQLi**.
3. Karena sudah di beri tau table dan kolomnya, kita bisa langsung injeksi menggunakan `' AND (SELECT SUBSTRING(password, 1, 1) FROM users WHERE username='administrator')='a` sudah di pastikan respon tidak akan mengirimkan *Welcome back!* atau mungkin benar jika huruf awal password berawalan **a**.
4. Di sini kita perlu menggunakan teknik **Brute Force**. Di karenakan *Burpsuite intruder (community)* cukup lambat, saya akan menggunakan [tool](https://github.com/noata5505/Portswigger-Lab-Burp-Community/blob/main/SQL-Injection/11_Bruteforce_Tool.py) yang saya buat sendiri.


---

## 🎯 Impact

---

## 💣 Payload
```sql

```
## 🔗 Reference:
For more powerful payloads, check out the [PortSwigger SQLi Cheat Sheet.](https://portswigger.net/web-security/sql-injection/cheat-sheet)
