# ==================================================
# CLASS : CATATAN STOK  (bagian dari komposisi)
# Objek ini hanya dibuat di dalam Sepatu.
# ==================================================
class CatatanStok:
    """Tidak punya arti mandiri tanpa Sepatu tempat perubahan stok terjadi."""

    def __init__(self, id_catatan, tipe, jumlah, keterangan):
        self.id_catatan = id_catatan
        self.tipe = tipe              # "MASUK" atau "KELUAR"
        self.jumlah = jumlah
        self.keterangan = keterangan

    def __str__(self):
        simbol = "+" if self.tipe == "MASUK" else "-"
        return (f"[{self.id_catatan}] {self.tipe:<6} {simbol}{self.jumlah} "
                f"| Ket: {self.keterangan}")


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

        self.__stok = stok          # data sensitif, tidak boleh diubah sembarangan
        self._riwayat_stok = []     # KOMPOSISI: berisi objek CatatanStok

        Sepatu.total_produk += 1

        if stok > 0:
            self._buat_catatan("MASUK", stok, "Stok awal produk")

    # KOMPOSISI: objek bagian dibuat langsung di dalam objek induk
    def _buat_catatan(self, tipe, jumlah, keterangan):
        id_baru = f"STK-{len(self._riwayat_stok) + 1:03d}"
        self._riwayat_stok.append(CatatanStok(id_baru, tipe, jumlah, keterangan))

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
        self._buat_catatan("MASUK", jumlah, "Restock dari supplier")
        print(f"Stok '{self.nama_sepatu}' bertambah {jumlah}. Stok sekarang: {self.stok}")

    def kurangi_stok(self, jumlah):
        """Mengurangi stok, dipakai saat terjadi transaksi penjualan."""
        if jumlah > self.__stok:
            print(f"Stok '{self.nama_sepatu}' tidak cukup! Sisa stok: {self.__stok}")
            return False
        self.__stok -= jumlah
        self._buat_catatan("KELUAR", jumlah, "Penjualan")
        return True

    def tampilkan_info(self):
        """Menampilkan informasi lengkap produk sepatu."""
        print(f"[{self.merek}] {self.nama_sepatu} | Ukuran: {self.ukuran} "
              f"| Harga: Rp{self.harga:,} | Stok: {self.__stok}")

    def cetak_riwayat_stok(self):
        """Menampilkan seluruh CatatanStok milik sepatu ini."""
        print(f"Riwayat stok {self.nama_sepatu}:")
        for catatan in self._riwayat_stok:
            print(f"  {catatan}")

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


# ==================================================================
# CLASS 2 : KARYAWAN  (SUPERCLASS)
# Atribut & method umum yang dimiliki SEMUA jenis karyawan.
#   - _gaji   : PROTECTED -> dipakai langsung oleh subclass
#   - __pin   : PRIVATE   -> rahasia, hanya untuk Karyawan
# ==================================================================
class Karyawan:

    # ATRIBUT KELAS
    nama_perusahaan = "Toko Sepatu Otep"
    total_karyawan = 0
    jam_kerja_standar = 8    # jam per hari

    def __init__(self, nama, jabatan, gaji, pin="0000"):
        self.nama = nama
        self.jabatan = jabatan

        self._gaji = gaji       # protected: boleh diakses subclass
        self.__pin = pin        # private: eksklusif milik Karyawan

        Karyawan.total_karyawan += 1

    # PROPERTY: GETTER & SETTER
    @property
    def gaji(self):
        """Getter untuk mengambil nilai gaji (protected)."""
        return self._gaji

    @gaji.setter
    def gaji(self, nilai_baru):
        """Setter untuk mengubah gaji dengan validasi tidak boleh negatif."""
        if nilai_baru < 0:
            raise ValueError("Gaji tidak boleh bernilai negatif!")
        self._gaji = nilai_baru

    # INSTANCE METHOD
    def verifikasi_pin(self, pin_input):
        """Satu-satunya cara memeriksa PIN (data private tidak dibuka keluar)."""
        return pin_input == self.__pin

    def tampilkan_profil(self):
        """Menampilkan profil karyawan."""
        print(f"Nama: {self.nama} | Jabatan: {self.jabatan} | "
              f"Perusahaan: {Karyawan.nama_perusahaan}")

    def hitung_gaji_bulanan(self):
        """Gaji yang diterima per bulan. Subclass boleh meng-override."""
        return self._gaji

    def naikkan_gaji(self, persen):
        """Menaikkan gaji karyawan berdasarkan persentase tertentu."""
        if persen <= 0:
            print("Persentase kenaikan harus lebih dari 0.")
            return
        gaji_baru = self._gaji + (self._gaji * persen / 100)
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


