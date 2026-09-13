def egcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = egcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inv(a, m=26):
    gcd, x, _ = egcd(a % m, m)
    if gcd != 1:
        return None
    return (x % m + m) % m

def get_inv_matrix(mat, m=26):
    det = (mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]) % m
    inv_det = mod_inv(det, m)
    if inv_det is None:
        return None
    
    # adjoin matriks 2x2: swap diagonal utama, negasikan diagonal samping
    adj = [
        [mat[1][1] % m, (-mat[0][1]) % m],
        [(-mat[1][0]) % m, mat[0][0] % m]
    ]
    
    # kalikan adjoin dengan 1/det mod 26
    inv_mat = [
        [(adj[r][c] * inv_det) % m for c in range(2)]
        for r in range(2)
    ]
    return inv_mat

def sanitize(text):
    return "".join([c.upper() for c in text if c.isalpha()])

def encrypt(pt, key):
    pt = sanitize(pt)
    # tambah padding kalau ganjil
    if len(pt) % 2 != 0:
        pt += 'X'
        
    ct = ""
    for i in range(0, len(pt), 2):
        p1 = ord(pt[i]) - 65
        p2 = ord(pt[i+1]) - 65
        c1 = (key[0][0] * p1 + key[0][1] * p2) % 26
        c2 = (key[1][0] * p1 + key[1][1] * p2) % 26
        ct += chr(c1 + 65) + chr(c2 + 65)
    return ct

def decrypt(ct, key):
    inv_key = get_inv_matrix(key, 26)
    if inv_key is None:
        return None, "Error: determinan kunci tidak punya invers di mod 26"
    
    ct = sanitize(ct)
    pt = ""
    for i in range(0, len(ct), 2):
        c1 = ord(ct[i]) - 65
        c2 = ord(ct[i+1]) - 65
        p1 = (inv_key[0][0] * c1 + inv_key[0][1] * c2) % 26
        p2 = (inv_key[1][0] * c1 + inv_key[1][1] * c2) % 26
        pt += chr(p1 + 65) + chr(p2 + 65)
    return pt, None

def find_key(pt_raw, ct_raw):
    pt = sanitize(pt_raw)
    ct = sanitize(ct_raw)
    
    if len(pt) < 4 or len(ct) < 4:
        return None, "Panjang teks minimal 4 huruf (2 blok 2x1)"
    
    # pecah per 2 huruf jadi vektor kolom
    num_blocks = min(len(pt), len(ct)) // 2
    b_P = [[ord(pt[2*i]) - 65, ord(pt[2*i+1]) - 65] for i in range(num_blocks)]
    b_C = [[ord(ct[2*i]) - 65, ord(ct[2*i+1]) - 65] for i in range(num_blocks)]
    
    # cari pasangan 2 blok sembarang yang determinannya coprime sama 26
    for i in range(num_blocks):
        for j in range(i + 1, num_blocks):
            P = [
                [b_P[i][0], b_P[j][0]],
                [b_P[i][1], b_P[j][1]]
            ]
            C = [
                [b_C[i][0], b_C[j][0]],
                [b_C[i][1], b_C[j][1]]
            ]
            
            inv_P = get_inv_matrix(P, 26)
            if inv_P is not None:
                # K = C * P^-1 mod 26
                K = [
                    [(C[0][0] * inv_P[0][0] + C[0][1] * inv_P[1][0]) % 26, 
                     (C[0][0] * inv_P[0][1] + C[0][1] * inv_P[1][1]) % 26],
                    [(C[1][0] * inv_P[0][0] + C[1][1] * inv_P[1][0]) % 26, 
                     (C[1][0] * inv_P[0][1] + C[1][1] * inv_P[1][1]) % 26]
                ]
                return K, None
                
    return None, "Semua kombinasi matriks P determinannya genap/kelipatan 13 (tidak invertible)"

def input_key():
    print("Masukkan matriks kunci 2x2:")
    k00, k01 = map(int, input("Baris 1: ").split())
    k10, k11 = map(int, input("Baris 2: ").split())
    return [[k00, k01], [k10, k11]]

def main():
    while True:
        print("\n=== Hill Cipher 2x2 ===")
        print("1. Enkripsi")
        print("2. Dekripsi")
        print("3. Cari Kunci (Known Plaintext Attack)")
        print("4. Keluar")
        opsi = input("Pilih menu: ").strip()

        if opsi == '1':
            pt = input("Plaintext : ")
            k = input_key()
            ct = encrypt(pt, k)
            print("Ciphertext:", ct)

        elif opsi == '2':
            ct = input("Ciphertext: ")
            k = input_key()
            pt, err = decrypt(ct, k)
            if err:
                print(err)
            else:
                print("Plaintext :", pt)

        elif opsi == '3':
            pt = input("Plaintext sampel  : ")
            ct = input("Ciphertext sampel : ")
            k, err = find_key(pt, ct)
            if err:
                print(err)
            else:
                print("Kunci ditemukan:")
                print(f"| {k[0][0]:2d} {k[0][1]:2d} |")
                print(f"| {k[1][0]:2d} {k[1][1]:2d} |")

        elif opsi == '4':
            break
        else:
            print("Pilihan salah, coba lagi.")

if __name__ == "__main__":
    main()