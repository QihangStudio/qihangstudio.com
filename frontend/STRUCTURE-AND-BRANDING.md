# 网站结构与 Logo 集成说明

## 完成的五项改动

1. Solutions、Gallery、About 各有独立目录与阅读页面，页眉、移动导航和首页三个入口指向对应页面。首页仍只有三个主栏目。
2. About 上方使用原头像的自然比例双栏布局，下方成为 Personal Notes 主入口。Me & Art 初始关闭，支持点击、Enter 和空格展开／收起，`aria-expanded`、+／− 与状态同步。两条 Coming Soon 分别代表待添加文章与待添加合集，均不可点击。
3. 全部九个 HTML 页面，包括兼容跳转页，均包含同一滚动轨道及共享脚本。820px 及以下继续采用首页既有的隐藏策略；桌面沿用原位置、颜色和进度算法。内容高度变化会重新计算进度。
4. 从原 PSD 图层和路径导出真实透明 Logo，集成到每页的同一个品牌首页链接。最终悬停设计以紫色向左上推进为准，450ms ease-in-out，停留时保持、离开时反向恢复。图形和 alpha 不变，未使用位移、旋转、缩放、染色或滤镜。
5. 每页引用统一的 ICO、16／32px PNG favicon 和 180px Apple touch icon。

## 本轮文件清单

修改：

- `frontend/index.html`
- `frontend/assets/site.css`
- `frontend/assets/site.js`
- `frontend/notes/index.html`
- `frontend/notes/me-and-art/index.html`
- `frontend/notes/arts-got-problems/index.html`
- `frontend/notes/before-the-next-stroke/index.html`
- `frontend/notes/within-the-mist/index.html`
- `frontend/notes/README.md`

新增：

- `frontend/solutions/index.html`
- `frontend/gallery/index.html`
- `frontend/about/index.html`
- `frontend/assets/about.js`
- `frontend/assets/pages.css`
- `frontend/assets/brand/logo.png`（680×680，原色透明 PNG）
- `frontend/assets/brand/logo-hover.png`（680×680，悬停透明 PNG）
- `frontend/assets/brand/logo-color.png`（内部不透明 RGB 渐变场）
- `frontend/assets/brand/logo-hover-color.png`（内部悬停 RGB 渐变场）
- `frontend/assets/brand/logo.svg`（原始贝塞尔路径、描边和镂空遮罩，无嵌入位图）
- `frontend/assets/brand/favicon.ico`（16、32、48px）
- `frontend/assets/brand/favicon-16.png`
- `frontend/assets/brand/favicon-32.png`
- `frontend/assets/brand/apple-touch-icon.png`（180px）
- `frontend/assets/brand/README.md`（Logo 来源、处理方法与精度说明）
- `frontend/STRUCTURE-AND-BRANDING.md`（本说明）

移动，内容不变：

- `frontend/pfp.jpg` → `frontend/about/pfp.jpg`

保持不变：原始 PSD、两份 Word 原稿、文章四语言模板、主题偏好 key、语言偏好 key、Cloudflare 配置、`data-solutions/`。首页主内容除三个栏目链接的目标地址以外与之前一致。

## Logo 保真与交互

PSD 中的白色描边作为透明度扣除处理，未按“删除所有白色像素”的方式处理。抗锯齿和浅色渐变保留；输出裁去原稿外部空白，不改变图形比例。PNG 铺白后与 PSD 合并图的平均 RGB 误差为 0.0334／255，最大 2／255，属于图层合成与整数舍入差异。

悬停 PNG 与默认 PNG 的 alpha 逐字节相同。高不透明度像素中，以色相 250°–285°估计的紫色面积从约 17% 增至 61%；紫色区域中心向左上分别移动约图案宽度的 18.1% 和 18.1%。页眉直接显示原始 PNG，并在隔离的透明容器中用 plus-lighter 对两份透明 PNG 作互补透明度交叉渐变，保持 alpha 不变。没有加法混合支持时保持默认 PNG。已移除外部 CSS mask 依赖，避免 file:// 下遮罩失败导致 Logo 消失。

SVG 保留原始矢量几何，渐变采用原色场的密集采样。Photoshop 的逐像素抖动不能由纯矢量渐变逐像素复制；网页和 favicon 使用的 PNG 是默认像素外观的依据。SVG 已与 PNG 在浏览器中并排检查。

触摸／粗指针保持默认 Logo；减少动态效果偏好下不播放过渡。键盘聚焦品牌链接可以得到同样的颜色场效果。

## 语言与导航

仍使用 `qihangstudio-language` 与 `qihangstudio-theme`，共享原有菜单与交互，没有新增独立偏好系统。About 新文案提供英文、简体中文、日文和法文。文章模板与四语言内容保持完整，返回链接现在直接到 About 的 Personal Notes 区域。

旧 `/notes/`、`/notes/me-and-art/`、`/notes/arts-got-problems/` 路径保留兼容跳转。资源和导航继续使用相对路径，使直接打开本地 HTML 时不会再次丢失样式；部署后仍对应目录页面。移动设备上在固定页眉下方提供同一组三个页面链接，不增加第四主栏目。

## 验证结果

