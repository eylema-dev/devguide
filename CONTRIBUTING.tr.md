# Eyleme'ye katkıda bulunma

[İngilizce](CONTRIBUTING.md) kaynak dildir. Sözleşme sürümü: **0.3.0**.

Eyleme şu anda tasarım sözleşmeleri ve depo araçlarını içerir. Rust web platformu, GPU motoru ve otonom AI takımı yol haritasındadır. İnsanlar, Claude, ChatGPT/Codex, MiniMax ve diğer araçlar aynı katkı sürecini kullanır; sağlayıcı/model desteği isimden varsayılmaz, görev sırasında doğrulanır.


## Yeterliği kabul edilmiş değişiklik PR'ları

Kod, belge ve yapılandırma değişiklikleri bakımcının tarihli değerlendirmeyle kabul ettiği frontier/SOTA LLM profilinin anlamlı kullanımını ve gerçek ayrı, bakımcının yetkilendirdiği AI incelemesini gerektirir. Tartışma, fikir ve hata bildirimi açık kalır. [Model yeterlik politikasını](docs/tr/contribution-model-policy.md) izleyin; istenen ad/effort veya başarılı CI yeterlik ya da yetki değildir. Gelecek görev aktivasyonu uygun yazar/inceleyen profillerini ve gerçek insan görev kararını bağlar. İlk sınırlı profil gerçek bakımcı kararı ve tarihli kanıta dayanır; diğer alanlar yeterli ilan edilmez.

## Somut bir ihtiyaçla başlama

