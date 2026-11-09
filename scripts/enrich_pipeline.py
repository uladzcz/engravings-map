"""
Паралельны канвеер аналізу гравюр з Вікісховішча, прывязкі да Вікіданых (Wikidata QID),
вызначэння аўтэнтычнасці/псеўда-відаў і лакальнай інтэграцыі ў інтэрактыўную карту.
"""

import os
import json
import urllib.request
import urllib.parse
import time
import re

HEADERS = {'User-Agent': 'EngravingsMapBot/1.0 (cultural-heritage research; contact: uladzcz@github.com)'}

def get_wikidata_info(city_name):
    """Шукае населены пункт у Вікіданых і вяртае QID, каардынаты і апісанне."""
    url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={urllib.parse.quote(city_name)}&language=be&type=item&format=json"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            results = data.get('search', [])
            if not results:
                # паспрабуем лацінкай або па-руску/па-англійску
                url2 = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={urllib.parse.quote(city_name)}&language=en&type=item&format=json"
                req2 = urllib.request.Request(url2, headers=HEADERS)
                with urllib.request.urlopen(req2) as resp2:
                    data2 = json.loads(resp2.read().decode('utf-8'))
                    results = data2.get('search', [])
            
            if not results:
                return None
            
            qid = results[0]['id']
            label = results[0].get('label', city_name)
            desc = results[0].get('description', '')
            
            # Атрымаем каардынаты (P625) па QID
            entity_url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={qid}&props=claims&format=json"
            req3 = urllib.request.Request(entity_url, headers=HEADERS)
            with urllib.request.urlopen(req3) as resp3:
                ent_data = json.loads(resp3.read().decode('utf-8'))
                claims = ent_data.get('entities', {}).get(qid, {}).get('claims', {})
                coords = claims.get('P625', [{}])[0].get('mainsnak', {}).get('datavalue', {}).get('value', {})
                
                lat = coords.get('latitude')
                lng = coords.get('longitude')
                
                return {
                    'qid': qid,
                    'name': label,
                    'desc': desc,
                    'lat': lat,
                    'lng': lng
                }
    except Exception as e:
        print(f"Wikidata error for {city_name}: {e}")
        return None

