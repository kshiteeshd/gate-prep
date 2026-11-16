# GATE Prep — content template and rules

Every subject follows the same shape and every sub-chapter page follows the same template. `python tools/check_learn.py`
enforces the rules marked **[checked]**; a sub-chapter that breaks one is an error, not a warning.

## 1. Structure of a subject

```
Subject
└── Section          a large concept area of the GATE syllabus   e.g. Discrete Mathematics
    └── Chapter      exactly one syllabus topic                  e.g. 5  Graph Theory
        └── Sub-chapter  exactly one sub-topic                   e.g. 5.4  Trees and spanning trees
```

- No overview, "at a glance" or catch-all lessons. Every page is one sub-topic. **[checked]**
- Sub-chapters are numbered `chapter.sub` (5.4) and read in order; later ones may assume earlier ones.
- Every piece of content sits under the sub-topic it teaches. Material that belongs to another sub-topic is moved
  there; material that repeats something already explained is dropped (the build reports it as dropped, not lost).
- Tests mirror the structure: one test per section (30 questions, 75 min), per chapter (20 questions, 50 min) and per
  sub-chapter (10 questions, 25 min), drawn from that sub-topic's own question pool. **[checked: every sub-chapter has a pool of 6+]**

## 2. The sub-chapter template (fixed order)

| # | Block | What it holds | Colour |
|---|---|---|---|
| 1 | Header | section › chapter, number + title, reading time, GATE weight, example and test counts | — |
| 2 | Key idea | one or two sentences, then an analogy, then "In this sub-chapter" (the concept list) | accent |
| 3 | Definitions | every new term, one card each: **term** + a precise one-sentence definition | blue |
| 4 | Concepts 1…n | numbered explanation blocks; formulas in boxes; a repeated reference section is folded in as "In brief" | violet for formulas |
| 5 | Try it yourself | the interactive tool, when the topic has one | — |
| 6 | Worked examples | numbered `5.4.1`, problem visible, step-by-step solution behind "Show the solution", answer bar | green |
| 7 | Proofs and derivations | collapsible | violet |
| 8 | Notes | collapsible extra detail | grey |
| 9 | Common mistakes | one red card per trap | red |
| 10 | Quick check | instant multiple-choice checks with explanations | — |
| 11 | GATE-level practice | 8 questions from this sub-topic's pool, graded with feedback | — |
| 12 | Summary | cheat-sheet box with ✓ bullets, then the sub-chapter test and "mark complete" | accent |

## 3. Writing rules

- **Definitions first.** Each sub-chapter has at least 1 definition card **[checked]**; a definition is one precise
  sentence of at most 45 words **[checked]**.
- **Key idea:** at most 70 words **[checked]**.
- **Concepts:** at least 2 blocks **[checked]**; no two blocks with the same heading **[checked]**. A heading names the
  idea ("Rank–nullity"), not the activity ("More facts").
- **Paragraphs:** one idea each, at most 110 words **[checked]**. A paragraph that lists several bold run-in points
  (`**Label:** …`) is shown as bullet points automatically.
- **Lists** for parallel items, **tables** for comparisons (property vs formula, distribution vs mean/variance),
  **display formulas** (`$$…$$` or the formulas list) for anything the reader must memorise.
- **Worked examples:** at least 3 **[checked]**, GATE level, each with at least 2 steps **[checked]** and a `verify`
  function that recomputes the answer **[checked: answer must match]**. Titles are unique within a page **[checked]**.
- **Quick checks:** at least 3, each with an explanation **[checked]**.
- **Common mistakes:** at least 3 **[checked]**.
- **Summary:** 4–7 bullets **[checked]**, each at most 30 words **[checked]**; every bullet is a fact you could be tested on.
- **Practice pool:** the sub-chapter's `subs` must name sub-topics that have questions **[checked at export]**.

## 4. Typography

| Element | Size | Font |
|---|---|---|
| Page title (with number chip) | 26–30 px | sans, bold |
| Block heading (with number) | 22 px (20 px on phones) | sans, bold |
| Example title / sub-heading | 18 px | sans, bold |
| Body text | 17 px (16 px on phones), line height 1.7, max 72 characters per line | sans |
| Tables, meta line | 14 px | sans |
| Labels (DEFINITION, EXAMPLE 5.4.1, ANSWER) | 12 px uppercase, letter-spaced | mono |

## 5. Colour code

| Colour | Meaning |
|---|---|
| Accent (theme colour) | key idea, summary, numbers |
| Blue | definitions |
| Violet | formulas, theorems, proofs |
| Green | worked examples and answers |
| Red | common mistakes |
| Amber | tips |
| Grey | notes, "In brief" boxes, analogies |

The colours have lighter variants in the dark themes (Slate, Midnight) so they stay readable.

## 6. How a subject is built

1. `learn/s_<code>.py` declares sections, chapters and sub-chapters and which pieces of the authored lessons each takes.
2. `learn/s_<code>_more.py` adds missing material and records deliberate drops; `learn/s_<code>_defs.py` holds the definitions.
3. `content/g_*.py` generators give every sub-topic its own question family with worked explanations.
4. `python tools/build_pack.py`, `python tools/export_site.py`, `python tools/check_learn.py`.
