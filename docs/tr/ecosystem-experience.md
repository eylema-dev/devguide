# Özel öğrenme ve paylaşılabilir ekosistem deneyimi

Eyleme, ekosistemi olan bir eylemci platformudur: değiştirilebilir yerel açık ağırlık uzman modelleri, kendi Rust motorlarımız, sabit rol arayüzleri ve harness araçları üzerinden işbirliği yapar. Tamamlanan işin kalitesi, kaynak verimliliği, gizlilik sınırları ve tekrarlanabilir gelişim birlikte ölçülür. Eyleme kaynak kodunun kontrollü geliştirilmesi, sahibin görev/merge yetkisi altında uygunluğu onaylanan güçlü dil modeli katkısı ve gerçek ayrı AI incelemesi kullanır. Tartışma, fikir ve hata bildirimi açık kalır. Yerel ürün kullanımı dışarıdaki büyük bir modeli zorunlu kılmaz; açıkça yapılandırılmış dış roller kendi veri/çağrı yetkisini gerektirir.

Bu belge hedef tasarım ve kabul sözleşmesidir; bütün çıkarım, modele özel eğitim, RAG veya kurum kurulumu bileşenlerinin çalıştığını iddia etmez. [Güncel aksiyon planı](platform-action-plan.md), [kaynak danışmanı](model-resource-planning.md) ve [katkı politikası](contribution-model-policy.md) uygulama kapılarını bağlar.

## Biriken değerin iki hedefi

| Hedef | Uygun içerikler | Gerekli sınır |
| --- | --- | --- |
| Özel proje veya kurum | Proje kapsamındaki memory/RAG/fine-tune için izinli gözlem, düzeltme, bilgi, değerlendirme ve öğrenme türevleri | Varsayılan özel; proje/kurum/amaç erişimi, saklama ve toplama/okuma/erişim/eğitim izinleri uygulanır; ekosistem dışa aktarımı doğmaz |
| İncelenen ekosistem adayı | Genelleştirilmiş, anonimlik incelemesinden geçmiş dersler, reçeteler, model/profil seçimleri, sentetik veya açıkça paylaşılabilir diğer veriler, değerlendirme ve kaynak ölçümleri | Depoya kabul öncesi ayrı açıklama/dışa aktarma/yayın yetkisi, kaynak ve türev hakları, köken ve yeniden kimliklendirme incelemesi |

Bir kayıt sonsuza kadar özel kalabilir ve sahibinin yerel sistemini yine geliştirebilir. Açık model ağırlıkları görev verisini, RAG kaynaklarını, promptları, düzeltmeleri, embeddingleri, adaptörleri veya eğitim türevlerini kamuya açmaz. Eyleme kaynak kodunu yayımlamak kullanıcı kayıtlarını yayımlama yetkisi vermez. Paket adayı yayın değildir; paket içe almak yürütme veya proje erişimi değildir.

## Gelişim döngüsü

1. Yalnız izinli türlenmiş sonuçları kaydet: öneri, denenmiş araç eylemi, gözlenen sonuç, insan düzeltmesi, hata ve bilinmeyen ayrılır. Görev/model/profil/reçete sürümleri ve kanıt durumu kaydedilir; ham sohbetler, özel muhakeme, erişim bilgileri ve kısıtlı içerik ekosistem adaylarına alınmaz.
2. Kaynak, amaç, toplama/erişim/eğitim/açıklama/dışa aktarma hakları, kapsam, saklama ve geri çekme kökenini bağla. Türetilen her özet, embedding, veri kümesi, adaptör veya reçete örneği kısıtlarını taşır.
3. Özel kapsamlı memory/RAG ve modele özel eğitim girdilerini düzenle. Eğitim/holdout ayrımında bölüm aileleri ve türevleri birlikte tutulur; dış model önerileri ölçülmüş sonuçlar ve insan kararlarından ayrılır.
4. Aday iyileştirmeleri değişmez holdoutlar ve bütün döngü kalite/kaynak/gizlilik kapılarıyla değerlendir. Native Rust operatör/profil desteği, canary ve geri dönüş kanıtı etkinleştirmeden önce gelir; yeni model adı, popüler reçete veya katalog içe alma bunları atlayamaz.
5. Ayrıca izin verilirse sınırlı bir ekosistem adayını genelleştir. Tanımlayıcı alanları kaldır veya dönüştür; dolaylı tanımlayıcıları, nadir olayları, bağlantılama ve yeniden oluşturma risklerini incele. Takma kimlik veya maskeleme tek başına anonimliği kanıtlamaz; eksik hak veya çözülmemiş risk adayı uygunsuz bırakır.
6. Tam paketi, kökeni, koşulları, süre/iptal durumunu ve hedefi incele. Gerçek yetkili yayın incelemeden sonra gelir; içe alma kısıtları korur ve uyumlu incelenmiş etkinleştirmeye kadar hareketsiz kalır. Doğrulanmış izinli dersler kaynak geliştirmesine ve yerel kullanıma geri beslenir.

Modeller ve yürütme ayrıntıları gelişebilir; rol anlamı, yetki sınırları, köken ve kanıt kuralları sürümlenir. Gelecek kurum profili kendi izolasyonunu ve çalışma ortamını kanıtlamalıdır; yerel konsol testi kurum kurulumu kabulü değildir.

## Planlanan Goal kabulü

| Goal | Gerekli ek kanıt |
| --- | --- |
| G33 bölümler | Kaynak geliştirme ve ürün içi derslerin ayrımı, gözlenen/önerilen/düzeltilen durumu, özel kapsam ve toplama/erişim/eğitim/açıklama/dışa aktarma izin hataları |
| G34 veri kümesi sürümü | Özel kurum RAG/eğitim yolları, devralınan türev kısıtları, geri çekme ve ilişkili bölüm holdout izolasyonu; otomatik kamuya dönüşüm yok |
| G64 paylaşım adayı | Sentetik doğrudan/dolaylı tanımlayıcı ve bağlantılama hataları, ayrı dışa aktarma/yayın hakları, paket kökeni ve belirsiz anonimlik reddi |
| G65 ekosistem kabulü | Tam incelenmiş paket kimliği/koşulları/kökeni, uyumluluk ve iptal edilmiş/süresi dolmuş/uyuşmayan hakların reddi; otomatik indirme/yürütme/eğitim/etkinleştirme yok |

Geri çekme gelecekteki kullanımı/kabulü durdurur ve denetlenen yerel türevlere yayılır. Zaten kamuya açık Git paketleri ve dış kopyalarda politika, ulaşılabilir kaldırmaları ve kalan açıklığı dürüstçe anlatmalıdır; bütün klonların geri alınacağını vaat edemez. Kamuya açık depolar, açık hedef kurallarıyla yalnız incelenmiş uygun paket/reçete/metaveriyi taşır; kullanıcı faaliyetleri varsayılan olarak buraya dökülmez.

Bu belge revizyonu kullanıcı verisi toplamaz, anonimleştirmez, dışa aktarmaz veya yayımlamaz. G33/G34/G64/G65 planlı kalır; kabul edilmiş G63 yerel sınır kanıtı test edilen kapsamda kalır. Mevcut bağımlılıklar, bütçeler, kabul geçmişi ve engelli G40 hakları değişmez.
