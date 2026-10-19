# Editing Mike Kerr's photo site

The site is just a few plain files. No build step. The list of photos lives in `photos.js`.

## Add a photo
1. **Convert the iPhone photo (HEIC) to JPG.** One-time setup: `pip install --user pillow pillow-heif`. Then, from this folder (replace `NAME`):
   ```
   python3 -c "
   from pillow_heif import register_heif_opener; register_heif_opener()
   from PIL import Image, ImageOps
   im = ImageOps.exif_transpose(Image.open('NAME.heic')).convert('RGB')
   for n in (2000, 800):
       c = im.copy(); c.thumbnail((n, n)); c.save(f'photos/NAME-{n}.jpg', quality=82, optimize=True)
   "
   ```
   This fixes rotation and saves new JPGs **without** location (GPS) data. (Or you can export as JPG from Photos on a Mac and resize it.)
2. **Put the files in `photos/`**: `NAME-2000.jpg` (large) and `NAME-800.jpg` (thumbnail).
3. **Edit `photos.js`.** Copy an existing `{ ... }` block, paste it, and change it:
   - `file`: the large image, e.g. `"photos/NAME-2000.jpg"`
   - `thumb`: the thumbnail, e.g. `"photos/NAME-800.jpg"`
   - `title`: a short name
   - `caption`: a sentence shown under the photo
   - `alt`: a plain description for people using screen readers
   Separate blocks with a comma.

## Remove a photo
Delete its `{ ... }` block from `photos.js` (and the comma), then optionally delete its files from `photos/`.

## Reorder photos
Move the blocks in `photos.js`. The **first** one is the big hero image at the top.

## Publish your changes
```
git add -A
git commit -m "Update photos"
git push
```
GitHub Pages updates the live site in a minute or two: https://kjt8bhsyh6-sketch.github.io/mike-kerr-photo/

## About section
Edit the placeholder text in the About section of `index.html`.
