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

def get_commons_file_info(title):
    url = f"https://commons.wikimedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}&prop=imageinfo&iiprop=url|size|extmetadata&iiurlwidth=500&format=json"
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
                    'url': ii.get('url'),
                    'page_url': f"https://commons.wikimedia.org/wiki/{urllib.parse.quote(title)}"
                }
    except Exception as e:
        print(f"Error fetching {title}: {e}")
    return {'ok': False}

def download_image(url, filename):
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
        print(f"Error downloading {filename} from {url}: {e}")
        return None

new_panoramas = [
    {
        "id": "smederevo-peeters-1686",
        "title": "Панарама крэпасці Смедэрэва (Якаб Пеэтэрс, 1686)",
        "original_title": "Sendrae (Jacob Peeters)",
        "view_type": "panorama",
        "commons_file": "File:Sendrae - Peeters Jacob - 1686.jpg",
        "local_img": "smederevo-peeters-1686.jpg",
        "year": 1686,
        "century": 17,
        "artist": "Якаб Пеэтэрс (Jacob Peeters)",
        "publisher": "Jacob Peeters (Antwerpen)",
        "album": "Description des principales villes... sous la domination du Grand Turc",
        "status": "authentic",
        "status_label": "Аўтэнтычная панарама",
        "location": {
            "name": "Смедэрэва (Sendrae)",
            "wikidata": "Q190774",
            "lat": 44.6633,
            "lng": 20.9289
        },
        "description": "Рэдкая медзярэзная панарама Смедэрэўскай фартэцыі над Дунаем часоў асманскага панавання. Паказаны велічныя вежы дэспата Бранкавіча, рачныя судны і прырэчныя ўмацаванні."
    },
    {
        "id": "timisoara-peeters-1686",
        "title": "Панарама фартэцыі Тэмешвар (Якаб Пеэтэрс, 1686)",
        "original_title": "Temeswar (Jacob Peeters)",
        "view_type": "panorama",
        "commons_file": "File:Temeswar - Peeters Jacob - 1686.jpg",
        "local_img": "timisoara-peeters-1686.jpg",
        "year": 1686,
        "century": 17,
        "artist": "Якаб Пеэтэрс (Jacob Peeters)",
        "publisher": "Jacob Peeters (Antwerpen)",
        "album": "Description des principales villes... sous la domination du Grand Turc",
        "status": "authentic",
        "status_label": "Аўтэнтычная панарама",
        "location": {
            "name": "Тымішаара (Temeswar)",
            "wikidata": "Q83404",
            "lat": 45.7597,
            "lng": 21.2300
        },
        "description": "Панарамны від сталіцы Баната — турэцкага эялета Тэмешвар: бастыёны, мінарэты мячэцей, водаправодныя збудаванні на рацэ Бега і турэцкі гарнізон."
    },
    {
        "id": "kanizsa-peeters-1686",
        "title": "Панарама воднай крэпасці Каніжа (Якаб Пеэтэрс, 1686)",
        "original_title": "Canisia (Jacob Peeters)",
        "view_type": "panorama",
        "commons_file": "File:Canisia - Peeters Jacob - 1686.jpg",
        "local_img": "kanizsa-peeters-1686.jpg",
        "year": 1686,
        "century": 17,
        "artist": "Якаб Пеэтэрс (Jacob Peeters)",
        "publisher": "Jacob Peeters (Antwerpen)",
        "album": "Description des principales villes... sous la domination du Grand Turc",
        "status": "authentic",
        "status_label": "Аўтэнтычная панарама",
        "location": {
            "name": "Надзьканіжа (Canisia)",
            "wikidata": "Q14424",
            "lat": 46.4558,
            "lng": 16.9975
        },
        "description": "Панарама знакамітай асманскай цвярдыні Каніжа сярод непраходных балот: паказаны масты, бастыёны і вежы ключавой памежнай крэпасці паўднёва-заходняга фронту."
    },
    {
        "id": "szeged-peeters-1686",
        "title": "Панарама крэпасці Сегед на Цісе (Якаб Пеэтэрс, 1686)",
        "original_title": "Segedin (Jacob Peeters)",
        "view_type": "panorama",
        "commons_file": "File:Segedin - Peeters Jacob - 1686.jpg",
        "local_img": "szeged-peeters-1686.jpg",
        "year": 1686,
        "century": 17,
        "artist": "Якаб Пеэтэрс (Jacob Peeters)",
        "publisher": "Jacob Peeters (Antwerpen)",
        "album": "Description des principales villes... sous la domination du Grand Turc",
        "status": "authentic",
        "status_label": "Аўтэнтычная панарама",
        "location": {
            "name": "Сегед (Segedin)",
            "wikidata": "Q81581",
            "lat": 46.2500,
            "lng": 20.1667
        },
        "description": "Перспектыўны від турэцкага Сегеда з боку ракі Ціса: мураваны замак, мячэці з паўмесяцамі і рачныя прыстані напярэдадні вызвалення 1686 года."
    },
    {
        "id": "varad-peeters-1686",
        "title": "Панарама крэпасці Варадзін / Арадзя (Якаб Пеэтэрс, 1686)",
        "original_title": "Waradin (Jacob Peeters)",
        "view_type": "panorama",
        "commons_file": "File:Waradin - Peeters Jacob - 1686.jpg",
        "local_img": "varad-peeters-1686.jpg",
        "year": 1686,
        "century": 17,
        "artist": "Якаб Пеэтэрс (Jacob Peeters)",
        "publisher": "Jacob Peeters (Antwerpen)",
        "album": "Description des principales villes... sous la domination du Grand Turc",
        "status": "authentic",
        "status_label": "Аўтэнтычная панарама",
        "location": {
            "name": "Арадзя / Надьварад (Waradin)",
            "wikidata": "Q93358",
            "lat": 47.0722,
            "lng": 21.9211
        },
        "description": "Маляўнічая панарама пяцікутнага бастыённага замка Вялікага Варадзіна (Nagyvárad / Oradea), важнага фарпоста на мяжы Трансільваніі і асманскіх уладанняў."
    },
    {
        "id": "buda-peeters-1686",
        "title": "Панарама Афена / Буды з Дуная (Якаб Пеэтэрс, 1686)",
        "original_title": "Buda (Jacob Peeters)",
        "view_type": "panorama",
        "commons_file": "File:Buda - Peeters Jacob - 1686.jpg",
        "local_img": "buda-peeters-1686.jpg",
        "year": 1686,
        "century": 17,
        "artist": "Якаб Пеэтэрс (Jacob Peeters)",
        "publisher": "Jacob Peeters (Antwerpen)",
        "album": "Description des principales villes... sous la domination du Grand Turc",
        "status": "authentic",
        "status_label": "Аўтэнтычная панарама",
        "location": {
            "name": "Буда (Будапешт)",
            "wikidata": "Q1781",
            "lat": 47.4983,
            "lng": 19.0408
        },
        "description": "Антверпенскі медзярэз з панарамай каралеўскага замка на Будайскай гары, габрэйскага і турэцкага кварталаў і рачной пераправы ў Пешт падчас асманскага валадарства."
    },
    {
        "id": "buda-pest-hoefnagel-1617",
        "title": "Грандыёзная панарама Буды і Пешта (Георг Хёфнагель, 1617)",
        "original_title": "Buda Citerioris Hungariae Caput Regni avita sedes. vulgo Ofen 1617",
        "view_type": "panorama",
        "commons_file": "File:Buda Citerioris Hungariae Caput Regni avita sedes. vulgo Ofen 1617.jpg",
        "local_img": "buda-pest-hoefnagel-1617.jpg",
        "year": 1617,
        "century": 17,
        "artist": "Георг Хёфнагель (Georg Hoefnagel)",
        "publisher": "Braun & Hogenberg (Köln)",
        "album": "Civitates Orbis Terrarum (Vol. VI)",
        "status": "authentic",
        "status_label": "Аўтэнтычная панарама",
        "location": {
            "name": "Буда і Пешт",
            "wikidata": "Q1781",
            "lat": 47.4870,
            "lng": 19.0550
        },
        "description": "Адна з найвялікшых рэнесансных панарам Еўропы: від Буды і Пешта з гары Гелерт, падрабязна паказаны каралеўскі палац, лазні Рудаш, мячэці і постаці венграў і туркаў на пярэднім плане."
    },
    {
        "id": "gyor-peeters-1686",
        "title": "Панарама фартэцыі Дзьёр / Рааб (Якаб Пеэтэрс, 1686)",
        "original_title": "Raab (Jacob Peeters)",
        "view_type": "panorama",
        "commons_file": "File:Raab - Peeters Jacob - 1686.jpg",
        "local_img": "gyor-peeters-1686.jpg",
        "year": 1686,
        "century": 17,
        "artist": "Якаб Пеэтэрс (Jacob Peeters)",
        "publisher": "Jacob Peeters (Antwerpen)",
        "album": "Description des principales villes... sous la domination du Grand Turc",
        "status": "authentic",
        "status_label": "Аўтэнтычная панарама",
        "location": {
            "name": "Дзьёр (Raab)",
            "wikidata": "Q134494",
            "lat": 47.6841,
            "lng": 17.6344
        },
        "description": "Панарама «Шчыта Вены» — бастыённай крэпасці Дзьёр (Яўрын / Рааб) на зліцці рэк Раба і Мошанскага Дуная, цэнтра зацятай барацьбы Габсбургаў і асманаў."
    },
    {
        "id": "esztergom-hoefnagel-1595",
        "title": "Панарама Эстэргама і Паркані (Георг Хёфнагель, 1595)",
        "original_title": "Gran (Esztergom) et Párkány (Hoefnagel 1595)",
        "view_type": "panorama",
        "commons_file": "File:Jacob Hoefnagel Esztergom 1595.jpg",
        "local_img": "esztergom-hoefnagel-1595.jpg",
        "year": 1595,
        "century": 16,
        "artist": "Георг і Якаб Хёфнагель (Georg & Jacob Hoefnagel)",
        "publisher": "Braun & Hogenberg (Köln)",
        "album": "Civitates Orbis Terrarum",
        "status": "authentic",
        "status_label": "Аўтэнтычная панарама",
        "location": {
            "name": "Эстэргам (Gran)",
            "wikidata": "Q171353",
            "lat": 47.7856,
            "lng": 18.7403
        },
        "description": "Шэдэўр еўрапейскай ведуты: панарама замкавай гары Эстэргама над Дунаем і асманскага фарпоста Паркані (Штурава) падчас славутай аблогі 1595 года."
    },
    {
        "id": "komarno-peeters-1686",
        "title": "Панарама фартэцыі Комарна (Якаб Пеэтэрс, 1686)",
        "original_title": "Komara (Jacob Peeters)",
        "view_type": "panorama",
        "commons_file": "File:Komara - Peeters Jacob - 1686.jpg",
        "local_img": "komarno-peeters-1686.jpg",
        "year": 1686,
        "century": 17,
        "artist": "Якаб Пеэтэрс (Jacob Peeters)",
        "publisher": "Jacob Peeters (Antwerpen)",
        "album": "Description des principales villes... sous la domination du Grand Turc",
        "status": "authentic",
        "status_label": "Аўтэнтычная панарама",
        "location": {
            "name": "Комарна (Komorn)",
            "wikidata": "Q210796",
            "lat": 47.7633,
            "lng": 18.1283
        },
        "description": "Панарама дунайскай цвярдыні Комарна: Стары і Новы замкі на стрэлцы рэк Ваг і Дунай, якія туркі беспаспяхова спрабавалі ўзяць падчас некалькіх паходаў."
    },
    {
        "id": "vac-peeters-1686",
        "title": "Панарама горада і крэпасці Вац (Якаб Пеэтэрс, 1686)",
        "original_title": "Waitzen vulgo Vacia (Jacob Peeters)",
        "view_type": "panorama",
        "commons_file": "File:Waitzen vulgo Vacia - Peeters Jacob - 1686.jpg",
        "local_img": "vac-peeters-1686.jpg",
        "year": 1686,
        "century": 17,
        "artist": "Якаб Пеэтэрс (Jacob Peeters)",
        "publisher": "Jacob Peeters (Antwerpen)",
        "album": "Description des principales villes... sous la domination du Grand Turc",
        "status": "authentic",
        "status_label": "Аўтэнтычная панарама",
        "location": {
            "name": "Вац (Waitzen)",
            "wikidata": "Q207408",
            "lat": 47.7753,
            "lng": 19.1311
        },
        "description": "Панарама горада Вац у лукавіне Дуная пад асманскай уладай: сабор, вежы, прыбярэжныя ўмацаванні і ландшафт Дунайскага павароту."
    },
    {
        "id": "eger-peeters-1686",
        "title": "Панарама замка Эгер (Якаб Пеэтэрс, 1686)",
        "original_title": "Erla (Jacob Peeters)",
        "view_type": "panorama",
        "commons_file": "File:Erla - Peeters Jacob - 1686.jpg",
        "local_img": "eger-peeters-1686.jpg",
        "year": 1686,
        "century": 17,
        "artist": "Якаб Пеэтэрс (Jacob Peeters)",
        "publisher": "Jacob Peeters (Antwerpen)",
        "album": "Description des principales villes... sous la domination du Grand Turc",
        "status": "authentic",
        "status_label": "Аўтэнтычная панарама",
        "location": {
            "name": "Эгер (Erlau)",
            "wikidata": "Q168342",
            "lat": 47.9025,
            "lng": 20.3772
        },
        "description": "Панарама знакамітага Эгерскага замка, праслаўленага абаронай Іштвана Доба 1552 г., а затым пераўтворанага ў цэнтр самага паўночнага асманскага вілаета з мінарэтам і цытадэллю."
    },
    {
        "id": "szigetvar-peeters-1686",
        "title": "Панарама фартэцыі Сігетвар (Якаб Пеэтэрс, 1686)",
        "original_title": "Zieget (Jacob Peeters)",
        "view_type": "panorama",
        "commons_file": "File:Zieget - Peeters Jacob - 1686.jpg",
        "local_img": "szigetvar-peeters-1686.jpg",
        "year": 1686,
        "century": 17,
        "artist": "Якаб Пеэтэрс (Jacob Peeters)",
        "publisher": "Jacob Peeters (Antwerpen)",
        "album": "Description des principales villes... sous la domination du Grand Turc",
        "status": "authentic",
        "status_label": "Аўтэнтычная панарама",
        "location": {
            "name": "Сігетвар (Szigetvár)",
            "wikidata": "Q373542",
            "lat": 46.0475,
            "lng": 17.7994
        },
        "description": "Панарама легендарнай астраўной крэпасці Сігетвар, пад сценамі якой у 1566 годзе памёр султан Сулейман Пышны падчас гераічнай абароны Міклаша Зрыні."
    },
    {
        "id": "szolnok-peeters-1686",
        "title": "Панарама крэпасці Сольнак (Якаб Пеэтэрс, 1686)",
        "original_title": "Solnock (Jacob Peeters)",
        "view_type": "panorama",
        "commons_file": "File:Solnock - Peeters Jacob - 1686.jpg",
        "local_img": "szolnok-peeters-1686.jpg",
        "year": 1686,
        "century": 17,
        "artist": "Якаб Пеэтэрс (Jacob Peeters)",
        "publisher": "Jacob Peeters (Antwerpen)",
        "album": "Description des principales villes... sous la domination du Grand Turc",
        "status": "authentic",
        "status_label": "Аўтэнтычная панарама",
        "location": {
            "name": "Сольнак (Solnock)",
            "wikidata": "Q181276",
            "lat": 47.1747,
            "lng": 20.1764
        },
        "description": "Панарама замка Сольнак на зліцці Цісы і Задзівы: важны асманскі стратэгічны пункт кантролю над рачнымі шляхамі і салянымі караванамі."
    },
    {
        "id": "kostajnica-peeters-1686",
        "title": "Панарама замка Кастайніца на рацэ Уна (Якаб Пеэтэрс, 1686)",
        "original_title": "Castanowiz (Jacob Peeters)",
        "view_type": "panorama",
        "commons_file": "File:Castanowiz - Peeters Jacob - 1686.jpg",
        "local_img": "kostajnica-peeters-1686.jpg",
        "year": 1686,
        "century": 17,
        "artist": "Якаб Пеэтэрс (Jacob Peeters)",
        "publisher": "Jacob Peeters (Antwerpen)",
        "album": "Description des principales villes... sous la domination du Grand Turc",
        "status": "authentic",
        "status_label": "Аўтэнтычная панарама",
        "location": {
            "name": "Кастайніца (Kostajnica)",
            "wikidata": "Q396575",
            "lat": 45.2333,
            "lng": 16.5333
        },
        "description": "Панарама замка Кастайніца на рацэ Уна — ключавога ўмацавання Харвацкай ваеннай мяжы (Vojna Krajina) на памежжы з Босніяй."
    },
    {
        "id": "veszprem-peeters-1686",
        "title": "Панарама замка Веспрэм (Якаб Пеэтэрс, 1686)",
        "original_title": "Vesprin (Jacob Peeters)",
        "view_type": "panorama",
        "commons_file": "File:Vesprin - Peeters Jacob - 1686.jpg",
        "local_img": "veszprem-peeters-1686.jpg",
        "year": 1686,
        "century": 17,
        "artist": "Якаб Пеэтэрс (Jacob Peeters)",
        "publisher": "Jacob Peeters (Antwerpen)",
        "album": "Description des principales villes... sous la domination du Grand Turc",
        "status": "authentic",
        "status_label": "Аўтэнтычная панарама",
        "location": {
            "name": "Веспрэм (Veszprém)",
            "wikidata": "Q146317",
            "lat": 47.1000,
            "lng": 17.9167
        },
        "description": "Панарама старажытнага замка каралеў Веспрэм на высокай скале на поўнач ад Балатона, неаднаразова пераходзіўшага з рук у рукі паміж туркамі і хрысціянамі."
    },
    {
        "id": "varpalota-peeters-1686",
        "title": "Панарама крэпасці Варпалата (Якаб Пеэтэрс, 1686)",
        "original_title": "Palotta (Jacob Peeters)",
        "view_type": "panorama",
        "commons_file": "File:Palotta - Peeters Jacob - 1686.jpg",
        "local_img": "varpalota-peeters-1686.jpg",
        "year": 1686,
        "century": 17,
        "artist": "Якаб Пеэтэрс (Jacob Peeters)",
        "publisher": "Jacob Peeters (Antwerpen)",
        "album": "Description des principales villes... sous la domination du Grand Turc",
        "status": "authentic",
        "status_label": "Аўтэнтычная панарама",
        "location": {
            "name": "Варпалата (Palota)",
            "wikidata": "Q755681",
            "lat": 47.1972,
            "lng": 18.1394
        },
        "description": "Панарама замка Палата — знакамітага фарпоста капітана Дзьёрдзя Туры, які вытрымліваў найцяжэйшыя асманскія аблогі ў XVI стагоддзі."
    },
    {
        "id": "gyula-peeters-1686",
        "title": "Панарама мураванай цвярдыні Дзьюла (Якаб Пеэтэрс, 1686)",
        "original_title": "Giula (Jacob Peeters)",
        "view_type": "panorama",
        "commons_file": "File:Giula - Peeters Jacob - 1686.jpg",
        "local_img": "gyula-peeters-1686.jpg",
        "year": 1686,
        "century": 17,
        "artist": "Якаб Пеэтэрс (Jacob Peeters)",
        "publisher": "Jacob Peeters (Antwerpen)",
        "album": "Description des principales villes... sous la domination du Grand Turc",
        "status": "authentic",
        "status_label": "Аўтэнтычная панарама",
        "location": {
            "name": "Дзьюла (Gyula)",
            "wikidata": "Q214938",
            "lat": 46.6500,
            "lng": 21.2828
        },
        "description": "Панарама адзінай захаванай цаглянай готыка-рэнесанснай крэпасці Цэнтральнай Еўропы на рацэ Кёрэш, цэнтра асманскага санджака на працягу 129 гадоў."
    },
    {
        "id": "pecs-peeters-1686",
        "title": "Панарама горада Печ / Фюнфкірхен (Якаб Пеэтэрс, 1686)",
        "original_title": "Funfkirchen (Jacob Peeters)",
        "view_type": "panorama",
        "commons_file": "File:Funfkirchen - Peeters Jacob - 1686.jpg",
        "local_img": "pecs-peeters-1686.jpg",
        "year": 1686,
        "century": 17,
        "artist": "Якаб Пеэтэрс (Jacob Peeters)",
        "publisher": "Jacob Peeters (Antwerpen)",
        "album": "Description des principales villes... sous la domination du Grand Turc",
        "status": "authentic",
        "status_label": "Аўтэнтычная панарама",
        "location": {
            "name": "Печ (Fünfkirchen)",
            "wikidata": "Q45779",
            "lat": 46.0708,
            "lng": 18.2331
        },
        "description": "Панарама паўднёвавенгерскага горада Печ ля падножжа гары Мечэк: відаць мінарэты і купалы знакамітай мячэці пашы Касіма, гарадскія муры і вінаграднікі."
    },
    {
        "id": "trnava-peeters-1686",
        "title": "Панарама горада Трнава (Якаб Пеэтэрс, 1686)",
        "original_title": "Tyrnavia vulgo Dyrna (Jacob Peeters)",
        "view_type": "panorama",
        "commons_file": "File:Tyrnavia vulgo Dyrna - Peeters Jacob - 1686.jpg",
        "local_img": "trnava-peeters-1686.jpg",
        "year": 1686,
        "century": 17,
        "artist": "Якаб Пеэтэрс (Jacob Peeters)",
        "publisher": "Jacob Peeters (Antwerpen)",
        "album": "Description des principales villes... sous la domination du Grand Turc",
        "status": "authentic",
        "status_label": "Аўтэнтычная панарама",
        "location": {
            "name": "Трнава (Tyrnavia)",
            "wikidata": "Q26175",
            "lat": 48.3778,
            "lng": 17.5862
        },
        "description": "Панарама «Славацкага Рыма» — мураванага горада Трнава з яго вежамі і касцёламі, куды пасля падзення Эстэргама перайшла рэзідэнцыя венгерскіх архібіскупаў."
    }
]

