# Screenshots of both apps (the UI/UX reference and the check)

Tools in `scripts/ui-shots/`; copy them to the scratchpad and adjust paths. Commit the results and the tools into the
new repo under `docs/porting/ui/` (`python/` or `source/`, `rails-before/`, `rails-after-*`, `tools/`).

## Source app (desktop)
- Drive the real app on a **throwaway database with demo data** (never the person's data): set the app's data-home
  environment variable to a temp folder and run its demo seed.
- Capture with the window's own pixels (`PrintWindow` via ctypes, flag 3 = client only + full content), **never a screen
  grab by coordinates**: at display scaling the window can exceed the screen, and a maximized window can land where the
  grab doesn't look — the first attempt captured the person's desktop instead of the app. If that happens, delete the
  images at once and tell the person.
- The window shows on the person's screen for about a minute: tell them before running, ask them not to click in it.
- `py_shots.py` is the customtkinter version (navigate each view and workspace tab, settle, PrintWindow, save PNG).
- For a web source app, use `shots.mjs` against it instead.

## Rails app
- `npm install playwright@<pinned>` in the tools folder with `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1`, and launch with
  `channel: "msedge"` — no browser download.
- Two-factor is required: `screens_user.rb` creates a development-only admin with a known OTP secret, `otp.rb` prints the
  current code. Both refuse to run outside development.
- `node shots.mjs <outDir> [baseUrl] [wslAppDir] [namePrefix]`, full-page screenshots at 1440×900, the tour suppressed.
- The app's dev database needs the demo client (`bin/rails db:seed:demo`).
- The Read tool shows PNGs: look at pairs yourself, and tell UI agents to do the same.

## What screenshots caught that tests didn't
- The whole theme and app shell gone (light indigo template vs the dark orange source).
- Two-level tabs flattened into one overflowing row; split-view registers turned into a list plus a drawer.
- A Dashboard still on phase 1 stand-in logic (checklist % instead of walkthrough progress): numbers disagreed with the
  source while every test passed.
- Whole cross-client screens (all findings, all risks, approval queue, checklist picker) never ported, hidden as
  "desktop-only" by the tour agent.
