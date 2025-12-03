from django.db import models
from django.utils import timezone

# 1. Master Data Jenis Sirkuit (Produk)
class Circuit(models.Model):
    CATEGORY_CHOICES = [
        ('MAIN', 'Main Harness'),
        ('ENGINE', 'Engine Harness'),
        ('BODY', 'Body Harness'),
        ('DOOR', 'Door/Sensor Harness'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Nama Part")
    code = models.CharField(max_length=50, unique=True, verbose_name="Kode Part")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="Kategori")
    stock_qty = models.IntegerField(default=0, verbose_name="Stok Saat Ini")
    min_stock_limit = models.IntegerField(default=100, verbose_name="Batas Buffer Stock")

    def __str__(self):
        return f"{self.code} - {self.name}"

    # Fitur Warna: Jika stok kurang dari batas, tandai merah di Admin
    def is_critical(self):
        return self.stock_qty < self.min_stock_limit
    is_critical.boolean = True
    is_critical.short_description = "Status Kritis?"

# 2. Status Mesin (Menjawab masalah kerusakan mesin)
class Machine(models.Model):
    STATUS_CHOICES = [
        ('RUNNING', 'Running Normal'),
        ('MAINTENANCE', 'Perbaikan Rutin'),
        ('BREAKDOWN', 'Rusak/Stop'),
    ]
    
    name = models.CharField(max_length=50, verbose_name="Nama Mesin")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='RUNNING')
    last_checked = models.DateTimeField(auto_now=True, verbose_name="Pengecekan Terakhir")

    def __str__(self):
        return self.name

# 3. Pencatatan Transaksi Supply (Keluar Masuk)
class SupplyLog(models.Model):
    TYPE_CHOICES = [
        ('IN', 'Masuk dari Gudang'),
        ('OUT', 'Supply ke Housing/Produksi'),
    ]
    
    circuit = models.ForeignKey(Circuit, on_delete=models.CASCADE, verbose_name="Sirkuit")
    transaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name="Tipe Transaksi")
    quantity = models.IntegerField(verbose_name="Jumlah")
    pic_name = models.CharField(max_length=100, verbose_name="PIC / Petugas")
    timestamp = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Logika Otomatis: Update stok saat transaksi disimpan
        # Jika ini data baru (belum punya ID), update stok
        if not self.pk: 
            if self.transaction_type == 'IN':
                self.circuit.stock_qty += self.quantity
            else:
                self.circuit.stock_qty -= self.quantity
            
            self.circuit.save() # Simpan perubahan stok ke master barang
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_type} - {self.circuit.name} ({self.quantity})"
