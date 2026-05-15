# YiwuYimei Website — Agent Guide

## Project Overview

This is the source code for **YiwuYimei** (义乌亿美), a multilingual B2B wholesale export company website built with [Hugo](https://gohugo.io/). The site showcases home appliances, lifestyle products, and curated gifts exported from China to buyers in the USA, Europe, Japan, Korea, and beyond.

- **Live site:** `https://www.yiwuyimei.com/`
- **Static site generator:** Hugo (specified version `0.145.0`; local environment currently runs `0.157.0+extended`)
- **Base theme:** [PaperMod](https://github.com/adityatelange/hugo-PaperMod) (Git submodule)
- **Hosting:** Netlify
- **Primary language:** English (`en`)
- **Total active languages:** 10

> **Note:** Almost all layouts, styles, and behavior are heavily customized. Do not assume PaperMod defaults apply — always check the files in `layouts/` and `static/css/` first.

---

## Technology Stack

| Layer | Technology |
|-------|------------|
| Static generator | Hugo (Go templates) |
| Styling | Plain CSS (custom design system, no framework) |
| Fonts | Google Fonts — Inter |
| Hosting / CDN | Netlify |
| Analytics | Umami (privacy-friendly, self-hosted at `umami.117global.cn`) |
| Image optimization | Optional Cloudflare Image Resizing (`cdn-cgi/image`) |
| CMS (lightweight) | Netlify CMS / Decap CMS config present in `static/admin/` |

---

## Project Structure

```
├── config.toml              # Hugo site config (languages, menus, params)
├── netlify.toml             # Netlify build settings (Hugo 0.145.0)
├── compress_images.sh       # Batch image compression script (ImageMagick)
├── content/                 # Content per language
│   ├── en/                  # English (source language)
│   ├── ko/                  # Korean
│   ├── ja/                  # Japanese
│   ├── es/                  # Spanish
│   ├── de/                  # German
│   ├── fr/                  # French
│   ├── it/                  # Italian
│   ├── pl/                  # Polish
│   ├── fi/                  # Finnish
│   └── ga/                  # Irish (Gaeilge)
│       ├── _index.md        # Homepage content
│       ├── products/        # Product categories & items
│       ├── services/        # Service pages
│       ├── contact/         # Contact page
│       └── posts/           # Blog / news (mostly empty)
├── i18n/                    # UI translation strings per language
├── layouts/                 # Custom Hugo templates
│   ├── _default/            # baseof, home, list, single
│   ├── partials/            # head, navbar, footer, responsive-img-cf
│   ├── contact/             # Contact page layout
│   ├── services/            # Service list & single layouts
│   └── robots.txt           # Custom robots template
├── static/                  # Static assets
│   ├── css/                 # Custom stylesheets
│   ├── images/              # Product images, banners, favicon
│   ├── _headers             # Netlify HTTP headers
│   ├── _redirects           # Netlify redirects
│   └── admin/               # Netlify CMS config
├── scripts/                 # Utility scripts
│   ├── TRANSLATION_GUIDE.md # Guide for adding new languages
│   └── translate_product_specs.py # Auto-translates product specs
└── themes/PaperMod          # Git submodule (base theme)
```

---

## Build & Development Commands

### Prerequisites
- Hugo installed (extended version recommended). The site targets **Hugo 0.145.0** but builds fine on 0.157.0+extended.
- ImageMagick (only needed to run `compress_images.sh`).
- Python 3 (only needed to run the translation script).

### Local Development
```bash
# Start local dev server with drafts enabled
hugo server -D

# Build the site (output goes to public/)
hugo

# Build with minification (production-like)
hugo --minify
```

### Netlify Build Settings (from `netlify.toml`)
```toml
[build]
  publish = "public"
  command = "hugo"

[build.environment]
  HUGO_VERSION = "0.145.0"
```

---

## Multilingual Architecture

Hugo is configured for **10 languages** with each language having its own content directory.

### Language Codes
| Code | Name | Content Dir | Status |
|------|------|-------------|--------|
| `en` | English | `content/en` | Source / default |
| `ko` | 한국어 | `content/ko` | Active |
| `ja` | 日本語 | `content/ja` | Active |
| `es` | Español | `content/es` | Active |
| `de` | Deutsch | `content/de` | Active |
| `fr` | Français | `content/fr` | Active |
| `it` | Italiano | `content/it` | Active |
| `pl` | Polski | `content/pl` | Active |
| `fi` | Suomi | `content/fi` | Active |
| `ga` | Gaeilge | `content/ga` | Active |

### Key Config in `config.toml`
- `defaultContentLanguage = "en"`
- `defaultContentLanguageInSubdir = true`  
  → English pages live under `/en/` just like other languages.
- `contentDir` per language points to `content/{lang}`.
- Menus, descriptions, keywords, and welcome text are defined per language under `[languages.{code}.params]` and `[[languages.{code}.menu.main]]`.

### i18n Strings
UI strings (navigation labels, buttons, product category names, etc.) live in `i18n/{lang}.yaml`. These are referenced in templates via `{{ T "key" }}`.

### Adding a New Language
1. Add the language block to `config.toml`.
2. Create `i18n/{code}.yaml`.
3. Add `SPEC_LABELS` and `SPEC_VALUES` mappings in `scripts/translate_product_specs.py`.
4. Create `content/{code}/` and copy/translate content.
5. Run `python3 scripts/translate_product_specs.py en {code}` to auto-translate product specifications.

See `scripts/TRANSLATION_GUIDE.md` for the full step-by-step guide.

---

## Content Model

### Product Page (`content/{lang}/products/{category}/{sku}.md`)

```yaml
---
title: "Product Name"
product_type: "portable fan"        # Used for category badges
date: 2025-04-01
section: "new"                      # Options: new, best, unique
cover:
  image: "/images/products/fans/YWF-046.webp"
  gallery:
    - "/images/products/fans/YWF-046/1.jpg"
    - "/images/products/fans/YWF-046/2.jpg"
  long_image: false                 # Optional: true = full-width gallery layout
draft: false
---
**Product name:** ...
**Product size:** ...
```

- The **body** contains product specifications as bold key-value pairs.
- The **`section`** front-matter key drives which products appear in the "New Arrivals", "Best Sellers", and "Unique Finds" grids on the homepage.
- **`product_type`** is shown as a category badge on cards and detail pages.

### Category Index (`content/{lang}/products/{category}/_index.md`)
Declares the category section. It may include a `banner` parameter for the category hero image.

### Service Page (`content/{lang}/services/{service}.md`)
Standard markdown page with `title` and `description` front matter.

### Contact Page (`content/{lang}/contact/_index.md`)
Minimal front matter; layout is hardcoded in `layouts/contact/list.html`.

---

## Layout System

All layouts are custom and live under `layouts/`. The PaperMod theme is present as a submodule but most behavior is overridden.

| Template | Purpose |
|----------|---------|
| `_default/baseof.html` | Root HTML shell. Loads head, navbar, main block, footer, global scripts. |
| `_default/home.html` | **Non-English** homepage with hero, trust badges, sidebar, product grids. |
| `index.html` | **English** homepage (slightly different structure, hardcoded English labels). |
| `_default/list.html` | Category pages and generic lists. Includes breadcrumb and product grid. |
| `_default/single.html` | Product detail page. Shows cover image, specs, inquiry CTA, image gallery, trust section. |
| `contact/list.html` | Contact page layout. |
| `services/list.html` | Services listing with icon cards. |
| `services/single.html` | Individual service page. |
| `partials/head.html` | SEO meta, Open Graph, Twitter Cards, JSON-LD structured data, canonical, fonts, CSS. |
| `partials/navbar.html` | Responsive nav with language switcher (desktop + mobile dropdown). |
| `partials/footer.html` | Site footer. |
| `partials/responsive-img-cf.html` | Cloudflare Image Resizing helper. Falls back to plain `<img>` when disabled. |

### Important Layout Behaviors
- **Gallery layout:** If a product gallery contains images with `详情页` or `slice` in the filename, or if `cover.long_image` is `true`, the gallery renders as a single full-width column instead of a CSS grid.
- **Inquiry button:** Product pages generate a `mailto:sales@yiwuyimei.com` link pre-filled with the product title.
- **Language switcher:** Falls back to constructing a URL if no translated page exists for the current page.

---

## CSS Architecture

All styles are plain CSS using a custom design-system defined in `static/css/modern-theme.css`.

### Custom Stylesheets
| File | Scope |
|------|-------|
| `modern-theme.css` | Design tokens (colors, spacing, shadows, typography), global styles, hero banners, product cards, grids, animations. |
| `extra.css` | Additional utilities and overrides. |
| `navbar.css` | Navbar-specific styles (loaded in head). |
| `footer.css` | Footer styles. |
| `products.css` | Product list & detail page styles. |
| `contact.css` | Contact page styles. |
| `service.css` | Services page styles. |
| `i18n.css` | Language-specific tweaks (if any). |
| `catalogue.css` | Catalogue / category styles. |

### Design Tokens (excerpt)
```css
:root {
  --color-primary: #1e3a5f;
  --color-accent: #4ecdc4;
  --color-warm: #d4a574;
  --color-bg: #faf9f7;
  --border-radius: 16px;
  --shadow-sm: 0 2px 8px rgba(30, 58, 95, 0.06);
  /* ... */
}
```

Font family: `Inter` (loaded from Google Fonts) with system-ui fallbacks.

---

## Images & Assets

### Image Organization
```
static/images/
├── banner.jpg                 # Homepage hero background
├── og-default.webp            # Default Open Graph image
├── catalogue/                 # Category banner images
└── products/
    ├── {category}/
    │   ├── {sku}.webp         # Cover image
    │   └── {sku}/
    │       ├── 01.jpg         # Gallery detail images
    │       └── ...
```

### Image Compression (`compress_images.sh`)
- Uses **ImageMagick** (`magick`).
- Scans `static/images` for files larger than **1 MB**.
- Resizes to **1200px max width** at **85% quality**.
- Converts **PNG → WebP** and removes the original PNG.
- ⚠️ The script contains **hardcoded absolute paths** pointing to a backup directory. Review paths before running.

### Responsive Images
The partial `responsive-img-cf.html` supports Cloudflare Image Resizing (`/cdn-cgi/image/...`). It is currently **disabled** (`useCloudflare = false` in `config.toml`). When disabled, the partial renders a standard `<img>` tag with `loading="lazy"` and `decoding="async"`.

---

## SEO & Structured Data

Every page includes:
- `<meta name="description">` and `<meta name="keywords">`
- Canonical link and `hreflang` alternates
- Open Graph (`og:*`) and Twitter Card meta tags
- JSON-LD structured data:
  - **Homepage:** `Organization`
  - **Product pages:** `Product` (with SKU, brand, category, image array)
  - **Posts:** `Article`
  - **Service pages:** `Service`
- `robots.txt` allows all, points to `sitemap.xml`
- Sitemap generated automatically by Hugo (`sitemap` config block)

---

## Security & Headers

Netlify headers are defined in `static/_headers`:
```
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
```

Static assets (`/images/*`, `/css/*`, `/js/*`) receive long-term immutable caching headers.

A small inline script in `head.html` adds `rel="noopener"` to any external links opened in a new tab.

---

## Redirects

Defined in `netlify.toml` and `static/_redirects`:
- `/checkout` → `/` (301)
- `/checkout/*` → `/` (301)

These redirect legacy checkout URLs to the homepage.

---

## Development Conventions

### File Naming
- Product SKUs are used as filenames (e.g., `fan001.md`, `YWF-046.md`).
- Category folders use kebab-case (`scent-diffusers`, `mobile-accessories`).
- Image filenames often contain Chinese characters for detail pages (e.g., `详情页_01.jpg`). Do not rename these unless you also update the corresponding `gallery` arrays in content files.

### Content Editing Rules
- Always keep **all language versions** in sync when adding or removing products.
- Use the translation script for specification labels/values rather than manual copy-paste to maintain consistency.
- Product `date` fields affect ordering; newer dates appear first in category lists.

### Git
- `public/` and `resources/` are gitignored.
- `themes/PaperMod` is a Git submodule. When cloning fresh, run:
  ```bash
  git submodule update --init --recursive
  ```

---

## Deployment

Pushing to the repository's `main` branch triggers a Netlify build:
```
Command: hugo
Publish directory: public
```

No CI/CD tests are configured. Verify the site locally with `hugo server -D` before pushing.

---

## Utilities

### `scripts/translate_product_specs.py`
Bulk-translates product specification labels and values across content files.

```bash
python3 scripts/translate_product_specs.py <source_lang> <target_lang>
# Example:
python3 scripts/translate_product_specs.py en es
```

It reads English product files, replaces known labels/values using hardcoded dictionaries (`SPEC_LABELS` and `SPEC_VALUES`), and writes translated versions to the target language directory.

### `compress_images.sh`
Batch-optimizes images. Review the hardcoded paths inside the script before executing.

---

## Common Pitfalls for Agents

1. **Do not assume PaperMod layouts apply.** Check `layouts/` first — almost everything is overridden.
2. **Language URLs:** Because `defaultContentLanguageInSubdir = true`, even English pages are under `/en/`. Always use `relLangURL` for internal links.
3. **Missing translations:** If a page lacks a translation in a given language, the language switcher falls back to URL heuristics. The link may 404 if the target file does not exist.
4. **Image paths:** Product galleries reference exact filenames. Renaming an image file in `static/` without updating the corresponding markdown front matter will break the gallery.
5. **Config ordering:** `config.toml` contains a large `[params]` block followed by additional `[languages.*]` blocks. Keep language-specific params inside the correct `[languages.{code}.params]` section.
6. **Hugo version lock:** Netlify pins Hugo to `0.145.0`. Using features only available in newer Hugo versions will break the production build.
