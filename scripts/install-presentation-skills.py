"""Install the presentation skill set into an explicitly chosen skill directory."""
import argparse
from pathlib import Path
import shutil


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', type=Path, required=True)
    parser.add_argument('--include-rtf', action='store_true', help='Also copy the optional video-analysis skill')
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1] / 'skills'
    target = args.destination.expanduser().resolve()
    names = ['scrolling-presentations', 'reference-led-ui', 'frontend-design', 'web-animation-design']
    if args.include_rtf:
        names.append('rtf')
    for name in names:
        if not (source / name / 'SKILL.md').is_file():
            parser.error(f'Source skill is missing: {name}')
    if target == source or source in target.parents:
        parser.error('Choose an installed-skills directory outside this repository’s skills folder.')
    conflicts = [name for name in names if (target / name).exists()]
    if conflicts:
        parser.error('Nothing copied. Existing skills would be overwritten: ' + ', '.join(conflicts)
                     + '. Review those folders or choose a fresh destination.')
    target.mkdir(parents=True, exist_ok=True)
    for name in names:
        shutil.copytree(source / name, target / name)
        print(f'Installed {name}')
    print('Start a fresh agent session. RTF dependencies, if selected, require separate setup.')


if __name__ == '__main__':
    main()
