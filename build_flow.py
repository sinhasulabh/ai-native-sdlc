#!/usr/bin/env python3
"""Generate index.html (AI-Native SDLC: Target Flow Design). Usage: python3 build_flow.py"""
import html, re
from pathlib import Path

root = Path(__file__).parent
e = html.escape


def rt(s):
    """Inline markup: **bold** and [text](url)."""
    s = e(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)",
               r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    return s


def p(s): return f"<p>{rt(s)}</p>"
def ul(items): return "<ul>" + "".join(f"<li>{rt(i)}</li>" for i in items) + "</ul>"
def ol(items): return "<ol>" + "".join(f"<li>{rt(i)}</li>" for i in items) + "</ol>"


def table(head, rows):
    th = "".join(f"<th scope='col'>{rt(h)}</th>" for h in head)
    body = "".join("<tr>" + "".join(f"<td>{rt(c)}</td>" for c in r) + "</tr>" for r in rows)
    return f"<div class='tbl'><table><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>"


# ---------- diagrams ----------
W, H = 156, 72


def box(cx, cy, human, name, l1, l2):
    cls = "bx h" if human else "bx"
    return (f"<rect class='{cls}' x='{cx - W // 2}' y='{cy - H // 2}' width='{W}' height='{H}' rx='8'/>"
            f"<text class='nm' x='{cx}' y='{cy - 12}'>{e(name)}</text>"
            f"<text class='bd' x='{cx}' y='{cy + 4}'>{e(l1)}</text>"
            f"<text class='bd' x='{cx}' y='{cy + 20}'>{e(l2)}</text>")


def flow_svg():
    c1, c2, c3, c4, r1, r2, r3 = 122, 300, 478, 656, 124, 256, 388
    h = W // 2
    paths = [
        f"M{c1 + h} {r1}H{c2 - h}", f"M{c2 + h} {r1}H{c3 - h}", f"M{c3 + h} {r1}H{c4 - h}",
        f"M{c4} {r1 + H // 2}V{r2 - H // 2}",
        f"M{c4 - h} {r2}H{c3 + h}", f"M{c3 - h} {r2}H{c2 + h}", f"M{c2 - h} {r2}H{c1 + h}",
        f"M{c1} {r2 + H // 2}V{r3 - H // 2}", f"M{c1 + h} {r3}H{c2 - h}",
        f"M{c2} {r3 + H // 2}V446H24V{r1}H{c1 - h}",
    ]
    arrows = "".join(f"<path d='{d}' marker-end='url(#fa)'/>" for d in paths)
    tie = f"<path d='M{c2} {r2 + H // 2}V306'/>"
    return f"""<svg viewBox='0 0 760 504' role='img' aria-labelledby='t1'>
<title id='t1'>Six human gates decide; AI and automation do the rest</title>
<defs><marker id='fa' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' markerHeight='6' orient='auto-start-reverse'><path d='M0 0L10 5L0 10z' class='mk'/></marker></defs>
<text class='ttl' x='24' y='28'>Six human gates decide; AI and automation do the rest</text>
<rect class='gov' x='8' y='44' width='744' height='436' rx='8'/>
<text class='q l' x='24' y='66'>Gate 6 · Governance sets the formula, autonomy per category and guardrail thresholds for every stage</text>
<g class='ln'>{arrows}{tie}</g>
{box(c1, r1, False, 'Intake', 'AI drafts and', 'ranks intents')}
{box(c2, r1, True, 'Gate 1', 'Which intents', 'go ahead')}
{box(c3, r1, True, 'Gate 2', 'Approve spec and', 'functional tests')}
{box(c4, r1, False, 'Build', 'Hooks in the loop,', 'same checks in CI')}
{box(c4, r2, True, 'Gate 3', 'PR review with', 'gate report')}
{box(c3, r2, False, 'Deploy', 'Behind a flag,', 'off by default')}
{box(c2, r2, False, 'Staged ramp', 'Pauses on a', 'guardrail breach')}
{box(c1, r2, True, 'Gate 4', 'Roll back, hold', 'or continue')}
<rect class='bx h' x='195' y='306' width='210' height='28' rx='14'/>
<text class='nm s' x='{c2}' y='324'>Gate 5: irreversible step</text>
{box(c1, r3, False, 'Close', 'Metric verified', 'in production')}
{box(c2, r3, False, 'Learn', 'Intent record and', 'flag removal')}
<rect class='bx h' x='420' y='366' width='14' height='14' rx='3'/><text class='bd l' x='442' y='377'>Human gate</text>
<rect class='bx' x='420' y='392' width='14' height='14' rx='3'/><text class='bd l' x='442' y='403'>AI or automation</text>
<text class='q l' x='44' y='462'>Outcome and lessons return to intake</text>
</svg>"""


