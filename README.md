# Plasma Workspace Wallpapers

Plasma Workspace Wallpapers provides additional wallpapers for Plasma.

## Next

The current default wallpaper is not included in this repository, but in [Breeze](https://invent.kde.org/plasma/breeze/-/tree/master/wallpapers/Next). When a new default wallpaper is selected, the previous default will be moved to this repository.

## Image format conversion

Wallpaper images can be converted during the build before installation by setting `WALLPAPER_IMAGE_FORMAT` to `JPEG` or `WEBP`. This requires ImageMagick (`magick` or `convert`) and converts wallpaper images and screenshots; leaving the option unset keeps the original formats.

For example, configure with `-DWALLPAPER_IMAGE_FORMAT=WEBP`.
