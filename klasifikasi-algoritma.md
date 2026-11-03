# Algoritma Klasifikasi: Penjelasan, Perbedaan, Kelebihan–Kekurangan, dan Kapan Dipakai

> Catatan singkat sebelum mulai: tanda seperti **[R2 hlm. 53]** artinya poin tersebut diambil dari referensi nomor 2 di bagian Referensi, halaman 53. Poin tanpa tanda adalah konsep umum machine learning (bukan klaim khusus dari satu jurnal), jadi tetap dicek lagi ya kalau mau dipakai sebagai sitasi di tugas.

---

## 1. Klasifikasi itu apa sih?

Klasifikasi adalah teknik *supervised learning* di data mining: model belajar dari data yang **sudah punya label** (misalnya "puas / tidak puas", "diabetes / tidak"), lalu dipakai untuk menebak label data baru. Klasifikasi dipahami sebagai cara mengelompokkan objek berdasarkan ciri-ciri yang dimilikinya **[R1 hlm. 550]**.

Karena ada banyak algoritma dan masing-masing punya kelebihan serta kelemahan, pemilihannya tidak boleh asal. Pemilihan model yang kurang sesuai bisa membuat performa rendah atau interpretasi menyesatkan **[R2 hlm. 52]**.

---

## 2. Penjelasan Tiap Algoritma

### A. Decision Tree (Pohon Keputusan, misalnya ID3 / C4.5 / CART)

**Cara kerja singkat:** data diubah menjadi pohon keputusan berisi aturan (*rule*). Tiap percabangan dipilih berdasarkan ukuran seperti *information gain* (ID3) atau *gain ratio* (C4.5) **[R1 hlm. 551–552]**. C4.5 lebih unggul dari ID3 karena bisa mengolah data numerik maupun diskrit **[R1 hlm. 552]**.

**Kelebihan**
- Aturannya mudah dipahami manusia, jadi gampang dijelaskan ke orang non-teknis **[R2 hlm. 53]**.
- Klasifikasinya cepat dan transparan **[R1 hlm. 555]**.
- Relatif mudah diimplementasikan dan jadi titik awal yang kuat **[R2 hlm. 53]**.

**Kekurangan**
- Berpotensi *overfitting*, sensitif terhadap perubahan data, dan kurang pas untuk hubungan non-linear yang sangat kompleks **[R2 hlm. 53]**.
- Pada satu studi diabetes, Decision Tree punya masalah overfitting dan kurang bagus di kelas minoritas **[R5 hlm. 54]**.

**Cocok dipakai kalau:** datamu terstruktur/tabular dan kamu butuh hasil yang bisa dijelaskan atau diaudit (misalnya evaluasi kebijakan, klasifikasi berbasis indikator) **[R2 hlm. 58]**.

---

### B. Random Forest

**Cara kerja singkat:** gabungan banyak Decision Tree yang hasilnya "dipilih bersama" (*voting*). Ide ini membuatnya biasanya lebih stabil daripada satu pohon saja.

**Kelebihan**
- Akurasinya konsisten tinggi di beberapa studi: 95,44% (kepuasan penumpang) mengalahkan Decision Tree 93,41% dan Naive Bayes 82,51% **[R3 hlm. 157]**; rata-rata akurasi 97,28% dan AUC 0,971 pada data diabetes, tertinggi di antara C4.5, Naive Bayes, dan KNN **[R4 hlm. 43]**.
- Umumnya lebih tahan overfitting dibanding satu pohon tunggal (konsep umum ensemble).

**Kekurangan**
- Interpretasinya tidak sejelas satu Decision Tree karena modelnya berisi banyak pohon (konsep umum).
- Lebih berat dihitung dan lebih besar ukuran modelnya dibanding model sederhana (konsep umum).

**Cocok dipakai kalau:** datamu tabular, jumlah fitur lumayan banyak, dan kamu mengejar akurasi tanpa terlalu butuh penjelasan aturan satu per satu. Sering dipakai sebagai kandidat utama pada data tabular **[R3 hlm. 157; R4 hlm. 43]**.

