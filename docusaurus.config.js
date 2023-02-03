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
        theme: {},
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
            position: 'right',
          },
          {
            href: 'https://scholar.google.com/citations?user=alanlivio',
            label: 'Scholar',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Social Links',
            items: [
              {
                label: 'LinkedIn',
                href: 'https://linkedin.com/alanlivio',
              },
              {
                label: 'Twitter',
                href: 'https://twitter.com/alanlivio',
              },
            ],
          },
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
