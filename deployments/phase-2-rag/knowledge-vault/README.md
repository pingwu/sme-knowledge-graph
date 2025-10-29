# Knowledge Vault

This directory contains your markdown files that will be indexed by ChromaDB for semantic search.

## How It Works

1. **Add your markdown files** to this directory (or subdirectories)
2. **Index them** using the chatbot's indexing feature
3. **Ask questions** and get answers with source citations

## Example Files

This vault includes sample files to demonstrate RAG capabilities:

- `sample-decision.md` - Example decision documentation
- `sample-meeting-notes.md` - Example meeting notes
- `sample-technical-doc.md` - Example technical documentation

## Best Practices

### File Organization
```
knowledge-vault/
├── decisions/
│   └── vendor-selection-2024.md
├── meetings/
│   └── weekly-standup-2024-01-15.md
├── technical/
│   └── database-architecture.md
└── relationships/
    └── acme-corp-partnership.md
```

### Markdown Format

Use clear headers and structure:

```markdown
# Title

## Context
What's the background?

## Decision
What was decided?

## Rationale
Why?

## People Involved
- @john (Engineering)
- @sarah (Product)

## Related Documents
- [[previous-decision]]
- [[meeting-notes-2024-01-10]]
```

### Metadata

Include metadata at the top for better searchability:

```markdown
---
date: 2024-01-15
tags: [database, architecture, postgres]
people: [john, sarah, mike]
status: approved
---
```

## Indexing

After adding files, index them using the chatbot UI:

1. Click "Index Knowledge Vault"
2. Wait for confirmation
3. Start asking questions!

## Example Queries

- "What did we decide about database selection?"
- "Why did we choose PostgreSQL?"
- "What did Sarah say in the January meetings?"
- "Show me all decisions related to vendors"
