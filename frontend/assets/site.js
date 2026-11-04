    // ---------------------------------------------------------------
    // Local copy for the shared interface. Only marked text is replaced.
    // Titles share one phrase sequence so source spans cannot split a phrase.
    // Keep manifesto segments adjacent to preserve language-specific spacing.
    // ---------------------------------------------------------------
    const translations = {
      en: {
        'meta.description': 'Qihang Studio — data, image, and the stories between them.',
        'nav.label': 'Primary navigation',
        'nav.solutions': 'Solutions',
        'nav.gallery': 'Gallery',
        'nav.about': 'About',
        'appearance.label': 'Appearance',
        'appearance.system': 'System',
        'appearance.light': 'Light',
        'appearance.dark': 'Dark',
        'appearance.hint': 'Click to switch light/dark. Right-click or long-press for options; press Arrow Down with the keyboard.',
        'appearance.status': 'Appearance: {preference}. Current theme: {theme}.',
        'language.label': 'Language',
        'language.choose': 'Choose language',
        'hero.titleLine1': 'Data, image, and stories',
        'hero.titleLine2': 'in conversation.',
        'hero.description': 'A personal studio for statistical thinking, visual practice, and experiments in how information can be understood — and seen.',
        'hero.location': 'Ann Arbor / Nanjing',
        'hero.studio': 'Studio',
        'practice.label': 'Explore',
        'practice.title': 'Three ways in.',
        'practice.description': 'The site is intentionally simple for now: three spaces, each reflecting a different way I work — analytical, visual, and personal.',
        'solutions.description': 'Data analysis, statistical reasoning, research, and computational work — organized around questions rather than software.',
        'gallery.description': 'A visual archive for drawing, design, image-making, and experiments that do not need to become “projects.”',
        'about.description': 'The thread connecting art, statistics, computation, and research — plus experience, CV, and contact.',
        'manifesto.label': 'Studio note',
        'manifesto.before': 'Not everything worth understanding begins as a dataset. Some things begin as an ',
        'manifesto.emphasis': 'image',
        'manifesto.after': ', a question, or a story that has not yet been told.',
        'footer.email': 'Email'
      },
      zh: {
        'meta.description': 'Qihang Studio — 数据、影像，以及其间的故事。',
        'nav.label': '主导航',
        'nav.solutions': '方法',
        'nav.gallery': '图集',
        'nav.about': '关于',
        'appearance.label': '外观',
        'appearance.system': '跟随系统',
        'appearance.light': '浅色',
        'appearance.dark': '深色',
        'appearance.hint': '点击切换浅色／深色；右键或长按打开选项，键盘可按向下方向键。',
        'appearance.status': '外观设置：{preference}。当前主题：{theme}。',
        'language.label': '语言',
        'language.choose': '选择语言',
        'hero.titleLine1': '数据成形，影像显现，叙事赋义。',
        'hero.titleLine2': '',
        'hero.description': '一个个人工作室，以统计思维与视觉实践，探索理解信息、看见信息的不同方式。',
        'hero.location': '安娜堡 / 南京',
        'hero.studio': '启航工作室',
        'practice.label': '探索',
        'practice.title': '三径通幽。',
        'practice.description': '网站暂且保持简单：三个空间，分别呈现我的分析探索、视觉实践与个人经历。',
        'solutions.description': '数据分析、统计推理、研究与计算——从问题出发，而非围绕软件展开。',
        'gallery.description': '收录绘画、设计与影像创作，也留下一些不必成为「项目」的实验。',
        'about.description': '串联艺术、统计、计算与研究的线索，以及个人经历、简历与联系方式。',
        'manifesto.label': '工作室手记',
        'manifesto.before': '值得理解的事物，并非都始于数据。有些始于一幅',
        'manifesto.emphasis': '影像',
        'manifesto.after': '、一个问题，或一段尚未讲述的故事。',
        'footer.email': '邮件'
      },
      ja: {
        'meta.description': 'Qihang Studio — データ、イメージ、そのあいだにある物語。',
        'nav.label': 'メインナビゲーション',
        'nav.solutions': 'アプローチ',
        'nav.gallery': 'ギャラリー',
        'nav.about': '私について',
        'appearance.label': '外観',
        'appearance.system': 'システム',
        'appearance.light': 'ライト',
        'appearance.dark': 'ダーク',
        'appearance.hint': 'クリックでライト／ダークを切り替え。右クリック、長押し、または下矢印キーで選択肢を表示。',
        'appearance.status': '外観設定：{preference}。現在のテーマ：{theme}。',
        'language.label': '言語',
        'language.choose': '言語を選ぶ',
        'hero.titleLine1': 'データは形をなし、イメージは現れ、物語は意味を与える。',
        'hero.titleLine2': '',
        'hero.description': '統計的思考と視覚表現を通して、情報の捉え方、見え方を探る個人スタジオ。',
        'hero.location': 'アナーバー / 南京',
        'hero.studio': 'スタジオ',
        'practice.label': '探る',
        'practice.title': '三つの道、奥へと続く。',
        'practice.description': '今は、シンプルな構成に。分析、視覚表現、そして私自身について。三つの場所から、日々の取り組みを紹介します。',
        'solutions.description': 'データ分析、統計的推論、研究、計算。ソフトウェアではなく、問いを起点にした取り組み。',
        'gallery.description': 'ドローイング、デザイン、イメージの制作を集めた視覚のアーカイブ。「プロジェクト」にならない実験も、ここに。',
        'about.description': 'アート、統計、計算、研究をつなぐもの。これまでの歩み、経歴、連絡先も。',
        'manifesto.label': '啓航スタジオノート',
        'manifesto.before': '理解したいことのすべてが、データから始まるわけではない。一つの',
        'manifesto.emphasis': 'イメージ',
        'manifesto.after': 'や問い、まだ語られていない物語から始まることもある。',
        'footer.email': 'メール'
      },
      fr: {
        'meta.description': 'Qihang Studio — données, images et récits qui les relient.',
        'nav.label': 'Navigation principale',
        'nav.solutions': 'Approches',
        'nav.gallery': 'Galerie',
        'nav.about': 'À propos',
        'appearance.label': 'Apparence',
        'appearance.system': 'Système',
        'appearance.light': 'Clair',
        'appearance.dark': 'Sombre',
        'appearance.hint': 'Cliquez pour alterner clair et sombre. Clic droit, appui long ou flèche bas pour les options.',
        'appearance.status': 'Apparence : {preference}. Thème actuel : {theme}.',
        'language.label': 'Langue',
        'language.choose': 'Choisir la langue',
        'hero.titleLine1': 'Données, images et récits en dialogue.',
        'hero.titleLine2': '',
        'hero.description': 'Un atelier personnel où se croisent réflexion statistique, pratique visuelle et expérimentations sur nos façons de comprendre — et de voir — l’information.',
        'hero.location': 'Ann Arbor / Nankin',
        'hero.studio': 'Atelier',
        'practice.label': 'Explorer',
        'practice.title': 'Trois portes d’entrée.',
        'practice.description': 'Pour l’instant, le site reste simple : trois espaces pour trois facettes de mon travail — analytique, visuelle et personnelle.',
        'solutions.description': 'Analyse de données, raisonnement statistique, recherche et calcul : des travaux guidés par les questions, plutôt que par les logiciels.',
        'gallery.description': 'Des archives visuelles de dessins, de créations graphiques, d’images et d’expériences qui n’ont pas besoin de devenir des « projets ».',
        'about.description': 'Le fil qui relie l’art, les statistiques, le calcul et la recherche. Et aussi : mon parcours, mon CV et mes coordonnées.',
        'manifesto.label': 'Note d’atelier',
        'manifesto.before': 'Tout ce qui mérite d’être compris ne commence pas par des données. Parfois, tout commence par une ',
        'manifesto.emphasis': 'image',
        'manifesto.after': ', une question ou une histoire qui reste à raconter.',
        'footer.email': 'Courriel'
      }
    };
    const notesTranslations = {
  "en": {
    "notes.heading": "Personal Notes.",
    "notes.subtitle": "Essays, reflections, and fragments on art, perception, and the ways we understand the world.",
    "notes.nav": "Personal Notes",
    "notes.personal": "Personal Essay",
    "notes.critical": "Critical Essay / Aesthetics",
    "notes.back": "Back to Personal Notes",
    "notes.home": "Home",
    "notes.pending": "Essay text has not been added yet.",
    "notes.placeholder": "Content placeholder",
    "notes.index": "Article index"
  },
  "zh": {
    "notes.heading": "个人札记。",
    "notes.subtitle": "关于艺术、感知，以及我们理解世界的方式的随笔、思考与片段。",
    "notes.nav": "个人札记",
    "notes.personal": "个人随笔",
    "notes.critical": "评论文章 / 美学",
    "notes.back": "返回个人札记",
    "notes.home": "首页",
    "notes.pending": "文章正文尚未添加。",
    "notes.placeholder": "正文占位",
    "notes.index": "文章目录"
  },
  "ja": {
    "notes.heading": "個人ノート。",
    "notes.subtitle": "アート、知覚、そして世界の捉え方をめぐるエッセイ、思索、断章。",
    "notes.nav": "個人ノート",
    "notes.personal": "個人エッセイ",
    "notes.critical": "批評 / 美学",
    "notes.back": "個人ノートへ戻る",
    "notes.home": "ホーム",
    "notes.pending": "本文はまだ追加されていません。",
    "notes.placeholder": "本文のプレースホルダー",
    "notes.index": "記事一覧"
  },
  "fr": {
    "notes.heading": "Notes personnelles.",
    "notes.subtitle": "Essais, réflexions et fragments sur l’art, la perception et nos façons de comprendre le monde.",
    "notes.nav": "Notes personnelles",
    "notes.personal": "Essai personnel",
    "notes.critical": "Essai critique / Esthétique",
    "notes.back": "Retour aux notes personnelles",
    "notes.home": "Accueil",
    "notes.pending": "Le texte de cet essai n’a pas encore été ajouté.",
    "notes.placeholder": "Texte à venir",
    "notes.index": "Liste des articles"
  }
};
    const essayInterfaceTranslations = {
  "en": {
    "notes.collection": "Me & Art",
    "notes.coming": "Coming Soon",
    "notes.stroke": "Before the Next Stroke",
    "notes.unavailable": "The original documents for this essay have not been provided yet.",
    "notes.noScript": "Please enable JavaScript to select a reading language.",
    "notes.reading": "Essay"
  },
  "zh": {
    "notes.collection": "我与艺术",
    "notes.coming": "敬请期待",
    "notes.stroke": "落笔之前",
    "notes.unavailable": "尚未收到这篇文章的原稿。",
    "notes.noScript": "请启用 JavaScript 以选择阅读语言。",
    "notes.reading": "文章"
  },
  "ja": {
    "notes.collection": "私とアート",
    "notes.coming": "近日公開",
    "notes.stroke": "次のひと筆の前に",
    "notes.unavailable": "このエッセイの原稿はまだ提供されていません。",
    "notes.noScript": "読む言語を選ぶには JavaScript を有効にしてください。",
    "notes.reading": "エッセイ"
  },
  "fr": {
    "notes.collection": "L’art et moi",
    "notes.coming": "À venir",
    "notes.stroke": "Avant le prochain trait",
    "notes.unavailable": "Les textes originaux de cet essai n’ont pas encore été fournis.",
    "notes.noScript": "Veuillez activer JavaScript pour choisir la langue de lecture.",
    "notes.reading": "Essai"
  }
};
    Object.keys(essayInterfaceTranslations).forEach(language => Object.assign(notesTranslations[language], essayInterfaceTranslations[language]));
    const pageTranslations = {
  "en": {
    "about.heading": "A few words from the studio’s creator",
    "about.creatorName": "Qihang",
    "about.creatorSubtitle": "Creator of Qihang Studio",
    "about.photoAlt": "Qihang Cheng seated beside the sea",
    "about.paragraph1": "Hello, fellow traveler!\nWhether or not we’ve met in the world beyond this screen, welcome to Qihang Studio.",
    "about.paragraph2": "I’m Qihang—nice to meet you! I’m currently studying data science at the University of Michigan.",
    "about.paragraph3": "I’m drawn to data, visual art, and literature. Data helps me explore the patterns of the world, images open up new ways of seeing, and words give me room to express myself and think.",
    "about.paragraph4": "Qihang Studio is a little corner I’ve made for these interests. Here, I keep a record of my research, creative work, and reflections, while trying to build a bridge between reason and feeling.",
    "pages.coming": "Coming Soon"
  },
  "zh": {
    "about.heading": "工作室创作者想对你说",
    "about.creatorName": "启航",
    "about.creatorSubtitle": "Qihang Studio 创作者",
    "about.photoAlt": "程启航坐在海边",
    "about.paragraph1": "旅者好呀！\n无论我们是否曾在现实世界中相识，都欢迎你来到 Qihang Studio。",
    "about.paragraph2": "启航～是我的名字哦。目前我就读于密歇根大学，主修数据科学。",
    "about.paragraph3": "我对数据、视觉艺术与文学都有着浓厚的兴趣。数据帮助我探索世界的规律，影像让我发现不同的观察角度，而文字则给予我表达与思考的空间。",
    "about.paragraph4": "Qihang Studio 是我为这些兴趣建立的一方天地。在这里，我记录自己的研究、创作与思考，也尝试在理性与感性之间架起一座桥梁。",
    "pages.coming": "敬请期待"
  },
  "ja": {
    "about.heading": "スタジオのつくり手から、あなたへ",
    "about.creatorName": "啓航",
    "about.creatorSubtitle": "Qihang Studio のつくり手",
    "about.photoAlt": "海辺に座る程啓航",
    "about.paragraph1": "旅人さん、こんにちは！\n現実の世界で会ったことがある方も、まだ会ったことのない方も、Qihang Studio へようこそ。",
    "about.paragraph2": "啓航（チーハン）といいます。どうぞよろしく！今はミシガン大学でデータサイエンスを専攻しています。",
    "about.paragraph3": "データ、視覚芸術、文学に心を惹かれています。データは世界の法則を探る手がかりとなり、イメージは新しいものの見方を教えてくれます。そして言葉は、自分を表現し、思いを巡らせる余白をくれます。",
    "about.paragraph4": "Qihang Studio は、そんな興味のためにつくった小さな場所です。ここでは研究や創作、日々考えたことを記録しながら、理性と感性のあいだに橋を架けようとしています。",
    "pages.coming": "近日公開"
  },
  "fr": {
    "about.heading": "Quelques mots du créateur du studio",
    "about.creatorName": "Qihang",
    "about.creatorSubtitle": "Créateur de Qihang Studio",
    "about.photoAlt": "Qihang Cheng assis au bord de la mer",
    "about.paragraph1": "Bonjour, ami de passage !\nQue nos chemins se soient déjà croisés dans le monde réel ou non, bienvenue dans Qihang Studio.",
    "about.paragraph2": "Moi, c’est Qihang ! J’étudie actuellement la science des données à l’Université du Michigan.",
    "about.paragraph3": "Les données, les arts visuels et la littérature me passionnent. Les données m’aident à explorer les régularités du monde, les images m’ouvrent de nouvelles perspectives, et les mots m’offrent un espace pour m’exprimer et réfléchir.",
    "about.paragraph4": "Qihang Studio est un petit univers que j’ai créé pour ces centres d’intérêt. J’y garde une trace de mes recherches, de mes créations et de mes réflexions, tout en essayant de tisser un lien entre raison et sensibilité.",
    "pages.coming": "À venir"
  }
};
    Object.keys(pageTranslations).forEach(language => Object.assign(notesTranslations[language], pageTranslations[language]));
    Object.keys(notesTranslations).forEach(language => Object.assign(translations[language], notesTranslations[language]));
    // Traditional Chinese mirrors the authoritative Simplified Chinese copy.
    translations['zh-Hant'] = {
      "meta.description": "Qihang Studio — 數據、影像，以及其間的故事。",
      "nav.label": "主導航",
      "nav.solutions": "方法",
      "nav.gallery": "圖集",
      "nav.about": "關於",
      "appearance.label": "外觀",
      "appearance.system": "跟隨系統",
      "appearance.light": "淺色",
      "appearance.dark": "深色",
      "appearance.hint": "點擊切換淺色／深色；右鍵或長按打開選項，鍵盤可按向下方向鍵。",
      "appearance.status": "外觀設置：{preference}。當前主題：{theme}。",
      "language.label": "語言",
      "language.choose": "選擇語言",
      "hero.titleLine1": "數據成形，影像顯現，敘事賦義。",
      "hero.titleLine2": "",
      "hero.description": "一個個人工作室，以統計思維與視覺實踐，探索理解信息、看見信息的不同方式。",
      "hero.location": "安娜堡 / 南京",
      "hero.studio": "啟航工作室",
      "practice.label": "探索",
      "practice.title": "三徑通幽。",
      "practice.description": "網站暫且保持簡單：三個空間，分別呈現我的分析探索、視覺實踐與個人經歷。",
      "solutions.description": "數據分析、統計推理、研究與計算——從問題出發，而非圍繞軟件展開。",
      "gallery.description": "收錄繪畫、設計與影像創作，也留下一些不必成為「項目」的實驗。",
      "about.description": "串聯藝術、統計、計算與研究的線索，以及個人經歷、簡歷與聯繫方式。",
      "manifesto.label": "工作室手記",
      "manifesto.before": "值得理解的事物，並非都始於數據。有些始於一幅",
      "manifesto.emphasis": "影像",
      "manifesto.after": "、一個問題，或一段尚未講述的故事。",
      "footer.email": "郵件",
      "notes.heading": "個人札記。",
      "notes.subtitle": "關於藝術、感知，以及我們理解世界的方式的隨筆、思考與片段。",
      "notes.nav": "個人札記",
      "notes.personal": "個人隨筆",
      "notes.critical": "評論文章 / 美學",
      "notes.back": "返回個人札記",
      "notes.home": "首頁",
      "notes.pending": "文章正文尚未添加。",
      "notes.placeholder": "正文佔位",
      "notes.index": "文章目錄",
      "notes.collection": "我與藝術",
      "notes.coming": "敬請期待",
      "notes.stroke": "落筆之前",
      "notes.unavailable": "尚未收到這篇文章的原稿。",
      "notes.noScript": "請啟用 JavaScript 以選擇閱讀語言。",
      "notes.reading": "文章",
      "about.heading": "工作室創作者想對你說",
      "about.creatorName": "啟航",
      "about.creatorSubtitle": "Qihang Studio 創作者",
      "about.photoAlt": "程啟航坐在海邊",
      "about.paragraph1": "旅者好呀！\n無論我們是否曾在現實世界中相識，都歡迎你來到 Qihang Studio。",
      "about.paragraph2": "啟航～是我的名字哦。目前我就讀於密歇根大學，主修數據科學。",
      "about.paragraph3": "我對數據、視覺藝術與文學都有著濃厚的興趣。數據幫助我探索世界的規律，影像讓我發現不同的觀察角度，而文字則給予我表達與思考的空間。",
      "about.paragraph4": "Qihang Studio 是我為這些興趣建立的一方天地。在這裡，我記錄自己的研究、創作與思考，也嘗試在理性與感性之間架起一座橋樑。",
      "pages.coming": "敬請期待"
};
    const LANGUAGE_STORAGE_KEY = 'qihangstudio-language';
    const languageTags = { en: 'en', zh: 'zh-CN', 'zh-Hant': 'zh-Hant', ja: 'ja', fr: 'fr' };
    let currentLanguage = 'en';
    function translate(key) {
      // Nullish fallback preserves intentionally empty hero title segments.
      return translations[currentLanguage][key] ?? translations.en[key];
    }
    // ---------------------------------------------------------------
    // Page scroll indicator
    // ---------------------------------------------------------------
    const scrollRail = document.getElementById('scrollRail');
    const scrollSpectrums = {
      light: [
        { stop: 0.00, color: [239, 189, 63] },
        { stop: 0.34, color: [235, 120, 149] },
        { stop: 0.67, color: [173, 105, 223] },
        { stop: 1.00, color: [101, 124, 242] }
      ],
      dark: [
        { stop: 0.00, color: [255, 215, 103] },
        { stop: 0.34, color: [255, 141, 170] },
        { stop: 0.67, color: [197, 140, 255] },
        { stop: 1.00, color: [143, 162, 255] }
      ]
    };
    function interpolateScrollColor(progress) {
      const theme =
        document.documentElement.dataset.theme === 'dark'
          ? 'dark'
          : 'light';
      const scrollSpectrum = scrollSpectrums[theme];
      for (let i = 0; i < scrollSpectrum.length - 1; i++) {
        const a = scrollSpectrum[i];
        const b = scrollSpectrum[i + 1];
        if (progress <= b.stop) {
          const local =
            (progress - a.stop) / (b.stop - a.stop);
          const channel = (index) =>
            Math.round(
              a.color[index] +
              (b.color[index] - a.color[index]) * local
            );
          return `rgb(${channel(0)}, ${channel(1)}, ${channel(2)})`;
        }
      }
      const last = scrollSpectrum[scrollSpectrum.length - 1].color;
      return `rgb(${last[0]}, ${last[1]}, ${last[2]})`;
    }
    function updateScrollProgress() {
      if (!scrollRail) return;
      const scrollable =
        document.documentElement.scrollHeight - window.innerHeight;
      const progress =
        scrollable > 0
          ? Math.min(1, Math.max(0, window.scrollY / scrollable))
          : 0;
      scrollRail.style.setProperty('--scroll-progress', progress);
      scrollRail.style.setProperty(
        '--scroll-color',
        interpolateScrollColor(progress)
      );
    }
    updateScrollProgress();
    window.addEventListener('scroll', updateScrollProgress, { passive: true });
    window.addEventListener('resize', updateScrollProgress);
    document.addEventListener('studio:content-resize', updateScrollProgress);
    if ('ResizeObserver' in window && document.querySelector('main')) {
      new ResizeObserver(updateScrollProgress).observe(document.querySelector('main'));
    }
    // ---------------------------------------------------------------
    // Appearance: System / Light / Dark
    // ---------------------------------------------------------------
    const THEME_STORAGE_KEY = 'qihangstudio-theme';
    const themeButton = document.getElementById('themeButton');
    const themeMenu = document.getElementById('themeMenu');
    const themeOptions = [...document.querySelectorAll('.theme-option')];
    const systemTheme = window.matchMedia('(prefers-color-scheme: dark)');
    function getThemePreference() {
      try {
        return localStorage.getItem(THEME_STORAGE_KEY) || 'system';
      } catch (_) {
        return 'system';
      }
    }
    function resolveTheme(preference) {
      if (preference === 'system') {
        return systemTheme.matches ? 'dark' : 'light';
      }
      return preference;
    }
    function updateThemeChecks(preference) {
      themeOptions.forEach((option) => {
        option.querySelector('.check')?.remove();
        if (option.dataset.themeChoice === preference) {
          const check = document.createElement('span');
          check.className = 'check';
          check.textContent = '✓';
          option.appendChild(check);
        }
      });
    }
    function applyTheme(preference, persist = true) {
      const resolved = resolveTheme(preference);
      document.documentElement.dataset.theme = resolved;
      document.documentElement.dataset.themePreference = preference;
      if (persist) {
        try {
          localStorage.setItem(THEME_STORAGE_KEY, preference);
        } catch (_) {}
      }
      updateThemeChecks(preference);
      updateScrollProgress();
      updateAppearanceLabel();
    }
    function updateAppearanceLabel() {
      const { themePreference, theme } = document.documentElement.dataset;
      themeButton.title = translate('appearance.hint');
      themeButton.setAttribute('aria-description', translate('appearance.hint'));
      themeButton.setAttribute(
        'aria-label',
        translate('appearance.status')
.replace('{preference}', translate(`appearance.${themePreference}`))
.replace('{theme}', translate(`appearance.${theme}`))
      );
    }
    function setThemeMenuOpen(open) {
      themeMenu.classList.toggle('open', open);
      themeButton.setAttribute('aria-expanded', String(open));
    }
    applyTheme(getThemePreference(), false);
    let themeHoldTimer;
    let suppressThemeClick = false;
    let themeTouchStart;

    function openThemeChoices() {
      setThemeMenuOpen(true);
      setLanguageMenuOpen(false);
    }

    themeButton.addEventListener('click', (event) => {
      event.stopPropagation();
      if (suppressThemeClick) {
        suppressThemeClick = false;
        return;
      }
      applyTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark');
      setThemeMenuOpen(false);
      setLanguageMenuOpen(false);
    });
    themeButton.addEventListener('contextmenu', (event) => {
      event.preventDefault();
      event.stopPropagation();
      openThemeChoices();
    });
    themeButton.addEventListener('keydown', (event) => {
      if (event.key === 'ArrowDown') {
        event.preventDefault();
        openThemeChoices();
        // Let the menu become visible before moving keyboard focus.
        requestAnimationFrame(() => {
          requestAnimationFrame(() => {
            if (themeMenu.classList.contains('open')) {
              themeOptions.find(option =>
                option.dataset.themeChoice === document.documentElement.dataset.themePreference
              )?.focus();
            }
          });
        });
      }
    });
    // Touch users can still choose System without a mouse.
    themeButton.addEventListener('pointerdown', (event) => {
      clearTimeout(themeHoldTimer);
      suppressThemeClick = false;
      if (event.pointerType !== 'touch') return;
      themeTouchStart = { x: event.clientX, y: event.clientY };
      themeHoldTimer = setTimeout(() => {
        suppressThemeClick = true;
        openThemeChoices();
      }, 500);
    });
    themeButton.addEventListener('pointermove', (event) => {
      if (event.pointerType === 'touch' && themeTouchStart &&
          Math.hypot(event.clientX - themeTouchStart.x, event.clientY - themeTouchStart.y) > 10) {
        clearTimeout(themeHoldTimer);
      }
    });
    ['pointerup', 'pointercancel', 'pointerleave'].forEach(type => {
      themeButton.addEventListener(type, () => clearTimeout(themeHoldTimer));
    });
    themeOptions.forEach((option) => {
      option.addEventListener('click', (event) => {
        event.stopPropagation();
        applyTheme(option.dataset.themeChoice);
        setThemeMenuOpen(false);
      });
    });
    systemTheme.addEventListener('change', () => {
      if (getThemePreference() === 'system') {
        applyTheme('system', false);
      }
    });
    // ---------------------------------------------------------------
    // Language menu and localization
    // ---------------------------------------------------------------
    const languageButton = document.getElementById('languageButton');
    const languageMenu = document.getElementById('languageMenu');
    const languageOptions = [...document.querySelectorAll('.language-option')];
    function getLanguagePreference() {
      try {
        return localStorage.getItem(LANGUAGE_STORAGE_KEY) || 'en';
      } catch (_) {
        return 'en';
      }
    }
    // Keep each punctuated phrase intact, including across the source title spans.
    function renderTitlePhrases(element, text) {
      element.replaceChildren();
      const phrases = text.match(/[^,，、。.!?！？;；:：]+[,，、。.!?！？;；:：]*/gu) || [];
      phrases.forEach((phrase, index) => {
        const leadingSpace = phrase.match(/^\s*/u)[0];
        if (leadingSpace) element.appendChild(document.createTextNode(leadingSpace));
        const span = document.createElement('span');
        span.className = 'title-phrase';
        span.textContent = phrase.slice(leadingSpace.length);
        element.appendChild(span);
        if (index < phrases.length - 1) element.appendChild(document.createElement('wbr'));
      });
    }

    let heroTitleViewportWidth = 0;

    function fitHeroTitle() {
      heroTitleViewportWidth = document.documentElement.clientWidth;
      const title = document.querySelector('.hero-title');
      if (!title) return;
      // Re-read the responsive CSS size so widening the viewport restores it.
      title.style.removeProperty('font-size');
      const available = title.clientWidth;
      const widest = Math.max(0, ...[...title.querySelectorAll('.title-phrase')]
        .map(phrase => phrase.getBoundingClientRect().width));
      if (available > 0 && widest > available) {
        const size = parseFloat(getComputedStyle(title).fontSize);
        title.style.fontSize = `${size * (available - 1) / widest}px`;
      }
      updateScrollProgress();
    }

    function applyLanguage(language, persist = true) {
      if (language === 'zh-CN' || language === 'zh-Hans') language = 'zh';
      if (language === 'zh-TW' || language === 'zh-HK') language = 'zh-Hant';
      currentLanguage = Object.prototype.hasOwnProperty.call(translations, language)
        ? language
        : 'en';
      document.documentElement.lang = languageTags[currentLanguage];
      document.querySelectorAll('[data-i18n]').forEach((element) => {
        element.textContent = translate(element.dataset.i18n);
      });
      document.querySelectorAll('[data-i18n-alt]').forEach(element => {
        element.alt = translate(element.dataset.i18nAlt);
      });
      const titleLines = [...document.querySelectorAll('.hero-title > [data-i18n]')];
      const titleText = titleLines.map(line => line.textContent).filter(Boolean).join(' ');
      titleLines.forEach((line, index) => renderTitlePhrases(line, index === 0 ? titleText : ''));
      // Only these explicit attributes are localized; markup is never injected.
      document.querySelectorAll('[data-i18n-aria-label]').forEach((element) => {
        element.setAttribute('aria-label', translate(element.dataset.i18nAriaLabel));
      });
      document.querySelectorAll('[data-i18n-content]').forEach((element) => {
        element.setAttribute('content', translate(element.dataset.i18nContent));
      });
      languageOptions.forEach((option) => {
        const selected = option.dataset.lang === currentLanguage;
        option.querySelector('.check').textContent = selected ? '✓' : '';
        option.setAttribute('aria-pressed', String(selected));
      });
      document.dispatchEvent(new CustomEvent('studio:language-change', {
        detail: { language: currentLanguage, tag: languageTags[currentLanguage] }
      }));
      updateScrollProgress();
      updateAppearanceLabel();
      // Text and font changes can alter both wrapping and scrollable height.
      fitHeroTitle();
      if (persist) {
        try {
          localStorage.setItem(LANGUAGE_STORAGE_KEY, currentLanguage);
        } catch (_) {}
      }
    }
    function setLanguageMenuOpen(open) {
      languageMenu.classList.toggle('open', open);
      languageButton.setAttribute('aria-expanded', String(open));
    }
    applyLanguage(getLanguagePreference(), false);
    window.addEventListener('resize', () => {
      // Mobile address bars trigger height-only resize events while scrolling.
      // Language/font changes still call fitHeroTitle directly.
      if (document.documentElement.clientWidth !== heroTitleViewportWidth) {
        fitHeroTitle();
      }
    });
    document.fonts.ready.then(fitHeroTitle);
    document.fonts.addEventListener('loadingdone', fitHeroTitle);
    languageButton.addEventListener('click', (event) => {
      event.stopPropagation();
      const willOpen = !languageMenu.classList.contains('open');
      setLanguageMenuOpen(willOpen);
      setThemeMenuOpen(false);
    });
    languageOptions.forEach((option) => {
      option.addEventListener('click', (event) => {
        event.stopPropagation();
        applyLanguage(option.dataset.lang);
        setLanguageMenuOpen(false);
      });
    });
    // ---------------------------------------------------------------
    // Procedural histogram
    // ---------------------------------------------------------------
    function generateHistogram() {
      const svg = document.getElementById('heroHistogram');
      const group = document.getElementById('histogramSquares');
      const gradient = document.getElementById('histogramSpectrum');
      if (!svg || !group || !gradient) return;
      const SVG_NS = 'http://www.w3.org/2000/svg';
      // Shared geometry for every square.
      const square = 18;
      const gap = 7;
      const step = square + gap;
      // This is the "personality" of the graphic:
      // mostly low on the left, increasingly tall toward the right,
      // with a few intentional dips so it does not look too mechanical.
      const baseHeights = [1, 1, 2, 2, 3, 2, 4, 3, 5, 4, 6, 8];
      const maxHeight = 8;
      const width =
        baseHeights.length * square +
        (baseHeights.length - 1) * gap;
      const height =
        maxHeight * square +
        (maxHeight - 1) * gap;
      svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
      // One shared color field across the entire histogram.
      gradient.setAttribute('x1', '0');
      gradient.setAttribute('y1', String(height));
      gradient.setAttribute('x2', String(width));
      gradient.setAttribute('y2', '0');
      group.replaceChildren();
      // Most columns stay unchanged; some move up/down by exactly one square.
      // This keeps each visit recognizably the same composition.
      const jitterChoices = [-1, 0, 0, 0, 0, 1];
      const heights = baseHeights.map((base, index) => {
        let value =
          base +
          jitterChoices[Math.floor(Math.random() * jitterChoices.length)];
        // Keep the left edge quiet.
        if (index < 2) value = 1;
        // Preserve the strong right-side visual weight.
        if (index === baseHeights.length - 3) value = Math.max(value, 4);
        if (index === baseHeights.length - 2) value = Math.max(value, 5);
        if (index === baseHeights.length - 1) value = Math.max(value, 7);
        return Math.max(1, Math.min(maxHeight, value));
      });
      const baseline = height - square;
      heights.forEach((columnHeight, column) => {
        for (let row = 0; row < columnHeight; row++) {
          const rect = document.createElementNS(SVG_NS, 'rect');
          rect.setAttribute('x', String(column * step));
          rect.setAttribute('y', String(baseline - row * step));
          rect.setAttribute('width', String(square));
          rect.setAttribute('height', String(square));
          group.appendChild(rect);
        }
      });
    }
    generateHistogram();
    // Click anywhere in the hero to gently reshuffle the histogram.
    // Links and buttons are ignored so normal UI interactions are unaffected.
    const hero = document.querySelector('.hero');
    hero?.addEventListener('click', (event) => {
      if (event.target.closest('a, button')) return;
      generateHistogram();
    });
    // Close either menu when the user clicks elsewhere or presses Escape.
    document.addEventListener('click', () => {
      setThemeMenuOpen(false);
      setLanguageMenuOpen(false);
    });
    window.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') {
        if (themeMenu.contains(document.activeElement)) themeButton.focus();
        setThemeMenuOpen(false);
        setLanguageMenuOpen(false);
      }
    });
