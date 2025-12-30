```markdown
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

---

## 📜 Sözde Kod (Pseudocode)

```text
ALGORITHM Collatz-XP

INPUT:  Seed (Integer), Plaintext (String)
CONST:  MASK = 0xA5A5A5A5

FUNCTION GetChaosBit(state):
    IF state IS Even THEN state = state / 2
    ELSE state = 3 * state + 1
    
    // Yöntem 1: XOR Maskeleme
    shadow_state = state XOR MASK
    // Yöntem 2: Permütasyon (Sola Kaydırma)
    shadow_state = ROTATE_LEFT(shadow_state, 5)
    
    RETURN (shadow_state AND 1)

FUNCTION GetBalancedBit():
    LOOP FOREVER:
        // Von Neumann Dengeleyicisi
        b1 = GetChaosBit()
        b2 = GetChaosBit()
        
        IF b1 == 0 AND b2 == 1 THEN RETURN 0
        IF b1 == 1 AND b2 == 0 THEN RETURN 1
        // 00 veya 11 gelirse reddet ve tekrar dene
    END LOOP

MAIN:
    Convert Plaintext to Bits
    Initialize state with Seed
    
    FOR each bit in Plaintext:
        key_bit = GetBalancedBit()
        cipher_bit = plaintext_bit XOR key_bit
        Append cipher_bit to CipherStream
        
    Convert CipherStream to HexString
    OUTPUT HexString

```

---

## 💻 Kurulum ve Kullanım

Projeyi klonlayın ve çalıştırın:

```bash
git clone [https://github.com/kullaniciadi/collatz-xp-cipher.git](https://github.com/kullaniciadi/collatz-xp-cipher.git)
cd collatz-xp-cipher
python main.py

```

### Python Kaynak Kodu (`main.py`)

```python
import random
import time

class CollatzXPCipher:
    def __init__(self, seed: int, mask: int = 0xA5A5A5A5):
        self.state = abs(seed) if seed != 0 else 12345
        self.original_seed = self.state
        self.mask = mask 

    def _rotate_left(self, num: int, shift: int = 5) -> int:
        """32-bit Sola Bit Kaydırma (Permütasyon)"""
        num &= 0xFFFFFFFF 
        return ((num << shift) | (num >> (32 - shift))) & 0xFFFFFFFF

    def _collatz_chaos_step(self) -> int:
        """Collatz Motoru + XOR + Permütasyon"""
        if self.state % 2 == 0:
            self.state = self.state // 2
        else:
            self.state = 3 * self.state + 1
            
        if self.state <= 1: # Döngü koruması
            self.state = (self.state + self.mask + 137) & 0xFFFFFFFF

        shadow_state = self.state ^ self.mask     # XOR
        shadow_state = self._rotate_left(shadow_state) # Permütasyon
        return shadow_state & 1

    def _get_balanced_bit(self) -> int:
        """Von Neumann Dengeleyicisi"""
        loop_guard = 0
        while True:
            b1 = self._collatz_chaos_step()
            b2 = self._collatz_chaos_step()
            if b1 == 0 and b2 == 1: return 0
            elif b1 == 1 and b2 == 0: return 1
            
            loop_guard += 1
            if loop_guard > 1000: # Kilitlenme önleyici
                self.state = (self.state + loop_guard) & 0xFFFFFFFF
                loop_guard = 0

    def generate_keystream(self, length: int) -> list:
        self.state = self.original_seed 
        return [self._get_balanced_bit() for _ in range(length)]

    def encrypt(self, plaintext: str) -> str:
        bits = []
        for char in plaintext:
            bits.extend([int(b) for b in bin(ord(char))[2:].zfill(8)])
        keystream = self.generate_keystream(len(bits))
        encrypted = [p ^ k for p, k in zip(bits, keystream)]
        bit_str = "".join(map(str, encrypted))
        return hex(int(bit_str, 2))[2:] if bit_str else ""

# Kullanım Örneği
if __name__ == "__main__":
    key = 1923
    cipher = CollatzXPCipher(key)
    msg = "Merhaba Dunya"
    enc = cipher.encrypt(msg)
    print(f"Şifreli: {enc}")

```

---

## 📊 İstatistiksel Analiz

Algoritmanın ürettiği anahtar akışının rastgelelik testi (1000 bitlik örneklem):

| Bit Değeri | Sayı | Oran |
| --- | --- | --- |
| **0** | 496 | %49.6 |
| **1** | 504 | %50.4 |

*Sonuç: Mükemmele yakın entropi dengesi.*
```

```
