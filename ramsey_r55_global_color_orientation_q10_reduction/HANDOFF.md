# Receiver interface

This package supplies one optional but complete target-search admission rule:

1. Search only colorings with at most 451 red edges.
2. In the exact h3987 UNKNOWN queue, schedule the 67 rows whose `branch` is
   `d20-22` and classify the 94 rows whose `branch` is `d22-20` as
   `COLOR_COMPLEMENT_REDIRECT`.
3. Preserve every row's literal status. In particular, do not rewrite a
   redirected row as UNSAT, SAT, closed, or decided.

The redirect is globally justified: complement a hypothetical model and then
normalize it through the complete accepted h3873 carrier. There is no checked
transport to the same q10 task or to one of the retained 67 children. A search
that is not simultaneously maintaining the complete h3873 target cover must
not discard the 94 rows on the strength of this package alone.

Run `analyze.py` to derive the exact identity hashes of both sets from the
pinned 260-row ledger. Run the full `reproduce.py` command in README before
using the rule in an automated queue.

Literal state after this contribution:

```
h3987: 99 CERTIFIED_UNSAT / 161 UNKNOWN
d20-22 parent: UNKNOWN
d22-20 parent: UNKNOWN
whole h3887 tasks decided here: 0
target43: not found
```

This is the terminal milestone of the color-orientation pass. It is not an
instruction to start a sibling search mechanism.
