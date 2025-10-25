import json

from inference_engine.disease_names import disease_names

def load_rules(path="rules.json"):
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rules_path = os.path.join(base_dir, path)
    with open(rules_path, "r") as f:
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
    rules = load_rules()
    hasil = infer(gejala_list, rules)
    if not hasil:
        return "Tidak ada penyakit yang terdeteksi."
    
    hasil_text = ""
    for kode, cf in hasil.items():
        nama = disease_names.get(kode, kode)
        hasil_text += f"{nama}: {cf*100:.2f}%\n"
    return hasil_text.strip()


if __name__ == "__main__":
    rules = load_rules()
    sample = ["G05"]
    print(infer(sample, rules))
