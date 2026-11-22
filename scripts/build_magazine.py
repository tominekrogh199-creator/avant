#!/usr/bin/env python3
"""Render magazine fronts from data. Standard library only; no server required."""
from pathlib import Path
from html import escape as esc
import argparse, json, re
parser=argparse.ArgumentParser();parser.add_argument('--output',default='.');args=parser.parse_args()
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/args.output
D=json.loads((OUT/'data/magasin.json').read_text()); E=ROOT/'editor'
brands={b['id']:b for b in D['brands']}; articles={a['id']:a for a in D['articles']}
assert len(brands)==len(D['brands']) and len(articles)==len(D['articles']), 'IDs must be unique'
for a in articles.values():
    assert a['brand'] in brands and (OUT/a['url']).is_file(), f"Missing brand or article: {a['id']}"
    assert (OUT/a['image']).is_file(), f"Missing image: {a['image']}"
def h(v):return esc(str(v),quote=True)
def link(url,text,cls='fashion-link'):return f'<a class="{cls}" href="{h(url)}">{h(text)}</a>'
def nav(active,current="page"):
    items=[('featured.html','Magasinet'),('saker.html','Alle saker'),('merker.html','Merker'),('om-avant.html','Om AVANT')]
    links=''.join(f'<a href="{url}"'+(f' aria-current="{current}"' if url==active else '')+f'>{label}</a>' for url,label in items)
    return f'<header class="couture-header" id="topp"><div class="couture-top"><span>Et norsk motemagasin</span><span>{h(D["season"])}</span></div><a class="couture-wordmark" href="featured.html" aria-label="AVANT, magasinets forside">AVANT</a><nav class="couture-nav" aria-label="Hovedmeny">{links}</nav></header>'
def dimensions(path):
    # JPEG intrinsic dimensions; avoid layout shifts without image dependencies.
    data=path.read_bytes()
    if data[:2] != b"\xff\xd8": return (1086,1448)
    i=2
    while i < len(data)-9:
        if data[i] != 255: i+=1; continue
        marker=data[i+1];i+=2
        if marker in (0xD8,0xD9): continue
        size=int.from_bytes(data[i:i+2],'big')
        if marker in (0xC0,0xC1,0xC2):
            return (int.from_bytes(data[i+5:i+7],'big'),int.from_bytes(data[i+3:i+5],'big'))
        if size<2: break
        i+=size
    raise ValueError(f"Cannot read image size: {path}")
def img(a,key='image',altkey='alt',extra='',sizes='(max-width:699px) calc(100vw - 36px), (max-width:1399px) 46vw, 640px'):
    src=a[key]; path=OUT/src;w,ht=dimensions(path)
    small=path.with_name(path.stem+'-900'+path.suffix)
    responsive=''
    if small.is_file():
        sw,_=dimensions(small)
        responsive=f' srcset="{h(small.relative_to(OUT))} {sw}w, {h(src)} {w}w" sizes="{sizes}"'
    return f'<img src="{h(src)}" alt="{h(a[altkey])}" width="{w}" height="{ht}" loading="lazy" decoding="async"{responsive} {extra}/>'
def meta(a):return f'{h(a["type"])} · {h(brands[a["brand"]]["name"])}'
def filterUI(label,placeholder,categories):
    buttons='<button type="button" data-filter="all" aria-pressed="true">Alle</button>'+''.join(f'<button type="button" data-filter="{h(c)}" aria-pressed="false">{h(c)}</button>' for c in categories)
    return f'<div class="browse-controls" data-controls hidden><div class="search-field"><label for="magazine-search">{label}</label><input id="magazine-search" type="search" placeholder="{placeholder}" autocomplete="off" aria-controls="browse-results"/></div><div class="filter-list" role="group" aria-label="Filtrer etter type">{buttons}</div><button type="button" class="clear-filters" data-clear hidden>Nullstill</button></div>'
