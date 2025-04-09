# 🏥 Sigorta Ücreti Tahmin Uygulaması

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-Learn"/>
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas"/>
  <img src="https://img.shields.io/badge/Matplotlib-3776AB?style=for-the-badge&logo=matplotlib&logoColor=white" alt="Matplotlib"/>
</div>

<p align="center">
  <img src="https://miro.medium.com/v2/resize:fit:1400/1*cG6U1qstYDijh9bPL42e-Q.jpeg" alt="Sigorta Ücreti Tahmin" width="600"/>
</p>

## 📋 Proje Tanımı

Bu web uygulaması, kişilerin demografik ve sağlık bilgilerine dayanarak sağlık sigortası ücretlerini tahmin eder. Üç farklı makine öğrenmesi modeli kullanarak en doğru tahmini yapmayı amaçlar ve modellerin performansını karşılaştırmalı olarak gösterir.

## ✨ Özellikler

- **Çoklu Model Tahmini:** Üç farklı regresyon algoritması kullanarak sigorta ücretini tahmin eder:

  - 📊 **Linear Regression:** Basit ve yorumlanabilir sonuçlar
  - 🌲 **Decision Tree:** Karmaşık, doğrusal olmayan ilişkileri yakalayabilme
  - 🌳 **Random Forest:** Yüksek doğruluk ve dayanıklılık

- **Performans Karşılaştırması:** Her modelin performansını üç farklı metrik ile değerlendirir:

  - 📉 **MSE (Mean Squared Error):** Ortalama kare hata
  - 📉 **MAE (Mean Absolute Error):** Ortalama mutlak hata
  - 📈 **R² Skoru:** Tahmin performansı değeri (1'e yakın olması daha iyi)

- **Etkileşimli Arayüz:** Kullanıcı dostu Streamlit arayüzü ile parametreleri kolayca ayarlama

  - 👩‍👨 Yaş, cinsiyet, vücut kitle indeksi (BMI)
  - 👨‍👩‍👧‍👦 Çocuk sayısı
  - 🚬 Sigara içme durumu
  - 🗺️ Bölgesel konum

- **Görsel Analiz:** Tahmin sonuçlarını ve model performansını karşılaştıran grafikler

## 🚀 Kurulum ve Çalıştırma

1. Gerekli paketleri yükleyin:

```bash
pip install -r requirements.txt
```

2. Model dosyalarını oluşturun:

```bash
python save_model.py
```

3. Web uygulamasını başlatın:

```bash
streamlit run app.py
```

4. Tarayıcınızda otomatik olarak açılan uygulama ile tahminler yapabilirsiniz (varsayılan: http://localhost:8501)

## 📊 Veri Seti

Projede kullanılan `insurance.csv` veri seti aşağıdaki özellikleri içerir:

| Özellik  | Açıklama                                        | Tip       |
| -------- | ----------------------------------------------- | --------- |
| age      | Sigortalının yaşı                               | Sayısal   |
| sex      | Sigortalının cinsiyeti (erkek/kadın)            | Kategorik |
| bmi      | Vücut kitle indeksi                             | Sayısal   |
| children | Bakmakla yükümlü olunan çocuk sayısı            | Sayısal   |
| smoker   | Sigara içme durumu (evet/hayır)                 | Kategorik |
| region   | ABD'deki yerleşim bölgesi                       | Kategorik |
| charges  | Sağlık sigortası ücreti (tahmin edilecek değer) | Sayısal   |

## 🔍 Kod Yapısı

Proje üç ana dosyadan oluşur:

- **app.py**: Streamlit web arayüzü ve kullanıcı etkileşimleri
- **save_model.py**: Veri ön işleme, model eğitimi ve kaydı
- **requirements.txt**: Gerekli Python paketleri

Ayrıca uygulama aşağıdaki dosyaları oluşturur ve kullanır:

- **model dosyaları (`*_model.pkl`)**: Eğitilmiş modeller
- **scaler.pkl**: Özellikleri standartlaştırmak için kullanılan scaler
- **columns.pkl**: Model eğitiminde kullanılan sütun isimleri
- **metrics.pkl**: Model performans metrikleri

## 📌 Kullanım İpuçları

- **BMI Hesaplama**: BMI değerinizi bilmiyorsanız, kilonuzu (kg) / boyunuzun karesi (m²) formülüyle hesaplayabilirsiniz
- **En İyi Model**: Genellikle R² skoru en yüksek olan model (Random Forest) en iyi tahmini verir
- **Sigara Kullanımı**: Sigara kullanımı sigorta ücretini önemli ölçüde artıran faktördür
- **Yaş Faktörü**: Yaş arttıkça sigorta ücretleri genellikle artış gösterir

## 📊 Model Başarım Karşılaştırması

| Model             | MSE     | MAE  | R² Skoru |
| ----------------- | ------- | ---- | -------- |
| Linear Regression | ~40,000 | ~150 | ~0.78    |
| Decision Tree     | ~25,000 | ~120 | ~0.86    |
| Random Forest     | ~15,000 | ~90  | ~0.92    |

_Not: Değerler örnek olarak verilmiştir, gerçek değerler modelin eğitildiği veri setine göre değişiklik gösterebilir._

## 🧠 Teknik Detaylar

- **Özellik Mühendisliği**: Sigara kullanımı ile BMI ve yaş arasındaki etkileşimi yakalamak için çarpımsal özellikler eklenmiştir
- **Standartlaştırma**: Özelliklerin ölçekleri farklı olduğu için StandardScaler kullanılmıştır
- **Hiperparametre**: Random Forest ve Decision Tree modelleri için random_state=24 kullanılmıştır
- **Session State**: Streamlit uygulamasında sayfayı yeniden yükleme sırasında durumu korumak için session state kullanılmıştır

---

<p align="center">
  Sağlıklı günler ve uygun sigorta ücretleri dileriz! 🏥💰
</p>
