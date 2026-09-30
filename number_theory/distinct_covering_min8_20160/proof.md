# An explicit minimum-eight distinct covering with LCM 20160

Actual author: **six-covering-1**, role **researcher**, 2026-09-30.
Status: explicit construction with exact finite verification and a separate
same-author audit. No external review of this new certificate is claimed.

**Theorem.** There is a finite covering of all integers by 77 congruences
with pairwise distinct moduli, smallest modulus **exactly eight**, and
actual least common multiple

\[
20160=2^6\,3^2\,5\,7.
\]

Thus \(L_{\min}(8)\le20160\). With the separately established and
[independently reviewed lower bound](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_min8_lower_bound_review1),
the current campaign interval is
\(10080\le L_{\min}(8)\le20160\). The unrestricted optimum remains open.

## Proof from the explicit congruences

In `cover.json`, every pair `[a,m]` means \(x\equiv a\pmod m\).
The moduli are precisely all divisors of 20160 that are at least eight;
each occurs once, and all residues satisfy \(0\le a<m\).
The row \(1\pmod8\) establishes the exact minimum.
The displayed moduli 64 and 315 have LCM 20160, while every other modulus
divides 20160. Hence the actual LCM is exactly the verification period.

The progression checker reconstructs the integer multiplicity

\[
c(r)=\#\{(a,m):r\equiv a\pmod m\},\qquad 0\le r<20160.
\]

It verifies the complete histogram

| Multiplicity | Number of representatives |
|---:|---:|
| 0 | 0 |
| 1 | 13665 |
| 2 | 6176 |
| 3 | 317 |
| 4 | 2 |

The counts sum to 20160, and their weighted sum is 26976, which also equals
\(\sum_m20160/m\). The SHA-256 of the ordered multiplicity bytes is
`2a265098f6eb7e0727dbc94b74d17f6b11e6bd3c799f3fe0ca90df07491cc7dc`.
The certificate file SHA-256 is
`f3b7ab8112f2fdba3ab32ea992f2380c43c404e8b54c8abdd71c839a9f5424e3`.

For every integer \(n\), its representative \(r\) modulo 20160 has the
same residue modulo every displayed modulus. Since \(c(r)>0\), some
displayed class contains \(r\), and that same class contains \(n\).
This proves coverage of all integers, including negative integers.

Every displayed class has at least one private representative, recorded
in `expected.json`. Therefore this particular cover is irredundant.
Irredundance does not determine the smallest possible number of classes.

## Verification and construction provenance

`verify.py` marks each actual arithmetic progression in the full period.
`audit.py` imports no other source module: it factors the moduli to derive
the LCM independently and directly checks all 77 predicates at each of the
20160 representatives. Both reconstruct every multiplicity and every
private-point count. `controls.py` rejects duplicate moduli, loss of
modulus eight, an incorrect LCM, a destructive phase change and an
unnormalized phase. It also checks the initializer's full period and the
three unchanged initializer classes. All proof checks use ordinary Python
integers and the standard library. No solver status or heuristic failure
is a mathematical premise; no proof-assistant kernel is claimed.

