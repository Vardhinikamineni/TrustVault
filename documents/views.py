
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.utils.dateparse import parse_date

from .models import Document, DocumentPermission, AuditLog

import os
import io
import zipfile


# HELPER: GET USER IP ADDRESS
def get_client_ip(request):
    return request.META.get("REMOTE_ADDR")


# HELPER: CREATE AUDIT LOG
def create_audit_log(request, action, outcome, document=None, details=""):
    AuditLog.objects.create(
        actor=request.user if request.user.is_authenticated else None,
        document=document,
        action=action,
        outcome=outcome,
        details=details,
        ip_address=get_client_ip(request)
    )


# HELPER: VALIDATE UPLOADED FILE CONTENT
def validate_uploaded_file(uploaded_file):
    allowed_extensions = {
        ".pdf", ".doc", ".docx", ".txt",
        ".png", ".jpg", ".jpeg"
    }

    extension = os.path.splitext(uploaded_file.name)[1].lower()

    if extension not in allowed_extensions:
        return "File type not allowed."

    if uploaded_file.size == 0:
        return "Empty files are not allowed."

    if uploaded_file.size > 5 * 1024 * 1024:
        return "File size must be below 5 MB."

    uploaded_file.seek(0)
    file_content = uploaded_file.read()
    uploaded_file.seek(0)

    if extension == ".pdf":
        if not file_content.startswith(b"%PDF-"):
            return "Invalid PDF file."

    elif extension == ".png":
        if not file_content.startswith(b"\x89PNG\r\n\x1a\n"):
            return "Invalid PNG image."

    elif extension in [".jpg", ".jpeg"]:
        if not file_content.startswith(b"\xff\xd8\xff"):
            return "Invalid JPEG image."

    elif extension == ".doc":
        if not file_content.startswith(
            b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"
        ):
            return "Invalid DOC file."

    elif extension == ".docx":
        try:
            with zipfile.ZipFile(io.BytesIO(file_content)) as archive:
                names = archive.namelist()

                if (
                    "[Content_Types].xml" not in names
                    or "word/document.xml" not in names
                ):
                    return "Invalid DOCX file."

        except (zipfile.BadZipFile, OSError):
            return "Invalid DOCX file."

    elif extension == ".txt":
        if b"\x00" in file_content:
            return "Invalid text file."

        try:
            file_content.decode("utf-8-sig")
        except UnicodeDecodeError:
            return "Text file must use UTF-8 encoding."

    return None


# HELPER: VALIDATE CATEGORY
def valid_category(category):
    return category in dict(Document.CATEGORY_CHOICES)


# HELPER: APPLY DOCUMENT SEARCH FILTERS
def filter_documents(documents, request):
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    upload_date = request.GET.get("date", "").strip()

    if query:
        documents = documents.filter(title__icontains=query)

    if category:
        if valid_category(category):
            documents = documents.filter(category=category)
        else:
            messages.error(request, "Invalid category selected.")

    if upload_date:
        valid_date = parse_date(upload_date)

        if valid_date:
            documents = documents.filter(uploaded_at__date=valid_date)
        else:
            messages.error(request, "Invalid date format.")

    return documents, query, category, upload_date


# HOME PAGE
def home(request):
    return render(request, "documents/home.html")


