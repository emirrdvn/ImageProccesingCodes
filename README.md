# 📌 Su Altı Görev Dronu - README

## 🚀 Proje Hakkında
Bu proje, su altı görevleri için geliştirilen otonom bir insansız su altı aracıdır (AUV). 
Ekip olarak geliştirdiğimiz bu dron, su altında çeşitli nesneleri tanıyıp üzerlerine iniş kalkış ve süzülme gibi çeşitli görevler için görüntü işleme ve otonom yönetim teknolojilerini kullanır. 

## 🔥 Temel Özellikler
- **Görüntü İşleme:** Şekil, renk ve derinlik algılama özellikleri
- **Motor Kontrolü:** Rasperry Pi Pico ile motor yönetimi
- **Gelişmiş İşlemci:** NVIDIA Jetson Nano ile yüksek performanslı görüntü işleme
- **Otonom Navigasyon:** Önceden belirlenen rotalarda veya nesne tanıma yoluyla bağımsız hareket edebilme
- **Gerçek Zamanlı Veri İşleme:** Kameralar aracılığıyla anlık analiz yapma

## 🛠 Kullanılan Teknolojiler
- **Donanım:**
  - Rasperry Pi Pico (Motor kontrolü için)
  - NVIDIA Jetson Nano (Görüntü işleme için)
  - Su geçirmez kamera sensörleri
- **Yazılım & Kütüphaneler:**
  - OpenCV (Görüntü işleme için)
  - Python (Genel yazılım geliştirme)
  - ROS (Robotik sistem yönetimi için)

## 📦 Kurulum
### 1. Gerekli Bağımlılıkları Yükleyin
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip
pip3 install opencv-python 
```

## 🚤 Nasıl Çalışır?
1. Su altı kamerasından alınan görüntü NVIDIA Jetson Nano tarafından işlenir.
2. OpenCV kullanılarak nesnelerin rengi, şekli ve derinliği tespit edilir.
3. Algılanan nesnelere göre motorlar Rasperry Pi Pico üzerinden kontrol edilir.
4. Dron, verilen görevlere uygun şekilde hareket eder.

## 🤝 Katkıda Bulunun
Eğer projeye katkıda bulunmak isterseniz, lütfen bir **pull request** açın veya bir **issue** oluşturun.

## 📜 Lisans
Bu proje MIT lisansı ile lisanslanmıştır.
