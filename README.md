# Plasma Workspace Wallpapers

Plasma Workspace Wallpapers provides additional wallpapers for Plasma.

## Next

The current default wallpaper is not included in this repository, but in [Breeze](https://invent.kde.org/plasma/breeze/-/tree/master/wallpapers/Next). When a new default wallpaper is selected, the previous default will be moved to this repository.

## Image format conversion

Each wallpaper is stored in its original PNG/JPEG format and as a WebP image. The WebP files are generated in the source tree and committed together with the originals, so the build does not depend on an image conversion tool. Only the WebP images are installed.

After adding or updating a wallpaper, regenerate the WebP files and commit them:

```sh
tools/convert-images.py
```

The script requires Python 3 with [Pillow](https://python-pillow.org/). Images are encoded as WebP with quality 95; pass `--force` to re-encode images that are already up to date.
