# Rust model harness aksiyon planı

Sürüm **1.1.0**, 13 Ekim 2026. İngilizce kanoniktir; [English](../en/platform-action-plan.md).

Bakımcı Eylema’yı yerel açık ağırlık modelleri ve isteğe bağlı açıkça yapılandırılmış dış büyük modellerin güçlü yanlarını birleştirerek planlanan işi tamamlayan birleşebilir Rust harness olarak istedi. Yerel inference kendi Rust motorumuzda kalır. Dokuz rol sabit arayüzdür; ses STT/TTS, görsel algı ve alan metin profilleri ayrı kabul edilir. RAG/embedding, özel proje kayıtları ve izinli ekosistem paketleri birinci sınıf iştir. [Mimari ve model örnekleri](https://github.com/eylema-dev/eylema-docs-tr/blob/main/docs/architecture.md#rust-harness-model-rolleri-ve-alana-göre-seçim) planı bağlar; [güncel kartlar](../../records/platform-goal-plan.json) İngilizce kanoniktir.

Kabul edilen yirmi dört Goal değişmez kanıtını korur. Kalan yirmi üç özgün kart issue kimliğini ve her özgün zorunlu bağımlılığı tutar; G46–G90 ayrı incelenebilir kırk beş parça ekler. Tarihsel [G00 kartları](../../records/goal-index.json) ve [takip](../../records/goal-tracking.json) tamamlanma diye yeniden yazılmaz. Revizyon runtime/model/performans kanıtı değildir. G06 lisans seçimi kesinleşmiştir, teslimi açıktır. G40 mevcut PR #59’da sıfır yeni süre/onarım/çağrı/gizlilik hakkıyla engelli kalır; bu revizyon provider/host/crash denemesi açmaz.

## Mevcut temelin yeniden değerlendirilmesi

Bu, kabul edilmiş kanıtın uyumluluk değerlendirmesidir; yeniden koşu veya geçmiş kabulün geriye dönük genişletilmesi değildir. Değişmez geçmiş tracker kesin teslimatları kaydeder. Yeni kullanıcı isteği gelecek sözleşmeleri güçlendirir ve şu kullanım/düzenlemeleri yönlendirir:

| Mevcut çalışma | Korunan değer | Gereken değişiklik veya eksik kanıt |
|---|---|---|
| G07–G09 workspace, görev sözleşmeleri ve codec | Kendi Rust'ımız, sınırlı türlü kayıtlar ve açık biçim sürümleri | G46'da platform rol/döngü/profil arayüzleri eklenir; yalnız ürün adı için görev/wire sürümü değiştirilmez |
| G10–G13 yürütme, gözetim ve kalıcı kurtarma | Deterministik etkiler, açık yetki, etkili durdurma ve replay sınırları | G54/G63'te harness araç/döngü ve özel veri soyu bağlanır; uzlaştırma bilinmeyen etkileri tekrar etmemeli |
| G14–G17 yerel servis, CLI, tarayıcı ve consumer | Tek servis sözleşmesi, loopback UI ve yeniden üretilebilir dış consumer | G73'te gerçek insan kaydı/yetkisi tamamlanır; otomasyon fixture'ları gerçek insan oturumunu kanıtlamaz |
| G18–G22 ölçümler, native Metal, WebGPU ve ortak bütçeler | Kayıtlı kapsamda adı belirtilmiş cihaz compute ve birleşik iş yükü kanıtı | G50/G80–G82'de eşzamanlı kabul edilmiş model/RAG/eğitim hesabı genişletilir; mevcut GPU çalışması model kernel veya eğitim kanıtı değildir |
| G38–G39 geliştirme protokolü/yalıtım | Sınırlı provider-neutral iş ve yayımlama erişiminden ayrım | Araç/iyileştirme işleri için kullanılır; G40 çözülmemiştir ve yeni host/provider/gizlilik hakkı almaz |
| Kalan model/öğrenme önerileri | Artifact, haklar, referans ve holdout kapıları | Değiştirilebilir roller, kendi Rust inference/eğitimimiz, router/RAG, skill, native LoRA/QLoRA ve izinli ekosistem türevleri için revize edilir |

Kabul edilmiş ilk görev konsolu temel olarak korunur. Önceki tam 3D yerleştirme sürüm yolu tam kabul için zorunlu kalır; G72 bağımsız erken özel metin/RAG iş kanıtı sağlar. Model değişimi sözleşme uyumunu, aktif iş kimliğini ve değerlendirme kanıtını korur; başarısız yeteneği doğrulanmamış iddiayla değiştiremez.


## Yürütme sözleşmesi

- Aynı anda bir uygulama Goal’i. **G46** ile başla; ardından proje sınırı **G63**, türlü araç **G54** ve kanıt **G50**; sayısal kimlik yerine kabul edilmiş bağımlılıkları izle.
- Etkinleştirmeden önce güncel main/policy, kabul edilen bağımlı SHA, tam yollar, gerçek roller/model/effort, referans/kalite/kaynak sınırları ve sonlu artifact/süreç/deneme sınırlarını bağla. Planlanan ayar `gpt-6.1-sol / high`; bilinmeyen gerçek kimlik bilinmeyen kalır.
- Yeni Goal başına varsayılan 120 aktif dakika, üç hedefli onarım ve on beş ayrı inceleme dakikası; sayısal token bütçesi veya yeni harcama yoktur. Hakkı tükenen iş sıfırlanmaz. İlk eğitim adayı bir kalır. Provider erişimi ve ücretli çağrı kayıt metni yerine gerçek yetki ister.
- Her Goal öncesi/sonrası onarım/inceleme dahil özel [tüketim defterini](usage-accounting.md) yenile. Ham kayıt, ağırlık, erişim bilgisi ve özel proje verisi public Git’e girmez.
- Tam AGENTS kontrollerini ve eşlenen native/model/tarayıcı/veri/davranış testlerini çalıştır. not_run ayrıdır. Sayısal kabulü başlangıç ölçümünden sonra, aday karşılaştırmasından önce sabitle; tam döngü faydasını ve rol çıkarma deneyini karşılaştırılabilir kaynakta ölç.
- Ayrı inceleme son head’e bağlanır. Güncel CI ve bakımcı merge yetkisi ayrıdır. Kabul edilen kartı merge et, main sürümünü bağla, sonra bağımlı işi etkinleştir. Geri dönüş incelenen scoped revert PR’dır; iptal/model rollback tamamlanan etkiyi geri almaz.

## Güncel uygulama sırası ve kartlar

Tablo bağımlılığa uygun sıradır; tamamlanma veya tarih sözü değildir. Her satırın amacı, tam etkinleştirme yükümlülüğü, yolları, kabul/kontrol eşlemesi, sonlu bütçesi ve issue’su kanonik kayıttadır. Bağımsız işler G40’ı beklemeyebilir; zorunlu sürüm/provider kapıları kaldırılmaz.

| Goal | Teslimat | Bağımlılıklar | Durum |
|---|---|---|---|
| **G46** | Döngü, rol ve model bağlama sözleşmeleri | G08, G09, G13, G17, G39 | `accepted` |
| **G63** | Projeye özel veri ve çıkış sınırları | G46, G13 | `accepted` |
| **G87** | Bellek sözleşmeleri, yönlendirme ve yaşam döngüsü | G46, G63 | `accepted` |
| **G54** | Türlü araç kaydı ve harness eylem yürütmesi | G46, G10, G11, G13, G39, G63 | `planned` |
| **G50** | Karar kanıtı ve döngü ölçümleri | G46, G54, G18, G63 | `planned` |
| **G75** | Sürümlü skill sözleşmesi ve yeniden kullanım paketleri | G46, G54, G50, G63, G87 | `planned` |
| **G73** | Gerçek insan harness yetkisi ve durdurma | G46, G11, G14, G16, G63 | `planned` |
| **G27** | Model sözleşmesi | G03, G18, G46 | `planned` |
| **G56** | Açık ağırlıklı yapılandırılmış karar modeli profili | G27, G46 | `planned` |
| **G67** | Embedding artifact ve erişim davranış profili | G27, G46 | `planned` |
| **G80** | Kontrollü kaynak ihtiyacı tahmini | G27, G46, G21, G18 | `planned` |
| **G23** | CPU tensor referansı | G18, G27 | `planned` |
| **G28** | Ağırlık yükleyici | G09, G27 | `planned` |
| **G29** | Tokenizer ve şablon | G27 | `planned` |
| **G30** | CPU model yürütümü | G23, G28, G29 | `planned` |
| **G57** | Kendi Rust CPU yapılandırılmış karar yürütmemiz | G56, G23, G28, G29, G30 | `planned` |
| **G68** | Kendi Rust CPU embedding yürütmemiz | G67, G23, G28, G29 | `planned` |
| **G70** | Projeye bağlı kendi Rust erişim indeksimiz | G68, G63, G13 | `planned` |
| **G74** | Karar router’ı ve RAG/skill yönlendirmesi | G57, G54, G50, G70, G75, G63, G87 | `planned` |
| **G88** | Kendi episodik, semantik ve knowledge graph belleğimiz | G87, G70, G50 | `planned` |
| **G72** | Erken uçtan uca yerel metin/RAG iş kanıtı | G30, G57, G68, G70, G54, G50, G63, G73, G88 | `planned` |
| **G24** | Metal tensor işlemleri | G19, G23 | `planned` |
| **G25** | Yerleşim görevi | G20, G23, G46, G54 | `planned` |
| **G31** | Metal model yürütümü | G24, G30 | `planned` |
| **G81** | Ölçülen donanım kalibrasyonu ve kapasite profilleri | G80, G18, G31 | `planned` |
| **G69** | Kendi Rust Metal embedding yürütmemiz | G68, G24, G21 | `planned` |
| **G58** | Kendi Rust Metal yapılandırılmış karar yürütmemiz | G57, G24, G31 | `planned` |
| **G49** | Algı modeli artifact ve operatör profili | G27, G46 | `planned` |
| **G52** | Kendi Rust CPU algı yürütmemiz | G49, G23, G28, G29, G30 | `planned` |
| **G53** | Kendi Rust Metal algı yürütmemiz | G52, G24, G31 | `planned` |
| **G59** | Ayrı STT ve TTS artifact/operatör profilleri | G27, G46 | `planned` |
| **G76** | Modele özel fine-tune ve LoRA/QLoRA profilleri | G27, G46 | `planned` |
| **G83** | Kendi Rust gradyan ve eğitim operatörlerimiz | G23, G76 | `planned` |
| **G26** | Küçük öğrenilmiş modeller | G24, G25, G46, G83 | `planned` |
| **G78** | Kendi Rust adaptör yükleme ve birleştirme eşliğimiz | G76, G28, G31 | `planned` |
| **G60** | Kendi Rust CPU ses-yazı yürütmemiz | G59, G23, G28, G29 | `planned` |
| **G61** | Kendi Rust CPU yazı-ses yürütmemiz | G59, G23, G28, G29 | `planned` |
| **G62** | Kendi Rust Metal ses ve birleşik akış yürütmemiz | G60, G61, G24, G21 | `planned` |
| **G47** | XState koordinasyon envanteri ve profili | G46 | `planned` |
| **G48** | Sınırlı iş akışı ve Rust uzlaştırması | G46, G47, G13, G21 | `planned` |
| **G66** | Birleşebilir alt akışlar ve alana göre model seçimi | G46, G48, G54, G63 | `planned` |
| **G55** | Açık dış model rol adaptörü | G46, G54, G39, G63 | `planned` |
| **G32** | Dil ile görev verme | G22, G26, G31, G48, G50, G54, G53, G58 | `planned` |
| **G71** | RAG alt akışı ve kaynaklı iş kabulü | G72, G69, G50, G66, G74, G88 | `planned` |
| **G33** | Episode ve düzeltme | G32, G46, G50, G63 | `planned` |
| **G34** | Veri sürümü | G33, G63 | `planned` |
| **G77** | Ürün içi sınırlı iyileştirme işleri | G76, G34, G63, G75, G39 | `planned` |
| **G84** | Kendi Rust CPU LoRA eğitimimiz | G83, G76, G78, G77, G34 | `planned` |
| **G85** | Kendi Rust Metal LoRA eğitimimiz | G84, G24, G31 | `planned` |
| **G86** | Kendi Rust QLoRA eğitim profilimiz | G85, G76, G78 | `planned` |
| **G64** | Paylaşılabilir ekosistem paket oluşturucusu | G33, G34, G63 | `planned` |
| **G65** | Ekosistem kataloğu ve uyumlu içe alma | G27, G64 | `planned` |
| **G35** | Yerel Unsloth tarifi | G27, G34, G77, G76 | `planned` |
| **G36** | Export ve yeniden kabul | G31, G35, G78 | `planned` |
| **G37** | Model seti ve rollback | G36, G46, G50, G65 | `planned` |
| **G51** | Yeniden kullanılabilir harness uygulamaları ve model değişimi | G32, G37, G48, G50, G54, G55, G66 | `planned` |
| **G89** | Kendi analitik belleğimiz ve iyileştirme snapshot’ları | G87, G33, G50 | `planned` |
| **G82** | Eylema içinde kapasite ve yatırım planlama | G80, G81, G50, G66, G77, G89 | `planned` |
| **G79** | Bütünleşik iyileştirme ve skill terfi kanıtı | G77, G78, G36, G37, G75, G51, G84, G85, G86, G89 | `planned` |
| **G06** | Dağıtım ve haklar | G00 | `planned` |
| **G40** | Codex adaptörü | G39 | `blocked` |
| **G41** | İkinci adaptör | G39 | `planned` |
| **G42** | GitHub teslimi | G38, G39, G40, G41, G54 | `planned` |
| **G43** | Gerçek geliştirme kabulü | G42, G50 | `planned` |
| **G90** | Bellek backend profilleri ve kontrollü veri alışverişi | G88, G89 | `planned` |
| **G44** | Tam macOS kabulü | Tüm özgün sürüm kapıları; G46–G90 | `planned` |
| **G45** | Deneysel dağıtım paketi | G06, G44 | `planned` |
| **W01** | Website doğruluğu | G03 | `planned` |

## Kanıt ve veri sınırları

Projeye özel veri, türev ve embedding varsayılan olarak projede kalır. Paylaşım adayı ekosistem kabulünden önce izin/hak/soy bağı taşır; içe alma etkinleştirme vermez. RAG kaynağı yetki veremez. Dokuz rol birleşebilir isteğe bağlı katılımcıdır; her işte dokuz model çalıştırma zorunluluğu değildir. Model/operatör tanımı native destek değildir. Gerçek yerel kabul artifact/profil/cihaz başına kaydedilir; desteksiz profil açık hata verir.

Yapı/tarihçe/bağımlılık/bütçe için `.venv/bin/python tools/check_platform_plan.py`, salt okunur güncel issue/kabul kanıtı için `--fetch` çalıştırılır. Eski tracker kabul kanıtının tarihsel snapshot’ıdır; live audit’i revize iş listesinin güncel denetimi değildir. Kontrol başarısı incelemeci bağımsızlığını veya runtime/model doğruluğunu kanıtlamaz. İlk sınırlı uygulama planı [G46](../plans/g46-platform-contracts.md) içindedir.

G79, önceden kabul edilmiş native eğitim adayı/checkpoint'ini değerlendirme/terfi ve skill paketlemeye bağlar; sıfır yeni eğitim adayı vardır ve arama hakkını sıfırlamaz.

## Bellek uzantısı

[Bellek katmanı](memory-layer.md) çalışma, episodik, semantik, prosedürel, knowledge graph ve analitik belleği ayırır. G87–G90 sınırlı kendi Rust eklemelerimizdir; SQLite/DuckDB referans/veri alışverişi adayıdır, onaylı motor değildir. Bakımcı CortexDB ile knowledge graph kastettiğini açıkladı. G72 artık G88’i içerir, G74/G75 G87’yi, G79/G82 G89’u gerektirir; bütün yeni kapılar G44’e bağlanır. Güncel kartlar 68 sınırlı kayıt taşır (kalan 23 özgün ve 45 ek); G46 kesin core-main kanıtıyla kabul edilmiştir, G63 ve G87 kesin core-main ve güncel CI kanıtıyla kabul edilmiştir; G88–G90 planlı kalır. Kabul edilmiş geçmiş, özgün gereksinimler ve G40 sınırları değişmez. Kaynak kısıtları embedding, graph ilişkisi, cache, özet, analitik ve eğitilmiş adayı izler. Bellek yetki vermez.
