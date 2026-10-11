# Belge taşıma kaydı

Görev `repository-split`, revizyon 2, 11 Ekim 2026. [English](../en/repository-migration.md).

Bakımcı üç belge/geliştirici deposunu istedi, ardından projeye özel ek depoların kurulmasına yetki verdi. [Harita](repository-map.md) sekiz yeni depoyu ve mevcut çekirdek/web sitesi sınırlarını kaydeder. Web sitesi değiştirilmez.

## Kaynaklar ve hedefler

[Makine tarafından okunabilen envanter](../../records/document-migration.json), 26 belge/kayıt aktarımının kesin kaynak yollarını/revizyonlarını/özetlerini ve son hedef yollarını/özetlerini eşler. Entegre edilen çekirdek main içindeki 21 dosya çekirdek PR’ında kaldırılır; üç katkı giriş dosyası ince yönlendirmelere dönüşür. PR #2 eşzamanlı olarak `8e529b4747aef2648c241354858d28aaf416ecaa` revizyonuyla birleşti ve görev dalına alındı. Diğer aktarımlar açık katkı taslağı [eylema PR #3](https://github.com/eylema-dev/eylema/pull/3), `406d1ab639cf70149f89832a1b03bd06d2d72633` revizyonundandır; ilk görev konsolu yönü korunur, birleşmemiş politika kabul edilmiş sayılmaz. [Özgün main](https://github.com/eylema-dev/eylema/blob/214a2c3d5313a251f1aae720b2ac1565f273d76b/README.md) Git geçmişinde erişilebilirdir.

| İçerik | Hedef |
|---|---|
| Güncel mimari, API, geliştirme/işletim, öğrenme, proje yapısı ve yol haritası | eylema-docs-en ve eylema-docs-tr içinde eşleşen `docs/` dosyaları |
| Eski Türkçe mimari/API taslakları | eylema-docs-tr/archive |
| Katkı sözleşmesi ve tam katkı rehberleri | devguide kökü; diğer köklerde yalnızca yönlendirmeler |
| Kalite kapıları, araçlar ve isim kararı metinleri | devguide/docs/en ve devguide/docs/tr |
| Tarihsel müsaitlik ve doğrulama JSON kayıtları | Açıkça tarihsel etiketli devguide/records |
| Makine şemaları, marka varlıkları ve üretim kaynağı | eylema içinde kalır |

Şema sürümü, API işlemi veya çalışma zamanı davranışı değişmez. Taşıma kayıtları dosya kökenini korur; bu, yeni depolara içerik aktarımıdır, ortak Git geçmişinin yeniden yazılması değildir. Bağlantılar ve depo sınırı bölümleri bilerek özgün baytlardan farklıdır.

[İlişkili PR kaydı](../../records/pull-requests.json) dokuz inceleme adresini listeler. [Yerel doğrulama kaydı](../../records/local-verification.json) çalıştırılan kontrolleri ve kalan kabul sınırlarını açıklar.

## İnceleme ve entegrasyon sırası

Uygulama ilişkili `codex/repository-split` PR'larıyla sunulur. Yeni depo main dalları başlangıçta yalnızca GitHub'ın oluşturduğu README'yi içerir. Depo kümesi manifesti incelenebilir üye commit'lerini sabitler; entegrasyon kontrolleri bu PR'ların önceden birleşmesini gerektirmez. Varsayılan dal bağlantıları son yerleşimi hedefler ve eşgüdümlü birleştirmelerden sonra tümü erişilebilir olur.

1. Hedef belgeleri, rehberi, ortak şablonları ve ayrılmış depo iskeletlerini; politika/kontrol değişiklikleriyle birlikte inceleyin.
2. Sabitlenmiş entegrasyon kanıtını ve tüm üye baş revizyonlarını inceleyin. Rehber indirilen üye içeriğini veri olarak okur; betiklerini çalıştırmaz.
3. Gerçek bakımcı onayından sonra önce hedef depoları, sonra devguide'ı, **en son çekirdekteki kaldırmayı** birleştirin. Bu görev otomatik birleştirme kurmaz veya yapmaz.
4. Çekirdek PR #2 birleşmiştir ve katkı temeli korunur. Açık çekirdek PR #3 bu yerleşimle örtüşür. Bölünmeden sonra aynen birleştirmeyin: bakımcı PR’ı geçersiz kılınmış olarak kapatmalı veya kalan işi yinelenen belge/politikaları geri getirmeden yeniden tabanlamalıdır. Bu görev PR’ı korur; sessizce kapatmaz.
5. Yetkili eşgüdümlü birleştirmeden sonra varsayılan dal bağlantılarını kontrol edin. Bu kontrol birleşmeden önce `not_run` durumundadır; sabit commit doğrulaması farklı bir sonuçtur.

## Geri dönüş

Çekirdek kaldırmasından önce eski varsayılan dal belgeleri erişilebilirdir. Sonrasında önce çekirdek taşıma commit'ini geri alarak özgün girişleri ve belgeleri geri getirin. Hedef depoları ve geçmişlerini koruyun; bağlantıları geri almak için depoları silmeyin. Politika/araçlar geri alınacaksa önceki incelenmiş depo kümesini ve kontrollerini birlikte geri yükleyin. Bu taşıma üretim verisi veya çalışma zamanı sürümü içermez.
