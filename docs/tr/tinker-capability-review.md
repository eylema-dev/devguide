# Tinker optimizer kabiliyetleri ve kabul edilen Eyleme plan yönü

15 Ekim 2026. İnsan bakımcı bu yazılı uyarlamayı ve altı planlı kart ekini onayladı. İngilizce kanonik; [İngilizce kaynak](../en/tinker-capability-review.md). Bu revizyon gelecekteki kabul koşullarını kaydeder; optimizer, model ve eğitim desteği `not_run` kalır.

## Kaynaklar ve sınırlar

Resmî [optimizer rehberi](https://tinker-docs.thinkingmachines.ai/tinker/optimizers/), AdamW ve Dimuon’u, eğitim istemcisi boyunca sabit optimizer ailesini ve uyumlu adım parametrelerini açıklar. Öğrenme oranı/rank/batch önerileri deneysel, sonuçlar iş yüküne bağlıdır; tek tohumlu deneyler vardır. Bunlar değerlendirme adaylarıdır; Eyleme ölçümü veya evrensel varsayılan değildir.

[LoRA rehberi](https://tinker-docs.thinkingmachines.ai/tinker/lora-primer/), hedef kapsamını ve rank/kapasiteyi ele alır. [Checkpoint rehberi](https://tinker-docs.thinkingmachines.ai/tinker/howto/checkpoints/), optimizer momentlerini içeren eğitim durumunu sampler ağırlıklarından ayırır. [Genel bakış](https://tinker-docs.thinkingmachines.ai/), bulut eğitim API’sini tanımlar.

Değişmez [SDK optimizer şeması](https://github.com/thinking-machines-lab/tinker/blob/b0ce8338acca5ab51779a4c417f1ecad346131f4/src/tinker/types/optimizer.py), sürümlü Dimuon ailesini ve adım parametrelerini belirtir; sunucunun sayısal güncelleme algoritmasını tanımlamaz. SDK `b0ce8338acca5ab51779a4c417f1ecad346131f4` ve cookbook `70767c738ba5f523b66210a70e50b0dc14c9fc1a`, canlı belgelerden ayrı gözlendi. Canlı sayfalar tarihli gözlemlerdir; bu commit’lerle aynı oldukları veya yerel HTML hash’i doğrulandığı iddia edilmez. Yayın tarihi veya bağımsız üstünlük kanıtlanmadı. Depo lisans metaverisi; model, veri seti veya algoritma haklarını belirlemez.

SDK, optimizer motoru, ağırlık, hesap veya dış eğitim servisi kurulmadı ya da kullanılmadı. Üretime dış kaynak kodu kopyalanmaz. Runtime birinci taraf Rust kalır; isteğe bağlı dış eğitim için ayrı tasarım, veri açıklama izni, hesaplama bütçesi ve gerçek yetki gerekir.

## Kabiliyet–Goal eşlemesi

| Kendi platformumuzdaki ek | Planlanan kabul | Gerekli kanıt |
| --- | --- | --- |
| Sürümlü optimizer kabiliyeti ve adım parametre şemaları | G76-T1 | Tam model/hedef/durum şekli/dtype; bilinmeyen aile/sürüm veya uyumsuz parametre reddi |
| Tipli gradient–güncelleme geçişi | G83-T1 | Güncellemeden önce tamamlanmış gradient nesli, reduction/token sayısı ve adım indeksi; bağımsız iki adımlı sayısal referanslar |
| Tam durumla CPU LoRA devamı | G84-T1 | Kesilip sürdürülmüş ve kesintisiz güncelleme, moment ve cursor karşılaştırması; beyan edilmiş taze durumlu warm start ayrımı |
| Tekrarlanabilir eğitim reçetesi | G35-T1 | Her varsayılanı, schedule/adım/token sayısını ve checkpoint amacını sabitlemek; kaynaklı hipotezler aday aramasını genişletmez |
| Amaca göre artifact teslimi | G36-T1 | Devam checkpoint’i, çıkarım adapteri ve birleştirilmiş model farklı kimlikler taşır; gerçek biçim/base/scaling/hak kontrolü ve kendi runtime’ımızda yeniden kabul |
| Ölçülen optimizer durum kapasitesi | G81-T1 | Kapsamlı donanımda adapter/gradient/optimizer/activation/checkpoint tepe belleği; eksik katsayı bilinmiyor kalır |

Kesin gereksinimler ve kontroller [güncel kartlardadır](../../records/platform-goal-plan.json). Hermes H1 ve Unsloth U1 korunur. G85 Metal eşitliği ve G86 QLoRA precision/durum koşulları özgün kapsamını korur; onlara yinelenen kriter veya yeni aday eklenmez. Kabul edilmiş G80 tahminleri ve G29 tokenizer kanıtları değişmez.

## Sabit eğitim döngüsü ve model değişimi

Kabul edilmiş model/yöntem/optimizer/donanım profili → tamamlanmış gradient → doğrulanmış tipli adım → gözlenen kendi güncellememiz → saklanan checkpoint → held-out değerlendirme → insan denetimli promotion veya rollback.

Oturum algoritma/sürüm ve durum şemasını sabitler. Yalnız açıkça tanımlanmış adım alanları değişebilir. Öğrenme oranı, schedule ve adım, hedef-token/microbatch reduction ve tüm etkili varsayılanlar kaydedilir. Bilinmeyen destek, eski gradient nesli ve geçersiz/sonlu olmayan parametreler kendi durumumuz değiştirilmeden reddedilir. Katalog adı veya kaynak örneği optimizer’ı etkinleştirmez.

Dimuon; tam, hukuken uygun sayısal tanım, bağımsız referans ve kendi Rust/native kabulü bulunana kadar yalnız keşif kalır. İlk kabul edilen optimizer kendi incelenmiş sayısal profiliyle seçilir; bu belge AdamW uygulamaz ve Tinker varsayılanlarını Eyleme varsayılanı saymaz. Yeni full fine-tune, RL, yöntem veya backend için kendi kapıları gerekir.

## Devam, warm start ve artifact amaçları

Tekrarlanabilir eğitim checkpoint’i, kabul edilen optimizer’ın gerekli durumunu, adım/schedule’ı, beyan edilmiş RNG/veri cursor’unu ve tam base/adapter/profil kimliklerini taşır. Amaç, durum şeması/dtype, model/hedef/quantization/scaling ve devralınan haklar doğrulanır. Devam edilen ve kesintisiz kendi CPU adımlarımız sabit toleranslarla karşılaştırılır; tüm platformlarda bit düzeyi eşitlik vaat edilmez.

Çıkarım adapteri veya birleştirilmiş model, optimizer durumuyla devam kabulünü karşılayamaz. Optimizer değişimi; soy bağı ve değerlendirmesi olan açık bir yeni taze durum koşusudur, sessiz devam değildir. Dönüştürme/remapping özgün dış referans ve kendi runtime’ımızda yeniden kabul kapılarını geçer. Bunlar Eyleme gereksinimleridir; Tinker’ın çökme veya atomiklik garantileri değildir.

## Gizlilik, kaynaklar ve reçete yeniden kullanımı

Çalıştırma, toplama, eğitim ve ekosistem dışa aktarımı ayrı izinlerdir. Checkpoint, optimizer durumu, adapter ve reçeteler proje-özel kapsamı ve türev/geri çekme kurallarını devralır. Anonimleştirme tek başına yayın izni vermez. Yeniden kullanılabilir kayıtlar izinli gözlenen sonuçları ve incelenmiş kaynak zincirini içerir; özel muhakeme veya otomatik özel veri paylaşımı içermez.

Kapasite analizi; adapter rank/hedefleri, batch ve context yanında tam optimizer durum düzenini/precision’ını ve checkpoint/çalışma belleği ek yükünü sayar. Paylaşılan fiziksel havuz bir kez sayılır; bilinmeyen durum veya katsayı kesin sığar sonucu üretemez. Kaynak hız/bellek garantisi, yeni donanım veya harcama kabul edilmez. Rank/batch/öğrenme oranı hipotezleri özgün sonlu aday ve kaynak sınırında held-out doğrulama ister; bu revizyon tarama koşuları yetkisi vermez.

## Teslim ve sonraki uygulama

Yalnız planned G35/G36/G76/G81/G83/G84 kartlarına T1 eklenir ve kendi issue/kart revizyonları ilerletilir. Her özgün kriter, bağımlılık, bütçe, aday sınırı, kabul edilmiş/geçmiş kanıt ve engellenmiş G40 korunur. Altı kart `planned`, sonuçları `not_run` kalır. Karşılaştırma, iki dilli aksiyon planı ve kapsamlı kayıtlar; yerel kapılar, gerçek ayrı son-commit incelemesi, güncel CI, yetkili merge ve tam main doğrulaması ister. Sonraki her runtime alt sistemi ayrıca incelenmiş tasarım/plan, uygun sayısal katkı profili ve gerçek kabul gerektirir.
