#!/usr/bin/env python3
"""Render the saved Markdown into a static, self-contained reading site."""
import html
import json
from pathlib import Path
import re
import shutil
import subprocess

from lxml import etree, html as dom

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
CONTENT = ROOT / "content"

TRACKS = {
    "F": {"name": "Foundations", "description": "Reason about correctness, uncertainty, and measurement.", "mark": "01"},
    "S": {"name": "Systems", "description": "Trace what happens under load, failure, and concurrency.", "mark": "02"},
    "A": {"name": "AI systems", "description": "Understand how models learn, retrieve, serve, and act.", "mark": "03"},
    "B": {"name": "Technology business", "description": "Connect customer evidence with cost and product choices.", "mark": "04"},
    "C": {"name": "Synthesis", "description": "Make and defend decisions across engineering and business.", "mark": "05"},
    "X": {"name": "Extensions", "description": "Deepen the foundation through new failure mechanisms and decisions.", "mark": "06"},
}
REFERENCES = {
    "SDE_EXTENSIONS": ("Extension roadmap", "New lessons, evidence checks, and the next useful questions.", "extensions"),
    "SDE_CONSOLIDATED_NOTES": ("Consolidated notes", "Cross-cutting principles and a reusable decision template.", "notes"),
    "SDE_REFERENCE_CARDS": ("Reference cards", "One compact recall prompt for each module.", "reference-cards"),
    "SDE_OPEN_QUESTIONS": ("Open questions", "Real inputs that the fictional cases leave unresolved.", "open-questions"),
    "SDE_SOURCES": ("Source register", "Primary links, exact passage checks, and verification limits.", "sources"),
    "SDE_INDEX": ("Execution index", "Artifact status, dependencies, revision history, and Library links.", "execution-index"),
    "SDE_Foundations_Library_v1": ("Original curriculum", "Module briefs, prerequisite bridges, and evidence requirements.", "curriculum"),
    "SDE_SOLUTIONS_INDEX": ("Solutions index", "Open a companion when you are ready to compare your work.", "solutions-index"),
    "SDE_START_HERE": ("Original study guide", "The saved guide, including study routes and the mastery ladder.", "study-guide"),
    "SDE_Foundations_Complete": ("Complete reading export", "The original consolidated learning notes.", "reading-export"),
    "SDE_Foundations_Solutions": ("Complete solutions export", "The original consolidated worked solutions.", "solutions-export"),
    "SDE_Foundations_Scheduled_Prompt": ("Production instructions", "The original instructions for producing and auditing learning packs.", "production-instructions"),
    "STUDY_PROGRESS": ("Original progress template", "The blank study template supplied with the vault.", "study-template"),
    "README": ("Vault readme", "Instructions for opening the original Obsidian vault.", "vault-readme"),
}
for letter in "ABCD":
    REFERENCES[f"SDE_Audit_{letter}"] = (f"Audit {letter}", "Verification results, repairs, and unresolved questions.", f"audit-{letter.lower()}")

ROUTES = [
    ("Define the decision", "Invariants, expected loss, and fair comparisons.", "F01 F02 F03"),
    ("Defend state changes", "Durable identity, concurrency, and replication.", "S02 S03 S04"),
    ("Defend operations", "Queues, overload, and authority boundaries.", "S05 S06"),
    ("Use AI with evidence", "Generalization, provenance, and bounded autonomy.", "A01 A03 A05"),
    ("Price the useful outcome", "Demand, unit economics, and product boundaries.", "B01 B02 B03"),
    ("Integrate judgment", "Work through decisions about effects, capacity, autonomy, and suppliers.", "C01 C03 C05 C06"),
]
TOPIC_ROUTES = [
    ("Cloud and distributed systems", "F01 S01 S02 S03 S04 S05 S06 C01 C03"),
    ("AI engineering and LLM judgment", "F02 F03 F04 A01 A02 A03 A04 A05 C02 C05 C06"),
    ("Technology and business decisions", "B01 F02 F03 B02 B03 C02 C04 C06"),
]
LEVELS = ["Unstarted", "Recognize", "Reproduce", "Transfer", "Defend"]

