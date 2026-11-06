# TrustVault – Threat Model

## 1. Project Overview
TrustVault is a secure document-sharing application developed using Python, Django and SQLite. It allows users to upload, access and share documents with controlled permissions.

## 2. Assets to Protect
- User account credentials
- Uploaded documents
- Document metadata
- User roles and permissions
- Encryption keys and security settings
- Audit logs

## 3. Potential Security Threats

### 3.1 Unauthorized Access
An unauthorized user may try to access private documents.

### 3.2 Password Attacks
Attackers may attempt to guess or steal user passwords.

### 3.3 SQL Injection
Malicious SQL input may attempt to access or modify database information.

### 3.4 Cross-Site Request Forgery (CSRF)
An attacker may attempt to perform unwanted actions through an authenticated user's browser.

### 3.5 Malicious File Uploads
Users may upload invalid or harmful files.

### 3.6 Privilege Escalation
A viewer may attempt to obtain owner or administrator permissions.

### 3.7 Audit Log Tampering
An attacker may try to modify or delete audit records.

## 4. Security Measures
- User authentication and role-based access control.
- Secure password hashing.
- Document-level read and edit permissions.
- Owner-controlled permission granting and revocation.
- File type and upload validation.
- Private document storage.
- Django ORM to reduce SQL injection risks.
- CSRF protection.
- Audit logging of important activities.

## 5. Risk Mitigation
- Verify user permissions before document access.
- Prevent unauthorized downloads, edits and deletions.
- Validate uploaded files.
- Restrict access to administrative functions.
- Protect audit records against unauthorized modification.
- Run automated security tests regularly.

## 6. Conclusion
TrustVault aims to provide secure document sharing through authentication, access control, file validation and audit logging. Security testing and continuous improvements help reduce risks and protect confidential documents.