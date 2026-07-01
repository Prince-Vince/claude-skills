---
name: web-animation-design
description: |
  Research and implement modern scroll animations and micro-interactions for web pages. References Dribbble, Jitter, and Mobbin for current design trends. Use when the user wants animations, scroll effects, micro-interactions, hover effects, page transitions, or says "animate", "scroll effects", "make it feel modern", "add motion", "Dribbble-style", or "Jitter animations".
allowed-tools:
  - WebSearch
  - WebFetch
  - Read
  - Edit
  - Write
  - Bash
  - Agent
---

# Web Animation & Design

Research current animation trends from Dribbble, Jitter, and Mobbin, then implement professional, accessible scroll animations and micro-interactions using vanilla CSS + JS. No heavy libraries.

## When to use

- User wants scroll-triggered animations on a page
- User references Dribbble, Jitter, or Mobbin design trends
- User says "make it feel modern", "add motion", "animate the page"
- User wants hover effects, card reveals, counters, timelines, or page transitions
- Enhancing an existing static page with tasteful motion

## Design research

Before implementing, research what's trending:

```
WebSearch: "site:dribbble.com scroll animation 2026 web design"
WebSearch: "site:mobbin.com scroll reveal cards animation"
WebSearch: "jitter.video animation trends landing page 2026"
WebSearch: "awwwards scroll animation examples minimal professional"
```

Focus on patterns that are:
- **Subtle and professional** — not flashy or gimmicky
- **Performance-friendly** — no layout thrashing, use `transform` and `opacity` only
- **Accessible** — always respect `prefers-reduced-motion`
- **Zero-dependency** — vanilla CSS + IntersectionObserver, no GSAP/AOS unless requested

## Animation patterns library

### 1. Fade-Up Reveal (universal)
Elements translate up 20-30px while fading in. The bread-and-butter of modern pages. Apply to section headings, text blocks, and content areas.

```css
.reveal {
    opacity: 0; transform: translateY(24px);
    transition: opacity 0.6s ease-out, transform 0.6s ease-out;
}
.reveal.visible { opacity: 1; transform: translateY(0); }
```

### 2. Staggered Card Cascade (grids)
Cards in a grid reveal sequentially with 100-150ms delays. Creates a wave effect. Use CSS custom property `--i` for delay calculation.

```css
.card-stagger {
    opacity: 0; transform: translateY(20px);
    transition: opacity 0.5s ease-out, transform 0.5s ease-out;
    transition-delay: calc(var(--i, 0) * 120ms);
}
.card-stagger.visible { opacity: 1; transform: translateY(0); }
```

```html
<div class="card-stagger" style="--i:0">Card 1</div>
<div class="card-stagger" style="--i:1">Card 2</div>
<div class="card-stagger" style="--i:2">Card 3</div>
```

### 3. Timeline Draw-In (process/timeline sections)
A vertical line draws downward as user scrolls, with nodes popping in (scale 0→1) when reached. High-impact showpiece for step-by-step processes.

```css
.timeline-progress {
    position: absolute; left: 18px; top: 0; width: 3px;
    height: 0; border-radius: 3px;
    background: linear-gradient(to bottom, var(--primary), var(--accent));
    transition: height 0.15s linear;
}
.timeline-step .dot {
    opacity: 0; transform: scale(0.4);
    transition: opacity 0.4s ease, transform 0.4s ease;
}
.timeline-step.visible .dot { opacity: 1; transform: scale(1); }
```

JS: Update `--progress` height based on scroll position within the timeline container using `requestAnimationFrame`.

### 4. Counter Roll-Up (statistics/numbers)
Numbers animate from 0 to target over ~1.4s with cubic ease-out. Triggered by IntersectionObserver.

