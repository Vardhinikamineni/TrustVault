# TrustVault
### Secure Document Sharing with Access Control and Audit Trail

## 1. Project Overview
TrustVault is a secure document-sharing web application developed using Python and Django. It allows users to upload, manage, share, view, and download documents with controlled permissions.

The system records document activities in an Admin Audit Dashboard so administrators can monitor user actions.

## 2. Problem Statement
Sharing documents without proper access control can lead to unauthorized viewing, editing, and downloading. TrustVault addresses this problem through role-based permissions and activity tracking.

## 3. Objectives
- Provide secure user authentication.
- Allow users to upload and manage documents.
- Share documents with specific users.
- Provide Read and Edit permissions.
- Prevent unauthorized document access.
- Maintain an audit trail of document activities.

## 4. Key Features
- User registration and login.
- Document upload and management.
- Document search and category filters.
- Read and Edit permissions.
- Permission granting and revocation.
- Secure document viewing and downloading.
- Unauthorized access prevention.
- Admin Audit Dashboard.
- Activity tracking with IP address and timestamp.

## 5. Technologies Used
- Programming Language: Python
- Framework: Django
- Database: SQLite
- Frontend: HTML and CSS
- Development Tool: Visual Studio Code

## 6. User Roles

### Admin
- Monitor document activities.
- View audit records.

### Owner
- Upload and manage documents.
- Share documents with other users.
- Grant or revoke permissions.

### Viewer
- View and download shared documents with Read permission.
- Edit documents only when Edit permission is granted.

## 7. Security Features
- Authentication-based access.
- Permission-based document access.
- Unauthorized edit and delete prevention.
- File type and size validation.
- Private document storage.
- Audit logging of successful and denied activities.

## 8. Audit Trail
TrustVault records activities such as:
- Document uploaded.
- Document viewed.
- Document downloaded.
- Document edited.
- Permission granted.
- Permission revoked.
- Unauthorized access attempts.

Audit records include the username, document, action, outcome, IP address, and date/time.

## 9. Installation and Execution

1. Install Python.
2. Open the TrustVault project folder in VS Code.
3. Open the terminal.
4. Activate the virtual environment:

```bash
venv\Scripts\activate
```

5. Install Django:

```bash
pip install django
```

6. Apply database migrations:

```bash
python manage.py migrate
```

7. Start the development server:

```bash
python manage.py runserver
```

8. Open the application:

http://127.0.0.1:8000/

## 10. Testing
The following test cases were performed:

- User login and authentication.
- Document upload and search.
- Document sharing.
- Read permission validation.
- Edit permission validation.
- Unauthorized edit prevention.
- Unauthorized delete prevention.
- Document download.
- Permission revocation.
- Audit trail verification.
- Document view tracking.

## 11. Future Enhancements
- Tamper-evident audit logging.
- Email notifications.
- Two-factor authentication.
- Cloud deployment.
- Advanced security monitoring.

## 12. Conclusion
TrustVault provides a document-sharing platform with access control and activity monitoring. It helps protect shared documents and provides administrators with visibility into document access activities.