# Workspace setup playbook (Cursor + Notion MCP + AGENTS)

Copy this file into any new repo and follow it end-to-end. It documents the Investory / Personal-Quant setup so you can reproduce the same workflow elsewhere.

**Stack of tools**

| Tool | Job |
|------|-----|
| **Notion** | Product docs: overview, PRD, architecture, ADRs, research, weekly notes |
| **Git** | Code: branch → commit → push (optional PRs). No project board required |
| **Cursor** | Implementation: `AGENTS.md`, `.cursor/rules/*.mdc`, Notion MCP |

Rule: **why/what** → Notion. **how in code** → git + Cursor. Do not duplicate a task board in Notion.

---

## 0. Prerequisites

- A git repo (local + remote optional)
- Cursor installed
- A Notion workspace you can edit (member, not guest)
- Basic app folders ready or planned (`backend/`, `frontend/`, etc.)

---

## 1. Repo skeleton (docs + agent guidance)

Create these at the **repo root** (adapt names to your product):

```text
YourRepo/
  AGENTS.md                 # always-on operating guide for humans + AI
  README.md                 # how to run the app
  .gitignore                # include .env, node_modules, .venv, .next, etc.
  .cursor/
    rules/
      project.mdc           # alwaysApply: true — product scope + Notion URL
      backend.mdc           # optional; globs for backend files
      frontend.mdc          # optional; globs for frontend files
    mcp.json                # Notion MCP config
  docs/
    SOURCE_OF_TRUTH.md      # which tool owns what
    REPO_STRUCTURE.md       # intended folder layout
    notion/                 # paste kits for Notion pages (optional but useful)
      SETUP.md
      00_OVERVIEW.md
      01_PRD.md
      02_ARCHITECTURE.md
      03_ADRS.md
      04_RESEARCH.md
      05_WEEKLY_NOTES.md
      06_GLOSSARY.md
    WORKSPACE_SETUP_PLAYBOOK.md   # this file
  backend/                  # your API
  frontend/                 # your UI
```

### What belongs in `AGENTS.md`

Keep it short and actionable:

- Product name + one-sentence purpose
- **Non-goals** (what agents must never build)
- Stack table
- Repo map
- Source-of-truth table (Notion vs git)
- **Canonical Notion parent page URL**
- Backend/frontend conventions that matter every session
- Git workflow (branch / commit / push)
- Definition of Done + security (never commit `.env`)

### What belongs in `.cursor/rules/project.mdc`

```markdown
---
description: <Product> scope, stack, and documentation ownership
alwaysApply: true
---

# <Product> — project rules

## Product
- …
- Non-goals: …

## Stack
- …

## Notion scope (required)
- Product docs live **only** under: <PASTE_PARENT_PAGE_URL>
- When using Notion MCP, search/read under that page only
- Do not use other Notion pages/workspaces for this repo

## Agent behavior
- Implement from Notion PRD/ADR scope; do not invent requirements
- Prefer Notion MCP over guessing product decisions
- Never commit secrets
- Prefer small commits on a feature branch
```

Add file-scoped rules (`backend.mdc`, `frontend.mdc`) with `globs:` when conventions differ by layer.

**Tip:** Keep editable copies under `docs/cursor-rules/*.md` and sync into `.cursor/rules/*.mdc` when you change them.

---

## 2. Notion workspace

### 2.1 Create the page tree

1. Create a **parent page** named after the product (example: `Investory`).
2. Create child pages (names can vary):

| Child page | Purpose |
|------------|---------|
| Overview | Problem, solution, non-goals, six-week/goal summary |
| PRD | Goals, epics, acceptance criteria |
| Architecture | Stack diagram, data model, request flows |
| ADRs | Short decisions: Context → Decision → Consequences |
| Research | Vendor/API/prompt experiments |
| Weekly notes | Progress log (lightweight tracker instead of Jira/Projects) |
| Glossary | Domain terms (optional) |

3. Nest every child **under** the parent (drag in the sidebar). Flat sibling pages outside the parent are easy to miss in MCP.

### 2.2 Copy content from repo (optional)

If you keep paste kits in `docs/notion/`, paste each file body into the matching Notion page once. After that, **Notion is the source of truth** — update Notion for product decisions; keep repo paste kits as templates for the next project.

### 2.3 Get the parent page URL

1. Open the **parent** page (not a child).
2. Copy link (`⋯` → Copy link, or address bar in browser).
3. Paste that URL into:
   - `AGENTS.md`
   - `.cursor/rules/project.mdc`
   - `docs/SOURCE_OF_TRUTH.md`

Example shape:

`https://app.notion.com/p/YourProduct-<id>`

---

## 3. Wire Notion MCP in Cursor

### 3.1 Project config

Create `.cursor/mcp.json` in the repo:

```json
{
  "mcpServers": {
    "notion": {
      "url": "https://mcp.notion.com/mcp"
    }
  }
}
```

