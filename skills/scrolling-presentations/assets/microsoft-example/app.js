'use strict';
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const chapters = [...document.querySelectorAll('.chapter')];
const nav = document.querySelector('.chapter-nav');
const motionButton = document.querySelector('#motion');
let paused = reduceMotion.matches;
let storyTimer = null;
let step = 0;
document.documentElement.classList.add('js-motion');
chapters.forEach((chapter, i) => {
  const link = document.createElement('a');
  link.href = '#' + chapter.id;
  link.setAttribute('aria-label', `${i + 1}. ${chapter.dataset.title}`);
  const label = document.createElement('span');
  label.textContent = chapter.dataset.title;
  link.append(label);
  nav.append(link);
});
const navLinks = [...nav.querySelectorAll('a')];
let pendingScroll = false;
function updateScroll() {
  const scrollable = document.documentElement.scrollHeight - window.innerHeight;
  document.querySelector('#progress').style.width = `${scrollable > 0 ? window.scrollY / scrollable * 100 : 0}%`;
  let active = 0;
  chapters.forEach((chapter, i) => { if (chapter.getBoundingClientRect().top < window.innerHeight * .42) active = i; });
  navLinks.forEach((link, i) => {
    link.classList.toggle('active', i === active);
    if (i === active) link.setAttribute('aria-current', 'location'); else link.removeAttribute('aria-current');
  });
  document.querySelector('#chapter-count').textContent = `${String(active + 1).padStart(2, '0')} / ${chapters.length}`;
  pendingScroll = false;
}
window.addEventListener('scroll', () => { if (!pendingScroll) { pendingScroll = true; requestAnimationFrame(updateScroll); } }, {passive:true});
window.addEventListener('resize', updateScroll);
updateScroll();
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    entry.target.classList.toggle('in-view', entry.isIntersecting);
    if (entry.isIntersecting) entry.target.classList.add('seen');
    if (entry.target.classList.contains('journey-stage') && !entry.isIntersecting) stopStory();
  });
}, {threshold:.1});
document.querySelectorAll('.reveal').forEach(element => observer.observe(element));
function setMotion() {
  document.documentElement.classList.toggle('paused', paused);
  motionButton.textContent = paused ? 'Resume motion' : 'Pause motion';
  motionButton.setAttribute('aria-pressed', String(paused));
  if (paused) stopStory();
}
motionButton.addEventListener('click', () => { paused = !paused; setMotion(); });
reduceMotion.addEventListener('change', e => { paused = e.matches; setMotion(); });
document.addEventListener('keydown', event => {
  if (['INPUT','TEXTAREA','SELECT','BUTTON','A'].includes(document.activeElement.tagName)) return;
  if (!['ArrowRight','ArrowLeft'].includes(event.key) || event.ctrlKey || event.altKey || event.metaKey) return;
  const current = navLinks.findIndex(link => link.classList.contains('active'));
  const next = Math.max(0, Math.min(chapters.length - 1, current + (event.key === 'ArrowRight' ? 1 : -1)));
  chapters[next].scrollIntoView({behavior:paused ? 'instant' : 'smooth'});
});
const story = [
  ['Ask for a laptop.', 'The agent explains the policy. Configured Copilot Studio actions let it start the request.'],
  ['Check. Create. Confirm.', 'The agent flow checks eligibility, creates the Dataverse record, and returns a request ID.'],
  ['Route the work.', 'Power Automate reacts to the request, routes approvals, and sends updates.'],
  ['Bring in the supplier.', 'The supplier submits a quote through Power Pages. It joins the shared request in Dataverse.'],
  ['Let staff decide.', 'Your team reviews the quote in Power Apps. Record changes can trigger the next automation.'],
  ['Optional: analyze the exception.', 'A Foundry capability can analyze a complex quote before approval. Integrate it only if needed.']
];
story.forEach((_, i) => {
  const dot = document.createElement('button');
  dot.setAttribute('aria-label', `Show walkthrough step ${i + 1}`);
  dot.addEventListener('click', () => { stopStory(); showStep(i); });
  document.querySelector('#story-dots').append(dot);
});
function showStep(index) {
  step = index;
  document.querySelector('#story-number').textContent = `0${step + 1} / 0${story.length}`;
  document.querySelector('#story-title').textContent = story[step][0];
  document.querySelector('#story-text').textContent = story[step][1];
  document.querySelectorAll('.journey-node').forEach((node, i) => {
    node.classList.toggle('active', step === i);
    node.setAttribute('aria-pressed', String(step === i));
  });
  document.querySelector('.optional-foundry').classList.toggle('active', step === story.length - 1);
  document.querySelectorAll('#story-dots button').forEach((dot, i) => {
    dot.classList.toggle('active', step === i);
    dot.setAttribute('aria-pressed', String(step === i));
  });
  document.querySelector('#previous-step').disabled = step === 0;
  document.querySelector('#next-step').textContent = step === story.length - 1 ? 'Restart ↺' : 'Next step →';
}
function stopStory() {
  clearInterval(storyTimer);
  storyTimer = null;
  const button = document.querySelector('#play-story');
  button.textContent = '▶ Play walkthrough';
  button.setAttribute('aria-pressed','false');
}
document.querySelector('#previous-step').addEventListener('click', () => {stopStory(); showStep(Math.max(0, step - 1));});
document.querySelector('#next-step').addEventListener('click', () => {stopStory(); showStep((step + 1) % story.length);});
document.querySelectorAll('.journey-node').forEach(node => node.addEventListener('click', () => {stopStory(); showStep(Number(node.dataset.step));}));
document.querySelector('#play-story').addEventListener('click', () => {
  if (storyTimer) {stopStory(); return;}
  if (paused) {paused = false; setMotion();}
  if (step === story.length - 1) showStep(0);
  const button = document.querySelector('#play-story');
  button.textContent = 'Ⅱ Pause walkthrough';
  button.setAttribute('aria-pressed','true');
  storyTimer = setInterval(() => {
    if (step < story.length - 1) showStep(step + 1); else stopStory();
  }, 6500);
});
document.addEventListener('visibilitychange', () => {if (document.hidden) stopStory();});
const needs = {
  knowledge: ['A knowledge agent.', 'Agent Builder plus a maintained knowledge source.', ['Microsoft 365 agent','SharePoint'], 'Add Copilot Studio when you need actions.'],
  task: ['An agent with an action.', 'Use an agent flow to check inputs, perform steps, and return a result.', ['Copilot Studio','Agent flow'], 'Reuse a suitable existing flow first.'],
  process: ['A business automation.', 'Power Automate connects the process across systems.', ['Power Automate','Existing systems'], 'Especially useful for existing flows or desktop tasks.'],
  workspace: ['A staff workspace.', 'Power Apps gives your team forms and work queues.', ['Power Apps','Data source'], 'Model-driven apps use Dataverse.'],
  portal: ['An external portal.', 'Power Pages lets customers or suppliers submit and track information.', ['Power Pages','Dataverse'], 'Set access through authentication and table permissions.'],
  ai: ['A specialized AI capability.', 'Foundry adds model choice, custom agents, and evaluation.', ['Microsoft Foundry'], 'Add it only when simpler tools fall short.']
};
document.querySelectorAll('[data-need]').forEach(button => button.addEventListener('click', () => {
  const [title, text, tags, next] = needs[button.dataset.need];
  document.querySelectorAll('[data-need]').forEach(other => {other.classList.toggle('selected',other===button);other.setAttribute('aria-pressed',String(other===button));});
  document.querySelector('#recommend-title').textContent = title;
  document.querySelector('#recommend-text').textContent = text;
  document.querySelector('#recommend-next').textContent = next;
  document.querySelector('#recommend-tags').replaceChildren(...tags.map(text => {const tag=document.createElement('span');tag.textContent=text;return tag;}));
}));
showStep(0);
setMotion();

let quoteSubmitted = false;
document.querySelector('#submit-quote').addEventListener('click', () => {
  quoteSubmitted = !quoteSubmitted;
  document.querySelector('.pages-stage').classList.toggle('quote-received', quoteSubmitted);
  document.querySelector('#quote-status').textContent = quoteSubmitted ? 'Quote received · Ready for review' : 'Awaiting supplier quote';
  document.querySelector('#portal-feedback').textContent = quoteSubmitted ? 'Sample saved in this demo only.' : 'Demo only. Nothing is sent.';
  document.querySelector('#submit-quote').textContent = quoteSubmitted ? 'Reset demo ↺' : 'Submit sample quote →';
});
document.querySelectorAll('a[href^="#source-"]').forEach(link => link.addEventListener('click', () => {
  const target = document.getElementById(link.getAttribute('href').slice(1));
  if (target) {
    const drawer = target.closest('details');
    if (drawer) drawer.open = true;
  }
}));
