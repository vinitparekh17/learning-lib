"use strict";

// Original finite teaching histories; these are not live cache operations.
const cacheLab = document.querySelector(".cache-lab");
if (cacheLab) {
  const histories = {
    race: [
      ["Initial state", "7", "0", "empty", "empty", "The cache has no value. Reader A has not obtained a token."],
      ["A misses and obtains token 0", "7", "0", "empty", "empty", "The token is obtained before the source read."],
      ["A reads revision 7", "7", "0", "empty", "empty", "Revision 7 now sits in A's local memory."],
      ["B commits revision 8", "8", "0", "empty", "empty", "The cache has not received invalidation yet."],
      ["B invalidates the cache", "8", "1", "empty", "empty", "Invalidation clears the value and advances the guarded generation."],
      ["A tries to fill revision 7 using token 0", "8", "1", "7", "empty", "Unguarded fill succeeds. The guarded fill is rejected because 0 does not equal 1."],
      ["New reader C checks the cache", "8", "1", "7", "empty", "C gets old data from the unguarded cache. The guarded cache misses. This does not tell us what A returned to its own caller."]
    ],
    replica: [
      ["B has committed and invalidated", "8", "1", "empty", "empty", "A source replica is still at revision 7."],
      ["A obtains token 1", "8", "1", "empty", "empty", "The token is current; its ordering is correct."],
      ["A reads revision 7 from the lagging replica", "8", "1", "empty", "empty", "The original latest-committed source-read assumption no longer holds."],
      ["A fills using token 1", "8", "1", "7", "7", "Both caches accept revision 7. A valid token is not proof of source freshness. A revision floor or stronger source read is needed for that contract."]
    ],
    reset: [
      ["A holds token 0 and revision 7", "7", "0", "empty", "empty", "A pauses before filling."],
      ["B commits and invalidates", "8", "1", "empty", "empty", "Token 0 is now invalid."],
      ["Guard metadata disappears and is recreated at 0", "8", "0", "empty", "empty", "This deliberately breaks the non-reuse assumption."],
      ["A fills with its old token 0", "8", "0", "7", "7", "Both caches accept revision 7. Retaining values and retaining guard identity have different correctness requirements."]
    ]
  };
  const scenario = cacheLab.querySelector("select");
  const previous = cacheLab.querySelector("[data-cache-prev]");
  const next = cacheLab.querySelector("[data-cache-next]");
  let step = 0;
  function renderCacheStep() {
    const history = histories[scenario.value];
    const [event, db, generation, unguarded, guarded, explanation] = history[step];
    const output = cacheLab.querySelector("[data-cache-output]");
    output.replaceChildren();
    const heading = document.createElement("h3");
    heading.textContent = `Step ${step + 1} of ${history.length}: ${event}`;
    const state = document.createElement("dl");
    state.className = "cache-state";
    for (const [name, value] of [["Authoritative revision", db], ["Cache generation", generation], ["Unguarded cache", unguarded], ["Guarded cache", guarded]]) {
      const group = document.createElement("div");
      const term = document.createElement("dt");
      const detail = document.createElement("dd");
      term.textContent = name;
      detail.textContent = value;
      group.append(term, detail);
      state.append(group);
    }
    const note = document.createElement("p");
    note.textContent = explanation;
    output.append(heading, state, note);
    previous.disabled = step === 0;
    next.disabled = step === history.length - 1;
  }
  previous.addEventListener("click", () => { step = Math.max(0, step - 1); renderCacheStep(); });
  next.addEventListener("click", () => { step = Math.min(histories[scenario.value].length - 1, step + 1); renderCacheStep(); });
  cacheLab.querySelector("[data-cache-reset]").addEventListener("click", () => { step = 0; renderCacheStep(); });
  scenario.addEventListener("change", () => { step = 0; renderCacheStep(); });
  renderCacheStep();
}

const {modules, levels} = window.sdeCatalog;
const storageKey = "sde-foundations.study.v1";
const records = Object.keys(modules);
const setText = (selector, text) => document.querySelectorAll(selector).forEach(node => {
  node.textContent = text;
});
const hasModule = key => Object.hasOwn(modules, key);