---

### C. Naive Bayes

**Cara kerja singkat:** memakai probabilitas (Teorema Bayes) dengan asumsi bahwa antar fitur saling independen.

**Kelebihan**
- Sederhana, efisien, dan sering dipakai sebagai *baseline* ringan **[R2 hlm. 53]**.
- Bisa sangat bagus di kasus tertentu, misalnya klasifikasi biner prediksi kerusakan mesin: Naive Bayes 97,90% vs Decision Tree 77% **[R2 hlm. 57]**.
- Pada data diabetes, nilai AUC-nya (0,953) stabil dan tinggi **[R4 hlm. 43]**.

**Kekurangan**
- Bekerja baik terutama kalau asumsi independensi fitur tidak terlalu melenceng **[R2 hlm. 53]**.
- Performa bisa turun saat kelas lebih banyak dan pola data lebih kompleks; pada kasus multikelas yang sama, Decision Tree kembali unggul **[R2 hlm. 57]**.
- Pada data kepuasan penumpang, akurasinya paling rendah (82,51%) **[R3 hlm. 157]**.

**Cocok dipakai kalau:** klasifikasi biner yang sederhana, butuh komputasi ringan, atau sebagai pembanding awal **[R2 hlm. 58]**. Cocok juga untuk data teks (konsep umum).

---

### D. K-Nearest Neighbor (KNN)

**Cara kerja singkat:** objek baru diberi label berdasarkan *k* tetangga terdekatnya di data latih. KNN termasuk *lazy learning* dan tidak punya proses training; datanya langsung dihitung jaraknya saat testing **[R1 hlm. 554]**. Kalau jumlah kelasnya 2, nilai k sebaiknya bilangan ganjil **[R1 hlm. 554]**.

**Kelebihan**
- Algoritmanya sederhana **[R1 hlm. 554]**.
- Dapat bekerja baik pada kelas multi modal **[R1 hlm. 555]**.

**Kekurangan**
- Proses komputasi lama, dan penggunaan atribut yang kurang tepat dapat memicu error **[R1 hlm. 555]**.
- Pada data besar, KNN sering berada di bawah Decision Tree (C4.5) **[R2 hlm. 58]**; pada data diabetes, akurasinya paling rendah (rata-rata 94,87%) di antara empat algoritma yang diuji **[R4 hlm. 43]**.
- Sensitif terhadap skala fitur, jadi biasanya perlu normalisasi (konsep umum).

**Cocok dipakai kalau:** datasetnya kecil sampai sedang, fiturnya sedikit dan sudah dinormalisasi, dan kamu butuh model yang cepat dicoba tanpa training.

---

### E. Support Vector Machine (SVM)

**Cara kerja singkat:** mencari *hyperplane* terbaik yang memisahkan dua kelas dengan margin maksimal. Untuk data non-linear dipakai *kernel trick* (linear, quadratic, RBF, polynomial) **[R1 hlm. 552, 555]**.

**Kelebihan**
- Bisa bekerja baik meski data training sedikit, dan tingkat akurasinya tinggi **[R1 hlm. 555]**.
- Kuat pada ruang fitur berdimensi tinggi **[R2 hlm. 53]**.
- Pada prediksi diabetes, SVM paling tinggi akurasinya (74,46%) dibanding Logistic Regression (73,59%) dan Decision Tree (70,56%) **[R5 hlm. 49]**.

**Kekurangan**
- Waktu pemrosesan bisa lama **[R1 hlm. 555]**.
- Parameter dan kernel perlu diatur (γ, d, r dikontrol pengguna untuk menambah akurasi) **[R1 hlm. 556]**.
- Modelnya lebih kompleks dibanding Logistic Regression atau Decision Tree, sehingga untuk kasus yang mengutamakan interpretasi, dua model itu tetap bisa dipilih **[R5 hlm. 54–55]**.

