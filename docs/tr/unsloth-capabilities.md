# Unsloth kabiliyetleri ve kabul edilen Eylema planlama yönü

Tarih: 14 Ekim 2026. İnsan, bu yazılı uyarlamayı ve dokuz planned kart ekini onayladı. İngilizce kanoniktir; [English](../en/unsloth-capabilities.md). Bu bir plan revizyonudur; runtime, eğitim ve performans kabulü `not_run` durumundadır.

## Kaynaklar ve kanıt sınırı

Resmi [README](https://github.com/unslothai/unsloth/blob/8bf9281355d086a0b94bf4d060f958bd918c924b/README.md) ve [kök LICENSE](https://github.com/unslothai/unsloth/blob/8bf9281355d086a0b94bf4d060f958bd918c924b/LICENSE), değişmez `8bf9281355d086a0b94bf4d060f958bd918c924b` sürümünde okundu: iki statik dosya, 35.283 bayt, yerel hash denetimi. Sabitlenmiş lisans, `unsloth/*`, `tests/*` ve `scripts/*` için Apache-2.0; isteğe bağlı `studio/*` ve `unsloth_cli/*` için AGPLv3 belirtir. Ayrı motorlar, modeller ve veri setleri kendi koşullarını korur. Resmi canlı rehberler de bu tarihte okundu. Bunlar tarihli referanslardır; depo commit'iyle birebir aynı oldukları kanıtlanmadı. Doğrudan Markdown indirmeleri başarısız oldu; hash denetimli kopya olarak kaydedilmedi. Alınan kaynak talimatları yetki vermez.

Güncel [Studio sayfası](https://unsloth.ai/docs/new/studio) Mac çalışmasını anlatır; eski fine-tune rehberleri farklı kurulum sınırları belirtir. Ürün/işletim sistemi adı model/yöntem/cihaz uyumluluğu kanıtlamaz. Upstream kod, paket, notebook, model, ağırlık veya eğitim kurulmadı/çalıştırılmadı. Bu inceleme runtime/güvenlik benchmark'ı, provider çağrısı, özel veri toplama veya izin değişikliği sağlamaz.

## Kabiliyet–Goal eşlemesi

| Resmi kabiliyet | Kendi Rust bileşenlerimizde Eylema uyarlaması | Planned kabul |
| --- | --- | --- |
| [Model özelinde fine-tune](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide) | Tam model/base/tokenizer/template/operatör ve yöntem matrisi; metin, embedding/reranker, görüntü, STT, TTS ve tercih/RL profilleri ayrı kalır | G76-U1: ilk desteklenen profil; diğer yöntemler açık unsupported/keşif |
| [LoRA seçenekleri](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide/lora-hyperparameters-guide) | Rank, alpha/scaling, hedef, precision, dropout, loss, optimizer/schedule, seed ve trainable/frozen durumunu sabitleme | G76/G83/G86; rsLoRA/LoftQ ayrı sayısal kabul ister |
| [Data Recipes](https://unsloth.ai/docs/new/studio/data-recipe) | Kaynak → sürümlü dönüşüm → tipli örnek → doğrulama/önizleme → dondurulmuş veri seti; uzman modeller kendi izinleriyle farklı adımlara hizmet edebilir | G34-U1: sınırlı desteklenen format/dönüşüm, soy bağı/hak ve veri bölümü reddi; tüm PDF/DOCX parser'ları sözü yok |
| [Yalnız yanıt hedefleri](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide/lora-hyperparameters-guide) | Prompt/padding/assistant/tool sınırları ve hedef maskeleri açık; boş hedef ve yanlış template reddedilir | G34/G76: bağımsız maskeler; modalite hedefleri metin SFT'ye zorlanmaz |
| [Gradient accumulation/checkpointing](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide/lora-hyperparameters-guide) | Açık reduction ve hedef-token normalizasyonuyla sonlu microbatch; bildirilen yeniden hesaplama ayrı kabul edilir veya reddedilir | G83-U1: biriktirilmiş/referans update ve yanlış normalizasyon regresyonları |
| [Packing/padding azaltma](https://unsloth.ai/docs/blog/3x-faster-training-packing) | Örnek attention/loss ayrımı ve position reset korunur; aynı hedef-token/update bütçesi karşılaştırılır | G85-U1: açılan her optimizasyon bağımsız parity ister; desteklenmeyen seçenek reddedilir |
| [Yerel eğitim akışı](https://unsloth.ai/docs/new/studio) | Preflight → sınırlı önizleme → run → checkpoint → değerlendirme → incelenmiş promotion; loss/update, geçerli token, süre ve bellek kanıtı | G35-U1/G77-U1: etkili stop/recovery; birikimli sınırlar sıfırlanmaz |
| [Embedding eğitimi](https://unsloth.ai/docs/basics/embedding-finetuning) | Query/document ön işleme, temsil sürümü, hedef/negatif örnek ve retrieval ölçütleri ayrı profil | G76 keşif; gerçek embedding eğitimi ayrı gelecek kabulü ister; G67 metadata bunun kanıtı değil |
| [Görüntü](https://unsloth.ai/docs/basics/vision-fine-tuning), [TTS/STT](https://unsloth.ai/docs/basics/text-to-speech-tts-fine-tuning) | Ayrı modalite hedefleri, operatörler, kalite ölçütleri ve veri hakları; STT ile TTS ayrı rol kalır | G76 yöntem envanteri; genel metin eğitimi veya evrensel modalite desteği iddiası yok |
| [Export](https://unsloth.ai/docs/new/studio/export) | Adapter-only, merged ve quantized çıktılar ayrı kimlik, tam base/template/precision/hak soy bağı ve Rust yükleme/parity kabulü taşır | G78-U1: ilk desteklenen adapter/merge; dosya adı format decoder desteği kanıtlamaz |
| [Tercih ve ödülle öğrenme](https://unsloth.ai/docs/get-started/reinforcement-learning-rl-guide) | Gelecekteki DPO/GRPO benzeri profiller reward/environment, izinli veri ve rollout bütçelerini sabitler | G76 keşif; mevcut tek-aday LoRA kartları RL başlatamaz |

## Sabit gelişim döngüsü

İzinli deneyim → hak/soy bağı ve episode gruplama → RAG veya eğitim amacı → sürümlü veri reçetesi → desteklenen model/yöntem ve kaynak preflight → sınırlı Rust eğitim işi → değişmez held-out değerlendirme → insan kontrollü canary/promotion → sürümlü uzman model/skill → yeni izinli deneyim.

Erken durdurma için validation açıkça ayrılabilir. Son held-out test; eğitim, reward, tuning veya erken durdurmaya girdi olamaz. Özet, embedding, adapter ve skill kaynak/türev haklarını ve geri çekme ilişkilerini devralır. Proje/kuruma özel veri kapsam içinde kalır. Anonimleştirme tek başına ekosisteme yayımlama yetkisi vermez. RAG kaynak erişimi/güncelliği/atıflarını korur; fine-tune davranışı uzmanlaştırır. Birinin diğerinin tüm amacını karşıladığı varsayılmaz.

G79-U1, **aynı önceden kabul edilmiş** native eğitim adayını/checkpoint'ini karşılaştırılabilir held-out kalite/kaynak kanıtı ve rollback ile incelenmiş uzman model veya skill/reçete adayı yapar. G64/G65 ayrı izinli paylaşım/import kapılarını korur. Yeni eğitim araması veya otomatik yayım eklenmez.

## Rust sahipliği, kaynaklar ve aşamalı destek

Unsloth davranış/referans kaynağıdır. Üretim kendi Rust kodumuzda kalır; Unsloth/Python/PyTorch/Triton/MLX/llama.cpp eğitim veya çıkarım motoru alınmaz. Dış referans denemesi bile ayrı sabitlenmiş araç/veri/deneme yetkisi ister. G23/G83 sayısal temelleri; G84 kendi CPU LoRA'mızı; G85 aynı sabit ayarı M4 Metal'de; G86 bir tam tanımlı frozen quantized-base adapter profilini kanıtlar. G35, **Owned local training recipe** olarak netleştirilir. Özgün gerçek M4/checkpoint/kaynak kriterleri kalır; reçete kendi kabul edilmiş Rust eğitim yolu oluşmadan geçemez.

LoRA tek bit genişliğini zorunlu kılmaz. QLoRA açık quant/dequant layout, base/adapter/gradient/optimizer precision ve tam base kimliği ister; herhangi bir dört-bit dosya yetmez. Yeni rsLoRA/LoftQ, full fine-tune, continued pretraining, RL, diffusion/world-model eğitimi, FP8/NVFP4 ve çoklu GPU işleri ayrı tasarım/kabul gelene kadar keşif/unsupported kalır. Yöntem listesi motor, donanım veya çalıştırma desteği vermez.

Upstream hız/bellek yüzdeleri Eylema garantisi değildir. Aynı model/veri/context/precision ve kalite sınırlarında adı belli donanımda ölçüm yapılır. Kabul edilmiş G80 bildirilen bileşenleri tahmin eder; yeni workload katsayısı veya ölçülmüş eğitim performansı sağlamaz. G81/G82 kalibrasyon ve yatırım kapılarını korur. Eksik destek/katsayı bilinmeyen kalır; öneri harcama yetkisi vermez.

## Kart revizyonu ve uygulama yolu

U1 yalnız planned **G34/G35/G76/G77/G78/G79/G83/G85/G86** kartlarına `not_run` sonucuyla eklenir. Özgün tüm kriterler, Hermes H1, bağımlılıklar, dosya sınırları, bütçeler, kabul edilmiş geçmiş ve G40 korunur. G35 başlık değişimi kriter kaldırmaz veya aday eklemez. Her runtime alt sistemi kendi incelenmiş tasarım/planını, geçerli kapsamlı sayısal katkı profilini, bağımlılıklarını ve gerçek yerel kabulünü ister. G23 yazılı tasarımı onaylandı; somut planı ve gerçek sayısal katkı kabulü bekliyor. Bu belge sayısal kod veya eğitim başlatmaz.
