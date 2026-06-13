import os
import glob

folder = "_search_source"
html_files = glob.glob(os.path.join(folder, "*.html"))

print(f"Disabling English stemming across {len(html_files)} files for strict exact-matching...")

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Kills the linguistic stemmer
    content = content.replace('<html lang="en">', '<html lang="none">')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Formatting complete! Ready for strict-match compilation.")