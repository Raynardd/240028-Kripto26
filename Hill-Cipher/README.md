# Program Kriptografi: Hill Cipher (Ordo 2x2)

Program implementasi algoritma **Hill Cipher 2x2** berbasis bahasa pemrograman Python yang mendukung tiga fungsionalitas utama: **Enkripsi**, **Dekripsi**, dan **Pencarian Kunci (Known-Plaintext Attack)**.

---

## 1. Alur & Struktur Program

Program bekerja dengan memanfaatkan operasi matriks dalam aritmatika modulo 26 ($\mathbb{Z}_{26}$):

### A. Modular Invers & Extended Euclidean Algorithm (`egcd`, `mod_inverse`)
* Menghitung nilai invers modulo dari suatu integer $a \pmod{26}$ menggunakan *Extended Euclidean Algorithm*.
* Memastikan nilai determinan memenuhi $\gcd(\det(M), 26) = 1$. Jika tidak memenuhi, invers matriks tidak dapat dibentuk.

### B. Invers Matriks 2x2 Modulo 26 (`matrix_mod_inverse_2x2`)
* Menghitung determinan matriks $M$: $\det(M) = (ad - bc) \bmod 26$.
* Menghitung invers determinan: $\det(M)^{-1} \pmod{26}$.
* Membentuk matriks Adjoin:
  $$\text{Adj}(M) = \begin{bmatrix} d & -b \\ -c & a \end{bmatrix} \pmod{26}$$
* Menghasilkan matriks invers:
  $$M^{-1} = (\det(M)^{-1} \cdot \text{Adj}(M)) \pmod{26}$$

### C. Fungsionalitas Operasi
1. **Enkripsi (`encrypt_hill`):**
   * Mengubah plaintext menjadi huruf kapital dan membuang karakter non-alfabet.
   * Melakukan padding huruf `X` jika panjang karakter ganjil.
   * Membagi teks menjadi vektor kolom berukuran $2 \times 1$ dan mengalikannya dengan matriks kunci $K$:
     $$C = K \cdot P \pmod{26}$$
2. **Dekripsi (`decrypt_hill`):**
   * Menghitung invers matriks kunci $K^{-1} \pmod{26}$.
   * Mengalikan setiap blok ciphertext dengan $K^{-1}$:
     $$P = K^{-1} \cdot C \pmod{26}$$
3. **Pencarian Kunci (`find_key_hill`):**
   * Menggunakan metode *Known-Plaintext Attack* dengan minimal 2 blok pasangan teks ($4$ karakter).
   * Menyusun matriks $P$ dan $C$ berukuran $2 \times 2$ dari blok kolom.
   * Menghitung kunci $K$ dengan formula:
     $$K = C \cdot P^{-1} \pmod{26}$$
   * *Catatan matematis:* Blok plaintext yang dipilih harus menghasilkan determinan yang koprima dengan 26 ($\gcd(\det(P), 26) = 1$).

---

## 2. Cara Menjalankan Program

Pastikan Python 3 sudah terpasang pada sistem operasi:

```bash
cd Hill-Cipher
python hillcipher.py
```

Pilih menu yang tersedia di terminal:
* Masukkan pilihan `1` untuk Enkripsi.
* Masukkan pilihan `2` untuk Dekripsi.
* Masukkan pilihan `3` untuk Mencari Kunci (*Known-Plaintext Attack*).
* Masukkan pilihan `4` untuk Keluar.

---

## 3. Screenshot Running Program

### A. Pengujian Enkripsi & Dekripsi
Pengujian menggunakan teks `MAGANG` dengan matriks kunci $K = \begin{bmatrix} 7 & 6 \\ 2 & 5 \end{bmatrix}$:
* **Enkripsi:** `MAGANG` $\rightarrow$ `GYQMXE`
* **Dekripsi:** `GYQMXE` $\rightarrow$ `MAGANG`

![Screenshot Enkripsi dan Dekripsi](screenshot_enkripsi_dekripsi_hill.png)

### B. Pengujian Pencarian Kunci (Known-Plaintext Attack)
Pengujian pencarian kunci menggunakan pasangan sampel valid:
* **Plaintext:** `FRIDAY`
* **Ciphertext:** `PQCFKU`
* **Hasil Kunci Ditemukan:**
  $$\begin{bmatrix} 7 & 8 \\ 19 & 3 \end{bmatrix}$$

![Screenshot Cari Kunci](screenshot_cari_kunci_hill.png)