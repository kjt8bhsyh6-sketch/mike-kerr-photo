#!/usr/bin/env python3
"""Build web images and regenerate the static parts of the site.

Usage (from the repo folder):
  python3 tools/build.py NAME.heic [MORE.jpg ...]   # make images for new photos, then rebuild pages
  python3 tools/build.py                            # just rebuild index.html blocks + sitemap from photos.js

For each source photo it writes to photos/:
  NAME-{800,1200,1600,2000}.{avif,webp,jpg}   (long edge <= width; sRGB with embedded profile)
  NAME-og.jpg                                  (1200x630 social-share crop)
All outputs: converted to sRGB, rotation fixed, ALL camera EXIF/GPS dropped,
creator + copyright embedded (XMP + EXIF Artist/Copyright).
Then it prints the size info to paste into photos.js, and refreshes the
<noscript> gallery, JSON-LD and sitemap.xml from photos.js.
One-time setup: pip install --user pillow pillow-heif   (Pillow >= 11.3)
"""
import io, json, re, sys, html
from pathlib import Path
from PIL import Image, ImageOps, ImageCms
try:
    from pillow_heif import register_heif_opener; register_heif_opener()
except ImportError:
    pass

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://kjt8bhsyh6-sketch.github.io/mike-kerr-photo/"
CREATOR = "Mike Kerr"
COPYRIGHT = "© Mike Kerr. All rights reserved."
WIDTHS = (800, 1200, 1600, 2000)
SRGB = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB"))
SRGB_BYTES = SRGB.tobytes()

XMP = f"""<?xpacket begin="\ufeff" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/"><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
<rdf:Description rdf:about="" xmlns:dc="http://purl.org/dc/elements/1.1/"
 xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/" xmlns:xmpRights="http://ns.adobe.com/xap/1.0/rights/"
 xmlns:plus="http://ns.useplus.org/ldf/xmp/1.0/"
 photoshop:Credit="{CREATOR}" xmpRights:Marked="True" xmpRights:WebStatement="{SITE}usage.html">
<dc:creator><rdf:Seq><rdf:li>{CREATOR}</rdf:li></rdf:Seq></dc:creator>
<dc:rights><rdf:Alt><rdf:li xml:lang="x-default">{COPYRIGHT}</rdf:li></rdf:Alt></dc:rights>
<plus:Licensor><rdf:Seq><rdf:li rdf:parseType="Resource"><plus:LicensorURL>{SITE}usage.html</plus:LicensorURL></rdf:li></rdf:Seq></plus:Licensor>
</rdf:Description></rdf:RDF></x:xmpmeta>
<?xpacket end="w"?>""".encode("utf-8")

def exif_bytes():
    e = Image.Exif(); e[0x013B] = CREATOR; e[0x8298] = "Copyright Mike Kerr. All rights reserved."  # Artist, Copyright (EXIF is ASCII-only; XMP has the (c) symbol)
    return e.tobytes()

def to_srgb(im):
    im = ImageOps.exif_transpose(im)
    icc = im.info.get("icc_profile")
    im = im.convert("RGB")
    if icc:
        src = ImageCms.ImageCmsProfile(io.BytesIO(icc))
        im = ImageCms.profileToProfile(im, src, SRGB, renderingIntent=0, outputMode="RGB")
    im.info = {}
    return im

def save_all(im, base):
    meta = dict(icc_profile=SRGB_BYTES, exif=exif_bytes(), xmp=XMP)
    im.save(f"{base}.jpg", quality=80, optimize=True, progressive=True, **meta)
    im.save(f"{base}.webp", quality=78, method=6, **meta)
    im.save(f"{base}.avif", quality=55, speed=4, **meta)

def build(src, name=None):
    src = Path(src); name = name or re.sub(r"[^a-z0-9-]+", "-", src.stem.lower()).strip("-")
    im = to_srgb(Image.open(src)); out = ROOT / "photos"; out.mkdir(exist_ok=True)
    for w in WIDTHS:
        c = im.copy(); c.thumbnail((w, w), Image.LANCZOS); save_all(c, out / f"{name}-{w}")
    og = ImageOps.fit(im, (1200, 630), Image.LANCZOS, centering=(0.5, 0.4))
    og.save(out / f"{name}-og.jpg", quality=82, optimize=True, icc_profile=SRGB_BYTES, exif=exif_bytes(), xmp=XMP)
    big = im.copy(); big.thumbnail((2000, 2000))
    print(f'Paste into photos.js:  name: "{name}", width: {big.width}, height: {big.height},')
    return name, big.width, big.height

