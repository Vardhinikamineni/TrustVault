
from django.urls import path
from . import views

urlpatterns = [
    # HOME
    path("", views.home, name="home"),

    # AUTHENTICATION
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),

    # DASHBOARD
    path("dashboard/", views.dashboard, name="dashboard"),

    # DOCUMENT UPLOAD AND MANAGEMENT
    path("upload/", views.upload_document, name="upload"),
    path("my-documents/", views.my_documents, name="my_documents"),

    # DOCUMENT VIEW
    path(
        "view-document/<int:document_id>/",
        views.view_document,
        name="view_document"
    ),

    # DOCUMENT DOWNLOAD
    path(
        "download/<int:document_id>/",
        views.download_document,
        name="download_document"
    ),

    # DOCUMENT EDIT
    path(
        "edit-document/<int:document_id>/",
        views.edit_document,
        name="edit_document"
    ),

    # DOCUMENT DELETE
    path(
        "delete-document/<int:document_id>/",
        views.delete_document,
        name="delete_document"
    ),

    # DOCUMENT SHARING
    path(
        "share-document/",
        views.share_document,
        name="share_document"
    ),

    path(
        "shared-documents/",
        views.shared_documents,
        name="shared_documents"
    ),

    # REVOKE PERMISSION
    path(
        "revoke-permission/<int:permission_id>/",
        views.revoke_permission,
        name="revoke_permission"
    ),

    # ADMIN AUDIT DASHBOARD
    path(
        "audit-dashboard/",
        views.audit_dashboard,
        name="audit_dashboard"
    ),
]
