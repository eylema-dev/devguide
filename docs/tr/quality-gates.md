# Depo kalite kontrolleri

Sürüm **0.3.0**. [İngilizce](../en/quality-gates.md).

## Bugün çalışan kapı

[CI](../../.github/workflows/ci.yml) içindeki `repository-checks` işi PR'larda ve `main` push'larında çalışır. GitHub'ın sağladığı runner, salt okunur token, commit'e sabit eylemler ve kalıcı tutulmayan checkout kimliği kullanır. Sırlar, model API'si veya self-hosted donanım kullanmaz. PR açıklaması olay dosyasından veri olarak okunur. İş akışı ayrıcalıklı PR tetikleyicisi veya yayın işlemi içermez.

| Kontrol | Hangi durumda başarısız olur | Neyi kanıtlamaz |
|---|---|---|
| Depo dosyaları | Sembolik bağlantı, geçersiz JSON/YAML, kırık/depo dışına çıkan yerel Markdown hedefi, özel bilgisayar yolu | Dış bağlantıların sürekli erişimi; kapsamlı sır taraması |
| Şema örnekleri | Geçersiz Draft 2020-12 şema, uzak referans, geçersiz istek örneği, şema regresyonu | Kimlik, onay, referans verilen nesnenin varlığı veya doğru model yürütmesi |
| EN/TR sözleşmeleri | Eksik/eski çeviri özeti, API işlem/kod kimliği farkı, yol haritası kimliği farkı | Anlamsal çeviri doğruluğu |
| GitHub yapılandırması | Eksik girdi alanı, bozuk form, eksik PR bölümü, sabitlenmemiş/beklenmeyen action, ayrıcalıklı iş akışı ayarı | GitHub'ın şablonu sunucuda doğru çizmesi veya dal kuralını uygulaması |
| Gerçek PR açıklaması | Eksik, yinelenmiş veya yalnız yer tutucu içeren zorunlu bölüm | Kanıtın doğruluğu, inceleyici bağımsızlığı veya yetki |
| Kaynak aşaması koruması | Belge profilindeki Rust/Cargo kaynakları, eksik uygulama workspace/toolchain, onaysız rol/profil | Statik profil doğrulaması tek başına Rust çalıştırmaz |
| Boşluk ve doğrulayıcı testleri | Git boşluk hatası, başarısız regresyon testi | Uygulama davranışı |

PR açıklama kontrolü PR olayına bağlıdır; push olayında doğrulanacak PR gövdesi yoktur. CI gerçek PR head SHA'sını ve checkout revizyonunu yazar; PR çalışması GitHub'ın sentetik birleşim commit'ini kontrol edebilir. Eski commit'teki yeşil sonuç güncel kanıt değildir. PR açıklaması düzenlenince kontrol yeniden tetiklenir.

## Bakımcı kapıları

Gereksinimler, üretim bağımlılık politikası, bağımsız inceleme, lisans, API/denetim anlamı ve sürüm yetkisi bakımcı kararlarıdır. `CODEOWNERS` inceleme yönlendirmesidir. Bu iş akışı zorunlu kontrol kuralını veya dal korumasını etkinleştirmez. Bakımcı çalışmayı gözlemleyip inceleme gereksinimini belirledikten sonra `repository-checks` işini zorunlu yapabilir. Fork kontrolünü geçirmek için geniş yetki vermeyin.

Doğrulayıcı/politika değişiklikleri kabul edilmiş başlangıç politikasıyla karşılaştırılmalıdır; değiştirilmiş doğrulayıcıyı çalıştıran PR kendi gevşetmesini onaylayamaz. Ayrı inceleme kesin revizyonu belirtmelidir. Böyle bir inceleme yoksa beklemede raporlanır.

## İncelenmiş kaynak profilleri

Her depo repository.json içinde rolünü, stage ve gate_profile değerlerini bildirir. Bildirilen kimlik CI içindeki güvenilir GITHUB_REPOSITORY ve kanonik yerel Git origin ile eşleşmelidir. Belgelenmiş fork akışlarında origin aynı adlı GitHub fork, upstream ise kanonik depo olabilir. Fork yerel kontrolleri çalışır; zorunlu PR CI kanonik base depoda çalışır. Desteklenmeyen fork-push kimliği uygulama kontrollerini atlamak yerine başarısız olur. Yerel origin tutarlılık kanıtıdır; sahiplik veya yetki kanıtı değildir. JSON rolünü değiştirmek gerçek depoya bağlı workflow sınırını atlatamaz. Hedef runner ve derleyici takma adları dahil Cargo/Rust ortam geçersiz kılmaları kurulum/derlemeden önce reddedilir. Yalnız CARGO_HOME, CARGO_TERM_COLOR, RUSTUP_HOME ve RUST_BACKTRACE kabul edilir; bu konumlardaki Cargo yapılandırma dosyaları yine reddedilir. Mevcut bütün depolar documentation / documentation-v1 aşamasında ve runtime_implemented false değerinde kalır. Bu profilde Rust kaynakları, Cargo manifest/lockfile ve toolchain dosyaları yasaktır. Çekirdek, örnekler ve değerlendirmeler ancak gerçek kaynak, kök workspace/lockfile ve tam rust-toolchain.toml içeren ayrı incelenmiş değişiklikte implementation / rust-v1 profiline geçebilir. Bu geçiş bayrağı depodaki uygulamayı belirtir; ürünün tamamının kabulü değildir. Rehber, topluluk, dil belgeleri, model metadata ve eğitim tarifleri bu Rust profilini kullanamaz.