def esc(value):
    return html.escape(str(value), quote=True)

def simple(value):
    return " ".join(value.split())

def clean_text(node):
    copy = dom.fromstring(etree.tostring(node, method="html", encoding="unicode"))
    for annotation in copy.xpath(".//annotation"):
        annotation.drop_tree()
    return simple(copy.text_content())

def route_url(stem):
    match = re.fullmatch(r"SDE_([FSABCX]\d\d)(_answers)?", stem)
    if match:
        directory = "answers" if match[2] else "learn"
        return f"/{directory}/{match[1].lower()}.html"
    return f"/reference/{REFERENCES[stem][2]}.html"

def button(href, label, style="primary", extra=""):
    return f'<a class="button {style}" href="{href}" {extra}>{label}</a>'

def link_nav(section, page):
    active = 'active' if section == page else ''
    current = ' aria-current="page"' if active else ''
    return active, current

def shell(title, section, main, crumb="", body_class="", module=""):
    heading = {"home": "Overview", "paths": "Study paths", "topics": "Topics", "progress": "My progress", "reference": "Reference"}[section]
    primary = [
        ("home", "/", "Overview", "home"),
        ("paths", "/paths.html", "Study paths", "route"),
        ("topics", "/topics.html", "Browse topics", "grid"),
        ("extensions", "/reference/extensions.html", "Extensions", "books"),
        ("progress", "/progress.html", "My progress", "progress"),
    ]
    docs_nav = [
        ("reference", "/reference.html", "Reference", "books"),
        ("sources", "/reference/sources.html", "Source register", "source"),
    ]
    def nav_row(key, href, label, icon):
        active, current = link_nav(key, "sources" if crumb == "Source register" else "extensions" if crumb == "Extension roadmap" else section)
        return f'<a class="nav-link {active}" href="{href}"{current}><span class="ico {icon}" aria-hidden="true"></span>{label}</a>'
    study_nav = "".join(nav_row(*item) for item in primary)
    ref_nav = "".join(nav_row(*item) for item in docs_nav)
    sub_crumb = f'<span class="header-separator">/</span><span class="header-topic">{esc(crumb)}</span>' if crumb else ''
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#f7f7f1">
<title>{esc(title)}</title>
<link rel="icon" href="/assets/mark.png" type="image/png">
<link rel="stylesheet" href="/assets/site.css">
<script src="/assets/catalog.js" defer></script>
<script src="/assets/site.js" defer></script>
</head>
<body class="{body_class}" data-module="{module}">
<a class="skip" href="#main">Skip to content</a>
<button class="scrim" type="button" aria-label="Close navigation" hidden></button>
<aside class="sidebar" id="sidebar">
<a class="brand" href="/"><span class="brand-mark" aria-hidden="true"><i></i><i></i><i></i></span><span><strong>SDE Foundations</strong><small>Private learning library</small></span></a>
<nav aria-label="Main navigation">
<div class="sidebar-label">Learn</div>{study_nav}
<div class="sidebar-label reference-nav">Library</div>{ref_nav}
</nav>
<a class="side-progress" href="/progress.html">
<span class="side-progress-label"><span>Your study progress</span><strong data-side-count>0 / {len(modules)}</strong></span>
<span class="meter"><span data-meter></span></span>
<span class="side-progress-note">Modules with a recorded level</span>
</a>
</aside>
<div class="workspace">
<header class="topbar">
<div class="topbar-inner">
<button class="mobile-menu" type="button" aria-controls="sidebar" aria-expanded="false" aria-label="Open navigation"><span class="ico menu" aria-hidden="true"></span></button>
<a class="mobile-brand" href="/">SDE Foundations</a>
<div class="header-location"><span>{heading}</span>{sub_crumb}</div>
<button class="search-trigger" type="button" aria-haspopup="dialog"><span class="ico search" aria-hidden="true"></span><span>Search library</span><kbd>Ctrl K</kbd></button>
</div>
</header>
<main id="main" class="page" tabindex="-1">{main}</main>
<footer class="site-footer"><a href="/">SDE Foundations</a><a href="/reference/sources.html">Source register</a><a href="/reference/execution-index.html">Execution index</a></footer>
</div>
<dialog id="search-dialog" aria-labelledby="search-name">
<div class="search-head"><span class="ico search" aria-hidden="true"></span><label id="search-name" class="sr-only" for="search-input">Search library</label><input id="search-input" type="search" placeholder="Search titles, concepts, or source IDs…" autocomplete="off"><button type="button" class="close-search" aria-label="Close search">×</button></div>
<div class="search-filter"><label for="search-scope">Search in</label><select id="search-scope"><option value="library">Lessons and reference</option><option value="modules">Lessons only</option><option value="references">Reference and sources</option><option value="answers">Worked answers</option></select></div>
<div class="search-output" aria-live="polite"><p>Try <strong>invariants</strong>, <strong>tail latency</strong>, or a source ID like <strong>R07</strong>.</p></div>
</dialog>
</body>
</html>"""

def write(url, page):
    file = DIST / (url.lstrip("/") or "index.html")
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(page, encoding="utf-8")

def document(path):
    result = subprocess.run(
        ["pandoc", "-f", "markdown+tex_math_single_backslash+wikilinks_title_after_pipe+autolink_bare_uris-raw_html", "--mathml", "--wrap=none", "-t", "html5", str(path)],
        capture_output=True, text=True, check=True,
    )
    if result.stderr:
        raise ValueError(f"{path.name}: {result.stderr.strip()}")
    tree = dom.fragment_fromstring(result.stdout, create_parent="div")
    title = tree.find("h1")
    if title is None:
        raise ValueError(f"Missing document title: {path.name}")
    return tree, title

def read_meta(tree):
    return {clean_text(cells[0]): clean_text(cells[1])
            for row in tree.xpath("./table[1]/tbody/tr")
            if len(cells := row.findall("td")) == 2}

def module_links(text):
    return "".join(f'<a class="module-chip" href="{modules[key]["url"]}" data-chip="{key}">{key}</a>' for key in text.split())

def module_rows(ids):
    return "".join(
        f'<li><a class="module-row" href="{modules[key]["url"]}">'
        f'<span class="module-code">{key}</span><span class="module-name">{esc(modules[key]["title"])}</span>'
        f'<span class="module-state" data-module-state="{key}">Unstarted</span><span class="row-arrow" aria-hidden="true">›</span></a></li>'
        for key in ids
    )

def page_intro(label, title, description):
    return f'<div class="page-intro"><p class="eyebrow">{label}</p><h1>{title}</h1><p class="page-description">{description}</p></div>'

def ref_cards(stems):
    return "".join(
        f'<a class="ref-card" href="{route_url(stem)}"><span class="ico source" aria-hidden="true"></span>'
        f'<span><strong>{esc(REFERENCES[stem][0])}</strong><small>{esc(REFERENCES[stem][1])}</small></span><span aria-hidden="true">›</span></a>'
        for stem in stems
    )

def home_page():
    track_cards = "".join(
        f'<a class="topic-card track-{key}" href="/topics.html?track={key}#track-{key}"><span class="track-mark" aria-hidden="true"></span>'
        f'<span class="topic-meta">{sum(module["track"] == key for module in modules.values())} modules</span>'
        f'<strong>{track["name"]}</strong><span class="topic-description">{track["description"]}</span><span class="topic-arrow" aria-hidden="true">↗</span></a>'
        for key, track in TRACKS.items()
    )
    return f"""