[AGENTS.md](AGENTS.md), [mimari](https://github.com/eyleme-dev/eylema-docs-tr/blob/main/docs/architecture.md), [proje yapısı](https://github.com/eyleme-dev/eylema-docs-tr/blob/main/docs/project-structure.md) ve [yol haritasını](https://github.com/eyleme-dev/eylema-docs-tr/blob/main/docs/roadmap.md) okuyun. Özellik, hata veya mimari issue formunu kullanın. Issue/PR açıklamalarını, kodu, yorumları, dosya adlarını ve teknik görev kayıtlarını İngilizce yazın. Dokümantasyon İngilizce ve Türkçe tutulur; sınanan davranış gerektiriyorsa örnekler İngilizce dışı test verisi içerebilir. Küçük düzeltmelerde PR'a bağlanan açık bir bakımcı talebi yeterlidir.

Başlangıç durumunu, eylemi, beklenen sonucu, hedef ortamları, izinli dosyaları ve kapsam dışını yazın. Ölçülebilir kabul koşulları ekleyin. Öncelik ve yetkiyi bakımcı belirler; issue açılması bir modele komut çalıştırma veya sır edinme yetkisi vermez. Büyük arayüz, bağımlılık, veri/denetim veya platform değişiklikleri uygulamadan önce incelenmiş mimari öneri gerektirir.

[NeedSpec şeması](https://github.com/eyleme-dev/eyleme/blob/main/ai-team-protocol/request.schema.json) makinece okunabilir girdi sözleşmesidir. GitHub formları bunun girdilerini toplar; otomatik issue–NeedSpec dönüştürücüsü veya AI hizmeti kurulmuş değildir. Mevcut örnek sentetiktir.

## Tek görev, incelenebilir değişiklik

1. Public depoyu fork edin veya yetkili dal kullanın. Güncel `main` üzerinden başlayın; uygun olduğunda `feat/<task>`, `fix/<task>` veya `docs/<task>` adı kullanın.
2. Görev/revizyon, başlangıç SHA'sı, dosya kapsamı, kabul kontrolleri ve sonlu süre/model çağrısı/düzeltme bütçeleriyle kısa plan yazın. Yetkilendirilmiş rutin adımlar yerine gerçek niyet belirsizliklerini netleştirin.
3. Sınırlı değişikliği uygulayın; üretim kodunu kendi Rust bileşenlerinde tutun. Yeni bağımlılık önerisini [araç envanterine](docs/tr/tooling.md) ve mimari öneriye ekleyin. Üretilmiş kod veya kopyalanmış paketlerle gizli bağımlılık getirmeyin.
4. Gerektiğinde davranış testleri ekleyin. İki dilde belgeleri güncelleyin, anlamlarını inceleyin ve AGENTS.md komutuyla `tools/translation-pairs.json` dosyasını yenileyin.
5. [Kalite kontrollerini](docs/tr/quality-gates.md) çalıştırın. Gerçek komutları, ortamı, sonuçları ve sınırları kaydedin. Performans değişikliğinde adlandırılmış donanımda yeniden üretilebilir önce/sonra kıyası veya gerekçeli uygulanamazlık kararı gerekir.
6. Şablonla taslak PR açın. İş tamamlanmadığında `Refs #123`, kabul koşulları karşılandığında `Closes #123` kullanın. Aynı görev revizyonunda mevcut dalı/PR'ı kullanın.
7. CI hatalarını ve inceleme bulgularını çözün. Kanıtlar güncel olduğunda bakımcı incelemesini isteyin. Yeni commit ilgili kanıtları geçersiz kılar; merge ve sürüm kararları bakımcıya aittir.

Yazar birden çok model kullanabilir; her rolü gerçekte kimin yürüttüğünü belirtmelidir. Bağımsız inceleme ayrı inceleyici/bağlam ve incelenen commit'e bağlı rapor gerektirir. Öz inceleme açıkça böyle adlandırılmalıdır. Bağımsız inceleme yoksa kapı beklemede kalır; geçmiş gösterilmez.

## Geliştirme komutları

```sh
python3 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r tools/requirements-ci.txt
.venv/bin/python -m unittest discover -s tools/tests -v
.venv/bin/python tools/check_repository.py
.venv/bin/python tools/check_pr.py --body-file .github/PULL_REQUEST_TEMPLATE.md --allow-template
git diff --check
```

Gerçek PR açıklamasını sanal ortamda `python tools/check_pr.py --body-file <path>` ile doğrulayın. CI, PR olay yükünü metni shell komutlarına yerleştirmeden okur. Bölüm yapısını ve doldurulmuş değerleri denetler; doğruluğu veya yetkiyi kanıtlamaz.

## Kanıt, dil ve inceleme

`passed`, `failed`, `skipped`, `not_run`, `not_applicable` değerlerini kullanın; son üçünü gerekçelendirin. PR'da başlangıç/güncel revizyonları ve kabul–test eşleşmesini belirtin. CI gerçek dal ucunu ve kontrol edilen birleşim revizyonunu kaydeder; PR açıklamasının kendi commit kimliğini sürekli yenilemesi gerekmez. Özel düşünce dökümleri, erişim bilgileri, üretim logları, kişisel veri veya model ağırlıklarını kanıt olarak paylaşmayın.

EN/TR parmak izleri kayda geçirilmemiş düzenlemeleri, API kimliği eşliği sözleşme kaymasını yakalar. Çeviri kalitesi yine insan veya ayrı inceleme gerektirir. Tarihsel mimari ve uygunluk kayıtları etiketlidir; güncel README veya yol haritasının yerine geçmez.

`CODEOWNERS` ilk bakımcıyı belirtir; tek başına onayı zorunlu kılmaz. Bu değişiklik CI ve inceleme politikasını sağlar; dal kuralları ayrı yönetilir ve doğrulanmadan uygulanıyor denmez. CI, politika veya şema değişiklikleri bakımcı incelemesi ister; PR kontrolleri gevşeterek kendi onayını oluşturamaz.

Bakımcı 12 Ekim 2026 tarihinde kendi Eyleme kaynak kodu ve belgeleri için [Apache-2.0](LICENSE) seçti. Projeye dahil edilmek üzere bilerek sunulan katkılar, aksi açıkça belirtilmedikçe lisansın 5. maddesine tabidir; ayrıca anlaşılmış koşullar korunur. Ayrı CLA veya DCO zorunluluğu getirilmez. Kökeni kaydedin ve üçüncü taraf bildirimlerini koruyun; model/veri izinleri varlığa özgüdür. [Lisans kapsamına](docs/tr/licensing.md) bakın. Şüpheli açıkların sömürü ayrıntılarını veya sırları public issue'ya koymayın; GitHub özel bildirim kanalı açıksa kullanın, değilse ayrıntıları yayımlamadan bakımcıdan özel kanal isteyin.

## Henüz otomatik olmayanlar

Issue sınıflandırma, yetki doğrulama, model erişimi, bağımsız inceleme, görev yönetimi, donanım kıyasları, model yükseltme ve merge kararları şablonlarla otomatikleşmez. Hiçbir iş akışı katkı içeriğini model sağlayıcısına göndermez veya model eğitmez. Planlanan protokol [takım tasarımındadır](https://github.com/eyleme-dev/eylema-docs-tr/blob/main/docs/development-and-operations.md).

## Depolar arası değişiklikler

[Depo kurulum ve çeviri akışını](docs/tr/repository-setup.md) izleyin. Politika burada; ürün belgeleri dil depolarında, şemalar çekirdektedir. İlişkili değişiklikleri sunun ve son üye commit'lerinden sonra sabitlenmiş depo kümesini yenileyin. Entegrasyon anlık görüntüsü sürekli zorlanan depolar arası birleştirme kuralı değildir.

Her yeni görev/Goal öncesi ve sonrasında, onarımlar ve ayrı incelemeler dahil özel [proje token ve maliyet defterini](docs/tr/usage-accounting.md) güncelleyin. Kesim zamanını ve tüketim artışını yerel kanıta kaydedin; yeni proje köklerini/provider metaverisini işe başlamadan kaydedin. Bilinmeyen tüketim/fiyat bilinmiyor olarak kalır; özel oturum kayıtları yayımlanmaz.
