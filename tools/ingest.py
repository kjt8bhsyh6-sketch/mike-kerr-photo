#!/usr/bin/env python3
"""Turn photos dropped into incoming/ into site photos (run by GitHub Actions, or by hand).

For each image in incoming/ (.heic .heif .jpg .jpeg .png):
  - makes web images with tools/build.py (sRGB, no GPS/camera data, creator/copyright embedded)
  - appends an entry to the END of photos.js (title from the file name, empty caption)
  - moves the original to originals/ (originals are kept, never deleted)
Optional sidecar text file with the same name, e.g. incoming/lake.txt:
    Title: Lake at dawn
    Caption: Mist over the water just after sunrise.
    Alt: A calm lake with low mist and pink sky.
Finally rebuilds index.html blocks + sitemap.xml.
"""
import json, re, shutil, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build

ROOT = build.ROOT; INC = ROOT / "incoming"; ORIG = ROOT / "originals"
EXTS = {".heic", ".heif", ".jpg", ".jpeg", ".png"}
CAMERA = re.compile(r"^(img|dsc|dscn|dscf|pxl|mvimg|photo|image|p|dji|gopr|screenshot|whatsapp image)?[\s_-]*[\d_\s-]+(\s*\(\d+\))?$", re.I)

def tidy_title(stem):
    s = stem.strip()
    if CAMERA.match(s) or not re.search(r"[A-Za-z]", s): return "Untitled"
    s = re.sub(r"[_-]+", " ", s); s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s*\(\d+\)$", "", s)  # "lake (1)" -> "lake"
    return s[:1].upper() + s[1:] if s else "Untitled"

def read_sidecar(img):
    meta = {}
    for ext in (".txt", ".TXT"):
        f = img.with_suffix(ext)
        if f.exists():
            for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
                m = re.match(r"\s*(title|caption|alt)\s*:\s*(.*)", line, re.I)
                if m and m.group(2).strip(): meta[m.group(1).lower()] = m.group(2).strip()
            return meta, f
    return meta, None

def unique_name(stem, taken):
    base = re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-") or "photo"
    n, i = base, 2
    while n in taken or (ROOT / "photos" / f"{n}-800.jpg").exists() or any(ORIG.glob(n + ".*")):
        n = f"{base}-{i}"; i += 1
    return n

def append_entry(entry):
    f = ROOT / "photos.js"; t = f.read_text()
    block = "  {\n" + ",\n".join(f"    {k}: {json.dumps(v, ensure_ascii=False)}" for k, v in entry.items()) + "\n  }"
    end = t.rindex("]")
    head = t[:end].rstrip()
    sep = "" if head.endswith("[") else ","
    f.write_text(head + sep + "\n" + block + "\n" + t[end:])

def main():
    files = sorted(p for p in INC.glob("*") if p.is_file() and p.suffix.lower() in EXTS) if INC.exists() else []
    taken = {p["name"] for p in build.load_photos()}
    ORIG.mkdir(exist_ok=True)
    for img in files:
        name = unique_name(img.stem, taken); taken.add(name)
        meta, side = read_sidecar(img)
        print(f"Processing {img.name} -> {name}")
        _, w, h = build.build(img, name)
        append_entry({"name": name, "width": w, "height": h,
                      "title": meta.get("title") or tidy_title(img.stem),
                      "caption": meta.get("caption", ""),
                      "alt": meta.get("alt") or "Photo by Mike Kerr"})
        shutil.move(str(img), ORIG / (name + img.suffix.lower()))
        if side: shutil.move(str(side), ORIG / (name + ".txt"))
    build.rebuild()
    print(f"Added {len(files)} photo(s).")

if __name__ == "__main__":
    main()
