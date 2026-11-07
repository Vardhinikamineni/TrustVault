
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .storage import PrivateDocumentStorage


class Profile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('owner', 'Document Owner'),
        ('viewer', 'Viewer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='viewer'
    )

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class Document(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('education', 'Education'),
        ('finance', 'Finance'),
        ('legal', 'Legal'),
        ('personal', 'Personal'),
        ('business', 'Business'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='general'
    )
    file = models.FileField(
        upload_to='documents/',
        storage=PrivateDocumentStorage()
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class DocumentPermission(models.Model):
    PERMISSION_CHOICES = [
        ('read', 'Read'),
        ('edit', 'Edit'),
    ]

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='permissions'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='document_permissions'
    )
    permission = models.CharField(
        max_length=10,
        choices=PERMISSION_CHOICES
    )
    granted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['document', 'user'],
                name='unique_document_user_permission'
            )
        ]

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.document.title} - "
            f"{self.permission}"
        )


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('view', 'Document Viewed'),
        ('upload', 'Document Uploaded'),
        ('download', 'Document Downloaded'),
        ('edit', 'Document Edited'),
        ('delete', 'Document Deleted'),
        ('permission_granted', 'Permission Granted'),
        ('permission_revoked', 'Permission Revoked'),
    ]

    OUTCOME_CHOICES = [
        ('success', 'Successful'),
        ('denied', 'Denied'),
    ]

    actor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs'
    )
    document = models.ForeignKey(
        Document,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs'
    )
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    outcome = models.CharField(
        max_length=10,
        choices=OUTCOME_CHOICES,
        default='success'
    )
    details = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return (
            f"{self.action} - "
            f"{self.outcome} - "
            f"{self.timestamp}"
        )