```js
function animateCounter(el) {
    var target = parseInt(el.dataset.count, 10);
    var suffix = el.dataset.suffix || '';
    var duration = 1400, start = performance.now();
    function step(now) {
        var progress = Math.min((now - start) / duration, 1);
        var eased = 1 - Math.pow(1 - progress, 3);
        el.textContent = Math.round(eased * target) + suffix;
        if (progress < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
}
```

```html
<div class="stat-num" data-count="60" data-suffix="+">60+</div>
```

### 5. Heading Underline Wipe (section headings)
A colored line animates from left to right beneath headings on scroll.

```css
.heading-wipe::after {
    content: ''; display: block; width: 0; height: 3px;
    background: var(--accent); transition: width 0.6s ease-out; margin-top: 8px;
}
.heading-wipe.visible::after { width: 60px; }
```

### 6. Scroll Progress Bar (long pages)
Thin bar at top of viewport fills left-to-right as user scrolls. Helps gauge position on long content pages.

```css
.scroll-progress {
    position: fixed; top: 0; left: 0; height: 3px; z-index: 9999;
    background: var(--accent); transform-origin: left; transform: scaleX(0);
}
```

JS: `scaleX = scrollY / (docHeight - viewportHeight)`

### 7. Card Hover Lift (interactive cards)
Subtle lift + shadow expansion on hover. Restrained: `translateY(-4px)` max.

```css
.card-lift {
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.card-lift:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}
```

### 8. Soft Parallax (hero sections only)
Background moves at 50-70% of scroll speed. Keep it very subtle — 20-40px total movement.

```css
.hero-parallax { background-attachment: fixed; background-size: cover; }
```

Or with JS: `transform: translateY(calc(var(--scroll) * 0.3))` updated on scroll.

## Shared IntersectionObserver (powers patterns 1-5)

One snippet handles all scroll-triggered animations:

```js
(function() {
    var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduced) {
        document.querySelectorAll('.reveal, .card-stagger, .timeline-step, .heading-wipe')
            .forEach(function(el) { el.classList.add('visible'); });
        return;
    }
    var observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.12, rootMargin: '0px 0px -30px 0px' });

    document.querySelectorAll('.reveal, .card-stagger, .timeline-step, .heading-wipe')
        .forEach(function(el) { observer.observe(el); });
}());
```

## Section-to-animation mapping guide

| Section Type | Recommended Animation |
|---|---|
| Hero | Counter roll-up on stats, fade-up on text |
| Intro / About | Fade-up reveal |
| Card grids (benefits, features, pricing) | Staggered cascade |
| Timeline / Process steps | Timeline draw-in (showpiece) |
| Statistics / Numbers | Counter roll-up |
| Section headings | Heading underline wipe |
| Document/download lists | Staggered cascade + hover lift |
| CTA banners | Fade-up reveal |
| Long-form pages | Scroll progress bar |
| Hero with background image | Soft parallax (use sparingly) |

## Rules

1. **Never animate layout properties** (width, height, top, left, margin, padding). Only `transform` and `opacity` — these are GPU-composited and don't cause reflow.
2. **Always include `prefers-reduced-motion` override** that shows all content instantly with no animation.
3. **Use `will-change` sparingly** — only on elements that are actively animating, and remove it after.
4. **Keep durations between 0.3s–0.8s** for micro-interactions. Anything longer feels sluggish.
5. **Stagger delays should be 80-150ms** — shorter feels like a flash, longer feels like waiting.
6. **Only animate on enter, not exit** — use `unobserve()` after triggering so animations fire once.
7. **Test on mobile** — reduce or simplify animations at smaller breakpoints if needed.
8. **Don't animate everything** — pick 3-4 patterns max per page. Too much motion is worse than none.

## Anti-patterns to avoid

- AOS library for simple reveals (adds 14KB for what 10 lines of CSS does)
- Parallax on anything other than hero backgrounds
- Animations that delay content visibility by more than 1 second
- Scroll-jacking (hijacking native scroll behavior)
- Animations on text that make it hard to read during transition
- Infinite/looping animations (distracting, accessibility concern)
