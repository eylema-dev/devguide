# GitHub Goal takibi ve koruma önerisi

Kaynak revizyon 0.1.0. İngilizce kanoniktir. [English](../en/github-work-management.md).

G05, kabul edilen planın 47 kimliğini ana depolarında issue olarak oluşturur. Mevcut G00–G04 issue’ları ve gövdeleri korunur. [Goal takip kaydı](../../records/goal-tracking.json) gerçek issue URL’lerini, mantıksal/sayısal milestone’ları, bağımlılıkları, koşullu kapıları, EYL-001–008 plan kimliklerini, etiketleri ve kabul edilen teslimleri bağlar. [G00 kart indeksi](../../records/goal-index.json) değişmez tarihsel öneri olarak kalır; yürütüm sonuçlarıyla üzerine yazılmaz. Takip dosyası sürümlü gözlemdir, sürekli eşitleme servisi değildir. Her Goal öncesi kapsamlı teslimde metaveriyi yenile; güncel main’i, tam yolları, gerçek rolleri ve kabul edilen bağımlılık sürümlerini bağla. Etiket, issue veya yetki referansı izin vermez.

Durumlar backlog, ready, implementing, verification, review, ready_for_maintainer ve accepted olarak tanımlanır. Aynı anda en fazla bir Goal uygulanır. Ready, koşulsuz bağımlılıkların kabulünü gerektirir; koşullu kapılar açık kalır. G06 gerçek lisans/katkı kararını bekler. W01, G03 sonrası doğru içerik hazırlayabilir; çalışan ürün iddiaları yine G44 gerektirir. Varsayılan öncelik, sıralama uydurmak yerine unranked olur. Ortak etiket alanları durum, milestone, plan kimliği, tür, platform ve bekleme nedenini kapsar. Projects erişimi veya token kapsam değişikliği gerekmez.

M0–M7 mantıksal kimlikleri korunur. Milestone’lar depo yereldir: depolar arasında sayısal kimliklerin eşleştiğini varsayma, gerçek kimlikleri ve URL’leri kaydet. G05 ön kontrolünde milestone yoktu; kullanılan eksik milestone’lar oluşturuldu. Tarihsel release/website kimlikleri ayrı kalır. Açıklamalar tek macOS M4 Pro/24 GiB kabul cihazını belirtir, Linux/ikinci cihaz desteğini erteler; milestone’lar tarih vaadi olmayan kapılardır.

[Gözlenen GitHub metaverisi](../../records/github-work-management.json), tam main sürümündeki kontrol kaynaklarını, klasik korumayı ve uygulanan kuralları ayrı kaydeder. G00–G04 ve G07 kabul kayıtları ayrı incelenen yazar head’lerini aynı dosya ağacına sahip merge main’ine ve başarılı main CI’a bağlar. [Salt okunur denetleyici](../../tools/check_goal_tracking.py) yerelde yapıyı doğrular; `--fetch` ile gerçek issue/milestone/etiketleri, merge ağaçlarını, başarılı commit bağlı çalıştırmaları ve gözlenen kontrol kaynaklarını denetleyebilir. Erişilemeyen okuma veya kayıt sapmasında başarısız olur. Özel inceleme bağlamını doğrulayamaz, yetki yaratamaz; gerçek ayrı inceleme ve maintainer kararı teslim kapıları olarak kalır.

```sh
.venv/bin/python tools/check_goal_tracking.py
.venv/bin/python tools/check_goal_tracking.py --fetch
```

[Koruma istekleri](../../records/github-protection-proposal.json) on depo için hazırlandı; G05 hiçbir yönetim ayarı yazmadı. Gözlenen GitHub Actions app 15368 kaynaklı repository-checks, yalnız core/examples/evals için ayrıca rust-checks gerektirirler. Dalın güncel olmasını gerektiren kontroller, yöneticilere uygulama, PR zorunluluğu, konuşma çözümü ve force push/silme yasağı önerilir. Sıfır GitHub onayı ilk tek hesaplı akışı korur; bağımsız AI incelemesi ve gerçek maintainer merge yetkisi ayrı kalır. Erişilemeyen ikinci insan inceleyici varmış gibi gösterilmez. Website deploy işi zorunlu kontrole dönüştürülmez; website kaynağı/yayını değişmez.

Ayarları uygulamak, somut istekler incelendikten sonra ayrıca gerçek maintainer izni gerektirir. Yazmadan önce mevcut koruma/kuralları tekrar oku; daha güçlü ilgisiz kuralları koru ve sonrasında gerçek API okumasını kaydet. Hazırlanmış isteği uygulanmış gösterme. Core’da repository-checks, güncellik, yöneticiler ve konuşma çözümü gerektiren klasik koruma zaten var; diğer klasik koruma okumaları 404 döndürdü, uygulanan kurallar/ruleset’lerin boş olması ayrı gözlendi. Bu zaman damgalı gözlem değişebilir.

[G05 planı](../plans/g05-github-work-management.md) kabul edilen kapsamı, tabanları, sonlu bütçeleri, kontrolleri ve geri dönüşü kaydeder. Kapsamlı Git değişikliklerini PR ile geri al; tarihsel issue/milestone’ları silme veya başka görevin ortamını kaldırma. Ayar geri dönüşü kendi yetkisini ve kaydedilmiş önceki durumu gerektirir. Planlama metaverisi ve depo CI’ı runtime, GPU, model, eğitim veya sürüm kabulü kanıtlamaz.
