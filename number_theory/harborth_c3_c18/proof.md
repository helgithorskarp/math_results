The Harborth constant of C3 ⊕ C18 is 21.

Here Cn denotes the additive cyclic group Z/nZ. For a finite abelian group
G, its Harborth constant g(G) is the least k such that every k-element
subset contains exp(G) distinct elements summing to zero. We prove the
following exact computer-assisted theorem:

> **Theorem.** Every 21-element subset of G=C3 ⊕ C18 contains an
> 18-element zero-sum subset, and some 20-element subset does not.
> Consequently, g(C3 ⊕ C18)=21.

All quantifiers are unrestricted. The proof uses no selected anchor,
prescribed class profile, or local repair neighborhood.

Let σ(S) denote the sum of a subset S. For |S|=21, an 18-element subset
T has sum zero precisely when its three-element complement U=S\T
satisfies σ(U)=σ(S). This elementary complement equivalence is also
Lemma 2.5 of [Guillot et al.](https://doi.org/10.5802/jtnb.1097).

First reduce the possible totals. An affine map f(x)=φ(x)+t, with φ a
group automorphism, preserves distinctness and 18-element zero sums,
because 18t=0. It transforms σ(S) into φ(σ(S))+21t=φ(σ(S))+3t.
It also transforms any triple sum by φ followed by addition of 3t, so
the complement formulation is equivariant.

Write σ(S)=(a,b), with 0≤a<3 and 0≤b<18. The following cases cover
all possible totals:

1. If b is divisible by 3 and a=0, translating the second coordinate by
   c with 3c≡−b (mod 18) gives total (0,0).
2. If b is divisible by 3 and a≠0, first scale the first coordinate by
   a⁻¹ in C3, and then use the preceding translation. The total becomes
   (1,0).
3. If b is not divisible by 3, let v≡−a b⁻¹ (mod 3). The automorphism
   (x,y)↦(x+vy, εy), where ε∈{1,−1} is chosen so that εb≡1 (mod 3),
   sends the total to (0,εb). Translate the second coordinate by c with
   3c≡1−εb (mod 18). The total becomes (0,1).

The first coordinate of vy is taken modulo 3. Each displayed linear
map is an automorphism: its second coordinate is invertible, then its
first coordinate can be recovered uniquely. Each required congruence
for c is soluble because its right side is divisible by 3. The three
classes contain 6, 12 and 36 totals, respectively. No condition on the
points of S was introduced. The finite audit independently checks all
54 explicit normalizers, their permutations of G, and their homomorphism
identities on every pair of group elements.

For each representative s∈{(0,0),(1,0),(0,1)}, introduce 54 Boolean
variables x_g, one for each g∈G. The intended subset is {g:x_g=1}.
The exact constraints are

\[
\sum_g x_g=21,\qquad
\sum_{g=(a,b)} a x_g\equiv s_1\pmod3,\qquad
\sum_{g=(a,b)} b x_g\equiv s_2\pmod{18},
\]

together with

\[
\neg x_g\lor\neg x_h\lor\neg x_j
\quad\text{for every three distinct points with }g+h+j=s.
\]

Thus a solution is exactly a normalized 21-element counterexample. Points
are ordered lexicographically, (0,0),(0,1),...,(2,17), and variable
1+18a+b represents (a,b). The generator enumerates unordered triples
directly. An independent pair-completion enumeration checks the entire
triple list, not just its count.

The cardinality and modular constraints are encoded by deterministic
prefix paths. For a modulus m, let q(i,r) represent residue r after the
first i membership choices. Initially q(0,0) is true and all other
initial states are false. For the next membership variable x and its
coordinate weight w, insert

\[
(\neg q(i,r)\lor x\lor q(i+1,r)),\qquad
(\neg q(i,r)\lor\neg x\lor q(i+1,r+w\bmod m)).
\]

At the final layer the desired state is true and all others are false.
The cardinality path uses states 0,...,21, weight 1, ordinary addition,
and desired final state 21. Its transition selecting a point at state 21
is forbidden by (¬q(i,21)∨¬x).

For any primary assignment, induction on i forces the state reached by
its actual prefix. An overflow or incorrect final state therefore creates
a contradiction. Conversely, if the cardinality and residues are correct,
setting just the actual state true at each layer satisfies every path
clause. Auxiliary one-hot constraints are unnecessary: extra true states
cannot remove the actual forced path. This proves soundness and
completeness of the CNF encoding, including its apparently weaker
forward-only form.

The three generated CNFs have the following sizes:

| Total | Variables | Clauses | Forbidden triples |
|---|---:|---:|---:|
| (0,0) | 2,419 | 5,192 | 462 |
| (1,0) | 2,419 | 5,189 | 459 |
| (0,1) | 2,419 | 5,189 | 459 |

Kissat produced a DRAT refutation of each formula; DRAT-trim independently
checked each refutation. Source, exact CNF hashes, proof hashes and
validation records are included in the package. The proof files are kept
outside the repository; `reproduce.py` regenerates and checks them.
Consequently all three formulas are unsatisfiable. Affine coverage and
the complement equivalence prove the upper bound g(G)≤21.

For the matching lower bound take

\[
S_0=\{(0,j):0\le j<18\}\cup\{(1,0),(1,1)\}.
\]

Any 18-element zero-sum subset would contain either zero, one or two of
the last two points. The first-coordinate sum forces zero, so the subset
would have to be the entire first row. Its second-coordinate sum is
0+1+...+17=153≡9 (mod 18), a contradiction. Hence |S₀|=20 is an
obstruction. This is an instance of the existing direct-sum lower-bound
construction underlying Lemmas 3.2–3.3 of Guillot et al.; the lower bound
is not new. `check_witness.py` additionally checks all 190 possible
18-subsets directly, independently of the complement encoding.

The trust boundary consists of the written reduction, the published
Python generator, the DRAT-trim proof checker, and their execution
environment. Solver UNSAT output is not used alone. Exact semantic
controls check every membership assignment and every total for C2 ⊕ C4
at sizes 5 and 6 and for C3² at sizes 4 and 5, comparing unit propagation
on the CNF against direct exponent-length subset enumeration. These
controls supplement the general encoding proof; they do not replace it.
This is not a proof-assistant formalization or an independent peer review.

The primary family paper proves the prime-parameter cases and computes
C3 ⊕ C12, but does not cover C3 ⊕ C18. The exact value 21 is new to the
primary sources searched through 11 September 2026. This is a calibrated
novelty assessment, not an absolute priority claim. The source trail and
additional checks against general restricted-sumset theorems appear in
[literature.md](literature.md).
