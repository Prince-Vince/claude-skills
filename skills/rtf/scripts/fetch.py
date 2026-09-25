"""Pull what the analysis needs from a YouTube URL: captions, metadata, and a small
copy of the picture.

    python3 fetch.py <url> --out work/<id> [--no-video]

The picture is downloaded at the worst available quality on purpose. Nothing here needs
detail, only where and when things move, and a 360p copy of a twenty minute video is a
few tens of megabytes instead of a gigabyte.
"""
import argparse
import json
import pathlib
import subprocess
import sys
import re
from urllib.parse import urlsplit, parse_qs

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import tool, run  # noqa: E402


def validate_url(url):
    parsed = urlsplit(url)
    if (parsed.scheme != 'https' or parsed.username or parsed.password
            or parsed.port not in (None, 443)):
        raise ValueError('Use an HTTPS YouTube video URL without credentials.')
    host = parsed.hostname
    parts = parsed.path.strip('/').split('/')
    if host == 'youtu.be' and len(parts) == 1:
        ident = parts[0]
    elif host in ('youtube.com', 'www.youtube.com', 'm.youtube.com'):
        if parsed.path == '/watch':
            ident = parse_qs(parsed.query).get('v', [''])[0]
        elif len(parts) == 2 and parts[0] in ('shorts', 'live', 'embed'):
            ident = parts[1]
        else:
            ident = ''
    else:
        ident = ''
    if not re.fullmatch(r'[A-Za-z0-9_-]{11}', ident):
        raise ValueError('Expected a single YouTube video URL.')
    return 'https://www.youtube.com/watch?v=' + ident


def video_id(url):
    url = validate_url(url)
    out = run([tool('yt-dlp'), '--ignore-config', '--no-playlist', '--skip-download',
               '--print', '%(id)s', '--no-warnings', '--', url])
    return out.strip().splitlines()[-1]


def fetch(url, outdir, want_video=True):
    url = validate_url(url)
    outdir = pathlib.Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    if any(outdir.iterdir()):
        raise FileExistsError('Output directory must be empty; use a fresh folder.')
    ytdlp = tool('yt-dlp')
    node = tool('node', required=False)
    runtime = ['--js-runtimes', 'node:' + node] if node else []

    # Captions, in two separate passes so the two kinds never overwrite each other.
    # Automatic captions are the ones that carry per word offsets, so they are tried first;
    # uploaded subtitles usually only time a whole line and are the fallback.
    #
    # The language list is spelled out rather than given as en.* on purpose. That pattern
    # also matches YouTube's machine translations (en-sq, en-fr and forty more), and asking
    # for all of them in one go earns an HTTP 429.
    common = [ytdlp, '--ignore-config', '--no-playlist', '--skip-download', '--sub-format', 'json3', '--no-warnings',
              '--retries', '5', '--sleep-requests', '0.5',
              '--sub-langs', 'en-orig,en,en-US,en-GB'] + runtime

    try:
        run(common + ['--write-auto-sub', '--write-info-json',
                      '-o', str(outdir / 'auto.%(ext)s'), '--', url])
    except RuntimeError as err:
        print(f'  automatic captions unavailable: {err}', file=sys.stderr)
    captions = next(iter(sorted(outdir.glob('auto*.json3'))), None)

    if captions is None:
        try:
            run(common + ['--write-sub', '--write-info-json',
                          '-o', str(outdir / 'manual.%(ext)s'), '--', url])
        except RuntimeError as err:
            print(f'  uploaded subtitles unavailable: {err}', file=sys.stderr)
        captions = next(iter(sorted(outdir.glob('manual*.json3'))), None)

    if captions is None:
        sys.exit('No English captions available for this video. The transcript is the whole '
                 'basis of this analysis, so there is nothing to work from.\n'
                 'If you own the video, turn automatic captions on and try again.')

    info_path = next(iter(sorted(outdir.glob('*.info.json'))), None)
    info = json.loads(info_path.read_text(encoding='utf-8')) if info_path else {}
    meta = {
        'id': info.get('id', ''),
        'url': url,
        'title': info.get('title', ''),
        'channel': info.get('channel') or info.get('uploader', ''),
        'duration': info.get('duration', 0),
        'fps': round(info.get('fps') or 30),
        'width': info.get('width', 0),
        'height': info.get('height', 0),
        'captions': captions.name,
        'video': '',
    }

    if want_video:
        target = outdir / 'picture.mp4'
        if not target.exists():
            try:
                run([ytdlp, '--ignore-config', '--no-playlist', '--max-filesize', '250M',
                     '-f', 'worst[height>=240]/worst', '--no-warnings'] + runtime +
                    ['-o', str(target), '--', url])
            except RuntimeError as e:
                print(f'  picture download failed, continuing on the transcript alone\n  {e}',
                      file=sys.stderr)
        if target.exists():
            meta['video'] = target.name

    (outdir / 'meta.json').write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding='utf-8')
    return meta


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('url')
    ap.add_argument('--out', required=True)
    ap.add_argument('--no-video', action='store_true')
    a = ap.parse_args()
    m = fetch(a.url, a.out, want_video=not a.no_video)
    print(json.dumps(m, indent=2, ensure_ascii=False))
