# Personal Notes 内容维护

## 入口与原稿

Personal Notes 位于 `../about/index.html#personal-notes`。Me & Art 默认折叠；展开后按 01–04 的原稿顺序列出四篇文章。旧 Notes／合集 URL 仍跳转到这个入口。

| 序号 | 中文标题 | 阅读路由 | 原稿目录（均位于 `me-and-art/`） |
| --- | --- | --- | --- |
| 01 | 落笔之前 | `before-the-next-stroke/` | `01 Before the Next Stroke/` |
| 02 | 迷雾之中 | `within-the-mist/` | `02 Within the Mist/` |
| 03 | 坠入记忆的汪洋 | `falling-into-the-oceanic-expanse-of-memory/` | `03 Falling into the Oceanic Expanse of Memory/` |
| 04 | 这里的符号丝线交织 | `the-signifiers-here-are-chained/` | `04 The Signifiers Here are Chaîned/` |

每个目录都有作者提供的 EN／CN Word 原稿。04 的两个文件名仍为 `Falling into the Oceanic Expanse of Memory CN.docx`／`EN.docx`，但正文标题及内容确为 04；网页以正文为准，没有改名或修改原文件。目录里的 Coming Soon 保留在现有层级。

## 原文与翻译

每篇阅读页都包含 en、zh、zh-Hant、ja、fr 五个静态模板，使用同一个 URL 和既有语言切换逻辑。简中内部语言代码为 `zh`，正文使用 `lang="zh-CN"`；繁中使用 `zh-Hant`。

02–04 的英文、简中正文从 Word 的正文段落提取，保留文字、标点、空格和段落顺序，没有修正文中的原有表达。标题与署名单独呈现，文件末尾的空白段落不写入网页。03 英文原稿开头重复出现两次标题，中间为空行；网页仅在标题处显示一次，不将重复标题当作正文。三个新增稿件均无图片、表格、脚注或正文强调格式。

| 文章 | 英文正文段落 | 简中／繁中正文段落 | 日文／法文正文段落 |
| --- | --- | --- | --- |
| 02 | 17 | 17 | 17 |
| 03 | 28 | 28 | 28 |
| 04 | 26 | 24 | 26 |

繁中从简中作字形转换，保留对应内容与分段。日法译文遵循作者确定的原则：意思参考英文，意境参考中文；逐段对应英文，不概括、省略或补入中文独有内容。02–04 中人物、曼陀林、海、表象／真实、能指链条的反复意象保持连贯。04 日文使用「シニフィアン」、法文使用 « signifiant »。

01 的正文及已有译文此次未修改。01 的中文曾有一处经作者授权的含义调整，将“一人觉得有艺术性就不能否认它是艺术”改为与英文一致的“至少拥有一位欣赏者”；原始 Word 一直保留原样。

## 当前排版约定

- 标题缩小居中，细线位于标题上方；署名只保留名字：启航／啟航／啓航／Qihang。
- 普通正文段落两端对齐。简繁中文首行缩进 `2em`，不向原文插入空格。
- 对话仍是普通段落。诗歌、明确标记的特殊段落及署名居中且不缩进；新增三篇没有诗歌或特殊居中段落。
- 简中使用本机 Songti SC Light（真实 300 字重），并保留现有 Noto Serif SC 等备用字体；桌面 19px，平板／手机 18px，行高 1.85，字距 0，列宽最多 680px。其他语言继承现有字体与响应式样式。
- 新增三篇正文没有粗体；不要额外添加。既有 `em`／`strong` 标签的语义与显示遵循 `notes.css`，不在新增页面中覆盖全站样式。

## 维护与核查

1. 保留作者原稿。核对 Word 正文标题，不能只根据文件名判断文章内容。
2. 每个阅读页包含五个 `<template data-essay-language="…" data-essay-lang="…">`，模板内为 `h1` 与 `.essay-body`。`data-source-paragraph` 是原始 Word 段落的 1 起始序号；日法使用对应英文段落的序号。
3. 正文不使用 UI 的 `data-i18n`。新增目录标题加入 `assets/site.js` 的对应语言字典。
4. `notes.js` 必须在 `site.js` 前加载，模板放在两者之前。正文仍从本页模板克隆，无额外 fetch。
5. 简中增加字符时，重新生成 `assets/fonts/noto-serif-sc.css` 的所有简中文章字符并集，避免备用字体缺字；保留许可证及真实字重。当前子集已覆盖 01–04。
6. 核对五种语言全文、目录跳转、重载与跨页语言偏好；检查桌面／平板／320px 手机、Light／Dark／System 及滚动指示器。页眉、菜单、主题、About 介绍和布局不属于文章内容更新的改动范围。

语言与主题偏好仍分别使用 `qihangstudio-language` 和 `qihangstudio-theme`。`site.js` 发出 `studio:language-change`，`notes.js` 更新标题、正文及 `lang`。关闭 JavaScript 时显示启用提示；直接 HTML 预览不依赖正文网络请求，跨页偏好以 HTTP 预览／正式站点为准。
