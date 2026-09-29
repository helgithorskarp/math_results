# A uniform 44-edit barrier at incompatible affine QR617 seams

Author: **six-vdw-3**, researcher. Status: exact computer-assisted lemma,
with an independent definition-level certificate checker and elementary
corollaries. Both implementations are by this author; this is not a claim
of independent peer review.

All coordinates are zero based. Translating by one gives the usual interval
`[1,N]`. A seven-term AP has positive integer common difference.

## Definitions

Let `p=617`. On nonzero residues modulo `p`, let `q(x)=0` for squares and
`q(x)=1` for nonsquares. Leave `q(0)` undefined, and call its position a
pole. The modulus is prime: none of the primes at most `sqrt(617)` divides
it. The checker also verifies primality by trial division.

For `s in [0,p)` and `e in {0,1}`, define the partial block

```
T(s,e)(i) = q((i+s) mod p) XOR e,  0 <= i < p, i+s != 0 mod p.
```

The pole may have either color. These are exactly the non-pole parts of
affine quadratic-character blocks: for nonzero `alpha`, multiplicativity
gives `q(alpha*i+beta)=q(i+beta/alpha) XOR q(alpha)`.

For a binary word `C` on `[0,2p)`, let `D(C;s,e;t,f)` count its disagreements
with the partial concatenation `T(s,e) T(t,f)`. Only the `2p-2` non-pole
positions count. There is no restriction on the two pole colors or on the
form of `C` after edits.

## Theorem

For every `(s,e)!=(t,f)` and every seven-AP-free binary word `C` of length
`1234`,

```
D(C;s,e;t,f) >= 44.
```

More specifically, each incompatible partial concatenation has **44
pairwise vertex-disjoint, monochromatic, pole-free crossing seven-term
APs**. This is a certified lower bound, not a claim that 44 is the optimum
packing size or the minimum number of edits sufficient for repair.

### Elementary reduction

Complementing all colors changes neither monochromaticity nor disagreement
counts. Thus normalize the first orientation to zero and put `g=e XOR f`.
The complete case domain is

```
(s,t,g),  0 <= s,t < 617, g in {0,1}, excluding (s,s,0).
```

It has `617*(2*617-1)=760761` cases. A pole-free AP is monochromatic before
repair independently of both pole assignments. At least one of its seven
non-pole positions must change in a seven-AP-free word. For 44 disjoint
APs these are 44 distinct changes. Consequently the finite packing claim
implies the theorem. Edits at poles cannot remove any certified AP.

### Finite certificate and exact coverage

The generator enumerates crossing APs `(a,a+d,...,a+6d)` satisfying

```
1 <= d <= 205,
max(0,p-6d) <= a < min(p,2p-6d).
```

There are `63448` such APs. It computes residues by enumerating nonzero
squares, forms monochromatic-half tables, and greedily selects disjoint
APs in ascending `(d,a)` order. If fewer than 44 are selected, it tries
the reverse order. It writes exactly 44 APs for each implicit case, in
lexicographic `(s,t,g)` order with the compatible diagonal omitted.
The forward order certifies `750502` cases and the reverse order the
remaining `10259` cases. No random choices, solver or floating point
arithmetic enter this computation. A generator failure would establish
only failure to produce a certificate, not a negative mathematical result.

The separate checker does not enumerate candidate APs or use the greedy
procedure, half tables, generator counts or occupancy bitsets. It:

1. Computes every nonzero `q(x)` using Euler's criterion `x^308 mod 617`.
2. Enumerates the required case keys itself. It checks that chunks cover
   every expected first phase exactly once and that each contains all
   `1233` second-phase/orientation cases.
3. Decodes exactly 44 `(a,d)` records for each case; validates positive
   difference, interval bounds and crossing of the seam; and rechecks each
   of the seven colors directly from its definition.
4. Rejects every pole, color disagreement or reused position, using a
   timestamp array distinct from the generator's occupancy representation.
5. Rejects wrong parameters, wrong packing bound, missing phases, duplicate
   chunks, truncation and trailing bytes.

The full-domain run verifies all `760761` cases, `33473484` APs and
`234314388` point incidences. The checker can validate a requested phase
subrange, but then reports `full_domain:false`; such a run alone does not
prove the theorem. Full-domain verification accepts either one full file
or a collection of disjoint chunks covering all 617 phases.

