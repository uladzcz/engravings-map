import urllib.request
import urllib.parse
import json
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {'User-Agent': 'EngravingsMapBot/1.0 (cultural-heritage research; contact: uladzcz@github.com)'}

base_dir = r"C:\Users\bafur\.gemini\antigravity\scratch\engravings-map"
images_dir = os.path.join(base_dir, "images")
data_file = os.path.join(base_dir, "data", "engravings.json")

def lookup_place(name):
    url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={urllib.parse.quote(name)}&language=en&format=json"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req) as resp:
        d = json.loads(resp.read().decode('utf-8'))
        for item in d.get('search', [])[:5]:
            qid = item['id']
            e_url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={qid}&props=claims|labels&languages=en|be&format=json"
            req2 = urllib.request.Request(e_url, headers=HEADERS)
            with urllib.request.urlopen(req2) as resp2:
                ed = json.loads(resp2.read().decode('utf-8'))
                ent = ed.get('entities', {}).get(qid, {})
                claims = ent.get('claims', {})
                coords = claims.get('P625', [{}])[0].get('mainsnak', {}).get('datavalue', {}).get('value', {})
                lat = coords.get('latitude')
                lng = coords.get('longitude')
                desc = item.get('description', '').lower()
                if lat is not None and any(w in desc for w in ['city', 'town', 'municipality', 'county', 'settlement', 'capital', 'hungary', 'serbia', 'croatia', 'slovakia', 'romania', 'greece', 'turkey']):
                    be_l = ent.get('labels', {}).get('be', {}).get('value')
                    en_l = ent.get('labels', {}).get('en', {}).get('value')
                    return {
                        'qid': qid,
                        'name_en': en_l or name,
                        'name_be': be_l or en_l or name,
                        'lat': lat,
                        'lng': lng
                    }
    return None

def get_commons_info(title):
    url = f"https://commons.wikimedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}&prop=imageinfo&iiprop=url|size&iiurlwidth=500&format=json"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            pages = data.get('query', {}).get('pages', {})
            page = list(pages.values())[0]
            if 'imageinfo' in page and page['imageinfo']:
                ii = page['imageinfo'][0]
                return {
                    'ok': True,
                    'thumburl': ii.get('thumburl'),
                    'page_url': f"https://commons.wikimedia.org/wiki/{urllib.parse.quote(title)}"
                }
    except Exception as e:
        print(f"Error fetching {title}: {e}")
    return {'ok': False}

def download_img(url, filename):
    out_path = os.path.join(images_dir, filename)
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
        return f"images/{filename}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read()
            with open(out_path, 'wb') as f:
                f.write(content)
            print(f"Downloaded {filename} ({len(content)} bytes)")
            return f"images/{filename}"
    except Exception as e:
        print(f"Error downloading {filename}: {e}")
        return None

