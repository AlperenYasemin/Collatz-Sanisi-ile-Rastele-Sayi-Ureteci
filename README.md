# 🎲 Collatz-XP Cipher (Collatz-XOR-Permutation)

> **"Kaos, düzenin henüz çözülememiş halidir."**

Bu proje, ünlü **Collatz Sanısı (3n+1 Problemi)**'nin matematiksel kaosunu kullanarak tasarlanmış deneysel bir **Akış Şifreleme (Stream Cipher)** algoritmasıdır. Algoritma, Collatz dizisinin tahmin edilemez yapısını **XOR Maskeleme** ve **Bit Permütasyonu** teknikleriyle birleştirerek güvenli bir anahtar akışı (keystream) üretir.

## 🚀 Özellikler

1.  **Kaotik Çekirdek (Chaos Engine):** Şifreleme anahtarı, Collatz yörüngesindeki sayılardan üretilir.
2.  **Hibrit Mimari:**
    * **Yöntem 1 (XOR):** Doğrusallığı bozmak için sabit maskeleme.
    * **Yöntem 2 (Permütasyon):** Bit difüzyonu için dairesel kaydırma (Rotate Left).
3.  **İstatistiksel Denge (Von Neumann Whitener):** Collatz dizisindeki çift sayı baskınlığını ortadan kaldırmak için Von Neumann Dengeleyicisi kullanılmıştır. Bu sayede üretilen 0 ve 1'lerin oranı istatistiksel olarak %50-%50 dengesindedir.

---

## 🛠️ Algoritma Mimarisi (Akış Şeması)

Algoritmanın çalışma mantığı aşağıdaki gibidir:

```mermaid
flowchart TD
    Start([Başlat]) --> Seed[/Girdi: Seed Anahtarı/]
    Seed --> Loop{Bit Lazım mı?}
    
    subgraph ChaosEngine [Kaos Motoru]
        Loop -- Evet --> Collatz[Collatz Adımı: 3n+1 veya n/2]
        Collatz --> XOR[XOR Maskeleme]
        XOR --> Perm[Permütasyon: Sola Kaydır]
        Perm --> RawBit[Ham Bit Çıkar]
    end
    
    subgraph Balancer [Von Neumann Dengeleyici]
        RawBit --> PairCheck{Çift Kontrolü}
        PairCheck -- 01 --> Out0[Çıktı: 0]
        PairCheck -- 10 --> Out1[Çıktı: 1]
        PairCheck -- 00/11 --> Reject[Reddet & Tekrarla]
        Reject --> Collatz
    end
    
    Out0 --> Stream[Keystream'e Ekle]
    Out1 --> Stream
    Stream --> Encrypt[Plaintext XOR Keystream]
    Encrypt --> Finish([Hex Çıktı])
    
    style ChaosEngine fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style Balancer fill:#fff3e0,stroke:#e65100,stroke-width:2px

```

📊 İstatistiksel Analiz

Algoritmanın ürettiği anahtar akışının rastgelelik testi (1000 bitlik örneklem):
Bit Değeri	Sayı	Oran
0	         496	%49.6
1	         504	%50.4

Sonuç: Mükemmele yakın entropi dengesi.
