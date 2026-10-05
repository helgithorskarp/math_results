# Internal check of Nova's eventual all-order lower component

Checker: Rowan, studio-researcher-4, researcher.
Author: Nova, studio-researcher-3, researcher. Author task17.
Campaign: Human-authorized Colloquium, 2026-10-05. Checker workday6.

**Verdict: accepted at the explicit ordinary primary-theorem boundary.**
The exact author proof below establishes, for every integer \(n\geq37\),

\[
 \log_2 M(n)\geq\log_2 N(T_n)>\frac5{36}n^2-\frac54n.
\]

This is an internal team check of the lower component, including one
entry-level reproduction of its new bounded author controls. It is not
external peer review, independent formal verification, exact-count
classification, a raw pebbling-move oracle, or acceptance of the assembled
global asymptotic. No material defect was found within the stated scope.

## Exact inputs

All five author files were copied and hash-verified before checking.
INPUT_RECEIPT.json preserves copy metadata; inputs/AUTHOR_MANIFEST.json
preserves the unchanged author manifest.

| Input | Bytes | SHA256 |
|---|---:|---|
| PROOF.md | 11494 | b7198174579fe7c275218c9e087b1ba0a350d28e1dad63e69e1bd0f051e37da8 |
| README.md | 1858 | 0ca195f866e3c4cd74883eb73f801191035492bfef0718e32a842fb6f307b5c7 |
| check_lower.py | 12196 | c5cc1e32d7b8a7a81b7907dc704a640b5f7b6c9884cf678c7faea2d724cd9375 |
| RESULT.json | 56690 | e00c703662c46c2c55344ff736169dc7464c562f64d56ce09eeeed469bef3910 |
| INPUTS.json | 7308 | bc52c70df893dca7134fa602e3b4d7ee86d7c52b4e061986dd7d523a8d5e2483 |

Author manifest SHA256:
d9a286400bfd5b3673c77d8be6c09ecd58e18f97b143766bf1607dca634fbde8.
Total89546 bytes. The earlier independent prior-source preparation remains
rowan_tree_lower_preparation_v1/DERIVATION.md, unchanged at its preliminary
scope; it did not accept this then-unreceived author version.

## Independent mathematical reconstruction

The literal nonleaf degrees are \(d+1\) at \(p\), \(e+1\) at \(q\),
and two at the \(t-1\) interior path vertices and the \(e\) arm parents.
Only \(p\) and the arm parents have graph-leaf neighbors. Summing ambient
distance weights independently gives

\[
 X_p=(d+1)+2\sum_{j=1}^{t-1}2^j+(e+1)2^t+2e2^{t+1}
     =d-3+(5e+3)2^t,
\]
\[
 X_a=2+2(e+1)+(d+1)2^{t+1}
       +4\sum_{j=1}^{t-1}2^j+8(e-1)
     =(d+3)2^{t+1}+10e-12.
\]

The empty sum at \(t=1\) and zero other-arm term at \(e=1\) agree.
Subtraction reproduces author(L5). For the global leaf-max eligibility,
moving from \(v\) to \(w\) halves the potential contribution \(S_w\)
from the \(w\)-side and doubles the complement:
\(\Phi(w)=2\Phi(v)-(3/2)S_w\).
At a nonleaf of degree \(D\geq2\), the average side contribution is
\((\Phi(v)-D)/D<\Phi(v)/2\). Some neighbor therefore strictly increases
the potential. A global maximum is at a graph leaf, whose potential is
twice its parent's \(X\). Comparing the leaf-parent potentials identifies
threshold maximizers; internal vertices and the factor two are not omitted.

Euclidean division \(n-1=18m+s\), \(0\leq s\leq17\), covers every
integer \(n\geq37\), with \(m\geq2\). The positive parameters
\(d=5m+3,e=2m+2,t=9m-7+s\) have order exactly \(n\).
They give \(X_p-X_a=2^t-(15m+8)>0\): the minimum base case is
\(2^{11}>38\), and each increment in \(m\) multiplies the exponential
by512, more than its linear comparison increases. All maximizing leaves
are thus adjacent to \(p\), without an omitted arm tie.

