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

Üye dallar yayımlandıktan sonra devguide içinde `.venv/bin/python tools/check_workspace.py --fetch` çalıştırın. İndirme yalnızca sabit açık eylema-dev depolarını ve tam commit kimliklerini okur; üye kodu yürütülmez. Temiz yerel kopyaları kontrol etmek için kısa depo isimlerini yerel dizinlere eşleyen JSON dosyasını `--workspace-file` ile verin; makineye özel bu dosyayı Git'e eklemeyin. Her dizinin baş revizyonu sabitlenen SHA ile aynı olmalıdır.

Entegrasyon manifesti bir kabul anlık görüntüsü adayıdır; en güncel main'i izlemez. Sonraki her üye değişikliği eşlik eden manifest PR'ı gerektirir; bu kurulumda webhook, zamanlanmış izleyici veya sunucuda zorlanan depolar arası birleştirme kontrolü yoktur. Son üye revizyonlarından sonra ve bakımcı kabulünden önce entegrasyonu yeniden çalıştırın.