def load_photos():
    txt = (ROOT / "photos.js").read_text()
    body = txt[txt.index("["): txt.rindex("]") + 1]
    body = re.sub(r"^\s*//.*$", "", body, flags=re.M)
    body = re.sub(r"(\{|,)\s*([A-Za-z_]\w*)\s*:", r'\1"\2":', body)   # bare keys -> "keys"
    body = re.sub(r",\s*([\]}])", r"\1", body)                          # trailing commas
    return json.loads(body)

def _s(t): return re.sub(r"[^a-z0-9]+", "-", (t or "").lower()).strip("-")
def slugs(P):
    """Link id per photo (#autumn-trees). Untitled/duplicate titles fall back to the file name. Mirrors app.js."""
    seen, out = set(), []
    for p in P:
        s = _s(p.get("title"))
        if not s or s == "untitled" or s in seen: s = _s(p["name"])
        seen.add(s); out.append(s)
    return out

def srcset(p, ext): return ", ".join(f"photos/{p['name']}-{w}.{ext} {w}w" for w in WIDTHS)

def replace_block(text, tag, content):
    a, b = f"<!-- BUILD:{tag} -->", f"<!-- /BUILD:{tag} -->"
    return re.sub(re.escape(a) + r".*?" + re.escape(b), lambda m: a + "\n" + content + "\n" + b, text, flags=re.S)

def rebuild():
    P = load_photos(); S = slugs(P); slug = lambda p: S[P.index(p)]; e = lambda s: html.escape(s or "", quote=True)
    ns = "\n".join(
        f'<figure id="{slug(p)}"><picture><source type="image/avif" srcset="{srcset(p,"avif")}" sizes="100vw">'
        f'<source type="image/webp" srcset="{srcset(p,"webp")}" sizes="100vw">'
        f'<img src="photos/{p["name"]}-1200.jpg" srcset="{srcset(p,"jpg")}" sizes="100vw" width="{p["width"]}" height="{p["height"]}" alt="{e(p["alt"])}"></picture>'
        f'<figcaption><strong>{e(p["title"])}</strong>{(" — " + e(p["caption"])) if p.get("caption") else ""} Photo by Mike Kerr.</figcaption></figure>' for p in P)
    person = {"@type": "Person", "@id": SITE + "#mike-kerr", "name": CREATOR, "url": SITE}
    graph = [person, {"@type": "WebSite", "@id": SITE + "#site", "url": SITE, "name": "Mike Kerr Photography", "author": {"@id": person["@id"]}}]
    for p in P:
        graph.append({"@type": "ImageObject", "contentUrl": f"{SITE}photos/{p['name']}-2000.jpg",
            "url": f"{SITE}#{slug(p)}", "name": p["title"], "caption": p.get("caption") or p["title"], "description": p["alt"],
            "width": p["width"], "height": p["height"], "creator": {"@id": person["@id"], "@type": "Person", "name": CREATOR},
            "creditText": CREATOR, "copyrightNotice": COPYRIGHT, "copyrightHolder": {"@id": person["@id"]},
            "license": SITE + "usage.html", "acquireLicensePage": SITE + "usage.html"})
    ld = '<script type="application/ld+json">\n' + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1).replace("</", "<\\/") + "\n</script>"
    f = ROOT / "index.html"; t = f.read_text()
    t = replace_block(t, "noscript", ns); t = replace_block(t, "jsonld", ld)
    if P:
        og = f"{SITE}photos/{P[0]['name']}-og.jpg"
        t = re.sub(r'(<meta (?:property|name)="(?:og|twitter):image" content=")[^"]*', lambda m: m.group(1) + og, t)
        t = re.sub(r'(<meta property="og:image:alt" content=")[^"]*', lambda m: m.group(1) + e(P[0]["alt"]), t)
        hero = P[0]
        t = re.sub(r'<link rel="preload" as="image"[^>]*>', f'<link rel="preload" as="image" type="image/avif" imagesrcset="{srcset(hero,"avif")}" imagesizes="min(100vw, calc(85vh * {hero["width"]/hero["height"]:.4f}))" fetchpriority="high">', t)
    f.write_text(t)
    imgs = "".join(f"\n    <image:image><image:loc>{SITE}photos/{p['name']}-2000.jpg</image:loc></image:image>" for p in P)
    (ROOT / "sitemap.xml").write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
  <url>
    <loc>{SITE}</loc>{imgs}
  </url>
  <url><loc>{SITE}usage.html</loc></url>
</urlset>
''')
    print(f"Rebuilt index.html blocks and sitemap.xml for {len(P)} photo(s).")

if __name__ == "__main__":
    for s in sys.argv[1:]: build(s)
    rebuild()
