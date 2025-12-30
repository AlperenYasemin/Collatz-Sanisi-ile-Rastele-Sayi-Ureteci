import random
import time


class CollatzXPCipher:
    def __init__(self, seed: int, mask: int = 0xA5A5A5A5):
        # Seed 0 veya negatif olmamalı
        self.state = abs(seed) if seed != 0 else 12345
        self.original_seed = self.state
        self.mask = mask

    def _rotate_left(self, num: int, shift: int = 5) -> int:
        """32-bit Sola Bit Kaydırma"""
        num &= 0xFFFFFFFF
        return ((num << shift) | (num >> (32 - shift))) & 0xFFFFFFFF

    def _collatz_chaos_step(self) -> int:
        """
        DÜZELTİLMİŞ MOTOR:
        State sadece Collatz kurallarıyla değişir.
        Çıktı (bit) ise XOR ve Permütasyon ile üretilir.
        """

        # 1. Collatz Yörüngesinde İlerle (State Güncellemesi)
        if self.state % 2 == 0:
            self.state = self.state // 2
        else:
            self.state = 3 * self.state + 1

        # Kilitlenme Önleyici: Eğer 4-2-1 döngüsüne (1'e) düşerse
        # Veya sayı 0 olursa (safety check)
        if self.state <= 1:
            # State'i maske ile "tuzlayarak" yeniden fırlat
            self.state = (self.state + self.mask + 137) & 0xFFFFFFFF
            if self.state == 0: self.state = 12345  # Asla 0 olmasına izin verme

        # 2. Bit Üretimi (State'i bozmadan maskele ve karıştır)
        # Burası "Gölge State" üzerinde çalışır
        shadow_state = self.state ^ self.mask  # YÖNTEM 1: XOR
        shadow_state = self._rotate_left(shadow_state)  # YÖNTEM 2: Permütasyon

        return shadow_state & 1

    def _get_balanced_bit(self) -> int:
        """
        VON NEUMANN DENGELEYİCİSİ
        Artık donmayacak çünkü Collatz sürekli yeni sayılar üretiyor.
        """
        loop_guard = 0
        while True:
            b1 = self._collatz_chaos_step()
            b2 = self._collatz_chaos_step()

            # 01 -> 0 kabul et
            if b1 == 0 and b2 == 1:
                return 0
            # 10 -> 1 kabul et
            elif b1 == 1 and b2 == 0:
                return 1

            # 00 veya 11 gelirse devam et (Discard)

            # Acil Durum Çıkışı (Sonsuz döngüden koruma sigortası)
            loop_guard += 1
            if loop_guard > 1000:
                # Çok nadir durumda buraya düşerse rastgelelik ekle
                self.state = (self.state + loop_guard) & 0xFFFFFFFF
                loop_guard = 0

    def generate_keystream(self, length: int) -> list:
        print(f"Anahtar üretiliyor ({length} bit)... ", end="", flush=True)
        self.state = self.original_seed
        keystream = []
        for _ in range(length):
            keystream.append(self._get_balanced_bit())
        print("Tamamlandı.")
        return keystream

    def str_to_bits(self, text: str) -> list:
        bits = []
        for char in text:
            # Türkçe karakter desteği için utf-8 encode
            bytes_val = char.encode('utf-8')
            for b in bytes_val:
                bin_val = bin(b)[2:].zfill(8)
                bits.extend([int(bit) for bit in bin_val])
        return bits

    def bits_to_str(self, bits: list) -> str:
        chars = []
        # Bitleri byte'lara dönüştür
        byte_array = bytearray()
        for i in range(0, len(bits), 8):
            byte_chunk = bits[i:i + 8]
            if len(byte_chunk) < 8: break
            byte_val = int("".join(map(str, byte_chunk)), 2)
            byte_array.append(byte_val)

        try:
            return byte_array.decode('utf-8')
        except UnicodeDecodeError:
            return "[Hata: Karakter çözülemedi - Yanlış Anahtar?]"

    def encrypt(self, plaintext: str) -> str:
        plaintext_bits = self.str_to_bits(plaintext)
        keystream = self.generate_keystream(len(plaintext_bits))
        encrypted_bits = [p ^ k for p, k in zip(plaintext_bits, keystream)]
        bit_str = "".join(map(str, encrypted_bits))
        # Hex'e çevirirken boş string kontrolü
        if not bit_str: return ""
        return hex(int(bit_str, 2))[2:]

    def decrypt(self, ciphertext_hex: str) -> str:
        try:
            val = int(ciphertext_hex, 16)
            bit_str = bin(val)[2:]
            padding = (8 - len(bit_str) % 8) % 8
            bit_str = "0" * padding + bit_str
            encrypted_bits = [int(b) for b in bit_str]
        except ValueError:
            return "Hata: Geçersiz Hex"

        keystream = self.generate_keystream(len(encrypted_bits))
        decrypted_bits = [c ^ k for c, k in zip(encrypted_bits, keystream)]
        return self.bits_to_str(decrypted_bits)


# --- ANA PROGRAM ---
if __name__ == "__main__":
    # Test için basit ve karmaşık seedler
    seeds = [1923, 987654321]

    for s in seeds:
        print(f"\n--- TEST BAŞLIYOR (SEED: {s}) ---")
        cipher = CollatzXPCipher(seed=s)

        # 1. Analiz Testi
        start_time = time.time()
        print("İstatistik toplanıyor...")
        try:
            sample_bits = cipher.generate_keystream(1000)
            zeros = sample_bits.count(0)
            ones = sample_bits.count(1)
            print(f"Süre: {time.time() - start_time:.4f} sn")
            print(f"0 Sayısı: {zeros} | 1 Sayısı: {ones}")
            print(f"Denge: %{ones / 10:.1f}")
        except KeyboardInterrupt:
            print("İşlem kullanıcı tarafından durduruldu!")
            break

        # 2. Şifreleme Testi
        mesaj = "Merhaba Dünya! Collatz Çalışıyor."
        sifreli = cipher.encrypt(mesaj)
        print(f"Şifreli: {sifreli}")

        cozulen = cipher.decrypt(sifreli)
        print(f"Çözülen: {cozulen}")

        if mesaj == cozulen:
            print(">>> DOĞRULAMA: BAŞARILI <<<")
        else:
            print(">>> DOĞRULAMA: HATALI <<<")