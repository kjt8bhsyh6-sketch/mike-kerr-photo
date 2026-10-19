# Editing Mike Kerr's photo site

Plain HTML/CSS/JS, hosted free on GitHub Pages. The photo list lives in `photos.js`.
One small script, `tools/build.py`, makes the web-ready images and refreshes a few generated bits of `index.html`.

One-time setup: `pip install --user pillow pillow-heif` (Pillow 11.3 or newer).

## Add a photo
1. Copy the iPhone photo (HEIC or JPG) into this folder, named simply, e.g. `lake.heic`.
2. Run (from this folder):
   ```
   python3 tools/build.py lake.heic
   ```
   It writes `photos/lake-800/1200/1600/2000` as `.avif`, `.webp` and `.jpg`, plus `photos/lake-og.jpg` (1200×630, used when the site is shared on social media).
   Every image is rotated correctly, converted to sRGB, has **all camera/GPS data removed**, and gets "Mike Kerr" / "© Mike Kerr. All rights reserved." embedded as creator/copyright.
   It prints a line like `name: "lake", width: 1500, height: 2000,`.
3. Edit `photos.js`: copy an existing `{ ... }` block, paste it, and set
   - `name`, `width`, `height`: paste the line the script printed
   - `title`: short name (also used for the photo's link, e.g. `#lake-at-dawn`)
   - `caption`: a sentence shown under the photo
   - `alt`: a plain description for people using screen readers
   Separate blocks with a comma.
4. Run `python3 tools/build.py` once more (no file name). This refreshes the no-JavaScript gallery, the search-engine data (JSON-LD), the share image tags and `sitemap.xml` from `photos.js`.
   (You can do steps 2 and 4 in one go if you edit `photos.js` first.)

The source HEIC does not need to stay in the folder. Note: anything committed here is public.

## Remove / reorder photos
Delete or move blocks in `photos.js`, then run `python3 tools/build.py`. The **first** photo is the big hero at the top and the social-share image.
Optionally delete the removed photo's files from `photos/`.

## Check locally
```
python3 -m http.server 8000
```
then open http://localhost:8000/

## Publish
```
git add -A
git commit -m "Update photos"
git push
```
Live in a minute or two: https://kjt8bhsyh6-sketch.github.io/mike-kerr-photo/

## Text placeholders
- About + contact: the About section of `index.html`.
- Usage/licensing contact: `usage.html` (replace "[placeholder]").
