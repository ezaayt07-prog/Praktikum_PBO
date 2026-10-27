import gc
import weakref
from abc import ABC, abstractmethod


# ==================================================
# CLASS : CATATAN STOK  (bagian dari KOMPOSISI)
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
# OPERATOR OVERLOADING: __str__, __eq__, __lt__
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

        self.__stok = stok          # PRIVATE: data sensitif
        self._riwayat_stok = []     # PROTECTED + KOMPOSISI: berisi objek CatatanStok

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

    # OPERATOR OVERLOADING
    def __str__(self):
        return f"{self.merek} {self.nama_sepatu} (ukuran {self.ukuran}) - Rp{self.harga:,}"

    def __eq__(self, other):
        """Dua sepatu dianggap sama jika nama, merek, dan ukurannya sama."""
        if not isinstance(other, Sepatu):
            return NotImplemented
        return ((self.nama_sepatu, self.merek, self.ukuran)
                == (other.nama_sepatu, other.merek, other.ukuran))

    def __lt__(self, other):
        """Sepatu dibandingkan berdasarkan harga (agar bisa dipakai sorted/min/max)."""
        return self.harga < other.harga

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
# CLASS 2 : KARYAWAN  (ABSTRACT BASE CLASS / SUPERCLASS)
# Kontrak untuk SEMUA jenis karyawan.
#   - 2 abstract method : hitung_gaji_bulanan(), deskripsi_tugas()
#   - method konkret    : tampilkan_profil(), cetak_slip_gaji()
#   - _gaji   : PROTECTED -> dipakai langsung oleh subclass
#   - __pin   : PRIVATE   -> rahasia, hanya untuk Karyawan
# Karyawan tidak bisa diinstansiasi langsung.
# ==================================================================
class Karyawan(ABC):

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

    # ----------- ABSTRACT METHOD (wajib diimplementasikan subclass) -----------
    @abstractmethod
    def hitung_gaji_bulanan(self):
        """Gaji yang diterima per bulan. Rumusnya berbeda di tiap jenis karyawan."""
        pass

    @abstractmethod
    def deskripsi_tugas(self):
        """Kalimat yang menjelaskan tugas khusus karyawan tersebut."""
        pass

    # ----------- METHOD KONKRET (dipakai bersama semua subclass) -----------
    def tampilkan_profil(self):
        """Alur yang sama untuk semua karyawan; bagian khusus dijawab tiap subclass."""
        print(f"Nama: {self.nama} | Jabatan: {self.jabatan} | "
              f"Perusahaan: {Karyawan.nama_perusahaan}")
        print(f"   -> Tugas: {self.deskripsi_tugas()}")

    def cetak_slip_gaji(self):
        """Slip gaji: format sama, nominal dihitung oleh method abstrak milik subclass."""
        print(f"Slip gaji {self.nama:<8} ({self.jabatan:<10}) : "
              f"Rp{self.hitung_gaji_bulanan():,.0f}")

    # INSTANCE METHOD
    def verifikasi_pin(self, pin_input):
        """Satu-satunya cara memeriksa PIN (data private tidak dibuka keluar)."""
        return pin_input == self.__pin

    def naikkan_gaji(self, persen):
        """Menaikkan gaji karyawan berdasarkan persentase tertentu."""
        if persen <= 0:
            print("Persentase kenaikan harus lebih dari 0.")
            return
        gaji_baru = self._gaji + (self._gaji * persen / 100)
        self.gaji = gaji_baru    # lewat setter agar tervalidasi
        print(f"Gaji {self.nama} naik {persen}% menjadi Rp{self.gaji:,.0f}")

    # OPERATOR OVERLOADING (memanfaatkan method abstrak -> polimorfis)
    def __str__(self):
        return f"{self.nama} ({self.jabatan})"

    def __lt__(self, other):
        """Karyawan dibandingkan berdasarkan gaji bulanan yang benar-benar diterima."""
        return self.hitung_gaji_bulanan() < other.hitung_gaji_bulanan()

    # CLASS METHOD
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

    # IMPLEMENTASI METHOD ABSTRAK
    def hitung_gaji_bulanan(self):
        return self._gaji + (self.jumlah_transaksi * Kasir.bonus_per_transaksi)

    def deskripsi_tugas(self):
        return (f"melayani pembayaran pelanggan (shift {self.shift}, "
                f"{self.jumlah_transaksi} transaksi ditangani)")

    @classmethod
    def dari_dict(cls, data):
        """Factory method: membuat Kasir dari dictionary."""
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

    # IMPLEMENTASI METHOD ABSTRAK
    def hitung_gaji_bulanan(self):
        return self._gaji + self.tunjangan_jabatan

    def deskripsi_tugas(self):
        return (f"mengawasi operasional divisi {self.divisi} "
                f"(tunjangan Rp{self.tunjangan_jabatan:,})")

    @classmethod
    def dari_dict(cls, data):
        """Factory method: membuat Supervisor dari dictionary."""
        return cls(data["nama"], data["gaji"], data["divisi"], data["tunjangan_jabatan"])