batch_panoramas = [
    {
        "id": "bratislava-merian-1650",
        "search_city": "Bratislava",
        "title": "Панарама Прэсбурга / Браціславы на Дунаі (Маціяс Мерыян)",
        "original_title": "Topographia Posoniensis (Pressburg)",
        "commons_file": "File:Topographia Regiae Liberaeq. Civitatis Posoniensis vulgo Pressburg Hungariae Superioris ad Danubium sita cum adiacenti castro ubi sacra regni Hungariae coronoa conservatur - btv1b53194611s (1 of 2).jpg",
        "local_img": "bratislava-merian-1650.jpg",
        "year": 1650,
        "century": 17,
        "artist": "Маціяс Мерыян (Matthäus Merian)",
        "publisher": "Merian (Frankfurt am Main)",
        "album": "Topographia Hungariae",
        "description": "Класічная медзярэзная панарама каралеўскага замка і сталіцы Верхняй Венгрыі над Дунаем, дзе захоўвалася святая карона Венгрыі."
    },
    {
        "id": "visegrad-hoefnagel-1595",
        "search_city": "Visegrád",
        "title": "Панарама дунайскага замка Вішэград (Георг Хёфнагель, 1595)",
        "original_title": "Vizzegrad (Visegrád) - G. Hoefnagel 1595",
        "commons_file": "File:Vizzegrad-1595-by Hoefnagel.jpg",
        "local_img": "visegrad-hoefnagel-1595.jpg",
        "year": 1595,
        "century": 16,
        "artist": "Георг і Якаб Хёфнагель (Hoefnagel)",
        "publisher": "Braun & Hogenberg (Köln)",
        "album": "Civitates Orbis Terrarum (Vol. V)",
        "description": "Манументальная ведута стратэгічнага каралеўскага замка Вішэград у Дунайскім павароце, цэнтра пастаянных баёў часоў 15-гадовай вайны з асманамі."
    },
    {
        "id": "tata-hoefnagel-1595",
        "search_city": "Tata Hungary",
        "title": "Панарама воднай крэпасці Тата (Георг Хёфнагель, 1595)",
        "original_title": "Dotis (Tata) - Hoefnagel 1595",
        "commons_file": "File:Tata G Hoefnagel.jpg",
        "local_img": "tata-hoefnagel-1595.jpg",
        "year": 1595,
        "century": 16,
        "artist": "Георг Хёфнагель (Georg Hoefnagel)",
        "publisher": "Braun & Hogenberg (Köln)",
        "album": "Civitates Orbis Terrarum (Vol. VI)",
        "description": "Выдатны перспектыўны від замка і возера Тата, узятага штурмам хрысціянскімі войскамі пры дапамозе новай падрыўной петарды ў 1597 годзе."
    },
    {
        "id": "novi-zrin-peeters-1686",
        "search_city": "Legrad",
        "title": "Панарама крэпасці Новы Зрын / Зрынівар (Якаб Пеэтэрс, 1686)",
        "original_title": "Serinwar Zatmar (Jacob Peeters)",
        "commons_file": "File:Serinwar Zatmar - Peeters Jacob - 1686.jpg",
        "local_img": "novi-zrin-peeters-1686.jpg",
        "year": 1686,
        "century": 17,
        "artist": "Якаб Пеэтэрс (Jacob Peeters)",
        "publisher": "Jacob Peeters (Antwerpen)",
        "album": "Description des principales villes... sous la domination du Grand Turc",
        "description": "Панарама знакамітай фартыфікацыі Новы Зрын (Zrínyivár), збудаванай харвацкім банам Міклашам Зрыні на зліцці рэк Мура і Драва для стрымлівання турэцкіх паходаў."
    },
    {
        "id": "szatmar-peeters-1686",
        "search_city": "Satu Mare",
        "title": "Панарама фартэцыі Сатмар / Сату-Марэ (Якаб Пеэтэрс, 1686)",
        "original_title": "Sadtwaer Sacmar (Jacob Peeters)",
        "commons_file": "File:Sadtwaer Sacmar - Peeters Jacob - 1686.jpg",
        "local_img": "szatmar-peeters-1686.jpg",
        "year": 1686,
        "century": 17,
        "artist": "Якаб Пеэтэрс (Jacob Peeters)",
        "publisher": "Jacob Peeters (Antwerpen)",
        "album": "Description des principales villes... sous la domination du Grand Turc",
        "description": "Панарама бастыённага воднага замка Сатмар на рацэ Самош — важнага стратэгічнага цэнтра на мяжы Венгрыі і Парцыума."
    },
    {
        "id": "zsambek-peeters-1686",
        "search_city": "Zsámbék",
        "title": "Панарама замка і мястэчка Жамбек (Якаб Пеэтэрс, 1686)",
        "original_title": "Schombock (Jacob Peeters)",
        "commons_file": "File:Schombock - Peeters Jacob - 1686.jpg",
        "local_img": "zsambek-peeters-1686.jpg",
        "year": 1686,
        "century": 17,
        "artist": "Якаб Пеэтэрс (Jacob Peeters)",
        "publisher": "Jacob Peeters (Antwerpen)",
        "album": "Description des principales villes... sous la domination du Grand Turc",
        "description": "Панарама Жамбека з яго раманскім абацтвам, пераўтвораным туркамі ў крэпасць на падыходах да Буды."
    },
    {
        "id": "gussing-peeters-1686",
        "search_city": "Güssing",
        "title": "Панарама замка Гюсінг / Неметуйвар (Якаб Пеэтэрс, 1686)",
        "original_title": "Verebel Giszing (Jacob Peeters)",
        "commons_file": "File:Verebel Giszing - Peeters Jacob - 1686.jpg",
        "local_img": "gussing-peeters-1686.jpg",
        "year": 1686,
        "century": 17,
        "artist": "Якаб Пеэтэрс (Jacob Peeters)",
        "publisher": "Jacob Peeters (Antwerpen)",
        "album": "Description des principales villes... sous la domination du Grand Turc",
        "description": "Панарама магутнага замка Гюсінг на вяршыні патухлага вулкана — радавога гнязда Бацьяні і шчыта заходняга венгерскага памежжа."
    },
    {
        "id": "lefkada-peeters-1686",
        "search_city": "Lefkada",
        "title": "Панарама марской фартэцыі Санта-Маўра / Лефкада (Якаб Пеэтэрс, 1686)",
        "original_title": "Piazza di Sta Maura (Jacob Peeters)",
        "commons_file": "File:Piazza di Sta Maura - Peeters Jacob - 1686.jpg",
        "local_img": "lefkada-peeters-1686.jpg",
        "year": 1686,
        "century": 17,
        "artist": "Якаб Пеэтэрс (Jacob Peeters)",
        "publisher": "Jacob Peeters (Antwerpen)",
        "album": "Description des principales villes... sous la domination du Grand Turc",
        "description": "Перспектыўны від марской крэпасці Санта-Маўра (Лефкада) на Іанічным моры, захопленай венецыянскім флотам Маразіні ў 1684 годзе."
    },
    {
        "id": "koroni-peeters-1686",
        "search_city": "Koroni",
        "title": "Панарама крэпасці Кароні — «Вока Венецыі» (Якаб Пеэтэрс, 1686)",
        "original_title": "Coron (Jacob Peeters)",
        "commons_file": "File:Coron - Peeters Jacob - 1686.jpg",
        "local_img": "koroni-peeters-1686.jpg",
        "year": 1686,
        "century": 17,
        "artist": "Якаб Пеэтэрс (Jacob Peeters)",
        "publisher": "Jacob Peeters (Antwerpen)",
        "album": "Description des principales villes... sous la domination du Grand Turc",
        "description": "Панарама паўднёвабалканскай цвярдыні Кароні (Марэя), вядомай як «Вока Венецыі», цэнтра баёў Марэйскай вайны 1685 года."
    },
    {
        "id": "chania-peeters-1686",
        "search_city": "Chania",
        "title": "Панарама горада і порта Ханья (Якаб Пеэтэрс, 1686)",
        "original_title": "Canea in Candia (Jacob Peeters)",
        "commons_file": "File:Canea in Candia - Peeters Jacob - 1686.jpg",
        "local_img": "chania-peeters-1686.jpg",
        "year": 1686,
        "century": 17,
        "artist": "Якаб Пеэтэрс (Jacob Peeters)",
        "publisher": "Jacob Peeters (Antwerpen)",
        "album": "Description des principales villes... sous la domination du Grand Turc",
        "description": "Панарама бастыённага порта і крэпасці Ханья на Крыце, заваяванай асманамі пасля цяжкай аблогі 1645 года."
    },
    {
        "id": "dardanelles-peeters-1686",
        "search_city": "Çanakkale",
        "title": "Панарама замкаў праліва Дарданэлы (Якаб Пеэтэрс, 1686)",
        "original_title": "Gli Dardanelli (Jacob Peeters)",
        "commons_file": "File:Gli Dardanelli - Peeters Jacob - 1686.jpg",
        "local_img": "dardanelles-peeters-1686.jpg",
        "year": 1686,
        "century": 17,
        "artist": "Якаб Пеэтэрс (Jacob Peeters)",
        "publisher": "Jacob Peeters (Antwerpen)",
        "album": "Description des principales villes... sous la domination du Grand Turc",
        "description": "Маляўнічая панарама асманавых замкаў Сестус і Абідас (Кале-і Султаніе) на берагах Дарданэлаў з галернымі флатамі."
    },
    {
        "id": "constantinople-peeters-1686",
        "search_city": "Istanbul",
        "title": "Грандыёзная панарама Канстанцінопаля / Стамбула (Якаб Пеэтэрс, 1686)",
        "original_title": "Constantinopelen (Jacob Peeters)",
        "commons_file": "File:Constantinopelen - Peeters Jacob - 1686.jpg",
        "local_img": "constantinople-peeters-1686.jpg",
        "year": 1686,
        "century": 17,
        "artist": "Якаб Пеэтэрс (Jacob Peeters)",
        "publisher": "Jacob Peeters (Antwerpen)",
        "album": "Description des principales villes... sous la domination du Grand Turc",
        "description": "Шыкоўная панарама сталіцы Асманскай імперыі цераз бухту Залаты Рог: бачны мячэць Султанахмет, Сафійскі сабор, палац Тапкапы і сотні караблёў."
    }
]

