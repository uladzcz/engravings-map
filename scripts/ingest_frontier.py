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

# List of Ottoman Frontier engravings and plans to integrate
frontier_entries = [
    # --- BELGRADE (Бялград / Belgrad / Singidunum) ---
    {
        "id": "belgrade-nypoort-1688",
        "title": "Аблога і штурм Бялграда 1688 г. (Юстус ван дэн Нейпарт)",
        "original_title": "Belgradum a Christianis expugnatum A. 1688",
        "commons_file": "File:Siege of Belgrád-1688-by Nypoort.jpg",
        "local_img": "belgrade-nypoort-1688.jpg",
        "year": 1688,
        "century": 17,
        "artist": "Юстус ван дэн Нейпарт (Justus van den Nypoort)",
        "publisher": "Wien / Frankfurt",
        "album": "Гістарычныя лісты Вялікай турэцкай вайны",
        "status": "authentic",
        "status_label": "Аўтэнтычная выява",
        "location": {
            "name": "Бялград (Калемегдан)",
            "wikidata": "Q3711",
            "lat": 44.8236,
            "lng": 20.4503
        },
        "description": "Манументальная гравюра фламандскага майстра Юстуса ван дэн Нейпарта з панарамай гераічнага штурму крэпасці Бялград войскамі курфюрста Максіміліяна Эмануэля Баварскага 6 верасня 1688 года."
    },
    {
        "id": "belgrade-leopold-1717",
        "title": "Перамога пры Бялградзе 1717 г. (Іаган Фрыдрых Леапольд)",
        "original_title": "Prospect und Belagerung der Haupt-Vestung Belgrad 1717",
        "commons_file": "File:Belgrad-1717-J-F-Leopold.jpg",
        "local_img": "belgrade-leopold-1717.jpg",
        "year": 1717,
        "century": 18,
        "artist": "Іаган Фрыдрых Леапольд (Johann Friedrich Leopold)",
        "publisher": "Johann Friedrich Leopold (Augsburg)",
        "album": "Аўгсбургскія ваенныя аркушы (Kriegs-Theatrum)",
        "status": "authentic",
        "status_label": "Аўтэнтычная выява",
        "location": {
            "name": "Бялград",
            "wikidata": "Q3711",
            "lat": 44.8200,
            "lng": 20.4530
        },
        "description": "Вядомая аўгсбургская гравюра з панарамай другой аблогі і разгрому турэцкай арміі прынцам Яўгенам Савойскім у 1717 годзе, з дэталёвым планам умацаванняў і батарэй на Дунаі і Саве."
    },
    {
        "id": "belgrade-peeters-1686",
        "title": "Від крэпасці Бялград (Якаб Пеэтэрс, 1686)",
        "original_title": "Belgrado (Jacob Peeters)",
        "commons_file": "File:Belgrado - Peeters Jacob - 1686.jpg",
        "local_img": "belgrade-peeters-1686.jpg",
        "year": 1686,
        "century": 17,
        "artist": "Якаб Пеэтэрс (Jacob Peeters)",
        "publisher": "Antwerpen",
        "album": "Description des principales villes... sous l'obéissance du Grand Turc",
        "status": "authentic",
        "status_label": "Аўтэнтычная выява",
        "location": {
            "name": "Бялград",
            "wikidata": "Q3711",
            "lat": 44.8236,
            "lng": 20.4503
        },
        "description": "Антверпенская медзярэзная панарама Бялграда з боку Дуная з выявай мінарэтаў, турэцкіх бастыёнаў і замка Калемегдан напярэдадні аўстрыйскай аблогі."
    },
    {
        "id": "belgrade-adlerschwung-1688",
        "title": "План і панарама аблогі Бялграда 1688 г. (Адлершвунг)",
        "original_title": "Belgrad 1688 von Adlerschwung",
        "commons_file": "File:Belgrad-1688-by Adlerschwung.jpg",
        "local_img": "belgrade-adlerschwung-1688.jpg",
        "year": 1688,
        "century": 17,
        "artist": "Франц Іаахім Адлершвунг (Adlerschwung)",
        "publisher": "Nürnberg",
        "album": "Theatrum Europaeum",
        "status": "authentic",
        "status_label": "Аўтэнтычная выява",
        "location": {
            "name": "Бялград",
            "wikidata": "Q3711",
            "lat": 44.8210,
            "lng": 20.4490
        },
        "description": "Нюрнбергская гравюра з сумеснай выявай тапаграфічнага плана аблогі 1688 г., размяшчэння баварскіх палкоў і перспектыўнага віду крэпасці."
    },
    {
        "id": "belgrade-weissenburg-1600",
        "title": "Бялград — «Грэчаскі Вейсэнбург» каля 1600 г.",
        "original_title": "Griechisch Weissenburg / Belgrad (c. 1600)",
        "commons_file": "File:Belgrade (Weissenburg) (1600).jpg",
        "local_img": "belgrade-weissenburg-1600.jpg",
        "year": 1600,
        "century": 16,
        "artist": "Невядомы майстар (кола Вільгельма Петэра Дыліха)",
        "publisher": "Frankfurt / Kassel",
        "album": "Ungarische Chronica",
        "status": "authentic",
        "status_label": "Аўтэнтычная выява",
        "location": {
            "name": "Бялград",
            "wikidata": "Q3711",
            "lat": 44.8250,
            "lng": 20.4510
        },
        "description": "Ранняя нямецкая гравюра рубяжа XVI–XVII стст., якая паказвае верхні і ніжні горад Бялграда пад уладай асманаў, зліццё рэк Савы і Дуная і караванныя шляхі."
    },
    {
        "id": "belgrade-griechisch-weissenburg-plan",
        "title": "План аблогі Бялграда: «Griechisch Weissenburg Belagert»",
        "original_title": "Griechisch Weissenburg Belagert",
        "commons_file": "File:GRIECHISCH WEISSENBURG BELAGERT.jpg",
        "local_img": "belgrade-griechisch-weissenburg-plan.jpg",
        "year": 1690,
        "century": 17,
        "artist": "Невядомы нямецкі ваенны інжынер",
        "publisher": "Augsburg / Nürnberg",
        "album": "Kriegs-Karten der Türkenkriege",
        "status": "authentic",
        "status_label": "Аўтэнтычная выява",
        "location": {
            "name": "Бялград",
            "wikidata": "Q3711",
            "lat": 44.8220,
            "lng": 20.4480
        },
        "description": "Медзярэзны ваенны план крэпасных збудаванняў Бялграда, рачных астравоў і ліній цыркумвалацыі падчас баёў за памежны вузел Сербіі."
    },

    # --- ZEMUN (Земун / Semlin) ---
    {
        "id": "semlin-zemun-1789",
        "title": "План горада і ўмацаванняў Зэмуна 1789 г. (Землін)",
        "original_title": "Plan der Stadt Semlin wie solche im Jahr 1789 bestanden ist",
        "commons_file": "File:Plan der Stadt Semlin wie solche im Jahr 789 mit ihren Verschanzungen und Retranchements bestanden ist (FL39696866 3705629).jpg",
        "local_img": "semlin-zemun-1789.jpg",
        "year": 1789,
        "century": 18,
        "artist": "Цэсарска-каралеўскія ваенныя картграфы",
        "publisher": "Wien (K.K. Militär-Ingenieure)",
        "album": "Karten der k.k. Militärgrenze",
        "status": "authentic",
        "status_label": "Аўтэнтычная выява",
        "location": {
            "name": "Земун (Semlin)",
            "wikidata": "Q189419",
            "lat": 44.8456,
            "lng": 20.4142
        },
        "description": "Падрабязнейшы ваенны план аўстрыйскага фарпоста Землін на супрацьлеглым ад Бялграда беразе Савы з бастыённымі рэтраншэментамі і каранцінным лагерам Вайсэнбургскай мяжы."
    },

    # --- SMEDEREVO (Смедэрэва / Semendria) ---
    {
        "id": "smederevo-siege-1693",
        "title": "Аблога Смедэрэўскай крэпасці 1693 г. (Семендрыя)",
        "original_title": "Imperial siege of Smederevo (Semendria), c. 1693",
        "commons_file": "File:Imperial siege of Smederevo (Semendria), c. 1693.jpg",
        "local_img": "smederevo-siege-1693.jpg",
        "year": 1693,
        "century": 17,
        "artist": "Невядомы імперскі гравёр",
        "publisher": "Wien / Nürnberg",
        "album": "Theatrum Europaeum",
        "status": "authentic",
        "status_label": "Аўтэнтычная выява",
        "location": {
            "name": "Смедэрэва (Semendria)",
            "wikidata": "Q190774",
            "lat": 44.6650,
            "lng": 20.9278
        },
        "description": "Гістарычная гравюра часоў Вялікай турэцкай вайны: магутная трохкутная сярэднявечная крэпасць дэспата Джураджа Бранкавіча на Дунаі, атакаваная імперскімі войскамі."
    },
    {
        "id": "smederevo-donau-ansicht",
        "title": "Горад і крэпасць Семендрыя на Дунаі",
        "original_title": "Donau-Ansichten: Türkei - Stadt und Festung Semendria",
        "commons_file": "File:Donau-Ansichten- Türkei- Stadt und Festung Semendria.jpg",
        "local_img": "smederevo-donau-ansicht.jpg",
        "year": 1790,
        "century": 18,
        "artist": "Невядомы мастак школы Донаў-панарам",
        "publisher": "Wien",
        "album": "Malerische Ansichten der Donau und des Orients",
        "status": "authentic",
        "status_label": "Аўтэнтычная выява",
        "location": {
            "name": "Смедэрэва",
            "wikidata": "Q190774",
            "lat": 44.6633,
            "lng": 20.9289
        },
        "description": "Рамантычны перспектыўны від Смедэрэўскага замка і вежаў над дунайскімі плёсамі на памежжы з Асманскай імперыяй."
    },

    # --- PETROVARADIN (Петварадын / Peterwardein) ---
    {
        "id": "petrovaradin-battle-1716",
        "title": "Бітва і фартэцыя Петварадын 1716 г.",
        "original_title": "Plan der Victoriosen Bataille bey Peterwardein 1716",
        "commons_file": "File:Battle-of-petrovaradin-map-1716.jpg",
        "local_img": "petrovaradin-battle-1716.jpg",
        "year": 1716,
        "century": 18,
        "artist": "Цэсарскія інжынеры (кола Габрыэля Бодэнера)",
        "publisher": "Augsburg / Nürnberg",
        "album": "Theatrum Belli in Hungaria",
        "status": "authentic",
        "status_label": "Аўтэнтычная выява",
        "location": {
            "name": "Петварадын (Гібралтар на Дунаі)",
            "wikidata": "Q19429",
            "lat": 45.2531,
            "lng": 19.8631
        },
        "description": "Гравіраваная карта грандыёзнай бітвы пры Петварадыне 5 жніўня 1716 г., дзе прынц Савойскі разграміў асманскую армію вялікага візіра Дамат Алі-пашы, а таксама план бастыённай цытадэлі."
    },
    {
        "id": "petrovaradin-prospect",
        "title": "Панарама фартэцыі Петварадын (Peterwardein)",
        "original_title": "Peterwardein an der Donau",
        "commons_file": "File:Petrovaradin BV044698772.jpg",
        "local_img": "petrovaradin-prospect.jpg",
        "year": 1720,
        "century": 18,
        "artist": "Невядомы нямецкі гравёр",
        "publisher": "Augsburg",
        "album": "Curioses Staats- und Kriegs-Theatrum",
        "status": "authentic",
        "status_label": "Аўтэнтычная выява",
        "location": {
            "name": "Петварадын",
            "wikidata": "Q19429",
            "lat": 45.2520,
            "lng": 19.8640
        },
        "description": "Перспектыўны від непрыступнай скальнай крэпасці Петварадын на Дунаі («Венгерскага Гібралтара») з пантонным мостам да Новага Сада."
    },

    # --- TIMIȘOARA (Тымішаара / Temeswar) ---
    {
        "id": "timisoara-bodenehr-1716",
        "title": "Аблога і крэпасць Тэмешвар 1716 г. (Габрыэль Бодэнер)",
        "original_title": "Temeswar. Im Bannat desselben Namens (Gabriel Bodenehr)",
        "commons_file": "File:Timisoara Temesvar Temeswar 1716 Gabriel Bodenehr.jpg",
        "local_img": "timisoara-bodenehr-1716.jpg",
        "year": 1716,
        "century": 18,
        "artist": "Габрыэль Бодэнер (Gabriel Bodenehr)",
        "publisher": "Gabriel Bodenehr (Augsburg)",
        "album": "Curioses Staats- und Kriegs-Theatrum in Ungarn",
        "status": "authentic",
        "status_label": "Аўтэнтычная выява",
        "location": {
            "name": "Тымішаара (Тэмешвар)",
            "wikidata": "Q83404",
            "lat": 45.7597,
            "lng": 21.2300
        },
        "description": "Выдатная гравюра Габрыэля Бодэнера: план і панарама сталіцы Баната Тэмешвара ў момант капітуляцыі турэцкага гарнізона перад войскамі прынца Савойскага ў 1716 годзе."
    },
    {
        "id": "timisoara-fortress-1788",
        "title": "Бастыённая крэпасць Тэмешвар у 1788 г.",
        "original_title": "The fortress of Temesvár in 1788",
        "commons_file": "File:The fortress of Temesvár in 1788.jpg",
        "local_img": "timisoara-fortress-1788.jpg",
        "year": 1788,
        "century": 18,
        "artist": "Венгерскія і аўстрыйскія ваенныя геадэзісты",
        "publisher": "Pest / Wien",
        "album": "Banater Festungs-Atlas",
        "status": "authentic",
        "status_label": "Аўтэнтычная выява",
        "location": {
            "name": "Тымішаара",
            "wikidata": "Q83404",
            "lat": 45.7537,
            "lng": 21.2257
        },
        "description": "Геаметрычны план адной з самых дасканалых зоркападобных фартэцый Габсбургскай манархіі на ўсходнім памежжы."
    },

    # --- VIDIN (Відзін / Widdin / Baba Vida) ---
    {
        "id": "vidin-baba-vida-1740",
        "title": "Відзін і замак Баба Віда каля 1740 г.",
        "original_title": "Plan der Stadt und Festung Widdin samt dem Schloss Baba Vida",
        "commons_file": "File:Ca. 1740 map of Vidin and the Baba Vida Fortress.jpg",
        "local_img": "vidin-baba-vida-1740.jpg",
        "year": 1740,
        "century": 18,
        "artist": "Нямецкі ваенны інжынер",
        "publisher": "Nürnberg / Augsburg",
        "album": "Kriegs-Karten des Donau-Stroms",
        "status": "authentic",
        "status_label": "Аўтэнтычная выява",
        "location": {
            "name": "Відзін (Widdin)",
            "wikidata": "Q178531",
            "lat": 43.9903,
            "lng": 22.8864
        },
        "description": "Гравіраваны план і профіль ключавой турэцкай цвярдыні на ніжнім Дунаі — крэпасці Баба Віда ў Відзіне, цэнтра пастаянных баёў паміж Асманскай і Габсбургскай імперыямі."
    },

    # --- OSIJEK / VUKOVAR / ERDUT (Осіек / Essegg — Марсільі 1726) ---
    {
        "id": "marsigli-danube-osijek-1726",
        "title": "Осіек (Essegg), Эрдут і Вукавар на Дунаі (Луіджы Марсільі, 1726)",
        "original_title": "Esseg (Össeg), Buginovitz, Erdut, Bucovar (Danubius Pannonico-Mysicus)",
        "commons_file": "File:Esseg (Össeg), Buginovitz, Erdut, Bucovar in Danubius Pannonico-Mysicus 1726 by Marsigli.png",
        "local_img": "marsigli-danube-osijek-1726.png",
        "year": 1726,
        "century": 18,
        "artist": "Граф Луіджы Фердынанда Марсільі (Luigi Ferdinando Marsigli)",
        "publisher": "Marsigli / Pieter Gosse (Den Haag / Amsterdam)",
        "album": "Danubius Pannonico-Mysicus (Том II)",
        "status": "authentic",
        "status_label": "Аўтэнтычная выява",
        "location": {
            "name": "Осіек (Tvrđa)",
            "wikidata": "Q1640",
            "lat": 45.5606,
            "lng": 18.6961
        },
        "description": "Унікальная гравюра з фундаментальнага 6-томнага атласа графа Марсільі: фартэцыя Осіек (Tvrđa) са знакамітым драўляным мастом Сулеймана Вялікапышнага праз балоты Дравы, а таксама замкі Эрдут і Вукавар."
    },

    # --- KOMÁROM (Камарам / Komorn — Марсільі 1726) ---
    {
        "id": "marsigli-danube-komarom-1726",
        "title": "Непрыступны замак Комарн (Луіджы Марсільі, 1726)",
        "original_title": "Comaromium vulgo Comorn (Danubius Pannonico-Mysicus)",
        "commons_file": "File:Comaromium vulgo Comorn in Danubius Pannonico-Mysicus 1726 by Marsigli.png",
        "local_img": "marsigli-danube-komarom-1726.png",
        "year": 1726,
        "century": 18,
        "artist": "Граф Луіджы Фердынанда Марсільі (Luigi Ferdinando Marsigli)",
        "publisher": "Den Haag / Amsterdam",
        "album": "Danubius Pannonico-Mysicus",
        "status": "authentic",
        "status_label": "Аўтэнтычная выява",
        "location": {
            "name": "Комарна / Камарам",
            "wikidata": "Q210796",
            "lat": 47.7540,
            "lng": 18.1320
        },
        "description": "Дэталёвы геаграфічны і фартыфікацыйны план знакамітай Старой і Новай фартэцыі Комарна на зліцці Дуная і Вага, якую туркі ніводнага разу не здолелі захапіць."
    },

    # --- BUDA & PEST (Буда і Пешт / Ofen) ---
    {
        "id": "marsigli-danube-buda-1726",
        "title": "Буда, Пешт і востраў Чэпель (Луіджы Марсільі, 1726)",
        "original_title": "Buda, Pest and Csepel Island (Danubius Pannonico-Mysicus)",
        "commons_file": "File:Buda, Pest and Csepel Island in Danubius Pannonico-Mysicus 1726 by Marsigli.jpg",
        "local_img": "marsigli-danube-buda-1726.jpg",
        "year": 1726,
        "century": 18,
        "artist": "Граф Луіджы Фердынанда Марсільі (Luigi Ferdinando Marsigli)",
        "publisher": "Den Haag / Amsterdam",
        "album": "Danubius Pannonico-Mysicus",
        "status": "authentic",
        "status_label": "Аўтэнтычная выява",
        "location": {
            "name": "Буда (Будапешт)",
            "wikidata": "Q1781",
            "lat": 47.4962,
            "lng": 19.0396
        },
        "description": "Гравіраваны гідраграфічны і тапаграфічны план ракі Дунай вакол замкавай гары Буды, Пешта і вострава Чэпель, створаны пасля вызвалення ад асманаў."
    },
    {
        "id": "buda-boethius-1686",
        "title": "Панарама вызвалення Буды 1686 г. (Крысціян Бетыус)",
        "original_title": "Boethius: Buda 1686 Prospect vom Aufgang",
        "commons_file": "File:Boethius Buda 1686 Prospect vom Aufgang.png",
        "local_img": "buda-boethius-1686.png",
        "year": 1686,
        "century": 17,
        "artist": "Крысціян Бетыус (Christian Boethius)",
        "publisher": "Nürnberg",
        "album": "Des Verwirrten Römischen Reichs Zustand (Kriegs-Helm)",
        "status": "authentic",
        "status_label": "Аўтэнтычная выява",
        "location": {
            "name": "Буда (Будапешт)",
            "wikidata": "Q1781",
            "lat": 47.5020,
            "lng": 19.0340
        },
        "description": "Гістарычная панарама штурму Будайскага замка войскамі Свяшчэннай лігі 2 верасня 1686 г., які паклаў канец 145-гадоваму асманскаму валадарству ў Венгрыі."
    },
    {
        "id": "buda-vanloon-1686",
        "title": "Аблога Буды войскамі Латарынгскага (Харман ван Лоан, 1686)",
        "original_title": "Buda 1686 (Harmanus van Loon)",
        "commons_file": "File:Buda 1686-Harmanus van Loon.jpg",
        "local_img": "buda-vanloon-1686.jpg",
        "year": 1686,
        "century": 17,
        "artist": "Харман ван Лоан (Harmanus van Loon)",
        "publisher": "Paris / Amsterdam",
        "album": "Les Forces de l'Europe",
        "status": "authentic",
        "status_label": "Аўтэнтычная выява",
        "location": {
            "name": "Буда (Будапешт)",
            "wikidata": "Q1781",
            "lat": 47.4980,
            "lng": 19.0410
        },
        "description": "Мастацкая медзярэзная панарама замкавай гары і разбураных сцен Афенскага эялета з артылерыйскімі пазіцыямі хрысціянскіх саюзнікаў."
    }
]

print(f"Processing {len(frontier_entries)} Ottoman Frontier engravings...")

new_db_entries = []

for entry in frontier_entries:
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
    new_db_entries.append(db_item)

print(f"\nSuccessfully processed and downloaded {len(new_db_entries)} frontier engravings!")

with open("C:/Users/bafur/.gemini/antigravity/scratch/engravings-map/scripts/frontier_batch.json", "w", encoding="utf-8") as f:
    json.dump(new_db_entries, f, ensure_ascii=False, indent=2)
