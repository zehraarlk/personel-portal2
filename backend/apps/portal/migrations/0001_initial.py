# Generated for unmanaged mapping to existing personel_db tables.
# database_operations boş: MySQL'de tablo oluşturulmaz / silinmez.

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='Duyuru',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('baslik', models.CharField(max_length=255)),
                        ('aciklama', models.TextField()),
                        ('resim', models.CharField(max_length=255)),
                        ('view', models.IntegerField(default=0)),
                    ],
                    options={
                        'verbose_name': 'Duyuru',
                        'verbose_name_plural': 'Duyurular',
                        'db_table': 'duyurular',
                        'ordering': ['-id'],
                        'managed': False,
                    },
                ),
                migrations.CreateModel(
                    name='Personel',
                    fields=[
                        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('sicil_no', models.CharField(max_length=50)),
                        ('ad', models.CharField(max_length=50)),
                        ('soyad', models.CharField(max_length=50)),
                        ('email', models.CharField(max_length=100)),
                        ('sifre', models.CharField(max_length=255)),
                        ('dogum_tarihi', models.DateField()),
                        ('foto_url', models.CharField(max_length=255)),
                        ('remember_token_hash', models.CharField(blank=True, max_length=64, null=True)),
                        ('remember_token_expires', models.DateTimeField(blank=True, null=True)),
                        ('tc_no', models.CharField(blank=True, max_length=11, null=True)),
                        ('telefon', models.CharField(blank=True, max_length=20, null=True)),
                    ],
                    options={
                        'verbose_name': 'Personel',
                        'verbose_name_plural': 'Personeller',
                        'db_table': 'personeller',
                        'ordering': ['ad', 'soyad'],
                        'managed': False,
                    },
                ),
            ],
            database_operations=[],
        ),
    ]
