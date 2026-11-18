# -*- coding: utf-8 -*-
import html, urllib.parse
OUT = 'C:/Users/dumes/Downloads/mobilier-a-vendre/index.html'
BASE = 'https://b329-lab.github.io/mobilier-a-vendre/'

NOW = 'now'; DATE = '15/12/2026'; SOLD = 'sold'
# Source de référence : « à vendre.docx » du 17/11/2026 (vélo ramené à 200 000 le 18/11).
# (id, titre, prix, détail, dispo, nb photos, libellé pour le message WhatsApp, précision prix)
ITEMS = [
 # Disponibles de suite
 ('a13','Lit bateau 1 place + matelas',100000,'',NOW,1,'le lit bateau 1 place avec matelas',''),
 ('a14','Lit princesse 1 place + matelas',100000,'',NOW,1,'le lit princesse 1 place avec matelas',''),
 ('a16','Canapé en bois sculpté',70000,'Vendu sans coussin',NOW,1,'le canapé en bois sculpté',''),
 ('a02','Coiffeuse vintage',45000,'125 × 48 cm',NOW,1,'la coiffeuse vintage',''),
 ('a03','Commode en bois massif',45000,'84 × 54 cm',NOW,1,'la commode en bois massif',''),
 ('a17','Miroir artisanal',15000,'',NOW,1,'le miroir artisanal',''),
 ('a18','Bureau + chaise',35000,'2 ensembles disponibles · 150 × 50 cm',NOW,2,'un bureau avec chaise','l’unité'),
 ('a19','Table console en bois massif',45000,'175 × 45 cm',NOW,1,'la table console en bois massif',''),
 ('a08','Meuble TV',40000,'235 × 55 cm',NOW,1,'le meuble TV',''),
 ('a21','Lampadaire artisanal en bambou',60000,'',NOW,1,'le lampadaire artisanal en bambou',''),
 ('a27','Chargeur universel',5000,'',NOW,1,'le chargeur universel',''),
 ('a28','Extracteur de jus SilverCrest',10000,'',NOW,1,'l’extracteur de jus SilverCrest',''),
 ('a29','Yaourtière 7 pots',10000,'',NOW,1,'la yaourtière 7 pots',''),
 ('a30','Vélo Fluide',200000,'',NOW,1,'le vélo Fluide',''),
 ('a31','Machine à coudre à pédale et électrique',130000,'',NOW,1,'la machine à coudre',''),
 # Disponibles à partir du 15/12/2026
 ('a11','Lit superposé triple + 2 matelas',180000,'',DATE,2,'le lit superposé triple avec ses deux matelas',''),
 ('a12','Lit 2 places + matelas',150000,'',DATE,1,'le lit 2 places avec matelas',''),
 ('a01','Lit Montessori + matelas',65000,'175 × 114 cm',DATE,1,'le lit Montessori avec matelas',''),
 ('a15','Lit 3 places + matelas',80000,'193 × 180 cm',DATE,1,'le lit 3 places avec matelas',''),
 ('a20','Table à manger + 6 chaises',130000,'180 × 90 cm',DATE,1,'la table à manger avec ses 6 chaises',''),
 ('a25','Table à manger',100000,'180 × 80 cm',DATE,1,'la table à manger 180 × 80 cm',''),
 ('a24','Canapé de jardin',120000,'',DATE,1,'le canapé de jardin',''),
 ('a22','Bureau + chaise',60000,'140 × 80 cm',DATE,1,'le bureau avec chaise',''),
 ('a23','Meuble de rangement',35000,'119 × 40 cm',DATE,1,'le meuble de rangement',''),
 ('a26','Meuble d’appoint',10000,'49 × 42 cm',DATE,1,'le meuble d’appoint',''),
 # Vendus : retirés de la page à la demande de Pons (18/11). Pour afficher un article vendu, le passer en SOLD ici.
 # Déjà vendus et retirés : A04 lampe en calebasse, A05 tables de chevet, A06 armoire 2 portes, A07 table console, A09 armoire, A10 étagères.
]
WA = '33767857959'

def price(p):
    return f'{p:,}'.replace(',', '\u202f')