# USER REGISTRATION
def register(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password")
        role = request.POST.get("role")

        if not username or not email or not password:
            messages.error(request, "All fields are required.")
            return redirect("register")

        if role not in ["owner", "viewer"]:
            messages.error(request, "Please select a valid role.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.profile.role = role
        user.profile.save()

        messages.success(request, "Registration successful!")
        return redirect("login")

    return render(request, "documents/register.html")


# USER LOGIN
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        messages.error(request, "Invalid username or password.")

    return render(request, "documents/login.html")


# DASHBOARD
@login_required
def dashboard(request):
    role = request.user.profile.role

    if request.user.is_superuser:
        role = "admin"

    return render(
        request,
        "documents/dashboard.html",
        {"role": role}
    )


# USER LOGOUT
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")


# UPLOAD DOCUMENT
@login_required
def upload_document(request):
    if request.user.profile.role != "owner":
        messages.error(
            request,
            "Only document owners can upload files."
        )
        return redirect("dashboard")

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        category = request.POST.get("category", "general")
        uploaded_file = request.FILES.get("file")

        if not title or not uploaded_file:
            messages.error(
                request,
                "Please enter title and select a file."
            )
            return redirect("upload")

        if not valid_category(category):
            messages.error(request, "Invalid category.")
            return redirect("upload")

        validation_error = validate_uploaded_file(uploaded_file)

        if validation_error:
            messages.error(request, validation_error)
            return redirect("upload")

        document = Document.objects.create(
            title=title,
            category=category,
            file=uploaded_file,
            owner=request.user
        )

        create_audit_log(
            request,
            "upload",
            "success",
            document,
            "Document uploaded successfully."
        )

        messages.success(request, "Document uploaded successfully!")
        return redirect("upload")

    return render(
        request,
        "documents/upload.html",
        {"categories": Document.CATEGORY_CHOICES}
    )


# OWNER - MY DOCUMENTS AND SEARCH
@login_required
def my_documents(request):
    if request.user.profile.role != "owner":
        messages.error(request, "Access denied.")
        return redirect("dashboard")

    documents = Document.objects.filter(owner=request.user)

    documents, query, category, upload_date = filter_documents(
        documents,
        request
    )

    documents = documents.order_by("-uploaded_at")

    return render(
        request,
        "documents/my_documents.html",
        {
            "documents": documents,
            "query": query,
            "category": category,
            "upload_date": upload_date,
            "categories": Document.CATEGORY_CHOICES,
        }
    )


# SECURE DOCUMENT VIEW
@login_required
def view_document(request, document_id):
    document = Document.objects.filter(id=document_id).first()

    if document is None:
        create_audit_log(
            request,
            "view",
            "denied",
            details=f"Attempted viewing of missing document ID {document_id}."
        )
        raise Http404("Document not found")

    is_owner = document.owner_id == request.user.id

    has_permission = DocumentPermission.objects.filter(
        document=document,
        user=request.user,
        permission__in=["read", "edit"]
    ).exists()

    if not is_owner and not has_permission:
        create_audit_log(
            request,
            "view",
            "denied",
            document,
            "Unauthorized document viewing attempt."
        )
        raise Http404("Document not found")

    try:
        file_handle = document.file.open("rb")
    except (OSError, ValueError):
        create_audit_log(
            request,
            "view",
            "denied",
            document,
            "Document file could not be opened."
        )
        raise Http404("Document file not found")

    create_audit_log(
        request,
        "view",
        "success",
        document,
        "Document viewed successfully."
    )

    return FileResponse(
        file_handle,
        as_attachment=False,
        filename=os.path.basename(document.file.name)
    )


# SECURE DOCUMENT DOWNLOAD
@login_required
def download_document(request, document_id):
    document = Document.objects.filter(id=document_id).first()

    if document is None:
        create_audit_log(
            request,
            "download",
            "denied",
            details=f"Attempted download of missing document ID {document_id}."
        )
        raise Http404("Document not found")

    is_owner = document.owner_id == request.user.id

    has_permission = DocumentPermission.objects.filter(
        document=document,
        user=request.user,
        permission__in=["read", "edit"]
    ).exists()

    if not is_owner and not has_permission:
        create_audit_log(
            request,
            "download",
            "denied",
            document,
            "Unauthorized download attempt."
        )
        raise Http404("Document not found")

    try:
        file_handle = document.file.open("rb")
    except (OSError, ValueError):
        create_audit_log(
            request,
            "download",
            "denied",
            document,
            "Document file could not be opened."
        )
        raise Http404("Document file not found")

    create_audit_log(
        request,
        "download",
        "success",
        document,
        "Document downloaded successfully."
    )

    return FileResponse(
        file_handle,
        as_attachment=True,
        filename=os.path.basename(document.file.name)
    )


# SHARE DOCUMENT
@login_required
def share_document(request):
    if request.user.profile.role != "owner":
        messages.error(
            request,
            "Only document owners can share documents."
        )
        return redirect("dashboard")

    documents = Document.objects.filter(owner=request.user)

    viewers = User.objects.filter(
        profile__role="viewer"
    ).order_by("username")

    if request.method == "POST":
        document_id = request.POST.get("document_id")
        username = request.POST.get("username")
        permission = request.POST.get("permission")

        if not document_id or not username or not permission:
            messages.error(request, "Please fill in all fields.")
            return redirect("share_document")

        if permission not in ["read", "edit"]:
            messages.error(request, "Invalid permission selected.")
            return redirect("share_document")

        document = get_object_or_404(
            Document,
            id=document_id,
            owner=request.user
        )

        viewer = User.objects.filter(
            username=username,
            profile__role="viewer"
        ).first()

        if viewer is None:
            messages.error(request, "Viewer account not found.")
            return redirect("share_document")

        DocumentPermission.objects.update_or_create(
            document=document,
            user=viewer,
            defaults={"permission": permission}
        )

        create_audit_log(
            request,
            "permission_granted",
            "success",
            document,
            f"{permission.title()} permission granted to {viewer.username}."
        )

        messages.success(request, "Document shared successfully!")
        return redirect("share_document")

    permissions = DocumentPermission.objects.filter(
        document__owner=request.user
    ).select_related("document", "user")

    return render(
        request,
        "documents/share_document.html",
        {
            "documents": documents,
            "viewers": viewers,
            "permissions": permissions
        }
    )


# VIEWER - DOCUMENTS SHARED WITH ME AND SEARCH
@login_required
def shared_documents(request):
    if request.user.profile.role != "viewer":
        messages.error(request, "Access denied.")
        return redirect("dashboard")

    query = request.GET.get("q", "").strip()
    owner = request.GET.get("owner", "").strip()
    category = request.GET.get("category", "").strip()
    upload_date = request.GET.get("date", "").strip()

    permissions = DocumentPermission.objects.filter(
        user=request.user
    ).select_related(
        "document",
        "document__owner"
    )

    if query:
        permissions = permissions.filter(
            document__title__icontains=query
        )

    if owner:
        permissions = permissions.filter(
            document__owner__username__icontains=owner
        )

    if category:
        if valid_category(category):
            permissions = permissions.filter(
                document__category=category
            )
        else:
            messages.error(request, "Invalid category selected.")

    if upload_date:
        valid_date = parse_date(upload_date)

        if valid_date:
            permissions = permissions.filter(
                document__uploaded_at__date=valid_date
            )
        else:
            messages.error(request, "Invalid date format.")

    permissions = permissions.order_by("-document__uploaded_at")

    return render(
        request,
        "documents/shared_documents.html",
        {
            "permissions": permissions,
            "query": query,
            "owner": owner,
            "category": category,
            "upload_date": upload_date,
            "categories": Document.CATEGORY_CHOICES,
        }
    )


# OWNER - REVOKE DOCUMENT PERMISSION
@login_required
def revoke_permission(request, permission_id):
    if request.method != "POST":
        return redirect("share_document")

    permission = get_object_or_404(
        DocumentPermission,
        id=permission_id,
        document__owner=request.user
    )

    document = permission.document
    viewer_username = permission.user.username
    permission_type = permission.permission

    permission.delete()

    create_audit_log(
        request,
        "permission_revoked",
        "success",
        document,
        f"{permission_type.title()} permission revoked from {viewer_username}."
    )

    messages.success(
        request,
        "Document access revoked successfully!"
    )

    return redirect("share_document")


# ADMIN - VIEW AUDIT LOGS
@login_required
def audit_dashboard(request):
    if not request.user.is_superuser:
        messages.error(request, "Only Admin can view audit logs.")
        return redirect("dashboard")

    audit_logs = AuditLog.objects.select_related(
        "actor",
        "document"
    ).all()

    return render(
        request,
        "documents/audit_dashboard.html",
        {"audit_logs": audit_logs}
    )


# HELPER: CHECK DOCUMENT EDIT PERMISSION
def can_edit_document(document, user):
    if document.owner_id == user.id:
        return True

    return DocumentPermission.objects.filter(
        document=document,
        user=user,
        permission="edit"
    ).exists()


# EDIT DOCUMENT
@login_required
def edit_document(request, document_id):
    document = get_object_or_404(
        Document,
        id=document_id
    )

    if not can_edit_document(document, request.user):
        create_audit_log(
            request,
            "edit",
            "denied",
            document,
            "Unauthorized document edit attempt."
        )
        raise Http404("Document not found")

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        category = request.POST.get(
            "category",
            document.category
        )
        uploaded_file = request.FILES.get("file")

        if not title:
            messages.error(request, "Document title is required.")
            return redirect("edit_document", document_id=document.id)

        if not valid_category(category):
            messages.error(request, "Invalid category selected.")
            return redirect("edit_document", document_id=document.id)

        if uploaded_file:
            validation_error = validate_uploaded_file(uploaded_file)

            if validation_error:
                messages.error(request, validation_error)
                return redirect("edit_document", document_id=document.id)

        old_file_name = document.file.name

        document.title = title
        document.category = category

        if uploaded_file:
            document.file = uploaded_file

        document.save()

        if uploaded_file and old_file_name:
            document.file.storage.delete(old_file_name)

        create_audit_log(
            request,
            "edit",
            "success",
            document,
            "Document title, category or file updated successfully."
        )

        messages.success(request, "Document updated successfully!")

        if request.user.profile.role == "viewer":
            return redirect("shared_documents")

        return redirect("my_documents")

    return render(
        request,
        "documents/edit_document.html",
        {
            "document": document,
            "categories": Document.CATEGORY_CHOICES
        }
    )


# DELETE DOCUMENT
@login_required
def delete_document(request, document_id):
    document = Document.objects.filter(id=document_id).first()

    if document is None:
        create_audit_log(
            request,
            "delete",
            "denied",
            details=f"Attempted deletion of missing document ID {document_id}."
        )
        raise Http404("Document not found")

    if document.owner_id != request.user.id:
        create_audit_log(
            request,
            "delete",
            "denied",
            document,
            "Unauthorized document deletion attempt."
        )
        raise Http404("Document not found")

    if request.method != "POST":
        return render(
            request,
            "documents/delete_document.html",
            {"document": document}
        )

    document_title = document.title

    create_audit_log(
        request,
        "delete",
        "success",
        document,
        f"Document '{document_title}' deleted by its owner."
    )

    if document.file:
        document.file.delete(save=False)

    document.delete()

    messages.success(request, "Document deleted successfully!")
    return redirect("my_documents")