def empty():return '<div class="empty-result" data-empty hidden><h2>Ingen treff</h2><p>Prøv et annet søkeord, eller se hele utvalget.</p><button type="button" data-reset>Vis alle</button></div>'
def card(a):
    b=brands[a['brand']]; search=' '.join(str(a.get(k,'')) for k in ['title','type','deck','issue'])+' '+b['name']+' '+b['designer']
    return f'<article class="archive-card" data-entry data-category="{h(a["type"])}" data-search="{h(search)}"><a class="archive-image" href="{h(a["url"])}" aria-label="{h(a["title"])}">{img(a)}</a><p class="fashion-label">{meta(a)}</p><h2>{link(a["url"],a["title"],"headline-link")}</h2><p>{h(a["deck"])}</p><div class="entry-meta">{h(a["issue"])} · {a["minutes"]} min lesetid</div></article>'
def brandRow(b,full=False):
    matched=[a for a in D['articles'] if a['brand']==b['id']]
    links=''.join(link(a['url'],a['title']) for a in matched)
    if full:
        search=' '.join([b['name'],b['designer'],b['discipline'],b['description']])
        return f'<article id="{h(b["id"])}" class="brand-entry" data-entry data-category="{h(b["discipline"])}" data-search="{h(search)}"><div class="brand-photo">{img(b,sizes="(max-width:699px) 110px, 230px")}</div><div class="brand-info"><div class="brand-heading"><p class="fashion-label">{h(b["discipline"])}</p><h2>{h(b["name"])}</h2><p class="brand-designer">{h(b["designer"])}</p></div><p class="brand-description">{h(b["description"])}</p><div class="brand-stories"><h3>Les i AVANT</h3>{links}</div></div></article>'
    return f'<a class="brand-index-row" href="merker.html#{h(b["id"])}"><span>{h(b["name"])}</span><span>{h(b["designer"])}</span><span>{h(b["discipline"])}</span></a>'
footer=(E/'footer.html').read_text()
footer=re.sub(r'<nav aria-label="Bunnmeny">.*?</nav>','<nav aria-label="Bunnmeny"><ul><li><a href="saker.html">Alle saker</a></li><li><a href="merker.html">Merker</a></li><li><a href="om-avant.html">Om AVANT</a></li><li><a href="om-avant.html#kontakt">Kontakt</a></li></ul></nav>',footer,flags=re.S)
def page(filename,title,desc,body,active,home=False,script=''):
    head=(E/'head.html').read_text()
    head=re.sub(r'<title>.*?</title>',f'<title>{h(title)} | AVANT</title>',head)
    for attr,key,value in [('name','description',desc),('property','og:title',title+' | AVANT'),('property','og:description',desc),('property','og:image','https://avantedit.no/'+articles[D['cover']]['image']),('property','og:image:alt',articles[D['cover']]['alt']),('name','twitter:image','https://avantedit.no/'+articles[D['cover']]['image'])]:
        head=re.sub(r'<meta [^>]*'+attr+'="'+key+r'"[^>]*>',f'<meta {attr}="{key}" content="{h(value)}"/>',head)
    classes='couture-home' if home else 'couture-article magazine-interior'
    html=f'<!doctype html>\n<html lang="nb" class="no-js">{head}<body class="editorial publication couture {classes}"><a class="skip" href="#innhold">Hopp til innhold</a>{nav(active)}<main class="couture-main" id="innhold" tabindex="-1">{body}</main>{footer}<script src="js/config.js"></script><script src="js/main.js"></script>{script}</body></html>\n'
    (OUT/filename).write_text(html)
