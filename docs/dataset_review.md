# ScopeMate Dataset Review

**Reviewed:** 2026-10-15  
**Scope:** Original dataset review and the subsequent 20-record training-data
expansion.

## Project and dataset inventory

- `dataset/train.jsonl`: 30 records (36,859 bytes), including 10 original
  records and 20 appended synthetic examples.
- `dataset/test.jsonl`: empty (0 bytes).
- `dataset/validation.jsonl`: empty (0 bytes).
- `training/check_dataset.py` was created during the original review and used
  again after expansion.
- No validation or test split was generated; the two existing empty files were
  left untouched.

## Validation results

| Check | Result |
|---|---|
| Training record count | 30 |
| Outer JSONL syntax | Pass: all 30 lines parse as JSON |
| Assistant inner JSON | Pass: all 30 assistant contents parse as JSON |
| Required field set | Pass: exactly the nine requested fields in every response |
| Required field types | Pass: all fields and array items have the requested types |
| Revision limit | Pass: all values are `null`; no negative or non-integer value found |
| Original record preservation | Pass: the original 10 JSONL lines remain byte-for-byte unchanged |

The new checker can be run from the project root with
`python training/check_dataset.py`. It defaults to `dataset/train.jsonl`,
reports line-specific errors, rejects blank lines and duplicate keys, and also
accepts an optional JSONL path. Its run returned:

> PASS: 30 record(s) checked; outer JSONL and assistant schema valid

## Quality concerns

1. **Ambiguous budget basis — original record 7.** The brief says the budget is ₹4,000,
   but does not say whether that is for all four scripts or per script. The
   response labels it “₹4000 total,” which is not established by the brief.
   Preserve the amount without choosing a basis and ask the client to clarify.
2. **Tentative collaboration detail stated as settled — original record 6.** The user
   says the creators *could* promote each other's channels. The response turns
   cross-promotion into a definite requirement and deliverable. Keep it marked
   as proposed or ask whether both creators agree before treating it as scope.
3. **Inconsistent label granularity.** Collaboration examples use labels such
   as “Brand and content creator collaboration,” “YouTube creator
   collaboration,” and “Potential creator collaboration.” These are
   understandable and not contradictory, but a label taxonomy or annotation
   guideline would improve consistency.
4. **Relative dates are not anchored.** Phrases such as “this Friday,” “in 10
   days,” and “next month” are retained without a reference date. This is
   reasonable for preserving the brief, but downstream use should retain the
   message date or ask for an exact calendar deadline when it matters.
5. **Unlimited revisions versus nullable integer — original record 9.** The request for
   unlimited revisions is preserved in `requirements`, and the response
   correctly asks about a defined limit. `revision_limit: null`, however,
   cannot distinguish “not specified” from “explicitly requested unlimited.”
   Keep the request explicit in text and document that `null` is not an
   accepted finite limit.
6. **No obvious duplicate examples in the original set.** Records 6 and 10 both involve creator
   collaboration, but one contains a specific video and tentative
   cross-promotion while the other is deliberately vague. They teach distinct
   levels of brief completeness and are not redundant as written.

## Recommended fixes before using the data for training

- Correct record 7's budget wording and ask whether ₹4,000 is total or per
  script.
- Reword record 6 so tentative cross-promotion is not represented as agreed
  scope.
- Add a compact, canonical `project_type` labeling guide.
- Keep relative date language tied to a known message date or ask for an exact
  date when necessary.
- Define how explicit “unlimited” requests are represented when
  `revision_limit` only supports a non-negative integer or `null`.

The 20 appended examples exercise the requested content-creation and
collaboration cases, including proposed terms, payment negotiation, usage
rights, vague briefs, missing details and conflicting constraints. The
validator checks JSONL and schema correctness, not semantic accuracy; review
the examples against these quality concerns before fine-tuning. No fine-tuning
was started.

## Expansion update

Twenty examples were appended on 2026-10-15. The original 10 records were
verified unchanged, bringing `dataset/train.jsonl` to 30 valid records. The
expanded file passed `python training/check_dataset.py`. The empty validation
and test files remain untouched.