# ==================================================================
# CLASS 5 : PETUGAS GUDANG  (SUBCLASS dari Karyawan)
# Ditambahkan TANPA mengubah satu baris pun kode lama (prinsip OCP).
# Atribut unik: jumlah_barang_diproses
# ==================================================================
class PetugasGudang(Karyawan):

    bonus_per_unit = 2000            # atribut kelas milik PetugasGudang

    def __init__(self, nama, gaji, pin="0000"):
        super().__init__(nama, "Gudang", gaji, pin)
        self.jumlah_barang_diproses = 0                 # atribut spesifik PetugasGudang

    # ASOSIASI: objek Sepatu diterima sebagai parameter, tidak disimpan
    def terima_barang(self, sepatu, jumlah):
        """Petugas gudang menerima kiriman supplier lalu menambah stok sepatu."""
        print(f"Petugas gudang {self.nama} menerima {jumlah} pasang '{sepatu.nama_sepatu}'")
        sepatu.tambah_stok(jumlah)
        self.jumlah_barang_diproses += jumlah

    # IMPLEMENTASI METHOD ABSTRAK
    def hitung_gaji_bulanan(self):
        return self._gaji + (self.jumlah_barang_diproses * PetugasGudang.bonus_per_unit)

    def deskripsi_tugas(self):
        return (f"mengelola penerimaan barang gudang "
                f"({self.jumlah_barang_diproses} pasang diproses)")


# ==================================================================
# CLASS 6 : TOKO SEPATU
# AGREGASI: menampung objek Sepatu & Karyawan yang dibuat di luar.
# Jika toko dihapus, sepatu dan karyawan tetap ada.
# OPERATOR OVERLOADING: __len__
# ==================================================================
class TokoSepatu:

    def __init__(self, nama_toko, alamat):
        self.nama_toko = nama_toko
        self.alamat = alamat
        self._daftar_sepatu = []        # agregasi: referensi objek dari luar
        self._daftar_karyawan = []      # agregasi: referensi objek dari luar

    def tambah_sepatu(self, sepatu):
        if isinstance(sepatu, Sepatu):                  # validasi masukan
            self._daftar_sepatu.append(sepatu)
            print(f"  [+] {sepatu.nama_sepatu} masuk katalog {self.nama_toko}")

    def tambah_karyawan(self, karyawan):
        if isinstance(karyawan, Karyawan):              # validasi masukan (semua subclass lolos)
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

    def total_gaji_bulanan(self):
        """POLIMORFISME: tiap karyawan menghitung gajinya sendiri, toko tidak perlu tahu jenisnya."""
        return sum(k.hitung_gaji_bulanan() for k in self._daftar_karyawan)

    def tampilkan_data_toko(self):
        print(f"\n  {self.nama_toko} - {self.alamat}")
        print(f"  Katalog sepatu ({self.total_sepatu}):")
        for s in self._daftar_sepatu:
            print(f"    - {s.nama_sepatu} ({s.merek}) stok {s.stok}")
        print(f"  Pegawai ({self.total_pegawai}):")
        for k in self._daftar_karyawan:
            print(f"    - {k.nama} ({k.jabatan})")

    # OPERATOR OVERLOADING
    def __len__(self):
        """len(toko) = jumlah jenis sepatu di katalog."""
        return len(self._daftar_sepatu)


