import csv

with open('data/processed/monitoring_inference.csv', 'r') as f:
    reader = csv.reader(f)
    headers = next(reader)
    print("Headers:", headers)

    # Compter les lignes
    lines = list(reader)
    print(f"Nombre de lignes de données: {len(lines)}")

    if lines:
        print("Première ligne de données:", lines[0])