# ==================================================================
# CLASS 3 : KASIR  (SUBCLASS dari Karyawan)
# Atribut unik: shift, jumlah_transaksi
# ==================================================================
class Kasir(Karyawan):

    bonus_per_transaksi = 10000      # atribut kelas milik Kasir

    def __init__(self, nama, gaji, shift="Pagi", pin="0000"):
        super().__init__(nama, "Kasir", gaji, pin)     # panggil konstruktor superclass
        self.shift = shift                              # atribut spesifik Kasir
        self.jumlah_transaksi = 0                       # atribut spesifik Kasir

    def catat_transaksi(self):
        """Dipanggil setiap kali kasir menyelesaikan satu penjualan."""
        self.jumlah_transaksi += 1

    # ASOSIASI: objek Sepatu diterima sebagai parameter, tidak disimpan
    def cek_ketersediaan(self, sepatu, jumlah):
        """Kasir mengecek apakah stok sepatu cukup untuk jumlah yang diminta."""
        cukup = sepatu.stok >= jumlah
        status = "TERSEDIA" if cukup else "TIDAK CUKUP"
        print(f"Kasir {self.nama} mengecek '{sepatu.nama_sepatu}' "
              f"x{jumlah}: {status} (stok {sepatu.stok})")
        return cukup

    # METHOD OVERRIDING: ditambah info shift & jumlah transaksi
    def tampilkan_profil(self):
        super().tampilkan_profil()
        print(f"   -> Shift: {self.shift} | Transaksi ditangani: {self.jumlah_transaksi}")

    # METHOD OVERRIDING: gaji + bonus per transaksi (memakai _gaji protected)
    def hitung_gaji_bulanan(self):
        return self._gaji + (self.jumlah_transaksi * Kasir.bonus_per_transaksi)

    @classmethod
    def dari_dict(cls, data):
        """Override factory method karena konstruktor Kasir berbeda."""
        return cls(data["nama"], data["gaji"], data.get("shift", "Pagi"))


# ==================================================================
# CLASS 4 : SUPERVISOR  (SUBCLASS dari Karyawan)
# Atribut unik: divisi, tunjangan_jabatan
# ==================================================================
class Supervisor(Karyawan):

    def __init__(self, nama, gaji, divisi, tunjangan_jabatan, pin="0000"):
        super().__init__(nama, "Supervisor", gaji, pin)
        self.divisi = divisi                            # atribut spesifik Supervisor
        self.tunjangan_jabatan = tunjangan_jabatan      # atribut spesifik Supervisor

    # ASOSIASI: objek Sepatu diterima sebagai parameter
    def periksa_stok_rendah(self, sepatu, batas=10):
        """Supervisor memeriksa apakah stok sepatu sudah menipis."""
        if sepatu.stok < batas:
            print(f"Supervisor {self.nama}: stok '{sepatu.nama_sepatu}' menipis "
                  f"({sepatu.stok}), segera restock!")
        else:
            print(f"Supervisor {self.nama}: stok '{sepatu.nama_sepatu}' aman ({sepatu.stok}).")

    # METHOD OVERRIDING: ditambah info divisi
    def tampilkan_profil(self):
        super().tampilkan_profil()
        print(f"   -> Divisi: {self.divisi} | Tunjangan: Rp{self.tunjangan_jabatan:,}")

    # METHOD OVERRIDING: gaji + tunjangan jabatan
    def hitung_gaji_bulanan(self):
        return self._gaji + self.tunjangan_jabatan

    @classmethod
    def dari_dict(cls, data):
        """Override factory method karena konstruktor Supervisor berbeda."""
        return cls(data["nama"], data["gaji"], data["divisi"], data["tunjangan_jabatan"])


