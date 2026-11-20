"""Install reviewed Humanizer files into explicitly chosen agent skill directories.

Uses only Python's standard library. No networking, package installs, or skill
execution. Existing copies require --replace and are backed up outside discovery.
"""
import argparse
from datetime import datetime, timezone
import hashlib
from pathlib import Path
import shutil


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', action='append', type=Path, required=True)
    parser.add_argument('--replace', action='store_true')
    parser.add_argument('--backup-dir', type=Path)
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1] / 'skills' / 'humanizer'
    source = source.resolve()
    expected = {p.relative_to(source): digest(p) for p in source.rglob('*') if p.is_file()}
    if Path('SKILL.md') not in expected:
        parser.error('Humanizer source is missing.')
    targets = list(dict.fromkeys((p.expanduser().resolve() / 'humanizer') for p in args.destination))
    backup_root = args.backup_dir.expanduser().resolve() if args.backup_dir else None
    if args.replace and backup_root is None:
        parser.error('--replace requires --backup-dir outside all skill directories.')
    for target in targets:
        if target == source or source in target.parents or target in source.parents:
            parser.error('Destination overlaps the source skill.')
        if backup_root and (backup_root == target.parent or target.parent in backup_root.parents):
            parser.error('Backups must be outside skill discovery directories.')
        if target.is_symlink():
            parser.error(f'Refusing to replace a symlink: {target}')
        if target.exists() and not args.replace:
            parser.error(f'Existing skill: {target}. Review it before using --replace.')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    for index, target in enumerate(targets):
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            # All moves are between already resolved, explicit skill/backup paths.
            backup = backup_root / f'humanizer-{stamp}-{index}'
            if backup.exists():
                parser.error(f'Backup already exists: {backup}')
            backup_root.mkdir(parents=True, exist_ok=True)
            target.rename(backup)
            print(f'Backed up {target} to {backup}')
        shutil.copytree(source, target)
        actual = {p.relative_to(target): digest(p) for p in target.rglob('*') if p.is_file()}
        if actual != expected:
            raise RuntimeError(f'Installed files do not match the reviewed source: {target}')
        print(f'Verified Humanizer: {target}')
    print('Reload skills or start a fresh agent session. No model settings were changed.')


if __name__ == '__main__':
    main()