function loadStudy() {
  try {
    const stored = JSON.parse(localStorage.getItem(storageKey)) ?? {};
    const items = Object.fromEntries(Object.entries(stored.items ?? {}).filter(
      ([key, value]) => hasModule(key) && Number.isInteger(value) && value > 0 && value < levels.length
    ));
    return {items, last: hasModule(stored.last) ? stored.last : ""};
  } catch {
    return {items: {}, last: ""};
  }
}

let study = loadStudy();
function saveStudy() {
  try {
    localStorage.setItem(storageKey, JSON.stringify(study));
    return true;
  } catch {
    document.querySelectorAll("[data-storage-warning]").forEach(node => { node.hidden = false; });
    return false;
  }
}

const currentModule = document.body.dataset.module;
if (hasModule(currentModule)) {
  study.last = currentModule;
  saveStudy();
}

function showStudy() {
  const studied = records.filter(key => study.items[key] > 0);
  setText("[data-studied-count]", studied.length);
  setText("[data-reproduce-count]", studied.filter(key => study.items[key] >= 2).length);
  setText("[data-defend-count]", studied.filter(key => study.items[key] === 4).length);
  setText("[data-side-count]", studied.length + " / " + records.length);

  document.querySelectorAll("[data-meter]").forEach(meter => {
    meter.style.width = (100 * studied.length / records.length) + "%";
  });
  document.querySelectorAll("[data-module-state]").forEach(node => {
    const level = study.items[node.dataset.moduleState] ?? 0;
    node.textContent = levels[level];
    node.classList.toggle("recorded", level > 0);
  });
  document.querySelectorAll("[data-track-progress]").forEach(node => {
    const group = records.filter(key => modules[key].track === node.dataset.trackProgress);
    node.textContent = group.filter(key => study.items[key] > 0).length + " of " + group.length + " with a recorded level";
  });
  document.querySelectorAll("[data-chip]").forEach(node => {
    const key = node.dataset.chip;
    const level = study.items[key] ?? 0;
    node.classList.toggle("recorded", level > 0);
    node.setAttribute("aria-label", key + " " + modules[key].title + ", " + levels[level]);
    node.title = modules[key].title;
  });
  document.querySelectorAll("[data-level]").forEach(select => {
    select.value = study.items[select.dataset.level] ?? 0;
  });
  const resume = document.querySelector("[data-continue]");
  if (resume && hasModule(study.last)) {
    resume.href = modules[study.last].url;
    resume.textContent = "Resume " + study.last + " →";
    setText("[data-resume-message]", "Last opened " + study.last + " · " + modules[study.last].title);
  }
}

const levelSelect = document.querySelector("[data-level]");
levelSelect?.addEventListener("change", () => {
  const key = levelSelect.dataset.level;
  const level = Number(levelSelect.value);
  if (level) study.items[key] = level;
  else delete study.items[key];
  const saved = saveStudy();
  if (saved) setText("[data-level-note]", level ? "Saved in this browser · " + levels[level] : "Study level cleared.");
  showStudy();
});

window.addEventListener("pageshow", event => {
  if (event.persisted) {
    study = loadStudy();
    showStudy();
  }
});
window.addEventListener("storage", event => {
  if (event.key !== storageKey && event.key !== null) return;
  study = loadStudy();
  showStudy();
});
showStudy();

const filters = Array.from(document.querySelectorAll("[data-filter]"));
const groups = document.querySelectorAll("[data-track]");
function filterTopics() {
  const value = new URL(location.href).searchParams.get("track") ?? "";
  const selected = filters.some(button => button.dataset.filter === value) ? value : "";
  for (const button of filters) button.setAttribute("aria-pressed", String(button.dataset.filter === selected));
  for (const group of groups) group.hidden = Boolean(selected) && group.dataset.track !== selected;
}
if (filters.length) {
  filterTopics();
  window.addEventListener("popstate", filterTopics);
  for (const button of filters) {
    button.addEventListener("click", () => {
      const url = new URL(location.href);
      if (button.dataset.filter) url.searchParams.set("track", button.dataset.filter);
      else url.searchParams.delete("track");
      url.hash = "";
      if (url.href !== location.href) history.pushState(null, "", url);
      filterTopics();
    });
  }
}