For the sufficient construction, every graph leaf stays occupied after
redistribution. The complementary \(p\)-side opposite any sibling leaf
contains an occupied arm tip because \(e\geq1\). Start from the canonical
configuration at a maximizing sibling leaf: pile \(1+2X_p\) there,
one at every other leaf, zero internally. Redistribute by a weak
composition of \(X_p\) into the \(d\) sibling excesses \(x_z\).
Their aggregate incoming message remains \(\sum(x_z-1)=X_p-d\).
All scores outside the sibling set stay at their canonical zero value.
The zero score at \(p\) makes the complementary effective input for
leaf \(z\) equal to \(1-x_z\). Its occupied complementary branch
sends \(-1-2x_z\), cancelling its pile \(1+2x_z\). All scores
remain zero, with no EMPTY/occupied-zero conflation.

The mass is \(|L|+2X_p=\operatorname{stack}(T_n)-1\).
Distinct weak compositions give distinct individual vertex functions.
Hence \(\binom{X_p+d-1}{d-1}\) is a sufficient lower count,
without converse classification or an automorphism quotient.

Put \(r=5m+2\), \(Y=(10m+13)2^t+10m+2\). Then \(Y/r>2^{t+1}\).
Each factor in \(\binom Yr=\prod_{i=0}^{r-1}(Y-i)/(r-i)\)
is at least \(Y/r\), by \(i(Y-r)\geq0\).
Thus \(\log_2 N(T_n)>A=(5m+2)(9m-6+s)\).
Independently expanding \(A\) and \(n^2\) gives

\[
 36[A-(5/36)n^2+(5/4)n]=198m-392+107s-5s^2.
\]

The first part is at least four for \(m\geq2\); the last part is
\(s(107-5s)\geq0\) for every residue. This checks the strict result,
constant and range, including the first order37, without an infinite census.

## Primary theorem boundary

I reread the relevant primary text:
[Fairfax-Ball, arXiv:2609.31811v1](https://arxiv.org/html/2609.31811v1).
Section2 has the least-\(k\geq2\), exact-mass and nonempty-stack
conventions used here. Identity(4) and Theorem1.1 give the potential
and threshold interfaces. Theorem3.3 gives the score criterion and
Theorem4.1 the canonical zero-score configuration. The transfer rule
and occupied/EMPTY convention match Section3. These are explicit published
mathematical imports; I did not reprove arbitrary-move necessity or
audit the paper's reported formal-verification environment.

The immutable R and sibling READMEs were read at the quoted hashes.
The original construction and restricted exponent remain prior art.
This check does not establish historical priority or correctness of the
excluded predecessor optimizer/census results.

## Control inspection and reproduction

I inspected the complete new code: literal adjacency, BFS potential,
directed deficit and occupied/EMPTY message routines, compositions and
exact polynomial dictionaries. Ordinary assertions are enabled.
One replay in the copied input directory used:

    PYTHONDONTWRITEBYTECODE=1 /scratch/venvs/discovery-team/bin/python check_lower.py

Exit zero. Complete records, controls and coefficient lists, together
with all deterministic metadata, were compared entry by entry with
the author's RESULT.json. All match:90 sampled all-residue witness
trees, six additional eligibility/boundary trees and378 all-target
score vectors. Deterministic record SHA256:
67c620281ebb8fe9deb170fb7bba5d30ce5ea1fb651b1244e3806aace47731a1.
REPLAY_RECEIPT.json identifies each compared field.

CPython3.12.14, standard library, exact integer/Fraction decisions,
one process and native-thread settings1;2.569607512 CPU seconds,
peak RSS16040KiB on this Linux host. Only the new bounded author
control was rerun, once. No predecessor554-order comparison,
restricted optimizer or unchanged old census was executed.

The replay reproduces the author algorithm. The independent mathematical
check is the direct shape, redistribution and all-order derivation above.
The finite controls are not a different computational reachability proof
or an infinite enumeration; the universal quantifier follows from the
ordinary written proof at its explicit primary theorem boundary.

## Accepted and excluded scopes

Accepted: exact-version sufficient lower construction, true critical mass,
individual-function count, all-order parameters and parent eligibility,
binomial estimate and \(C_-=5/4,n_0=37\), plus the bounded author
controls at their reported scope.

Excluded: converse classification, an exact count of all critical
configurations, arbitrary-tree upper, new structural budget, final global
assembly, historical priority, independent formal or raw-move verification.
Those remain separate artifacts and checking responsibilities.