<section class="hero">
<div class="hero-copy"><p class="eyebrow"><span class="hero-dot"></span> The learning library</p>
<h1>SDE Foundations<span>.</span></h1>
<p>Study the principles behind software systems, AI, and technology businesses. Work through the mechanisms, then use the evidence to defend a decision.</p>
<div class="hero-actions">{button("/learn/f01.html", "Start learning <span aria-hidden='true'>→</span>", extra='data-continue')}{button("/paths.html", "Explore study paths", "hero-secondary")}</div>
</div>
<div class="hero-graphic" aria-hidden="true"><div class="hero-grid"></div><div class="orbit orbit-one"></div><div class="orbit orbit-two"></div><div class="orbit orbit-three"></div><div class="orbit orbit-four"></div><div class="orbit orbit-five"></div><div class="orbit orbit-six"></div><div class="orbit orbit-seven"></div><div class="graphic-point"></div></div>
</section>
<div class="overview-facts"><span><strong>{len(modules)}</strong> modules</span><span><strong>{len(TRACKS)}</strong> topic areas</span><span><strong>{len(modules)}</strong> worked companions</span></div>
<section class="dashboard-section panel"><p class="eyebrow">New extension · X02</p><h2>When does a retry prevent recovery?</h2><p>Trace a recovering dependency and decide whether another attempt can finish before the deadline.</p><div class="hero-actions">{button('/learn/x02.html', 'Explore retry budgets')}{button('/reference/extensions.html', 'View extension roadmap', 'secondary')}</div></section>
<section class="dashboard-section"><div class="section-head"><div><p class="eyebrow">Choose a subject</p><h2>Browse by topic</h2></div><a class="text-link" href="/topics.html">All modules <span aria-hidden="true">→</span></a></div>
<div class="topic-grid">{track_cards}</div>
</section>
<div class="home-bottom dashboard-section">
<section class="panel start-panel"><p class="eyebrow">Recommended study path</p><h2>Build the decision first</h2><p>Start with invariants, base rates, and measurement. Attempt one exercise before opening its companion.</p>
<ul class="module-list compact">{module_rows(["F01", "F02", "F03"])}</ul>
<a class="text-link" href="/paths.html">See the full study path <span aria-hidden="true">→</span></a></section>
<section class="panel home-progress"><p class="eyebrow">Your progress</p><h2>Pick up where you left off</h2><p data-resume-message>Your last opened module will appear here.</p><div class="home-progress-count"><strong data-studied-count>0</strong><span>of {len(modules)} with a recorded level</span></div><span class="meter"><span data-meter></span></span>
<a class="text-link" href="/progress.html">View my progress <span aria-hidden="true">→</span></a></section>
</div>
<section class="dashboard-section"><div class="section-head"><div><h2>Keep close at hand</h2></div><a class="text-link" href="/reference.html">All reference material <span aria-hidden="true">→</span></a></div><div class="ref-grid">{ref_cards(["SDE_CONSOLIDATED_NOTES", "SDE_REFERENCE_CARDS", "SDE_SOURCES"])}</div></section>
"""

def paths_page():
    recommended = "".join(
        f'<li class="path-stage"><span class="stage-marker" aria-hidden="true"></span><div><h3>{title}</h3><p>{desc}</p><div class="module-chips">{module_links(sequence)}</div></div></li>'
        for title, desc, sequence in ROUTES
    )
    full = "".join(
        f'<li class="path-stage"><span class="stage-marker" aria-hidden="true"></span><div><h3>{track["name"]}</h3><div class="module-chips">{module_links(" ".join(key for key in modules if key.startswith(letter)))}</div></div></li>'
        for letter, track in TRACKS.items()
    )
    topical = "".join(f'<div class="panel path-topic"><h3>{title}</h3><div class="module-chips">{module_links(sequence)}</div></div>' for title, sequence in TOPIC_ROUTES)
    return page_intro("Curriculum", "Study paths", "Start with the high-ROI sequence or follow all modules in curriculum order.") + f"""
