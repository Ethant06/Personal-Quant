# Source of Truth

One job per tool. Do not duplicate the same information in two places.

## Ownership

| Tool | Owns | Does not own |
|------|------|--------------|
| **Notion** | PRD, architecture narrative, ADRs, research, weekly notes, glossary | Code |
| **GitHub (git)** | Source code, branches, commits, push, optional PRs | Long-form product docs |
| **Cursor + MCP** | Implementation using repo rules + Notion context | A second backlog |

**Rule of thumb**

- **Why / what / weekly progress** → Notion  
- **How in code** → Repo via normal git (`branch` → `commit` → `push`)  

No GitHub Projects / Jira boards — keep execution lightweight.

## Linking convention

- Notion PRD epics can note which week they target.
- Commits/PRs can mention the Notion section or week in the message body when helpful.

## Notion page tree

**Parent URL:** https://app.notion.com/p/Investory-4086257be62f809baff1fdac8c9464bd

See paste-ready content in [docs/notion/](notion/).

```
Investory/   ← use only this parent for MCP reads
  00 — Overview
  01 — PRD
  02 — Architecture
  03 — ADRs
  04 — Research
  05 — Weekly notes
  06 — Glossary
```

Do **not** keep a task board in Notion — use Weekly notes for progress and git history for what shipped.

## When to update what

| Event | Update |
|-------|--------|
| Scope or acceptance criteria change | Notion PRD |
| New technical decision | Notion ADR |
| Starting work | Branch from `Main` |
| Finishing work | Commit + push (PR optional); note progress in Weekly notes |
| Agent coding session | Read Notion (MCP); follow AGENTS.md |
