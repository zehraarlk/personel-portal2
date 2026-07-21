from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        'personel_db hazır tablolar kullanılıyor; seed gerekmez. '
        'Veri phpMyAdmin / mevcut MySQL kayıtlarından gelir.'
    )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.WARNING(
                'Seed atlandı: duyurular ve personeller tabloları personel_db içinde hazır.'
            )
        )