<div class="jump-links"><a href="#high-roi">High ROI first</a><a href="#full-curriculum">Full curriculum</a><a href="#topic-routes">Topic routes</a></div>
<div class="paths-grid"><section class="panel" id="high-roi"><h2>High ROI first</h2><p class="muted">The saved route for backend work, cloud systems, and judgment about AI.</p><ol class="path-list">{recommended}</ol></section>
<section class="panel" id="full-curriculum"><h2>Full curriculum and extensions</h2><p class="muted">The original 24 modules remain complete. Extensions add focused depth; check each lesson for its direct prerequisites.</p><ol class="path-list">{full}</ol></section></div>
<section class="dashboard-section" id="topic-routes"><h2>Topic routes</h2><div class="paths-grid">{topical}</div></section>
<section class="dashboard-section panel"><h2>A study session</h2><p>Use 45–60 minutes to name the decision, trace an example, attempt one exercise, compare your work, and write one transfer to a real problem.</p><p>Have 15 minutes? Read one section and write what it assumes, what it establishes, and where its conclusion stops.</p><a class="text-link" href="/reference/study-guide.html">Original study guide <span aria-hidden="true">→</span></a></section>"""

def topics_page():
    filters = '<button type="button" aria-pressed="true" data-filter="">All topics</button>' + "".join(
        f'<button type="button" aria-pressed="false" data-filter="{key}">{track["name"]}</button>' for key, track in TRACKS.items()
    )
    groups = "".join(
        f'<section class="topic-group track-{key}" id="track-{key}" data-track="{key}"><div class="group-heading"><span class="track-mark" aria-hidden="true"></span>'
        f'<div><h2>{track["name"]}</h2><p>{track["description"]}</p></div></div><ul class="module-list">{module_rows(m for m in modules if m.startswith(key))}</ul></section>'
        for key, track in TRACKS.items()
    )
    return page_intro("Curriculum", "Browse topics", "Find a module by subject and see your current study level.") + f'<div class="filters" role="group" aria-label="Filter topics">{filters}</div><div class="topic-groups">{groups}</div>'

def progress_page():
    ladder = [
        ("Recognize", "Explain the vocabulary."),
        ("Reproduce", "Rebuild a trace or calculation from memory."),
        ("Transfer", "Apply the idea elsewhere and state which assumptions change."),
        ("Defend", "Name a counterexample and evidence that could reverse your decision."),
    ]
    summaries = "".join(
        f'<div><strong data-{kind}-count>0</strong><span>{label}</span></div>'
        for kind, label in [("studied", "Recorded a level"), ("reproduce", "Reproduce or above"), ("defend", "At Defend")]
    )
    cards = "".join(
        f'<section class="topic-group track-{key}"><div class="group-heading"><span class="track-mark" aria-hidden="true"></span><div><h2>{track["name"]}</h2><p data-track-progress="{key}">0 with a recorded level</p></div></div><ul class="module-list">{module_rows(m for m in modules if m.startswith(key))}</ul></section>'
        for key, track in TRACKS.items()
    )
    levels = "".join(f"<div><dt>{name}</dt><dd>{desc}</dd></div>" for name, desc in ladder)
    return page_intro("Your learning", "My progress", "Set a study level in each module. Your levels and last opened module are saved in this browser.") + f"""
