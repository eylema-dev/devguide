# Organizasyon depo haritası

Revizyon **0.2.0**, 11 Ekim 2026. [English](../en/repository-map.md). Depo oluşturmak, uygulamanın kabul edildiği anlamına gelmez.

| Depo | Sorumluluk |
|---|---|
| [eylema](https://github.com/eylema-dev/eylema) | Rust çekirdeği, sözleşmeler, CLI ve makine şemaları |
| [eylema-docs-en](https://github.com/eylema-dev/eylema-docs-en) | Kanonik İngilizce ürün sözleşmeleri ve yol haritası |
| [eylema-docs-tr](https://github.com/eylema-dev/eylema-docs-tr) | Türkçe karşılıklar ve tarihsel Türkçe taslaklar |
| [devguide](https://github.com/eylema-dev/devguide) | Ortak politika, araç kaynakları, depo kaydı ve entegrasyon kontrolleri |
| [.github](https://github.com/eylema-dev/.github) | Organizasyon profili ve varsayılan katkı şablonları |
| [eylema-examples](https://github.com/eylema-dev/eylema-examples) | Çekirdek API sürümüne sabitlenmiş tüketici örnekleri |
| [eylema-evals](https://github.com/eylema-dev/eylema-evals) | Sentetik örnekler, değerlendirme araçları ve tekrarlanabilir sonuçlar |
| [eylema-models](https://github.com/eylema-dev/eylema-models) | Katalog üstverisi, uyumluluk ve model kümesi manifestleri; ağırlık içermez |
| [eylema-training](https://github.com/eylema-dev/eylema-training) | Eğitim tarifleri, ortam kilitleri ve izinli veri hazırlama |
| [eylemadotdev](https://github.com/eylema-dev/eylemadotdev) | Mevcut tanıtım sitesi; bu bölünmeden bağımsız yönetilir |

## Sahiplik ve sınırlar

Çekirdek tek Rust çalışma alanıyla başlar: sözleşme tipleri, deterministik çalışma zamanı, günlük, web arayüzü ve CLI birlikte değişir. Gerçekten bağımsız sürümlenen tüketici oluşmadan her crate veya sağlayıcı için ayrı depo açmayın. API/SDK üreticileri ve GitHub/model sağlayıcı adaptörleri, arayüz ve yaşam döngüsü ayrılmayı gerektirene kadar çekirdek modülleridir. Mimari öneriler ürün belgelerinde, katkı süreci kararları devguide içinde kalır.

Örnekler açık API'leri gösterir; çalışma zamanının çatallanmış kopyalarını taşımaz. Değerlendirmeler iş yüklerini ve ölçüm araçlarını yönetir; çalışma zamanı optimizasyonlarını değil. Model üstverisi lisanslı varlıklara ve kabul edilmiş kanıtlara bağlanır; ağırlıklar ayrıca onaylanmış varlık deposuna aittir. Eğitim tarifleri ve ortam kilitleri eğitim deposundadır; veri kabulü, gizlilik, lisanslar ve hesaplama harcamaları ayrı kabul edilmiş görev gerektirir. Burada varlık deposu, kayıt servisi veya eğitim hizmeti kurulmaz.

Marka varlıkları ve mevcut üretim betiği, ayrı yaşam döngüsü gerekene kadar çekirdekte kalır. Web sitesi mevcut ayrı projedir. Yeni iskeletler Rust, GPU, çıkarım, eğitim, kıyaslama veya örnek uygulama gerçekleştirmiş sayılmaz. Açık dağıtım lisansı kararı beklemektedir.

## Gerekçe olduğunda depo ayırın

Yeni deponun farklı sahibi, kitlesi veya sürüm takvimi; açık girdi/çıktı sözleşmesi; görev listesi; aşamasına uygun testler; sürüm/uyumluluk kuralları ve belirli bakım yolu olmalıdır. Bunlar yoksa mevcut sorumlu depoda dizin kullanın. Bağımlılıklar sürümlenen çekirdek sözleşmelerine yönelsin; depolar arası değişiklikleri ilişkili tek görev olarak kaydedin.

## Ortak dosyalar

Politika `devguide/AGENTS.md` ve katkı rehberlerine aittir. Diğer depolar ince yönlendirme dosyaları taşır. Doğrulama uygulamasının kaynağı `devguide/tools/` içindedir; kopyalar `tools/vendor.json` içindeki içerik özetleriyle kaydedilir ve depo kümesi kapısında birlikte denetlenir. Kopyaları PR’larla birlikte güncelleyin; değişken uzak betiği indirip çalıştırmayın. Python ve ayrıştırıcı bağımlılıkları yalnızca CI içindir ve özetlerle kilitlenir.

Açık `.github` deposu, kendi dosyası olmayan depolara varsayılan katkı dosyaları sağlar. Mevcut yerel şablonlar önceliklidir. CI akışları ve CODEOWNERS her depoda ayrıca yapılandırılır; varsayılan dosyalar dal kurallarını zorunlu kılmaz. [GitHub varsayılan dosya kuralları](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file).
