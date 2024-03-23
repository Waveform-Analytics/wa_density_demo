// See https://observablehq.com/framework/config for documentation.
export default {
  // The project’s title; used in the sidebar and webpage titles.
  title: "Marine Mammal Density Explorer",

  // The pages and sections in the sidebar. If you don’t specify this option,
  // all pages will be listed in alphabetical order. Listing pages explicitly
  // lets you organize them into sections and have unlisted pages.
  pages: [
    {
      name: "More info",
      pages: [
        {name: "Overview", path: "/overview"},
        {name: "Sources", path: "/sources"},
        {name: "Waveform Analytics", path: "/waveform"}
      ]
    }
  ],

  head: `<link rel="icon" href="/favicon.png">`,

  // Some additional configuration options and their defaults:
  // theme: "default", // try "light", "dark", "slate", etc.
  theme: ["dashboard", "light"],
  // header: `<div style="display: flex; align-items: center; gap: 0.5rem; height: 2.2rem; margin: -1.5rem -2rem 2rem -2rem; padding: 0.5rem 2rem; font: 500 16px var(--sans-serif);">
  // <a href="https://waveformanalytics.com/" style="display: flex; align-items: center;">
  //   <img src='/favicon.png' style='width: 30px;'>
  // </a>
  // </div>`,
  footer: `© ${new Date().getUTCFullYear()} Waveform Analytics, LLC`, // what to show in the footer (HTML)
  // toc: true, // whether to show the table of contents
  // pager: true, // whether to show previous & next links in the footer
  // root: "docs", // path to the source root for preview
  // output: "dist", // path to the output root for build
  // search: true, // activate search
};




// header: `<div style="display: flex; align-items: center; gap: 0.5rem; height: 2.2rem; margin: -1.5rem -2rem 2rem -2rem; padding: 0.5rem 2rem; border-bottom: solid 1px var(--theme-foreground-faintest); font: 500 16px var(--sans-serif);">
// <a href="https://waveformanalytics.com/" style="display: flex; align-items: center;">
//   <img src='/favicon.png' style='width: 25px;'>
// </a>
// </div>`,