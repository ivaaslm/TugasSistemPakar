import json
import os

# Tentukan path relatif ke rules.json (satu tingkat di atas)
RULES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'rules.json')

def muat_aturan(file_path=RULES_FILE):
    """Memuat aturan dari rules.json."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File aturan tidak ditemukan: {file_path}")
    
    with open(file_path, 'r') as f:
        # Asumsi rules.json sudah ada dan terisi
        return json.load(f)

def run_inference(gejala_list):
    """
    Fungsi Mesin Inferensi (Simulasi).
    
    Dalam implementasi nyata, fungsi ini akan menggunakan muat_aturan() 
    dan menerapkan Forward/Backward Chaining.
    """
    
    try:
        # Coba muat aturan nyata (opsional, untuk debugging)
        aturan_dasar = muat_aturan()
        # Di sini, Anda akan menggunakan aturan_dasar untuk inferensi
    except Exception:
        # Lanjutkan dengan logika dummy jika rules.json kosong/gagal dimuat
        pass 

    print(f"Mesin Inferensi: Menerima gejala: {gejala_list}")
    
    # Logika simulasi sederhana (Ganti ini dengan logika Inferensi Engine Anda)
    gejala_set = set(gejala_list)
    
    if "demam" in gejala_set and "batuk" in gejala_set and "kelelahan" in gejala_set:
        return "Diagnosis: Infeksi Virus (Perlu Istirahat)"
    elif "sakit kepala" in gejala_set and "mual" in gejala_set:
        return "Diagnosis: Migrain Klasik"
    elif "sakit kepala" in gejala_set or "demam" in gejala_set:
        return "Diagnosis: Gejala Umum (Minum Obat Bebas)"
    else:
        return "Diagnosis: Tidak Ada Hasil Jelas. Konsultasi lebih lanjut."

# end of inference_engine/engine.py