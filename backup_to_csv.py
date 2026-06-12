import json
import csv
import os

# Map target JSON files to output CSV filenames
targets = {
    "data/escribe/sd68.json": "sd68_local_backup.csv",
    "data/wordpress/stzuminus.json": "stzuminus_local_backup.csv"
}

for json_path, csv_path in targets.items():
    if not os.path.exists(json_path):
        print(f"[-] Missing file: {json_path}")
        continue
        
    with open(json_path, 'r', encoding='utf-8') as jf:
        try:
            data = json.load(jf)
        except json.JSONDecodeError:
            print(f"[-] Corrupt JSON: {json_path}")
            continue
            
    if not data:
        print(f"[-] Empty data: {json_path}")
        continue

    # Dynamically extract all structural headers
    headers = set()
    for entry in data:
        headers.update(entry.keys())
    headers = list(headers)
    
    # Prioritize core columns in the CSV output
    core_columns = ["doc_title", "source_url", "jurisdiction", "doc_date", "sourceName"]
    sorted_headers = [col for col in core_columns if col in headers] + \
                     [col for col in headers if col not in core_columns]

    with open(csv_path, 'w', newline='', encoding='utf-8-sig') as cf:
        writer = csv.DictWriter(cf, fieldnames=sorted_headers)
        writer.writeheader()
        writer.writerows(data)
        
    print(f"[+] Backup generated: {csv_path} | Records: {len(data)}")
