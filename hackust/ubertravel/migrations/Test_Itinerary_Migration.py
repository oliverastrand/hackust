from django.db import migrations


def test_itinerary_load(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('ubertravel', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(test_itinerary_load)
    ]