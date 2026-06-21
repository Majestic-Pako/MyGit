const DEFAULT_META = {
  icon: null,
  label: 'Code',
  accent: '#8b949e',
}

const LANGUAGE_META = {
  javascript: { icon: 'simple-icons:javascript', label: 'JS', accent: '#d8a657' },
  typescript: { icon: 'simple-icons:typescript', label: 'TS', accent: '#79c0ff' },
  python: { icon: 'simple-icons:python', label: 'Py', accent: '#58a6ff' },
  java: { icon: 'devicon:java', label: 'Java', accent: '#f59e6c' },
  vue: { icon: 'simple-icons:vuedotjs', label: 'Vue', accent: '#42b883' },
  react: { icon: 'simple-icons:react', label: 'React', accent: '#61dafb' },
  angular: { icon: 'simple-icons:angular', label: 'Angular', accent: '#dd315a' },
  html: { icon: 'simple-icons:html5', label: 'HTML', accent: '#e34c26' },
  css: { icon: 'simple-icons:css', label: 'CSS', accent: '#663399' },
  scss: { icon: 'simple-icons:sass', label: 'SCSS', accent: '#cc6699' },
  sass: { icon: 'simple-icons:sass', label: 'Sass', accent: '#cc6699' },
  php: { icon: 'simple-icons:php', label: 'PHP', accent: '#777bb4' },
  laravel: { icon: 'simple-icons:laravel', label: 'Laravel', accent: '#ff5a50' },
  blade: { icon: 'simple-icons:laravel', label: 'Blade', accent: '#f05340' },
  'c#': { icon: 'simple-icons:csharp', label: 'C#', accent: '#9b4f96' },
  'c++': { icon: 'simple-icons:cplusplus', label: 'C++', accent: '#f34b7d' },
  c: { icon: 'simple-icons:c', label: 'C', accent: '#8f9bb3' },
  go: { icon: 'simple-icons:go', label: 'Go', accent: '#00add8' },
  rust: { icon: 'simple-icons:rust', label: 'Rust', accent: '#dea584' },
  ruby: { icon: 'simple-icons:ruby', label: 'Ruby', accent: '#cc342d' },
  kotlin: { icon: 'simple-icons:kotlin', label: 'Kotlin', accent: '#a97bff' },
  swift: { icon: 'simple-icons:swift', label: 'Swift', accent: '#f05138' },
  dart: { icon: 'simple-icons:dart', label: 'Dart', accent: '#54c5f8' },
  flutter: { icon: 'simple-icons:flutter', label: 'Flutter', accent: '#54c5f8' },
  shell: { icon: 'simple-icons:gnubash', label: 'Shell', accent: '#89e051' },
  powershell: { icon: 'simple-icons:powershell', label: 'PowerShell', accent: '#5391fe' },
  dockerfile: { icon: 'simple-icons:docker', label: 'Docker', accent: '#2496ed' },
  sql: { icon: 'mdi:database-outline', label: 'SQL', accent: '#8b949e' },
  mysql: { icon: 'simple-icons:mysql', label: 'MySQL', accent: '#4479a1' },
  postgresql: { icon: 'simple-icons:postgresql', label: 'PostgreSQL', accent: '#4169e1' },
  sqlite: { icon: 'simple-icons:sqlite', label: 'SQLite', accent: '#80c2e8' },
  'jupyter notebook': { icon: 'simple-icons:jupyter', label: 'Jupyter', accent: '#f37626' },
  r: { icon: 'simple-icons:r', label: 'R', accent: '#75aadb' },
  matlab: { icon: 'simple-icons:mathworks', label: 'MATLAB', accent: '#e16737' },
  perl: { icon: 'simple-icons:perl', label: 'Perl', accent: '#39457e' },
  lua: { icon: 'simple-icons:lua', label: 'Lua', accent: '#7f7fff' },
  elixir: { icon: 'simple-icons:elixir', label: 'Elixir', accent: '#a078b5' },
  haskell: { icon: 'simple-icons:haskell', label: 'Haskell', accent: '#a78bfa' },
  scala: { icon: 'simple-icons:scala', label: 'Scala', accent: '#dc322f' },
  'objective-c': { icon: 'simple-icons:apple', label: 'Objective-C', accent: '#a8b0b8' },
  groovy: { icon: 'simple-icons:apachegroovy', label: 'Groovy', accent: '#4298b8' },
  yaml: { icon: 'simple-icons:yaml', label: 'YAML', accent: '#cb171e' },
  json: { icon: 'simple-icons:json', label: 'JSON', accent: '#b8b8b8' },
  markdown: { icon: 'simple-icons:markdown', label: 'Markdown', accent: '#b8b8b8' },
}

const LANGUAGE_ALIASES = {
  'vue.js': 'vue',
  vuejs: 'vue',
  'react.js': 'react',
  reactjs: 'react',
  'angular.js': 'angular',
  angularjs: 'angular',
  html5: 'html',
  css3: 'css',
  csharp: 'c#',
  cpp: 'c++',
  golang: 'go',
  bash: 'shell',
  'shell script': 'shell',
  ps1: 'powershell',
  docker: 'dockerfile',
  postgres: 'postgresql',
  jupyter: 'jupyter notebook',
  objectivec: 'objective-c',
  md: 'markdown',
  yml: 'yaml',
}

export function normalizeLanguageName(languageName) {
  const normalizedName = String(languageName || '').trim().toLowerCase()
  return LANGUAGE_ALIASES[normalizedName] || normalizedName
}

export function getLanguageMeta(languageName) {
  const normalizedName = normalizeLanguageName(languageName)
  const knownMeta = LANGUAGE_META[normalizedName]

  if (!knownMeta && normalizedName) {
    const fallbackAccents = ['#8b949e', '#f59e6c', '#79c0ff', '#a78bfa', '#56d4c0', '#e879a9']
    const accentIndex = [...normalizedName]
      .reduce((sum, character) => sum + character.charCodeAt(0), 0) % fallbackAccents.length

    return {
      ...DEFAULT_META,
      accent: fallbackAccents[accentIndex],
    }
  }

  return {
    ...DEFAULT_META,
    ...knownMeta,
  }
}

export function getLanguageIcon(languageName) {
  return getLanguageMeta(languageName).icon
}

export function getLanguageAccent(languageName) {
  return getLanguageMeta(languageName).accent
}
