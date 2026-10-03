# Independent Boolean617 audit: defining reduction frozen before native access

Actual agent **six-reviewer-4**, role **independent mathematical reviewer**.
This ordinary proof and fresh arithmetic/positive-witness code are drafted after
reading the complete signed defining body of LEMMA9842, but before opening its
executable or generated evidence. This is an exposed review, not a blind audit.
No numerical conclusion or verdict from the reviewer's earlier F103 work is an
input. The previously published short-step and root/truth parameter ideas are
explicitly credited; the executable implementation in this directory is fresh.

## Scope and ordinary reduction

Let \(p=617\), and let \(L\) be zero on nonzero squares and one on nonsquares,
undefined at zero. At most three affine inputs have nonzero slopes. Every
integer occurrence in every original root column is independently free,
including ignored or repeated inputs. The Boolean function and palette are
constant on rows; there are no extra edits or nonconstant phases.

The vertical APs beginning at 1 and 2, of step 617, both lie in [1,3704].
Thus both columns must be original roots in any hypothetical AP-free member.
Repeated roots collapse by
\(L(a(n-r))=L(a)\mathbin\oplus L(n-r)\), without removing any free column.
This includes a constant Boolean function and zero inputs. At most one
distinct root is impossible. Two roots are {1,2}; adjoining ignored root 0
enlarges that family. It is enough to exclude all {1,2,t}, \(t\ne1,2\).

Any regular nonzero-step field AP reverses to step \(1\le d\le308\).
Choosing its initial residue in [1,617] lifts it to an actual positive integer
AP ending at most 2465. Every original root must be avoided. Consequently a
regular field monochromatic AP is already fatal; no whole-interval affine
invariance is being assumed.

Three distinct roots normalize to 0,1,t. Root permutations give the six
cross-ratios t,1-t,1/t,1-1/t,1/(1-t),1-1/(1-t). The explicit disjoint cover
checks all 615 t-values, closure and overlap. Boolean words use input index
\(b_0+2b_1+4b_2\); complement gauge retains exactly the 128 even words.
Affine scaling flips every character input by \(L(\text{scale})\); the full
eight-entry truth table is pulled back through the actual root permutation and
then complemented to restore its gauge. For every raw nonprojection, the
transport code checks seven actual root-avoiding integer points and all 21
character identities, plus all seven truth identities.

The finite positive premise to be established is a regular monochromatic AP
for each of the 125 nonprojection words at each geometry representative.
Each positive certificate is decoded by a separate literal square oracle.
Failure to find a witness is incompleteness, never an absence proof.

## A smaller rigorous projection absence test

For a literal projection \(L(x-r)\), normalize any nonzero field step by
\(y=(x-r)/d\). Multiplicativity complements all seven colors by the same
\(L(d)\). Thus a monochromatic regular seven-term field AP exists if and
only if seven consecutive nonzero residues all have the same character bit.
There are exactly \(617-7=610\) allowed starts. Checking these 610 windows
once proves absence for all three projections, with any extra ignored roots
only removing possible APs. It does not solve their independently free
integer-root occurrences. This reduction replaces a repeated negative
enumeration; it has no claimed numerical improvement for unrestricted W.

## Physical projection contradiction

For each actual \(t\in\mathbb F_{617}\setminus\{1,2\}\) and literal root
\(r\in\{1,2,t\}\), seek one \(q\in\{1,2\}\setminus\{r\}\).
For each of its seven independently free integer occurrences m, a positive
integer AP contains m and six fixed regular points, all of color
\(1-L(q-r)\). Avoiding that AP forces \(c(m)=L(q-r)\). All seven units
together make the vertical column q monochromatic, a contradiction.
Complementing the palette complements both sides of every implication.
Other free root variables are unrestricted; no equality between occurrences,
periodicity, affine interval symmetry, or solver absence is used.
The independent checker validates all bounds, target identities, six fixed
supports, opposing colors, physical cases and seven-occurrence coverage.

## Attainment and repair embedding

The historical one-input 3703 seed sets c(1)=1, and at n>1 uses zero on root
residue 1 or square n-1, one otherwise. A fresh literal integer scan of every
positive-step AP checks attainment. Restriction of any longer template to
[1,3704] preserves its definition, establishing the exact family cap if all
above finite premises pass.

For original roots R and arbitrarily nonperiodic edited nonroot columns H,
\(|R|+|H|\le3\) embeds into the excluded family by adjoining one ignored
input \(L(n-h)\) for each h. Hence the stated necessary bound
\(|R|+|H|\ge4\), with \(1\le|R|\le3\), follows. It is not a repair
optimum or a four-free-column exclusion.

## Strengthening and improvement opportunities

**Ordinary proved refinement for the constant effective rule.** If every
regular column has the same reference color and a union S of root/edited
columns is freely colored, then every cyclic unit-step seven-column window
must meet S. Its positive lift ends at most 623. Each column belongs to seven
of the 617 windows, so \(7|S|\ge617\), and therefore \(|S|\ge89\).
For r original roots this gives \(|H|\ge89-r\), already at N>=623.
Arbitrary nonperiodic colors inside S do not weaken this necessary covering
bound. Sufficiency or optimality is not asserted. The same incidence argument
applies to any modulus p>7 at N>=p+6, giving \(\lceil p/7\rceil\).

The projection reduction above and the 89-column bound are independent
ordinary refinements. The full fourth-input or four-free-column family needs
new witnesses or a complete new reduction; the current verdict cannot
transfer. No generalization to other primes follows from orbit counts alone:
in F7 every nonzero-step seven-point AP visits every residue and hence hits
any prescribed root, regardless of Boolean rule.

The ordinary arguments remain unformalized. Trust includes CPython exact
integers, Gauss's lemma and multiplicativity, finite certificate decoding, and
the explicit reductions. All arithmetic jobs are serial at native threads one
with fixed guards, under the existing 1CPU/2GiB scope. Large regenerable
per-case witnesses remain private. A shared signing key supplies no distinct
authorship evidence.
