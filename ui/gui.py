import tkinter as tk
from tkinter import messagebox
import sys
import os

# --- 1. SETUP PATH UNTUK MENGIMPOR INFERENCE ENGINE ---
# Ini memungkinkan gui.py (di folder ui/) mengimpor engine.py (di folder inference_engine/)
# Tambahkan folder induk (nama_proyek/) ke path sistem
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Coba impor mesin inferensi yang sebenarnya
# Asumsikan Anda memiliki file engine.py di folder inference_engine/
try:
    # Anda akan mengganti 'inference_engine' dan 'engine' dengan nama folder dan file Anda
    from inference_engine.engine import run_inference
except ImportError:
    # Jika impor gagal (misalnya, untuk pengujian cepat), gunakan fungsi dummy
    def run_inference(gejala_list):
        """Fungsi dummy untuk simulasi hasil inferensi."""
        print(f"Simulasi: Menerima gejala: {gejala_list}")
        
        # Logika simulasi sederhana:
        if "demam" in gejala_list and "batuk" in gejala_list:
            return "Diagnosis: Flu Biasa"
        elif "sakit kepala" in gejala_list and "mual" in gejala_list:
            return "Diagnosis: Migrain"
        else:
            return "Diagnosis: Tidak Ada Hasil Jelas"

# --- 2. KONFIGURASI APLIKASI UTAMA (GUI) ---

class ExpertSystemGUI:
    def __init__(self, master):
        self.master = master
        master.title("Sistem Pakar Diagnosa Sederhana")

        # Variabel untuk menampung gejala yang dipilih
        self.gejala_vars = {
            "demam": tk.BooleanVar(),
            "batuk": tk.BooleanVar(),
            "sakit kepala": tk.BooleanVar(),
            "mual": tk.BooleanVar(),
            "pusing": tk.BooleanVar()
        }

        # Header
        tk.Label(master, text="Pilih Gejala yang Dirasakan:", font=("Arial", 12, "bold")).pack(pady=10)

        # Frame untuk Checkbox Gejala
        self.gejala_frame = tk.Frame(master)
        self.gejala_frame.pack(padx=20, pady=5)
        
        # Membuat Checkbox untuk setiap Gejala
        for i, (gejala, var) in enumerate(self.gejala_vars.items()):
            # Checkbutton (Checkbox)
            chk = tk.Checkbutton(self.gejala_frame, text=gejala.capitalize(), variable=var)
            chk.grid(row=i // 2, column=i % 2, sticky="w", padx=10, pady=5) # Tata letak 2 kolom

        # Tombol Proses
        self.process_button = tk.Button(master, text="Proses Diagnosa", command=self.proses_diagnosa, bg="green", fg="white")
        self.process_button.pack(pady=20)

        # Area Hasil
        tk.Label(master, text="Hasil Diagnosa:", font=("Arial", 10)).pack()
        self.result_label = tk.Label(master, text="", fg="blue", font=("Arial", 11, "italic"))
        self.result_label.pack(pady=10)

    def proses_diagnosa(self):
        """Fungsi yang dipanggil saat tombol Proses Diagnosa ditekan."""
        
        # 1. Kumpulkan Fakta (Gejala)
        gejala_dipilih = []
        for gejala, var in self.gejala_vars.items():
            if var.get():
                gejala_dipilih.append(gejala)

        if not gejala_dipilih:
            messagebox.showwarning("Input Kosong", "Mohon pilih setidaknya satu gejala.")
            self.result_label.config(text="")
            return

        # 2. Panggil Mesin Inferensi
        try:
            # Panggil fungsi run_inference dari mesin inferensi
            hasil_diagnosa = run_inference(gejala_dipilih)
            
            # 3. Tampilkan Hasil
            self.result_label.config(text=hasil_diagnosa)