def card(it):
    aid, title, p, detail, dispo, n, wa_label, note = it
    sold = dispo == SOLD
    photos = ''.join(f'<img src="img/{aid}-{k}.jpg" alt="{html.escape(title)}" loading="lazy">' for k in range(1, n + 1))
    if sold:
        badge = '<span class="availability badge-sold">Vendu</span>'
    elif dispo == NOW:
        badge = '<span class="availability">Disponible de suite</span>'
    else:
        badge = f'<span class="availability badge-date">Disponible le {dispo}</span>'
    if sold:
        cta = '<span class="reserve sold-button">Article vendu</span>'
    else:
        for a, b in (('le ', 'du '), ('les ', 'des '), ('la ', 'de la '), ('l’', 'de l’'), ('un ', 'd’un ')):
            if wa_label.startswith(a):
                de_label = b + wa_label[len(a):]
                break
        msg = f'Bonjour, je vous contacte au sujet {de_label} (réf. {aid.upper()}). Est-ce toujours disponible ?'
        href = f'https://wa.me/{WA}?text=' + urllib.parse.quote(msg, safe='')
        cta = f'<a class="reserve" href="{href}" target="_blank" rel="noopener">Réserver sur WhatsApp <span aria-hidden="true">↗</span></a>'
    note_html = f'<small> FCFA {note}</small>' if note else '<small> FCFA</small>'
    detail_html = html.escape(detail) if detail else '&nbsp;'
    return f'''<article class="card" id="{aid}">
  <div class="photo photo-{n}{' photo-sold' if sold else ''}">{photos}{badge}</div>
  <div class="card-body">
    <div class="card-top"><span class="ref">Réf. {aid.upper()}</span><span class="price">{price(p)}{note_html}</span></div>
    <h3>{html.escape(title)}</h3>
    <p class="detail">{detail_html}</p>
    {cta}
  </div>
</article>
'''

avail = [i for i in ITEMS if i[4] != SOLD]
sold = [i for i in ITEMS if i[4] == SOLD]
n_now = sum(1 for i in avail if i[4] == NOW)
n_date = len(avail) - n_now

CSS = '''
    :root { --ink:#262820; --muted:#74756b; --paper:#f6f3ed; --card:#fffefa; --line:#e7e1d6; --green:#365c45; --green-dark:#294936; --gold:#bf9b62; }
    * { box-sizing:border-box; }
    html { scroll-behavior:smooth; }
    body { margin:0; color:var(--ink); background:var(--paper); font-family:Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
    .wrap { width:min(1160px, calc(100% - 40px)); margin:0 auto; }
    header { padding:58px 0 36px; border-bottom:1px solid var(--line); }
    .eyebrow { text-transform:uppercase; letter-spacing:.16em; color:var(--green); font-size:11px; font-weight:750; }
    h1 { font-family:Georgia, "Times New Roman", serif; font-size:clamp(38px, 6vw, 68px); line-height:1.02; letter-spacing:-.04em; font-weight:500; margin:15px 0 14px; }
    .intro { color:var(--muted); max-width:560px; line-height:1.65; font-size:16px; margin:0; }
    .contact { display:flex; align-items:center; justify-content:space-between; gap:20px; margin-top:30px; padding:17px 20px; border:1px solid var(--line); border-radius:14px; background:rgba(255,254,250,.7); }
    .contact-label { display:block; color:var(--muted); font-size:12px; margin-bottom:4px; }
    .contact a { color:var(--ink); font-weight:700; text-decoration:none; letter-spacing:.02em; }
    .contact-note { color:var(--muted); font-size:13px; }
    .infos { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:14px; margin-top:16px; }
    .info { padding:14px 16px; border:1px solid var(--line); border-radius:12px; background:rgba(255,254,250,.7); }
    .info b { display:block; font-size:11px; text-transform:uppercase; letter-spacing:.1em; color:var(--green); margin-bottom:5px; }
    .info span { font-size:13px; color:var(--ink); line-height:1.5; }
    main { padding:32px 0 72px; }
    .section-head { display:flex; justify-content:space-between; align-items:end; margin-bottom:18px; gap:16px; }
    .section-head h2 { font:500 27px Georgia, "Times New Roman", serif; margin:0; }
    .count { color:var(--muted); font-size:13px; text-align:right; }
    .grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:18px; }
    .card { overflow:hidden; background:var(--card); border:1px solid var(--line); border-radius:16px; box-shadow:0 7px 24px rgba(39,37,28,.035); }
    .photo { height:245px; padding:15px; position:relative; display:flex; justify-content:center; align-items:center; gap:7px; background:#eeeae2; }
    .photo img { display:block; width:100%; height:100%; min-width:0; object-fit:contain; }
    .photo-2 img { width:50%; }
    .photo-3 img { width:33%; }
    .availability { position:absolute; top:12px; left:12px; padding:7px 10px; border-radius:99px; background:rgba(255,254,250,.94); color:var(--green); font-size:10px; letter-spacing:.03em; font-weight:750; }
    .badge-date { color:#725222; }
    .badge-sold { color:#8b3f35; background:#fff6f3; }
    .photo-sold img { filter:grayscale(.75); opacity:.8; }
    .card-body { padding:17px 18px 18px; }
    .card-top { display:flex; justify-content:space-between; align-items:center; gap:10px; }
    .ref { color:var(--muted); font-size:11px; letter-spacing:.1em; text-transform:uppercase; }
    .price { font-size:17px; font-weight:750; white-space:nowrap; }
    .price small { font-size:10px; font-weight:650; color:var(--muted); }
    .card h3 { font:500 22px Georgia, "Times New Roman", serif; margin:10px 0 4px; }
    .detail { color:var(--muted); font-size:13px; min-height:20px; margin:0 0 17px; }
    .reserve { display:flex; justify-content:space-between; align-items:center; text-decoration:none; color:white; background:var(--green); border-radius:9px; padding:12px 14px; font-size:13px; font-weight:700; transition:background .15s, transform .15s; }
    .reserve:hover { background:var(--green-dark); transform:translateY(-1px); }
    .sold-button { background:#e9e3da; color:#735f52; cursor:default; }
    .sold-section { margin-top:56px; padding-top:32px; border-top:1px solid var(--line); }
    .sold-section .section-head h2 { color:var(--muted); font-size:22px; }
    footer { padding:20px 0 32px; border-top:1px solid var(--line); color:var(--muted); font-size:12px; line-height:1.6; }
    @media (max-width:850px) { .grid { grid-template-columns:repeat(2,minmax(0,1fr)); } .infos { grid-template-columns:repeat(2,minmax(0,1fr)); } }
    @media (max-width:560px) { .wrap { width:min(100% - 28px, 440px); } header { padding-top:40px; } .grid { grid-template-columns:1fr; gap:14px; } .infos { grid-template-columns:1fr; gap:10px; } .photo { height:270px; } .contact { align-items:flex-start; flex-direction:column; gap:10px; } .contact-note { font-size:12px; } }
'''

