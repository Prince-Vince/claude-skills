# Optional RTF setup

This video-analysis helper is not required for browser presentations. Use it only when you want transcript timing or suggested overlay positions in a video that already exists.

Use Python 3.12, the version used in the original local setup. Create an isolated environment in the copied skill directory. From that directory:

Windows PowerShell:

```powershell
python -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
& .\.venv\Scripts\python.exe scripts/run.py --help
```

macOS / Linux:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/run.py --help
```

Invoke `run.py` from your working project with absolute or correctly resolved relative paths to both the environment's interpreter and the script. This keeps generated reports out of the installed skill. The pinned dependency versions match the original installation, but YouTube changes can require an update. Imageio-ffmpeg supplies an FFmpeg binary where a compatible wheel is available; otherwise install FFmpeg separately. Node.js on PATH is useful for YouTube's JavaScript challenges.

## Provenance and changes

Original source: user-supplied `RTFSkill.zip`, SHA-256 `63DA97FF6945053C18EC8C569477FF1D8BD1C4F8CAFD034D05A9D0CCC5A7B0DD`.

This is not an official upstream release. Original authorship is not claimed. The archive did not provide a license notice in the inspected skill files, so this backup does not assign it a new license.

Prior hardening retained:

- Unique output folders; no recursive deletion of old runs.
- Single HTTPS YouTube video validation; no playlists or inherited yt-dlp config.
- Text-node transcript highlighting instead of inserting transcript text through innerHTML.
- UTF-8 handling and support for an isolated Python environment.
- Optional imageio-ffmpeg tool lookup; 250 MB video size limit.

Portability changes in this backup:

- Removed the original user's absolute Node.js runtime path. Use PATH or standard install locations.
- Replaced machine-specific invocation instructions and wheel inventory with portable setup instructions and pinned direct dependencies.
- Excluded virtual environments, downloaded media, generated reports, and the original example transcript.

Validation scope: source review, syntax checks, local helper tests, and `--help`. No new full video download or end-to-end analysis is claimed by this packaging task. Static review is not a guarantee of safety.
