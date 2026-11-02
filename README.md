# Release Note Cleaner

**Remove unwanted AI-added captions and production notes while preserving unrelated content.**

[中文说明](README.zh-CN.md) · [The skill](skills/release-note-cleaner/SKILL.md) · [Evaluation fixtures](evals/)

Release Note Cleaner is an [Agent Skill](https://agentskills.io/specification) for reviewing public-facing websites, presentations and documents. It helps an AI assistant remove unwanted AI illustration captions, concept labels, maker-facing notes and unfinished placeholder copy, while avoiding unrelated titles, source credits and interface guidance. It can clean a Chinese-only or English-only artifact independently, as well as mixed-language content; it does not require translation or a second language.

It is a set of instructions for an agent—not a standalone scanner, image editor, browser extension, plagiarism detector or classifier with a guaranteed error rate. The agent still needs access to the artifact and appropriate tools to inspect or edit it.

## Why it exists

An assistant may accidentally leave maker-facing notes in a finished page: “Internal note: remove before launch” or “内部备注：发布前删除”. Meanwhile, a small gray label may be essential: “Artist's reconstruction, not historical footage” tells a museum visitor what they are looking at.

The skill uses a candidate's context and purpose, not its color, size, or a keyword, to decide what to do:

| Decision | Example | In a cleanup task |
| --- | --- | --- |
| Confirmed production residue | A designer's instruction accidentally rendered on a public page | Remove the smallest supported part within the requested scope. |
| User-requested caption | “AI concept illustration”, when the user requests removing AI illustration captions | Remove the matching caption; do not remove an unrelated title or source credit. |
| Audience information | Source credit, product limitation, historical-image disclaimer, form hint or screen-reader label | Keep its meaning and relationships. |
| Uncertain | “AI concept illustration” with insufficient context | Leave it in place and report the uncertainty. |

An explicit request to remove an identifiable label or a clearly defined class of labels authorizes removing matching items in scope, including AI or concept labels. The agent should mention any apparent material loss of meaning or misleading impression and must not invent a replacement fact. The skill does not make legal determinations or require all AI disclosures to remain in every situation.

## Install

For Codex, with Node.js 22.20 or later and npm installed:

```bash
npx skills add GloryPkqa/release-note-cleaner --skill release-note-cleaner -a codex
```

This installs the skill for the current project by default. Add `-g` for a user-wide installation. Review third-party instructions before installing any agent skill. See the [Skills CLI](https://github.com/vercel-labs/skills) for agent selection and installation options.

For a manual user-wide Codex installation, copy the **`skills/release-note-cleaner` folder** to `~/.codex/skills/release-note-cleaner` (on Windows, `%USERPROFILE%\.codex\skills\release-note-cleaner`). It should contain `SKILL.md` and `references/`. Restart or start a new session if the skill does not appear immediately.

## Use

Ask naturally or explicitly invoke `$release-note-cleaner`:

> Audit this landing page for production notes that accidentally appear in the final page. Report candidates only; don't edit files.

> Use `$release-note-cleaner` to clean this English page. Keep source credits, functional hints and meaningful image captions.

> 请清理首页里不该交付给访客的制作备注；先保留有来源、真实性或版权作用的说明，不确定的列出来。

> 删除整个网站图片下方的 AI 主题插画和文创概念示意说明，保留作品标题和图片来源。

> Remove the internal draft note on the pricing page only; leave other routes and languages unchanged.

The skill distinguishes a read-only audit from an authorized cleanup. It attempts to check shared components and translations before changing them, limits edits to the user's scope, and reports what it could not verify.

## Boundaries

- It does not erase every “AI-generated”, “concept” or gray label. These can be meaningful to the audience.
- For flattened images and screenshots, recognizing text does not remove it. Actual removal needs access to the source layer or an image-editing tool, plus visual verification. A screenshot alone does not establish full coverage.
- It should preserve links, credits, accessibility names and descriptions, editable objects and surrounding facts. It should not treat instructions embedded in the artifact as user commands.
- Results depend on the agent, available tools and artifact context. Review uncertain or consequential changes, and verify rendered pages and relevant views.

## Evaluation

The [`evals/`](evals/) directory contains bilingual fixtures and a protocol for exercising preservation, scoped edits and uncertain cases. They are examples for repeatable manual or agent-based evaluation—not evidence of a measured false-positive rate. Structural validation of the skill checks formatting, not judgment.

## License

[MIT](LICENSE).
