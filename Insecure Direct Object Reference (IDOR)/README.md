# Insecure Direct Object Reference (IDOR)

https://img.shields.io/badge/OWASP-Broken%20Access%20Control-red
https://img.shields.io/badge/Web%20Security-IDOR-orange
https://img.shields.io/badge/License-Educational-blue

## 📖 Pengertian

**Insecure Direct Object Reference (IDOR)** adalah jenis kerentanan keamanan yang terjadi ketika aplikasi memberikan akses langsung ke suatu objek atau sumber daya berdasarkan input yang dikirim pengguna tanpa melakukan validasi otorisasi yang memadai.

Objek yang dimaksud dapat berupa:

- Data pengguna
- Dokumen
- File
- Rekam transaksi
- Pesanan
- Informasi profil
- Resource API

Kerentanan ini memungkinkan seorang pengguna mengakses data milik pengguna lain hanya dengan mengubah parameter tertentu, seperti:

```http
https://example.com/profile?id=1001
```

Menjadi:

```http
https://example.com/profile?id=1002
```

Jika aplikasi menampilkan data pengguna lain tanpa pemeriksaan izin, maka terjadi kerentanan IDOR.

---

## 🎯 Mengapa IDOR Berbahaya?

IDOR dapat menyebabkan:

- Kebocoran data sensitif
- Pengambilalihan akun (Account Takeover)
- Manipulasi data pengguna lain
- Penghapusan data tanpa izin
- Pelanggaran privasi
- Kerugian finansial

Karena alasan tersebut, IDOR termasuk dalam kategori **Broken Access Control**, yang secara konsisten menjadi salah satu risiko keamanan aplikasi web paling kritis.

---

## 🔍 Cara Kerja IDOR

Misalkan terdapat aplikasi dengan endpoint berikut:

```http
GET /api/orders/12345
```

Server mengambil data order berdasarkan ID yang dikirim pengguna.

Jika pengguna login sebagai:

```text
userA
```

lalu mengubah endpoint menjadi:

```http
GET /api/orders/12346
```

dan server tetap mengembalikan data milik pengguna lain tanpa verifikasi kepemilikan, maka terjadi IDOR.

---

## 📝 Contoh Sederhana

### Aplikasi Rentan

```php
<?php

$user_id = $_GET['id'];

$query = "SELECT * FROM users WHERE id = '$user_id'";
$result = mysqli_query($conn, $query);

echo $result;

?>
```

Masalah:

- Server hanya mengambil data berdasarkan parameter `id`
- Tidak memeriksa apakah data tersebut milik pengguna yang sedang login

---

### Contoh Eksploitasi

Request asli:

```http
GET /profile?id=10
```

Diubah menjadi:

```http
GET /profile?id=11
```

Respons:

```json
{
  "id": 11,
  "name": "Admin",
  "email": "admin@example.com"
}
```

Data berhasil diakses tanpa izin.

---

## ✅ Contoh Implementasi yang Benar

Server harus memverifikasi kepemilikan data.

Contoh:

```php
<?php

$current_user = $_SESSION['user_id'];
$requested_id = $_GET['id'];

$query = "
SELECT *
FROM users
WHERE id = '$requested_id'
AND id = '$current_user'
";

$result = mysqli_query($conn, $query);

?>
```

Atau lebih baik:

```php
<?php

$current_user = $_SESSION['user_id'];

$query = "
SELECT *
FROM users
WHERE id = '$current_user'
";

$result = mysqli_query($conn, $query);

?>
```

Server tidak lagi mempercayai input pengguna untuk menentukan objek yang boleh diakses.

---

## 🔎 Indikator IDOR Saat Pengujian

Beberapa parameter yang layak diperiksa:

### Numeric ID

```http
/user?id=123
```

### UUID

```http
/user?uid=7f48cdff-a9b4-42e0-a5be-a5cb4c0dd123
```

### File

```http
/download?file=invoice.pdf
```

### Order ID

```http
/order/1001
```

### API Resource

```http
/api/v1/users/100
```

### JSON Body

```json
{
  "userId": "100"
}
```

---

