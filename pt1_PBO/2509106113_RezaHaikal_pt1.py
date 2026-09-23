# ==================================================
# CLASS 1 : SEPATU
# Mengelola data produk sepatu beserta stoknya.
# ==================================================
class Sepatu:

    # ATRIBUT KELAS
    nama_toko = "Toko Sepatu Otep"
    total_produk = 0
    diskon_member = 0.10

    def __init__(self, nama_sepatu, merek, ukuran, harga, stok):
        self.nama_sepatu = nama_sepatu
        self.merek = merek
        self.ukuran = ukuran
        self.harga = harga

        self.__stok = stok      # data sensitif, tidak boleh diubah sembarangan

        Sepatu.total_produk += 1    # setiap objek baru menambah atribut kelas

    # PROPERTY: GETTER & SETTER
    @property
    def stok(self):
        """Getter untuk mengambil nilai stok (private)."""
        return self.__stok

    @stok.setter
    def stok(self, nilai_baru):
        """Setter untuk mengubah stok dengan validasi tidak boleh negatif."""
        if nilai_baru < 0:
            raise ValueError("Stok tidak boleh bernilai negatif!")
        self.__stok = nilai_baru

    # INSTANCE METHOD
    def tambah_stok(self, jumlah):
        """Menambah stok sepatu (misalnya karena restock dari supplier)."""
        if jumlah <= 0:
            print("Jumlah tambah stok harus lebih dari 0.")
            return
        self.stok = self.stok + jumlah      # lewat setter agar tervalidasi
        print(f"Stok '{self.nama_sepatu}' bertambah {jumlah}. Stok sekarang: {self.stok}")

    def kurangi_stok(self, jumlah):
        """Mengurangi stok, dipakai saat terjadi transaksi penjualan."""
        if jumlah > self.__stok:
            print(f"Stok '{self.nama_sepatu}' tidak cukup! Sisa stok: {self.__stok}")
            return False
        self.__stok -= jumlah
        return True

    def tampilkan_info(self):
        """Menampilkan informasi lengkap produk sepatu."""
        print(f"[{self.merek}] {self.nama_sepatu} | Ukuran: {self.ukuran} "
              f"| Harga: Rp{self.harga:,} | Stok: {self.__stok}")

    # CLASS METHOD
    @classmethod
    def dari_dict(cls, data):
        """Factory method: membuat objek Sepatu dari data berbentuk dictionary."""
        return cls(data["nama_sepatu"], data["merek"], data["ukuran"],
                    data["harga"], data["stok"])

    @classmethod
    def ubah_diskon_member(cls, diskon_baru):
        """Mengubah atribut kelas diskon_member, berlaku untuk semua objek Sepatu."""
        if 0 <= diskon_baru <= 1:
            cls.diskon_member = diskon_baru
            print(f"Diskon member berhasil diubah menjadi {cls.diskon_member * 100:.0f}%")
        else:
            print("Nilai diskon tidak valid (harus antara 0 - 1).")

    # STATIC METHOD
    @staticmethod
    def validasi_ukuran(ukuran):
        """Fungsi bantu (tidak butuh self/cls) untuk memvalidasi ukuran sepatu."""
        return isinstance(ukuran, (int, float)) and 30 <= ukuran <= 46


