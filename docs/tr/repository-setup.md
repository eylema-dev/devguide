# Yeni depo kurulumu

[English](../en/repository-setup.md). Önce [depo haritasında](repository-map.md) ayrılma gerekçesini açıklayın. Bakımcı talebini, sorumluyu, yaşam döngüsünü, görünürlüğü ve lisans durumunu kaydedin; plan kaydı yetki vermez.

1. Organizasyondaki isimleri ve hedef dizini inceleyin; eşleşen mevcut depoyu kullanın ve yerel çalışmayı koruyun. Varsayılan dalı doğrulayın.
2. Yetkilendirilmiş depoyu kısa README ile oluşturun. Başlangıç kurulumu uygulama kanıtı değildir. Güncel main üzerinden sınırlı tek dal açın; temel SHA'yı ve sonlu görev bütçesini kaydedin.
3. README ve Türkçe karşılığını, repository.json içinde kapsam/aşamayı, devguide'a bağlanan ince katkı/sağlayıcı dosyalarını yazın. Başka depoda kalan dosya ve arayüzleri belirtin; ürün sözleşmelerini çatallamayın.
4. İncelenmiş araçları, özetlerle kilitli gereksinimleri, olumsuz testleri, sabitlenmiş salt okunur CI'ı, issue/PR şablonlarını ve CODEOWNERS'ı kopyalayın. Kopya baytlarını tools/vendor.json içine kaydedin. Bu CI araçları üçüncü taraf üretim bağımlılığı eklemez.
5. Çalıştırılabilir uygulama kabul edilmeden önce aşamaya uygun anlamlı kontroller ekleyin. AGENTS.md komutlarını aynen çalıştırın, çeviri anlamını inceleyin ve parmak izlerini yenileyin.
6. Görev dalını commit edip yayımlayın. Devguide tools/repository-set.json içine değişmez üye SHA'larını ve incelenmiş çeviri özetlerini yazın. Depo kümesi kontrolünü çalıştırıp şablonla ilişkili PR'ları açın.
7. Her farkı ilgisiz değişiklikler, özel yollar, kimlik bilgileri, operasyon verileri ve ağırlıklar açısından inceleyin. Yerel/uzak CI'ı, kesin baş revizyonlarını, öz incelemeyi ve bekleyen bağımsız incelemeyi ayrı kaydedin. Birleştirme ve dal kuralı yönetimi gerçek bakımcı yetkisi gerektirir.

## Ayrılmış belgeyi güncelleme

İngilizce ve Türkçeyi ilişkili PR'larda güncelleyin. Her dil deposu incelenen yerel baytları kaydeder. Devguide iki revizyonu ve her eşleşen ürün belgesinin özetini sabitler; entegrasyon kapısı API tanımlayıcılarını, işlem sırasını ve yol haritası kilometre taşı/görev kimliklerini karşılaştırır. Yerel kontrolün yeşil olması diğer dilin güncelliğini kanıtlamaz. Parmak izlerinden önce anlamı inceleyin.

Üye dallar yayımlandıktan sonra devguide içinde `.venv/bin/python tools/check_workspace.py --fetch` çalıştırın. İndirme yalnızca sabit açık eyleme-dev depolarını ve tam commit kimliklerini okur; üye kodu yürütülmez. Temiz yerel kopyaları kontrol etmek için kısa depo isimlerini yerel dizinlere eşleyen JSON dosyasını `--workspace-file` ile verin; makineye özel bu dosyayı Git'e eklemeyin. Her dizinin baş revizyonu sabitlenen SHA ile aynı olmalıdır.

Entegrasyon manifesti bir kabul anlık görüntüsü adayıdır; en güncel main'i izlemez. Sonraki her üye değişikliği eşlik eden manifest PR'ı gerektirir; bu kurulumda webhook, zamanlanmış izleyici veya sunucuda zorlanan depolar arası birleştirme kontrolü yoktur. Son üye revizyonlarından sonra ve bakımcı kabulünden önce entegrasyonu yeniden çalıştırın.

Sıradan belge değişiklikleri için `records/document-migration.json` veya `records/migration-snapshot.json` dosyalarını yeniden yazmayın. Bunlar ilk taşımanın kaynak/hedef baytlarını değişmez commit’lerde korur. Güncel belgeler inceleme sonrasında gelişebilir; yeni revizyonun girdileri yerel parmak izleri ve güncel entegrasyon pinleridir. Taşıma kapısı güncel yerleşim/kaldırmaları tarihsel bayt kanıtından ayrı kontrol eder. Tarihsel cache yalnız doğrulanmış public kimlik/tam commit’leri indirip Git blob’larını okur; üye kodu yürütülmez.

## GitHub kimlik geçişi — 14 Ekim 2026

Kanonik organizasyon `eyleme-dev`, çekirdek depo `eyleme-dev/eyleme` oldu. Yardımcı depoların kısa adları aynı kaldı. Güncel depo kimlikleri, CI kapsamı, üye sabitlemeleri ve örnek bağımlılık kaynakları kanonik adları kullanmalıdır.

Tarihsel taşıma/Goal kanıtları özgün depo adlarını, bağlantılarını, özetlerini ve commit'lerini korur. Salt okunur geçmiş kontrolleri yalnız yönetilen depoları `eylema-dev` organizasyonundan `eyleme-dev` organizasyonuna; çekirdeğin bilinen iki önceki kimliğini (`eylema-dev/eylema`, `eyleme-dev/eylema`) ise `eyleme-dev/eyleme` kimliğine eşler. Git fetch ve GitHub API okumaları kanonik hedefi kullanır; değişmez kaynak baytları, kesin revizyonlar ve depo sahipliği kontrolleri geçerliliğini korur. Bu eşleme yetki vermez ve benzer görünümlü sahip veya depo adlarını kabul etmez.
