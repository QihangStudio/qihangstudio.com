# Simplified Chinese essay font

`noto-serif-sc.css` embeds a genuine Noto Serif SC variable WOFF subset as a data URL. Keeping the font self-contained avoids external font services and file-origin font-fetch restrictions in direct HTML previews. Only the Simplified Chinese essay body selects it; other languages, headings and menus retain their existing fonts.

Source: Google Fonts’ official [`ofl/notoserifsc`](https://github.com/google/fonts/tree/main/ofl/notoserifsc), `NotoSerifSC[wght].ttf`. License: SIL OFL 1.1, included in `OFL-NotoSerifSC.txt` and retained in font name records.

The original font supports continuous weights 200–900. FontTools subsets the Simplified Chinese template characters plus ASCII, U+00A0 and U+3000, preserving variation tables and restricting the shipped weight axis to 300–500, with default 350. The WOFF is 354,784 bytes and covers all 834 required codepoints. Its `fvar`, `avar` and `gvar` tables remain present. CSS declares `font-weight: 300 500`; the browser confirms the face loads at 300, 350, 400 and 500. No synthetic weight is needed.

Following comparison of 300, 350 and 400, Simplified Chinese body text uses 350 and existing strong/b emphasis uses 500. Font family, size, line height, spacing, color and column width are unchanged. Other language typography is unchanged.

When new Simplified Chinese essays introduce characters, regenerate the subset from the official variable source using the union of all Simplified Chinese templates. Include normal spaces, U+00A0, U+3000 and ASCII, preserve name/license records, retain the 300–500 variation range, save WOFF, replace the embedded base64 and verify every source codepoint has a cmap entry. No font build step or font-tool dependency is needed to serve the site.
