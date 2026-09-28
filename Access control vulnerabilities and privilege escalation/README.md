# 🔐 Access Control Vulnerabilities & Privilege Escalation

> 🎯 **What's Access Control?**  
Access control is the process of making sure users can only access the data, features, and actions they're actually allowed to use.

When access checks are missing, weak, or implemented incorrectly, attackers may gain access to resources they shouldn't be able to see or perform actions they shouldn't be able to perform.

This category includes vulnerabilities such as:

- Insecure Direct Object Reference (IDOR)
- Missing Authorization
- Forced Browsing
- Horizontal Privilege Escalation
- Vertical Privilege Escalation
- Broken Role Validation
- Insecure API Authorization

According to OWASP, **Broken Access Control** remains one of the most common and impactful web security issues.

---

## 🧰 Security Stack
<p align="left">
  <img src="https://img.shields.io/badge/Web_Security-6f42c1?style=for-the-badge" alt="Web Security"/>
  <img src="https://img.shields.io/badge/Broken_Access_Control-b91c1c?style=for-the-badge" alt="Broken Accessge/Privilege_Escalation-dc2626?style=for-the-badge"
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

The content is intended to help developers, students, security researchers, and bug bounty hunters understand how access control vulnerabilities work and how to prevent them.

## 📌 Important

- **DO NOT** access data that doesn't belong to you
- **DO NOT** test systems without permission
- **ALWAYS** use legal labs and safe environments
- **FOLLOW** applicable laws and regulations

## ✅ Responsible Use

| ✅ Do | ❌ Don't |
|--------|----------|
| Learn secure coding | Access other people's accounts |
| Test in legal labs | Attack production systems |
| Report findings responsibly | Steal sensitive data |
| Improve application security | Sell obtained information |

## ⚖️ Legal Notice

Unauthorized access to systems and user data is illegal in many jurisdictions.

Possible consequences include:

- Criminal charges
- Financial penalties
- Imprisonment
- Civil lawsuits

**You are fully responsible for your own actions.**

---

# 📚 Table of Contents

- What Is Access Control?
- Common Types of Access Control Vulnerabilities
- Horizontal Privilege Escalation
- Vertical Privilege Escalation
- IDOR
- Real-World Examples
- Impact
- Where These Issues Commonly Appear
- Detection & Testing
- Prevention & Mitigation
- Security Checklist
- Learning Resources

---

# 🔍 What Is Access Control?

Access control determines **who can access what** inside an application.

A secure application should verify:

1. Who the user is (Authentication)
2. What the user is allowed to do (Authorization)

Many applications successfully authenticate users but fail to properly authorize requests.

This can lead to unauthorized access to:

- User profiles
- Orders
- Documents
- Payment information
- Admin functionality
- Internal APIs
- Company data

---

# 🚨 Common Types of Access Control Vulnerabilities

## 1️⃣ IDOR (Insecure Direct Object Reference)

An application directly uses user-supplied identifiers without properly checking ownership.

Example:

```http
GET /profile?id=1001
```

Changing it to:

```http
GET /profile?id=1002
```

may expose another user's profile.

---

## 2️⃣ Horizontal Privilege Escalation

A user gains access to another user with the same privilege level.

Example:

```text
User A → accesses User B's data
```

The attacker doesn't become an admin.

They simply access data belonging to someone else.

---

## 3️⃣ Vertical Privilege Escalation

A lower-privileged user gains access to higher-privileged functionality.

Example:

```text
User → Admin
```

Attempting to access:

```http
/admin
```

or:

```http
POST /admin/delete-user
```

without proper permissions.

---

## 4️⃣ Forced Browsing

Sensitive pages are accessible simply by knowing the URL.

Example:

```http
/admin/dashboard
```

Even if the link is hidden from normal users, the page may still be reachable directly.

---

## 5️⃣ Missing Function-Level Authorization

The backend never checks whether a user is allowed to perform an action.

Example:

```http
POST /api/delete-account
```

The endpoint works regardless of user role.

---

# ⚙️ How These Vulnerabilities Happen

Applications often trust data sent by the client.

Example of vulnerable code:

```python
@app.route('/profile')
def profile():
    user_id = request.args.get("id")
    return get_user_profile(user_id)
```

What's missing?

```python
if user_id != current_user.id:
    return "Forbidden", 403
```

Without authorization checks, attackers can manipulate parameters and access data they shouldn't see.

---

# 🧪 Example Scenarios

## User Profile Access

Normal request:

```http
GET /user/123
```

Modified request:

```http
GET /user/124
```

If another user's profile is returned, access control is broken.

---

## Invoice Access

Normal request:

```http
GET /invoice/1001
```

Modified request:

```http
GET /invoice/1002
```

If the invoice belongs to another customer and is still accessible, authorization is missing.

---

## Admin Functionality

Normal admin request:

```http
POST /admin/create-user
```

If a regular user can perform the same action, that's vertical privilege escalation.

---

## API Authorization

Request:

```http
GET /api/orders/1001
```

Changing the identifier:

```http
GET /api/orders/1002
```

should never return another user's confidential data.

