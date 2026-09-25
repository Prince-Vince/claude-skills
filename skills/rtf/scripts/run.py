"""One command, start to finish.

    python3 run.py "https://youtu.be/VIDEO_ID"
    python3 run.py "<url>" --out ~/Desktop/analysis --top 10
    python3 run.py "<url>" --no-video        # transcript only, much faster, no screen check

Produces, in the output folder:
    report.html    the whole thing in one file you can send to anyone
    rtf.json       every word with its timestamp, plus sentences
    words.tsv      seconds<TAB>word, one row per word
    moments.json   the ranked moments with their scores and reasons
    picture.json   where the speaker sits and how still the screen is
"""
import argparse
import pathlib
import sys
import time
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import fetch  # noqa: E402
import moments as moments_mod  # noqa: E402
import picture as picture_mod  # noqa: E402
import report as report_mod  # noqa: E402
import transcript as transcript_mod  # noqa: E402
from common import slug, tc, tool  # noqa: E402


def step(n, total, msg):
    print(f'[{n}/{total}] {msg}', flush=True)


def main():
    ap = argparse.ArgumentParser(description='Timestamp every word of a YouTube video and '
                                             'find the moments worth a graphic.')
    ap.add_argument('url')
    ap.add_argument('--out', help='output folder (default: ./rtf-<video title>)')
    ap.add_argument('--top', type=int, default=8, help='how many moments to return')
    ap.add_argument('--min-gap', type=float, default=None,
                    help='seconds to leave between moments (default: scaled to the video)')
    ap.add_argument('--no-video', action='store_true',
                    help='skip the picture download and the screen check')
    a = ap.parse_args()

    fetch.validate_url(a.url)
    if a.top < 1:
        ap.error('--top must be at least 1')
    tool('yt-dlp')
    if not a.no_video:
        tool('ffmpeg')

    started = time.time()
    total = 4 if a.no_video else 5

    step(1, total, 'fetching captions' + ('' if a.no_video else ' and a small copy of the video'))
    staging = pathlib.Path(a.out) if a.out else None
    if staging is not None:
        staging.mkdir(parents=True, exist_ok=False)
    tmp = staging or pathlib.Path(tempfile.mkdtemp(prefix='rtf-', dir=pathlib.Path.cwd()))
    meta = fetch.fetch(a.url, tmp, want_video=not a.no_video)

    if staging is None:
        # Keep the unique folder. Never delete or replace a previous run.
        work = tmp
    else:
        work = staging

    step(2, total, 'mapping every word to its timestamp')
    rtf = transcript_mod.build(work)
    print(f'      {rtf["word_count"]:,} words, {len(rtf["sentences"])} sentences')

    n = 2
    if not a.no_video:
        n += 1
        step(n, total, 'reading the picture: where the speaker sits, when the screen is parked')
        pic = picture_mod.analyse(work)
        if pic:
            sp = pic['hotspot']
            where = f"{sp['looks_like']} {sp['position']}" if sp.get('found') else 'nothing moving'
            print(f'      {where}, screen still '
                  f'{int(pic["still_share"] * 100)}% of the time')

    n += 1
    step(n, total, 'scoring the moments')
    found = moments_mod.find(work, top=a.top, min_gap=a.min_gap)

    n += 1
    step(n, total, 'writing the report')
    out = report_mod.build(work)

    print(f'\ndone in {time.time() - started:.0f}s\n')
    print(f'{"#":>2}  {"in":>9}  {"len":>5}  why')
    for m in found:
        why = ', '.join(s['label'] for s in m['signals'][:2]) or 'strong line'
        print(f'{m["rank"]:>2}  {m["tc_in"]:>9}  {m["dur"]:>4.1f}s  {why}')
    print(f'\nreport   {out}')
    print(f'folder   {work}')


if __name__ == '__main__':
    main()
