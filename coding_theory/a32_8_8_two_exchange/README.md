# The published 1667-word `A(32,8,8)` code is 2-exchange-maximal

## Result and scope

Let `C` be the 1667-word binary constant-weight `(32,8,8)` code in
[`incumbent_1667.txt`](incumbent_1667.txt).  There is no set `R` of at most two
words of `C` for which replacing the words in `R` by `|R|+1` new weight-eight
words leaves minimum distance at least eight.  Thus this named incumbent is
**2-exchange-maximal**.

This is a complete finite neighborhood result for one explicit incumbent.  It
does **not** prove that `A(32,8,8)=1667`, and it does not rule out a 1668-word
code farther away.  Its construction-search consequence is exact: any
one-word improvement starting from this incumbent must destroy at least three
incumbent words before refilling.

The code was reported by William Echols in [*New lower bounds for
constant-weight codes via seeded bit-swap tabu
search*](https://arxiv.org/abs/2608.13906), where it establishes the current
lower bound `A(32,8,8) >= 1667`.  The source repository was pinned at commit
`4f0bf18b094fb15c3634001ea8aed847e8353d1c`; see [NOTICE.md](NOTICE.md).

## Exact reduction

Identify a word with its eight-point support.  For an outsider word `x`, define
its blocker set

```text
B(x) = { i : |x intersect C[i]| >= 5 }.
```

The distance condition is equivalent to intersection at most four.  After
removing incumbent indices `R`, `x` can be inserted exactly when `B(x)` is a
subset of `R`.  Therefore:

- a direct insertion requires `|B(x)|=0`;
- an improving one-removal exchange requires two mutually compatible outsiders
  with the same singleton blocker;
- an improving two-removal exchange requires three pairwise compatible
  outsiders whose blocker sets are contained in the removed pair.

The exhaustive census over all `binom(32,8)=10,518,300` weight-eight words
finds no zero-blocker outsider, 158 one-blocker outsiders, and 636 two-blocker
outsiders.  The complete low-blocker list is
[`low_candidates.tsv`](low_candidates.tsv).  Testing every relevant refill
gives:

```text
one-removal add-pairs tested:                         76
incumbent removal-pairs tested:                1,388,611
two-removal pools having at least 3 candidates:    17,965
two-removal add-triples tested:                    107,820
improving exchanges found:                              0
```

## Enumeration and independent checks

[`exchange_profile.cpp`](exchange_profile.cpp) performs two complete universe
enumerations by different reductions.

1. **Five-subset ownership.**  Minimum distance eight means that no five-subset
   belongs to two incumbent words.  The program maps each of the 201,376
   five-subsets to its unique owner, if any, and obtains every `B(x)` by looking
   up the 56 five-subsets of `x`.  This produces the full blocker histogram.
2. **Direct popcount threshold scan.**  A separate pass compares every outsider
   directly with the 1667 incumbent words and stops only after its third
   blocker.  It independently regenerates all outsiders with at most two
   blockers.  The two ordered lists must agree entry for entry.

The full census also satisfies the independent double-counting identity

```text
sum_{x outside C} |B(x)|
  = 1667 * (sum_{j=5}^8 binom(8,j) binom(24,8-j) - 1)
  = 202,147,088.
```

[`verify_exchange.py`](verify_exchange.py) is a definition-level Python
checker.  It reparses and verifies the incumbent, directly recomputes the
blocker set of every listed low candidate, and independently enumerates all
one- and two-removal refill tests.  It deliberately does not duplicate the
10.5-million-word completeness scan; that boundary is covered by the two C++
algorithms, their entry-level comparison, the binomial enumeration checks, and
the incidence identity.

## Reproduction

Requirements are GCC with C++20 support, GNU Make, and Python 3.  The recorded
run used GCC 12.2.0 and Python 3.11 on one CPU core.

```bash
make check
```

This compiles the release enumerator, runs its full analysis, compares the
generated low-candidate certificate and deterministic report against the
checked-in files, and runs the independent Python verifier.  The two production
enumerations took about 6 and 4 seconds respectively on the recorded machine.
Generated binaries and logs remain under ignored `build/`.

For a sanitizer replay:

```bash
make sanitize
```

The full AddressSanitizer/UndefinedBehaviorSanitizer analysis was run and
matched the release artifacts byte for byte.  Fixed-width values are bounded:
words use 32 bits; combinadic ranks are below 10,518,300; blocker indices are
below 1667; counters and incidence totals use unsigned 64-bit integers.

Compact expected outputs are in
[`expected_analysis.txt`](expected_analysis.txt) and
[`expected_verification.txt`](expected_verification.txt).  File hashes are in
[`SHA256SUMS`](SHA256SUMS).

## Downstream use

The next exact neighborhood is radius three.  Only the 2,356 outsiders with at
most three blockers can participate, so the full histogram and named blocker
sets give a sharply reduced input for a four-word refill search.  Beyond that,
the same blocker representation supplies targeted destroy-and-repair seeds for
the unrestricted attempt to construct 1668 words.
