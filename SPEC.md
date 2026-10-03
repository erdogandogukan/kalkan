# Kalkan — Spesifikasyon

## 1. Tek cümle
Kalkan, LLM'e giden mesajları koruyan bir güvenlik katmanı.

## 2. Problem
KVKK ve saldırılar. Yaygın araçlar Türkçe desteklemiyor.

## 3. Kullanıcı
Yazılımcı kullanır. Hiçbir model eğitmez, kodunda sadece LLM'in adresini Kalkan'ın adresiyle
değiştirir. Kalkan'ın içindeki saldırı dedektörünü biz eğitiriz.

## 4. Kapsam: 6 haftada ne yapacak
- Türkçe kişisel veri maskeleme (TCKN, IBAN, kart, telefon, e-posta, VKN, plaka) ve cevapta geri açma
- Mevcut dedektörlerin Türkçe saldırıları ne kadar kaçırdığını ölçen bir benchmark
- Bizim eğittiğimiz Türkçe saldırı dedektörü
- OpenAI-uyumlu geçit: yazılımcı sadece adresi değiştirir
- Akış hâlinde gelen (streaming) cevapları parça parça kontrol etme
- RAG belgelerinde ve MCP araç tanımlarında gizli talimat taraması
- Denetim kaydı (PostgreSQL), API anahtarı, hız sınırı
- İzleme panosu (Prometheus + Grafana)
- CI'da benchmark kapısı
- Tek bir buluta (AWS) yayına alma

## 5. Kapsam dışı: ne YAPMAYACAK
- İsim ve adres gibi serbest metindeki kişisel veriyi bulmak. Bunun için ayrı bir model gerekir,
  6 haftaya sığmıyor
- Kubernetes (k3s) + Helm ve React yönetim paneli (6. haftadan sonra opsiyonel)
- Türkçe dışındaki diller
- Yeni saldırı içeriği üretmek. Yalnızca açık, yayımlanmış veri setleri ve bilinen biçim
  dönüşümleri kullanılır
- LLM'in kendisini eğitmek ya da değiştirmek. Kalkan bir LLM değildir, cevap üretmez

## 6. Kabul kriterleri: "bitti" ne demek
1. Geçerli bir TCKN içeren istek LLM'e `[TCKN_1]` olarak maskeli gider. Cevaptaki `[TCKN_1]`
   kullanıcıya gerçek numara olarak geri açılır.
2. Checksum'ı tutmayan 11 haneli bir sayı maskelenmez. IBAN için mod-97, kart için Luhn kontrolü
   aynı şekilde geçerlidir.
3. OpenAI Python SDK'da yalnızca `base_url` değiştirilerek Kalkan üzerinden istek gönderilir ve
   cevap alınır. Başka bir kod değişikliği gerekmez.
4. Dedektörün "saldırı" dediği istek LLM'e hiç gönderilmez. İstemciye isteğin engellendiğini bildiren
   bir hata döner ve olay denetim kaydına yazılır.
5. Benchmark tek komutla çalışır ve aynı veriyle her seferinde aynı sayıları üretir.
6. Kalkan'ın dedektörü ile Prompt Guard 2, aynı Türkçe test setinde ve aynı koşulda (FPR %1)
   ölçülür, sonuçlar yan yana raporlanır.
7. İçine talimat gömülmüş bir RAG belgesi yakalanır ve kayda geçer.
8. Streaming cevapta iki parçaya bölünmüş bir TCKN de maskelenir.
9. CI'da benchmark'ın recall'u düşerse ya da yanlış alarm oranı artarsa build kırmızı olur.

## 7. Başarıyı nasıl ölçeceğim
- **Dedektör:** FPR %1'de recall (hedef: ?) · masum Türkçe prompt'larda yanlış alarm oranı (hedef: ≤ %1)
- **Kıyas:** Prompt Guard 2'nin aynı setteki recall'u
- **Maskeleme:** kirli gerçekçi metinde, veri türü başına yakalama oranı ve yanlış maskeleme oranı
- **Gecikme:** Kalkan'ın isteğe eklediği gecikme, p50 ve p95 (hedef: ?)

## 8. Açık sorular
- Masum Türkçe prompt'ları nereden bulacağız? Yanlış alarm ölçümü buna bağlı.
- Kullanacağımız veri setlerinin lisansları benchmark'ı yayınlamaya izin veriyor mu?
- Maskeleme eşleme tablosu (TCKN ↔ `[TCKN_1]`) nerede ve ne kadar süre tutulacak?
- Dedektör emin olamazsa ne olacak: engellensin mi, uyarı mı verilsin, sadece kayda mı geçsin?
- Gecikme bütçesi ne olmalı?