def states_svg():
    c1, c2, c3, c4, r1, r2 = 122, 300, 478, 656, 190, 312
    h = W // 2
    paths = [
        f"M{c1 + h} {r1}H{c2 - h}", f"M{c2 + h} {r1}H{c3 - h}", f"M{c3 + h} {r1}H{c4 - h}",
        f"M{c2} {r1 - H // 2}V108", f"M{c3} {r1 - H // 2}V108", f"M{c4} {r1 - H // 2}V108",
        f"M222 80H{c1}V{r1 - H // 2}",
        f"M{c4} {r1 + H // 2}V{r2 - H // 2}", f"M{c4 - h} {r2}H{c3 + h}",
    ]
    arrows = "".join(f"<path d='{d}' marker-end='url(#fb)'/>" for d in paths)
    return f"""<svg viewBox='0 0 760 372' role='img' aria-labelledby='t2'>
<title id='t2'>A guardrail breach rolls a live flag back; success ends in removal</title>
<defs><marker id='fb' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' markerHeight='6' orient='auto-start-reverse'><path d='M0 0L10 5L0 10z' class='mk'/></marker></defs>
<text class='ttl' x='24' y='28'>A guardrail breach rolls a live flag back; success ends in removal</text>
<g class='ln'>{arrows}</g>
<rect class='bx h' x='222' y='52' width='512' height='56' rx='8'/>
<text class='nm' x='478' y='76'>Rolled back</text>
<text class='bd' x='478' y='92'>A human decides after a guardrail breach; the AI turns the flag off</text>
<text class='q l' x='132' y='136'>fix, then re-ramp</text>
{box(c1, r1, False, 'Dark', 'Deployed, nobody', 'sees it')}
{box(c2, r1, False, 'Targeted', 'On for chosen', 'groups only')}
{box(c3, r1, False, 'Ramping', 'On for a rising', 'share of traffic')}
{box(c4, r1, False, 'Fully on', 'Everyone, under', 'observation')}
{box(c4, r2, False, 'Cleanup-ready', 'Intent verified;', 'flag not needed')}
{box(c3, r2, False, 'Removed', 'Flag and dead path', 'deleted by a change')}
</svg>"""


def fig(svg, caption):
    return f"<figure class='fig'><div class='figin'>{svg}</div><figcaption>{rt(caption)}</figcaption></figure>"


# ---------- content ----------
S = []


def sec(i, title, *parts):
    S.append(f"<section id='{i}'><h2>{e(title)}</h2>" + "".join(parts) + "</section>")


sec("purpose", "Purpose and scope",
    p("This document defines a target flow for AI-native software delivery: how work moves from a user signal to verified value in production when AI does the building and humans hold the decisions."),
    p("The flow was designed from first principles, without the constraints of today's process (sprints, ticket types, role titles). It is an attempt to reinvent the SDLC flow for an AI-native world, rather than to adapt today's process."),
    p("It is a design model, not a tool selection, an adoption plan or a replacement for an organisation's risk and compliance policy. Where the design deliberately leaves a choice to teams, the document says so and lists it under open points. Overlaying a specific organisation's real-world constraints on this flow is a separate, later step."))

sec("principles", "Design principles",
    p("Six principles shape every choice in the flow."),
    ol(["**North star: time from user signal to verified value in production, with quality held constant.** A shortcut that trades correctness for speed does not count.",
        "**The unit of work is an intent**: an outcome plus how it will be verified. Stories describe activity; intents describe outcomes, so what enters the flow already carries its own verification.",
        "**AI suggests, humans decide.** AI collects signals, drafts intents, builds, checks and recommends. Humans decide at defined gates.",
        "**Autonomy is earned per category of intent.** Every category starts with full human review. Agreement between AI and human, and delivered outcomes, decide when a category gets more autonomy.",
        "**Deploying is separate from releasing.** Every change that can be flagged ships behind a flag, off by default, so it can be reversed without a redeploy.",
        "**Every closed intent teaches the system.** Each one writes a structured record that feeds autonomy decisions and turns missed issues into new rules and tests."]))

