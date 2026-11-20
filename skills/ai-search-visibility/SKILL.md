---
name: ai-search-visibility
description: Benchmark non-branded public web-search visibility for a business or service against a fixed query set, and track changes across reporting periods without misrepresenting web rankings as LLM recommendation rates.
---

# AI and web-search visibility benchmark

Use for repeatable market visibility snapshots, especially for regional professional services.

## Method
1. Define an unchanging list of at least six buyer-intent queries, target geography, competitor criteria, and reporting timestamp. Keep the exact wording and source configuration in a data file so future runs can be compared.
2. With the repository's `firecrawl` skill, search each query using consistent location and result limits. Collect first 10 organic-style returned result URLs, ranks, page titles, and domains. The tool's ranking may differ from an ordinary personalized Google SERP.
3. Normalize `www.` prefixes and common tracking URLs for domain comparisons without collapsing distinct companies.
4. For each query, record target-domain appearance and exact returned position if any; if absent report "outside sampled top 10", not "unindexed".
5. Track recurring competitor domains, distinguish directories and job boards from direct service competitors, and flag newly observed content without asserting an unverified publication date.
6. Compare like-for-like prior snapshots; disclose changes to provider, geography, query, or sampling method.
7. Include a concise action plan: indexing checks, content targeting, internal links, external references, and measurement gaps.

## Required output
- Date, search source/method, region, and six-query top-10 table.
- Comparisons to previous snapshots with a clear baseline.
- Three most important observed changes, their source URLs, and top three actions.
- Explicit note: **search-result visibility is not the same as actual ChatGPT, Claude, Gemini, or Perplexity recommendation frequency**.

## For actual AI recommendation testing
Run a separately documented, repeated prompt experiment across the named products, where use is authorized. Keep the prompt, model/product, date, context, location assumptions, citations, and response. Record brand mention and direct site citation independently. Never infer a rate from traditional search result sets.

## Optional inputs
Google Search Console exports can measure query impressions, clicks, and average position; URL Inspection is needed for definitive account-level indexing diagnosis. Obtain data legitimately; do not automate private account access without approval.
