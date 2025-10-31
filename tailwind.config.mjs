import typography from '@tailwindcss/typography';

/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      fontFamily: {
        'sans': [
          '-apple-system',
          'BlinkMacSystemFont',
          '"SF Pro SC"',
          '"Noto Sans SC"',
          '"Segoe UI"',
          'Roboto',
          '"Helvetica Neue"',
          'Arial',
          '"PingFang SC"',
          '"Hiragino Sans GB"',
          '"Microsoft YaHei"',
          'sans-serif'
        ],
        'mono': [
          'ui-monospace',
          'SFMono-Regular',
          'Menlo',
          'Consolas',
          '"JetBrains Mono"',
          'monospace'
        ]
      },
      colors: {
        bg: 'var(--bg)',
        fg: 'var(--fg)',
        muted: 'var(--muted)',
        primary: 'var(--primary)',
        link: 'var(--link)',
        border: 'var(--border)',
        'code-bg': 'var(--code-bg)',
        'code-fg': 'var(--code-fg)'
      },
      maxWidth: {
        'a4': '896px'
      }
    },
  },
  plugins: [typography],
  typography: {
    extend: {
      colors: {
        DEFAULT: 'var(--fg)',
        heading: 'var(--fg)',
        link: 'var(--link)',
        code: 'var(--code-fg)',
        quote: 'var(--muted)',
        hr: 'var(--border)'
      },
      fontFamily: {
        sans: ['var(--font-sans)'],
        mono: ['var(--font-mono)']
      }
    }
  }
}