sec("flow", "The target flow at a glance",
    p("Humans hold six gates; everything between them is AI or automation."),
    fig(flow_svg(), "Target flow: 10 steps, 6 human gates."),
    p("Gate 4 applies only when a guardrail is breached, and Gate 5 only to irreversible data-migration steps. Closing an intent returns outcomes and lessons to intake, which is what lets each category earn more autonomy over time."))

sec("intake", "Intake and prioritisation",
    p("AI drafts and ranks candidate intents, and a human decides which go ahead. The ranking formula is the team's choice, applied to a fixed set of inputs."),
    p("Signals (user feedback, telemetry, support tickets, incidents) are collected continuously. AI clusters them and drafts candidate intents, each with an outcome and a verification. Gate 1 is the human decision on which intents proceed."),
    p("**Fixed inputs.** Every intent carries the same five inputs, whatever formula the team uses."),
    table(["Input", "Meaning", "Example"], [
        ["Value", "Reach and impact", "40,000 users per month, +5% conversion"],
        ["Confidence", "How sure the estimate is", "70%"],
        ["Risk", "Blast radius if it goes wrong", "Medium (touches checkout)"],
        ["Cost", "Human review hours, not build time", "3 review-hours"],
        ["Urgency", "How fast the value decays", "None"]]),
    p("Cost means review load because AI makes build effort much smaller, though not uniform: complex changes still cost more iterations, compute and verification. The scarce resource is human attention."),
    p("**Configurable formula.** Teams choose the prioritisation framework that suits them. Common options include RICE, ICE and WSJF, as well as MoSCoW, the Kano model, value-versus-effort matrices and weighted scoring, or a custom formula over the same fixed inputs. WSJF is the suggested default. The inputs, score and rationale are stored with every intent so the ranking can be compared with the human's decision later."))

sec("build", "Build and verification",
    p("Nothing is built until a human has approved the spec and its verification plan, and nothing merges until the same checks have run twice: in the agent loop and in CI."),
    ol(["**Gate 2, the spec gate.** A human approves the spec and the verification plan: functional tests derived from the spec, the rollout plan and the guardrail thresholds. The approved tests are the contract. The builder does not write its own tests after the fact, because the same misunderstanding could then sit in both the code and the tests.",
        "**Hooks in the agent loop.** Deterministic checks run at lifecycle points (tests, types, security, policy) and block the agent early.",
        "**The same checks in CI.** They run again on the finished code, so a misconfigured or bypassed hook cannot let a change through. Hooks give early feedback; CI gives the guarantee.",
        "**A scope-drift gate.** It flags changes outside the files and behaviour the spec names, such as an unrequested edit.",
        "**Flag combination tests.** Flags in the same area can interact, so their combinations need testing, and the number of combinations grows as 2^N. How much to test, and how many child flags a master flag carries, is left to teams.",
        "**Gate 3, human PR review.** The reviewer receives a report: gate results, the scope check, a mapping from the change to the spec, and an AI first-pass summary. Every PR goes to a human for now."]),
    p("Code conflicts between intents are resolved before merge, by rebasing and re-verifying. A merge that is clean as text can still break behaviour, which is why the combination tests matter. The gates check rules and the approved tests; the human review covers what they cannot, such as UX feel and maintainability."))

sec("release", "Release and rollback",
    p("Every change that can be flagged ships behind a flag, off by default, and a human decides whether to roll back."),
    ul(["**A flag on every flaggable change,** including changes with no functional impact. Performance, memory and dependency effects can still break production, and one uniform rule keeps the flow simple.",
        "**Staged, rule-based ramp.** The rollout plan sits in the approved spec, for example internal users, then 1%, 10%, 50% and 100%. Automation advances a step only while the guardrail metrics hold.",
        "**On a guardrail breach the AI pauses the ramp,** then recommends turning the flag off, holding or continuing, with the evidence. A human decides (Gate 4) and the AI executes. If nobody responds, the ramp stays paused and the alert escalates. Turning a flag off reverts code paths, not data: anything the new path wrote, and sessions already in progress, survive it.",
        "**Concurrent intents in one area** ship under one master flag with independent child flags, to the same cohort. Any child can be turned off without affecting the others. Teams plan the combination testing, and each intent records its attribution method.",
        "**Changes that cannot be flagged** get a named alternative. Data migrations run in canary cycles using expand-contract, which keeps the schema reversible until the final step that drops old data; that step needs a human (Gate 5). Dual-write and backfill steps can still damage data before then, so each canary cycle verifies the data, not only the code. Security fixes ship immediately to everyone, with rollback kept and the same gates run at urgent priority. Rolling one back reopens the vulnerability, so the Gate 4 decision for a security fix includes someone accountable for security. Dependency and runtime upgrades go through a canary rollout."]),
    fig(states_svg(), "Flag states: 7 states, 1 human decision."),
    p("Permanent flags, such as kill switches and entitlements, are typed as permanent and stay in the fully-on state. Only temporary release flags reach cleanup."))

