// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require('prism-react-renderer/themes/github');
const darkCodeTheme = require('prism-react-renderer/themes/dracula');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Alan Guedes',
  url: 'https://alanlivio.github.io',
  baseUrl: '/',
  trailingSlash: true,
  onBrokenLinks: 'throw',
  deploymentBranch: 'gh-pages',
  onBrokenMarkdownLinks: 'warn',
  organizationName: 'alanlivio',
  projectName: 'alanlivio.github.io',
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },
  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: false,
          routeBasePath: '/',
          remarkPlugins: []
        },
        blog: false,
        theme: {
          customCss: [require.resolve('./src/css/custom.css')],
        },
        sitemap: false
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      colorMode: {
        defaultMode: 'dark',
        disableSwitch: true,
        respectPrefersColorScheme: false,
      },
      navbar: {
        hideOnScroll: false,
        title: 'Alan Guedes',
        items: [
          {
            type: 'doc',
            docId: 'research',
            position: 'left',
            label: 'Research Interests',
          },
          {
            type: 'doc',
            docId: 'tools',
            position: 'left',
            label: 'Tools',
          },
          {
            type: 'doc',
            docId: 'social-impact',
            position: 'left',
            label: 'Social Impact',
          },
          // {to: '/blog', label: 'Blog', position: 'left'},
          {
            href: 'https://github.com/alanlivio',
            label: 'GitHub',
            className: 'header-github-link',
            'aria-label': 'GitHub repository',
            position: 'left',
          },
          {
            href: 'https://scholar.google.com/citations?user=1bEOmkUAAAAJ',
            label: 'Scholar',
            position: 'left',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          // {
          //   title: 'Social Links',
          //   items: [
          //     {
          //       label: 'LinkedIn',
          //       href: 'https://linkedin.com/alanlivio',
          //     },
          //     {
          //       label: 'Twitter',
          //       href: 'https://twitter.com/alanlivio',
          //     },
          //   ],
          // },
        ],
        copyright: `Creative Commons. Built with <a href="http://docusaurus.io">Docusaurus<a/>.`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
    }),
};

module.exports = config;
