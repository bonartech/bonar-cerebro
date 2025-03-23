import { themes as prismThemes } from "prism-react-renderer";
import type { Config } from "@docusaurus/types";
import type * as Preset from "@docusaurus/preset-classic";

const config: Config = {
  title: "CEREBRO",
  tagline: "AGI basada en conciencia y razonamiento",
  favicon: "img/favicon.ico",

  // 🌐 URL de producción
  url: "https://bonartech.github.io",
  baseUrl: "/bonar-cerebro/",

  // GitHub Pages deployment config.
  organizationName: "bonartech",
  projectName: "bonar-cerebro",
  deploymentBranch: "gh-pages",

  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "warn",

  i18n: {
    defaultLocale: "es",
    locales: ["es"],
  },

  presets: [
    [
      "classic",
      {
        docs: {
          sidebarPath: require.resolve("./sidebars.ts"),
          routeBasePath: "docs",
          editUrl: "https://github.com/bonartech/bonar-cerebro/edit/main/",
        },
        blog: {
          showReadingTime: true,
          editUrl: "https://github.com/bonartech/bonar-cerebro/edit/main/blog/",
        },
        theme: {
          customCss: require.resolve("./src/css/custom.css"),
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: "img/cerebro-banner.jpg", // Cambialo si tenés un social card
    navbar: {
      title: "CEREBRO",
      logo: {
        alt: "Logo de CEREBRO",
        src: "img/logo.svg",
      },
      items: [
        {
          type: "docSidebar",
          sidebarId: "tutorialSidebar",
          position: "left",
          label: "Documentación",
        },
        {
          href: "https://github.com/bonartech/bonar-cerebro",
          label: "GitHub",
          position: "right",
        },
      ],
    },
    footer: {
      style: "dark",
      links: [
        {
          title: "Documentación",
          items: [
            {
              label: "Introducción",
              to: "/docs/cerebro",
            },
          ],
        },
        {
          title: "Comunidad",
          items: [
            {
              label: "GitHub",
              href: "https://github.com/bonartech",
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} CEREBRO. Desarrollado con Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