FAVICON = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='20' fill='%23365c45'/%3E%3Ctext x='50' y='68' font-size='52' text-anchor='middle' fill='%23f6f3ed' font-family='Georgia,serif'%3EM%3C/text%3E%3C/svg%3E"

SOLD_HTML = '' if not sold else f'''    <div class="sold-section">
      <div class="section-head"><h2>Déjà vendus</h2><span class="count">{len(sold)} articles</span></div>
      <section class="grid" aria-label="Articles vendus">
{''.join(card(i) for i in sold)}      </section>
    </div>
'''

desc = f'{len(avail)} articles disponibles pour cause de départ : lits, armoires, bureaux, table à manger, pièces artisanales. Prix en FCFA, réservation par WhatsApp.'

page = f'''<!doctype html>
<!--
  Version | Date       | Statut  | Rédigé par | Modifié par | Objet de la révision
  v0.3    | 18/11/2026 | Ébauche | Claude     | Pons        | Retrait des articles vendus de la page, visuels de partage Facebook dans partage/
-->
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#f6f3ed">
  <title>Mobilier &amp; objets de maison à vendre, Lomé</title>
  <meta name="description" content="Mobilier et décoration à vendre à Lomé pour cause de départ. {desc}">
  <link rel="canonical" href="{BASE}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="fr_FR">
  <meta property="og:site_name" content="Mobilier à vendre, Lomé">
  <meta property="og:title" content="Mobilier &amp; objets de maison à vendre, Lomé">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{BASE}">
  <meta property="og:image" content="{BASE}img/apercu.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="{FAVICON}">
  <style>{CSS}  </style>
</head>
<body>
  <header><div class="wrap">
    <div class="eyebrow">Mobilier &amp; objets de maison · Lomé</div>
    <h1>De belles pièces<br>prêtes pour leur prochaine maison.</h1>
    <p class="intro">Mobilier et décoration à vendre pour cause de départ. La disponibilité de chaque article est indiquée sur sa fiche. Choisissez un article et contactez-nous directement sur WhatsApp pour le réserver.</p>
    <div class="contact"><div><span class="contact-label">Téléphone local</span><a href="tel:+22893826288">+228 93 82 62 88</a></div><div class="contact-note">Pour réserver, utilisez le bouton WhatsApp de l’article choisi.</div></div>
    <div class="infos">
      <div class="info"><b>Où</b><span>Lomé, quartier Kodjoviakopé. Adresse exacte communiquée à la réservation.</span></div>
      <div class="info"><b>Retrait</b><span>À venir chercher sur place, aux dates de disponibilité. Pas de livraison.</span></div>
      <div class="info"><b>État</b><span>Meubles de famille, utilisés et entretenus. Les photos sont celles des pièces vendues.</span></div>
      <div class="info"><b>Prix</b><span>Prix affichés en FCFA. Une remise se discute pour plusieurs articles.</span></div>
    </div>
  </div></header>
  <main class="wrap">
    <div class="section-head"><h2>Les articles disponibles</h2><span class="count">{len(avail)} articles · {n_now} de suite, {n_date} à partir du {DATE} · prix en FCFA</span></div>
    <section class="grid" aria-label="Articles disponibles">
{''.join(card(i) for i in avail)}    </section>
{SOLD_HTML}  </main>
  <footer><div class="wrap">Mobilier à vendre, Lomé · Pour toute question, appelez le +228 93 82 62 88.<br>Mise à jour le 18/11/2026.</div></footer>
</body>
</html>
'''
open(OUT, 'w', encoding='utf-8', newline='\n').write(page)
print('written', len(page), 'bytes;', len(avail), 'disponibles,', len(sold), 'vendus')