# =========================================
# CLASS 2 : KARYAWAN
# Mengelola data karyawan/kasir toko.
# =========================================
class Karyawan:

    # ATRIBUT KELAS
    nama_perusahaan = "Toko Sepatu Otep"
    total_karyawan = 0
    jam_kerja_standar = 8    # jam per hari

    def __init__(self, nama, jabatan, gaji):
        self.nama = nama
        self.jabatan = jabatan

        self.__gaji = gaji   # data sensitif

        Karyawan.total_karyawan += 1

    # PROPERTY: GETTER & SETTER
    @property
    def gaji(self):
        """Getter untuk mengambil nilai gaji (private)."""
        return self.__gaji

    @gaji.setter
    def gaji(self, nilai_baru):
        """Setter untuk mengubah gaji dengan validasi tidak boleh negatif."""
        if nilai_baru < 0:
            raise ValueError("Gaji tidak boleh bernilai negatif!")
        self.__gaji = nilai_baru

    # INSTANCE METHOD
    def tampilkan_profil(self):
        """Menampilkan profil karyawan."""
        print(f"Nama: {self.nama} | Jabatan: {self.jabatan} | "
              f"Perusahaan: {Karyawan.nama_perusahaan}")

    def naikkan_gaji(self, persen):
        """Menaikkan gaji karyawan berdasarkan persentase tertentu."""
        if persen <= 0:
            print("Persentase kenaikan harus lebih dari 0.")
            return
        gaji_baru = self.__gaji + (self.__gaji * persen / 100)
        self.gaji = gaji_baru    # lewat setter agar tervalidasi
        print(f"Gaji {self.nama} naik {persen}% menjadi Rp{self.gaji:,.0f}")

    # CLASS METHOD
    @classmethod
    def dari_dict(cls, data):
        """Factory method: membuat objek Karyawan dari data dictionary."""
        return cls(data["nama"], data["jabatan"], data["gaji"])

    @classmethod
    def ubah_jam_kerja(cls, jam_baru):
        """Mengubah atribut kelas jam_kerja_standar, berlaku untuk semua karyawan."""
        cls.jam_kerja_standar = jam_baru
        print(f"Jam kerja standar diubah menjadi {jam_baru} jam/hari")

    # STATIC METHOD
    @staticmethod
    def validasi_nama(nama):
        """Fungsi bantu untuk memvalidasi nama karyawan tidak boleh kosong."""
        return isinstance(nama, str) and len(nama.strip()) > 0


# =====================================================================
# CLASS 3 : TRANSAKSI
# Menghubungkan objek Sepatu dan Karyawan untuk memproses penjualan.
# =====================================================================
class Transaksi:

    # ATRIBUT KELAS
    nama_toko = "Toko Sepatu Otep"
    total_transaksi = 0
    pajak = 0.11

    def __init__(self, id_transaksi, sepatu, karyawan, jumlah_beli):
        # ATRIBUT INSTANCE
        self.id_transaksi = id_transaksi
        self.sepatu = sepatu          # objek dari class Sepatu
        self.karyawan = karyawan      # objek dari class Karyawan
        self.jumlah_beli = jumlah_beli

        self.__total_bayar = 0

        Transaksi.total_transaksi += 1

    # PROPERTY: GETTER & SETTER
    @property
    def total_bayar(self):
        """Getter untuk mengambil nilai total_bayar (private)."""
        return self.__total_bayar

    @total_bayar.setter
    def total_bayar(self, nilai):
        """Setter untuk total_bayar dengan validasi tidak boleh negatif."""
        if nilai < 0:
            raise ValueError("Total bayar tidak boleh bernilai negatif!")
        self.__total_bayar = nilai

    # INSTANCE METHOD
    def proses_transaksi(self, pakai_diskon_member=False):
        """Memproses transaksi: mengurangi stok sepatu & menghitung total bayar."""
        berhasil = self.sepatu.kurangi_stok(self.jumlah_beli)
        if not berhasil:
            print("Transaksi dibatalkan karena stok tidak mencukupi.\n")
            return

        subtotal = self.sepatu.harga * self.jumlah_beli
        if pakai_diskon_member:
            subtotal -= subtotal * Sepatu.diskon_member

        total = Transaksi.hitung_total_dengan_pajak(subtotal, Transaksi.pajak)
        self.total_bayar = total
        print(f"Transaksi {self.id_transaksi} berhasil diproses oleh {self.karyawan.nama}.\n")

    def tampilkan_struk(self):
        """Menampilkan struk hasil transaksi."""
        print("========== STRUK PEMBELIAN ==========")
        print(f"Toko        : {Transaksi.nama_toko}")
        print(f"ID Transaksi: {self.id_transaksi}")
        print(f"Kasir       : {self.karyawan.nama}")
        print(f"Produk      : {self.sepatu.nama_sepatu} ({self.sepatu.merek})")
        print(f"Jumlah      : {self.jumlah_beli}")
        print(f"Total Bayar : Rp{self.total_bayar:,.0f}")
        print("======================================\n")

    # CLASS METHOD
    @classmethod
    def dari_dict(cls, data):
        """Factory method: membuat objek Transaksi dari data dictionary."""
        return cls(data["id_transaksi"], data["sepatu"], data["karyawan"], data["jumlah_beli"])

    @classmethod
    def ubah_pajak(cls, pajak_baru):
        """Mengubah atribut kelas pajak, berlaku untuk semua transaksi berikutnya."""
        if 0 <= pajak_baru <= 1:
            cls.pajak = pajak_baru
            print(f"Pajak transaksi diubah menjadi {cls.pajak * 100:.0f}%")
        else:
            print("Nilai pajak tidak valid (harus antara 0 - 1).")

    # STATIC METHOD
    @staticmethod
    def hitung_total_dengan_pajak(subtotal, pajak):
        """Fungsi bantu menghitung total bayar setelah ditambah pajak."""
        return subtotal + (subtotal * pajak)


