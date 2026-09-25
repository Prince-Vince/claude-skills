# Adapting the working example

`assets/microsoft-example/` is the finished demonstration from this workflow, not an empty starter and not a live Microsoft integration.

| File | What to change |
|---|---|
| `index.html` | Chapters, headline copy, diagram labels, example records, sources and disclosure notes |
| `style.css` | Base typography, colors, layout, scenes and responsive behavior |
| `revision.css` | Concise comparison, Power Pages scene, and final layout refinements |
| `app.js` | Walkthrough `story`, recommendation `needs`, selection state and demo interaction |
| `assets/*.svg` | Official Microsoft icons for this educational example |

The example has 12 chapters. Navigation is built from `.chapter` elements and `data-title`; changing chapter order updates the navigation, but visible eyebrow numbers in the HTML must also be updated.

The walkthrough has five main `.journey-node` buttons and a final optional Foundry step. If your story has a different structure, adapt both the HTML nodes and JavaScript highlights. Do not merely replace text in the array while leaving incompatible node logic. Keep button `data-step` values aligned with the array.

The tool selector links each `[data-need]` button to an entry in `needs`. Each entry contains a title, explanation, tags, and next-step note. Keep the initial HTML recommendation consistent with the initial selection.

The supplier quote button only updates local display state. It sends nothing to Microsoft. For a different subject, replace or remove the demo and its associated JavaScript together. Never imply a sample form is connected.

Most diagrams loop only while visible. The main walkthrough is manually playable and stops at the final step. Reduced-motion styling leaves the content readable without animation. Native browser fullscreen is preferable to a custom control that does not work in an embedded browser.

For a new topic, remove obsolete content and selectors rather than accumulating overrides. Choose a new design direction if requested; the example's ivory/green palette and Microsoft icons are not universal defaults.

Product documentation was reviewed September 24–25, 2026. Reverify it when reusing the Microsoft story, especially Copilot Studio experience names, licensing, and preview integrations.
