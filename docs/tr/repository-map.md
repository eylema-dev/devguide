# Organizasyon depo haritası

Revizyon **0.3.0**, 15 Ekim 2026. [English](../en/repository-map.md). Depo oluşturmak, uygulamanın kabul edildiği anlamına gelmez.

| Depo | Sorumluluk |
|---|---|
| [Eyleme](https://github.com/eyleme-dev/eyleme) | Rust çekirdeği, sözleşmeler, CLI ve makine şemaları |
| [eyleme-docs-en](https://github.com/eyleme-dev/eyleme-docs-en) | Kanonik İngilizce ürün sözleşmeleri ve yol haritası |
| [eyleme-docs-tr](https://github.com/eyleme-dev/eyleme-docs-tr) | Türkçe karşılıklar ve tarihsel Türkçe taslaklar |
| [devguide](https://github.com/eyleme-dev/devguide) | Ortak politika, araç kaynakları, depo kaydı ve entegrasyon kontrolleri |
| [.github](https://github.com/eyleme-dev/.github) | Organizasyon profili ve varsayılan katkı şablonları |
| [eyleme-examples](https://github.com/eyleme-dev/eyleme-examples) | Çekirdek API sürümüne sabitlenmiş tüketici örnekleri |
| [eyleme-evals](https://github.com/eyleme-dev/eyleme-evals) | Sentetik örnekler, değerlendirme araçları ve tekrarlanabilir sonuçlar |
| [eyleme-models](https://github.com/eyleme-dev/eyleme-models) | Katalog üstverisi, uyumluluk ve model kümesi manifestleri; ağırlık içermez |
| [eyleme-training](https://github.com/eyleme-dev/eyleme-training) | Eğitim tarifleri, ortam kilitleri ve izinli veri hazırlama |
| [eylemedotdev](https://github.com/eyleme-dev/eylemedotdev) | eyleme.dev üzerindeki açık Eyleme topluluk ve ürün merkezi |

## Açık topluluk ve isteğe bağlı ticari ürünler

Bu depolar, tek **Eyleme** markası altında public ve bağımsız kullanılabilen Eyleme projesini destekler. [eyleme.dev](https://eyleme.dev/tr/), başlangıç adımlarını, belgeleri, örnekleri, katkı yollarını ve ürün bilgisini birleştirir. **Eyleme Derleme** ve **Eyleme Onama**, ücretli abonelik modelini izleyen private kaynak kodlu isteğe bağlı ürünlerdir; ticari hizmetler ve koşullar geliştirme aşamasındadır, fiyatlar ve kullanıma sunulma durumu yayımlanmamıştır. Private depoları başlangıç adımlarının bağımlılığı veya public salt okunur depo kümesi anlık görüntüsünün üyesi değildir. Arayüzleri ve ürün sınırları için [public ürün ailesi açıklamasını](https://github.com/eyleme-dev/eyleme/blob/main/docs/tr/product-family.md) kullanın.

Anlatım sırası **Derleme → Onama → Eyleme** şeklindedir. Bu sıra zorunlu bir abonelik hattı oluşturmaz: public Eyleme temel yerel erişim ve güvenlik kontrollerini korur. Ortak marka örtük yetki veya private kaynak koduna ve müşteri kayıtlarına erişim sağlamaz. [Lisans kapsamı](licensing.md), public topluluk kodunu, private birinci taraf ürünleri ve bağımsız lisanslı varlıkları ayırır.

## Sahiplik ve sınırlar

Çekirdek tek Rust çalışma alanıyla başlar: sözleşme tipleri, deterministik çalışma zamanı, günlük, web arayüzü ve CLI birlikte değişir. Gerçekten bağımsız sürümlenen tüketici oluşmadan her crate veya sağlayıcı için ayrı depo açmayın. API/SDK üreticileri ve GitHub/model sağlayıcı adaptörleri, arayüz ve yaşam döngüsü ayrılmayı gerektirene kadar çekirdek modülleridir. Mimari öneriler ürün belgelerinde, katkı süreci kararları devguide içinde kalır.

Örnekler açık API'leri gösterir; çalışma zamanının çatallanmış kopyalarını taşımaz. Değerlendirmeler iş yüklerini ve ölçüm araçlarını yönetir; çalışma zamanı optimizasyonlarını değil. Model üstverisi lisanslı varlıklara ve kabul edilmiş kanıtlara bağlanır; ağırlıklar ayrıca onaylanmış varlık deposuna aittir. Eğitim tarifleri ve ortam kilitleri eğitim deposundadır; veri kabulü, gizlilik, lisanslar ve hesaplama harcamaları ayrı kabul edilmiş görev gerektirir. Burada varlık deposu, kayıt servisi veya eğitim hizmeti kurulmaz.

Marka varlıkları ve mevcut üretim betiği, ayrı yaşam döngüsü gerekene kadar çekirdekte kalır. Web sitesi mevcut ayrı projedir. Yeni iskeletler Rust, GPU, çıkarım, eğitim, kıyaslama veya örnek uygulama gerçekleştirmiş sayılmaz. Kendi kaynak/belgelerimiz Apache-2.0 kullanır; [varlığa özgü haklar](licensing.md) ayrıdır.

## Gerekçe olduğunda depo ayırın

Yeni deponun farklı sahibi, kitlesi veya sürüm takvimi; açık girdi/çıktı sözleşmesi; görev listesi; aşamasına uygun testler; sürüm/uyumluluk kuralları ve belirli bakım yolu olmalıdır. Bunlar yoksa mevcut sorumlu depoda dizin kullanın. Bağımlılıklar sürümlenen çekirdek sözleşmelerine yönelsin; depolar arası değişiklikleri ilişkili tek görev olarak kaydedin.

## Ortak dosyalar

Politika `devguide/AGENTS.md` ve katkı rehberlerine aittir. Diğer depolar ince yönlendirme dosyaları taşır. Doğrulama uygulamasının kaynağı `devguide/tools/` içindedir; kopyalar `tools/vendor.json` içindeki içerik özetleriyle kaydedilir ve depo kümesi kapısında birlikte denetlenir. Kopyaları PR’larla birlikte güncelleyin; değişken uzak betiği indirip çalıştırmayın. Python ve ayrıştırıcı bağımlılıkları yalnızca CI içindir ve özetlerle kilitlenir.

Açık `.github` deposu, kendi dosyası olmayan depolara varsayılan katkı dosyaları sağlar. Mevcut yerel şablonlar önceliklidir. CI akışları ve CODEOWNERS her depoda ayrıca yapılandırılır; varsayılan dosyalar dal kurallarını zorunlu kılmaz. [GitHub varsayılan dosya kuralları](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file).
