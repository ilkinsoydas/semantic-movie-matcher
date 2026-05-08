# 🎬 Semantic Movie Matcher: Hibrit Film Öneri Sistemi

Bu proje, sadece basit anahtar kelime eşleşmelerine dayanmayan, **içerik ve yaratıcı (Yönetmen/Oyuncu) dengesini** matematiksel olarak optimize eden, içerik tabanlı (Content-Based) bir film tavsiye algoritmasıdır. Model, "Yönetmen Sineması" ve "Tür Uyumu" arasındaki dengeyi korumak için özel ağırlıklandırma teknikleri kullanır.

                                                         Görsel örnektir

<img width="900" height="700" alt="image" src="https://github.com/user-attachments/assets/2ef2763f-2179-4c8d-94d5-948451f9a2c5" />


## 🚀 Öne Çıkan Teknik Özellikler

* **Zeki Metin Ön İşleme (NLP):** `NLTK PorterStemmer` kullanılarak kelimeler köklerine indirgenmiştir. Bu sayede "space", "spaces" ve "spacing" gibi kelimelerin aynı anlamsal paydada buluşması sağlanmıştır.
* **TF-IDF Vektörleştirme:** `CountVectorizer` (sadece kelime sayma) yerine, kelimelerin nadirliğini ve ayırt ediciliğini ölçen **TF-IDF (Term Frequency-Inverse Document Frequency)** kullanılmıştır. Bu sayede her filmde geçen sıradan kelimelerin puanı düşürülmüş, filme özgü anahtar kelimeler öne çıkarılmıştır.
* **Stratejik Ağırlıklandırma (Fine-Tuning):** Modelin "fazla yönetmen odaklı" veya "yanlış anahtar kelime odaklı" olmasını engellemek için özelliklere şu ağırlıklar verilmiştir:
    * 🎭 **Türler (Genres):** x5 (Tür uyumu ana öncelik).
    * 🎬 **Yönetmen (Crew):** x3 (Yönetmen dokunuşu korunur).
    * 🔑 **Anahtar Kelimeler:** x2 (Atmosferik benzerlik).
    * 👥 **Oyuncular:** x1 (Kadro benzerliği).



## 🧠 Algoritma Mantığı: Kosinüs Benzerliği

Model, her filmi 5000 boyutlu bir vektör uzayında temsil eder. İki film arasındaki benzerlik, bu vektörler arasındaki açının kosinüsü hesaplanarak bulunur. Formül:

$$similarity = \cos(\theta) = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|}$$



## 🛠️ Teknoloji Yığını

* **Dil:** Python 3.x
* **Kütüphaneler:** * `Pandas` & `NumPy` (Veri manipülasyonu)
    * `Scikit-learn` (TfidfVectorizer, Cosine Similarity)
    * `NLTK` (Natural Language Toolkit - Stemming)
    * `Pickle` (Model Serileştirme)

## 📊 Örnek Tavsiye Sonuçları

Modelin hibrit yapısı sayesinde, hem yönetmen tarzını hem de tür benzerliğini koruyan sonuçlar elde edilmiştir:

| Aratılan Film | Öneri 1 | Öneri 2 | Öneri 3 |
| :--- | :--- | :--- | :--- |
| **Pulp Fiction** | Kill Bill: Vol. 2 | Reservoir Dogs | Easy Money |
| **Avatar** | Aliens | Jupiter Ascending | Star Trek Into Darkness |

## ⚙️ Kurulum ve Kullanım

1.  Projenizi klonlayın:
    ```bash
    git clone [https://github.com/ilkinsoydas/semantic-movie-matcher.git](https://github.com/ilkinsoydas/semantic-movie-matcher.git)
    cd semantic-movie-matcher
    ```
2.  Gerekli kütüphaneleri yükleyin:
    ```bash
    pip install pandas numpy scikit-learn nltk
    ```
3.  Modeli çalıştırın:
    ```bash
    python semanticMovieMatcher.py
    ```

    ## 📊 Örnek Çıktılar

Modelin tür ve yönetmen ağırlıklı dengesi sayesinde elde edilen gerçek dünya sonuçlarından bazıları şunlardır:

| Aratılan Film | Öneri 1 | Öneri 2 | Öneri 3 |
| :--- | :--- | :--- | :--- |
| **Pulp Fiction** | Kill Bill: Vol. 2 | Reservoir Dogs | Easy Money |
| **Avatar** | Aliens | Jupiter Ascending | Star Trek Into Darkness |

> **💡 Kritik Geliştirme Notu:** > Projenin geliştirme aşamasında, sadece anahtar kelimelere odaklanmanın bir yan etkisi olarak; içinde boksör karakteri bulunan *Pulp Fiction* gibi filmlerde algoritmanın tüm listeyi alakasız boks filmlerine çevirdiği (Ali, Million Dollar Baby vb.) gözlemlenmiştir. 
> 
> Bu durumun önüne geçmek ve öneri kalitesini korumak için **"ince ayar" (fine-tuning)** süreci uygulanmış; tür ve yönetmen ağırlıkları artırılırken, spesifik anahtar kelimelerin (keywords) baskınlığı optimize edilmiştir. Bu sayede model, sadece kelime eşleşmesine değil, filmin genel "ruhuna" odaklanır hale getirilmiştir.

---
*Bu proje, veri biliminde "ince ayar" (fine-tuning) süreçlerinin öneri kalitesi üzerindeki etkisini gözlemlemek amacıyla geliştirilmiştir.*