# ==================================================================
# CLASS 5 : TOKO SEPATU
# AGREGASI: menampung objek Sepatu & Karyawan yang dibuat di luar.
# Jika toko dihapus, sepatu dan karyawan tetap ada.
# ==================================================================
class TokoSepatu:

    def __init__(self, nama_toko, alamat):
        self.nama_toko = nama_toko
        self.alamat = alamat
        self._daftar_sepatu = []        # agregasi: referensi objek dari luar
        self._daftar_karyawan = []      # agregasi: referensi objek dari luar

    def tambah_sepatu(self, sepatu):
        if isinstance(sepatu, Sepatu):
            self._daftar_sepatu.append(sepatu)
            print(f"  [+] {sepatu.nama_sepatu} masuk katalog {self.nama_toko}")

    def tambah_karyawan(self, karyawan):
        # isinstance(..., Karyawan) juga True untuk Kasir & Supervisor
        if isinstance(karyawan, Karyawan):
            self._daftar_karyawan.append(karyawan)
            print(f"  [+] {karyawan.nama} ({karyawan.jabatan}) mulai bekerja di {self.nama_toko}")

    def keluarkan_karyawan(self, nama):
        """Melepas referensi karyawan tanpa memusnahkan objeknya."""
        awal = len(self._daftar_karyawan)
        self._daftar_karyawan = [k for k in self._daftar_karyawan if k.nama != nama]
        if len(self._daftar_karyawan) < awal:
            print(f"  [-] {nama} telah berhenti dari {self.nama_toko}")

    @property
    def total_sepatu(self):
        return len(self._daftar_sepatu)

    @property
    def total_pegawai(self):
        return len(self._daftar_karyawan)

    def tampilkan_data_toko(self):
        print(f"\n  {self.nama_toko} - {self.alamat}")
        print(f"  Katalog sepatu ({self.total_sepatu}):")
        for s in self._daftar_sepatu:
            print(f"    - {s.nama_sepatu} ({s.merek}) stok {s.stok}")
        print(f"  Pegawai ({self.total_pegawai}):")
        for k in self._daftar_karyawan:
            print(f"    - {k.nama} ({k.jabatan})")


