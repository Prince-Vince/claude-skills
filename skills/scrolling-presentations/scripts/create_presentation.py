"""Copy the bundled working example into a new folder, without overwriting files."""
import argparse
from pathlib import Path
import shutil


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path, help='New output directory; must not exist')
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1] / 'assets' / 'microsoft-example'
    output = args.output.expanduser().resolve()
    if output.exists():
        parser.error('Output already exists. Choose a new folder; nothing was changed.')
    if output == source or source in output.parents:
        parser.error('Output must be outside the bundled example.')
    shutil.copytree(source, output)
    print(f'Created {output}')
    print('Open index.html. Replace the Microsoft example content for a different topic.')


if __name__ == '__main__':
    main()
