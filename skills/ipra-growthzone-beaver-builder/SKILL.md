---
name: ipra-growthzone-beaver-builder
description: Field guide for rebuilding IPRA pages in GrowthZone's Beaver Builder (+ PowerPack). Captures the environment's quirks, the sanitizer landmines, and the proven CSS/layout patterns so future pages go fast instead of ping-ponging. Use when building or restyling any IPRA page in GrowthZone/Beaver Builder.
---

# IPRA × GrowthZone × Beaver Builder — Build Field Guide

Hard-won notes from rebuilding the **Regions page**. Read the "Golden Rules" first; the rest is detail + copy-paste patterns. This environment has several non-obvious traps — most of our wasted time came from not knowing them.

> Environment: GrowthZone CMS → WordPress → **Beaver Builder + PowerPack** add-on. WCAG 2.1 AA required (no AudioEye violations). IPRA Blue: `#009abc` / `#007191`. Font: Raleway. Icons: **Font Awesome 5** (`"Font Awesome 5 Free"`, weight 900).

---

## ⭐ Golden Rules (the TL;DR that saves hours)

1. **Decide *where* CSS goes by reuse (this matters a lot here):**
   - **Single page / single row of styling → that ROW's Custom CSS field** (PowerPack, Row → Advanced). It renders live in the canvas, bundles with the row when you template it, auto-scopes to the row, and — critically — **likely dodges the Customizer sanitizer** (so `>`, `:has()`, and FA glyph escapes tend to work there). This is the better default for page-specific work and would have prevented most of our pain.
   - **Shared across multiple pages / truly page-wide → Customize → Additional CSS**, scoped to a page-only class (e.g. `.regions-page-section`). Global + live, but watch the sanitizer (rule 2).
2. **The Customizer's Additional CSS sanitizer mangles things** (the row Custom CSS field generally does NOT). When writing in **Additional CSS**, AVOID:
   - `>` child combinators → **use descendant selectors instead** (`.a .b`, not `.a > .b`).
   - `:has()` → it can invalidate the **entire** rule block. Don't use it there.
   - Font Awesome glyph escapes `content:"\fXXX"` → get eaten → **use an embedded SVG** for icons instead.
3. **Native modules for content, HTML modules only for code.** Heading / Text Editor / Button for anything an editor will touch. HTML module *only* for the interactive map + its JS.
4. **Top-level rows only.** Nested rows are unreliable in this environment.
5. **Judge layout in Preview (P), never the editing canvas.** The canvas renders a *different DOM* than the live page and is not WYSIWYG for custom CSS.
6. **Select modules from the Outline panel** (list icon, top-right), not by hovering the canvas. This is the teachable workflow for non-technical successors.
7. **After any CSS change: Publish, then hard-refresh (Ctrl+Shift+R).** GrowthZone caches CSS aggressively.

---

## Where CSS/JS can and can't go

| Location | Page-wide? | Live-renders in canvas? | Notes |
|---|---|---|---|
| **Customize → Additional CSS** ✅ | Yes | Yes | **Primary home for page CSS.** Sanitizer caveats above. |
| BB Tools → "Layout CSS & JavaScript" | — | — | **DISABLED in this build** (Tools menu jumps History → Global Styles). Not available. |
| Row → Custom CSS field (`bb_css_code`, PowerPack) | Scoped to that row | **Yes (live)** | **Best for single-page / single-row styling.** Auto-scopes to the row; **likely dodges the sanitizer** (`>`, `:has()`, FA escapes tend to work); bundles with the row when templated. Not for cross-page sharing. |
| HTML module `<style>` (module **main content** field) | Yes | **No (stale until reload)** | Works but the module is invisible & canvas won't refresh it live. Use only when CSS isn't an option (it always is here). |
| HTML module — the module's separate **"CSS" field** | n/a | n/a | ⚠️ **TRAP:** strips/scopes `<style>`, module renders empty. Never put `<style>` here. |

JS (e.g. the interactive map script) has no panel either → it lives in the **HTML module's main content field** alongside the map markup. **Map JS does not run in the editing canvas — only in Preview/live.**

### Where to put CSS — decision

| Situation | Put it in | Why |
|---|---|---|
| Styling used on **one page / one row** | That **Row's Custom CSS field** | Live in canvas, bundles with the row when templated, **dodges the Customizer sanitizer** (so `>`/`:has()`/FA escapes work), scoped automatically |
| Styling **shared across pages** or genuinely page-wide | **Customize → Additional CSS** (scoped by class) | One source of truth; but obey the sanitizer rules |
| A **one-off** tweak to a single element | That node's CSS field | Self-contained, travels with the node |

**Default for page-specific work: the Row Custom CSS field.** It likely would have prevented most of the Regions-page saga (the sanitizer eating `>`, `:has()`, and the FA glyph). Target the **class** (`.ipra-card`, etc.) from the row field — one rule covers all cards in the row; don't write per-individual-card CSS.