# =====================================================================
# CLASS 6 : TRANSAKSI
# Menghubungkan objek Sepatu dan Karyawan untuk memproses penjualan.
# (ASOSIASI: kedua objek dibuat di luar dan hanya diterima.)
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
        self.karyawan = karyawan      # objek Karyawan / Kasir / Supervisor
        self.jumlah_beli = jumlah_beli
        self.status = "BELUM DIPROSES"

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
            self.status = "GAGAL"
            print("Transaksi dibatalkan karena stok tidak mencukupi.\n")
            return

        subtotal = self.sepatu.harga * self.jumlah_beli
        if pakai_diskon_member:
            subtotal -= subtotal * Sepatu.diskon_member

        total = Transaksi.hitung_total_dengan_pajak(subtotal, Transaksi.pajak)
        self.total_bayar = total
        self.status = "BERHASIL"
        print(f"Transaksi {self.id_transaksi} berhasil diproses oleh {self.karyawan.nama}.\n")

    def tampilkan_struk(self):
        """Menampilkan struk hasil transaksi."""
        if self.status != "BERHASIL":
            print(f"Struk {self.id_transaksi} tidak dapat dicetak (status: {self.status}).\n")
            return
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

    # 2. Membuat objek Karyawan (INHERITANCE: Kasir & Supervisor)
    print("--- 2. Membuat Objek Karyawan (Subclass) ---")
    kasir1 = Kasir("Dimas", 3500000, shift="Pagi", pin="1234")
    supervisor1 = Supervisor.dari_dict({
        "nama": "Rina", "gaji": 5000000,
        "divisi": "Operasional", "tunjangan_jabatan": 1000000
    })
    kasir1.tampilkan_profil()          # versi override milik Kasir
    supervisor1.tampilkan_profil()     # versi override milik Supervisor
    print(f"Total karyawan terdaftar (atribut kelas): {Karyawan.total_karyawan}")
    print("isinstance(kasir1, Karyawan)      :", isinstance(kasir1, Karyawan))
    print("issubclass(Supervisor, Karyawan)  :", issubclass(Supervisor, Karyawan))
    print()

    # 3. Uji instance method
    print("--- 3. Uji Instance Method ---")
    sepatu1.tambah_stok(5)
    kasir1.naikkan_gaji(10)            # method diwarisi dari Karyawan
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

    # 6. ASOSIASI: objek Sepatu hanya dipakai lewat parameter method
    print("--- 6. Relasi ASOSIASI (Kasir/Supervisor ..> Sepatu) ---")
    kasir1.cek_ketersediaan(sepatu1, 2)
    kasir1.cek_ketersediaan(sepatu2, 100)
    supervisor1.periksa_stok_rendah(sepatu1, batas=30)
    supervisor1.periksa_stok_rendah(sepatu2, batas=10)
    print()

    # 7. Membuat & memproses Transaksi
    print("--- 7. Membuat & Memproses Transaksi ---")
    transaksi1 = Transaksi("TRX001", sepatu1, kasir1, 2)
    transaksi1.proses_transaksi(pakai_diskon_member=True)
    kasir1.catat_transaksi()
    transaksi1.tampilkan_struk()

    transaksi2 = Transaksi("TRX002", sepatu2, supervisor1, 3)
    transaksi2.proses_transaksi()
    transaksi2.tampilkan_struk()

    transaksi3 = Transaksi("TRX003", sepatu2, kasir1, 999)   # stok tidak cukup
    transaksi3.proses_transaksi()
    transaksi3.tampilkan_struk()

    print(f"Total transaksi tercatat (atribut kelas): {Transaksi.total_transaksi}\n")

    # 8. KOMPOSISI: Sepatu *-- CatatanStok
    print("--- 8. Relasi KOMPOSISI (Sepatu *-- CatatanStok) ---")
    sepatu1.cetak_riwayat_stok()
    sepatu2.cetak_riwayat_stok()
    print()

    # 9. AGREGASI: TokoSepatu o-- Sepatu & Karyawan
    print("--- 9. Relasi AGREGASI (TokoSepatu o-- Sepatu & Karyawan) ---")
    toko = TokoSepatu("Toko Sepatu Otep", "Samarinda")
    toko.tambah_sepatu(sepatu1)
    toko.tambah_sepatu(sepatu2)
    toko.tambah_karyawan(kasir1)
    toko.tambah_karyawan(supervisor1)
    toko.tampilkan_data_toko()

    toko.keluarkan_karyawan("Dimas")
    print("\nToko dibubarkan (del toko) ...")
    del toko
    print("Objek tetap ada di memori setelah toko dihapus:")
    sepatu1.tampilkan_info()
    kasir1.tampilkan_profil()
    print()

    # 10. Method overriding & akses protected / private
    print("--- 10. Method Overriding & Tingkat Akses ---")
    print(f"Gaji pokok Dimas (Kasir)      : Rp{kasir1.gaji:,.0f}")
    print(f"Gaji bulanan Dimas (+bonus)   : Rp{kasir1.hitung_gaji_bulanan():,.0f}")
    print(f"Gaji pokok Rina (Supervisor)  : Rp{supervisor1.gaji:,.0f}")
    print(f"Gaji bulanan Rina (+tunjangan): Rp{supervisor1.hitung_gaji_bulanan():,.0f}")
    print("PIN Dimas benar (1234)? :", kasir1.verifikasi_pin("1234"))
    print("PIN Dimas benar (0000)? :", kasir1.verifikasi_pin("0000"))
    try:
        print(kasir1.__pin)      # private: tidak bisa diakses dari luar
    except AttributeError as e:
        print("Akses __pin ditolak (private):", e)
    print()

    # 11. Uji property setter: DATA VALID & TIDAK VALID
    print("--- 11. Uji Setter & Validasi Data ---")

    print("Stok sepatu2 sebelum diubah :", sepatu2.stok)
    sepatu2.stok = 50                       # valid
    print("Stok sepatu2 setelah diubah (valid) :", sepatu2.stok)
    try:
        sepatu2.stok = -10                  # tidak valid -> harus ditolak
    except ValueError as e:
        print("Gagal mengubah stok (tidak valid) :", e)

    print("\nGaji supervisor1 sebelum diubah :", supervisor1.gaji)
    supervisor1.gaji = 5500000              # valid
    print("Gaji supervisor1 setelah diubah (valid) :", supervisor1.gaji)
    try:
        supervisor1.gaji = -1000000         # tidak valid -> harus ditolak
    except ValueError as e:
        print("Gagal mengubah gaji (tidak valid) :", e)

    print("\nTotal bayar transaksi1 saat ini :", transaksi1.total_bayar)
    try:
        transaksi1.total_bayar = -500       # tidak valid -> harus ditolak
    except ValueError as e:
        print("Gagal mengubah total bayar (tidak valid) :", e)