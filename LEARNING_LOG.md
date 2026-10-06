# Öğrenme Günlüğü — Kalkan

Her gün 17:00'de beş satır. **Kendi cümlelerinle yaz, agent'a yazdırma.** Burada anlatamadığın
şeyi bildiğin şey sayma.

---

## Gün 0 — 3 Ekim 2026

- **Ne yaptım:** Kalkan reposunu açtım (public), `kalkan` conda ortamını kurdum. Karpathy'nin
  *Software Is Changing (Again)* konuşmasını izledim.
- **LLM'lerin hangi zayıflığı CLAUDE.md'yi, hangisi Kalkan'ı gerekli kılıyor?**
  hafizasizlik claude.md'yi, saflik da kalkani gerekli kiliyor
- **"Yapay zekâyı tasmada tut" neden?**
  dogrulamak aslinda, ajan buyuk olcekte degisiklik yapabilir ama ben bunun takibini yapamam o
  yuzden kucuk parcalara bolunmesi gerekiyorki takip edebilelim
- **Mülakatçı sorsa: "Agent'lar kodu yazıyorsa sen ne yapıyorsun?"**
  Neyin dogru olup olmadigini ben karar veririm beklenenen degerleri vs, kanitlarim her diff veya
  olcumleri, ajan bazi seyleri bilmeyebilir ona ben veririm
- **Kafamda kalan soru:**

## Gün 1 — 3 Ekim 2026

- **Ne yaptım:** `SPEC.md`'yi yazdık. Deney (`deneyler/gun1/`): Türkçe para tutarı ayrıştırıcı. Plan
  mode'da belirsiz bir istek verdim, agentic loop'u izledim, beklenen değerleri kendim verip bilerek
  yanlış bir değer ekledim. Agent bir mevcut testle çelişkiyi fark edip durdu ve bana sordu.
- **Agent ile workflow arasındaki fark ne?**
  ajan kendi karar verir, is akisi sabit adimlar
- **Kalkan'da adımların sırasına bir model mi karar vermeli, yoksa sabit bir akış mı olmalı? Neden?**
  bilmiyorum
  *(Konuşmadan sonra:)* guvenlik icin her istek kontrolden gecmeli, model atlatilabilir o yuzden
  sabit workflow olmali
- **Kafamda kalan soru:**

## Gün 2 — 4 Ekim 2026

