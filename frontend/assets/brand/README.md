# Qihang Studio logo assets

Source: `frontend/Qihang Studio copy.psd` (1000 × 1000). The PSD is unchanged.

## Export

The PSD contains original 8.24 fixed-point Bézier paths, separate gradient ring layers, separate white stroke layers, cached RGB/alpha channels, a white background, and hidden lettering. The export uses the artwork's original stacking order. Gradient layers paint normally; white stroke layers subtract alpha with destination-out compositing. The background and hidden lettering are excluded. This preserves pale gradient colors without selecting or deleting pixels by color.

The PNG is cropped to the original artwork bounds plus a one-pixel transparent margin, 680 × 680 pixels. Geometry is not stretched, redrawn or upscaled. Flattening it over white and comparing it to the source's merged image gives mean absolute RGB difference 0.0334 on the 0–255 scale (maximum 2, caused by compositing/rounding at edges).

`logo.svg` contains genuine original Bézier paths, original stroke widths, and ordered knockout masks. Its color ramps are sampled from the source gradient fields with 129 stops per ring. There is no embedded raster. Photoshop's per-pixel gradient dithering cannot be represented identically by a vector gradient; the PNG remains the authoritative pixel appearance used in the header and icons.

## Hover

The hovered color field uses a monotone smooth remapping along the original upper-left/lower-right gradient axis. The lavender region advances toward the upper-left and expands to roughly 60% coverage; champagne is almost entirely displaced in the hovered state, while rose and periwinkle remain. The default image stays unchanged. It is not a tint, hue rotation, brightness filter, or shape transformation.

`logo.png` and `logo-hover.png` have byte-identical alpha channels. Counting high-opacity pixels with hue 250°–285° gives approximately 17% purple in the default field and 61% in the hovered field. This metric is an estimate for balance, not a visual boundary.

The header always renders the normal PNG as an actual image. Where `mix-blend-mode: plus-lighter` is supported, it crossfades that image and the hovered PNG with complementary opacities inside an isolated transparent group. Additive compositing keeps the shared alpha unchanged: `(1-t) × alpha + t × alpha = alpha`. There is no external CSS mask, so local-file mask restrictions cannot hide the logo. Without additive blending support, the normal image remains a static fallback.

Transitions take 450ms ease-in-out, hold while hovered, and reverse on pointer exit. Keyboard focus gets the same treatment. Coarse/touch pointers keep the default image; reduced-motion disables transitions.

## Outputs

- `logo.png`: 680 × 680 transparent original appearance.
- `logo-hover.png`: 680 × 680 transparent hovered appearance, same alpha.
- `logo-color.png`: opaque original RGB field retained from the source export; no longer used by the header.
- `logo-hover-color.png`: opaque hovered RGB field retained from the source export; no longer used by the header.
- `logo.svg`: genuine vector paths, masks and sampled gradient ramps.
- `favicon.ico`: 16, 32 and 48px representations.
- `favicon-16.png`, `favicon-32.png`: transparent PNG favicons.
- `apple-touch-icon.png`: 180px transparent icon.

All HTML pages reference the same icon assets with relative paths. All CSS asset URLs resolve relative to `assets/site.css`, including direct local-file previews.
