# Yeterliği kabul edilmiş LLM katkı politikası

[İngilizce](../en/contribution-model-policy.md) kaynak dildir. Bakımcının onayladığı politika revizyonu merge edildikten sonraki değişiklik PR'ları için geçerlidir; kabul edilmiş geçmiş kanıt korunur.

## Kapsam ve bakımcı kontrolü

Kod, belge, yapılandırma veya başka değişiklik içeren her PR, mimari ya da uygulamada bakımcının kabul ettiği frontier/SOTA LLM profilinin anlamlı kullanımını ve gerçekten ayrı, bakımcının yetkilendirdiği AI incelemesini gerektirir. Tartışma, fikir ve hata bildirimi model şartı olmadan açıktır; bunlardan doğan değişiklik PR'ları bu politikayı izler. İnsan uzmanlığı ve ek incelemeler değerlidir. Eyleme geliştirmesi bu yeterliği kabul edilmiş büyük model sürecini kullanır; ürün işleri dış çıkarım gerektirmeden gizlilik odaklı yerel açık ağırlık modelleri birleştirebilir.

Profil kabulü, geçerlilik/iptal, görev yetkisi, PR kabulü ve merge bakımcının kontrolündedir. Gerçek insan kararını yazarın ürettiği metinden ayrı kaydedin; JSON onay metni, model çıktısı, başarılı CI veya katalog kaydı yetki vermez. Yayın kimlik bilgileri model/araç worker'larında bulunmaz. Ayrı inceleme son commit'i ve anlamlı kanıtı bağlar; öz inceleme ya da uydurulmuş insan GitHub onayı değildir. Mevcut koşullu merge izni yalnız gerekli kabul, güncel CI ve gerçek ayrı inceleme geçince uygulanır.

## Tarihli yeterlik

| Gerekli kanıt | Anlamı |
|---|---|
| Sağlayıcı/model/sürüm veya alias, kayıtlı effort ve kanıt kaynağı | İstenen ayar, gözlenen yapılandırma metaverisi ve gizli sunucu kimliği ayrıdır; bilinmeyeni koruyun |
| Değerlendirme tarihi, görev/alan kapsamı ve sabit kalite ölçütleri | Tekrarlanabilir görev sonucu, güvenlik/olumsuz regresyonlar ve sonlu onarım/kaynak sınırları kullanılır; ad veya popülerlik sıralaması yetmez |
| Gerçek sonuç, değerlendirilen revizyon ve bağımsız rapor | Başarısızlık ve düzeltmeleri koruyun; başka görev veya desteklenmeyen alan kendiliğinden yeterlik sayılmaz |
| Bakımcı kararı, geçerlilik aralığı, iptal ve politika/profil revizyonu | Önerilen profil gerçek bakımcı kararına kadar bekler; eski, iptal edilmiş veya uyumsuz profil değişikliği kabul ettiremez |
| Yazar ve inceleyen rol bağları | Aynı kabul edilmiş yapılandırılmış model gerçekten ayrı bağlamlarda kullanılabilir; her rolün gerçek ayarı ve kanıtı kaydedilir |

Bakımcının kabul ettiği katkı profili kapsamı belirli bir yönetişim kararıdır; doğrulanmış global SOTA sıralaması iddiası değildir. Bakımcı ilk sınırlı [profil kaydını](../../records/contribution-model-profiles.json) kabul etti: kayıtlı `gpt-6.1-sol / high`, tarihli G27 sözleşme/katalog/belge kanıtı, 13 Kasım 2026 sonuna kadar geçerli. Bu kapsamı sınırlı bakımcı yeterliğidir; sayısal kernel ve çıkarım/eğitim performansı ayrı değerlendirme ister. Gizli sunucu kimliğini açmayan sağlayıcı dürüstçe belirtilir; gözlenen yapılandırma kanıtının ilan edilen güven seviyesine uyup uymadığına bakımcı karar verir. Bilinmeyen yapılandırılmış kimlik veya kabul edilmemiş değerlendirme sessizce başka modelle değiştirilemez.

Gelecek değişiklik görevi başlamadan güncel uygun profil, insan görev kararı, tam base/dosya kapsamı, sonlu bütçe ve gerçek ayrı inceleme bağlanır. Eksik veya süresi dolmuş yeterlikte uygulama/PR kabulü bekler. Yeni model, effort, sağlayıcı, alan veya politika değişikliği ilan edilmiş kapsamda yeniden değerlendirilir; model kendiliğinden değiştirilmez. G42/G43 ileride gerçek bakımcı kontrollü kabul/teslim ve aşma denemelerinin kabulünü sağlar. Bugünkü şablon ve CI yapıyı ve depo verisini kontrol eder; SOTA kimliğini, insan kararını veya otonom teslimi doğrulamaz. Bu politika geçişi önceden yetkilendirilmiş iş akışını izler ve geçmiş işleri sonradan yeterli ilan etmez.

## Eyleme'yi geliştirebilecek deneyim

Doğrulanmış görev sonuçlarını, düzeltmeleri, tipli araç sonuçlarını, kaynak/revizyon bağlarını, test kanıtını, sınırlı onarım özetlerini ve ölçülen kaynakları köken bilgisiyle kaydedin. Yeniden kullanılabilir dersler: katı wire tipleri, bağımsız sabitlenmiş ölçülen hash'ler, birleşik boyutlarda taşma denetimi, doğru desteklenmeyen-kabiliyet sınıflaması, bağımlılığa duyarlı testler ve tam incelenen/main eşleşmesi. Bunlar genelleştirilmiş doğrulanmış derslerdir; ham sohbetler, özel muhakeme, kimlik bilgileri ve özel operasyon izleri public kayıtlara aktarılmaz.

Proje verisi ve türevleri varsayılan olarak proje içinde özeldir. Execute, collect, train, external disclosure ve ecosystem export ayrı izinlerdir. Kabul edilmiş memory, RAG kaynakları, reçeteler, veri setleri, adaptörler ve skill'ler hak, köken, geri çekme ve kapsamı taşır; retrieval/import yetki vermez. Yalnız incelenmiş uygun adaylar ekosisteme katılabilir. Yerel model özelinde fine-tune/LoRA/QLoRA, bağımsız holdout, canary/promotion/rollback ve skill paketleme kendi Rust kabul kapılarımız olarak kalır. Unsloth seçenek adları incelenmiş referans/reçete hedefleridir; gizli motor veya evrensel yerel eşdeğerlik vaadi değildir.

[Güncel kartlar](../../records/platform-goal-plan.json), [aksiyon planı](platform-action-plan.md), [kaynak planlama](model-resource-planning.md) ve [kalite kapılarına](quality-gates.md) bakın.