- **Ne yaptım:** DeepLearning.AI Claude Code kursundan 3 ders izledim. TCKN testlerinin beklenen
  değerlerine karar verdim (0 ile başlayan numara TCKN sayılmaz). Agent'a proje iskeletini
  (`pyproject.toml`, `src/kalkan/`), Kalkan'ın `CLAUDE.md`'sini, `.claude/settings.json` izinlerini
  ve 10 kırmızı TCKN testini yazdırdım (TDD'nin ilk adımı). Plan mode'da agent, ruff'ın `deneyler/`
  klasörüne bakıp bakmayacağını sordu, ben karar verdim.
- **c kuralı hem CLAUDE.md'de hem settings.json'daki deny'da yazıyor. Agent'ı gerçekten durduran hangisi?**
  deny olan
- **a–h kurallarından hangisi tavsiye olarak kalmamalı, hook olmalı?**
  d ve f olabilir cunku bir eylem ve sonrasinda aksiyon var
- **Kafamda kalan soru:**

## Gün 3 — 4 Ekim 2026

- **Ne yaptım:** f kuralını PostToolUse hook'una çevirdim (her düzenlemeden sonra pytest ve ruff),
  d kuralını `ask` izin kuralı yaptım. Agent "ask çalışmıyor" diye yanlış teşhis koydu. Aslında
  bana sormuştu, ben yanlışlıkla 1'e bastım. TCKN prompt'unu ilk kez kendim yazdım, agent
  `is_valid_tckn`'i yazdı ve 10 test yeşile döndü. ASCII olmayan rakamlar için iki test eklemeye
  karar verdim.
- **Hook'u bugün kim çalıştırdı, agent mı Claude Code mu? Fark neden önemli?**
  claude code calistirdi cunku kural olarak biz verdik agentin karar almasini beklemedik.
- **Kalkan neden her 11 haneli sayıyı maskelemiyor da kontrol hanelerine bakıyor?**
  genel tc no kuralimiz yuzunden
- **Kafamda kalan soru:**

## Gün 4 — 5 Ekim 2026

- **Ne yaptım:** Metnin içinden TCKN bulan `find_tckns`'i yaptırdım. Karar tablosunu ben verdim
  (boşluklu numara şimdilik bulunmuyor, harfe bitişik numara bulunuyor, daha uzun bir sayının
  parçası olan bulunmuyor). Prompt'u kendim yazdım. Plan mode'da agent'ın normalize yöntemine ve
  konumların orijinal metne göre kalmasına baktım. Sonra bir subagent'a incelettim. Subagent
  6 durum buldu. Üst simge ve daire içi rakamları düzelttirdim, görünmez karakterleri yarına bıraktım.
  27 test geçiyor.
- **İncelemeyi neden subagent'a yaptırdık, kodu yazan agent'a yaptırsaydık ne farklı olurdu?**
  temiz context ve tarafsız bakış
- **Yanlış alarm mı kaçırma mı, Kalkan için hangisi daha kötü? Neden?**
  kaçırma daha kötü
- **Kafamda kalan soru:**

## Gün 5 — 5 Ekim 2026

- **Ne yaptım (1. iş):** Görünmez karakterlerle (Unicode Cf: zero-width space, soft hyphen, ZWJ,
  RTL override) bölünmüş TCKN'leri buldurdum. Plan mode'da konumların orijinal metne nasıl geri
  eşlendiğine baktım (`positions` listesi). 3 test kırmızıdan yeşile döndü, 4 test regression guard
  olarak eklendi. 34 test geçiyor.
- **Konumları neden orijinal metne göre tutmak zorundayız?**
  konumlar kayardı yanlış yer maskelenirdi
- **Ne yaptım (2. iş):** `/clear` yapıp `mask_tckns` / `unmask` yaptırdım. Dört kararı ben verdim:
  aynı numaraya aynı etiket, eşlemede ASCII hâli, eşleme hiçbir yerde saklanmıyor, bilinmeyen
  etiketlere dokunulmuyor. Plan mode'da eşlemenin global bir yerde tutulmadığını kontrol ettim.
  45 test geçiyor.
- **Eşleme herkes için ortak tek bir tablo olsaydı, B müşterisine giden cevapta ne olabilirdi?**
  A müşterisinin numarası B'nin cevabında açılabilirdi
- **Kafamda kalan soru:**

## Gün 6 — 6 Ekim 2026

- **Ne yaptım:** Kalkan'ı OpenAI-uyumlu bir proxy yaptırdım (FastAPI → Ollama `gemma3:12b`).
  Altı karar verdim: bütün roller maskeleniyor, bir istekteki mesajlar tek eşlemeyi paylaşıyor,
  stream kapalı, maskesiz içerik loglanmıyor, sadece 127.0.0.1, Ollama kapalıysa 502. Demoyu kendim
  çalıştırdım. LLM sadece `[TCKN_1]` gördü. İlk turda model reddetti, ikinci turda cevaptaki etiket
  benim numarama geri açıldı. Agent'ın verdiği başlatma komutu çalışmadı, `pip install -e .`
  gerekiyordu. Agent `ask` kuralını python.exe'nin tam yolunu yazarak atlattı. Kalıbı genişlettim.
- **50 test yeşildi ama ilk çalıştırma hata verdi. Neden, nasıl önlenir?**
  baslatma olmadigi icin
- **ask kuralı neden atlatıldı, bunun Kalkan'la ilgisi ne?**
  cunku ask teki belirttimiz kural yazimla eslesmedigi icin
- **Kafamda kalan soru:**
