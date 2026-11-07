from django.conf import settings
from django.db import migrations


def promote_admin(apps, schema_editor):
    app_label, model_name = settings.AUTH_USER_MODEL.split(".")
    User = apps.get_model(app_label, model_name)

    User.objects.filter(username="admin").update(
        is_staff=True,
        is_superuser=True
    )


class Migration(migrations.Migration):

    dependencies = [
        ("documents", "0008_alter_auditlog_action"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(
            promote_admin,
            migrations.RunPython.noop
        ),
    ]
