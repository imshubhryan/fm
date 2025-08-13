from django.conf import settings
import django.db.models.deletion
from django.db import migrations, models

def get_default_user_id():
    # Yeh function bina arguments ke chalega, migration me use karenge
    from django.contrib.auth import get_user_model
    User = get_user_model()
    first_user = User.objects.first()
    return first_user.id if first_user else 1

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_remove_category_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='user',
            field=models.ForeignKey(
                to=settings.AUTH_USER_MODEL,
                on_delete=django.db.models.deletion.CASCADE,
                default=get_default_user_id  # Note: callable without args
            ),
            preserve_default=False,
        ),
    ]
