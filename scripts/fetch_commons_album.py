"""
Скрыпт для аўтаматычнага выцягвання гравюр і метаданых з любой катэгорыі альбома на Вікісховішчы (Wikimedia Commons)
Выкарыстанне:
    python fetch_commons_album.py "Curioses Staats und Kriegs Theatrum in Polen (1730)"
"""

import sys
import os
import json
import urllib.request
import urllib.parse
import re

def fetch_category_files(category_name, limit=50):
    encoded_cat = urllib.parse.quote(category_name)
    url = f"https://commons.wikimedia.org/w/api.php?action=query&generator=categorymembers&gcmtitle=Category:{encoded_cat}&gcmlimit={limit}&prop=imageinfo&iiprop=url|extmetadata&iiurlwidth=800&format=json"
    
    headers = {
        'User-Agent': 'EngravingsMapBot/1.0 (historical research; contact: user@github.com)'
    }
    
    req = urllib.request.Request(url, headers=headers)
    print(f"Запыт да Вікісховішча па катэгорыі: {category_name}...")
    
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"Памылка запыту: {e}")
        return []

    pages = data.get('query', {}).get('pages', {}).values()
    results = []

    for page in pages:
        title = page.get('title', '')
        imageinfo = page.get('imageinfo', [{}])[0]
        
        url_thumb = imageinfo.get('thumburl', '')
        url_full = imageinfo.get('url', '')
        meta = imageinfo.get('extmetadata', {})
        
        desc_html = meta.get('ImageDescription', {}).get('value', '')
        desc_clean = re.sub('<[^<]+?>', '', desc_html).strip()
        
        artist_html = meta.get('Artist', {}).get('value', '')
        artist_clean = re.sub('<[^<]+?>', '', artist_html).strip()
        
        date = meta.get('DateTimeOriginal', {}).get('value', '')
        
        # Шаблон для дадання ў базу
        safe_id = re.sub(r'[^a-zA-Z0-9_-]', '_', title.replace('File:', '')).lower()[:40]
        
        entry = {
            "id": safe_id,
            "title": title.replace('File:', '').replace('.jpg', '').replace('.tif', ''),
            "original_title": "",
            "status": "authentic",  # або 'pseudo', 'composite'
            "status_label": "Аўтэнтычная выява",
            "claimed_location": {
                "name": "Не вызначана",
                "lat": 53.9,
                "lng": 27.56
            },
            "actual_location": {
                "name": "Не вызначана",
                "lat": 53.9,
                "lng": 27.56
            },
            "year": None,
            "century": 18,
            "artist": artist_clean or "Невядомы",
            "publisher": "",
            "album": category_name,
            "commons_url": f"https://commons.wikimedia.org/wiki/{urllib.parse.quote(title)}",
            "image_url": url_thumb or url_full,
            "description": desc_clean[:300]
        }
        results.append(entry)

    return results

def main():
    cat = sys.argv[1] if len(sys.argv) > 1 else "Curioses Staats und Kriegs Theatrum in Polen (1730)"
    out_file = "extracted_plates.json"
    
    files = fetch_category_files(cat)
    print(f"Знойдзена аркушаў: {len(files)}")
    
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(files, f, ensure_ascii=False, indent=2)
        
    print(f"Захавана ў файл: {out_file}")
    print("Цяпер вы можаце адрэдагаваць каардынаты гарадоў і дадаць запісы ў data/engravings.json!")

if __name__ == '__main__':
    main()
