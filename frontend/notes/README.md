# Personal Notes 内容维护

## 文件与路由

- `../about/index.html#personal-notes`：Personal Notes 的主入口，位于 About 下方。Me & Art 默认折叠，文章直接链接到阅读页；两个 Coming Soon 是不同层级的普通文本。
- `index.html`：兼容旧 Notes URL，跳转到 About 的 Personal Notes 区域。
- `before-the-next-stroke/index.html`：四语言全文，共用一个阅读 URL。
- `within-the-mist/index.html`：暂未收到原稿，只显示本地化状态，不含虚构正文。
- `me-and-art/Before the Next Stroke/`：作者提供的 EN / CN Word 原稿，文件内容未经修改。
- `me-and-art/Within the Mist/`：按作者要求创建并留空，等待原稿。空目录不会被 Git 保存。
- 旧的 `me-and-art/index.html` 和 `arts-got-problems/index.html` 仅跳转到 About 的 Personal Notes 区域，避免留下多余的合集页面或过期文章。

## 原稿与翻译

网页英文从 Word 文本和格式逐段提取，没有改写。中文版同样保留原稿内容，只有一处经过作者明确授权的修改：

原句：人是多样的，对事物的审美也是多样的，如是，仅仅是一人觉得事物存在艺术性，那么我们就不能否认它是艺术。

网页改为：人是多样的，对事物的审美也是多样的；如果哪怕只有一个人感受到某件事物的艺术性，那么这件事物至少拥有一位欣赏者。

两份 Word 文件本身保持原样。标题、中文署名、段落、诗行、原有斜体与粗体均保留在对应语言模板中；英文中的原有不规则标点、语法、空格也未修正。原稿没有实际脚注、尾注、表格或图片。

作者已确定日法翻译原则：所有意思参考英文，意境参考中文。日法版本逐段对应英文，不概括、不省略。差异处据此处理：

1. 艺术性论断保留英文的“至少有一位欣赏者”，中文版该句按授权同步。
2. 英文没有“南洋杉替代故乡水杉”的对照，日法不添加这一中文独有意象。
3. 英文结尾含银蕨、几维鸟，且“走得很远，也并不那么远”的表述不同于中文；日法保留英文内容。
4. “启航”同时是姓名和扬帆起程的双关。日文使用“啓航”并接扬帆、出发的解释；法文保留 Qihang 并解释为 mettre les voiles, commencer le voyage。
5. 中文独有署名仅保留在中文版，不向英文或译文添加新署名。

已发现的版本差异均按作者给定优先级处理，无未解决的论断冲突。《Within the Mist》尚无原文，因此没有制作任何版本或译文。

## 添加或更新文章

1. 将原稿放入对应原稿目录，保留作者提供的文件。
2. 复制现有阅读页到 `notes/<slug>/index.html`，更新目录链接。保留相对资源路径，兼容本地文件预览和静态服务器。
3. 为 en、zh、zh-Hant、ja、fr 各维护一个 `<template data-essay-language="…" data-essay-lang="…">`。中文菜单内部代码是 `zh`，HTML 语言标记是 `zh-CN`。
4. 每个模板包含一个 `h1` 和一个 `.essay-body`。使用语义 HTML 保留段落、`em`、`strong`、`blockquote`、标题与引用；`data-source-paragraph` 用于逐段核查。正文不要使用 UI 的 `data-i18n`，避免覆盖整段格式。
5. 更新 About 页的 Personal Notes 目录。必要的新界面文案加入 `assets/site.js` 的 `essayInterfaceTranslations` 四语言字典。
6. 正文模板放在 `notes.js` 和 `site.js` 两个脚本之前；脚本顺序必须是 `notes.js` 在前、`site.js` 在后。
7. 在 HTTP 本地预览中检查四语言全文、重载和跨页偏好、主题、320px 布局。直接双击本地 HTML 时资源无需 fetch；浏览器对 file:// 的存储共享策略不同，跨页偏好应以 HTTP/实际站点为准。

## 语言与主题

`site.js` 是唯一语言菜单与偏好的实现，仍保存到 `qihangstudio-language`。语言应用时同步发出 `studio:language-change`；`notes.js` 克隆对应静态模板，更新标题、全文、页面标题及 `lang`。繁体中文使用 `zh-Hant`，正文与简体字形转换版本对应。初次渲染前文章隐藏，避免闪现错误语言。没有 JavaScript 时显示四语言启用提示。

主题继续由 `theme-init.js` 和 `site.js` 管理，保存到既有 `qihangstudio-theme`，没有独立主题系统。长文和中日文字体在 `notes.css` 中维护；About 布局使用 `pages.css`。共享页眉、Logo 和移动导航使用 `site.css`；主题和滚动指示器仍复用原有实现。

## 中文版本与明體

菜单现在为“中文简体”和“中文繁體”，两项固定使用各自的黑体／无衬线字体，字重与其他语言选项一致（400）。简繁标题与繁中正文保留明體栈；简中正文单独使用随站点提供的 Noto Serif SC 400，详见 `assets/fonts/README.md`。语言菜单使用各语言的无衬线字体：Manrope、PingFang SC／TC、Hiragino Sans 等；各选项从 400 字重校准，不使用滤镜、文字描边或强制细字面。

繁体界面字典存放在 `site.js` 的 `translations['zh-Hant']`，由合并后的简体界面文案作字形转换生成。繁体正文位于同页 `data-essay-language="zh-Hant"` 模板，直接对应简体版的 32 段、署名、诗行和强调，未重新翻译或改写。更新简体内容时，应同步更新对应繁体字典／模板；不能只更新其中一份。原英文、简体、日文、法文模板不变。

## 中文段落与可读性

简繁普通段落均使用 `text-indent: 2em` 首行缩进，不向原文添加空格。诗行（`essay-verse`）、独立问句／反思／对话（`essay-special`）、署名（`essay-byline`）居中且不缩进。段落的原始文本、标点与内联标签保持不变。

按作者最新要求，正文中的 `strong`／`b` 只保留源语义，显示字重继承正常正文，不再加粗。简中正文使用真实 Noto Serif SC 400，桌面 19px、移动／平板 18px、行高 1.85、字距 0，左对齐，最大列宽 680px。浅色正文颜色单独提高对比度，深色继续使用原有 `--copy`。英、法、日正文排版不变。