# ==================================================================
# SALURAN PENGIRIM STRUK  (DUCK TYPING)
# Tiga kelas di bawah TIDAK berhubungan lewat pewarisan,
# tetapi semuanya punya method kirim(teks).
# ==================================================================
class PrinterStruk:
    def __init__(self, nama_printer):
        self.nama_printer = nama_printer

    def kirim(self, teks):
        print(f"[PRINTER {self.nama_printer}] mencetak struk:")
        for baris in teks.splitlines():
            print(f"    {baris}")


class EmailStruk:
    def __init__(self, alamat):
        self.alamat = alamat

    def kirim(self, teks):
        print(f"[EMAIL -> {self.alamat}] struk terkirim ({len(teks.splitlines())} baris)")


class WhatsAppStruk:
    def __init__(self, nomor):
        self.nomor = nomor

    def kirim(self, teks):
        print(f"[WHATSAPP -> {self.nomor}] struk terkirim ({len(teks.splitlines())} baris)")


def distribusikan_struk(daftar_saluran, teks):
    """Duck typing: saluran apa pun yang punya kirim() bisa dipakai."""
    for saluran in daftar_saluran:
        saluran.kirim(teks)


# =====================================================================
# CLASS 7 : TRANSAKSI
# Menghubungkan objek Sepatu dan Karyawan untuk memproses penjualan.
# (ASOSIASI: kedua objek dibuat di luar dan hanya diterima.)
# OPERATOR OVERLOADING: __add__, __radd__
# =====================================================================
class Transaksi:

    # ATRIBUT KELAS
    nama_toko = "Toko Sepatu Otep"
    total_transaksi = 0
    pajak = 0.11

    def __init__(self, id_transaksi, sepatu, karyawan, jumlah_beli):
        # ATRIBUT INSTANCE
        self.id_transaksi = id_transaksi
        self.sepatu = sepatu          # objek dari class Sepatu (dibuat di luar)
        self.karyawan = karyawan      # objek Karyawan apa pun (dibuat di luar)
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

    def teks_struk(self):
        """Menyusun isi struk sebagai teks (tidak peduli akan dikirim ke mana)."""
        return "\n".join([
            "========== STRUK PEMBELIAN ==========",
            f"Toko        : {Transaksi.nama_toko}",
            f"ID Transaksi: {self.id_transaksi}",
            f"Kasir       : {self.karyawan.nama}",
            f"Produk      : {self.sepatu.nama_sepatu} ({self.sepatu.merek})",
            f"Jumlah      : {self.jumlah_beli}",
            f"Total Bayar : Rp{self.total_bayar:,.0f}",
            "======================================",
        ])

    def tampilkan_struk(self):
        """Menampilkan struk hasil transaksi."""
        if self.status != "BERHASIL":
            print(f"Struk {self.id_transaksi} tidak dapat dicetak (status: {self.status}).\n")
            return
        print(self.teks_struk() + "\n")

    def kirim_struk(self, daftar_saluran):
        """DIP: saluran pengiriman disuntikkan dari luar, Transaksi tidak membuatnya sendiri."""
        if self.status != "BERHASIL":
            print(f"Struk {self.id_transaksi} tidak dapat dikirim (status: {self.status}).")
            return
        distribusikan_struk(daftar_saluran, self.teks_struk())

    # OPERATOR OVERLOADING
    def __add__(self, other):
        """transaksi_a + transaksi_b = jumlah total bayar keduanya (bisa juga + angka)."""
        return self.total_bayar + getattr(other, "total_bayar", other)

    __radd__ = __add__               # agar sum([...]) yang diawali angka 0 tetap bekerja

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

    # 2. ABSTRAKSI: abstract class tidak bisa diinstansiasi
    print("--- 2. Bukti Abstraksi: Abstract Class Tidak Bisa Diinstansiasi ---")
    print("Abstract method milik Karyawan :", sorted(Karyawan.__abstractmethods__))
    try:
        karyawan_langsung = Karyawan("Budi", "Umum", 3000000)
    except TypeError as e:
        print("Karyawan(...) langsung -> TypeError:", e)

    class KaryawanTidakLengkap(Karyawan):
        """Subclass yang LUPA mengimplementasikan deskripsi_tugas()."""
        def hitung_gaji_bulanan(self):
            return self._gaji

    try:
        karyawan_cacat = KaryawanTidakLengkap("Tono", "Magang", 1000000)
    except TypeError as e:
        print("Subclass tidak lengkap -> TypeError:", e)
    print()

    # 3. INHERITANCE: tiga subclass dari Karyawan
    print("--- 3. Membuat Objek Karyawan (Subclass dari Abstract Class) ---")
    kasir1 = Kasir("Dimas", 3500000, shift="Pagi", pin="1234")
    supervisor1 = Supervisor.dari_dict({
        "nama": "Rina", "gaji": 5000000,
        "divisi": "Operasional", "tunjangan_jabatan": 1000000
    })
    gudang1 = PetugasGudang("Joko", 3000000)
    kasir1.tampilkan_profil()          # method konkret milik Karyawan
    supervisor1.tampilkan_profil()
    gudang1.tampilkan_profil()
    print(f"Total karyawan terdaftar (atribut kelas): {Karyawan.total_karyawan}")
    print("isinstance(kasir1, Karyawan)      :", isinstance(kasir1, Karyawan))
    print("issubclass(Supervisor, Karyawan)  :", issubclass(Supervisor, Karyawan))
    print()

    # 4. Uji instance, static & class method
    print("--- 4. Uji Instance, Static & Class Method ---")
    sepatu1.tambah_stok(5)
    kasir1.naikkan_gaji(10)            # method diwarisi dari Karyawan
    print("Validasi ukuran 42        :", Sepatu.validasi_ukuran(42))
    print("Validasi ukuran 60        :", Sepatu.validasi_ukuran(60))
    print("Validasi nama 'Dimas'     :", Karyawan.validasi_nama("Dimas"))
    Sepatu.ubah_diskon_member(0.15)
    Karyawan.ubah_jam_kerja(9)
    print()

    # 5. ASOSIASI: objek Sepatu hanya dipakai lewat parameter method
    print("--- 5. Relasi ASOSIASI (Kasir/Supervisor/PetugasGudang ..> Sepatu) ---")
    kasir1.cek_ketersediaan(sepatu1, 2)
    kasir1.cek_ketersediaan(sepatu2, 100)
    supervisor1.periksa_stok_rendah(sepatu1, batas=30)
    supervisor1.periksa_stok_rendah(sepatu2, batas=10)
    gudang1.terima_barang(sepatu2, 10)
    print()

    # 6. Membuat & memproses Transaksi
    print("--- 6. Membuat & Memproses Transaksi ---")
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

    # 7. KOMPOSISI: Sepatu *-- CatatanStok
    print("--- 7. Relasi KOMPOSISI (Sepatu *-- CatatanStok) ---")
    sepatu1.cetak_riwayat_stok()
    sepatu2.cetak_riwayat_stok()

    sepatu_sementara = Sepatu("Court Classic", "Puma", 41, 700000, 8)
    ref_catatan = weakref.ref(sepatu_sementara._riwayat_stok[0])   # pantau CatatanStok
    print("\nCatatanStok milik 'Court Classic' masih hidup? :", ref_catatan() is not None)
    del sepatu_sementara
    gc.collect()
    print("Setelah Sepatu dihapus, CatatanStok masih ada?  :", ref_catatan() is not None)
    print()

    # 8. AGREGASI: TokoSepatu o-- Sepatu & Karyawan
    print("--- 8. Relasi AGREGASI (TokoSepatu o-- Sepatu & Karyawan) ---")
    toko = TokoSepatu("Toko Sepatu Otep", "Samarinda")
    toko.tambah_sepatu(sepatu1)
    toko.tambah_sepatu(sepatu2)
    toko.tambah_karyawan(kasir1)
    toko.tambah_karyawan(supervisor1)
    toko.tambah_karyawan(gudang1)
    toko.tampilkan_data_toko()
    print(f"len(toko) (operator overloading __len__) : {len(toko)}")

    toko.keluarkan_karyawan("Joko")
    print("\nToko dibubarkan (del toko) ...")
    del toko
    print("Objek tetap ada di memori setelah toko dihapus:")
    sepatu1.tampilkan_info()
    kasir1.tampilkan_profil()
    gudang1.tampilkan_profil()
    print()

    # 9. POLIMORFISME VIA PEWARISAN: satu loop, perilaku berbeda
    print("--- 9. Polimorfisme via Pewarisan (satu loop, tiga perilaku) ---")
    semua_karyawan = [kasir1, supervisor1, gudang1]
    for k in semua_karyawan:
        k.cetak_slip_gaji()            # hitung_gaji_bulanan() dijawab sendiri oleh tiap objek
    print()

    # 10. DUCK TYPING: kelas tidak berhubungan, method kirim() sama
    print("--- 10. Duck Typing (PrinterStruk, EmailStruk, WhatsAppStruk) ---")
    saluran = [PrinterStruk("Kasir-01"), EmailStruk("pelanggan@mail.com"),
               WhatsAppStruk("0812-3456-7890")]
    transaksi1.kirim_struk(saluran)
    transaksi3.kirim_struk(saluran)     # gagal -> tidak dikirim
    print()

    # 11. OPERATOR OVERLOADING
    print("--- 11. Operator Overloading ---")
    print("str(sepatu1)                      :", sepatu1)
    sepatu_kembar = Sepatu("Air Runner", "Nike", 42, 850000, 0)
    print("sepatu1 == sepatu_kembar (__eq__) :", sepatu1 == sepatu_kembar)
    print("sepatu1 == sepatu2        (__eq__):", sepatu1 == sepatu2)
    print("sepatu1 < sepatu2         (__lt__):", sepatu1 < sepatu2)
    print("Sepatu terurut dari termurah (sorted -> __lt__):")
    for s in sorted([sepatu2, sepatu1, sepatu_kembar]):
        print("   ", s)
    print("Karyawan terurut dari gaji bulanan terbesar (sorted -> __lt__):")
    for k in sorted(semua_karyawan, reverse=True):
        print(f"    {k} : Rp{k.hitung_gaji_bulanan():,.0f}")
    print(f"transaksi1 + transaksi2 (__add__) : Rp{transaksi1 + transaksi2:,.0f}")
    print(f"sum([transaksi1, transaksi2])     : Rp{sum([transaksi1, transaksi2]):,.0f}")
    print()

    # 12. Method overriding & akses protected / private
    print("--- 12. Akses Protected / Private ---")
    print(f"Gaji pokok Dimas (protected via property) : Rp{kasir1.gaji:,.0f}")
    print(f"Gaji bulanan Dimas (+bonus)               : Rp{kasir1.hitung_gaji_bulanan():,.0f}")
    print("PIN Dimas benar (1234)? :", kasir1.verifikasi_pin("1234"))
    print("PIN Dimas benar (0000)? :", kasir1.verifikasi_pin("0000"))
    try:
        print(kasir1.__pin)      # private: tidak bisa diakses dari luar
    except AttributeError as e:
        print("Akses __pin ditolak (private):", e)
    print()

    # 13. Uji property setter: DATA VALID & TIDAK VALID
    print("--- 13. Uji Setter & Validasi Data ---")
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