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



---

## 💣 Payload

---

## 🎯 Impact

---

## 🔗 Reference

For more SQL injection payloads and database-specific syntax, check out the **[PortSwigger SQL Injection Cheat Sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)**