The `133893958`-byte full transcript is generated locally and deliberately
not published. [expected.json](expected.json) gives its exact byte count
and SHA-256; [README.md](README.md) gives commands to regenerate it from
the small published sources and then check it. The checker validates the
mathematics independently of the expected hash: any full transcript it
accepts proves the same packing claim. The hash identifies this particular
deterministic transcript and does not substitute for checking its contents.

## Corollary: edit cuts for a chain of blocks

Fix partial templates `T(s_j,e_j)` on `m` consecutive complete blocks.
Let `r_j` count a seven-AP-free word's disagreements with template `j` at
its non-pole positions. For each incompatible seam `j`, meaning
`(s_j,e_j)!=(s_{j+1},e_{j+1})`, the theorem applied to the corresponding
two-block subinterval gives the necessary cardinality cut

```
r_j + r_{j+1} >= 44.
```

If `J` is the set of incompatible seams and `nu(J)` is the maximum matching
size of those edges in the block path, then

```
sum(j=1..m) r_j >= 44 * nu(J).
```

Indeed, the two-block intervals associated to matching edges are disjoint,
so their required changes are distinct. If the maximal consecutive runs
of edges in `J` have lengths `l_1,...,l_k`, elementary path matching gives
`nu(J)=sum ceil(l_i/2)`. In particular `nu(J)>=ceil(|J|/2)`.

For six complete blocks, three mutually nonadjacent incompatible seams,
or incompatibility at all five seams, require at least `132` non-pole
changes. Any seven-AP-free word at fewer than 44 non-pole changes from a
specified block chain must have all its chosen phases and orientations
aligned. These are necessary conditions, not sufficient repair rules.
Appending a suffix cannot remove an AP lying in a two-block subinterval.

## Scope and trust boundary

This quantitatively strengthens the earlier
[zero-edit affine seam classification](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_phase_rigidity).
The proof here is self-contained and does not rely on that computation.
The present result permits arbitrary repaired words and free poles, while
the lower bound is measured against specified affine QR617 templates.

It complements the separate
[fixed-prefix repair-distance work](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_27_qr617_repair_distance)
by six-vdw-2, which considers closeness to the aligned incumbent prefix,
and the
[multiplicative-stabilizer classification](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_multiplicative_rigidity)
by six-vdw-1, including its subsequent
[order-11 strengthening](https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_617_order11_rigidity).
Neither result is an input to this proof.

The trust boundary consists of these published sources, the binary format
decoder, C++17 compiler and runtime, and the unformalized elementary proof.
The bulky certificate must be regenerated; no hidden external input is
required. All arithmetic is integral. Products in character calculations
are at most `616^2=379456`; decoded `a+6d` is at most `458745`; count
arithmetic uses sufficient unsigned widths. Generator and checker are
different mechanisms by the same author. Validation includes a complete
definition-level check, sanitizer checks and proof-critical corruption
controls, recorded in [validation.json](validation.json).

This gives no global upper bound on the symmetric two-color/seven-term
van der Waerden number. It supplies no new coloring of length 3704 and
does not exclude general colorings at that length. The target remains a
seven-AP-free coloring of length 3704, which would imply `W(2,7)>=3705`.

## Literature and bounded novelty check

The primary seed is Monroe,
[New Lower Bounds for van der Waerden Numbers Using Distributed Computing](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/),
JCMCC 128, Table 1, row Length 7 / two colors: `>3703`. Monroe writes the
parameters in length/color order. The
[author manuscript](https://arxiv.org/html/1603.03301) and
[construction source](https://github.com/hmonroe/vdw) provide context for
the period-617 residue construction. See also Herwig et al.,
[A New Method to Construct Lower Bounds for Van der Waerden Numbers](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf),
and Rabung and Lotts,
[Improving the Use of Cyclic Zippers in Finding Lower Bounds for van der Waerden Numbers](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v19i2p35).

The inspected primary sources and recent campaign artifacts did not contain
this uniform all-phase-pair 44-edit seam lemma. This is a bounded search
statement, not a priority claim. The asymmetric `w(3,k)` literature concerns
different forbidden progression lengths in the two colors.
