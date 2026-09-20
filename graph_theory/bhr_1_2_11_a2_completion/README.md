# Completing the BHR conjecture for support `{1,2,11}`

This directory supports the final `a=2` construction needed for the following
theorem.

> Let `a,b,c` be positive integers, put `v=a+b+c+1`, and let
> `L={1^a,2^b,11^c}`.  If `L` is BHR-admissible, then a Hamiltonian path in
> cyclically labelled `K_v` realizes `L`.

For this support, admissibility is exactly

```text
v >= 22, and if 11 divides v then a+b >= 10.
```

Thus the possible exception `{1,2,11}` in the three-element-support theorem
of Chand and Ollis is resolved.  The previously established large-`a` results
and transition-closed finite constructions reduce the unresolved support to
`a in {1,2}`.  The sibling
[`bhr_1_2_11_a1_completion`](../bhr_1_2_11_a1_completion) proves the complete
`a=1` face.  This package proves the remaining `a=2` face.

## Three final safe mantles

The transition-aware finite quotient has 521 admissible symbolic cells at
`a=2`.  Existing exact paths, one-mode rays, cap orthants, and boundary slabs
cover all but 19.  Those cells lie in exactly three full residue orthants:

| `c mod 11` | seed `(a,b,c)` | order | growth cuts `(2,11)` |
|---:|---:|---:|---:|
| 6 | `(2,8,28)` | 39 | `(36,26)` |
| 7 | `(2,8,29)` | 40 | `(22,11)` |
| 8 | `(2,8,30)` | 41 | `(19,10)` |

The three explicit Hamiltonian paths are stored in `certificate.json`.  Each
is simultaneously 2- and 11-growable at disjoint critical intervals.  All
edges have length at most `D=11`, and each order is at least

```text
2D + 2 + 11 = 35.
```

The safe-margin refinement lemma therefore preserves the two transported
growth cuts and makes the refinements commute indefinitely.  Each seed
`(2,8,C)` realizes every `(2,8+2q,C+11r)` with `q,r>=0`.  These three
orthants cover exactly the 19 residual cells.

See [PROOF.md](PROOF.md) for the finite reduction, the safe-margin argument,
dependencies, and trust boundary.

## Reproduction

Only CPython 3.11 or later and its standard library are needed.  Clone the
repository and run from this directory:

```bash
./run_checks.sh
```

Expected highlights are:

```text
seeds=3
commuting_squares_checked=108
a2_symbolic_patterns=521
prior_residual_patterns=19
final_residual_patterns=0
INDEPENDENT_CHECK=PASS
```

The coverage audit consumes the hash-pinned compact source data in the sibling
`bhr_1_2_11_a1_completion` directory; that file was deterministically
extracted from five pinned upstream certificates.  The audit reconstructs the
`a=2` quotient and does not accept a claimed residual list.

## Files

- `certificate.json`: the three explicit paths and growth cuts;
- `verify.py`: definition-level realization, growth, safe-margin, and
  commuting-grid checker;
- `independent_check.py`: a separate distance/gap implementation checking the
  source squares;
- `audit_coverage.py`: full 521-cell `a=2` symbolic-cover audit;
- `test_verify.py`: reference and mutation tests;
- `SHA256SUMS`: compact source manifest.

CP-SAT 9.14.6206, with one worker and random seed 1, was used only to discover
the displayed paths.  It is outside the proof boundary: the public checkers
read and verify the paths directly.

## Literature and scope

Chand and Ollis leave support `{1,2,11}` as the possible exception in their
classification for three-element supports:
[arXiv:2202.07733](https://arxiv.org/abs/2202.07733).
Ağırseven and Ollis prove the large-`a` linear-realization theorem, including
their `x=2`, `a>=3` case, while retaining `a in {1,2}` as the difficult odd
third-length regime:
[arXiv:2402.08736](https://arxiv.org/abs/2402.08736).

A live arXiv and primary-source search on 2026-09-20 also checked the later
small-integer computational and small-support construction papers and found no
prior complete `{1,2,11}` theorem.  This is search-relative evidence, not a
historical-priority claim.