<div class="progress-summary panel">{summaries}</div><p class="storage-warning" data-storage-warning hidden>Browser storage is unavailable. Changes last until you leave this page.</p>
<section class="panel ladder"><h2>Mastery levels</h2><dl>{levels}</dl></section>
<div class="topic-groups">{cards}</div>"""

def reference_page():
    groups = [
        ("Study aids", ["SDE_EXTENSIONS", "SDE_CONSOLIDATED_NOTES", "SDE_REFERENCE_CARDS", "SDE_OPEN_QUESTIONS", "SDE_START_HERE"]),
        ("Evidence and curriculum", ["SDE_SOURCES", "SDE_INDEX", "SDE_Foundations_Library_v1", "SDE_Foundations_Scheduled_Prompt"]),
        ("Audit reports", [f"SDE_Audit_{letter}" for letter in "ABCD"]),
        ("Companions and exports", ["SDE_SOLUTIONS_INDEX", "SDE_Foundations_Complete", "SDE_Foundations_Solutions", "STUDY_PROGRESS", "README"]),
    ]
    intro = page_intro("Library", "Reference", "Revisit the source checks, use a recall aid, or open a saved export.")
    return intro + "".join(f'<section class="dashboard-section"><h2>{label}</h2><div class="ref-grid">{ref_cards(stems)}</div></section>' for label, stems in groups)

def diagram(original):
    source = esc(original.text_content())
    return dom.fragment_fromstring(f"""
