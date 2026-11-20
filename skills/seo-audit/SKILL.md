---
name: seo-audit
description: Audit on-page and technical SEO of a supplied website, with prioritized evidence-based fixes. Use for page titles, meta descriptions, headings, canonical URLs, crawlability, structured data, and internal-link audits.
---

# SEO audit

Conduct a bounded audit of the user's website against its target audience, offerings, and geography. This is a **portable, independently authored** workflow, not a copy of a platform-provided integration.

## Inputs
- Website or priority URLs, target services, geography, and primary buyer questions.
- Existing benchmark or Search Console export, if available.
- Scope limit. Inspect only representative pages when a full crawl is not requested.

## Procedure
1. Use the existing `firecrawl` skill/CLI for fresh page retrieval: start with the supplied URLs, then map to find other significant pages if needed. Consult `firecrawl --help` for supported commands and options.
2. Record each page's response status, title, meta description, H1/H2 structure, canonical declaration, robots directives, structured-data types, and major internal links. Read the **raw HTML head**, not only cleaned Markdown, before declaring a tag absent.
3. Inspect `robots.txt` and the sitemap. Distinguish crawl permission, indexability, evidence of public search discovery, and **actual Google index status**. A `site:` query does not confirm indexing or deindexing.
4. Check that important service pages are linked with descriptive anchor text, including from an established parent company domain where applicable.
5. Identify claims needing citations, unverified testimonials/ROI figures, outdated product terms, or claims of certifications that cannot be substantiated.
6. Compare page framing with relevant buyer search terms without keyword stuffing or repeating near-identical suburb pages.
7. Deliver a prioritized remediation table with columns: page, evidence, severity, suggested change, validation step, and source URL. Separate **confirmed** from **inferred** and **not verified**.

## Guardrails
- Do not report Search Console status, search volume, backlinks, traffic, or Core Web Vitals unless obtained from a suitable source.
- Avoid invented search rankings, business reviews, citations, and performance forecasts.
- Never publish sensitive customer records, credentials, internal data, or private analytics.
- Do not edit live websites unless the user separately authorizes the change.

## Reference
- Google Search Central: https://developers.google.com/search/docs/appearance/ai-features
- Google link practices: https://developers.google.com/search/docs/crawling-indexing/links-crawlable
- Google's people-first content: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
