# Notion setup checklist (Investory)

Do this once. Paste page bodies from the sibling files in this folder.

## 1. Create the page tree

In Notion, create a top-level page **Investory**, then nested pages:

| Order | Page title | Paste from |
|------:|------------|------------|
| 00 | Overview | [00_OVERVIEW.md](00_OVERVIEW.md) |
| 01 | PRD | [01_PRD.md](01_PRD.md) |
| 02 | Architecture | [02_ARCHITECTURE.md](02_ARCHITECTURE.md) |
| 03 | ADRs | [03_ADRS.md](03_ADRS.md) |
| 04 | Research | [04_RESEARCH.md](04_RESEARCH.md) |
| 05 | Weekly notes | [05_WEEKLY_NOTES.md](05_WEEKLY_NOTES.md) |
| 06 | Glossary | [06_GLOSSARY.md](06_GLOSSARY.md) |

Tip: create empty child pages first, then paste Markdown (Notion “Import” or paste and fix headings).

## 2. Rules for Notion

- No Kanban / task database here — track progress in **Weekly notes** and ship via git.
- Keep ADRs short: Context → Decision → Consequences.

## 3. Cursor MCP (official Notion OAuth)

Config is already in the repo at [`.cursor/mcp.json`](../../.cursor/mcp.json):

```json
{
  "mcpServers": {
    "notion": {
      "url": "https://mcp.notion.com/mcp"
    }
  }
}
```

1. Reload Cursor / open **Settings → MCP** (or **Customize** in the sidebar) and enable **notion**.
2. Complete the **OAuth** browser login when prompted — use the Notion account that owns the Investory pages.
3. No internal integration token is required for this hosted MCP.
4. Verify in chat: “Read the Investory PRD overview from Notion.”

## 4. Done when

- [ ] Seven pages exist under Investory
- [ ] Notion MCP shows as connected/authenticated in Cursor
- [ ] Cursor chat can return PRD text from Notion
