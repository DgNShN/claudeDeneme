# Flask Web Sitesi

Flask ve SQLite ile geliştirilmiş basit bir web sitesi. İletişim formu, admin paneli ve otomatik email bildirimi içerir.

## Özellikler

- Ana sayfa, Ürünler, Hakkımızda ve İletişim sayfaları
- SQLite veritabanı ile mesaj kayıt sistemi
- Admin girişi ile korunan mesaj paneli
- Mesajlarda arama ve filtreleme
- Mesaj silme
- Yeni mesaj gelince email bildirimi
- Otomatik GitHub push (git_watch.py)

## Kurulum

```bash
pip install flask watchdog
```

## Çalıştırma

```bash
python app.py
```

Tarayıcıda aç: `http://127.0.0.1:5000`

## Admin Paneli

`http://127.0.0.1:5000/messages` adresine git.
Varsayılan şifre: `admin123`

## Email Bildirimi

Gmail ile bildirim almak için terminalde ayarla:

```bash
$env:EMAIL_SENDER="senin@gmail.com"
$env:EMAIL_PASSWORD="gmail-uygulama-sifresi"
$env:EMAIL_RECEIVER="bildirim@gmail.com"
python app.py
```

> Gmail uygulama şifresi için: Google Hesabı → Güvenlik → 2 Adımlı Doğrulama → Uygulama Şifreleri

## Otomatik Git Push

Dosya değişikliklerini otomatik GitHub'a göndermek için:

```bash
python git_watch.py
```

## Sayfalar

| Sayfa | URL |
|-------|-----|
| Ana Sayfa | `/` |
| Ürünler | `/products` |
| Hakkımızda | `/about` |
| İletişim | `/contact` |
| Mesajlar (Admin) | `/messages` |