**Cocok dipakai kalau:** data berdimensi tinggi (misalnya teks dengan banyak fitur), data latih tidak terlalu besar, dan akurasi lebih penting daripada penjelasan **[R2 hlm. 53; R1 hlm. 555]**.

---

### F. Logistic Regression

**Cara kerja singkat:** model statistik yang menghitung peluang suatu data masuk ke kelas tertentu dari kombinasi linear fitur (konsep umum).

**Kelebihan**
- Lebih mudah diinterpretasikan dan sederhana **[R5 hlm. 49, 53–54]**.
- Cepat dilatih dan cocok jadi baseline (konsep umum).

**Kekurangan**
- Pada studi diabetes, *recall* kelas diabetes hanya 0,62, menunjukkan lemah menangkap kelas tersebut **[R5 hlm. 54]**.
- Asumsinya cenderung linear, jadi kurang kuat untuk pola yang sangat rumit (konsep umum).

**Cocok dipakai kalau:** kamu butuh model sederhana yang mudah dijelaskan, hubungan antar fitur dan target kira-kira linear, dan target biner (misalnya risiko penyakit ya/tidak) **[R5 hlm. 55]**.

---

### G. Neural Network / Deep Learning

**Cara kerja singkat:** jaringan unit (neuron) berbobot yang meniru sistem saraf. Ada banyak jenis, misalnya backpropagation, self-organizing map, dan learning vector quantization **[R1 hlm. 553]**.

**Kelebihan**
- Akurasi tinggi, dan lebih unggul pada data tidak terstruktur (citra, teks) serta pola non-linear kompleks **[R1 hlm. 555; R2 hlm. 53]**. Contoh: klasifikasi stroke dari CT Scan 96,78% dan analisis sentimen GRU/LSTM hingga 98% **[R2 hlm. 57]**.

**Kekurangan**
- Butuh data latih banyak, konvergensi lambat, dan solusi optimalnya bisa hanya bersifat lokal **[R1 hlm. 555]**.
- Interpretabilitas rendah dan kebutuhan komputasi tinggi **[R2 hlm. 53]**.

**Cocok dipakai kalau:** datamu tidak terstruktur (gambar/teks/suara) atau polanya sangat kompleks, dan kamu punya data besar serta sumber daya komputasi cukup **[R2 hlm. 58]**.

---

## 3. Tabel Ringkasan Perbandingan

| Algoritma | Kelebihan utama | Kekurangan utama | Cocok untuk data | Mudah dijelaskan? |
|---|---|---|---|---|
| Decision Tree | Aturan jelas, cepat | Rawan overfitting | Tabular, butuh transparansi | Sangat |
| Random Forest | Akurasi tinggi, stabil | Lebih berat, kurang transparan | Tabular, fitur banyak | Sedang |
| Naive Bayes | Ringan, baseline kuat | Asumsi independensi | Biner sederhana, teks | Cukup |
| KNN | Sederhana, tanpa training | Lambat saat prediksi, sensitif skala | Data kecil, fitur sedikit | Cukup |
| SVM | Bagus di dimensi tinggi, data sedikit | Waktu proses lama, tuning kernel | Dimensi tinggi, teks | Kurang |
| Logistic Regression | Sederhana, mudah ditafsir | Lemah di pola non-linear/kelas minoritas | Biner, hubungan linear | Sangat |
| Neural Network / DL | Akurasi tinggi di data kompleks | Butuh data & komputasi besar | Citra, teks, pola kompleks | Sulit |

---

## 4. Panduan Cepat: Kapan Pakai yang Mana?

1. **Butuh hasil yang bisa dijelaskan ke dosen/klien/auditor?** → Decision Tree atau Logistic Regression.
2. **Data tabular dan mengejar akurasi?** → Random Forest (bandingkan juga dengan Decision Tree).
3. **Mau baseline cepat dan ringan?** → Naive Bayes (atau Logistic Regression).
4. **Data teks atau fitur sangat banyak?** → SVM, atau Naive Bayes sebagai pembanding.
5. **Dataset kecil dan fitur sedikit?** → KNN boleh dicoba, jangan lupa normalisasi.
6. **Data gambar/teks panjang/suara dan data besar?** → Neural Network / Deep Learning.

