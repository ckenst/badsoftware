# Copilot instructions for ckenst/badsoftware

Build / test / lint
- No build, test, or lint scripts were found in the repository.
- To preview locally: serve the docs/ directory as static files:
  - python3 -m http.server 8000 --directory docs
  - or: npx serve docs
- There are no automated tests; there is no single-test command to run.

High-level architecture
- Static site under docs/: HTML pages (index.html, about.html, services.html, contact.html, 404.html) and assets/ (style.css, theme.js).
- Theme is implemented with CSS custom properties (variables) and a small JS controller: docs/assets/theme.js.
- The site is intentionally minimal — no build tooling, just static files and a CNAME for deployment.

Key conventions and repository-specific notes
- Tagline: "so bad, we're good" (used in docs/index.html hero).
- Company description: "The Bad Software Company is a boutique systems-engineering advisory firm." (in docs/about.html).
- Copyright: all footers updated to "© 2026 and beyond The Bad Software Company".
- Theme handling:
  - localStorage key: 'badsw-theme'
  - theme toggle button id: 'theme-toggle'
  - html[data-theme] attribute used for stronger overrides
  - CSS variables for colors live in docs/assets/style.css
- Mobile-first layout: styles favor small screens by default; wider-screen rules live in @media (min-width:600px).
- Contact form:
  - docs/contact.html now contains an HTML form (id="contact-form") with action="#" and novalidate; it is intentionally not hooked up.
  - If wiring up later, update the form's action/method and add progressive enhancement (client-side validation) or server endpoint.
- Design tokens and interactive behavior:
  - Accent, background, text and other tokens use CSS variables defined in :root / .theme-light / html[data-theme].
  - theme.js toggles localStorage and toggles classes/attributes on <html>.

Files of interest for future Copilot sessions
- docs/index.html — hero, tagline
- docs/about.html — company description
- docs/contact.html — contact form (not hooked)
- docs/assets/style.css — theming variables and mobile-first layout
- docs/assets/theme.js — theme controller (localStorage key: 'badsw-theme')

AI / assistant configs checked
- No CLAUDE.md, .cursorrules, AGENTS.md, .windsurfrules, CONVENTIONS.md, AIDER_CONVENTIONS.md, .clinerules or other assistant-specific config files were found.

Notes for tasks Copilot may perform
- Editing visual styles: prefer editing docs/assets/style.css (mobile-first changes are localized there).
- When adding JS behavior, prefer unobtrusive enhancement that preserves the static HTML (keep action="#" until backend integrated).
- For previews during PR review, a simple static server (python3 -m http.server) is sufficient.

If anything in this file should be expanded (more commands, CI tips, or scaffolding instructions), say so and it will be extended.