# ==================================
# MAIN PROGRAM - PENGUJIAN
# ==================================
if __name__ == "__main__":
    print("=" * 71)
    print("  SELAMAT DATANG DI SISTEM PENGELOLAAN PENJUALAN DAN STOK TOKO SEPATU")
    print("=" * 71, "\n")

    # 1. Membuat objek Sepatu
    print("--- 1. Membuat Objek Sepatu ---")
    sepatu1 = Sepatu("Air Runner", "Nike", 42, 850000, 20)
    sepatu2 = Sepatu.dari_dict({
        "nama_sepatu": "UltraBoost", "merek": "Adidas",
        "ukuran": 40, "harga": 1200000, "stok": 15
    })
    sepatu1.tampilkan_info()
    sepatu2.tampilkan_info()
    print(f"Total produk terdaftar (atribut kelas): {Sepatu.total_produk}\n")

    # 2. Membuat objek Karyawan
    print("--- 2. Membuat Objek Karyawan ---")
    karyawan1 = Karyawan("Dimas", "Kasir", 3500000)
    karyawan2 = Karyawan.dari_dict({
        "nama": "Rina", "jabatan": "Supervisor", "gaji": 5000000
    })
    karyawan1.tampilkan_profil()
    karyawan2.tampilkan_profil()
    print(f"Total karyawan terdaftar (atribut kelas): {Karyawan.total_karyawan}\n")

    # 3. Uji instance method
    print("--- 3. Uji Instance Method ---")
    sepatu1.tambah_stok(5)
    karyawan1.naikkan_gaji(10)
    print()

    # 4. Uji static method
    print("--- 4. Uji Static Method ---")
    print("Validasi ukuran 42        :", Sepatu.validasi_ukuran(42))
    print("Validasi ukuran 60        :", Sepatu.validasi_ukuran(60))
    print("Validasi nama 'Dimas'     :", Karyawan.validasi_nama("Dimas"))
    print("Validasi nama '' (kosong) :", Karyawan.validasi_nama(""))
    print()

    # 5. Uji class method
    print("--- 5. Uji Class Method ---")
    Sepatu.ubah_diskon_member(0.15)
    Karyawan.ubah_jam_kerja(9)
    print()

    # 6. Membuat & memproses objek Transaksi
    print("--- 6. Membuat & Memproses Transaksi ---")
    transaksi1 = Transaksi("TRX001", sepatu1, karyawan1, 2)
    transaksi1.proses_transaksi(pakai_diskon_member=True)
    transaksi1.tampilkan_struk()

    transaksi2 = Transaksi("TRX002", sepatu2, karyawan2, 3)
    transaksi2.proses_transaksi()
    transaksi2.tampilkan_struk()

    print(f"Total transaksi tercatat (atribut kelas): {Transaksi.total_transaksi}\n")

    # 7. Uji property setter: DATA VALID & TIDAK VALID
    print("--- 7. Uji Setter & Validasi Data ---")

    print("Stok sepatu2 sebelum diubah :", sepatu2.stok)
    sepatu2.stok = 50                       # valid
    print("Stok sepatu2 setelah diubah (valid) :", sepatu2.stok)
    try:
        sepatu2.stok = -10                  # tidak valid -> harus ditolak
    except ValueError as e:
        print("Gagal mengubah stok (tidak valid) :", e)

    print("\nGaji karyawan2 sebelum diubah :", karyawan2.gaji)
    karyawan2.gaji = 5500000                # valid

    print("Gaji karyawan2 setelah diubah (valid) :", karyawan2.gaji)
    try:
        karyawan2.gaji = -1000000           # tidak valid -> harus ditolak
    except ValueError as e:
        print("Gagal mengubah gaji (tidak valid) :", e)

    print("\nTotal bayar transaksi1 saat ini :", transaksi1.total_bayar)
    try:
        transaksi1.total_bayar = -500       # tidak valid -> harus ditolak
    except ValueError as e:
        print("Gagal mengubah total bayar (tidak valid) :", e)