Intinya, **tidak ada satu algoritma yang selalu paling bagus di semua kondisi**, jadi pemilihan harus mempertimbangkan jenis data, kompleksitas masalah, kebutuhan interpretabilitas, dan sumber daya komputasi **[R2 hlm. 52, 58]**.

---

## 5. Bukti dari Beberapa Jurnal (2022–2026)

| Studi (data) | Hasil | Sumber |
|---|---|---|
| Kepuasan penumpang (129.880 baris) | RF 95,44% > DT 93,41% > NB 82,51% | R3 hlm. 157 |
| Diabetes (10.000 rekod, kelas tidak seimbang) | RF 97,28% (AUC 0,971), C4.5 97,22% (AUC 0,835), NB 95,59%, KNN 94,87% | R4 hlm. 43 |
| Prediksi diabetes (Kaggle) | SVM 74,46% > LR 73,59% > DT 70,56% | R5 hlm. 49 |
| SLR 2019–2025 | DT unggul di data terstruktur, NN/DL di data tidak terstruktur | R2 hlm. 56 |

Catatan menarik dari R4: pada data diabetes yang kelasnya tidak seimbang (859 positif vs 9.141 negatif), akurasi C4.5 dan Random Forest hampir sama, tetapi AUC Random Forest (0,971) jauh lebih tinggi daripada C4.5 (0,835). Jadi jangan hanya melihat akurasi, cek juga AUC, presisi, recall, dan F1.

---

## 6. Catatan Penting Biar Tidak Salah Kaprah

- Angka akurasi di atas hanya berlaku untuk dataset dan pengaturan masing-masing penelitian; hasil di datamu bisa berbeda.
- Beberapa penelitian hanya memakai akurasi sebagai metrik, dan penulisnya sendiri menyarankan metrik tambahan **[R3 hlm. 158]**.
- Tabel kelebihan–kekurangan di R1 (2022) merangkum temuan dari literatur yang lebih lama, jadi anggap sebagai gambaran umum, bukan hasil eksperimen baru.
- Selalu coba beberapa algoritma dengan *cross-validation* lalu bandingkan, jangan hanya mengandalkan satu pembagian data.

---

## 7. Referensi (2022–2026, akses publik)

**[R1]** Ramadhani, N. A., & Rosyid, H. A. (2022). *Algoritma-Algoritma Data Mining untuk Klasifikasi Data*. Jurnal Inovasi Teknik dan Edukasi Teknologi, 2(12), 550–556. Universitas Negeri Malang.
- Kutipan (hlm. 555, tabel perbandingan, SVM): "Mampu bekerja dengan baik meskipun dengan sedikit data training"
- Halaman yang dirujuk: 550, 551–556
- Link: https://journal3.um.ac.id/index.php/ft/article/view/3637
- PDF: https://journal3.um.ac.id/index.php/ft/article/download/3637/2387/7509

**[R2]** Syahputra, F., Sabrina, E., Tarigan, F. S. B., Sarumaha, M. I., Rahmadhani, A., Simanjorang, S. C., & Gorat, L. M. B. (2025). *Tinjauan Literatur Sistematis (2019–2025) Kinerja Decision Tree dan Neural Network (Deep Learning) serta Perbandingannya dengan Naive Bayes dan SVM*. TRILOGI, 6(4), 51–59. DOI: 10.33650/trilogi.v6i4.13429
- Kutipan (hlm. 58, Kesimpulan): "tidak ada satu algoritma yang selalu superior pada semua kondisi"
- Halaman yang dirujuk: 52, 53, 56, 57, 58
- Link: https://ejournal.unuja.ac.id/index.php/trilogi/article/view/13429
- PDF: https://ejournal.unuja.ac.id/index.php/trilogi/article/download/13429/pdf

