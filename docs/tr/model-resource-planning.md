# Modelden bağımsız yerel sistem planlama

[İngilizce](../en/model-resource-planning.md) kaynak dildir. Bu belge G80/G81/G82 ve bağlı model/döngü kartlarının kabul tasarımıdır; yönlendirme aracı ve model yürütmesi belgeyle uygulanmış olmaz.

Eylema yeni bir yerel sistemi görev/kalite/gizlilik şartları ve gerçek yerel kaynak envanterinden hareketle yönlendirmelidir. Sabit rol ve kabiliyet arayüzleri model ailesi ve sürümünün değişmesine izin verir. Güncel aday kataloğu, mimari özelinde taşma denetimli tahmin ve adlandırılmış cihaz ölçümü işbirliği yapan model gruplarını seçer; yalnız en yeni veya en büyük olmak seçim ölçütü değildir.

## Gerekli planlama girdileri

| Girdi | Gerekli ayrım |
|---|---|
| Donanım ve eşzamanlı yük | Fiziksel RAM/VRAM veya birleşik havuz, kullanılabilir bütçe, OS/allocator payı, cihaz/backend ve ölçülen örtüşme; rezervasyon fiziksel tahsis değildir |
| Model kimliği ve mimari | Kaynak/artifact/lisans/tokenizer/operator, parametre sayısı, toplam resident ve aktif MoE parametreleri, embeddings/heads ve incelenmiş yerleşim; bilinmeyen tür desteklenmeyen kalır |
| Hassasiyet ve depolama | Gerçek artifact byte'ları, yerel dönüşüm/quantization formatı, scale/metaveri, cache hassasiyeti ve adaptör durumu; yalnız ağırlık boyutu sığmayı belirlemez |
| Context ve modalite | Görev/system/geçmiş/tool/RAG token'ları, generation üst sınırı, batch ve KV/recurrent durum; kabul edilmiş profil başına ayrı görüntü/video, STT/TTS ve streaming buffer'ları |
| Döngü işbirliği | Aynı anda resident modeller, planlanmış örtüşme, rollerin paylaştığı model, saklanan/genişletilen aktivasyonlar, router/retrieval/memory maliyeti ve stop/recovery sınırları |
| Öğrenme ve RAG | Desteklenen eğitilebilir hedefler, gradient/optimizer/activation/checkpoint durumları, LoRA/QLoRA base ve adaptörler, index/embedding/storage/retention maliyeti; desteklenmeyen katsayı bilinmeyen kalır |
| Kabul tabanı | Görev sonucu, kalite, latency/throughput, ölçülen kaynak, izin, rollback ve tüm döngüde rol-ablation kanıtı |

Parametre sayısı ve context uzunluğu ilk boyut önerisini belirler; mimari/yerleşim/cache/workspace/örtüşme tahmini ayrıntılandırır. Taşma denetimli aritmetik, açık birimler ve sınırlı aralıklar kullanın; taşma, eski/uyumsuz kaynak ve eksik zorunlu katsayıyı reddedin. Birleşik RAM ve GPU belleğini iki bağımsız havuz, aktif MoE parametresini toplam resident ağırlık sayısı saymayın. Profil özelinde incelenmiş formüller ve bağımsız boyut fixture'ları gereklidir; formül performans veya destek kanıtlamaz.

## Planlama ve güncelleme döngüsü

1. İzinli güncel görev, gizlilik/kalite tabanı ve adlandırılmış yerel envanteri okuyun; bilinmeyen kullanılabilirlik açık kalsın.
2. Model türleri ve güncel adayları tarihli resmi kaynaklardan keşfedin. Denetleme tarihini ve değişmez artifact/profil/değerlendirme bağlarını kaydedin. Güncellik incelemesi indirme, aktivasyon veya provider çağrısı izni değildir.
3. Hak, proje izinleri ve kabul edilmiş kendi Rust mimari/operator/tokenizer/backend desteğine göre eleyin. Yeni tür kendi yerel sayısal/kalite/cihaz kapılarını gerektirir.
4. İsteniyorsa RAG/memory/eğitim dahil parametre/hassasiyet/context/batch bileşimlerini ve işbirliği yapan grupları tahmin edin. Kalite tabanını düşürmeden zamanlama, context sınırı, quantization veya daha küçük/alan uzmanı seçenekleri karşılaştırın.
5. Desteklenen profilleri gerçek cold/warm/birleşik adlandırılmış cihaz ölçümü ve tahmin hatasıyla kalibre edin; ölçülmemiş eğitim veya cihaz bilinmeyen kalsın. Fiziksel gözlemi rezervasyon sayaçlarından ayırın.
6. Belirsizlik ve karşılaştırılabilir kaynaklarda tüm döngü yararı/ablation ile izlenebilir uygun/desteklenmeyen/bilinmeyen seçenekler sunun. Ek donanım/dış servis seçenekleri tarihli fiyat/para birimi/koşul ve gizlilik uygunluğu ister; yatırım öneridir, otomatik harcama değildir.
7. Gerçek insan kabulünden sonra işin model/context/parametre/backend/zamanlama/hak revizyonlarını sabitleyin. Katalog güncellemesi sürmekteki atamayı değiştirmez veya bütçeyi sıfırlamaz.
8. İzinli gözlenen sonuç ve düzeltmeleri proje kapsamlı memory, değerlendirme ve iyileştirmeye aktarın. Yalnız incelenmiş uygun ekosistem türevleri dışa çıkar; model değiştirme/yeniden eğitim holdout/canary/rollback kapılarını gerektirir.

G80 taşma denetimli boyutlandırma, G81 fiziksel kalibrasyon ve G82 önerileri yönetir. G65 incelenmiş model/profil güncellik/import metaverisini, G66 işbirlikli bileşimi, G74 kaynağa duyarlı yönlendirmeyi, G37 sabitlenmiş değiştirme/rollback'i kapsar. Yerel destek, proje gizliliği, SOTA katkı yönetişimi veya asıl yayın/provider kapıları aşılmaz. [Aksiyon planı](platform-action-plan.md), [güncel kartlar](../../records/platform-goal-plan.json) ve [katkı model politikasına](contribution-model-policy.md) bakın.
