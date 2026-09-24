# 📝 Lab: Blind SQL injection with conditional errors

**Vulnerability:** SQL Injection  
**Difficulty:** PRACTITIONER  
**Objective:** Log in as the `administrator` user.  

> **Description:** This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie. The results of the SQL query are not returned, and the application does not respond any differently based on whether the query returns any rows. If the SQL query causes an error, then the application returns a custom error message. The database contains a different table called users, with columns called username and password. You need to exploit the blind SQL injection vulnerability to find out the password of the administrator user.  
> To solve the lab, log in as the administrator user.

---

## 🛠️ Tools Used

- Browser (FoxyProxy)
- Burp Suite
- Python

---

## 🐾 Steps to Reproduce

1. **Capture the Request:** Fire up your browser, open the lab homepage, and make sure your traffic is routed through **Burp Suite**.
2. **Send to Repeater:** Head over to **Proxy → HTTP History**, grab the main request, right-click it, and send it to **Repeater** (`Ctrl + R`).
3. **Identify the Database Type:** The vulnerable entry point is the `TrackingId` cookie. Let's test the database flavor by injecting `'||(SELECT '')||'`. If you get a **200 OK**, it's not Oracle. If you get a **500 Internal Server Error**, try `'||(SELECT '' FROM dual)||'` to confirm it's **Oracle SQL**.
4. **Trigger a Conditional Error:** Confirm the injection point actually processes logic by forcing a division-by-zero error conditionally. Use a payload like `'||(SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM DUAL)||'`. If it throws a 500 error, our conditional trigger works like a charm!
5. **Craft the Data Extraction Payload:** Knowing the database schema (`users` table with `username` and `password` columns), target the admin's password character by character with a query like:  
   `'||(SELECT CASE WHEN SUBSTR(password, 1, 1)='a' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'`
6. **Automate the Guessing Game:** Since guessing manually character-by-character takes forever, we can automate it using **Burp Intruder** or write a quick **Python script** to brute-force the password length and characters.
7. **Run the Exploit Script:** Fire up your custom Python script:
   - Provide your lab URL: `https://(YOUR-ID).web-security-academy.net/`
   - Plug in the tracking cookie payload structure containing our logic loop.
8. **Log In and Win:** Wait for the script to churn out the full admin password. Take those credentials back to the login page, sign in as `administrator`, and boom—lab solved! 🎉

---

## 🎯 Impact

If an attacker successfully exploits this vulnerability, they can:
- Silently extract sensitive data from the database (such as user credentials, PII, or internal configurations) character-by-character, even when the application never directly displays query results.
- Compromise high-privileged accounts like the `administrator`, leading to full application takeover and unauthorized access to restricted features or sensitive user data.

---

## 💣 Payload

Here are the key payloads used throughout this lab for Oracle SQL error-based extraction:

* **Database Type Detection (Non-Oracle Check):**
  ```sql
  '||(SELECT '')||'
