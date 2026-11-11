# Gallery

The existing `/gallery/` page displays all six supplied works, in order: Canton, Junction, Nanjing, Eastport, Skycity, Way Home. Titles remain unchanged in every language. No dates, descriptions, locations or techniques are invented. The requested toolbar provides All, Cityscape, Illustration and Experiment filters plus grid/list views. Initial visual groupings place Canton, Junction, Nanjing, Eastport and Skycity in Cityscape, and all six works in Illustration. Experiment is currently empty. These editable groupings live in each artwork’s `data-categories` attribute.

## Files

- `index.html`: existing shared header/footer and controls, localized introduction, semantic six-work list, native image-viewer dialog.
- `../assets/gallery.css`: Gallery-only editorial layout, responsive grid/list views, filter toolbar and image viewer. Previews use equal 16:9 frames at every viewport with `object-fit: cover` and centered cropping, filling each frame without empty bands or distortion and aligning captions. Viewer images fit inside the available stage without cropping.
- `../assets/gallery.js`: dependency-free filtering, grid/list switching, viewer interaction, keyboard navigation, focus containment/restoration and background scroll locking/restoration. The viewer navigates only the filtered works.
- `../assets/site.js`: added Gallery translation dictionaries; existing language/theme/scroll logic is unchanged. English, Simplified/Traditional Chinese, Japanese and French use the same preference lifecycle.

The full-resolution `Canton.jpg` (2081×1080), `Junction.jpg` (3508×2480) and `Nanjing.jpg` (1920×1080) remain in this directory, unmodified. Original files are not modified, recolored or dimmed. Preview frames crop visually; the full-image viewer preserves the complete composition. The first image loads eagerly; the remaining five are lazy-loaded. Explicit intrinsic dimensions reserve layout space. No derived files or duplicate originals are needed.

Following the author’s request to include every artwork in this directory, `Eastport.jpg` (1200×900), `Skycity.jpg` (2480×1748) and `Way Home.jpg` (1920×1080) are also displayed unmodified. All six current JPG files are included. Non-image files such as HTML and this README are not artwork. Future additions require explicit markup and localized viewer labels rather than runtime directory scanning.

## Interaction

Click or tap an image to open a full-viewport native dialog. Closing, Escape, Left/Right, previous/next buttons, wraparound navigation, Enter activation and Tab/Shift+Tab are supported. Controls have 48px targets and translated accessible labels. The caption is a dialog heading and the position is announced through a polite live region. The modal makes background content inert, fixes the background at its scroll position, and restores both scroll and opener focus on close.

The viewer uses the original image URL. Modified clicks, JavaScript-disabled browsing and browsers without native dialog support retain ordinary links to the original images. There is no separate theme or language preference, backend or build step.

## Validation

Browser responsive checks on 2026-11-11:

| Viewport width | Grid columns |
| --- | --- |
| 320px | 1 |
| 375px | 1 |
| 430px | 1 |
| 768px | 2 |
| 1024px | 2 |
| 1280px | 3 |
| 1440px | 3 |
| 1920px | 3 |

All grid cases had no horizontal overflow. Full-image viewer checks retained the original image ratios; previews now use uniform filled 16:9 frames. All 48 full-image cases (six works × eight widths) loaded and fit completely inside the viewer stage. Focus loops, Escape, Enter, previous/next wraparound, background scroll lock and exact scroll/focus restoration were checked. All five languages retain artwork titles, translated introduction and accessible controls. Light/Dark/System and language preferences survive reload and cross-page navigation; artwork filters remain `none` and opacity `1`. The existing desktop scroll indicator reaches progress `1` at the footer and keeps its existing mobile visibility rule.

Original JPGs and unrelated page/style files were checksum-verified unchanged. JavaScript syntax and `git diff --check` pass. Browser console has no warnings or errors. Physical iPhone/iPad hardware was not used; the device-width checks were performed in the browser.

Toolbar checks: both layouts in all five languages at 320px, 768px and 1440px had no horizontal overflow. Category filtering, the empty Experiment state and filtered viewer wraparound (Skycity → Canton, 1 / 5) were verified. Console had no warnings or errors. Controls are hidden without JavaScript; original-image links remain usable.
