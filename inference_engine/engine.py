import json

from inference_engine.disease_names import disease_names

def load_rules(path="rules.json"):
    with open(path, "r") as f:
        return json.load(f)

def infer(facts, rules):
    results = {}
    for rule in rules:
        if all(cond in facts for cond in rule["if"]):
            conclusion = rule["then"]
            cf = rule["cf"]
            if conclusion in results:
                # aturan perhitungan cf paralel
                cf_old = results[conclusion]
                cf = cf_old + cf * (1 - cf_old)
            results[conclusion] = cf
    return results

def run_inference(gejala_list):
    """Wrapper untuk menjalankan inferensi dari GUI."""
    rules = load_rules()
    hasil = infer(gejala_list, rules)
    if not hasil:
        return "Tidak ada penyakit yang terdeteksi."
    
    hasil_text = ""
    for kode, cf in hasil.items():
        nama = disease_names.get(kode, kode)  # fallback ke kode kalau belum ada nama
        hasil_text += f"{nama}: {cf*100:.2f}%\n"
    return hasil_text.strip()

    # Format hasil ke bentuk teks agar bisa ditampilkan di GUI
    ## hasil_text = "\n".join([f"{kode}: {cf*100:.2f}%" for kode, cf in hasil.items()])
    ## return hasil_text


if __name__ == "__main__":
    rules = load_rules()
    sample = ["G05"]
    print(infer(sample, rules))
