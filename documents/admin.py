
from django.contrib import admin
from .models import Profile, Document, DocumentPermission, AuditLog


admin.site.register(Profile)
admin.site.register(Document)
admin.site.register(DocumentPermission)
admin.site.register(AuditLog)
