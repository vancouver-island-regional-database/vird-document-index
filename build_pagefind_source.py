import csv
import os
import subprocess
import time

csv_files = [
    "Escr_Ladysmith_json_format.csv",
    "Escr_sd68_json_format.csv",
    "WP_Ladysmithca_json_format.csv",
    "WP_stzuminus_json_format.csv"
]

output_dir = "_search_source"
os.makedirs(output_dir, exist_ok=True)

total_processed = 0

for file in csv_files:
    if not os.path.exists(file):
        continue
        
    print(f"\n[+] Processing: {file}")
    with open(file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            title = row.get('doc_title', 'Unknown Title')
            url = row.get('source_url', '')
            jurisdiction = row.get('jurisdiction', 'Unknown')
            date = row.get('doc_date', 'Unknown Date')
            
            if not url.startswith("http"):
                continue

            try:
                curl_cmd = ["curl", "-s", "-L", url]
                pdf_cmd = ["pdftotext", "-", "-"]
                
                curl_process = subprocess.Popen(curl_cmd, stdout=subprocess.PIPE)
                pdf_process = subprocess.Popen(pdf_cmd, stdin=curl_process.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                curl_process.stdout.close()
                
                raw_text, err = pdf_process.communicate(timeout=45)
                clean_text = raw_text.decode('utf-8', errors='ignore').strip()
                
            except Exception as e:
                clean_text = f"Extraction failed or timeout: {e}"

            html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
</head>
<body>
    <article data-pagefind-body>
        <h1 data-pagefind-meta="title">{title}</h1>
        <div data-pagefind-meta="jurisdiction" style="display:none;">{jurisdiction}</div>
        <div data-pagefind-meta="date" style="display:none;">{date}</div>
        <a href="{url}" data-pagefind-meta="link">Original PDF</a>
        <p>{clean_text}</p>
    </article>
</body>
</html>"""
            
            safe_title = "".join([c for c in title if c.isalnum() or c in (' ', '-', '_')]).strip().replace(' ', '_')
            if not safe_title:
                safe_title = f"document_{total_processed}"
                
            output_filename = os.path.join(output_dir, f"{safe_title}_{total_processed}.html")
            
            with open(output_filename, 'w', encoding='utf-8') as out_f:
                out_f.write(html_content)
                
            print(f"  - [{total_processed}] HTML built: {title[:50]}...")
            total_processed += 1
            
            # Rate limit to prevent IP bans
            time.sleep(0.25)
            
print(f"\n[=] Total documents processed: {total_processed}")
