#!/usr/bin/env python3
"""Build a static preview of the Arabesque custom pages for local browser checks."""

from __future__ import annotations

import csv
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".preview"
OBJECTS = ROOT / "objects"
CSS = ROOT / "assets" / "css" / "arabesque.css"
THEME = ROOT / "assets" / "img" / "theme_image.png"
META = ROOT / "_data" / "collectionbuilder-metadata.csv"


def header(is_home: bool = False) -> str:
    wordmark = (
        '<h1 class="wordmark">'
        if is_home
        else '<a class="wordmark" href="./index.html">'
    )
    wordmark_close = "</h1>" if is_home else "</a>"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Arabesque — Muhammed Saied Kalash</title>
  <link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Noto+Naskh+Arabic:wght@400;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="./assets/css/arabesque.css">
</head>
<body class="arabesque{' home' if is_home else ''}">
  <header class="site-header">
    {wordmark}
      <span class="wordmark-ar ar" lang="ar">أرابيسك</span>
      <span class="wordmark-en">Arabesque</span>
    {wordmark_close}
    <div class="header-names">
      <div class="header-side header-left">
        <div>Muhammed Saied Kalash</div>
        <div class="header-sub">The Art Works</div>
      </div>
      <div class="header-side header-right">
        <div class="ar" lang="ar">محمد سعيد كلش</div>
        <div class="ar header-sub" lang="ar">الأعمال الفنية</div>
      </div>
    </div>
  </header>
  <main id="maincontent">
"""


def footer(is_home: bool = False) -> str:
    contact = ""
    if is_home:
        contact = """
  <footer class="site-footer">
    <p class="contact-label">Contact <span class="ar" lang="ar">للتواصل</span></p>
    <p><a href="mailto:kalasharabesque@gmail.com">kalasharabesque@gmail.com</a></p>
  </footer>
"""
    return f"""
  </main>
{contact}
</body>
</html>
"""


def write_home() -> None:
    body = """
<div class="home-stage">
  <section class="home-col home-browse" aria-label="Browse works">
    <ul class="home-list">
      <li><a href="./calligraphy.html"><span class="en-caps">All works</span><span class="ar" lang="ar">كل الأعمال</span></a></li>
      <li><a href="./calligraphy.html"><span class="en-caps">Calligraphy</span><span class="ar" lang="ar">الخط العربي</span></a></li>
      <li><a href="./about-kalash.html"><span class="en-caps">Islamic geometry</span><span class="ar" lang="ar">هندسة إسلامية</span></a></li>
      <li><a href="./about-kalash.html"><span class="en-caps">Botanical ornaments</span><span class="ar" lang="ar">زخارف إسلامية</span></a></li>
      <li><a href="./about-kalash.html"><span class="en-caps">Abstract works</span><span class="ar" lang="ar">زخارف مجردة</span></a></li>
      <li><a href="./about-kalash.html"><span class="en-caps">Wood works</span><span class="ar" lang="ar">أعمال الخشب</span></a></li>
      <li><a href="./about-kalash.html"><span class="en-caps">Glass and plexiglass</span><span class="ar" lang="ar">أعمال الزجاج والأكريليك</span></a></li>
    </ul>
  </section>
  <div class="home-theme">
    <img src="./assets/img/theme_image.png" alt="Tree of life">
  </div>
  <section class="home-col home-about">
    <h2 class="home-col-title">
      <a href="./about-kalash.html">
        <span class="en-caps">About</span>
        <span class="ar" lang="ar">عن الأعمال</span>
      </a>
    </h2>
    <ul class="home-list">
      <li><a href="./about-kalash.html"><span class="en-caps">Muhammed Saied Kalash</span><span class="ar" lang="ar">محمد سعيد كلش</span></a></li>
      <li><a href="./about-kalash.html"><span class="en-caps">Islamic art and calligraphy</span><span class="ar" lang="ar">الفن الإسلامي والخط العربي</span></a></li>
      <li><a href="./about-kalash.html"><span class="en-caps">The techniques</span><span class="ar" lang="ar">التقنية</span></a></li>
    </ul>
  </section>
</div>
"""
    (OUT / "index.html").write_text(header(True) + body + footer(True), encoding="utf-8")


def write_construction() -> None:
    body = """
<div class="construction-message">
  <p class="en-caps">Page under construction</p>
  <p class="ar" lang="ar">الصفحة قيد الإنشاء</p>