⚠️ **Verify scoping once per new page:** PowerPack node CSS auto-scopes to that node (it prepends the row's selector, or exposes a `selector`/`node` keyword). Drop a throwaway rule (e.g. a red border on `.ipra-card`) and confirm it (a) lands and (b) only affects that row, before building on it. The layout gremlins below (`.fl-col-group::before` stealing grid cells, `.fl-col-small` stacking) still apply wherever the CSS lives — but the fixes work fine in the row field.

---

## Page skeleton (Regions example)

Top-level rows, each `<section>`, class `regions-page-section` + a row modifier:

| Row | Width | Class | ID |
|---|---|---|---|
| Hero | Full Width | `regions-page-section regions-hero` | `regions-hero-row` |
| Map | Fixed | `regions-page-section regions-map` | `main-content` (skip-link target) |
| Cards | Fixed | `regions-page-section regions-cards` | — |
| CTA | Fixed | `regions-page-section regions-cta` | — |

Add class/ID/tag via Row → **Advanced → HTML Element**. Rename a node via right-click → Rename (or Outline).

---

## The card-grid saga → the pattern that works

Goal: a 2×2 card grid from a single 4-column row. What we learned:

- BB tags narrow columns **`.fl-col-small`** and force-stacks them `width:100% !important` with high specificity. Low-specificity overrides lose.
- The group is **`.fl-col-group`** in the DOM (PowerPack doesn't actually rename it — earlier failures were the `:has()`/`>` sanitizer issue, not the class).
- **CSS Grid is the winning model** (no flex wrap-math to overflow). BUT:
- **BB's `.fl-col-group::before/::after` clearfix pseudo-elements become grid cells** and shove every card off by one (classic "first cell empty, cards brick"). **You must hide them.**

Proven card layout (descendant selectors only, no `>` outside what survives, high specificity to beat `.fl-col-small`):

```css
/* 2-column grid, equal-height */
.regions-cards .fl-col-group{display:grid !important;grid-template-columns:1fr 1fr !important;gap:26px !important;align-items:stretch !important;}
.regions-cards .fl-col-group::before,.regions-cards .fl-col-group::after{display:none !important;} /* <-- the fix for bricking */
.regions-page-section.regions-cards .fl-col-group .fl-col.ipra-card{
  width:auto !important;max-width:none !important;min-width:0 !important;
  flex:none !important;float:none !important;clear:none !important;
}
/* internal padding — descendant, NOT ".ipra-card > .fl-col-content" */
.regions-page-section.regions-cards .ipra-card .fl-col-content{padding:34px 36px !important;}
@media(max-width:900px){
  .regions-cards .fl-col-group{grid-template-columns:1fr !important;}
}
```

Card module class goes on the **column** (e.g. `ipra-card ipra-card--teal`). Card background/border/shadow on `.ipra-card`. Remember: cards stack to 1 column under 900px **by design** — a narrow browser window (or the Claude side panel open) will show the stack; judge at full desktop width.

---

## Icons without Font Awesome (sanitizer eats the glyph)

The site runs FA5, but `content:"\f3c5"` gets stripped by the Customizer, so the icon square renders empty. Use an **embedded, URL-encoded SVG** as a background (encode `<`→`%3C`, `>`→`%3E`, `"`→`%22`, `#`→`%23`). Set the colored square with **`background-color`** in variants (not the `background` shorthand, which would wipe the SVG):

```css
.ipra-card h3::before{content:"";width:48px;height:48px;border-radius:14px;flex-shrink:0;pointer-events:none;
  background-color:#009abc;background-repeat:no-repeat;background-position:center;background-size:20px 20px;
  background-image:url('data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 384 512%22%3E%3Cpath fill=%22%23ffffff%22 d=%22M172.268 501.67C26.97 291.031 0 269.413 0 192 0 85.961 85.961 0 192 0s192 85.961 192 192c0 77.413-26.97 99.031-172.268 309.67-9.535 13.774-29.93 13.773-39.464 0zM192 272c44.183 0 80-35.817 80-80s-35.817-80-80-80-80 35.817-80 80 35.817 80 80 80z%22/%3E%3C/svg%3E');}
.ipra-card--lime h3::before{background-color:#5a8e22;}
```

(That path is FA `map-marker-alt`. Swap the `d=` path for other icons.)

---

## Native module gotchas

- **Eyebrow / label text:** keep it formatted as **Paragraph** in the Text Editor, not "Heading 2" — a stray heading format changes the tag and breaks `.eyebrow p` selectors. Style robustly with `.eyebrow, .eyebrow *{...!important}`.
- **Headings:** BB wraps Heading text in `<span class="fl-heading-text">`; the theme styles that span with high specificity. Target `.row .fl-module-heading .fl-heading-text` (and add `!important`) to win.
- **County / tag lists as pills:** type the list in a Text Editor's **"Text" (HTML) tab** as `<ul><li>…</li></ul>` (the Visual tab dumps everything into one bullet). Then CSS turns `li` into pills:
  ```css
  .ipra-card-counties ul{display:flex;flex-wrap:wrap;gap:6px;list-style:none;margin:0;padding:0;}
  .ipra-card-counties li{background:#f8fafc;border:1px solid #e2e8f0;border-radius:20px;padding:4px 12px;font-size:12px;font-weight:600;color:#009abc;display:inline-flex;}
  ```
- **"Representative:" bold/colored:** must be wrapped in `<strong>` in the editor (select word → Bold) for `.rep strong{color:…}` to apply.

---

## Editor-friendliness (for whoever inherits the page)

Decorative CSS fights the editing canvas. BB adds class **`fl-builder-edit`** to the page while editing (the site already relies on `body:not(.fl-builder-edit)` patterns) — use it to switch effects off in the editor only:

```css
/* EDITOR OVERRIDES — Beaver Builder canvas only */
.fl-builder-edit .regions-hero{overflow:visible !important;}
.fl-builder-edit .regions-hero::before,.fl-builder-edit .regions-hero::after{display:none !important;}
.fl-builder-edit .regions-hero .fl-row-content-wrap{z-index:auto !important;}
.fl-builder-edit .ipra-card{transition:none !important;}
.fl-builder-edit .ipra-card:hover{box-shadow:0 5px 15px rgba(0,0,0,.06) !important;}
```

Also:
- Put **`pointer-events:none`** on every decorative pseudo-element (background blobs, icon squares) so they don't block clicking the text/modules underneath.
- Prefer **shadow-only hover** (no `transform:translateY`) so cards don't dodge the cursor / shift BB's toolbar.
- The hover "artifacting" (duplicated content under the toolbar) is **BB's own hover overlay** — editor-only, cosmetic, **not fixable via CSS**. Tell editors to use the **Outline panel**.

---

## Diagnostics that actually settle arguments

Run in DevTools **Console on the live/preview page** (not the editor — the editor lives in `#fl-builder-ui-iframe`):

```js
// What wraps the cards, and is it laying out as expected?
let c=document.querySelector('.ipra-card');let p=c.parentElement;
console.log('CARD width:',getComputedStyle(c).width);
console.log('PARENT display:',getComputedStyle(p).display,'| class:',p.className);

// What Font Awesome family is actually loaded?
let i=document.querySelector('i.fas,i.fa,.fl-icon i');console.log(i&&getComputedStyle(i).fontFamily);
```

Rule of thumb: if a cosmetic style applies but a layout/`>`/`:has()`/`content` rule doesn't, suspect the **sanitizer**, not specificity.

---

## Build fast: duplicate + Save As templates

Don't rebuild repeating elements (cards, callouts, section shells) from scratch.

- **Node toolbar** (hover any row/column/module) icons L→R: move · **settings (wrench)** · **duplicate** · **save as (disk)** · delete.
- **Build one, duplicate it, edit text.** Right-click → Duplicate (or the toolbar icon) clones the node *with its classes* — far faster than rebuilding the module stack each time.
- **Save As a reusable template:** settings dialog → **"Save As..."** (bottom), or the toolbar disk icon, or right-click → Save As. Name it (e.g. "IPRA Region Card"). Reuse via **+ Add Content → "Saved" tab** (Saved Rows / Columns / Modules) — available on **every page**, site-wide.
- ⚠️ **Global vs not:** "Save as Global" (checked) links all instances to one master — editing one changes them all. Leave it **unchecked** for things you customize per-use (like cards); check it only for truly identical site-wide blocks.
- **Templates carry markup + classes, not the stylesheet.** Keep visual/layout CSS centralized by class in Additional CSS; the saved item picks it up automatically wherever that CSS is present.
- Recommended card workflow: build one card column → duplicate ×3 → edit text → (optionally) Save As the whole row for other pages.

## Fast path for a new page

1. Build rows top-level, native modules for content, one HTML module for any interactive/code block.
2. Add classes: `<page>-page-section` on each row + a row modifier; a clear class on every styled module.
3. Drop the page CSS into **Customize → Additional CSS**, scoped to those classes. Start `@import` (fonts) at the very top.
4. Use **CSS Grid** for multi-card layouts; **hide `.fl-col-group::before/::after`**; beat `.fl-col-small` with high-specificity card widths.
5. **No `>`, no `:has()`, no FA glyph escapes** — descendant selectors + SVG icons.
6. Add the **editor-overrides** block + `pointer-events:none` on decorations.
7. Publish (Customizer **and** BB layout) → hard-refresh → verify in **Preview at full width** + mobile.

---

## WCAG quick-keeps
- Skip link to `#main-content` (put that ID on the first content row).
- Visible focus: `outline:3px solid #e2cc00` on links/buttons.
- `@media (prefers-reduced-motion: reduce)` to kill animations.
- Contrast: stick to the IPRA teal/navy on white; white text only on `#007191`/`#005f7a` or darker.
