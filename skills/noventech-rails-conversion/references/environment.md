# Environment and repo setup (Windows host)

## WSL2 + Ubuntu
- `wsl --install` from a non-admin shell fails silently; run it elevated so the person gets the UAC prompt, capturing output:
  `Start-Process powershell.exe -ArgumentList "-NoProfile","-Command","wsl.exe --install -d Ubuntu --no-launch *> '<log>'" -Verb RunAs -Wait`
- Reboot. If no Ubuntu window appears, `wsl.exe --install -d Ubuntu --no-launch` (no admin needed now), then the person
  opens Ubuntu from the Start menu and creates a lowercase username + password.
- A firmware "virtualization disabled" reading can be wrong; trust a successful `wsl -d Ubuntu -u root -- uname -r`.
- System packages as root: `build-essential git curl ca-certificates sqlite3 libsqlite3-dev libssl-dev libyaml-dev zlib1g-dev libffi-dev libgmp-dev libreadline-dev rustc pkg-config libvips`.

## Ruby and Rails (as the user)
- `curl -fsSL https://mise.run | sh`; add `eval "$(~/.local/bin/mise activate bash)"` to `~/.bashrc` AND
  `export PATH="$HOME/.local/bin:$HOME/.local/share/mise/shims:$PATH"` to `~/.profile` (login and VS Code shells).
- `mise use -g ruby@latest`, `gem install rails --no-document`.
- An Ubuntu window opened before this won't see Ruby: open a new one or `source ~/.bashrc`.
- Git: `user.name`, `user.email`, and the Windows Git Credential Manager as helper so GitLab sign-in is shared:
  `git config --global credential.helper "/mnt/c/Program\ Files/Git/mingw64/bin/git-credential-manager.exe"`.

## Generating the app
- Clone the template into the Linux home (`~/noventech-rails-template`), never under `/mnt/c` (slow).
- `~/noventech-rails-template/bin/new-app <name>`; then `bin/ci` must end with "Continuous Integration passed".
- `config/master.key` exists only locally and is gitignored: the person backs it up to their password manager
  (`\\wsl.localhost\Ubuntu\home\<user>\<app>\config\master.key`).
- First login: `admin@example.com` / `change-me-please`, then required TOTP 2FA. 1Password's browser extension can scan
  the QR code (item → add One-Time Password field → QR icon).

## New GitLab repo
- The saved git credential is usually a password, which the GitLab API rejects (it needs a personal access token).
  Push-to-create works with a password: push a one-README commit to `https://gitlab.nvtlabs.com/<user>/<repo>.git`.
- `main` is then protected against force pushes: merge the placeholder into the generated app
  (`git merge origin/main --allow-unrelated-histories -X ours`) instead of force-pushing.
- The project is private under the person's namespace; Joe needs adding as a member (or transfer to a group).

## Running commands from Windows tools
- PowerShell mangles quotes and `$` inside `wsl.exe -- bash -lc "..."`. For anything beyond a one-liner, write a `.sh`
  file (Write tool) and run `wsl.exe -d Ubuntu -- bash -l /mnt/c/Users/<user>/AppData/Local/Temp/.../script.sh`.
  Use the long path (`Vince.Davis`), not the 8.3 short name; `wslpath` strips backslashes.
- Piping a PowerShell here-string into bash adds a BOM that breaks the first line. Use files.
- In the Bash tool (Git Bash), `~` and `/tmp` are Windows paths. Never write project files from Git Bash.
- Edit files in WSL through `\\wsl.localhost\Ubuntu\home\<user>\...` with the Write/Edit tools.
- Node is on Windows, not WSL: syntax-check Stimulus controllers by copying them to `.mjs` and running `node --check`.
- `$env:WSL_UTF8=1` before `wsl.exe` makes its own messages readable.
