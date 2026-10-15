# Eyleme geliştirici rehberi

**Tek Eyleme markası — 15 Ekim 2026:** [eyleme.dev](https://eyleme.dev/tr/), Eyleme ve topluluğunun ortak merkezidir. Eyleme bağımsız kullanılabilen, public ve Apache-2.0 lisanslı bir proje olarak kalır. **Eyleme Derleme** ve **Eyleme Onama**, isteğe bağlı ürünler olarak private kaynak kodlu, ücretli abonelik modelini izler. Ticari hizmetler ve koşullar geliştirme aşamasındadır; fiyatlar ve kullanıma sunulma durumu yayımlanmamıştır. Bu depo abonelik hizmeti sunmaz.

Ürün ailesi **Derleme → Onama → Eyleme** sırasıyla anlatılır: veriyi hazırla, işi yetkilendir, ardından yürüt. Eyleme kendi temel erişim kontrollerini korur ve bağımsız kullanım için iki aboneliğe de ihtiyaç duymaz. [Public ürün ailesi açıklamasına](https://github.com/eyleme-dev/eyleme/blob/main/docs/tr/product-family.md) bakın.

Teknik tanımlayıcılar uyumluluk için mevcut yazımlarını korur. Tarihsel kanıtlar özgün ad ve bağlantılarını korur.

`eyleme-dev` için ortak katkı sözleşmeleri ve depo araçları. [English](README.md). İngilizce kanoniktir. Ürün/çalışma zamanı uygulaması sorumlu deposunda kalır.

- [Güncel Rust harness aksiyon planı ve kalan Goal kartları](docs/tr/platform-action-plan.md)
- [Proje token ve maliyet takibi](docs/tr/usage-accounting.md)
- [GitHub Goal takibi ve koruma önerisi](docs/tr/github-work-management.md)
- [macOS Goal programı ve G00 başlangıç kaydı](docs/tr/goal-program.md)
- [Katkı sözleşmesi](AGENTS.md) ve [iş akışı](CONTRIBUTING.tr.md)
- [Depo haritası](docs/tr/repository-map.md) ve [yeni depo kontrol listesi](docs/tr/repository-setup.md)
- [Kalite kapıları](docs/tr/quality-gates.md) ve [araç envanteri](docs/tr/tooling.md)
- [Taşıma, birleştirme sırası ve geri dönüş](docs/tr/repository-migration.md)
- [Tarihsel isim kararı](docs/tr/name-availability.md)

Yerel kontroller belgeleri ve katkı iskeletini doğrular. Depo kümesi kontrolü sabitlenmiş açık depo commit'lerini veri olarak okur; çeviri/API/yol haritası uyumunu, ortak araç özetlerini ve bağlantıları denetler. İndirilen çalışma dizinlerinden kod yürütmez. Uygulama, GPU, model veya eğitim davranışını kanıtlamaz. Bağımsız bakımcı incelemesi hâlâ gereklidir; birleştirme, dal kuralı veya dağıtım burada otomatikleştirilmez. Kendi kaynak kodumuz ve belgelerimiz [Apache-2.0](LICENSE) lisanslıdır. Ayrı belirtilen üçüncü taraf içerikleri, model ağırlıkları ve veri kümeleri kendi koşullarını korur.

- [Apache-2.0 lisans ve katkı kapsamı](docs/tr/licensing.md)