<figure class="authority-diagram">
<figcaption>Allowed interfaces in the approval workflow</figcaption>
<div class="diagram-inputs"><div>Reviewer identity<small>Request</small></div><div>Proposal worker<small>Untrusted proposal</small></div><div>Policy and object metadata<small>Current facts</small></div></div>
<ol class="diagram-chain"><li><strong>Approval authority</strong><small>Atomic decision ↓</small></li><li><strong>Receipts and intents</strong><small>Committed intent ↓</small></li><li><strong>Payment dispatcher</strong><small>Stable payment identity ↓</small></li><li><strong>External provider</strong></li></ol>
<details><summary>Mermaid source</summary><pre><code>{source}</code></pre></details>
</figure>
""")

def decorate(tree, stem):
    for link in tree.xpath(".//a[@href]"):
        target = link.attrib["href"]
        name, separator, fragment = target.partition("#")
        if not name or name.startswith(("https://", "http://", "mailto:")):
            continue
        name = name.removesuffix(".md")
        if name not in docs:
            raise ValueError(f"{stem}: Unknown Markdown link {target}")
        link.attrib["href"] = route_url(name) + (separator + fragment)
        link.attrib.pop("title", None)
    for table in tree.xpath(".//table"):
        wrapper = dom.Element("div", {"class": "table-scroll", "tabindex": "0", "role": "region", "aria-label": "Scrollable table"})
        table.addprevious(wrapper)
        wrapper.append(table)
    for paragraph in tree.xpath(".//p[math[@display='block']]"):
        paragraph.attrib.update({"class": "math-scroll", "tabindex": "0", "role": "region", "aria-label": "Equation"})
    for pre in tree.xpath(".//pre"):
        if "mermaid" in pre.get("class", "").split():
            pre.getparent().replace(pre, diagram(pre))
            continue
        pre.attrib.update({"tabindex": "0", "aria-label": "Code example"})

def toc_for(tree, is_export):
    headings = tree.xpath("./h1[@id]" if is_export else "./h2[@id] | ./h3[@id]")
    return [(head.attrib["id"], clean_text(head), head.tag) for head in headings]

def section_index(tree, url, title, category, key, track):
    parts = []
    label = title
    target = url
    content = []
    level_tags = {"h1", "h2", "h3"}
    for child in tree:
        if child.tag in level_tags and child.get("id"):
            if content:
                parts.append({"url": target, "section": label, "text": simple(" ".join(content))})
            label = clean_text(child)
            target = url + "#" + child.attrib["id"]
            content = []
        else:
            content.append(clean_text(child))
    if content:
        parts.append({"url": target, "section": label, "text": simple(" ".join(content))})
    return {"url": url, "title": title, "category": category, "key": key, "track": track, "sections": parts}

def render_doc(stem, tree, first):
    key_match = re.fullmatch(r"SDE_([FSABCX]\d\d)(_answers)?", stem)
    key = key_match[1] if key_match else ""
    is_answer = bool(key_match and key_match[2])
    is_export = stem in {"SDE_Foundations_Complete", "SDE_Foundations_Solutions"}
    is_lesson = bool(key and not is_answer)
    url = route_url(stem)
    title = clean_text(first)
    doc_title = title.split(" — ", 1)[1] if key else title
    h1_id = first.attrib.get("id", "document-top")
    tree.remove(first)
    if key == "X01" and not is_answer:
        tree.insert(1, dom.fragment_fromstring('''<section class="cache-lab panel" aria-labelledby="cache-lab-title">
<h2 id="cache-lab-title">Explore the stale-fill race</h2>
<p>Compare the same events with and without a generation guard. Each step is atomic in this teaching model.</p>
<label for="cache-scenario">Scenario</label>
<select id="cache-scenario"><option value="race">Delayed fill after invalidation</option><option value="replica">Valid token, lagging replica</option><option value="reset">Guard metadata forgotten</option></select>
<div class="hero-actions"><button class="button secondary" type="button" data-cache-prev>Previous step</button><button class="button primary" type="button" data-cache-next>Next step</button><button class="button secondary" type="button" data-cache-reset>Restart trace</button></div>
<div data-cache-output aria-live="polite" aria-atomic="true"></div>
<noscript><p>The scripted explorer needs JavaScript. The complete trace and boundaries are explained in the lesson below.</p></noscript>
</section>'''))
    toc = toc_for(tree, is_export)
    decorate(tree, stem)
    label = (f'{TRACKS[key[0]]["name"]} <span aria-hidden="true">/</span> {key}' if is_lesson
             else f'{key} <span aria-hidden="true">/</span> Worked companion' if is_answer else "Reference")
    parent_href = f"/topics.html?track={key[0]}#track-{key[0]}" if is_lesson else modules[key]["url"] if is_answer else "/reference.html"
    parent_text = TRACKS[key[0]]["name"] if is_lesson else "Back to lesson" if is_answer else "Reference"
    evidence = next((f"#{anchor}" for anchor, name, _ in reversed(toc) if re.search(r"\b(evidence|source)\b", name, re.I)), "")
    practice = next((f"#{anchor}" for anchor, name, _ in toc if re.search(r"\b(practice|exercises?|analysis prompts|assignment|self-assessment)\b", name, re.I)), "")
    if is_lesson and not evidence:
        for table in tree.xpath(".//table[thead]"):
            if any(clean_text(header) == "Evidence" for header in table.xpath("./thead/tr/th")):
                table.getparent().set("id", "evidence-ledger")
                evidence = "#evidence-ledger"
                toc.append(("evidence-ledger", "Evidence ledger", "h2"))
                break
    toolbar = ""
    footer = ""
    if is_lesson:
        if not evidence or not practice:
            raise ValueError(f"Missing lesson jump: {key} ({evidence}, {practice})")
        prereqs = prereq_ids.get(key, [])
        register_jump = register_anchors.get(key, "")
        register_url = "/reference/extensions.html#extension-evidence-register" if key.startswith("X") else "/reference/sources.html" + register_jump
        prereq_links = f'<div class="prereq-line"><span>Related prerequisites</span><div class="module-chips">{module_links(" ".join(prereqs))}</div></div>' if prereqs else ""
        toolbar = f'''<p class="article-description">{esc(modules[key]["description"])}</p>{prereq_links}
<div class="article-actions">{button(practice, "Jump to practice")}{button(evidence, "Evidence", "secondary")}{button(route_url(stem+"_answers"), "Worked companion", "secondary")}<a class="text-link level-jump" href="#study-level-heading">Record level</a></div>'''
        options = "".join(f'<option value="{level}">{name}</option>' for level, name in enumerate(LEVELS))
        progress_box = f'''<section class="lesson-progress"><div><h2 id="study-level-heading">Your study level</h2><p data-level-note>Record what you can do after working through this module.</p><p class="storage-warning" data-storage-warning hidden>Browser storage is unavailable. This level lasts until you leave this page.</p></div><div><label class="sr-only" for="study-level">Study level</label><select id="study-level" data-level="{key}">{options}</select><a href="/progress.html">Mastery levels</a></div></section>'''
        sequence = list(modules)
        i = sequence.index(key)
        def neighbor(index, caption):
            if 0 <= index < len(sequence):
                neighbor_key = sequence[index]
                return f'<a href="{modules[neighbor_key]["url"]}"><small>{caption} · {neighbor_key}</small><strong>{esc(modules[neighbor_key]["title"])}</strong></a>'
            return ''
        footer = f'''<nav class="learning-links" aria-label="Lesson resources"><a href="{route_url(stem+"_answers")}">Open worked companion <span aria-hidden="true">→</span></a><a href="{register_url}">Source register <span aria-hidden="true">→</span></a></nav>
{progress_box}<nav class="lesson-neighbors" aria-label="Adjacent lessons">{neighbor(i-1, "Previous module")}{neighbor(i+1, "Next module")}</nav>'''
    elif is_answer:
        toolbar = f'<p class="article-description">Use the hints first, then compare your reasoning with the worked analysis and checks.</p>{button(modules[key]["url"], "Return to lesson", "secondary")}'
    if toc:
        nav_items = "".join(f'<li class="{tag}"><a href="#{esc(anchor)}">{esc(name)}</a></li>' for anchor, name, tag in toc)
        toc_list = f'<ol>{nav_items}</ol>'
        toc_elements = f'<details class="toc-mobile"><summary>On this page</summary><nav aria-label="On this page">{toc_list}</nav></details>'
        toc_side = f'<aside class="toc-side"><nav aria-label="On this page"><p>On this page</p>{toc_list}</nav></aside>'
    else:
        toc_elements = toc_side = ""
    page = f"""