sec("loop", "Closing the loop and learning",
    p("An intent is done only when its outcome metric is verified in production, and every closed intent leaves a record the system learns from."),
    ul(["**Closing rule.** The metric named in the intent must move as promised over the verification window. If it does not, the result returns to intake as new signal.",
        "**Attribution method, recorded per intent.** Split the cohort so each change has its own group, or stagger the releases. Either can add a holdout group (5 to 10%) that gets none of the changes. Teams choose. Staggering compares before and after, so seasonality can distort the result.",
        "**A structured record per closed intent:** the AI's recommendation, the human's choice and the reason when they differ, the outcome against the promised value, and lessons.",
        "**Two measures per category of intent.** Agreement: how often the human accepted the AI's recommendation. Outcome: whether approved intents delivered the value they promised. Agreement alone can mislead if reviewers rubber-stamp, so a category gains autonomy only when both hold. Outcome data also calibrates the AI's value estimates.",
        "**Misses become rules.** When a gate missed something or a human caught it, the case becomes a new rule or test.",
        "**Automated flag removal.** Closing the intent triggers a flag-removal change that passes the same gates. Temporary release flags are removed. Permanent flags (kill switches, entitlements) are typed as such and stay. A flag that ended permanently off has its new code path removed instead."]))

sec("gates", "Human gates",
    p("Humans decide at six gates, and a gate is a decision point, not a role: whoever is eligible can pass it. Each gate is defined by four fields, so a team can configure it without inventing new roles. Anyone may decide, but every gate names who is accountable for the outcome."),
    table(["Gate", "Decision", "Evidence shown", "Who is eligible", "If nobody responds"], [
        ["1. Intake", "Which intents go ahead", "Ranked candidate intents with inputs, score and rationale", "Team defines", "Intent waits; escalates"],
        ["2. Spec", "Is the spec and verification plan right", "Spec, functional tests, rollout plan, guardrail thresholds", "Team defines", "Build does not start; escalates"],
        ["3. PR review", "Is the change good to merge", "PR report: gate results, scope check, spec mapping, AI summary", "Anyone qualified to review the area", "PR waits; escalates"],
        ["4. Rollback", "Roll back, hold or continue", "Breached guardrail, AI recommendation, metrics before and after", "Anyone with production access on the rotation", "Ramp stays paused; alert escalates"],
        ["5. Irreversible migration step", "Approve the final step, such as dropping old data", "Migration results from every canary cycle", "Someone who owns the data", "Step does not run; escalates"],
        ["6. Governance", "Set the prioritisation formula, autonomy level per category and guardrail thresholds", "Agreement and outcome measures per category", "Team defines", "Current settings stay in force"]]),
    p("Decided so far: the four fields, and Gate 4's rule that the ramp stays paused when nobody responds. The other eligibility and no-response entries are proposals for teams to confirm. The escalation chain (who is alerted first, how long before the next person, who is the final owner) is left for each team to define."))

sec("sources", "Sources",
    ul(["[Anthropic, The AI-native SDLC playbook](https://claude.com/resources/articles/the-ai-native-sdlc-playbook)",
        "[AWS, AI-Driven Development Life Cycle](https://aws.amazon.com/blogs/devops/ai-driven-development-life-cycle/)",
        "[Atlassian, AI SDLC transformation playbook](https://www.atlassian.com/blog/ai-at-work/ai-sdlc-transformation-playbook)",
        "[OpenAI, Building an AI-native engineering team](https://cdn.openai.com/business-guides-and-resources/building-an-ai-native-engineering-team.pdf)",
        "[Microsoft, HVE Core](https://github.com/microsoft/hve-core)",
        "[GitHub, Introducing Agent HQ](https://github.blog/news-insights/company-news/welcome-home-agents/)",
        "[Google, The New SDLC With Vibe Coding (Day 1 whitepaper)](https://www.kaggle.com/whitepaper-the-new-SDLC-with-vibe-coding)",
        "[Google, Day 5 podcast (summary page)](https://videohighlight.com/v/VSRdL4wlbLY)"]))

