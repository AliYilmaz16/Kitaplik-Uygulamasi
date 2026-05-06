# Kutuphane Desktop (PySide6)

Bu klasör, `kutuphane` Spring Boot projesindeki book endpoint’lerini kullanan basit bir masaüstü uygulaması içerir.

## Backend (Spring Boot)

1) PostgreSQL’i çalıştırın ve `kutuphane/src/main/resources/application.properties` içindeki ayarlara uygun bir DB erişimi olduğundan emin olun.

2) Backend’i başlatın:

```bash
cd /Users/aliyilmaz/Desktop/java/springboot/Workspace/kutuphane
mvn spring-boot:run
```

Varsayılan olarak `http://localhost:8080` üzerinde çalışır.

## Desktop App (PySide6)

1) Sanal ortam oluşturun ve bağımlılıkları kurun:

```bash
cd /Users/aliyilmaz/Desktop/java/springboot/Workspace/frontend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2) Uygulamayı çalıştırın:

```bash
python -m app.main
```

## Kullanım

- Üstteki **API Base URL** alanı default `http://localhost:8080`.\n+- **Bağlan / Yenile** ile kitap listesini çekin (`GET /rest/api/book/list`).\n+- Formdan **Yeni Kaydet** ile kitap ekleyin (`POST /rest/api/book/save`).\n+- Tablodan satır seçip **Seçileni Güncelle** (`PUT /rest/api/book/update/{id}`) veya **Seçileni Sil** (`DELETE /rest/api/book/delete/{id}`) kullanın.\n+
