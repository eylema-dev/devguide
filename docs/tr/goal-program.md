# Eylema v0.1 Goal programı ve G00 başlangıç kaydı

Revizyon 2, 11 Ekim 2026. İngilizce kanoniktir. [English](../en/goal-program.md).

Kabul edilen maintainer planı, 24 GB birleşik belleğe sahip tek M4 Pro üzerinde deneysel uçtan uca macOS yürütümünü hedefler: yerel birinci taraf Rust servis/CLI, CPU/Metal çıkarımı, tarayıcı Rust/Wasm/WebGPU görünümü, yerel sınırlı Unsloth eğitimi ve gerçek Codex/Claude geliştirme teslimi. Linux ve ikinci fiziksel cihaz kabulü sonraya kalır. G03 ürün sözleşmelerini bu kapsamla uyumlu hâle getirdi; kabul edilen G04 ortam denemeleri ürün kabulünden ayrı kalır. G00 çalışma zamanı, model, eğitim veya benchmark teslim etmez.

Makine tarafından okunabilen [Goal kartları](../../records/goal-index.json), aşağıdaki her satırın amaç, kapsam, base SHA, sözleşme sürümleri, kabul/kontrol eşlemesi, sınırlı bütçe, rol, teslim ve devir alanlarını içerir. EYL kimlikleri korunmuştur; issue oldukları varsayılmaz. G00 başlangıçta yalnız [issue #2](https://github.com/eylema-dev/devguide/issues/2) oluşturdu. G05, 47 issue için ayrı [sürümlü takip kaydı](../../records/goal-tracking.json) ve [gerçek GitHub iş yönetimi](github-work-management.md) ekler; yukarıdaki sabit kartlar tarihsel kalır.

Kart bir yürütüm önerisidir; yetki veya kabul edilmiş bağımlılık değildir. Başlatmadan önce güncel main/politikayı oku, kabul edilmiş bağımlılık SHA’larını ve issue bağlantısını bağla, bağlı depoların kesin yollarını belirt, gerçek model/ayar/rolleri kaydet ve gerekli kapsam kabulünü al. Aynı anda tek uygulama Goal’i yürür. Her teslim kapsamlı dal, AGENTS komutları, ilgili davranış kontrolleri, iki dilin anlam/fingerprint incelemesi, PR, tam head üzerinde ayrı inceleme ve gerçek maintainer merge kararı gerektirir. Varsayılan sınır 120 aktif dakika ve üç hedefli onarımdır; sayısal token bütçesi veya yeni harcama atanmaz. Çözülemeyen hata, eksik yetki/donanım/erişim veya bütçe aşımında durulur.

## Başlangıç kanıtı

Zaman damgalı [başlangıç kaydı](../../records/g00-baseline.json), on deponun güncel main commit/ağaçlarını, rollerini, commit bağlı kontrollerini, klasik koruma ve uygulanan kurallarını, ortak politika hash’lerini ve mevcut 14 çalışma ağacının özetlerini içerir. Canlı kayıt değil, tarihsel kanıttır. `tools/repository-set.json` ayrı kabul edilmiş entegrasyon pin kümesi olarak kalır; güncel main SHA’ları pinlerin yerine geçirilmez.

Çekirdekte zorunlu `repository-checks`, güncel tabana dayanma, adminlere uygulama ve konuşma çözümü vardır; zorunlu inceleme onayı sıfırdır. Kayıt anında diğer dokuz depoda klasik koruma dönmedi ve uygulanan kural/ruleset yoktu. Ayarlar değiştirilmez. CI depo kontrollerini kanıtlar; Rust/GPU/model/eğitim yürütümünü kanıtlamaz. Projects erişimi sınanmaz ve isteğe bağlıdır. 12 Ekim 2026 tarihli [Apache-2.0 kararı](licensing.md) G06 lisans seçimini kapatır; bağlantılı PR incelemesi, varlık kökeni ve dağıtım kabulü ayrıdır.

Kirli çekirdek ve eş depolar korunur: reset, temizlik, dal değiştirme, stash veya ilgisiz işi commit etme yapılmaz. Özel yerel doğrulama kesin yol/durum/dosya özetlerini kullanır; kamu kaydında yalnız taşınabilir takma ad ve hash bulunur. HEAD, dal, izlenen/ignore edilmeyen izlenmeyen dosya baytları ve durum önce/sonra eşleşmelidir. Ignore edilen cache’ler bayt denetimi dışında kalır ve değiştirilmez. G00 kayıtlı main’den yeni temiz devguide checkout’unda çalışır.

## Goal indeksi

| Goal | Ana depo | Bağımlılıklar | Kabul kanıtı |
|---|---|---|---|
| **G00 — Başlangıç kaydı** | `eylema-dev/devguide` | Yok | Her deponun rolü, başlangıç revizyonu ve Goal bağımlılıkları izlenebilir; mevcut çalışma korunmuş |
| **G01 — Taşıma kontrolünü ayır** | `eylema-dev/devguide` | G00 | Yeni ve gözden geçirilmiş belge değişikliği geçer; bozulmuş tarihsel kanıt, kopuk bağlantı ve eski kopyanın geri getirilmesi reddedilir |
| **G02 — Uygulama aşaması kontrolleri** | `eylema-dev/devguide` | G01 | Kontrolsüz Rust kaynağı hâlâ reddedilir; gerçek Rust kapıları olan onaylı profil kabul edilir; ortak araç hash’leri tutarlı |
| **G03 — macOS sözleşmesi** | `eylema-dev/eylema-docs-en` | G02 | API/şema/roadmap uyumlu; Linux ve ikinci cihaz hedefleri açıkça sonraya taşınmış |
| **G04 — Geliştirme ortamı** | `eylema-dev/eylema` | G03 | Gerçek ARM64 derleme/çalıştırma ve Metal araç kontrolü; ortam tekrarlanabilir kayıtla sabitlenmiş |
| **G05 — GitHub çalışma düzeni** | `eylema-dev/devguide` | G02, G03 | İşler Goal’lere bağlı; gerekli CI kaynakları gözlenmiş; yetkili ayar değişiklikleri API’den doğrulanmış |
| **G06 — Dağıtım ve haklar** | `eylema-dev/devguide` | G00 | Lisans ve katkı şartları senin gerçek kararınla kaydedilmiş; üçüncü taraf bildirimleri belirlenmiş |
| **G07 — Rust workspace ve CI** | `eylema-dev/eylema` | G02, G03, G04 | Rust kaynaklarıyla aynı değişiklikte gerçek kontroller etkin; üretim bağımlılık envanteri temiz |
| **G08 — Tipli sözleşmeler** | `eylema-dev/eylema` | G07 | Geçerli/geçersiz örnekler ve sürüm testleri; istemciler aynı semantiği kullanıyor |
| **G09 — Kodlama ve kimlik bağları** | `eylema-dev/eylema` | G08 | Bozuk/taşan veri reddi; kanonik örnekler aynı hash’i üretir; native/Wasm paylaşımı doğrulanır |
| **G10 — Deterministik yürütücü** | `eylema-dev/eylema` | G08, G09 | Başarı, hata, yetkisiz işlem, tekrar teslim, deadline ve bütçe testleri geçer |
| **G11 — İnsan denetimi** | `eylema-dev/eylema` | G10 | Yanlış veya süresi dolmuş onay etkisiz; durdurma isteği ile etkili duruş ayrı; geç durdurma sonucu bozmaz |
| **G12 — Yerel journal** | `eylema-dev/eylema` | G10 | Kesik yazma, bozuk kayıt, disk hatası ve uyumsuz format açık sonuç verir |
| **G13 — Yeniden açma ve recovery** | `eylema-dev/eylema` | G11, G12 | Aynı kimlikler ve sonuçlar geri gelir; tamamlanmış etki yinelenmez; belirsizlik saklanır |
| **G14 — Yerel HTTP servisi** | `eylema-dev/eylema` | G09, G10, G11, G12, G13 | Origin, yetki, sınır, timeout ve bozuk istek testleri; arayüz yetkiyi atlayamaz |
| **G15 — CLI** | `eylema-dev/eylema` | G14 | CLI ile web aynı execution kimliklerini ve hata kodlarını kullanır |
| **G16 — Web görev konsolu** | `eylema-dev/eylema` | G14, G15 | Bu Mac’te gerçek tarayıcı akışı; yenileme/bağlantı kopması sonrası doğru durum |
| **G17 — Dış tüketici örneği** | `eylema-dev/eylema-examples` | G16 | Oluştur–çalıştır–incele–durdur–yeniden başlat–geri aç akışı; F1–F7 kabul senaryoları |
| **G18 — Ölçüm altyapısı** | `eylema-dev/eylema-evals` | G17 | Sürüm/ortam bağlı, tekrar edilebilir ölçüm; başarısız ve ölçülmemiş değerler korunur |
| **G19 — Metal işçisi** | `eylema-dev/eylema` | G18 | Gerçek M4 üzerinde hesaplama/readback; hatalı boyut, işçi kaybı ve kaynak temizliği testleri |
| **G20 — WebGPU görünümü** | `eylema-dev/eylema` | G17, G18 | Gerçek Chrome/WebGPU görüntüsü; seçim/hareket; destek yokluğu ve device-loss davranışı |
| **G21 — Kaynak yöneticisi** | `eylema-dev/eylema` | G19, G20 | Yoğunluk altında kontrollü kuyruk; sınırsız allocation yok; ölçülen durdurma gecikmesi |
| **G22 — Birleşik GPU kabulü** | `eylema-dev/eylema-evals` | G21 | Frame-time dağılımı, gecikme ve bellek raporu; sekme kapanınca native işin sürdüğü gösterilir |
| **G23 — CPU tensor referansı** | `eylema-dev/eylema` | G18, G27 | Bağımsız referans vektörleri; taşma, geçersiz shape ve NaN senaryoları |
| **G24 — Metal tensor işlemleri** | `eylema-dev/eylema` | G19, G23 | Önceden tanımlı toleranslarla CPU/Metal karşılaştırması; gerçek GPU yürütüm kaydı |
| **G25 — Yerleşim görevi** | `eylema-dev/eylema-examples` | G20, G23 | Sabit görev tohumları, açık kurallar ve tekrar üretilebilir sonuçlar |
| **G26 — Küçük öğrenilmiş modeller** | `eylema-dev/eylema` | G24, G25 | Ayrılmış görevlerde kapalı döngü başarı, çok adımlı hata ve ihlal ölçümü; baseline karşılaştırması |
| **G27 — Model sözleşmesi** | `eylema-dev/eylema-models` | G03, G18 | Tam kaynak revizyonu, hash’ler, haklar ve desteklenecek dar konfigürasyon sabitlenmiş |
| **G28 — Ağırlık yükleyici** | `eylema-dev/eylema` | G09, G27 | Bozuk offset, yanlış dtype/shape, eksik tensor ve değiştirilmiş artifact reddi |
| **G29 — Tokenizer ve şablon** | `eylema-dev/eylema` | G27 | EN/TR ve Unicode örneklerinde referansla aynı token kimlikleri |
| **G30 — CPU model yürütümü** | `eylema-dev/eylema` | G23, G28, G29 | Katman/logit referansları, context sınırı, durdurma ve tekrar üretilebilir testler |
| **G31 — Metal model yürütümü** | `eylema-dev/eylema` | G24, G30 | Aynı modelin M4 Metal’de gerçek çalışması; sayısal uygunluk ve kaynak sınırları |
| **G32 — Dil ile görev verme** | `eylema-dev/eylema` | G22, G26, G31 | LLM, policy ve 3D birlikte çalışır; yanlış öneri yetkisiz etki doğurmaz; bulut fallback yok |
| **G33 — Episode ve düzeltme** | `eylema-dev/eylema` | G32 | Eğitim izni olmayan içerik eğitim kuyruğuna girmez; gözlem ve öğretmen önerisi ayrıdır |
| **G34 — Veri sürümü** | `eylema-dev/eylema-training` | G33 | Aynı episode türevleri bölümler arasında sızmaz; her örnek kaynağına izlenebilir |
| **G35 — Yerel Unsloth tarifi** | `eylema-dev/eylema-training` | G27, G34 | Bu M4’te tamamlanmış bounded training run, checkpoint ve kaynak kaydı |
| **G36 — Export ve yeniden kabul** | `eylema-dev/eylema-training` | G31, G35 | Tokenizer/sayısal/görev uygunluğu; bağımsız görevlerde mevcut modele karşı sonuç |
| **G37 — Model seti ve rollback** | `eylema-dev/eylema-models` | G36 | Aynı Mac’in farklı yüklerinde ölçülmüş atama; başarısız canary geri alınır; devam eden görevlerin sürümü belirli |
| **G38 — Geliştirme koordinatörü** | `eylema-dev/eylema` | G05, G17 | Bütçe, iptal, eksik bilgi ve onarım sınırları çalışır; issue metni yetki sayılmaz |
| **G39 — Kontrollü çalışma alanı** | `eylema-dev/eylema` | G38 | Yol kapsamı, kirli checkout ve süreç sahipliği testleri; sırlar uygulayıcı çıktısına sızmaz |
| **G40 — Codex adaptörü** | `eylema-dev/eylema` | G39 | Gerçek çağrı, yapılandırılmış çıktı, timeout, quota ve model bulunamaması davranışı |
| **G41 — İkinci adaptör** | `eylema-dev/eylema` | G39 | Aynı sözleşme senaryoları gerçek sağlayıcıda çalışır; erişim ve sürüm kaydı vardır |
| **G42 — GitHub teslimi** | `eylema-dev/eylema` | G38, G39, G40, G41 | Belirsiz cevap sonrası sorgulama; tekrar denemede aynı PR; token görev kodundan ayrıdır |
| **G43 — Gerçek geliştirme kabulü** | `eylema-dev/eylema` | G42 | İhtiyaç, kod, test, ayrı inceleme ve gerçek PR zinciri; süre, müdahale ve onarım ölçümü |
| **G44 — Tam macOS kabulü** | `eylema-dev/eylema` | G07, G08, G09, G10, G11, G12, G13, G14, G15, G16, G17, G18, G19, G20, G21, G22, G23, G24, G25, G26, G27, G28, G29, G30, G31, G32, G33, G34, G35, G36, G37, G38, G39, G40, G41, G42, G43 | Tek makinede görev, GPU, model, eğitim, promotion/rollback ve PR akışı; tüm kanıtlar aynı aday sürüme bağlı |
| **G45 — Deneysel dağıtım paketi** | `eylema-dev/eylema` | G06, G44 | Artifact hash’leri, dependency inventory, destek sınırları ve tekrar kurulum kanıtı; yayın kararı için hazır paket |
| **W01 — Website doğruluğu** | `eylema-dev/eylemadotdev` | G03; G44 çalışan ürün anlatımı için | EN/TR içerik doğru; DNS/TLS ayrı doğrulanmış; yayın yapılırsa Git/Actions/live SHA eşleşmiş |

## Sıra, riskler ve devir

Sayısal sırayı değil bağımlılık grafiğini izle: G18 ve G27, G23’ten önce gelir; G38–G43, GPU/eğitimi beklemeden M2 sonrasında yapılabilir. G06 lisans seçimi kararlaştırılmıştır; bağlantılı teslimatın inceleme ve köken kabulü G45 için gereklidir. W01 içeriği G03 sonrası hazırlayabilir; çalışan ürün anlatımı G44 gerektirir. Bütün M1–M7 gerekleri G44’e bağlanır. M0–M7 ve EYL-001–008 plan kimlikleridir; gerçek milestone/issue bağlantılarını G05 oluşturur.

G01 değişmez taşıma kanıtını güncel belge kontrolünden ayırır; G02 Rust kabulünden önce gerçek uygulama kapılarını ekler. G03 macOS planını ürün sözleşmeleriyle uyumlar. Kurulu Unsloth, seçilen Qwen3-0.6B veya önerilen Rust 1.99.0 desteği kanıtlamaz; kendi Goal’lerinde sınanırlar. Metal ve WebGPU ayrı bağlamlardır; ortak kuyruk/evrensel sıfır kopya varsayılmaz. Aynı cihazın farklı yük profilleri iki cihaz değildir. Ağırlık, özel eğitim örneği veya kimlik bilgisi kamu Git’ine konmaz.

G00 başlangıç kaydı, tüm kartlar, PR kontrolleri, koruma denetimi ve ayrı incelemeyi devreder. G01 ancak maintainer G00’ı kabul ettikten ve kabul edilmiş main SHA bağlandıktan sonra başlar. Geri dönüş kapsamlı revert PR’ıdır. Kabul edilen yollar, bütçe ve karar kaydı için [G00 çalışma planına](../plans/g00-baseline.md) bak. Güncel durumlar ve kabul edilen teslimler ayrı G05 kaydında tutulur; sabit kart tamamlanmayı kanıtlamaz.

## Kabul edilen öncelik güncellemesi — 12 Ekim 2026

[Güncel ürün kararları](https://github.com/eylema-dev/eylema-docs-tr/blob/main/docs/project-structure.md), isteğe bağlı model/eğitim tamamlanmadan kullanılabilir M2 görev konsolu önizlemesini ve sınırlı tek ihtiyaçtan PR’a kanıtı önceler. G38–G43 kabul edilmiş M2/G17 temelinden yürütülebilir; tam G44/G45 sürümü bütün kabul kapılarını korur. Mac mini M4/24 GB ve Linux RTX 4070 Ti Super/16 GB VRAM + 32 GB RAM, birincil M4 Pro hedefini değiştirmeden veya yeni backend desteği iddia etmeden sahibinin bildirdiği test envanterine katılır. Tarihsel Goal kartları ve kabul edilmiş yürütüm kanıtları korunur.
