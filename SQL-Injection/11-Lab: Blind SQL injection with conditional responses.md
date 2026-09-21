# 📝 Lab: Blind SQL Injection with Conditional Responses

- **Vulnerability:** SQL Injection
- **Difficulty:** PRACTITIONER
- **Objective:** Log in as the `administrator` user.
- **Description:** This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics and performs a SQL query containing the value of the submitted cookie.

The results of the SQL query are not returned directly, and no database errors are displayed. However, the application shows a **"Welcome back!"** message whenever the query returns at least one row.

The database contains a `users` table with `username` and `password` columns. The goal is to exploit the blind SQL injection vulnerability to extract the password of the `administrator` user and then log in.

---

## 🛠️ Tools Used

- Browser (FoxyProxy)
- Burp Suite
- Python

---

## 🐾 Steps to Reproduce

1. Open the lab homepage and intercept the request using **Burp Suite**.
2. Go to **Proxy → HTTP History**, right-click the request, and send it to **Repeater** (`Ctrl + R`).
3. Locate the `TrackingId` cookie and test the injection point using:

   ```sql
   ' AND '1'='1
   ```

   If the page still shows **"Welcome back!"**, the condition is true.

4. Try the following payload:

   ```sql
   ' AND '1'='2
   ```

   The **"Welcome back!"** message should disappear because the condition is false.

5. Since the application behaves differently depending on the query result, the cookie is vulnerable to **Blind SQL Injection (Conditional Responses)**.

6. To extract the administrator password, test individual characters using:

   ```sql
   ' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator')='a
   ```

   If **"Welcome back!"** appears, the first character of the password is `a`. If not, continue testing other characters.

7. Repeat the process for each character position of the password until the entire password is recovered.

8. Because manually testing every character is time-consuming, I used a small Python brute-force tool to automate the process.

9. Run the tool and enter:

   - **URL**
     ```
     https://YOUR-LAB-ID.web-security-academy.net/
     ```

   - **Cookie Payload**
     ```sql
     (YOUR-TRACKING-ID)' AND (SELECT SUBSTRING(password,{i},1) FROM users WHERE username='administrator')='{char}
     ```

10. Wait for the script to recover the full administrator password.

11. Navigate to **My Account**, log in as:

    - Username: `administrator`
    - Password: `<recovered password>`

12. If successful, the lab will be marked as solved and the **"Lab Solved"** banner will appear.

---

## 🎯 Impact

This vulnerability allows an attacker to extract sensitive information from the database without receiving direct query results or error messages.

Possible impacts include:

- Unauthorized access to user accounts.
- Disclosure of administrator credentials.
- Full compromise of privileged accounts.
- Exposure of sensitive database information through inference techniques.
- Potential privilege escalation and complete application takeover if an administrator account is compromised.

Although the application does not display database contents directly, attackers can still retrieve data character-by-character by observing differences in application responses. This makes blind SQL injection just as dangerous as traditional SQL injection vulnerabilities.

---

## 💣 Payload

### 1. Confirming the Injection Point (True Condition)

```sql
' AND '1'='1
```

**Explanation:**

This payload appends a condition that always evaluates to **TRUE**. If the application still displays **"Welcome back!"**, it means the injected condition successfully affects the SQL query result.

---

### 2. Confirming the Injection Point (False Condition)

```sql
' AND '1'='2
```

**Explanation:**

This condition always evaluates to **FALSE**. If the **"Welcome back!"** message disappears, it confirms that application behavior changes based on the SQL query result, indicating a blind SQL injection vulnerability.

---

### 3. Testing a Single Password Character

```sql
' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator')='a
```

**Explanation:**

This payload checks whether the first character of the administrator's password is `a`.

- **TRUE** → "Welcome back!" is displayed.
- **FALSE** → "Welcome back!" is not displayed.

By changing both the character position and tested character, an attacker can recover the password one character at a time.

---

### 4. Generic Brute-Force Payload

```sql
' AND (SELECT SUBSTRING(password,{i},1) FROM users WHERE username='administrator')='{char}
```

**Parameters:**

- `{i}` = password character position (1, 2, 3, ...)
- `{char}` = character being tested (`a-z`, `0-9`, etc.)

**Example:**

```sql
' AND (SELECT SUBSTRING(password,5,1) FROM users WHERE username='administrator')='m
```

This checks whether the fifth character of the administrator password is `m`.

When automated with a script, the entire password can be extracted efficiently by testing all possible characters for every position.

---

## 🔗 Reference

For more SQL injection payloads and database-specific syntax, check out the **[PortSwigger SQL Injection Cheat Sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)**
