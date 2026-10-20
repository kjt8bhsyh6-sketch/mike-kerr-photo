# How to add photos to your website (Mike)

Your website: https://kjt8bhsyh6-sketch.github.io/mike-kerr-photo/

You only ever need to do two things: **upload a photo**, and (if you like) **give it a name and caption**. The website takes care of the rest — resizing, removing the location data from your phone, adding your copyright, and publishing. New photos show up at the end of the gallery a few minutes after you upload.

Before the first time: make a free account at https://github.com/signup and tell Bill your username. Bill will give you access, and you'll get an email invitation — click **Accept**.

---

## Add photos from a computer
1. Go to https://github.com/kjt8bhsyh6-sketch/mike-kerr-photo/tree/main/incoming and sign in.
2. Click **Add file** (top right) → **Upload files**.
3. Drag your photos onto the page (or click "choose your files"). iPhone photos (HEIC), JPG and PNG all work. You can do several at once.
4. Scroll down and click the green **Commit changes** button.
5. Wait about 3–5 minutes, then reload your website. Done!

## Add photos from a phone
1. Open https://github.com/kjt8bhsyh6-sketch/mike-kerr-photo/tree/main/incoming in Safari or Chrome and sign in. (The GitHub app can't upload files — use the browser.)
2. If you don't see **Add file**, tap the **aA** (Safari) or **⋮** (Chrome) menu and choose **Request Desktop Website**.
3. Tap **Add file** → **Upload files** → **choose your files** → **Photo Library**, and pick your photos.
   - iPhone tip: if it asks, choose "Most Compatible" or just accept the default; both are fine.
4. Tap the green **Commit changes** button.
5. Wait a few minutes and check your website.

---

## Give a photo a name and caption
Photos straight from a phone are called something like `IMG_1234`, so they show up as **"Untitled"** with no caption. Two easy ways to fix that:

**Option A — name the file before uploading.** A file called `Lake at dawn.jpg` gets the title "Lake at dawn" automatically.

**Option B — edit the list afterwards (works on phone too):**
1. Go to https://github.com/kjt8bhsyh6-sketch/mike-kerr-photo/blob/main/photos.js
2. Click the **pencil ✏️** icon ("Edit this file").
3. Find your photo's block. It looks like this:
   ```
     {
       name: "img-1234",
       width: 1500,
       height: 2000,
       title: "Untitled",
       caption: "",
       alt: "Photo by Mike Kerr"
     }
   ```
4. Change only the words **inside the quotes**:
   - `title` — a short name, e.g. `"Lake at dawn"`
   - `caption` — a sentence shown under the photo
   - `alt` — a plain description of what's in the photo, for people who can't see it (e.g. `"A calm lake with mist and a pink sky"`)
   Keep the quote marks and the commas exactly as they are. Don't change `name`, `width` or `height`.
5. Click **Commit changes** (twice if it asks). The site updates in a few minutes.

**Move a photo or hide one:** in the same file, each `{ ... }` block is one photo, in the order they appear. The **first** one is the big photo at the top. You can cut and paste whole blocks to reorder (keep a comma between blocks), or delete a block to take a photo off the site. Your original is always kept safe in the `originals` folder.

## If something goes wrong
- Nothing appeared after 10 minutes? Open https://github.com/kjt8bhsyh6-sketch/mike-kerr-photo/actions — a red ✗ means it hit a problem. Just let Bill know; nothing is lost.
- Made a typo in photos.js and the gallery is empty? Tell Bill — every change is saved and can be undone.
