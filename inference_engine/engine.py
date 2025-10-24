import json

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

if __name__ == "__main__":
    rules = load_rules()
    sample = ["G05"]
    print(infer(sample, rules))
