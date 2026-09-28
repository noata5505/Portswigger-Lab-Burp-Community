# 🔓 Insecure Direct Object Reference (IDOR)

> 🎯 **What's IDOR?** Insecure Direct Object Reference (IDOR) happens when an application gives direct access to a resource (data, files, records, etc.) based on user-supplied input without properly checking whether the user is actually allowed to access it.

IDOR is one of the most common examples of **Broken Access Control**, and it continues to show up in modern web apps, APIs, and mobile applications.

---

## 🧰 Security Stack

<p align="left">
  <img src="https://img.shields.io/badge/Web_Security-6f42c1?style=for-the-badge" alt="Web Security"/>
  <img src="https://img.shields.io/badge/IDOR-Broken_Access_Control-b91c1c?style=for-the-badge" alt="IDOR"/>
  <img src="https://img.shields.io/badge/OWASP-000000?style=for-the-badge&logo=owasp&logoColor=white" alt="OWASP"/>
  <img src="https://img.shields.io/badge/Burp_Suite-ff6633?style=for-the-badge&logo=burpsuite&logoColor=white" alt="Burp Suite"/>
  <img src="https://img.shields.io/badge/OWASP_ZAP-00549e?style=for-the-badge&logo=owasp&logoColor=white" alt="OWASP ZAP"/>
  <img src="https://img.shields.io/badge/API_Security-0ea5e9?style=for-the-badge" alt="API Security"/>
  <img src="https://img.shields.io/badge/Access_Control-16a34a?style=for-the-badge" alt="Access Control"/>
  <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" alt="Linux"/>
  <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/>
</p>

---

# ⚠️ Disclaimer

> **This repository is for EDUCATIONAL PURPOSES ONLY.** 📚

This content is intended to help developers, students, security researchers, and bug bounty hunters understand how IDOR vulnerabilities work and, more importantly, how to prevent them.

## 📌 Important

- **DO NOT** access data that doesn't belong to you
- **DO NOT** test systems without permission
- **ALWAYS** practice in a legal and controlled environment
- **FOLLOW** local laws and regulations regarding cybersecurity

## ✅ Responsible Use

| ✅ Do | ❌ Don't |
|--------|----------|
| Learn secure coding | Access other people's accounts |
| Practice in legal labs | Attack production systems |
| Report bugs responsibly | Steal user data |
| Improve application security | Abuse vulnerabilities for profit |

## ⚖️ Legal Notice

Unauthorized access to computer systems or user data is illegal in many countries.

Possible consequences include:

- Criminal charges
- Financial penalties
- Jail time
- Civil lawsuits

**You are fully responsible for your own actions.**

---

# 📚 Table of Contents