</div>
"""
    (OUT / "about-kalash.html").write_text(header() + body + footer(), encoding="utf-8")


def load_items() -> list[dict]:
    with META.open(encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_calligraphy(items: list[dict]) -> None:
    calligraphy = [i for i in items if i.get("content_en") == "Text"][:40]
    lis = []
    for item in calligraphy:
        lis.append(
            f'<li><a href="./item.html?id={item["objectid"]}&amp;from=calligraphy">'
            f'<span class="work-en">{item["title"]}</span>'
            f'<span class="work-ar ar" lang="ar">{item["title_ar"]}</span>'
            f"</a></li>"
        )
    body = (
        '<header class="page-heading">'
        '<span class="en-caps">Calligraphy</span>'
        '<span class="ar" lang="ar">الخط العربي</span>'
        "</header>"
        f'<ul class="work-list">{"".join(lis)}</ul>'
    )
    (OUT / "calligraphy.html").write_text(header() + body + footer(), encoding="utf-8")


def write_item(items: list[dict]) -> None:
    # Embed a trimmed item payload for the preview JS
    payload = [
        {
            "objectid": i["objectid"],
            "filename": i["filename"],
            "title": i["title"],
            "title_ar": i["title_ar"],
            "technique": i.get("technique", ""),
            "technique_ar": i.get("technique_ar", ""),
            "script_en": i.get("script_en", ""),
            "script_ar": i.get("script_ar", ""),
            "date": i.get("date", ""),
            "dimensions": i.get("dimensions", ""),
            "piece_number": i.get("piece_number", ""),
            "content_en": i.get("content_en", ""),
            "material": i.get("material", ""),
        }
        for i in items
        if i.get("content_en") == "Text"
    ][:80]

    # Prefer the mockup example in the preview set
    for i in items:
        if i.get("objectid") == "acr-099":
            sample = {
                "objectid": i["objectid"],
                "filename": i["filename"],
                "title": i["title"],
                "title_ar": i["title_ar"],
                "technique": i.get("technique", ""),
                "technique_ar": i.get("technique_ar", ""),
                "script_en": i.get("script_en", ""),
                "script_ar": i.get("script_ar", ""),
                "date": i.get("date", ""),
                "dimensions": i.get("dimensions", ""),
                "piece_number": i.get("piece_number", ""),
                "content_en": i.get("content_en", ""),
                "material": i.get("material", ""),
            }
            if all(p["objectid"] != "acr-099" for p in payload):
                payload.append(sample)
            break

    # Copy first few object images used in preview
    for item in payload[:12] + [p for p in payload if p["objectid"] == "acr-099"]:
        src = OBJECTS / item["filename"]
        if src.exists():
            shutil.copy2(src, OUT / "objects" / item["filename"])

    js_items = json.dumps(payload, ensure_ascii=False)
    body = f"""
<div id="item-page" class="item-page">
  <p id="item-loading" class="item-loading">…</p>
  <p id="item-missing" class="item-missing" hidden>Work not found. / العمل غير موجود.</p>
  <article id="item-article" hidden>
    <nav id="item-breadcrumb" class="item-breadcrumb" aria-label="Breadcrumb"></nav>
    <div class="item-viewer">
      <a id="item-prev" class="item-arrow" href="#" aria-label="Previous work" hidden>&lt;</a>
      <figure class="item-figure"><img id="item-image" alt=""></figure>
      <a id="item-next" class="item-arrow" href="#" aria-label="Next work" hidden>&gt;</a>
    </div>
    <div class="item-meta">
      <div class="item-meta-en">
        <p id="item-title-en" class="item-title-en"></p>
        <p id="item-technique" class="item-technique"></p>
      </div>
      <p id="item-number" class="item-number"></p>
      <div class="item-meta-ar">
        <p id="item-title-ar" class="item-title-ar ar" lang="ar"></p>
        <p id="item-technique-ar" class="item-technique-ar ar" lang="ar"></p>
      </div>
    </div>
    <p id="item-size" class="item-size"></p>
    <p id="item-year" class="item-year"></p>
  </article>