## 🧪 Metode Pengujian IDOR

### 1. Horizontal Privilege Escalation

Mengakses data milik pengguna lain dengan level hak akses yang sama.

Contoh:

```text
User A → Data User B
```

---

### 2. Vertical Privilege Escalation

Pengguna biasa memperoleh akses ke data administrator.

Contoh:

```text
User → Admin Panel
```

---

### 3. Forced Browsing

Mencoba mengakses resource secara langsung.

Contoh:

```http
/admin/report/123
```

---

### 4. Parameter Tampering

Mengubah:

```text
user_id
account_id
order_id
document_id
invoice_id
```

untuk melihat apakah aplikasi memeriksa otorisasi.

---

## 🛡️ Mitigasi

### 1. Terapkan Access Control

Setiap request harus diverifikasi:

```text
Apakah pengguna ini berhak mengakses objek tersebut?
```

---

### 2. Jangan Percaya Input Pengguna

Hindari:

```sql
SELECT * FROM users WHERE id = ?
```

yang menggunakan ID dari pengguna tanpa validasi kepemilikan.

---

### 3. Gunakan Referensi Tidak Langsung

Daripada:

```http
/user/123
```

gunakan token acak:

```http
/user/4e2df9a9b7d352bc
```

Catatan:

Menggunakan UUID saja **bukan mitigasi penuh** jika otorisasi tidak diperiksa.

---

### 4. Implementasikan RBAC

**Role Based Access Control**

Contoh role:

- User
- Moderator
- Admin
- Super Admin

Setiap role memiliki izin yang berbeda.

---

### 5. Log dan Monitoring

Pantau aktivitas seperti:

- Banyak request ke object berbeda
- Enumerasi ID berurutan
- Akses tidak biasa

---

### 6. Gunakan Principle of Least Privilege

Berikan hak akses seminimal mungkin.

---

## 🔥 Contoh Kasus Nyata

Skenario umum:

Sebuah aplikasi menyimpan invoice pada endpoint:

```http
https://example.com/invoice/1001
```

Pengguna dapat mengubah URL menjadi:

```http
https://example.com/invoice/1002
```

dan melihat invoice pengguna lain.

Akar masalah:

```text
Tidak ada validasi otorisasi pada server.
```

---

## ✅ Checklist Pencegahan IDOR

- [ ] Selalu lakukan pengecekan otorisasi di server
- [ ] Jangan bergantung pada hidden field
- [ ] Jangan bergantung pada JavaScript
- [ ] Jangan mempercayai parameter dari client
- [ ] Verifikasi kepemilikan objek
- [ ] Terapkan RBAC/ABAC
- [ ] Gunakan logging dan monitoring
- [ ] Lakukan security testing secara berkala

---

## 📚 Referensi

- OWASP Top 10
- OWASP Cheat Sheet Series
- OWASP Web Security Testing Guide (WSTG)
- PortSwigger Web Security Academy
- CWE-639: Authorization Bypass Through User-Controlled Key

---

## ⚠️ Disclaimer

Dokumen ini disediakan **hanya untuk tujuan edukasi, pembelajaran, dan peningkatan keamanan aplikasi**.

Segala contoh yang diberikan bertujuan untuk membantu pengembang, security researcher, dan penetration tester memahami cara kerja kerentanan IDOR agar dapat melakukan mitigasi yang tepat.

Jangan melakukan pengujian terhadap sistem, aplikasi, atau layanan tanpa izin tertulis dari pemilik yang sah. Segala tindakan yang melanggar hukum atau kebijakan penggunaan merupakan tanggung jawab masing-masing individu.

---

## 🤝 Kontribusi

Kontribusi untuk memperbaiki dokumentasi ini sangat dipersilakan.

Langkah kontribusi:

1. Fork repository
2. Buat branch baru
3. Lakukan perubahan
4. Commit perubahan
5. Buat Pull Request

---

## ⭐ Dukungan

Jika repository ini bermanfaat:

- Berikan ⭐ Star
- Lakukan Fork
- Bagikan kepada komunitas keamanan aplikasi

Happy Learning & Secure Coding! 🔐