The construction search began from
[six-reviewer-1's 82-class refinement](https://github.com/helgithorskarp/math_results/blob/main/number_theory/distinct_covering_30240_review1/refined_cover.json)
of the earlier
[LCM-30240 construction](https://github.com/helgithorskarp/math_results/tree/main/number_theory/distinct_covering_min8_local_search).
The initializer was authored independently by that reviewer; it is copied
as mathematical input in `seed.tsv`, with source commit
`d2221d221b1c2fc80715a504ccb48f88dcd84538` and hashes in `provenance.json`.
The original source commit is
`f1cb44bd52e4267f21664a4fb1d2cdd9a470c25c`.
Its confirming review at graph height 7258 applies to the older covering,
not to this new period-20160 certificate.

The single-thread weighted local search assigns one residue to each
eligible divisor of 20160. It discards initializer rows whose moduli do
not divide that period and greedily fills missing rows. Each later move
routes a currently uncovered point to one modulus, comparing gained
uncovered weight against lost private weight. Uncovered points receive
penalties at local stalls; four percent of moves choose a random modulus.
The fixed random seed is 2026093005. All moduli were mutable, and the
first complete witness occurred at iteration 178161, after about 24.42
seconds in the one-CPU scope. Only three initializer pairs are unchanged.
This search description is reproducibility information, not a completeness
or optimality argument. `prepare.py` verifies any purported witness before
deleting redundant classes; it deleted none from this certificate.

The search uses at most 200000 iterations, period at most 100000 and a wall
limit at most 50 seconds. Multiplicities fit unsigned 16-bit counts;
each penalty weight is at most 200001 and each score has magnitude at most
20000100000, within signed 64-bit arithmetic. Search termination with
`INCONCLUSIVE` or a resource interruption establishes no exclusion.

## Primary literature and precise scope

[Bosma, *Some computational experiments in number theory*](https://www.math.ru.nl/~bosma/pubs/bosmaexp.pdf),
Section 2 and the table on printed page 5, gives minimum-eight covering
period 60480. The same table's period 20160 belongs to minimum seven.
The table does not assert optimality. Its primary PDF was inspected on
2026-09-30; this construction improves its displayed minimum-eight upper
bound by a factor of three, without asserting a historical record.

[Zhang and Zhang](https://arxiv.org/html/2607.19029), Section 7, provide
the minimum-seven seed at period 10080 behind the earlier construction.
Their claimed minimum-seven optimality is not used in this proof.
[Harrington, Klein, Lowrance and Trifonov](https://arxiv.org/html/2605.18644),
Theorem 1.11, construct a minimum-eight covering at 172800 on prime support
2,3,5. The present example also uses prime seven.
These sources and candidate-specific current searches were refreshed;
the present minimum-eight period-20160 witness was absent from the inspected
material. Exhaustive priority and record status remain unestablished.

The bound concerns minimum **exactly eight**, with modulus eight present.
No assertion about the optimum for the different at-least-eight family or
about minimum moduli greater than 42 is made. Smaller periods remain
unresolved; bounded failed searches are not exclusions.

## Explicit table

Each column pair below gives modulus \(m\) and its chosen residue \(a\).

| m | a | m | a | m | a |
|---:|---:|---:|---:|---:|---:|
| 8 | 1 | 80 | 77 | 480 | 253 |
| 9 | 8 | 84 | 12 | 504 | 54 |
| 10 | 2 | 90 | 56 | 560 | 100 |
| 12 | 7 | 96 | 63 | 576 | 239 |
| 14 | 6 | 105 | 9 | 630 | 294 |
| 15 | 4 | 112 | 52 | 672 | 669 |
| 16 | 5 | 120 | 100 | 720 | 461 |
| 18 | 14 | 126 | 84 | 840 | 54 |
| 20 | 10 | 140 | 18 | 960 | 541 |
| 21 | 15 | 144 | 23 | 1008 | 222 |
| 24 | 3 | 160 | 125 | 1120 | 829 |
| 28 | 10 | 168 | 24 | 1260 | 546 |
| 30 | 16 | 180 | 128 | 1344 | 285 |
| 32 | 13 | 192 | 111 | 1440 | 509 |
| 35 | 23 | 210 | 156 | 1680 | 1500 |
| 36 | 11 | 224 | 125 | 2016 | 1533 |
| 40 | 0 | 240 | 173 | 2240 | 1501 |
| 42 | 18 | 252 | 168 | 2520 | 2406 |
| 45 | 29 | 280 | 278 | 2880 | 221 |
| 48 | 39 | 288 | 95 | 3360 | 1053 |
| 56 | 26 | 315 | 218 | 4032 | 861 |
| 60 | 28 | 320 | 61 | 5040 | 726 |
| 63 | 0 | 336 | 108 | 6720 | 2781 |
| 64 | 15 | 360 | 20 | 10080 | 4893 |
| 70 | 28 | 420 | 358 | 20160 | 6909 |
| 72 | 59 | 448 | 61 |  |  |
