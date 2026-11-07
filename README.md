# TrustVault – Secure Document Sharing with Audit Trail

## 1. Project Overview

TrustVault is a secure document-sharing web application developed using Python and Django. It allows users to upload, manage, view, download, edit, and share documents with other users.

The application provides role-based access control and permission management. It also maintains audit logs to track document-related activities, including uploads, views, downloads, edits, deletions, and permission changes.

## 2. Problem Statement

Sharing confidential documents without proper access control can lead to unauthorized access and misuse. It can also be difficult to track who accessed or modified a document.

TrustVault addresses these problems through controlled document sharing, user permissions, and activity tracking.

## 3. Objectives

- Provide secure user registration and login.
- Allow users to upload and manage documents.
- Support document sharing between users.
- Provide Read and Edit permissions.
- Prevent unauthorized document access.
- Maintain an audit trail of document activities.
- Provide an Admin dashboard for monitoring activities.

## 4. Main Modules

1. **Authentication and Role Management**
   - User registration and login.
   - Owner, Viewer, and Admin roles.

2. **Document Upload and Management**
   - Upload documents.
   - View, search, filter, edit, download, and delete documents.

3. **Document Sharing and Permissions**
   - Share documents with other users.
   - Grant Read or Edit permissions.
   - Revoke previously granted permissions.

4. **Secure Document Access**
   - Allow document access based on ownership and permissions.
   - Restrict unauthorized viewing and downloading.
   - Prevent unauthorized editing and deletion.

5. **Audit Logging and Monitoring**
   - Record document activities.
   - Track the user, document, action, outcome, and timestamp.
   - Provide an Audit Dashboard.

## 5. Technologies Used

- Programming Language: Python
- Backend Framework: Django
- Frontend: HTML, CSS, Django Templates
- Local Database: SQLite
- Deployment Database: PostgreSQL
- Web Server: Gunicorn
- Static File Handling: WhiteNoise
- Version Control: Git and GitHub
- Deployment Platform: Render

## 6. User Roles

- **Owner:** Uploads and manages documents, shares documents, and controls permissions.
- **Viewer:** Accesses shared documents according to the permissions granted.
- **Admin:** Monitors application activities through the Admin Audit Dashboard.

## 7. Key Features

- User registration and authentication.
- Document upload and management.
- Document search and filtering.
- Read and Edit permission management.
- Document viewing and downloading.
- Permission revocation.
- Unauthorized access protection.
- Audit logging and monitoring.

## 8. Audit Trail

TrustVault records activities such as:

- Document Uploaded
- Document Viewed
- Document Downloaded
- Document Edited
- Document Deleted
- Permission Granted
- Permission Revoked

Each audit record can include the user, document, action, outcome, details, IP address, and timestamp.

## 9. Installation and Execution

### Prerequisites
- Python installed
- Visual Studio Code
- Git

### Steps

1. Clone the repository:

   `git clone https://github.com/Vardhinikamineni/TrustVault.git`

2. Open the project folder:

   `cd TrustVault`

3. Create a virtual environment:

   `python -m venv venv`

4. Activate the virtual environment on Windows:

   `venv\Scripts\activate`

5. Install dependencies:

   `pip install -r requirements.txt`

6. Apply database migrations:

   `python manage.py migrate`

7. Create an administrator account if required:

   `python manage.py createsuperuser`

8. Start the development server:

   `python manage.py runserver`

9. Open the application:

   `http://127.0.0.1:8000/`

## 10. Testing

The project test suite completed successfully:

- Total tests executed: 9
- Result: Passed
- Django system check: Passed

Functional testing included registration, login, document upload, sharing, permission management, document viewing, editing, downloading, deletion, and audit logging.

## 11. Deployment

**Live Application:** https://trustvault-u63f.onrender.com

**GitHub Repository:** https://github.com/Vardhinikamineni/TrustVault

The application is deployed on Render using Django, Gunicorn, and PostgreSQL.

## 12. Limitations

- The application uses Render's free hosting plan.
- Uploaded files on the current free deployment may not persist after redeployment or service restarts.
- The free PostgreSQL database has an expiry date.
- Persistent document storage requires an external storage service or suitable persistent disk.

## 13. Future Enhancements

- Add cloud-based persistent document storage.
- Implement stronger file encryption.
- Add email notifications for document sharing.
- Improve audit log reporting and export options.
- Add multi-factor authentication.

## 14. Conclusion

TrustVault provides a document-sharing platform with role-based access control, permission management, and audit logging. It helps users manage shared documents and monitor important document activities while restricting unauthorized access.