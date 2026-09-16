# Independent review verdict

**Verdict: ACCEPT AND STRENGTHEN.**  At target commit
`49b81225ca13eb0c4c4e184c25e61499da65dd2c`, all sixteen frozen 508-point
supports are exactly reproduced and their literal four-colourings are valid
on their complete physical unit graphs.  No sub-509 five-chromatic candidate
survives this cohort.

The reviewer adds a stronger positive certificate: the full 952-point union
of the sixteen supports is four-colourable.  This is stronger than sixteen
unrelated positive words and was not claimed or tested by the target.  It is
still negative record evidence, not a chromatic-number-four theorem.

## Checks that matter

- An independent integer-bitset selector reproduces all sixteen label and
  edge hashes without importing the target's heap or set-based checker.
- All sixteen source words, the parent five-word, connectedness, degrees,
  quotas, pins and retained private-half contacts are directly checked.
- A distinct SymPy exact-field route reconstructs all 452,676 unordered
  pairs in the support union and recovers exactly 4,773 unit pairs.
- The new 952-symbol word is checked edge by edge, in normal and
  assertion-disabled Python; four damaged words are rejected.
- The target's stated maximum metric-ball order through 508 is independently
  reproduced as 507.

## Clarification and limitations

The phrase "the only cross-half edges" is correct when, as the construction
requires, it means edges between the two **private** halves: these are
`(303,1368)` and `(435,1500)`.  Because label 0 belongs to both halves, it
also has 58 edges to the right private half.  This is a wording clarification,
not a defect in the selection or colouring claims.

The SymPy route is arithmetically independent of the target's rational
24-tuple quotient implementation, but both routes share the pinned Appendix-A
path transcription.  No proof assistant is used.  Exact lower bounds on the
chromatic numbers of the sixteen supports and their union are outside scope.
The result is not a classification of all 508-point subsets and does not
independently prove that the 2,131-point parent is five-chromatic.