---

# 💀 Impact

Access control flaws can lead to:

- 🔓 Unauthorized account access
- 📄 Sensitive document exposure
- 💳 Payment data disclosure
- 📧 User information leaks
- ⚙️ Unauthorized actions
- 👤 Account takeover scenarios
- 🏢 Corporate data breaches
- 🛠 Administrative function abuse

In many real-world incidents, broken access control causes some of the most severe security impacts because attackers can directly access legitimate application data.

---

# 🎯 Where These Issues Are Commonly Found

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

## Invoice Systems

```http
/invoice/5001
```

## Cloud Storage

```http
/storage/file123.pdf
```

## Admin Panels

```http
/admin
```

## Internal Management Tools

```http
/manage/users
```

---

# 🕵️ Detection & Testing

## Manual Testing

Look for identifiers such as:

```http
?id=1001
```

Try different values:

```http
?id=1002
```

```http
?id=9999
```

Then check:

- Does the response change?
- Can you see another user's data?
- Is sensitive information exposed?
- Can restricted actions be performed?

---

## Authorization Testing

Test whether permissions are enforced for:

- User IDs
- Account IDs
- Order IDs
- UUIDs
- Document IDs
- Admin functionality
- Sensitive actions

---

## Tools Commonly Used

| Tool | Purpose |
|--------|----------|
| Burp Suite | Intercept and modify requests |
| OWASP ZAP | Proxy and testing |
| Postman | API testing |
| Insomnia | REST API testing |
| Caido | Modern web testing |
| FFUF | Discover endpoints and parameters |

---

# 🛡️ Prevention & Mitigation

## ✅ 1. Always Perform Authorization Checks

Never trust data coming from the client.

Verify access permissions on every request.

Example:

```python
if requested_user_id != current_user.id:
    return "Forbidden", 403
```

---

## ✅ 2. Implement Role-Based Access Control (RBAC)

Example:

```text
Admin → Can access all records
User  → Can only access their own records
```

---

## ✅ 3. Verify Resource Ownership

Always confirm ownership before returning sensitive data.

Example:

```sql
SELECT * FROM invoices
WHERE invoice_id = ?
AND owner_id = ?
```

---

## ✅ 4. Use Secure Object References

Instead of sequential IDs:

```text
1
2
3
4
5
```

Use UUIDs:

```text
6fbeda77-cc6d-4b18-bd61-f2ec803f55bc
```

This won't fix authorization issues, but it makes object enumeration more difficult.

---

## ✅ 5. Apply Least Privilege

Principle:

```text
Users should have only the minimum permissions necessary.
```

---

## ✅ 6. Log and Monitor Suspicious Activity

Watch for behavior such as:

```text
/user/1001
/user/1002
/user/1003
/user/1004
```

Sequential access attempts may indicate object enumeration or privilege escalation attempts.

---

## ✅ 7. Deny By Default

If permission cannot be verified:

```text
Deny access.
```

Never assume access should be allowed.

---

# ❌ Common Developer Mistakes

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

```javascript
// Vulnerable
if(user.loggedIn){
   return adminPanel()
}
```

The problem is that these examples perform actions without validating authorization properly.

---

# ✅ Access Control Security Checklist

- [ ] Every endpoint performs authorization checks
- [ ] Ownership validation is enforced
- [ ] RBAC or ABAC is implemented
- [ ] Sensitive actions require permission validation
- [ ] APIs verify user context
- [ ] Hidden form fields are not trusted
- [ ] Client-side checks are not relied upon
- [ ] Audit logging is enabled
- [ ] Security testing is performed regularly
- [ ] Broken Access Control scenarios are included in reviews

---

# 📚 Learning Resources

## Official References

- OWASP Broken Access Control
- OWASP Testing Guide
- OWASP API Security Top 10
- PortSwigger Web Security Academy

## Safe Practice Platforms

- PortSwigger Web Security Academy
- DVWA
- OWASP Juice Shop
- Hack The Box
- TryHackMe

---

# 🎯 Quick Reference

| Scenario | Recommended Control |
|-----------|--------------------|
| User Profile | Ownership Validation |
| API Endpoint | Authorization Check |
| Document Download | Access Validation |
| Invoice Access | Ownership Verification |
| Admin Function | Role Validation |
| Mobile API | User Context Validation |
| Sensitive Actions | Permission Checks |

---

# 📝 Final Thoughts

Access control vulnerabilities are often simple mistakes with serious consequences.

The biggest lesson is:

1. Never trust identifiers sent by clients
2. Always verify authorization on the server
3. Check ownership for every sensitive resource
4. Follow the principle of least privilege
5. Test access control regularly
6. Assume attackers will manipulate requests

🔒 **Authentication answers: "Who are you?"**

🛡️ **Authorization answers: "What are you allowed to do?"**

Most privilege escalation and access control vulnerabilities happen when applications handle authentication correctly but forget to enforce authorization consistently.

---

<div align="center">

### 🛡️ Learn Security Responsibly

Build secure applications, test ethically, and always respect user privacy.

Made with ❤️ for Security Researchers & Developers

</div>