print(f"Starting processing of {len(batch_panoramas)} new panoramas...")

with open(data_file, 'r', encoding='utf-8') as f:
    database = json.load(f)

existing_ids = {item['id'] for item in database}

added = 0
for p in batch_panoramas:
    place_info = lookup_place(p['search_city'])
    if not place_info:
        print(f"FAILED place lookup: {p['search_city']}")
        continue
        
    c_info = get_commons_info(p['commons_file'])
    if not c_info.get('ok'):
        print(f"FAILED commons info: {p['commons_file']}")
        continue
        
    local_path = download_img(c_info['thumburl'], p['local_img'])
    if not local_path:
        print(f"FAILED download: {p['local_img']}")
        continue
        
    db_item = {
        "id": p["id"],
        "title": p["title"],
        "original_title": p["original_title"],
        "view_type": "panorama",
        "status": "authentic",
        "status_label": "Аўтэнтычная панарама",
        "claimed_location": {
            "name": place_info["name_be"],
            "lat": place_info["lat"],
            "lng": place_info["lng"],
            "wikidata": place_info["qid"]
        },
        "actual_location": {
            "name": place_info["name_be"],
            "lat": place_info["lat"],
            "lng": place_info["lng"],
            "wikidata": place_info["qid"]
        },
        "year": p["year"],
        "century": p["century"],
        "artist": p["artist"],
        "publisher": p["publisher"],
        "album": p["album"],
        "commons_url": c_info["page_url"],
        "image_url": local_path,
        "description": p["description"]
    }
    
    if p["id"] in existing_ids:
        database = [db_item if x['id'] == p['id'] else x for x in database]
    else:
        database.insert(0, db_item)
        added += 1
    print(f"Added panorama: {p['id']} -> {place_info['name_be']} ({place_info['qid']})")

print(f"\nFinished! Added {added} panoramas. Total in database: {len(database)}")

with open(data_file, 'w', encoding='utf-8') as f:
    json.dump(database, f, ensure_ascii=False, indent=2)

print("Database updated!")