- 已在浏览器检查 320、375、390、430、768、820、1024、1280、1440、1920px 宽度。
- About、首页和长文章页在上述宽度无横向溢出，页眉 Logo／品牌文字／控件不碰撞。
- 展开后的 About 在十个宽度 × 四种语言的 40 组检查中均通过：无横向溢出，Coming Soon 无链接，展开状态正确。
- Solutions、Gallery 和 Within the Mist 在 320px 下的四语言检查通过。
- 五个主要子页面的 Light／Dark／System 共 15 组检查通过，均有 favicon 和原滚动轨道。
- 语言与主题在跨页导航、刷新后保留。文章通过菜单和返回链接进入／退出正常。
- Me & Art 默认关闭；Enter、空格展开／收起正常，+／− 与 `aria-expanded` 同步。
- 文章滚动轨道到末尾时进度为 1，深色模式末端颜色为原有 `rgb(143, 162, 255)`。
- 首页直方图点击重生成仍正常。
- 原文章四份模板逐字比较不变；Word 和 PSD 的 SHA-256 不变。
- 九页 HTML 标签配对、唯一 ID、相对资源路径和链接目标检查通过；JavaScript 语法与 `git diff --check` 通过；浏览器未发现 JavaScript 错误。

## 内容与验证限制

没有完整个人简介或项目材料，因此 About 使用既有工作室介绍并标明详细介绍待补充；Solutions／Gallery 只显示已有说明和 Coming Soon。《Within the Mist》仍等待原稿，没有生成正文或替代翻译。

浏览器验证使用本地 HTTP 静态服务器与模拟视口，并非实际 iPad／手机硬件。`file://` 的自动浏览器访问受工具限制，因此仅验证其相对文件路径；实际跨文件存储偏好仍由浏览器策略决定。减少动态效果和触摸设备行为由媒体查询及原有触摸事件支持，未改变系统设置进行硬件级验证。

未安装新依赖、未修改部署配置、未运行 commit／push／deploy。

## 本地 Logo 与语言菜单修复

移除了可能在 file:// 下失败的外部 CSS mask，原始 PNG 不再被隐藏。悬停改为隔离容器中的 plus-lighter 互补交叉渐变。语言名称使用固定的自身语种字体、字号和行高，不随页面语言改变；同时兼容偏好值 zh-CN。320px 与 1280px 的反复四语言切换中，“中文”均保持 32px 宽、16px 字号及 44px 行高；各活动页面的原始 Logo 图片加载且可见。HTTP 浏览器检查通过，file:// 自动访问仍受工具限制。

悬停配色按最新要求加强为约 60% 紫色（实测约 61.1%），黄色基本退场；默认 Logo、SVG、favicon、透明镂空和 450ms ease-in-out 规则均保持不变。

## 简繁中文与明體更新

全部九页语言菜单改为“中文简体”并新增“中文繁體”，中文标签字重与其他语言选项一致（300）。新增 `zh-Hant` 界面字典与全文模板，内容对应当前简体版转换，不新增文章、不重写原文。中文标题与长文从原宋体栈切换为 MingLiU／PMingLiU／LiSong Pro／Noto Serif TC 明體栈；中文 UI 仍保留各语种无衬线字体。沿用原 localStorage key，支持跨页与刷新持久化。已检查 320、390、820、1280px 的简繁正文无溢出，均为 32 段、6 行诗。字体显示依设备可用明體及网络字体加载情况回退。

## 简繁字体分别设置与菜单视觉校准

按最新要求，简中标题和正文恢复宋体，繁中保留明體。语言菜单里的日文名称改用本机真实 Hiragino W2 细字面，以解决 W3 与中文 Light 虽然 CSS 字重相同、实际笔画却偏重的问题。所有菜单标签保持相同字号、行高、CSS 字重和稳定的自身语种字体，并禁止人工合成字重；不修改文章内容或语言转换。

最新字体选择：简体标题与正文也改回明體，与繁体使用相同明體栈；语言菜单的字体与视觉校准保持不变。

## 中文长文与语言菜单最新排版

本轮只调整简中正文的阅读字体和参数、简繁段落格式，以及语言选择器的字重。简中正文现在使用随站点附带的 Noto Serif SC 真正 400 字重，835 个所需字形均已核对；字体作为 WOFF 嵌入独立本地 CSS，兼容直接打开 HTML，不依赖外部字体服务器。桌面 19px、移动／平板 18px，行高 1.85，字距 0，左对齐，列宽最多 680px；浅色文字为 #353532，深色沿用原配色。简繁普通段落首行缩进两字，诗行、独立问句、反思、对话与署名居中；原始文本和段落未重写。依作者最后一条要求，正文原有粗体取消加粗显示，保留原内联标签。

语言选项恢复各自标准无衬线栈并统一从 400 字重校准，保留字号、行高、44px 触摸行高、选中勾、悬停与菜单动画。原日文 W2 映射移除。

字体加载 QA 已通过浏览器 FontFace API 确认为 Noto Serif SC、400、loaded。已验证 320、390、768、820、1024、1440px 的简繁缩进、诗行居中、无粗体及无横向溢出。所有原文字符与原段落内联内容逐段比较相同；英、日、法模板逐字节相同。

文件变化：assets/notes.css、assets/site.css、notes/before-the-next-stroke/index.html、notes/README.md、本说明；新增 assets/fonts/noto-serif-sc.css、assets/fonts/OFL-NotoSerifSC.txt、assets/fonts/README.md。未修改语言／主题脚本、导航逻辑或部署配置。