- [What is IDOR?](#-what-does-it-work
- #-simple-examples
- #-impact-of-idor
- #-where-idor-is-commonly-found
- #-detection--testing
- [Mitigation &-prevention
- #-security-checklist
- [Resources & Learning](#-resourceshat is IDOR?

IDOR (**Insecure Direct Object Reference**) is a vulnerability that occurs when an application directly references objects such as:

- User IDs
- Order numbers
- Documents
- Files
- API resources

without verifying whether the current user is allowed to access them.

## A Simple Scenario

Imagine you're logged into a website and access:

```http
GET /profile?id=1001
```

The server returns your profile information.

Now you change the request to:

```http
GET /profile?id=1002
```

If the application returns another user's profile without checking permissions...

🚨 Congratulations, you've found an IDOR vulnerability.

---

# ⚙️ How Does It Work?

Many applications trust user input a little too much.

Here's an example of vulnerable backend code:

```python
@app.route('/profile')
def profile():
    user_id = request.args.get("id")
    return get_user_profile(user_id)
```

The problem?

- The server retrieves data based on the supplied ID
- No ownership verification is performed
- Any authenticated user might access someone else's data

Sometimes changing a single number is enough.

---

# 🧪 Simple Examples

## 1️⃣ User Profile IDOR

### Normal Request

```http
GET /user/123
```

Response:

```json
{
  "name": "John",
  "email": "john@example.com"
}
```

### Modified Request

```http
GET /user/124
```

Response:

```json
{
  "name": "Alice",
  "email": "alice@example.com"
}
```

Since the application doesn't verify ownership, another user's information becomes accessible.

---

## 2️⃣ Document Download IDOR

A user receives:

```http
/download?file=invoice_123.pdf
```

Changing it to:

```http
/download?file=invoice_124.pdf
```

If another user's invoice is downloaded successfully:

🚨 That's an IDOR vulnerability.

---

## 3️⃣ API IDOR

Request:

```http
GET /api/orders/1001
```

Response:

```json
{
  "order_id": 1001,
  "owner": "user1"
}
```

Changing the request:

```http
GET /api/orders/1002
```

If another user's order details are returned, the API is vulnerable to IDOR.

---

# 💀 Impact of IDOR

IDOR can lead to:

- 🔓 Unauthorized access to user data
- 📄 Sensitive document disclosure
- 💳 Payment information exposure
- 📧 Email address leakage
- ⚙️ Unauthorized data modification
- 👤 Account compromise
- 🏢 Corporate data breaches

In some cases, IDOR can be even more damaging than SQL Injection because it may provide direct access to sensitive information without requiring advanced exploitation techniques.

---

# 🎯 Where IDOR Is Commonly Found

## URL Parameters

```http
/profile?id=1001
```

## REST APIs

```http
/api/user/1001
```

## Mobile Applications

```http
/api/v2/account/1001
```

## File Downloads

```http
/download/document/1234
```

## Payment & Invoice Systems

```http
/invoice/5001
```

## Cloud Storage Resources

```http
/storage/file123.pdf
```

---

# 🕵️ Detection & Testing

## Manual Testing

Look for parameters like:

```http
?id=1001
```

Try changing them:

```http
?id=1002
```

or

```http
?id=9999
```

Then check:

- Does the data change?
- Can you access another user's information?
- Does the server expose sensitive content?

---

## API Testing

Common targets include:

- User IDs
- Account IDs
- Order IDs
- UUIDs
- Document IDs

Observe how the application responds when identifiers are changed.

---

## Common Tools

| Tool | Purpose |
|--------|---------|
| Burp Suite | Intercept and modify requests |
| OWASP ZAP | Proxy and security testing |
| Postman | API testing |
| Insomnia | REST API testing |
| Caido | Modern web testing |
| FFUF | Parameter discovery |

---

# 🛡️ Mitigation & Prevention

## ✅ 1. Enforce Authorization Checks

Authentication alone isn't enough.

Always verify whether the user owns or is allowed to access the requested resource.

Example:

```python
if requested_user_id != current_user.id:
    return "Forbidden", 403
```

---

## ✅ 2. Implement Proper Access Control

Use:

- RBAC (Role-Based Access Control)
- ABAC (Attribute-Based Access Control)

Example:

```text
Admin → Can access all records
User  → Can only access their own records
```

---

## ✅ 3. Use UUIDs

Avoid predictable IDs like:

```text
1
2
3
4
5
```

Prefer UUIDs:

```text
6fbeda77-cc6d-4b18-bd61-f2ec803f55bc
```

UUIDs are not a complete fix, but they make enumeration significantly harder.

---

## ✅ 4. Verify Resource Ownership

A safer query might look like this:

```sql
SELECT * FROM invoices
WHERE invoice_id = ?
AND owner_id = ?
```

Never return objects unless ownership has been validated.

---

## ✅ 5. Monitor Suspicious Activity

Watch for patterns such as:

```text
/user/1001
/user/1002
/user/1003
/user/1004
```

Sequential access attempts may indicate object enumeration or IDOR testing.

---

## ✅ 6. Follow the Principle of Least Privilege

Give users only the permissions they actually need.

Basic rule:

```text
Users should only access their own data.
```

---

# ❌ Common Mistakes

```python
# Vulnerable
user = User.query.get(request.args['id'])
```

```javascript
// Vulnerable
app.get('/invoice/:id', async(req,res)=>{
   const data = await Invoice.findByPk(req.params.id)
   res.json(data)
})
```

These examples retrieve objects directly without verifying ownership or permissions.

---

# ✅ IDOR Security Checklist

- [ ] Authorization checks exist on every endpoint
- [ ] API endpoints verify resource ownership
- [ ] Hidden fields are not trusted
- [ ] Client-supplied identifiers are validated
- [ ] RBAC or ABAC is implemented
- [ ] Audit logging is enabled
- [ ] Security reviews are performed regularly
- [ ] Developers understand Broken Access Control risks

---

# 📚 Resources & Learning

## Must Read

- OWASP Broken Access Control
- OWASP Testing Guide
- PortSwigger Web Security Academy IDOR
- OWASP API Security Top 10

## Practice Labs

- PortSwigger Web Security Academy
- DVWA
- OWASP Juice Shop
- Hack The Box
- TryHackMe

---

# 🎯 Quick Reference

| Scenario | Recommended Fix |
|-----------|-----------------|
| User Profile | Ownership Validation |
| API Endpoint | Authorization Checks |
| Invoice Access | RBAC + Ownership Verification |
| File Download | Access Control Validation |
| Admin Panel | Role Validation |
| Mobile API | User Context Validation |

---

# 📝 Final Thoughts

IDOR looks simple on the surface, which is exactly why it's so dangerous.

Most IDOR vulnerabilities don't exist because authentication is broken.

They exist because **authorization is missing**.

Remember:

1. Never trust IDs sent by the 
