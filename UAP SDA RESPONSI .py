import csv

class Buku:
    def __init__(self, id, judul, pengarang, deskripsi, harga_per_hari):
        self.id = id
        self.judul = judul
        self.pengarang = pengarang
        self.deskripsi = deskripsi
        self.harga_per_hari = harga_per_hari

    def __str__(self):
        return f"{self.judul} oleh {self.pengarang}"

class PeminjamanBuku:
    def __init__(self):
        self.buku = []
        self.antrian = []
        self.pemesanan = []
        self.transaksi = []

    def tambah_buku(self, id, judul, pengarang, deskripsi, harga_per_hari):
        buku_baru = Buku(id, judul, pengarang, deskripsi, harga_per_hari)
        self.buku.append(buku_baru)
        print("Buku berhasil ditambahkan.")

    def simpan_buku_ke_csv(self, filename="buku.csv"):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Judul", "Pengarang", "Deskripsi", "Harga Per Hari"])
            for buku in self.buku:
                writer.writerow([buku.id, buku.judul, buku.pengarang, buku.deskripsi, buku.harga_per_hari])
        print(f"Data buku berhasil disimpan ke {filename}")

    def muat_buku_dari_csv(self, filename="buku.csv"):
        try:
            with open(filename, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    id, judul, pengarang, deskripsi, harga_per_hari = row
                    self.tambah_buku(int(id), judul, pengarang, deskripsi, float(harga_per_hari))
            print(f"Data buku berhasil dimuat dari {filename}")
        except FileNotFoundError:
            print(f"File {filename} tidak ditemukan.")

    def tampilkan_buku(self):
        if not self.buku:
            print("Tidak ada buku yang tersedia.")
            return
        print(f"{'ID':<5} {'Judul':<30} {'Pengarang':<20} {'Harga Per Hari':<15}")
        print("="*70)
        for buku in self.buku:
            print(f"{buku.id:<5} {buku.judul:<30} {buku.pengarang:<20} Rp{buku.harga_per_hari:<15.2f}")

    def pesan_buku(self, id_buku, durasi_peminjaman):
        buku = self.cari_buku_berdasarkan_id(id_buku)
        if buku:
            total_harga = buku.harga_per_hari * durasi_peminjaman
            pesanan = f"Pemesanan: {buku}, Durasi: {durasi_peminjaman} hari, Total Harga: Rp{total_harga:.2f}"
            self.antrian.append((buku, durasi_peminjaman, total_harga))
            self.pemesanan.append(pesanan)
            print(pesanan)
        else:
            print("Buku tidak ditemukan.")

    def proses_pemesanan(self):
        if self.antrian:
            buku, durasi_peminjaman, total_harga = self.antrian.pop(0)
            transaksi = f"Transaksi: {buku}, Durasi: {durasi_peminjaman} hari, Total Harga: Rp{total_harga:.2f}"
            self.transaksi.append(transaksi)
            print(transaksi)
        else:
            print("Tidak ada pemesanan dalam antrian.")

    def tampilkan_transaksi(self):
        if not self.transaksi:
            print("Tidak ada transaksi yang tersedia.")
        for transaksi in self.transaksi:
            print(transaksi)

    def tampilkan_pemesanan(self):
        if not self.pemesanan:
            print("Tidak ada pemesanan yang tersedia.")
        for pesanan in self.pemesanan:
            print(pesanan)

    def cari_buku_berdasarkan_id(self, id):
        for buku in self.buku:
            if buku.id == id:
                return buku
        return None

def utama():
    peminjaman = PeminjamanBuku()
    while True:
        print("\nSistem Peminjaman Buku:")
        print("1. Tambah Buku")
        print("2. Tampilkan Buku")
        print("3. Pesan Buku")
        print("4. Proses Pemesanan")
        print("5. Lihat Transaksi")
        print("6. Lihat Pemesanan")
        print("7. Simpan Buku ke CSV")
        print("8. Muat Buku dari CSV")
        print("9. Keluar")

        pilihan = input("Masukkan pilihan Anda: ")
        if pilihan == '1':
            try:
                id = int(input("Masukkan ID Buku: "))
                judul = input("Masukkan Judul Buku: ")
                pengarang = input("Masukkan Pengarang Buku: ")
                deskripsi = input("Masukkan Deskripsi Buku: ")
                harga_per_hari = float(input("Masukkan Harga Peminjaman Per Hari: "))
                peminjaman.tambah_buku(id, judul, pengarang, deskripsi, harga_per_hari)
            except ValueError:
                print("Input tidak valid. Harap masukkan tipe data yang benar.")
        elif pilihan == '2':
            peminjaman.tampilkan_buku()
        elif pilihan == '3':
            try:
                id_buku = int(input("Masukkan ID Buku untuk pemesanan: "))
                durasi_peminjaman = int(input("Masukkan Durasi Peminjaman (hari): "))
                peminjaman.pesan_buku(id_buku, durasi_peminjaman)
            except ValueError:
                print("Input tidak valid. Harap masukkan tipe data yang benar.")
        elif pilihan == '4':
            peminjaman.proses_pemesanan()
        elif pilihan == '5':
            peminjaman.tampilkan_transaksi()
        elif pilihan == '6':
            peminjaman.tampilkan_pemesanan()
        elif pilihan == '7':
            peminjaman.simpan_buku_ke_csv()
        elif pilihan == '8':
            peminjaman.muat_buku_dari_csv()
        elif pilihan == '9':
            break
        else:
            print("Pilihan tidak valid. Harap coba lagi.")
        input("\nTekan Enter untuk melanjutkan...")

if __name__ == "__main__":
    utama()
