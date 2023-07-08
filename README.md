# Gomoku Bot Competition
Made by Dimas Faidh Muzaki

## Latar Belakang
Masih ingatkah kalian dengan tugas besar 1 stima kalian ? Kalian diminta membuat bot untuk memenangkan sebuah game kapal perang. Tujuan dari task ini adalah sama, yaitu membuat bot dengan menggunakan algoritma greedy. Tapi pada kali ini, game yang berusaha dimenangkan adalah Gomoku atau sering disebut five in a row. Berbeda dengan task lainnya, task ini akan membandingkan hasil kerja kalian dengan teman seleksi lainnya dalam sebuah kompetisi. Jadi distribusi skor akan berdasarkan pemenang dari kompetisi. Maka kalian harus bisa membuat bot seoptimal mungkin. Good Luck Have Fun!

## Spesifikasi
* Pada task ini kalian akan membuat sebuah Bot Gomoku memanfaatkan algoritma Greedy
* Bot dibuat dengan mengoverwrite kelas Bot13521xxx di dalam `bots/Bot13521xxx.py`. Silakan ubah nilai xxx dengan NIM kalian. Selain itu, ubah nilai atribut NIM menjadi NIM kalian
* Pastikan method-method lain selain get_input tidak berubah di dalam submisi kalian.
* Kalian dipersilahkan untuk membuat method lain untuk membantu penentuan aksi.
* Silakan modifikasi method get_input sesuai strategi kalian. Pastikan keluarannya adalah sebuah string "x,y" yang menggambarkan koordinat board untuk menaruh pion
* Berikut spesifikasi dari game Connect Four yang akan digunakan:
  1. Ukurang board adalah 8x8
  2. Thinking time dari bot maksimal 3 detik. Setelah timeout, bot akan dianggap kalah
* **Dilarang** Mengcopas algoritma dari internet ataupun teman seleksi lainnya. 
* **Dilarang** Mengimplementasikan algoritma selain metode Greedy
* Peserta yang melanggar aturan diatas akan diskualifikasi dari kompetisi dan tidak dapat mendapatkan skor.

## Teknis Kompetisi
* Kompetisi dimulai ketika submisi pertama dilakukan
* Kompetisi ini akan berlangsung selama keberjalanan seleksi asisten IRK
* Pemenang dari kompetisi akan ditentukan dari peserta yang berhasil mengumpulkan poin terbanyak di akhir kompetisi (**berbeda dengan poin seleksi**)
* Peserta dapat mengumpulkan poin berdasarkan **peringkat** dari memenangkan **daily tournament** yang akan diadakan 5 kali dalam seminggu (pukul 12:00 WIB), pada hari kerja. 
* **Daily tournament** menggunakan format round-robin tournament. Dengan begitu, semua bot submisi akan saling bertanding satu kali.
* Pertandingan di dalam turnamen menggunakan scoring 3-1-0, bot yang menang akan mendapat 3 poin, bot yang kalah tidak mendapat poin, dan pertandingan seri akan memberikan poin 1 kepada kedua bot.
* Hasil peringkat pada tiap turnamen akan menentukan perolehan poin peserta dalam kompetisi ini.
* Poin kompetisi dilihat dari peringkat dan jumlah bot yang berpartisipasi dalam turnamen. Peringkat pertama akan mendapatkan n poin kompetisi, dengan n adalah jumlah partisipan. Peringkat selanjutnya mendapat poin kompetisi sebesar n-1.
* Bila terdapat kesamaan pada poin turnamen maka mereka yang berpoin turnamen sama akan mendapat poin kompetisi tertinggi yang mungkin.

* Anda bingung? Ini adalah contoh standings.
#### Tournament Scoreboard
<img width="536" alt="image" src="https://github.com/maspaitujaki/Gomoku_IRK/assets/72780615/81167e02-ef04-4654-a86b-d268b439e011">


#### Competition Scoreboard
<img width="152" alt="image" src="https://github.com/maspaitujaki/Gomoku_IRK/assets/72780615/879d43e3-3359-46e5-9e79-def5a242f849">

*p.s. Lebih baik ikut berkompetisi sesegera mungkin untuk mengumpulkan poin kompetisi.

* Scoreboard kompetisi dan informasi **Daily tournament** dapat dilihat pada [sheet berikut](https://docs.google.com/spreadsheets/d/1V9XLoJRv9-RWinbQc4vUVj_JZrRCCer-ouFLebEB4tU/edit#gid=0)
* Berikut distribusi skor pada pemenang kompetisi setelah kompetisi berakhir:

| Posisi | Poin Seleksi |
| ----------- | ----------- |
| 1   | 2300 |
| 2   | 2185 |
| 3   | 2070 |
| 4   | 1955 |
| 5 - dst   | 1840 |

## Pengerjaan & Pengumpulan Bot
1. Clone repository ini pada sebuah repository private pada github Anda dan invite `maspaitujaki` ke dalam repository tersebut.
2. Memberikan tag `vn` pada commit terakhir Anda setiap kali ingin melakukan submisi bot dengan n adalah urutan submisi keberapa. (contoh: `v1` untuk submisi pertama)
3. Lalu buat release untuk tag terbaru dengan release title bebas asal mencerminkan versi bot
4. Submisi bot pada website (dengan memasukkan link release) dan lakukan konfirmkasi ke LINE @oohmasdim.
5. Setiap kali membuat release baru, mohon konfirmasi ulang ke LINE @oohmasdim.
6. Setiap peserta maksimal hanya dapat melakukan submisi bot sebanyak 5x, jadi pastikan bot yang dikumpulkan tidak ada error atau bug.
7. Peserta yang mengumpulkan bot setelah jam 12.00 WIB siang tidak dapat mengikuti **Daily tournament** hari tersebut.
8. Jika ada pertanyaan silahkan buat issues di [repository original](https://github.com/maspaitujaki/Gomoku_IRK)

## Credit
Original game by [junxiaosong](https://github.com/junxiaosong/AlphaZero_Gomoku)

Thanks to Kak Jonathan CJ IRK'19