TOC = [("purpose", "Purpose"), ("principles", "Principles"), ("flow", "The flow"), ("intake", "Intake"),
       ("build", "Build"), ("release", "Release"), ("loop", "Learning"), ("gates", "Gates"),
       ("sources", "Sources")]
toc = "".join(f"<a href='#{i}'>{e(t)}</a>" for i, t in TOC)

CSS = """
:root{--bg:#fbfaf7;--fg:#1d1d1b;--muted:#5f5e5a;--line:#dcd9d0;--card:#fff;--accent:#8a3b12;
--hum:#dbe7f5;--hum-b:#2f5fa8;--edge:#8c8a82;--tint:#f1efe9}
@media (prefers-color-scheme:dark){:root{--bg:#161614;--fg:#ecebe6;--muted:#a3a198;--line:#34332f;--card:#1e1e1c;--accent:#e08a5a;
--hum:#1f2a3d;--hum-b:#8fa8e0;--edge:#8a8880;--tint:#1b1b19}}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.wrap{max-width:860px;margin:0 auto;padding:32px 16px 64px}
h1{font:700 clamp(1.6rem,4vw,2.3rem)/1.15 Georgia,"Times New Roman",serif;margin:0 0 8px;letter-spacing:-.01em}
h2{font:700 1.3rem/1.3 Georgia,serif;margin:44px 0 12px;padding-top:8px;border-top:1px solid var(--line)}
.sub{color:var(--muted);margin:0 0 16px;max-width:70ch}.meta{font-size:.85rem;color:var(--muted);margin-bottom:16px}
.xlink{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--accent);padding:10px 14px;border-radius:6px;font-size:.92rem;margin:0 0 20px}
nav.toc{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:.88rem;margin:0 0 8px}
a{color:var(--accent);text-underline-offset:2px}a:focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:2px}
p{margin:0 0 12px}ul,ol{margin:0 0 14px;padding-left:22px}li{margin-bottom:8px}
.tbl{overflow-x:auto;border:1px solid var(--line);border-radius:8px;background:var(--card);margin:0 0 16px}
table{border-collapse:collapse;width:100%;min-width:520px;font-size:.9rem}
th,td{padding:10px 12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line)}
thead th{background:var(--tint);font-weight:600}tbody tr:last-child td{border-bottom:0}
.fig{margin:16px 0}.figin{overflow-x:auto;border:1px solid var(--line);border-radius:8px;background:var(--card)}
.figin svg{display:block;width:100%;min-width:640px;height:auto}
figcaption{font-size:.82rem;color:var(--muted);margin-top:6px}
svg text{fill:var(--fg);text-anchor:middle;font-family:inherit}
svg .ttl{font-size:15px;font-weight:600;text-anchor:start}
svg .nm{font-size:13px;font-weight:600}svg .nm.s{font-size:11.5px}
svg .bd{font-size:11.5px}svg .q{font-size:11.5px;fill:var(--muted)}svg .l{text-anchor:start}
svg .bx{fill:none;stroke:var(--edge);stroke-width:1.25}
svg .bx.h{fill:var(--hum);stroke:var(--hum-b);stroke-width:2}
svg .gov{fill:var(--tint);stroke:var(--line)}
svg .ln{fill:none;stroke:var(--edge);stroke-width:1.25}svg .mk{fill:var(--edge)}
footer{margin-top:48px;color:var(--muted);font-size:.82rem;border-top:1px solid var(--line);padding-top:16px}
@media print{section{break-inside:avoid-page}}
"""

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI-Native SDLC: Target Flow Design</title>
<meta name="description" content="A target flow for AI-native software delivery, from user signal to verified value, with six human gates. Designed from first principles.">
<style>{CSS}</style>
</head>
<body>
<main class="wrap">
<h1>AI-Native SDLC: Target Flow Design</h1>
<p class="sub">How work moves from a user signal to verified value in production when AI does the building and humans hold the decisions.</p>
<p class="meta">Last updated 2026-10-25 &middot; Design model, not an adoption plan</p>
<p class="xlink">See also <a href="comparison.html">the vendor comparison</a>, which compares seven vendors' AI-native SDLC frameworks.</p>
<nav class="toc" aria-label="Sections">{toc}</nav>
{"".join(S)}
<footer>Personal project; views are the author's own and do not represent any employer or client. Based on public sources only. See also the <a href="comparison.html">vendor comparison</a>.</footer>
</main>
</body>
</html>
"""
(root / "index.html").write_text(page)
print("wrote index.html", len(page), "bytes")
