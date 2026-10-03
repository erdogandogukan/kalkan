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
