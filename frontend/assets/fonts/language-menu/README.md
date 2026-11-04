# Chinese language menu font variants

Official Google Fonts variable sources:
- https://github.com/google/fonts/tree/main/ofl/notosanssc
- https://github.com/google/fonts/tree/main/ofl/notosanstc

The source wght axis supports 100–900. These local WOFF subsets contain exactly the current Simplified or Traditional Chinese menu label, instantiated at genuine 150, 200, 250 and 300 positions with FontTools. Each static file has the matching OS/2 weight. No synthesized thinning is used. Included OFL licenses apply.

`menu-fonts.css` embeds only the 200 WOFF faces as data URLs so direct HTML previews do not need a separate font fetch. The Chinese menu labels use scoped CSS aliases Noto Sans SC Menu / Noto Sans TC Menu, ahead of system fonts. Only those two labels select these subsets; other Chinese text and essay fonts are unchanged. Other menu languages keep their existing typography. Regenerate the subsets if the menu labels change.

Japanese menu label 日本語 also uses a local Noto Sans JP subset instantiated at genuine weight 200, embedded in menu-fonts.css. Source: https://github.com/google/fonts/tree/main/ofl/notosansjp . The included OFL license applies. Japanese article typography is unchanged.