print(f"Processing and downloading {len(new_panoramas)} historical panoramas...")

with open(data_file, 'r', encoding='utf-8') as f:
    existing_db = json.load(f)

# Tag existing items with view_type
for item in existing_db:
    if 'view_type' not in item:
        # If title or description has 'план', it's plan; otherwise panorama
        t = item['title'].lower()
        if 'план' in t or 'карта' in t or 'штурм' in t:
            item['view_type'] = 'plan'
        else:
            item['view_type'] = 'panorama'

existing_ids = {item['id'] for item in existing_db}

added_count = 0
for entry in new_panoramas:
    commons_file = entry['commons_file']
    local_filename = entry['local_img']
    info = get_commons_file_info(commons_file)
    if not info.get('ok'):
        print(f"FAILED commons info: {commons_file}")
        continue
    
    thumburl = info['thumburl']
    local_path = download_image(thumburl, local_filename)
    if not local_path:
        print(f"FAILED download: {local_filename}")
        continue
        
    db_item = {
        "id": entry["id"],
        "title": entry["title"],
        "original_title": entry["original_title"],
        "view_type": entry["view_type"],
        "status": entry["status"],
        "status_label": entry["status_label"],
        "claimed_location": {
            "name": entry["location"]["name"],
            "lat": entry["location"]["lat"],
            "lng": entry["location"]["lng"],
            "wikidata": entry["location"]["wikidata"]
        },
        "actual_location": {
            "name": entry["location"]["name"],
            "lat": entry["location"]["lat"],
            "lng": entry["location"]["lng"],
            "wikidata": entry["location"]["wikidata"]
        },
        "year": entry["year"],
        "century": entry["century"],
        "artist": entry["artist"],
        "publisher": entry["publisher"],
        "album": entry["album"],
        "commons_url": info["page_url"],
        "image_url": local_path,
        "description": entry["description"]
    }
    
    if entry["id"] in existing_ids:
        # replace
        existing_db = [db_item if x['id'] == entry['id'] else x for x in existing_db]
    else:
        # add at beginning of frontier
        existing_db.insert(0, db_item)
        added_count += 1

print(f"\nAdded/updated {added_count} panoramas. Total database size now: {len(existing_db)}")

with open(data_file, 'w', encoding='utf-8') as f:
    json.dump(existing_db, f, ensure_ascii=False, indent=2)

print("Database updated successfully!")