This uses Notion’s **hosted OAuth MCP** (no internal integration token required for personal setups).

For all projects, you can instead put the same block in `~/.cursor/mcp.json` (Windows: `C:\Users\<you>\.cursor\mcp.json`).

### 3.2 Authenticate

1. Reload Cursor / open **Settings → MCP**.
2. Enable **notion**.
3. Complete the browser **OAuth** login with the Notion account that owns the docs.
4. Pick the correct Notion **workspace** if prompted.

### 3.3 Scope behavior (important)

OAuth MCP can see many pages you can access. It does **not** auto-lock to one parent.

**Scoping is done by you via:**

1. Parent URL pinned in `AGENTS.md` + `project.mdc`
2. Prompts that name the product/doc (“Investory PRD”, not “my Notion”)
3. Nesting all project docs under that one parent

You usually do **not** paste the URL in every chat once rules are pinned.

### 3.4 Smoke test

In Cursor chat (in that repo):

> List child pages under the \<Product\> Notion parent and summarize PRD goals.

Expect: correct children + PRD goals from Notion (not from stale local markdown alone).

---

## 4. Day-to-day usage

### Prompting agents

| Situation | What to say |
|-----------|-------------|
| Start a feature | “Implement Week 1 foundation from the Notion PRD / Architecture.” |
| Ambiguous scope | “Check Notion PRD first; don’t invent requirements.” |
| Architecture decision | “Add ADR-00N to Notion ADRs for \<decision\>.” |
| Pure bugfix | No Notion mention needed |
| Wrong workspace fear | “Use Notion MCP — \<Product\> parent only.” |

### Weekly rhythm

1. Update **Weekly notes** in Notion (plan / shipped / blocked).
2. Branch: `feat/short-name` from `Main`.
3. Implement in Cursor with MCP + rules.
4. Commit + push (PR optional).
5. Log shipped work in Weekly notes; write an ADR if a decision changed.

### Definition of Done (lightweight)

- Matches Notion acceptance criteria for that slice
- Committed (and pushed)
- No secrets in git
- README updated if run steps changed
- ADR updated when architecture changed

---

## 5. Checklist for a brand-new project

Copy this checklist into the new repo’s first PR / note:

- [ ] `AGENTS.md` written (product, non-goals, stack, Notion URL)
- [ ] `.cursor/rules/project.mdc` with `alwaysApply: true` + Notion parent URL
- [ ] Optional `backend.mdc` / `frontend.mdc` with globs
- [ ] `docs/SOURCE_OF_TRUTH.md` (tool ownership)
- [ ] Notion parent + child pages created and nested
- [ ] Parent page URL pinned in AGENTS + rules
- [ ] `.cursor/mcp.json` with Notion MCP URL
- [ ] OAuth completed in Cursor Settings → MCP
- [ ] Smoke test: list children + summarize PRD goals
- [ ] First feature branch started from Notion Week / epic scope

---

## 6. What we intentionally skipped (and why)

| Skipped | Why |
|---------|-----|
| Jira / Linear | Overhead for solo / small class projects |
| GitHub Projects Kanban | Optional; weekly notes + git history are enough |
| Duplicating full PRD only in git | Notion owns product narrative; repo keeps runbooks + agent rules |
| Sharing every Notion page via old “internal integration” | Hosted Notion MCP uses OAuth instead |

---

## 7. Troubleshooting

| Problem | Fix |
|---------|-----|
| MCP not listed / not connecting | Check `.cursor/mcp.json`, reload Cursor, re-auth under Settings → MCP |
| Agent reads wrong Notion pages | Confirm parent URL in rules; nest docs under parent; say product name in prompt |
| Guest account can’t connect | Notion MCP requires workspace **member**, not guest |
| Children missing in fetch | Drag pages under the parent in Notion sidebar |
| Rules seem ignored | Ensure files are `.mdc` under `.cursor/rules/` with correct frontmatter |

---

## 8. Minimal copy-paste starter files

### `.cursor/mcp.json`

```json
{
  "mcpServers": {
    "notion": {
      "url": "https://mcp.notion.com/mcp"
    }
  }
}
```

### `.cursor/rules/project.mdc` (fill blanks)

```markdown
---
description: Product scope and Notion ownership
alwaysApply: true
---

# <PRODUCT> — project rules

## Notion scope (required)

- Docs only under: <PARENT_PAGE_URL>
- Ignore other Notion pages for this repo.

## Non-goals

- …

## Stack

- …
```

---

## Reference (this repo)

- Product: **Investory**
- Repo: Personal-Quant
- Notion parent: https://app.notion.com/p/Investory-4086257be62f809baff1fdac8c9464bd
- Local paste kits: `docs/notion/`
- Agent guide: `AGENTS.md`

When starting the next project: copy this playbook, replace product name + Notion URL, recreate the Notion tree, drop in `mcp.json` + rules, OAuth once, smoke-test, then build.
