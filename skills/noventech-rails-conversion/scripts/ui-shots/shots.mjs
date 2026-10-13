// Screenshot Rails screens for the UI/UX comparison with docs/porting/ui/python. Uses the installed Edge (no browser
// download). Run from Windows (node is on Windows): node shots.mjs <outDir> [baseUrl] [wslAppDir] [onlyPrefix]
//   e.g. node shots.mjs C:\shots\mine http://localhost:3005 /home/vincedavis/wt/theme 1
// The app's development database needs the demo client (bin/rails db:seed:demo).
import { chromium } from "playwright";
import { execSync } from "node:child_process";
import { mkdirSync } from "node:fs";
import { dirname } from "node:path";
import { fileURLToPath } from "node:url";

const out = process.argv[2] || "rails";
const BASE = process.argv[3] || "http://localhost:3000";
const APP = process.argv[4] || "/home/vincedavis/ai-governance-tracker";
const ONLY = process.argv[5] || "";
// The .rb helpers sit next to this script; WSL sees Windows paths under /mnt/<drive>.
const here = dirname(fileURLToPath(import.meta.url)).replace(/\\/g, "/");
const W = here.startsWith("/") ? here : `/mnt/${here[0].toLowerCase()}${here.slice(2)}`;
const rails = (script) =>
  execSync(`wsl.exe -d Ubuntu -- bash -lc "cd ${APP} && bin/rails runner ${W}/${script} 2>/dev/null"`, { encoding: "utf8" }).trim().split("\n").pop();

mkdirSync(out, { recursive: true });
const { password, client_id: c } = JSON.parse(rails("screens_user.rb"));

const pages = [
  ["01-dashboard", "/"],
  ["02-clients", "/clients"],
  ["10-overview", `/clients/${c}/overview`],
  ["11-tenant", `/clients/${c}/tenant`],
  ["12-engagement", `/clients/${c}/engagement`],
  ["12b-step-S01", `/clients/${c}/walkthrough/steps/S01`],
  ["12c-next-steps", `/clients/${c}/next-steps`],
  ["12d-intake-cockpit", `/clients/${c}/intake`],
  ["12e-intake-all", `/clients/${c}/intake?view=all`],
  ["12f-session", `/clients/${c}/session`],
  ["13-checklist", `/clients/${c}/checklist`],
  ["14-ai-tools", `/clients/${c}/ai-tools`],
  ["15-use-cases", `/clients/${c}/use-cases`],
  ["15b-risks", `/clients/${c}/risks`],
  ["16-findings", `/clients/${c}/findings`],
  ["17-incidents", `/clients/${c}/incidents`],
  ["18-admin-log", `/clients/${c}/admin-log`],
  ["19-notes", `/clients/${c}/notes`],
  ["20-history", `/clients/${c}/activities`],
  ["21-readiness", `/clients/${c}/readiness`],
  ["22-data-governance", `/clients/${c}/governance-policies`],
  ["23-dlp", `/clients/${c}/dlp`],
  ["24-overshared", `/clients/${c}/overshared-files`],
  ["25-ai-policy", `/clients/${c}/ai-policy/discovery`],
  ["26-deliverables", `/clients/${c}/deliverables`],
  ["30-vendors", "/vendors"],
  ["31-knowledge", "/knowledge"],
  ["32-scope", "/service_scope"],
  ["33-reports", "/reports"],
  ["34-help", "/help"],
  ["35-admin-cipp", "/admin/cipp"],
];

const browser = await chromium.launch({ channel: "msedge", headless: true });
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
await page.addInitScript(() => { try { localStorage.setItem("aigt.tour", JSON.stringify({ dismissed: true, offered: true })); } catch (_) {} });
await page.goto(`${BASE}/users/sign_in`);
await page.getByLabel("Email").fill("screens@noventech.local");
await page.getByLabel("Password").fill(password);
await page.getByRole("button", { name: "Sign in" }).click();
await page.getByLabel("Authentication code").fill(rails("otp.rb"));
await page.getByLabel("Authentication code").press("Enter");
await page.waitForLoadState("networkidle");

for (const [name, path] of pages.filter(([n]) => n.startsWith(ONLY))) {
  const response = await page.goto(BASE + path);
  await page.waitForLoadState("networkidle");
  await page.screenshot({ path: `${out}/${name}.png`, fullPage: true });
  console.log(`${name}: ${response.status()} ${page.url().replace(BASE, "")}`);
}
await browser.close();
