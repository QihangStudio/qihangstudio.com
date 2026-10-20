# Development Log

## 2026-10-03
- Initiate qihangstudio.com.

## 2026-10-20

Focus
Continued refinement of the Qihang Studio homepage, with emphasis on theme behavior, multilingual localization, responsive typography, procedural graphics, and the custom scroll indicator.

Homepage / Visual Direction
- Continued moving the homepage away from a generic AI / SaaS landing-page aesthetic and toward a more editorial, architectural, research-studio identity.
- Preserved the existing neutral editorial layout, spectrum color system, large display typography, and restrained UI.
- Current English hero title:
  Data, image, and stories
  in conversation.
- Hero title and supporting paragraph were aligned to the same left edge.
- Slightly increased title line spacing for a less compressed composition.
- Continued exploring localized hero wording, including:
  Chinese: 数据成形，影像显现，叙事赋义。
  Chinese section-title direction: 三径通幽。

Dark / Light Mode
- Added a complete System / Light / Dark theme system.
- Theme preference is persisted with localStorage.
- System mode follows prefers-color-scheme.
- Added an early theme initializer in <head> to prevent light-mode flashing during page load.
- Dark mode background was progressively deepened to a near-black gallery tone (#090909).
- Adjusted dark-mode surfaces, borders, menus, muted text, and spectrum colors for visibility.
- Appearance button behavior was later refined:
  - Left click directly switches between light and dark mode.
  - Right click opens the full appearance selection menu.
  - Mobile supports long-press for the menu.
- Unified theme transition timing across the page, header, and menus:
  0.28s, same easing, no transition delay.
- Existing visual fade behavior and menu animation were preserved.

Procedural Histogram
- Replaced the large set of hard-coded SVG <rect> elements with a procedural JavaScript generator.
- The histogram keeps the same visual personality:
  - low columns on the left
  - increasing visual weight toward the right
  - controlled irregularity rather than pure randomness
- Individual columns vary slightly on every page load.
- The final columns remain relatively tall so the composition stays visually weighted to the right.
- All squares continue to sample one shared spectrum gradient.
- Clicking an empty area of the hero regenerates the histogram.
- Removed the earlier fade / translate shuffle animation.
- Histogram distribution now changes immediately on click for a harder, more data-like transition.

Scroll Indicator
- Converted the original decorative vertical line into a functional scroll indicator.
- Final interaction uses:
  - a thin gray vertical rail
  - one small moving segment inside the rail
  - segment width exactly matches the rail width
  - segment never extends beyond the rail
- The moving segment changes color according to its vertical position in the Qihang Studio spectrum.
- Light mode uses a more saturated scroll spectrum.
- Dark mode uses a brighter spectrum for visibility against the near-black background.
- The gray rail is synchronized with the corresponding theme divider-line color.
- Positioning was repeatedly adjusted to avoid two problems:
  - overlapping content on smaller desktop widths
  - drifting too far inward on very wide monitors
- Current positioning follows the page/content gutter rather than using a single fixed viewport offset.
- Mobile portrait hides the custom scroll indicator.

Multilingual Localization
- Implemented localization directly inside the existing shared frontend.
- No separate language pages or routes were introduced.
- The site remains one unified interface.
- Supported languages:
  - English
  - Simplified Chinese
  - Japanese
  - French
- A local JavaScript translation dictionary now drives visible copy using data-i18n attributes.
- Language switching:
  - replaces visible text immediately
  - changes <html lang="">
  - updates accessibility labels
  - updates the language-menu checkmark
  - persists the preference using localStorage
- Saved language is restored on reload.
- English remains the default.
- Translation uses textContent rather than unsafe arbitrary HTML injection.
- Manifesto emphasis remains semantic through the existing <em> structure.
- 28 translation keys were added across:
  meta
  nav
  appearance
  language
  hero
  practice
  solutions
  gallery
  about
  manifesto
  footer
- “Solutions” was localized interpretively rather than literally:
  Chinese: 方法
  Japanese: アプローチ
  French: Approches

Localized Typography
- English and French retain the existing typography:
  Display: Cormorant Garamond
  Body / UI: Manrope
- Chinese display typography uses a light Song-style serif stack:
  Songti SC
  STSong
  Noto Serif SC
  SimSun
- Chinese body/UI typography uses a light sans-serif stack:
  PingFang SC
  Noto Sans SC
  Microsoft YaHei
- Japanese display typography uses a light Mincho stack:
  Yu Mincho
  Hiragino Mincho ProN
  Hiragino Mincho Pro
  Noto Serif JP
- Japanese body/UI typography uses:
  Hiragino Sans
  Yu Gothic
  Noto Sans JP
- CJK display sizes, line heights, and letter spacing were tuned independently rather than forcing Latin typography metrics.

Responsive / Mobile Work
- Fixed multiple portrait-mobile collisions between hero copy, histogram, footer metadata, and other elements.
- Adjusted narrow-screen title sizing and spacing.
- Adjusted histogram size and placement on mobile.
- Footer metadata now reflows more safely on narrow screens.
- Practice-list spacing was reduced where necessary for mobile.
- Added localized wrapping rules:
  - Hero-title phrases should not break in the middle of an unfinished phrase between punctuation marks.
  - On narrow screens, the title may reduce in size rather than split awkwardly.
  - Colored / emphasized text in body copy should remain together on one line where possible and move as a unit when wrapping.
- Checked layouts across approximately 320–1440 px widths.

Code Cleanup
- Removed the large hard-coded histogram SVG block.
- Fixed malformed pasted-Markdown artifacts that had entered earlier HTML versions, including broken CSS property names, escaped JavaScript syntax, malformed href values, and SVG syntax.
- Removed excessive blank lines and trailing whitespace from the HTML.
- Kept the project frontend-only with HTML, CSS, and vanilla JavaScript.
- No backend, framework, API, or database was introduced.

Validation
- JavaScript syntax checks passed.
- Browser console checks passed.
- CSS structure checks passed.
- All four languages were tested.
- Language preference persists after reload.
- Light / Dark / System theme persistence works.
- Histogram regeneration continues to work after language changes.
- Scroll indicator remains synchronized with scrolling and theme state.
- Responsive layouts were checked across desktop and mobile widths.
- No deployment configuration was changed.
- No commit, push, or deployment was performed as part of the latest localization / responsive pass.

### Notes

The homepage is still a prototype.  
Next steps:
- refine histogram composition
- improve responsive layout
- begin Solutions / Gallery page structure