</div>
<script>
(function () {{
  var objectsBase = './objects/';
  var itemBase = './item.html';
  var items = {js_items};
  var categories = {{
    all: {{ en: 'All works', ar: 'كل الأعمال', href: './calligraphy.html' }},
    calligraphy: {{ en: 'Calligraphy', ar: 'الخط العربي', href: './calligraphy.html' }}
  }};
  function matchesFilter(item, filter) {{
    if (filter === 'all') return true;
    if (filter === 'calligraphy') return item.content_en === 'Text';
    return true;
  }}
  function catalogueCode(filename) {{
    var base = String(filename || '').replace(/\\.[^.]+$/, '');
    return base.split('_')[0] || '';
  }}
  function sizeCode(filename, dimensions) {{
    var base = String(filename || '').replace(/\\.[^.]+$/, '');
    var parts = base.split('_');
    for (var i = parts.length - 1; i >= 1; i--) {{
      var part = parts[i];
      if (/^\\d/i.test(part) || /[xX]/.test(part) || /d$/i.test(part) || /poly/i.test(part)) {{
        return part.replace(/x/g, 'X').replace(/d$/i, 'D');
      }}
    }}
    var dims = String(dimensions || '');
    var m = dims.match(/(\\d+(?:\\.\\d+)?)\\s*[×xX]\\s*(\\d+(?:\\.\\d+)?)/);
    if (m) return m[1] + 'X' + m[2];
    return '';
  }}
  var params = new URLSearchParams(window.location.search);
  var id = params.get('id') || (items[0] && items[0].objectid);
  var from = params.get('from') || 'calligraphy';
  var loading = document.getElementById('item-loading');
  var missing = document.getElementById('item-missing');
  var article = document.getElementById('item-article');
  var item = null;
  var index = -1;
  for (var i = 0; i < items.length; i++) {{
    if (items[i].objectid === id) {{ item = items[i]; break; }}
  }}
  loading.hidden = true;
  if (!item) {{ missing.hidden = false; return; }}
  var set = items.filter(function (it) {{ return matchesFilter(it, from); }});
  for (var k = 0; k < set.length; k++) {{
    if (set[k].objectid === item.objectid) {{ index = k; break; }}
  }}
  var cat = categories[from] || categories.calligraphy;
  var allCat = categories.all;
  document.getElementById('item-breadcrumb').innerHTML =
    '<a class="crumb" href="' + allCat.href + '"><span class="en-caps">' + allCat.en + '</span><span class="ar" lang="ar">' + allCat.ar + '</span></a>' +
    '<span class="crumb-sep">&gt;</span>' +
    '<a class="crumb" href="' + cat.href + '"><span class="en-caps">' + cat.en + '</span><span class="ar" lang="ar">' + cat.ar + '</span></a>';
  var img = document.getElementById('item-image');
  img.src = objectsBase + item.filename;
  img.alt = item.title || '';
  document.getElementById('item-number').textContent = catalogueCode(item.filename);
  document.getElementById('item-title-en').textContent = item.title || '';
  document.getElementById('item-title-ar').textContent = item.title_ar || '';
  document.getElementById('item-technique').textContent = item.technique || item.script_en || '';
  document.getElementById('item-technique-ar').textContent = item.technique_ar || item.script_ar || '';
  document.getElementById('item-size').textContent = sizeCode(item.filename, item.dimensions);
  document.getElementById('item-year').textContent = item.date || '';
  function itemHref(other) {{
    return itemBase + '?id=' + encodeURIComponent(other.objectid) + '&from=' + encodeURIComponent(from);
  }}
  var prev = document.getElementById('item-prev');
  var next = document.getElementById('item-next');
  if (index > 0) {{ prev.hidden = false; prev.href = itemHref(set[index - 1]); }}
  if (index >= 0 && index < set.length - 1) {{ next.hidden = false; next.href = itemHref(set[index + 1]); }}
  article.hidden = false;
}})();
</script>
"""
    (OUT / "item.html").write_text(header() + body + footer(), encoding="utf-8")


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets" / "css").mkdir(parents=True)
    (OUT / "assets" / "img").mkdir(parents=True)
    (OUT / "objects").mkdir(parents=True)
    shutil.copy2(CSS, OUT / "assets" / "css" / "arabesque.css")
    shutil.copy2(THEME, OUT / "assets" / "img" / "theme_image.png")
    items = load_items()
    write_home()
    write_construction()
    write_calligraphy(items)
    write_item(items)
    print(f"Preview written to {OUT}")


if __name__ == "__main__":
    main()
