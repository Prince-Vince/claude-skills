---
name: short-form-video-workflow
description: Research and script original talking-head Shorts or Reels, then edit supplied A-roll with B-roll, captions, music, and purposeful graphics. Use for an end-to-end short-form video workflow or a specific stage, including learning from approved edits and channel performance.
---

# Short-form video workflow

Turn a topic or source URL into a recordable script, then turn the creator's raw talking-head footage into a reviewed short. Support research-only, script-only, edit-only, and revision requests without forcing the entire pipeline.

## Establish the brief

Use conversation context first: intended viewer, takeaway, destination, duration, source links, footage paths, and any reference videos. Ask one focused question only when the missing answer materially affects the result. For an unspecified Short/Reel, propose vertical 1080 × 1920 and roughly 30–60 seconds as adjustable defaults. Preserve deliberate pauses and the creator's natural voice.

Distinguish creator decisions from assumptions. Never treat the tutorial that inspired this workflow as the creator's brand, catchphrase, channel identity, or editing style. Start with one complete short before expanding into a production system.

Use a dedicated output directory for each video with source notes, script, edit plan, captions, and rendered versions. Preserve originals and keep intermediates separate. Do not put footage, private channel analytics, credentials, or temporary download URLs in a skill or Git repository.

## Check capabilities for the requested stage

- Discover current vidIQ tools and their schemas; do not assume installation means account authorization. For private analytics resolve the authorized channel and ask if multiple candidates remain. Public-reference research does not require linking the user's channel. Use available vidIQ workflow guidance when relevant.
- Inspect available yt-dlp, FFmpeg/ffprobe, transcription, and graphics capabilities. Resolve real executable paths rather than assuming PATH is current. Do not install dependencies, connect accounts, change permissions, or start subscriptions without existing user authorization for that setup.
- Treat vidIQ credit estimates and service prices as current tool data. Stay within an authorized budget, avoid duplicate calls, and pause paid operations whose cost is unknown. Report actual usage only when returned.
- Transcription may use an available local engine or an authorized service. ElevenLabs is optional for transcription, music, or effects. Use existing licensed audio or omit music with disclosure when generation is unavailable. Private footage must not be uploaded to an external service without authorization covering that transfer.
- Hyperframes or Remotion can provide designed overlays and motion graphics; Blender is optional for concepts that actually benefit from 3D. Use their available guidance when producing those assets. Do not make every renderer a prerequisite for an ordinary edit.

## Research and script

1. Read the primary source and separate verified facts from promotional claims. Use vidIQ for relevant public videos, transcripts, keywords, and comparable performance when requested and available. If unavailable, continue from supplied references and primary sources and state the evidence limit.
2. Compare a small relevant sample, accounting for publication age, channel baseline, format, and audience. Record source URLs and retrieval dates. Describe observations separately from explanations you are testing. Views alone do not establish why an edit worked; a transcript alone does not reveal visual pacing.
3. Look for useful patterns: first-frame clarity, hook, concrete demonstration, explanation density, payoff, recurring viewer questions, and retention when authorized data exists. Create original material, not lightly rewritten competitor scripts.
4. Deliver a hook, conversational script or talking-point outline, approximate spoken duration, and a compact shot list connecting each beat with footage or graphics. Give title options when useful. Verify claims against sources and flag uncertainty. Any rubric score is an editorial assessment, not a predicted view count or guaranteed virality.
5. Prefer filmable instructions over ornate prose. Let the user record in their own words. For script-only work, stop at a complete recordable artifact; for supplied footage, proceed to editing within scope.

## Edit supplied footage

Read [editing-and-review.md](references/editing-and-review.md) for the cut, mix, caption, and quality checks.

1. Inspect media metadata, rotation, frame rate, audio, and usable framing. Produce a timestamped transcript with word timing when possible; inspect waveform or voice-activity boundaries as well.
2. Make an edit decision list referencing original files and source in/out times. Remove false starts, duplicate attempts, mistakes, and excess dead air while preserving meaning. Choose the best complete take, not just the shortest transcript.
3. Assemble a rough A-roll cut before expensive graphics. Review the transitions with sound. Avoid a mandatory approval gate unless the user asked for staged review or there is a consequential unresolved choice.
4. Map B-roll to the spoken claim. Prefer the creator's footage and authorized source assets. A public URL is not permission to republish. Track source, selected time range, attribution, and reuse basis. yt-dlp is an acquisition tool, not a license grant; do not bypass access controls. Inspect sampled frames and the chosen segments before claiming they illustrate the point.
5. Add readable timed captions, B-roll, restrained graphics, and a music bed/effects where appropriate. Keep the face, demonstration, and captions clear of platform controls. Use animation to explain a concept or direct attention rather than fill every pause.
6. Render a versioned output and inspect the actual exported file. Fix detected problems within scope, retain the editable plan and caption files, and report any unresolved limitations.

## Deliver and improve

Return a playable video or file link, editable supporting files, and a concise account of what changed and what was checked. Distinguish implemented, technically checked, watched/listened to, and validated by the creator. Do not claim a full review if only sampled frames or segments were examined.

Translate feedback into an observable change: for example, “the cut clips the last consonant” means moving the out-point after the sound ends; “too busy” may mean fewer overlays, longer shot holds, or less caption emphasis. Preserve approved choices across revisions.

When asked to save learning, update a project style profile or this skill with stable, approved preferences. Keep video-specific facts and channel analytics out of reusable instructions. Do not silently modify unrelated skills or create recurring jobs. Periodic channel analysis should compare meaningful samples and suggest experiments; apply enduring rule changes only when the user's request covers them.

Publishing, scheduling, replacing thumbnails or metadata, and responding to comments are separate actions. Preparing a video does not authorize them. For requested account changes, use the service's required exact-target and final-value approval flow.