<div class="reader-heading"><a class="back-link" href="{parent_href}"><span aria-hidden="true">←</span> {esc(parent_text)}</a><p class="eyebrow">{label}</p><h1 id="{esc(h1_id)}">{esc(doc_title)}</h1>{toolbar}</div>
<div class="reader-grid"><div class="reader-main">{toc_elements}<article class="prose">{''.join(etree.tostring(node, method="html", encoding="unicode") for node in tree)}</article>{footer}</div>{toc_side}</div>"""
    write(url, shell(f"{title} | SDE Foundations", "topics" if key else "reference", page, key or REFERENCES[stem][0], "reading-page", key if is_lesson else ""))
    if not is_export and stem not in {"STUDY_PROGRESS", "README"}:
        category = "answers" if is_answer else "modules" if is_lesson else "references"
        index.append(section_index(tree, url, doc_title, category, key, key[0] if key else ""))

if DIST.exists():
    shutil.rmtree(DIST)
shutil.copytree(ROOT / "assets", DIST / "assets")

docs = {}
for path in sorted(CONTENT.glob("*.md")):
    stem = path.stem
    route_url(stem)
    docs[stem] = document(path)

modules = {}
for letter in TRACKS:
    for stem, (tree, first) in docs.items():
        if not re.fullmatch(rf"SDE_{letter}\d\d", stem):
            continue
        key = stem.removeprefix("SDE_")
        title = clean_text(first).split(" — ", 1)[1]
        modules[key] = {"title": title, "url": route_url(stem), "track": letter, "description": read_meta(tree).get("Capability developed", "")}
if len([key for key in modules if not key.startswith('X')]) != 24 or any(f"SDE_{key}_answers" not in docs for key in modules):
    raise ValueError("Expected the original 24 modules and companions for every module")

prereq_ids = {}
execution = docs["SDE_INDEX"][0]
for entry in execution.xpath(".//tr[td]"):
    cells = entry.findall("td")
    key = clean_text(cells[0])
    if key in modules and len(cells) == 3:
        text = clean_text(cells[1])
        for start, end in re.findall(r"([FSABC]\d\d)[–-]([FSABC]\d\d)", text):
            expanded = " ".join(item for item in modules if start <= item <= end and item[0] == start[0])
            text = text.replace(f"{start}–{end}", expanded).replace(f"{start}-{end}", expanded)
        prereq_ids[key] = list(dict.fromkeys(re.findall(r"\b[FSABC]\d\d\b", text)))

prereq_ids["X01"] = ["F01", "S02", "S03"]
prereq_ids["X02"] = ["S05", "S06", "C03"]
register_anchors = {}
for heading in docs["SDE_SOURCES"][0].xpath("./h2[@id] | ./h3[@id]"):
    match = re.search(r"\b([FSABC]\d\d)\b", clean_text(heading))
    if match:
        register_anchors[match[1]] = "#" + heading.attrib["id"]

index = []
for stem, (tree, first) in docs.items():
    render_doc(stem, tree, first)

write("/", shell("SDE Foundations | Study library", "home", home_page(), body_class="overview-page"))
write("/paths.html", shell("Study paths | SDE Foundations", "paths", paths_page()))
write("/topics.html", shell("Browse topics | SDE Foundations", "topics", topics_page()))
write("/progress.html", shell("My progress | SDE Foundations", "progress", progress_page()))
write("/reference.html", shell("Reference | SDE Foundations", "reference", reference_page()))
write("/404.html", shell("Page not found | SDE Foundations", "home", page_intro("404", "Page not found", "Return to the overview or search the library.")))

(DIST / "assets/catalog.js").write_text(
    "window.sdeCatalog = " + json.dumps({"modules": modules, "levels": LEVELS}, ensure_ascii=False, separators=(",", ":")) + ";\n",
    encoding="utf-8",
)
(DIST / "assets/search.json").write_text(json.dumps(index, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
(DIST / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
print(f"Rendered {len(docs)} Markdown documents and indexed {sum(len(doc['sections']) for doc in index)} sections.")
