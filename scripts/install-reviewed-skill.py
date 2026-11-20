"""Copy a reviewed repository skill to explicit local agent directories."""
import argparse
from datetime import datetime, timezone
import hashlib
from pathlib import Path
import shutil


def manifest(root):
    return {p.relative_to(root): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skill', choices=['humanizer', 'impeccable'], required=True)
    parser.add_argument('--destination', action='append', type=Path, required=True)
    parser.add_argument('--replace', action='store_true')
    parser.add_argument('--backup-dir', type=Path)
    args = parser.parse_args()
    source = (Path(__file__).resolve().parents[1] / 'skills' / args.skill).resolve()
    expected = manifest(source)
    if Path('SKILL.md') not in expected:
        parser.error('Reviewed source is missing.')
    backup_root = args.backup_dir.expanduser().resolve() if args.backup_dir else None
    targets = list(dict.fromkeys(p.expanduser().resolve() / args.skill for p in args.destination))
    if args.replace and backup_root is None:
        parser.error('--replace requires --backup-dir outside skill discovery.')
    for target in targets:
        if target == source or source in target.parents or target in source.parents:
            parser.error('Source and destination must not overlap.')
        if target.is_symlink() or getattr(target, 'is_junction', lambda: False)():
            parser.error(f'Refusing to replace a linked directory: {target}')
        if backup_root and (backup_root == target.parent or target.parent in backup_root.parents):
            parser.error('Backups must be outside skill discovery.')
        if target.exists() and manifest(target) != expected and not args.replace:
            parser.error(f'Existing different skill: {target}; review before replacing.')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    for index, target in enumerate(targets):
        if target.exists() and manifest(target) == expected:
            print(f'Already verified: {target}')
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            backup = backup_root / f'{args.skill}-{stamp}-{index}'
            if backup.exists():
                raise RuntimeError(f'Backup exists: {backup}')
            backup_root.mkdir(parents=True, exist_ok=True)
            target.rename(backup)
            print(f'Backed up to: {backup}')
        shutil.copytree(source, target)
        if manifest(target) != expected:
            raise RuntimeError(f'Copy verification failed: {target}')
        print(f'Verified: {target}')
    print('Reload skills or start a fresh agent session. No model settings changed.')


if __name__ == '__main__':
    main()
