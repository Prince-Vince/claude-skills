# Editing and review reference

## Speech and cuts

- Retain a mapping from each edited segment to the original file and timestamps. Check stream start times and variable frame rate before relying on timestamps; normalize only when needed, preserving originals.
- Use transcript semantics to identify retakes and audio evidence to choose boundaries. Word timestamps are approximate. Leave enough room for consonants, breath, and natural delivery; never cut solely because a caption or silence detector ends.
- Listen around each cut. Resolve clicks with short audio fades where appropriate without blending different words. Preserve deliberate emphasis and meaningful pauses. Review ambiguous takes in context rather than automatically deleting repeated words.
- If word alignment is unavailable, use segment timing plus manual audio checks and disclose the limitation. Do not fabricate word-level precision.

## Visuals and captions

- Inspect the subject's position before cropping; adapt portrait framing when a center crop would lose the face or demonstration. Avoid stretching footage.
- Sample candidate B-roll, then inspect the actual selected span. Keep on-screen examples consistent with narration; label illustrative reconstructions when viewers could mistake them for evidence.
- Build captions from the final edited timeline, not the uncut transcript. Correct names and technical terms, use natural phrase breaks, readable contrast, and placement appropriate to the platform's current interface. Keep an editable SRT or equivalent alongside any burned-in captions.
- Match graphics to the evidence and creator style. Use actual inspected references for visual claims. Prefer a simple callout over unnecessary 3D or complicated animation.

## Audio

- Start with the natural voice. Avoid heavy denoising, EQ, compression, or gain changes without an audible reason. Compare processed speech with the original.
- Duck music under dialogue, fade entries/exits, and check for clipping, clicks, pumping, and sudden level changes. Use a documented loudness target appropriate to the destination, then listen for intelligibility; loudness measurements alone do not prove a good mix.
- Keep a source and license record for music and effects. Do not generate or buy assets beyond the authorized scope and budget.

## Export and QA

- Choose a delivery codec/container supported by the destination; H.264 video with AAC audio in MP4 is a practical default. Check dimensions, pixel aspect, duration, audio presence, and successful decoding with available media tools.
- Verify subtitle sync at the start, middle, and end; inspect every cut boundary and overlay transition. Check for black frames, missing assets, frozen frames, crop errors, clipped words, and drift between voice and image.
- Watch and listen to the full short when the available tools permit. Otherwise clearly report the sampled coverage and what still needs human playback review. Never infer audible quality from a waveform alone.
- Deliver a fresh version instead of overwriting the only approved render. Include the edit decision list with source in/out times and output offsets, corrected captions, and relevant source/attribution notes so revisions are reproducible.

## Useful handoff fields

A compact project brief can contain: intended viewer and takeaway; destination and duration; approved style references; verified claims and sources; A-roll paths; B-roll source/time range/reuse basis; script beats; edit decisions; caption file; music/effects source; render settings; QA coverage; unresolved issues; creator-approved preferences.
