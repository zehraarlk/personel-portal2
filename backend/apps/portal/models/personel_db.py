"""personel_db — mevcut phpMyAdmin tabloları (managed=False, yeni tablo yok)."""

from django.db import models


class AnasayfaDuyurular(models.Model):
    baslik = models.CharField(max_length=255)
    aciklama = models.TextField()
    resim = models.CharField(max_length=255)
    view = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'anasayfa_duyurular'


class AnasayfaLinkler(models.Model):
    baslik = models.CharField(max_length=255)
    logo_url = models.CharField(max_length=255, blank=True, null=True)
    hedef_url = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'anasayfa_linkler'
        unique_together = (('baslik', 'hedef_url'),)


class AnketlerKategori(models.Model):
    slug = models.CharField(unique=True, max_length=100)
    ad = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'anketler_kategori'


class Anketler(models.Model):
    baslik = models.CharField(max_length=255)
    aciklama = models.TextField(blank=True, null=True)
    resim_url = models.CharField(max_length=500, blank=True, null=True)
    baslangic_tarihi = models.DateField(blank=True, null=True)
    bitis_tarihi = models.DateField(blank=True, null=True)
    katilim_sayisi = models.IntegerField(blank=True, null=True)
    hedef_katilim = models.IntegerField(blank=True, null=True)
    favori = models.IntegerField()
    kategori = models.ForeignKey(
        AnketlerKategori, models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = 'anketler'


class AnketSorulari(models.Model):
    anket = models.ForeignKey(Anketler, models.DO_NOTHING)
    soru_metni = models.TextField()
    soru_tipi = models.CharField(max_length=14)
    sira = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'anket_sorulari'


class AnketSecenekleri(models.Model):
    soru = models.ForeignKey(AnketSorulari, models.DO_NOTHING)
    secenek_metni = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'anket_secenekleri'


class Personeller(models.Model):
    sicil_no = models.CharField(unique=True, max_length=50)
    ad = models.CharField(max_length=50)
    soyad = models.CharField(max_length=50)
    email = models.CharField(unique=True, max_length=100)
    sifre = models.CharField(max_length=255)
    dogum_tarihi = models.DateField()
    foto_url = models.CharField(max_length=255)
    remember_token_hash = models.CharField(
        unique=True, max_length=64, blank=True, null=True
    )
    remember_token_expires = models.DateTimeField(blank=True, null=True)
    tc_no = models.CharField(max_length=11, blank=True, null=True)
    telefon = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'personeller'

    def __str__(self):
        return f'{self.ad} {self.soyad}'


class AnketCevaplari(models.Model):
    anket = models.ForeignKey(Anketler, models.DO_NOTHING)
    personel = models.ForeignKey(Personeller, models.DO_NOTHING)
    soru = models.ForeignKey(AnketSorulari, models.DO_NOTHING)
    secenek = models.ForeignKey(
        AnketSecenekleri, models.DO_NOTHING, blank=True, null=True
    )
    cevap_metni = models.TextField(blank=True, null=True)
    olusturma_tarihi = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'anket_cevaplari'
        unique_together = (('personel', 'soru'),)


class AnketKatilimlari(models.Model):
    anket_id = models.IntegerField()
    personel_id = models.IntegerField()
    tamamlanma_tarihi = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'anket_katilimlari'
        unique_together = (('anket_id', 'personel_id'),)


class DuyurularKategori(models.Model):
    slug = models.CharField(unique=True, max_length=100)
    ad = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'duyurular_kategori'


class Duyurular(models.Model):
    baslik = models.CharField(max_length=255)
    aciklama = models.TextField()
    resim = models.CharField(max_length=255)
    view = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'duyurular'
        ordering = ['-id']

    def __str__(self):
        return self.baslik


class EtkinliklerDurum(models.Model):
    slug = models.CharField(unique=True, max_length=100)
    ad = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'etkinlikler_durum'


class Etkinlikler(models.Model):
    baslik = models.CharField(max_length=255)
    aciklama = models.TextField(blank=True, null=True)
    tarih = models.DateField()
    bitis_tarihi = models.DateField(blank=True, null=True)
    view = models.IntegerField(blank=True, null=True)
    resim = models.CharField(max_length=255, blank=True, null=True)
    durum = models.ForeignKey(
        EtkinliklerDurum,
        models.DO_NOTHING,
        blank=True,
        null=True,
        db_column='durum_id',
    )
    durum_kodu = models.CharField(db_column='durum', max_length=20)

    class Meta:
        managed = False
        db_table = 'etkinlikler'


class EtkinliklerDuyurular(models.Model):
    sayfa_tipi = models.CharField(max_length=50)
    baslik = models.CharField(max_length=255)
    aciklama = models.TextField(blank=True, null=True)
    resim_url = models.CharField(max_length=255, blank=True, null=True)
    tarih = models.DateField(blank=True, null=True)
    kategori = models.ForeignKey(
        DuyurularKategori, models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = 'etkinlikler_duyurular'


class Haberler(models.Model):
    baslik = models.CharField(max_length=255)
    resim = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'haberler'


class HaberGaleri(models.Model):
    haber = models.ForeignKey(Haberler, models.DO_NOTHING)
    resim_url = models.CharField(max_length=255)
    sira = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'haber_galeri'


class IcerikIzlemeleri(models.Model):
    tablo = models.CharField(max_length=64)
    kayit_id = models.IntegerField()
    izleyici = models.CharField(max_length=96)
    olusturma_tarihi = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'icerik_izlemeleri'
        unique_together = (('tablo', 'kayit_id', 'izleyici'),)


class KaynaklarKategori(models.Model):
    slug = models.CharField(unique=True, max_length=100)
    ad = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'kaynaklar_kategori'


class KaynaklarAltKategori(models.Model):
    kaynak_kategori = models.ForeignKey(KaynaklarKategori, models.DO_NOTHING)
    slug = models.CharField(max_length=100)
    ad = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'kaynaklar_alt_kategori'
        unique_together = (('kaynak_kategori', 'slug'),)


class Kaynaklar(models.Model):
    baslik = models.CharField(max_length=255)
    aciklama = models.TextField()
    ikon = models.CharField(max_length=50, blank=True, null=True)
    dosya_yolu = models.CharField(max_length=255)
    resmi_sayfa = models.CharField(max_length=500, blank=True, null=True)
    boyut = models.CharField(max_length=50)
    tarih = models.CharField(max_length=50)
    kategori = models.ForeignKey(
        KaynaklarKategori, models.DO_NOTHING, blank=True, null=True
    )
    alt_kategori = models.ForeignKey(
        KaynaklarAltKategori, models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = 'kaynaklar'


class OturumKayitlari(models.Model):
    personel = models.ForeignKey(Personeller, models.DO_NOTHING)
    giris_zamani = models.DateTimeField()
    cikis_zamani = models.DateTimeField(blank=True, null=True)
    ip_adresi = models.CharField(max_length=45, blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    kapanis_tipi = models.CharField(max_length=20, blank=True, null=True)
    son_aktivite = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oturum_kayitlari'


class SiteIkonlari(models.Model):
    anahtar = models.CharField(unique=True, max_length=100)
    ad = models.CharField(max_length=150)
    kategori = models.CharField(max_length=50)
    ikon_sinifi = models.CharField(max_length=150)
    renk = models.CharField(max_length=30, blank=True, null=True)
    sira = models.IntegerField()
    aktif = models.IntegerField()
    olusturma_tarihi = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'site_ikonlari'


class SizdengelenlerKategori(models.Model):
    slug = models.CharField(unique=True, max_length=100)
    ad = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'sizdengelenler_kategori'


class SizdenGelenler(models.Model):
    baslik = models.CharField(max_length=255)
    ozet = models.TextField()
    tarih = models.DateField()
    goruntulenme = models.IntegerField(blank=True, null=True)
    gorsel_yolu = models.CharField(max_length=255, blank=True, null=True)
    olusturma_tarihi = models.DateTimeField()
    kategori = models.ForeignKey(
        SizdengelenlerKategori, models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = 'sizden_gelenler'


class VefatBilgileri(models.Model):
    vefat_eden_adi = models.CharField(max_length=255)
    iliski_pozisyon = models.TextField()
    vefat_tarihi = models.DateField()
    vefat_tarihi_metin = models.CharField(max_length=50)
    cenaze_mesaji = models.TextField()

    class Meta:
        managed = False
        db_table = 'vefat_bilgileri'


class VideolarKategori(models.Model):
    slug = models.CharField(unique=True, max_length=100)
    ad = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'videolar_kategori'


class Videolar(models.Model):
    youtube_id = models.CharField(unique=True, max_length=50)
    baslik = models.CharField(max_length=255)
    aciklama = models.TextField()
    sure = models.CharField(max_length=20)
    kategori = models.ForeignKey(
        VideolarKategori, models.DO_NOTHING, blank=True, null=True
    )
    vitrin = models.IntegerField()
    vitrin_baslik = models.CharField(max_length=255, blank=True, null=True)
    vitrin_aciklama = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'videolar'


class YardimciLinklerKategori(models.Model):
    slug = models.CharField(unique=True, max_length=100)
    ad = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'yardimci_linkler_kategori'


class YardimciLinkler(models.Model):
    baslik = models.CharField(max_length=255)
    logo_url = models.CharField(max_length=255, blank=True, null=True)
    hedef_url = models.CharField(max_length=500)
    kategori = models.ForeignKey(
        YardimciLinklerKategori, models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = 'yardimci_linkler'
        unique_together = (('kategori', 'baslik', 'hedef_url'),)


class Yoneticiler(models.Model):
    kullanici_adi = models.CharField(unique=True, max_length=50)
    sifre = models.CharField(max_length=255)
    ad = models.CharField(max_length=100)
    soyad = models.CharField(max_length=100)
    yetki = models.CharField(max_length=6)
    aktif = models.IntegerField()
    olusturma_tarihi = models.DateTimeField()
    foto_url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'yoneticiler'


class YoneticiOturumKayitlari(models.Model):
    yonetici = models.ForeignKey(Yoneticiler, models.DO_NOTHING)
    giris_zamani = models.DateTimeField()
    cikis_zamani = models.DateTimeField(blank=True, null=True)
    ip_adresi = models.CharField(max_length=45, blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    kapanis_tipi = models.CharField(max_length=20, blank=True, null=True)
    son_aktivite = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'yonetici_oturum_kayitlari'


# Geriye uyumlu takma adlar
Duyuru = Duyurular
Personel = Personeller