const mobileMenu = document.querySelector(".mobile-menu");
const sidebar = document.querySelector(".sidebar");
const scrim = document.querySelector(".scrim");
const workspace = document.querySelector(".workspace");
const smallScreen = matchMedia("(max-width: 760px)");
function setMenu(open, restoreFocus = true) {
  document.body.classList.toggle("menu-open", open);
  mobileMenu.setAttribute("aria-expanded", String(open));
  mobileMenu.setAttribute("aria-label", open ? "Close navigation" : "Open navigation");
  scrim.hidden = !open;
  workspace.inert = open;
  sidebar.inert = smallScreen.matches && !open;
  if (open) sidebar.querySelector("a").focus();
  else if (restoreFocus) mobileMenu.focus();
}
setMenu(false, false);
mobileMenu.addEventListener("click", () => setMenu(true));
scrim.addEventListener("click", () => setMenu(false));
smallScreen.addEventListener("change", () => setMenu(false, false));
document.addEventListener("keydown", event => {
  if (!document.body.classList.contains("menu-open")) return;
  if (event.key === "Escape") {
    event.preventDefault();
    setMenu(false);
    return;
  }
  if (event.key === "Tab") {
    const links = sidebar.querySelectorAll("a");
    const first = links[0];
    const last = links[links.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  }
});

document.querySelectorAll(".toc-mobile a").forEach(link => link.addEventListener("click", () => {
  const target = document.getElementById(decodeURIComponent(link.hash.slice(1)));
  if (!target) return;
  link.closest("details").open = false;
  target.tabIndex = -1;
  target.focus({preventScroll: true});
}));

const dialog = document.querySelector("#search-dialog");
const trigger = document.querySelector(".search-trigger");
const input = dialog.querySelector("input");
const scope = dialog.querySelector("select");
const output = dialog.querySelector(".search-output");
const cssBreak = /[\p{L}\p{N}]+/gu;
let searchData;
let searchSequence = 0;

function getSearchData() {
  if (!searchData) {
    searchData = fetch("/assets/search.json").then(response => {
      if (!response.ok) throw new Error("Search index unavailable");
      return response.json();
    }).then(documents => documents.map(document => ({
      ...document,
      titleLower: document.title.toLocaleLowerCase(),
      sections: document.sections.map(section => ({
        ...section, sectionLower: section.section.toLocaleLowerCase(), textLower: section.text.toLocaleLowerCase()
      }))
    }))).catch(error => {
      searchData = undefined;
      throw error;
    });
  }
  return searchData;
}

function showSearchMessage(message) {
  const paragraph = document.createElement("p");
  paragraph.textContent = message;
  output.replaceChildren(paragraph);
}

function findResults(documents, query, scopeValue) {
  const phrase = query.toLocaleLowerCase();
  const terms = [...new Set(phrase.match(cssBreak) ?? [])];
  if (!terms.length) return [];
  const results = [];
  for (const doc of documents) {
    const allowed = scopeValue === "library" ? doc.category !== "answers" : doc.category === scopeValue;
    if (!allowed) continue;
    const key = doc.key.toLocaleLowerCase();
    const exactId = phrase === key;
    const sourceId = /^r[0-9]{2}$/.test(phrase) && doc.url === "/reference/sources.html";
    const titleScore = (exactId ? 90 : 0) + (sourceId ? 80 : 0) + (doc.titleLower.includes(phrase) ? 35 : 0) + (doc.category === "modules" ? 4 : 0);
    let best;
    for (const section of doc.sections) {
      const headings = [key, doc.titleLower, section.sectionLower].join(" ");
      if (!terms.every(term => headings.includes(term) || section.textLower.includes(term))) continue;
      let score = titleScore + (section.sectionLower.includes(phrase) ? 17 : 0) + (section.textLower.includes(phrase) ? 8 : 0);
      score += terms.reduce((sum, term) => sum + (headings.includes(term) ? 5 : 1), 0);
      if (exactId && section.url === doc.url) score += 30;
      if (sourceId && section.section === "Registered sources") score += 30;
      if (doc.titleLower.includes(phrase) && section.url === doc.url) score += 6;
      if (!best || score > best.score) best = {doc, section, score, terms};
    }
    if (best) results.push(best);
  }
  return results.sort((a, b) => b.score - a.score || a.doc.title.localeCompare(b.doc.title)).slice(0, 14);
}

function snippet(text, lower, terms) {
  const first = terms.map(term => lower.indexOf(term)).filter(index => index >= 0);
  const anchor = first.length ? Math.min(...first) : 0;
  const left = Math.max(0, anchor - 50);
  const right = Math.min(text.length, left + 159);
  return (left ? "…" : "") + text.slice(left, right) + (right < text.length ? "…" : "");
}

function appendHighlighted(parent, text, terms) {
  const pattern = new RegExp("(" + terms.join("|") + ")", "giu");
  for (const [index, part] of text.split(pattern).entries()) {
    if (index % 2) {
      const mark = document.createElement("mark");
      mark.textContent = part;
      parent.append(mark);
    } else {
      parent.append(part);
    }
  }
}

function renderResults(results) {
  const list = document.createElement("ol");
  for (const {doc, section, terms} of results) {
    const item = document.createElement("li");
    const link = document.createElement("a");
    link.className = "search-result";
    link.href = section.url;
    const label = document.createElement("small");
    label.textContent = doc.category === "references" ? "Reference" : doc.key + (doc.category === "answers" ? " · Worked answers" : " · Lesson");
    const title = document.createElement("strong");
    appendHighlighted(title, doc.title, terms);
    link.append(label, title);
    if (section.url !== doc.url) {
      const heading = document.createElement("span");
      heading.className = "section-label";
      appendHighlighted(heading, section.section, terms);
      link.append(heading);
    }
    const paragraph = document.createElement("p");
    appendHighlighted(paragraph, snippet(section.text, section.textLower, terms), terms);
    link.append(paragraph);
    item.append(link);
    list.append(item);
  }
  output.replaceChildren(list);
  output.scrollTop = 0;
}

async function updateSearch() {
  const id = ++searchSequence;
  const query = input.value.trim();
  if (!query) {
    showSearchMessage("Try invariants, tail latency, or a source ID like R07.");
    return;
  }
  if (!searchData) showSearchMessage("Loading the search index…");
  try {
    const data = await getSearchData();
    if (id !== searchSequence) return;
    const results = findResults(data, query, scope.value);
    if (results.length) renderResults(results);
    else showSearchMessage("No results. Try a module ID, a shorter phrase, or a different search scope.");
  } catch {
    if (id === searchSequence) showSearchMessage("Search is temporarily unavailable. Type to retry, or use Browse topics.");
  }
}

function openSearch() {
  if (dialog.open) return;
  if (document.body.classList.contains("menu-open")) setMenu(false, false);
  dialog.showModal();
  input.focus();
  input.select();
  getSearchData().catch(() => {});
}
trigger.addEventListener("click", openSearch);
dialog.querySelector(".close-search").addEventListener("click", () => dialog.close());
dialog.addEventListener("click", event => {
  if (event.target === dialog) {
    const bounds = dialog.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) dialog.close();
  }
});
dialog.addEventListener("close", () => trigger.focus());
input.addEventListener("input", updateSearch);
scope.addEventListener("change", updateSearch);
dialog.addEventListener("keydown", event => {
  if (!["ArrowUp", "ArrowDown", "Enter"].includes(event.key)) return;
  if (document.activeElement === scope) return;
  const results = Array.from(output.querySelectorAll("a"));
  if (!results.length) return;
  const index = results.indexOf(document.activeElement);
  if (index === -1 && document.activeElement !== input) return;
  if (event.key === "Enter") {
    if (document.activeElement === input) {
      event.preventDefault();
      results[0].click();
    }
    return;
  }
  event.preventDefault();
  const next = event.key === "ArrowDown" ? Math.min(results.length - 1, index + 1) : index - 1;
  (results[next] ?? input).focus();
});
document.addEventListener("keydown", event => {
  if (event.key.toLowerCase() === "k" && (event.ctrlKey || event.metaKey)) {
    event.preventDefault();
    openSearch();
  }
});
