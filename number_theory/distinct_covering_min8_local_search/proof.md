# A distinct minimum-eight covering with LCM 30240

Actual authoring agent: **six-covering-1**. Role: **researcher**.
Status: explicit construction with complete exact finite verification.

## Statement and finite proof

Let `C` be the 85 residue-modulus pairs `[a,m]` in [cover.json](cover.json),
interpreted as the congruences `x = a (mod m)`.

**Lemma.** These congruences form a distinct covering of all integers with
minimum modulus exactly eight and least common multiple 30240.
Therefore `L_min(8) <= 30240`.

All phases are normalized: `0 <= a < m`. The smallest modulus is 8,
whose phase is 7. All 85 moduli are different and divide
`L = 30240 = 2^5*3^3*5*7`. In particular the displayed moduli 864 and 35
occur, and `lcm(864,35)=30240`, so their actual LCM is L.

Define the integer multiplicity

    c(r) = sum_[a,m] in C [r = a (mod m)],    0 <= r < 30240.

The exact computation gives:

| Multiplicity | Number of residues |
|---:|---:|
| 1 | 18862 |
| 2 | 10466 |
| 3 | 909 |
| 4 | 3 |
| 0 | 0 |

The counts sum to 30240. Thus every representative satisfies a congruence
in C. For an arbitrary integer x, put r equal to its normalized residue
modulo L. Because every m divides L, x and r have the same residue modulo
m. The congruence covering r therefore covers x. This proves the lemma.

The proof's finite verification is small enough to reproduce directly.
`verify.py` marks each progression `a,a+m,...` in `[0,L)` and counts its
hits. `audit.py` imports none of that code and instead evaluates all 85
congruence predicates separately for every integer representative. It
also derives the LCM independently from prime exponents. Both compute
every point's multiplicity, every class's private-point count, and the
same full manifest. The multiplicity sequence, one unsigned byte per
representative in increasing order, has SHA-256

    97b16fb2a89d0b54acfc03790e83afa45934edb570e57d1b6d54825c7def3994.

Every class has at least two private points. Consequently removing any
one class from this particular cover destroys coverage. This is an
irredundance statement, not a minimum possible number of classes.

## Construction mechanism and reproduction

The optional C++ search represents a phase for every eligible divisor
`m|L`, `m>=8`. It starts with the phases of the 66-class Zhang–Zhang seed
for the compatible moduli other than seven, and greedily chooses the
remaining phases. All phases may subsequently move; the output is not
restricted to preserving any designated seed class.

For a currently uncovered integer r, a candidate move for modulus m
changes its phase to `r mod m`. Its score is the total nonnegative weight
of newly covered points minus the weight of points covered only by the
old class. The search chooses a greatest-score move, with deterministic
pseudorandom ties and an eight-percent random move probability. At a
nonpositive score it increases the weights of the uncovered points.
Coverage counts and the list of uncovered points are maintained exactly.

The specified seed 20260929 found a complete 89-class covering at 30240
after 940 moves, about 0.20 seconds on the tested GCC 12.2.0 build.
`prepare.py` independently checks the output, then greedily removes
redundant classes in decreasing modulus order while keeping modulus 8.
It deletes four classes, giving the stored 85-class cover. The final
certificate retains 29 of the designated 65 classes of the supplied seed
after deleting its modulus-seven class. The compiler and heuristic are
discovery aids; the explicit stored certificate and literal checks prove
the result independently of them.

Run the three standard-library commands in the [README](README.md).
Optional regeneration compiles `search.cpp`, runs the specified seed,
applies `prepare.py`, and compares the exact complete manifest with the
stored one. A search that stops with holes exits with code 2 and cannot
pass `prepare.py`. No bounded failure becomes a mathematical exclusion.

## Validation and arithmetic boundary

The C++ implementation uses one thread and caps a run at 50 seconds and
200000 moves; the supplied reproduction requests five seconds. The
working period is limited to 100000. Each point's coverage count is at
most the number of moduli, checked below 60000, and stored in 16 bits.
Each penalty weight is at most 200001; score magnitude is at most
`100000*200001=20000100000`, safely inside signed 64-bit arithmetic.
The exact Python verifiers use arbitrary-precision integers.

Checking builds use GCC 12.2.0, C++20, `-O1 -g -Wall -Wextra -Wconversion
-Wshadow -fsanitize=address,undefined -fno-omit-frame-pointer`. A supplied
positive cover at period 70560 is preserved, and a small period-120
inconclusive walk exercises count updates. The successful 30240 replay
is also run under both sanitizers. No relevant compiler warning or
sanitizer failure occurred. These are implementation controls, rather
than exclusions or independent reviewer verdicts.

The Python controls reject a repeated modulus, loss of the exact minimum,
an incorrect period, an invalid normalized phase, and a changed essential
class that leaves uncovered points. They also check the literal 66-class
initializer at period 10080 and the claimed 29 retained classes.

The remaining proof trust boundary is ordinary exact Python execution,
the explicit input pairs, and the unformalized elementary periodicity
argument. Both checker algorithms are by the same researcher; no external
review or proof-assistant formalization is claimed.

## Primary context and unresolved target

[Zhang–Zhang](https://arxiv.org/html/2607.19029), Section 7, supplies the
explicit initializer with minimum seven and period 10080. Only that
literal covering is used and checked here; their claimed optimality
`L_min(7)=10080` is not a premise.

[Harrington–Klein–Lowrance–Trifonov](https://arxiv.org/html/2605.18644),
Theorem 1.11, constructs a minimum-eight covering at period 172800 on
prime support 2,3,5. The present period uses prime seven. These primary
sources and targeted current searches for smaller minimum-eight LCM
constructions were refreshed on 2026-09-29. The explicit 30240 witness
was absent from the inspected sources and committed graph. No exhaustive
priority or record claim is made.

This improves six-covering-1's [70560 upper construction](../distinct_covering_min8_prime_lift).
With six-covering-2's [complete lower-bound certificate](../distinct_covering_min8_lower_bound)
and its [independent review](../distinct_covering_min8_lower_bound_review1),
the campaign interval is `10080 <= L_min(8) <= 30240`. The lower bound
is context, not a premise needed for this existence proof. The exact
unrestricted value remains unresolved; this construction does not exclude
any smaller LCM or determine the different at-least-eight problem.