a=articles[D['cover']];b=brands[a['brand']];second=articles[D['secondary']]
coverimg=img(a).replace('loading="lazy"','fetchpriority="high"')
contents=f'<aside class="cover-contents" aria-label="I utgaven"><p class="fashion-label">I denne utgaven</p><a href="{a["url"]}"><span>{h(a["type"])}</span><strong>{h(b["name"])}</strong></a><a href="#intervju"><span>{h(second["type"])}</span><strong>{h(brands[second["brand"]]["name"])}</strong></a></aside>'
hero=f'<div class="couture-issue"><span>Featured Edit</span><span>{h(D["edition"])}</span></div><section class="cover-story" aria-labelledby="cover-title"><a class="cover-photo" href="{a["url"]}" aria-label="{h(a["title"])}">{coverimg}<span class="cover-mark">På forsiden</span></a><div class="cover-copy"><div class="cover-intro"><p class="fashion-label">{meta(a)}</p><h1 id="cover-title">{h(a["title"])}</h1><p class="cover-deck">{h(a["deck"])}</p>{link(a["url"],"Les reportasjen")}<p class="entry-meta">Av AVANT · {a["minutes"]} min lesetid</p></div>{contents}</div></section><p class="cover-credit">Foto: {h(a["credit"])}</p>'
portrait=f'<figure class="interview-portrait">{img(second,"portrait","portraitAlt",sizes="135px")}<figcaption>{h(brands[second["brand"]]["designer"])}, designeren bak {h(brands[second["brand"]]["name"])}.</figcaption></figure>' if second.get('portrait') else ''
feature=f'<section class="interview-feature" id="intervju" aria-labelledby="interview-title"><div class="feature-rule"><p class="fashion-label">Møt designeren</p>{link("saker.html","Alle saker")}</div><div class="interview-layout"><a class="interview-photo" href="{second["url"]}" aria-label="{h(second["title"])}">{img(second)}</a><div class="interview-copy"><p class="fashion-label">{meta(second)}</p><h2 id="interview-title">{h(second["title"])}</h2><p>{h(second["deck"])}</p>{link(second["url"],"Les intervjuet")}{portrait}</div></div><p class="cover-credit">Foto: {h(second["credit"])}</p></section>'
# Additional real stories become a front-page grid automatically as the edition grows.
remaining=[x for x in D['articles'] if x['id'] not in (D['cover'],D['secondary'])]
more='<section class="more-stories"><h2>Flere historier</h2><div class="archive-grid">'+''.join(card(x) for x in remaining)+'</div></section>' if remaining else ''
discovery='<section class="brand-discovery" aria-labelledby="discovery-title"><div><p class="fashion-label">Oppdag</p><h2 id="discovery-title">Merker med<br/>egne ideer.</h2><p>Fra skreddersøm til redesign. Bli kjent med merkene vi har møtt, og menneskene som står bak.</p>'+link('merker.html','Utforsk merkene')+'</div><div>'+''.join(brandRow(x) for x in sorted(D['brands'],key=lambda x:x['name']))+'</div></section>'
about='<section class="editor-note"><p class="fashion-label">Om magasinet</p><p>Det finnes mer å oppdage i norsk mote. AVANT møter små og nye merker, besøker arbeidsrommene deres og lar designerne fortelle om det de lager.</p>'+link('om-avant.html','Dette er AVANT')+'</section>'
page('featured.html','Featured Edit – et norsk motemagasin','Møt designerne bak små og nye norske motemerker. Atelierbesøk, intervjuer og nye perspektiver på garderoben.',hero+feature+more+discovery+about+(E/'credits.html').read_text(),'featured.html',True)
(OUT/'index.html').write_text((OUT/'featured.html').read_text())
archive='<header class="collection-heading"><p class="fashion-label">AVANT · Arkiv</p><h1>Alle saker</h1><p>Arbeidsrommene, menneskene og ideene bak klærne.</p></header><section data-browser aria-label="Søk i magasinet" data-noun="saker">'+filterUI('Søk i sakene','Tittel, merke eller designer',list(dict.fromkeys(x['type'] for x in D['articles'])))+f'<p class="result-count" role="status" aria-live="polite" data-count>{len(D["articles"])} saker</p><div class="archive-grid" id="browse-results">'+''.join(card(x) for x in D['articles'])+'</div>'+empty()+'</section>'
page('saker.html','Alle saker','Atelierbesøk og intervjuer fra AVANT. Finn en historie, designer eller et merke.',archive,'saker.html',script='<script src="js/browse.js" defer></script>')
directory='<header class="collection-heading"><p class="fashion-label">AVANT · Merkeoversikt</p><h1>Merker</h1><p>Små og nye merker, samlet på ett sted. Bli kjent med designerne gjennom historiene våre.</p></header><section data-browser aria-label="Søk blant merkene" data-noun="merker">'+filterUI('Søk etter merke eller designer','Navn eller designretning',list(dict.fromkeys(x['discipline'] for x in D['brands'])))+f'<p class="result-count" role="status" aria-live="polite" data-count>{len(D["brands"])} merker · A–Å</p><div class="brand-directory" id="browse-results">'+''.join(brandRow(x,True) for x in sorted(D['brands'],key=lambda x:x['name']))+'</div>'+empty()+'</section>'
page('merker.html','Merker','Bli kjent med merkene i AVANT. Utforsk designere, atelierbesøk og intervjuer.',directory,'merker.html',script='<script src="js/browse.js" defer></script>')
aboutpage='''<header class="collection-heading" id="om-oss"><p class="fashion-label">Om AVANT</p><h1>Et blikk på det som skapes her.</h1><p>AVANT er et digitalt motemagasin om små og nye norske merker – og menneskene bak dem.</p></header><section class="about-columns" id="visjon" aria-labelledby="about-title"><h2 id="about-title">Nysgjerrighet på norsk mote.</h2><div><p>Hvem står bak klærne? Hvordan arbeider de? Og hva ønsker de å lage? Det er spørsmålene vi tar med oss inn i Featured Edit, AVANTs magasinserie.</p><p>Gjennom atelierbesøk, bilder og intervjuer vil vi gjøre det lettere å oppdage merker du kanskje ikke kjenner fra før. Du kan lese historiene i magasinet og finne merket igjen i merkeoversikten.</p><p>AVANT startet som et studentprosjekt ved BI Oslo. Vi studerer forretningsutvikling og entreprenørskap, og bygger et magasin og et kreativt fellesskap rundt små norske motemerker og unge skapere.</p></div></section><section class="contact-editorial" id="kontakt" aria-labelledby="contact-title"><div><p class="fashion-label">Kontakt</p><h2 id="contact-title">Har du en historie vi bør kjenne til?</h2><p>Vi vil gjerne høre fra designere, skapere og lesere. Send oss et tips, en idé eller en henvendelse om samarbeid.</p><a class="contact-mail" href="mailto:Tominekrogh199@gmail.com">Tominekrogh199@gmail.com</a><p class="entry-meta">Tomine Mariam Krogh · medgründer og deleier</p></div>'''+(E/'contact.html').read_text()+'</section>'
page('om-avant.html','Om AVANT','Et norsk motemagasin med nysgjerrighet på små og nye merker. Les om AVANT eller ta kontakt.',aboutpage,'om-avant.html')
# The same navigation on every article; brand names are content, never permanent tabs.
for a in D['articles']:
    path=OUT/a['url'];html=path.read_text()
    html=re.sub(r'<header class="couture-header".*?</header>',nav('saker.html','location'),html,flags=re.S)
    if 'css/magazine-system.css' not in html:html=html.replace('</head>','<link rel="stylesheet" href="css/magazine-system.css"/></head>')
    html=re.sub(r'<footer class="bunn">.*?</footer>',footer,html,flags=re.S)
    path.write_text(html)
print('Rendered front, archive, brand directory, about page and shared article navigation.')

# Production URLs for sharing and search; the two front URLs share one canonical.
for path in OUT.glob('*.html'):
    html=path.read_text()
    url='https://avantedit.no/'+('' if path.name in ('index.html','featured.html') else path.name)
    html=re.sub(r'<link[^>]*rel="canonical"[^>]*>','',html)
    html=re.sub(r'<meta[^>]*property="og:url"[^>]*>','',html)
    html=html.replace('</head>',f'<link rel="canonical" href="{url}"/><meta property="og:url" content="{url}"/></head>')
    path.write_text(html)
