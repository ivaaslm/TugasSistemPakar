import tkinter as tk
from tkinter import messagebox
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from inference_engine import infer, load_rules, run_inference

# --- KONSTANTA WARNA ---
PINK_BG = "#FFC0CB"    # Warna Merah Jambu Muda untuk latar belakang
PINK_BUTTON = "#FF69B4" # Warna Merah Jambu Cerah untuk tombol
TEXT_COLOR = "#333333"

# --- 1. SETUP PATH DAN IMPOR INFERENCE ENGINE ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from inference_engine.engine import run_inference
    INFERENCE_READY = True
except ImportError:
    INFERENCE_READY = False
    print("ERROR: Mesin Inferensi tidak terhubung. Menggunakan fungsi dummy.")
    # Fungsi Dummy jika Engine gagal diimpor
    def run_inference(gejala_list):
        return f"SIMULASI: Diagnosis P01 (80%)" 

# --- 2. BASIS DATA GEJALA (DARI TABEL 2 JURNAL) ---
# Menggunakan Gejala yang relevan untuk GUI
GEJALA_DATA = {
    "G04": "Tidak terdapat benjolan pada payudara",
    "G05": "Tidak terdapat metastasis pada kelenjar getah bening regional di ketiak/aksila",
    "G06": "Terdapat benjolan pada payudara berukuran diameter 2 cm atau kurang",
    "G07": "Terdapat benjolan pada payudara berukuran diameter 2 cm hingga 5 cm",
    "G13": "Tidak terdapat metastasis jauh",
    # Tambahkan gejala lain sesuai kebutuhan (G01, G02, dst)
    "G01": "Kulit payudara berwarna kemerahan",
    "G14": "Terdapat metastasis jauh" 
}

# --- 3. KELAS APLIKASI GUI ---

class ExpertSystemGUI:
    def __init__(self, master):
        self.master = master
        master.title("Sistem Pakar Kanker Payudara")
        master.config(bg=PINK_BG, padx=20, pady=20) 
        root.resizable(False, False)

        # Variabel untuk menampung Gejala
        self.gejala_vars = {code: tk.BooleanVar() for code in GEJALA_DATA.keys()}

        # 3.1. Header
        header_frame = tk.Frame(master, bg=PINK_BUTTON)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        tk.Label(header_frame, text="APLIKASI KONSULTASI", font=("Arial", 16, "bold"), fg="white", bg=PINK_BUTTON).pack(pady=10)
        
        tk.Label(master, text="Pilih Gejala yang Anda Rasakan:", font=("Arial", 12), fg=TEXT_COLOR, bg=PINK_BG).pack(pady=(10, 5), anchor=tk.W)

        # 3.2. Frame untuk Checkbox Gejala
        self.gejala_frame = tk.Frame(master, bg="white", padx=10, pady=10, bd=1, relief=tk.SOLID)
        self.gejala_frame.pack(pady=10)
        
        # Membuat Checkbox
        for i, (code, deskripsi) in enumerate(GEJALA_DATA.items()):
            text_display = f"[{code}] {deskripsi}"
            chk = tk.Checkbutton(self.gejala_frame, 
                                 text=text_display, 
                                 variable=self.gejala_vars[code], 
                                 font=("Arial", 9),
                                 bg="white",
                                 fg=TEXT_COLOR,
                                 activebackground=PINK_BG,
                                 justify=tk.LEFT,
                                 anchor=tk.W)
            # Menata checkbox dalam 1 kolom (sticky W untuk rata kiri)
            chk.pack(fill=tk.X, padx=5, pady=2) 
        
        # 3.3. Tombol Proses
        self.process_button = tk.Button(master, 
                                        text="PROSES DIAGNOSA", 
                                        command=self.proses_diagnosa, 
                                        bg=PINK_BUTTON, fg="white", 
                                        font=("Arial", 11, "bold"), 
                                        activebackground="#FFD1E0")
        
        if not INFERENCE_READY:
             self.process_button.config(state=tk.DISABLED, text="ENGINE ERROR - CEK engine.py")

        self.process_button.pack(fill=tk.X, padx=20, pady=20)

        # 3.4. Area Hasil
        result_frame = tk.Frame(master, bg="white", bd=2, relief=tk.GROOVE, padx=15, pady=15)
        result_frame.pack(fill=tk.X, padx=5, pady=10)

        tk.Label(result_frame, text="HASIL DIAGNOSA:", font=("Arial", 10, "bold"), bg="white", fg=TEXT_COLOR).pack(anchor=tk.W)
        self.result_label = tk.Label(result_frame, text="Tekan 'PROSES DIAGNOSA' untuk melihat hasilnya.", 
                                     fg="#800080", font=("Arial", 12, "italic"), bg="white")
        self.result_label.pack(fill=tk.X, pady=5)

    def proses_diagnosa(self):
        """Mengumpulkan input dan memanggil Mesin Inferensi."""
        
        gejala_dipilih = [code for code, var in self.gejala_vars.items() if var.get()]

        if not gejala_dipilih:
            messagebox.showwarning("Input Kosong", "Mohon pilih setidaknya satu gejala untuk memulai diagnosa.")
            self.result_label.config(text="Menunggu input...", fg=TEXT_COLOR)
            return

        try:
            # Panggil fungsi run_inference dari mesin inferensi
            hasil_diagnosa = run_inference(gejala_dipilih)
            
            # Tampilkan Hasil
            self.result_label.config(text=hasil_diagnosa, fg=PINK_BUTTON)
            
        except Exception as e:
            messagebox.showerror("Error Logika", f"Kesalahan saat memproses inferensi: {e}")
            self.result_label.config(text="ERROR DALAM LOGIKA INFERENSI", fg="red")


# --- 4. EKSEKUSI UTAMA ---

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpertSystemGUI(root)
    root.mainloop()
