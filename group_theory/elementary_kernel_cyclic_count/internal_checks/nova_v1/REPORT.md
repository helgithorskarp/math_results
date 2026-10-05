# Internal check of Rowan's elementary-kernel lemma

Checker: Nova / studio-researcher-3, researcher, Colloquium 2026-10-05.
Task: research-room task 7. This is another researcher's internal check.

**Verdict: accepted within the stated scope.** The exact formula, lower
bound, equality conditions and conditional persistent-prime proposition
in the following fixed proof are correct. The 22 fixture computations
have been independently reproduced as mathematical outputs, with the
representation-dependent limitations stated below.

Accepted author artifacts:

- `PROOF.md`: SHA256
  `813c8449357199d7db6ff9ac3f13725b6239dbb44f2bb721a78f748a90adc7de`.
- `verify.py`: SHA256
  `17773841a6613dde87faa77dcbdf821b53629c78718c93c5f65a021ce3035845`.
- `EXPECTED.json`: SHA256
  `a9c019cc56412b79d36658ea18bf3dda6e465552a60e9682ec6ec09015262c8f`.

The universal statement assumes only a finite extension with a nonzero
elementary abelian kernel V=(F_p)^d. It assumes neither a complement nor
minimality, faithful action or nonsolvability. For each quotient element
h of order e, a lift x has x^e=a in V, and conjugation T has T^e=I.
The identity (vx)^e=a+(I+T+...+T^(e-1))v follows by multiplication.
Every lift has order e or pe, and the short lifts are exactly the affine
norm solutions N_e v=-a. If solutions exist, their number is the kernel
size p^(d-rank N_e). Translating the lift changes a by a norm-image
element, so the short-lift count is well defined for that coset.

For p not dividing e, averaging projects onto the fixed space of T.
The vector a is fixed, so the norm equation has p^(d-f_h) solutions.
This establishes the local short-lift count without assuming global
splitting. Partitioning elements by generated cyclic subgroup and
using phi(pe)=(p-1)phi(e) gives the first defect
(p-2)(p^(d-f_h)-1)/((p-1)phi(e)). For p dividing e,
phi(pe)=p phi(e) gives the second defect (p-1)s_h/(p phi(e)).
Summing the cosets proves formula (2), not merely its inequality.
All terms are nonnegative. At odd p equality forces every coprime-order
action to be trivial and every divisible-order coset to have no short
lift. At p=2 the first coefficient is zero, so these actions need not
be trivial. No claim that general equality implies centrality is made.

I separately reconstructed the conditional specialization to
Q=A5 x C_m with the stated coprime allowed prime-exponent profile.
The A5 reciprocal-totient weights are (17,15), (22,10), (26,6) for
p=2,3,5, respectively. Since that prime already divides Q, there is no
new-prime denominator factor. The respective minimum normalized bounds
49/8, 27/4 and 29/4 are above six and increase with d.
For p>=7 dividing m=p^a r, the weights are 32 tau(r) and
32 a tau(r), giving 2 delta(r)[c(V)+a p^(d-1)]. This exceeds six
unless d=a=1 and r is squarefree. Equality then forces eta=6.
The coprime-order A5 x C_r factors act trivially on V=C_p, and the
remaining order-p factor has trivial image in Aut(C_p), of order p-1.
Thus centrality follows in this specialization. The proposition does
not identify the resulting central extension or establish its quotient
family; those remain separate interfaces. It uses no Schur multiplier.

## Independent exact computation

`check_extensions.g` builds separate GAP-native permutation, polycyclic
and matrix models. It does not import the author's Python group tables,
kernel-vector parser, norm matrices or code. For each whole group and
quotient it enumerates literal sets of powers to count cyclic subgroups;
it also verifies the reciprocal-totient sum and records full element-
order and cyclic-subgroup-order histograms. In each quotient coset it
checks every lift order, the affine norm identity, norm-image cardinality,
short-lift fiber size, centralizer size, defect and equality predicate.
Fixed-space dimensions come from group centralizers and norm ranks from
image cardinalities, rather than the author's matrix elimination.

`compare_expected.py` matches all the author's representation-invariant
fields for all 22 fixtures. This includes both group and quotient orders,
cyclic counts, eta, both full histograms, A/B weights, both defects, lower
bound and three equality/action predicates. Particularly informative
counts include Q8=5, SL(2,5)=49 and A5 x C49=96; the first two attain
their corresponding lower bounds despite nonsplitting.

Four additional inputs passed:

| Input | Order | Cyclic count | Lower bound | Coprime defect | Divisible defect |
| --- | ---: | ---: | ---: | ---: | ---: |
| F3^3 with a size-three Jordan C3 action | 81 | 29 | 23 | 0 | 6 |
| F5^2 with scalar-2 C4 action | 100 | 57 | 21 | 36 | 0 |
| F2^3 with faithful C7 action | 56 | 16 | 16 | 0 | 0 |
| C121 over C11 | 121 | 3 | 3 | 0 | 0 |

The first has nonzero norm rank, and the third shows why the
characteristic-two equality exception matters. Three guards reject
C4 as an alleged F2^2 kernel, a nonhomomorphic C4-to-C2 projection,
and composite characteristic 4. These are independent semantic checks;
they do not assert identical parser behavior or identical error strings.

The successful run uses GAP 4.12.1, SmallGrp 1.5.1, one serial native
process and a 512 MiB GAP heap ceiling. Python comparison passed with
`ALL_22_MATHEMATICAL_OUTPUTS_MATCH`. An initial complement generator-list
mistake in this checker was corrected before the successful run; its
private transcript is preserved outside the publication allowlist.

## Limits

GAP's constructors, group arithmetic and algorithms remain computational
trust boundaries. Coordinate-dependent cyclic-set and coset digests in
the author's output are deliberately not equated across representations;
the independent checker directly verifies all coset equations instead.
The author code hash identifies the implementation whose mathematical
outputs were checked, not a formal software-verification claim.

The universal mathematical proof is independent of these fixtures.
Historical novelty and the complete nonsolvable eta<=6 theorem are
outside this report. Rowan's later modular-family supplement in message
136 is also outside this fixed proof/evidence check and has its own
internal checking assignment. No graph submission or publication is
claimed by this report.
