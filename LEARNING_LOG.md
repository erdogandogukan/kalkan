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
