# incoming/ — drop new photos here

Upload photos (HEIC, JPG or PNG) into this folder using **Add file → Upload files** on GitHub.
A few minutes later they appear at the end of the gallery on https://kjt8bhsyh6-sketch.github.io/mike-kerr-photo/

What happens automatically (GitHub Actions, "Add photos and publish"):
- web-sized copies are made in `photos/` (location/GPS and camera data removed, "© Mike Kerr" embedded)
- an entry is added to the end of `photos.js` (title from the file name; camera names like `IMG_1234` become "Untitled")
- the original is moved to `originals/` (kept, not shown on the website)

Optional: upload a text file with the same name (e.g. `lake.txt` next to `lake.heic`) containing:
```
Title: Lake at dawn
Caption: Mist over the water just after sunrise.
Alt: A calm lake with low mist and a pink sky.
```
Please don't delete this README.