def download_commons_thumbnail(commons_file_title, local_filename, out_dir):
    """Атрымлівае URL мініяцюры шырынёй 500px з Вікісховішча і спампоўвае яе лакальна."""
    url = f"https://commons.wikimedia.org/w/api.php?action=query&titles={urllib.parse.quote(commons_file_title)}&prop=imageinfo&iiprop=url|extmetadata&iiurlwidth=500&format=json"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            page = list(data.get('query', {}).get('pages', {}).values())[0]
            ii = page.get('imageinfo', [{}])[0]
            thumb_url = ii.get('thumburl')
            if not thumb_url:
                print(f"No thumburl for {commons_file_title}")
                return None
            
            if '?' in thumb_url:
                thumb_clean = thumb_url.split('?')[0]
            else:
                thumb_clean = thumb_url
                
            img_req = urllib.request.Request(thumb_clean, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(img_req) as img_resp:
                img_bytes = img_resp.read()
                out_path = os.path.join(out_dir, local_filename)
                with open(out_path, 'wb') as f:
                    f.write(img_bytes)
                print(f"Saved local image {local_filename}: {len(img_bytes)} bytes")
                return f"images/{local_filename}"
    except Exception as e:
        print(f"Download error {commons_file_title}: {e}")
        return None

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    images_dir = os.path.join(base_dir, "images")
    data_file = os.path.join(base_dir, "data", "engravings.json")
    
    os.makedirs(images_dir, exist_ok=True)
    
    with open(data_file, 'r', encoding='utf-8') as f:
        database = json.load(f)
        
    print(f"Цяперашняя колькасць у базе: {len(database)}")
    
    # Новыя аб'екты для аналізу і дадання
    new_candidates = [
        {
            "id": "vilnius-braun-1581",
            "city_search": "Вільня",
            "title": "Панарама Вільні (Браўн і Хогенберг, 1581)",
            "original_title": "Vilna Lituaniae metropolis",
            "commons_title": "File:Civitates orbis terrarum, 1581. Vilna. 27 die dir garde.jpg",
            "local_img": "vilnius-braun-1581.jpg",
            "year": 1581,
            "century": 16,
            "artist": "Георг Браўн і Франц Хогенберг",
            "publisher": "Braun & Hogenberg (Cologne)",
            "album": "Civitates Orbis Terrarum (Vol. III)",
            "status": "authentic",
            "status_label": "Аўтэнтычная выява",
            "description": "Першая класічная еўрапейская панарама сталіцы Вялікага Княства Літоўскага. Падрабязна паказаны Верхні і Ніжні замкі, кафедральны сабор, ратуша і шматлікія храмы Вільні."
        },
        {
            "id": "nesvizh-makowski-1604",
            "city_search": "Нясвіж",
            "title": "План і замак у Нясвіжы (Тамаш Макоўскі)",
            "original_title": "Niesvisium",
            "commons_title": "File:Niasvizh Makouski.jpg",
            "local_img": "nesvizh-makowski-1604.jpg",
            "year": 1604,
            "century": 17,
            "artist": "Тамаш Макоўскі",
            "publisher": "Нясвіжская друкарня Радзівілаў",
            "album": "Асобная гравюра Радзівілаўскага кола",
            "status": "authentic",
            "status_label": "Аўтэнтычная выява",
            "description": "Выдатная рэнесансная гравюра Тамаша Макоўскага з выявай новай бастыённай фартэцыі Радзівілаў у Нясвіжы, ратушы і езуіцкага касцёла Божага Цела."
        },
        {
            "id": "smolensk-hondius-1636",
            "city_search": "Смаленск",
            "title": "Аблога Смаленска 1632–1634 гг. (Вільгельм Гондыус)",
            "original_title": "Smolenscum",
            "commons_title": "File:Smolensk-1632-1634.jpg",
            "local_img": "smolensk-hondius-1636.jpg",
            "year": 1636,
            "century": 17,
            "artist": "Вільгельм Гондыус (Wilhelm Hondius)",
            "publisher": "Wilhelm Hondius (Danzig)",
            "album": "Грандыёзны 16-аркушны план Смаленскай вайны",
            "status": "authentic",
            "status_label": "Аўтэнтычная выява",
            "description": "Манументальная гравюра вядомага галандска-гданьскага майстра Вільгельма Гондыуса, прысвечаная перамозе Уладзіслава IV пад Смаленскам. Надзвычайная тапаграфічная дакладнасць сцен, вежаў і Дняпра."
        }
    ]
    
    # Абнавіць існыя запісы QID і дадаць новыя
    existing_ids = {e['id']: e for e in database}
    
    # Дадаем Wikidata QID да старых запісаў
    wikidata_cache = {
        "Магілёў": "Q154835",
        "Гродна": "Q181385",
        "Полацк": "Q180744",
        "Брэст": "Q140147",
        "Гюстраў": "Q16147",
        "Гюстраў (Güstrow)": "Q16147"
    }
    
    for item in database:
        c_name = item['claimed_location']['name']
        if c_name in wikidata_cache:
            item['claimed_location']['wikidata'] = wikidata_cache[c_name]
            
    for cand in new_candidates:
        if cand['id'] in existing_ids:
            continue
            
        print(f"\n--- Аналіз: {cand['title']} ---")
        w_info = get_wikidata_info(cand['city_search'])
        time.sleep(0.5)
        
        if not w_info or not w_info.get('lat'):
            print(f"Не атрымалася знайсці каардынаты для {cand['city_search']}")
            continue
            
        print(f"Знойдзена ў Вікіданых: {w_info['name']} ({w_info['qid']}) -> {w_info['lat']}, {w_info['lng']}")
        
        local_path = download_commons_thumbnail(cand['commons_title'], cand['local_img'], images_dir)
        time.sleep(1)
        
        if not local_path:
            print(f"Не атрымалася спампаваць выяву для {cand['commons_title']}")
            continue
            
        new_entry = {
            "id": cand['id'],
            "title": cand['title'],
            "original_title": cand['original_title'],
            "status": cand['status'],
            "status_label": cand['status_label'],
            "claimed_location": {
                "name": w_info['name'],
                "wikidata": w_info['qid'],
                "lat": w_info['lat'],
                "lng": w_info['lng']
            },
            "actual_location": {
                "name": w_info['name'],
                "wikidata": w_info['qid'],
                "lat": w_info['lat'],
                "lng": w_info['lng']
            },
            "year": cand['year'],
            "century": cand['century'],
            "artist": cand['artist'],
            "publisher": cand['publisher'],
            "album": cand['album'],
            "commons_url": f"https://commons.wikimedia.org/wiki/{urllib.parse.quote(cand['commons_title'])}",
            "image_url": local_path,
            "description": cand['description']
        }
        
        database.append(new_entry)
        print(f"Дададзена ў базу: {cand['id']}")
        
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(database, f, ensure_ascii=False, indent=2)
        
    print(f"\nУсяго запісаў у абноўленай базе: {len(database)}")

if __name__ == '__main__':
    main()
