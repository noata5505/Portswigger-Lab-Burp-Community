# 📝 Lab: Blind SQL Injection with Time Delays

* **Vulnerability:** Blind SQL Injection (Time-Based)
* **Difficulty:** PRACTITIONER
* **Objective:** Make the server response delay by 10 seconds.

> **Description**
>
> This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics and performs a SQL query using the value of the submitted cookie.
>
> The results of the query are not returned, and the application's response remains the same whether the query succeeds, fails, or returns data. However, because the SQL query is executed synchronously, it is possible to trigger time delays and use those delays as evidence of successful SQL injection.
>
> To solve the lab, exploit the SQL injection vulnerability and force the database to pause execution for 10 seconds.

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

Locate the following cookie in the request:

```http
TrackingId=<value>
```

The `TrackingId` cookie is the vulnerable parameter that will be used for the injection.

---

### 3. Trigger a Time Delay

Replace the value of `TrackingId` with the following payload:

```sql
'||pg_sleep(10)--
```

Example:

```http
Cookie: TrackingId='||pg_sleep(10)--; session=<session_id>
```

This payload causes PostgreSQL to execute the `pg_sleep()` function, which pauses query execution for 10 seconds.

---

### 4. Send the Request

Click **Send** in Burp Repeater and observe the server response time.

Instead of receiving an immediate response, the server will take approximately **10 seconds** to respond.

This confirms that the input is being executed as part of the SQL query.

---

### 5. Verify the Result

Once the delayed response is observed, the lab objective is completed.

The **"Lab Solved"** banner will appear.

---

## 💣 Payload

### Basic Time-Based Payload

```sql
'||pg_sleep(10)--
```

**Purpose:**

* Calls PostgreSQL's `pg_sleep()` function.
* Forces the database to pause execution for 10 seconds.
* Confirms that SQL injection is possible even when no data is reflected in the response.
* Demonstrates a classic **time-based blind SQL injection** technique.

---

### Example in Cookie

```http
Cookie: TrackingId='||pg_sleep(10)--; session=<session_id>
```

**Expected Result:**

```text
Response delayed by approximately 10 seconds.
```

---

## 🎯 Impact

Although this lab only requires triggering a response delay, the vulnerability is much more serious in a real-world application.

An attacker could:

* Confirm the presence of a blind SQL injection vulnerability.
* Extract sensitive database information without seeing query results directly.
* Enumerate database names, table names, and column names.
* Retrieve usernames and passwords one character at a time using conditional delays.
* Bypass security controls that hide database errors.
* Potentially gain unauthorized access to user or administrator accounts.
* Escalate the attack to full database compromise depending on database permissions.

**Risk:** High

**Attack Complexity:** Low

**Privileges Required:** None

**Potential Business Impact:**

A successful attacker could silently extract sensitive information from the database without generating visible errors, making detection significantly more difficult than traditional SQL injection attacks.

---

## 🔗 Reference

For more SQL injection payloads and database-specific syntax, check out the **[PortSwigger SQL Injection Cheat Sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)**