**[R3]** Rahmat, W. A., Ladjamuddin, S. M., & Awaludin, D. T. (2023). *Perbandingan Algoritma Decision Tree, Random Forest dan Naive Bayes pada Prediksi Penilaian Kepuasan Penumpang Maskapai Pesawat Menggunakan Dataset Kaggle*. Jurnal Rekayasa Informasi, 12(2), 150–159. Institut Sains dan Teknologi Nasional.
- Kutipan (hlm. 157, Kesimpulan): "pada studi kasus serupa lebih disarankan menggunakan algoritma random forest"
- Halaman yang dirujuk: 157, 158
- Link: https://journal.istn.ac.id/index.php/rekayasainformasi/article/view/1726
- PDF: https://ejournal.istn.ac.id/index.php/rekayasainformasi/article/download/1726/1133

**[R4]** Fadillah, M. A., Mulyani, E. D. S., & Ruuhwan. (2024). *Komparasi Algoritma C4.5, Naive Bayes, K-Nearest Neighbor, Random Forest untuk Prediksi Faktor Penyebab Penyakit Diabetes*. Indonesian Journal of Digital Business, 4(1), 37–46. Universitas Perjuangan Tasikmalaya.
- Kutipan (hlm. 45, Kesimpulan): "kinerja algoritma C4.5 dan Random Forest hampir sama bagusnya"
- Halaman yang dirujuk: 42, 43, 45
- Link: https://ejournal.upi.edu/index.php/IJDB/article/view/68999
- PDF: https://ejournal.upi.edu/index.php/IJDB/article/download/68999/pdf

**[R5]** Mandias, G. F., & Manoppo, I. J. (2025). *Analisis Komparatif Algoritma Klasifikasi untuk Prediksi Diabetes Menggunakan Pembelajaran Mesin*. Jurnal Ilmiah MATRIK, 27(1), 49–55. Universitas Klabat.
- Kutipan (hlm. 54, hasil Decision Tree): "Overfitting juga menjadi masalah utama pada model ini"
- Halaman yang dirujuk: 49, 53, 54, 55
- PDF: https://journal.binadarma.ac.id/index.php/jurnalmatrik/article/download/3566/1537/11441

### Bacaan tambahan (belum dikutip per halaman)

**[R6]** Pangestu, P. (2024). *Systematic Literature Review: Perbandingan Algoritma Klasifikasi*. Jurnal Inovtek Polbeng – Seri Informatika, 8(2), 431–440. Kajian 500 artikel (2019–2023) tentang Naive Bayes, Decision Tree, Neural Network, Random Forest, dan SVM. Menurut abstraknya, untuk prediksi Random Forest paling sering dipakai (rata-rata akurasi 91,18%), sedangkan untuk klasifikasi yang paling sering dipakai adalah SVM (rata-rata akurasi 88,85%). *Catatan: saya hanya membaca abstraknya, jadi belum ada kutipan halaman.*
- Link: https://repository.uin-suska.ac.id/77242/

**[R7]** Pratama, B. A., dkk. (2026). *Klasifikasi Data Mining: Konsep, Metode, dan Implementasi*. Universitas Medan Area Press. Buku ini punya bab khusus Decision Tree, Random Forest dan Naive Bayes, KNN, SVM, Logistic Regression, hingga Neural Network. Menurut daftar isinya, bagian kelebihan dan kekurangan ada di antaranya pada hlm. 64 (RF vs NB), hlm. 92–93 (KNN), dan hlm. 105–106 (SVM). *Catatan: yang berhasil saya baca hanya halaman depan dan daftar isi, bukan isi babnya, jadi nomor halaman di atas dari daftar isi dan belum saya verifikasi ke teksnya.*
- PDF: https://phki-pghc.uma.ac.id/wp-content/uploads/2026/05/WEB.pdf
