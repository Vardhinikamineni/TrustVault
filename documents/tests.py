
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from .models import Document, DocumentPermission, AuditLog


class TrustVaultSecurityTests(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            username="testowner",
            password="OwnerPass123"
        )
        self.owner.profile.role = "owner"
        self.owner.profile.save()

        self.viewer = User.objects.create_user(
            username="testviewer",
            password="ViewerPass123"
        )
        self.viewer.profile.role = "viewer"
        self.viewer.profile.save()

        self.other_owner = User.objects.create_user(
            username="otherowner",
            password="OtherPass123"
        )
        self.other_owner.profile.role = "owner"
        self.other_owner.profile.save()

        test_file = SimpleUploadedFile(
            "test_document.pdf",
            b"This is a test PDF document.",
            content_type="application/pdf"
        )

        self.document = Document.objects.create(
            title="Test Document",
            file=test_file,
            owner=self.owner
        )

        self.download_url = reverse(
            "download_document",
            args=[self.document.id]
        )

        self.edit_url = reverse(
            "edit_document",
            args=[self.document.id]
        )

        self.delete_url = reverse(
            "delete_document",
            args=[self.document.id]
        )

    def get_and_close_response(self, url):
        response = self.client.get(url)
        response.close()
        return response

    def tearDown(self):
        for document in Document.objects.all():
            if document.file:
                document.file.close()
                document.file.delete(save=False)

    # TEST 1: Owner can download own document
    def test_owner_can_download_own_document(self):
        self.client.force_login(self.owner)

        response = self.get_and_close_response(
            self.download_url
        )

        self.assertEqual(response.status_code, 200)

    # TEST 2: Viewer can download with Read permission
    def test_viewer_can_download_with_read_permission(self):
        DocumentPermission.objects.create(
            document=self.document,
            user=self.viewer,
            permission="read"
        )

        self.client.force_login(self.viewer)

        response = self.get_and_close_response(
            self.download_url
        )

        self.assertEqual(response.status_code, 200)

    # TEST 3: Viewer cannot download without permission
    def test_viewer_cannot_download_without_permission(self):
        self.client.force_login(self.viewer)

        response = self.get_and_close_response(
            self.download_url
        )

        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            AuditLog.objects.filter(
                actor=self.viewer,
                document=self.document,
                action="download",
                outcome="denied"
            ).exists()
        )

    # TEST 4: Revoked permission blocks download
    def test_revoked_permission_blocks_download(self):
        permission = DocumentPermission.objects.create(
            document=self.document,
            user=self.viewer,
            permission="read"
        )

        permission.delete()

        self.client.force_login(self.viewer)

        response = self.get_and_close_response(
            self.download_url
        )

        self.assertEqual(response.status_code, 404)

    # TEST 5: Another owner cannot download document
    def test_another_owner_cannot_download_document(self):
        self.client.force_login(self.other_owner)

        response = self.get_and_close_response(
            self.download_url
        )

        self.assertEqual(response.status_code, 404)

    # TEST 6: Read-only viewer cannot edit document
    def test_read_only_viewer_cannot_edit_document(self):
        DocumentPermission.objects.create(
            document=self.document,
            user=self.viewer,
            permission="read"
        )

        self.client.force_login(self.viewer)

        response = self.get_and_close_response(
            self.edit_url
        )

        self.assertEqual(response.status_code, 404)

    # TEST 7: Viewer with Edit permission can access edit page
    def test_viewer_with_edit_permission_can_access_edit_page(self):
        DocumentPermission.objects.create(
            document=self.document,
            user=self.viewer,
            permission="edit"
        )

        self.client.force_login(self.viewer)

        response = self.get_and_close_response(
            self.edit_url
        )

        self.assertEqual(response.status_code, 200)

    # TEST 8: Viewer cannot delete owner's document
    def test_viewer_cannot_delete_owners_document(self):
        self.client.force_login(self.viewer)

        response = self.client.post(
            self.delete_url,
            follow=True
        )

        self.assertEqual(response.status_code, 404)

        # Confirm document still exists
        self.assertTrue(
            Document.objects.filter(
                id=self.document.id
            ).exists()
        )
    
    # TEST 9: Unauthorized deletion is recorded in audit log
    def test_unauthorized_deletion_is_logged(self):
        self.client.force_login(self.viewer)

        response = self.client.post(
            self.delete_url
        )

        self.assertEqual(response.status_code, 404)

        self.assertTrue(
            Document.objects.filter(
                id=self.document.id
            ).exists()
        )

        self.assertTrue(
            AuditLog.objects.filter(
                actor=self.viewer,
                document=self.document,
                action="delete",
                outcome="denied"
            ).exists()
        )
       