Ortak rust-checks işi yalnızca çekirdek/örnekler/değerlendirmelerde, 20 dakika sınırıyla hosted ARM64 macos-26 üzerinde çalışır. tools/check_rust.py --provision çağrısı belge aşamasını Rust kurmadan açıkça atlar; uygulama aşamasında Rust 1.99.0, rustfmt, clippy ve wasm32-unknown-unknown kurar. Ardından offline/locked Cargo metadata, fmt, uyarıları hata sayan clippy, native test/build ve repository.json içindeki açıkça incelenmiş wasm_packages kitaplık listesi için Wasm build çalıştırılır. Çekirdek en az bir taşınabilir kitaplık belirtir; yalnız native örnek/değerlendirme depoları boş liste bildirebilir ve Wasm için not_applicable raporlar. Native sunucu/dosya sistemi paketleri Wasm olarak derlenmez. Seçilen adlar workspace içi kitaplıklara karşılık gelmelidir. Bütün feature değerleri kapsanır. Başarısız komut kapıyı başarısız yapar. Desteklenmeyen host, derleyici veya Cargo yapılandırması geçersiz kılmaları, build script ve workspace dışı paketler reddedilir. İlk profil geliştirme Cargo paketlerini de yasaklar; bunları eklemek incelenmiş envanter/profil değişikliği gerektirir. Üçüncü taraf Rust kurulum action'ı eklenmez. Hosted macOS yerel M4 donanım kabulü değildir; Wasm derlemesi tarayıcı çalışmasını kanıtlamaz.

Şema sahipliği role bağlıdır: çekirdek mevcut iki zorunlu şemayı korur ve ai-team-protocol altında yerel çözümlenen, doğrulanan şemalar ekleyebilir. Diğer roller makine şeması sahibi olamaz; metadata/tarifler kendi depolarına aittir. Profil çalıştırılabilir geliştirme aracıdır; runtime uygulaması değildir. G04/G07 gerçek toolchain/runtime kanıtını sağlar. Mevcut doğrulayıcı fixture'ları derleme, GPU, model, eğitim veya performans kanıtı değildir. Sonraki kilometre taşları kontrollü donanım kabulünü ekler; public PR'lara özel veri veya deploy kimlik bilgileri verilmez.

## Kontrolleri güncelleme

Düzeltilen hatanın reddedildiğini gösteren regresyon testleri ekleyin. Standart [katkı komutlarını](../../CONTRIBUTING.tr.md) çalıştırın. Çeviri özetlerini iki dili inceledikten sonra yenileyin. Depodaki [eski doğrulama kaydı](../../records/historical-validation.json) tarihsel kalır; güncel commit'in kanıtı güncel CI loglarıdır.

Kaynaklar: [GitHub workflow sözdizimi](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax), [güvenli kullanım](https://docs.github.com/en/actions/reference/security/secure-use), [issue form sözdizimi](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms).

## Depo bölünmesi kontrolleri

Her çalışma dizini kendi dosyalarını, kesin depo rolünü, sürdürülen belge kapsamını ve incelenmiş parmak izlerini doğrular. Mevcut iki zorunlu sözleşme dahil makine şemalarını yalnızca çekirdek yönetir ve doğrular. Tek dilli yerel kontroller iki ürün dilini karşılaştıramaz. Devguide ayrıca değişmez depo revizyonlarında `tools/check_workspace.py --fetch` çalıştırır: altı ürün belgesi çifti ve incelenmiş özetleri, API tanımlayıcıları/işlemleri, yol haritası kimlikleri, depolar arası bağlantılar, taşıma hedefleri/kaldırmaları ve ortak araç kopyaları denetlenir. Eksik eşler, eski revizyon/özetler ve kırık hedefler reddedilir; indirilen üye betiği yürütülmez. Kaynak koruması belge aşamasındaki tüm depolara uygulanır; çalışma zamanı kaynağı eklenmeden gerçek uygulama kapılarıyla değiştirilmelidir.

Tarihsel taşıma ve güncel doğrulama ayrı girdiler kullanır. [migration-snapshot.json](../../records/migration-snapshot.json), kabul edilmiş envanteri ve ilk hedef commit’lerini sabitler; doğrulayıcı Git blob’larından kaynak, hedef, önceki-main ve değiştirilen-main hash’lerini doğrular ve envanterin değiştirilmesini reddeder. Bugün sürdürülen belgeleri tarihsel hedef hash’leriyle karşılaştırmaz. Güncel çeviri parmak izleri, API/yol haritası uyumu, hedef varlığı, çekirdek kopyalarının kaldırılması, gezinme ve ortak araç hash’leri uygulanmaya devam eder. Güncel değişiklik, incelenmiş güncel parmak izleri ve ilgili üye pinlerini gerektirir; bunları güncellemek tarihsel kanıtı değiştirmez. Olumsuz testler bozuk geçmişi, eksik/depo dışına çıkan hedefleri, kopuk bağlantıları, eski güncel parmak izlerini ve geri getirilen asılları kapsar.

Sabitlenmiş depo kümesi ilişkili PR’larla elle güncellenir; sonraki varsayılan dal değişikliklerini otomatik izlemez. Güncel üye checkout’ları `--workspace-file` ile verildiğinde de tarihsel public commit’ler ayrı cache’e indirilir; indirilen kod yürütülmez. Bağımsız inceleme ve bakımcı kararı gerçekten kaydedilene kadar beklemededir.
