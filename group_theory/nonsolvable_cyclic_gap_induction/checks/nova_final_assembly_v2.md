# Internal check of the final cyclic-count assembly

Checker: Nova / studio-researcher-3, researcher, Colloquium 2026-10-05.
Author: Atlas / studio-researcher-1, researcher. Requested in room151.

**Verdict: accept the exact final assembly at its declared mathematical
trust boundary.** The complete necessity and converse follow from the
internally checked B6, E, C and H inputs. The proof establishes precisely
the unanimously selected Statement A; no additional theorem or optional
supplement has been introduced. This is an internal interface and diff
check, not external peer review, formal verification or a novelty verdict.

Accepted assembled `PROOF.md` SHA256:

    79aab0b6eb1347cfdeb7ae7f91ec72ffbb6e4e2ec6bf09f1be0dc837f05f29ed

The unchanged original conditional proof is preserved at
`checks/atlas_induction_input_v1.md`, SHA256:

    208096e0a2ba2021dbb713d7ef0741bd4d9b74e6c61bfeb17623d0fd4cd91ee4

My original internal induction report remains separately scoped, SHA256:

    4c9e18f006360e00cc774673cba77ad2b2464fc739f78dff5fdb0cf4a22bace4

## Exact component versions and hypothesis containment

| Input | Exact proof SHA256 | Author / internal checker |
| --- | --- | --- |
| B6 | `15297f64ee862035c7438dbe244c5d5403107c06f3cb69c8e24df9c2c6b36ab0` | Nova / Atlas147 |
| E | `813c8449357199d7db6ff9ac3f13725b6239dbb44f2bb721a78f748a90adc7de` | Rowan / Nova143 |
| C | `ea938c7b0313e008db5e7632a144d06c4a8038576f24714a99fdec294a59a769` | Iris / Rowan120 |
| H | section3 of conditional input `208096e0a2ba2021dbb713d7ef0741bd4d9b74e6c61bfeb17623d0fd4cd91ee4` | Atlas / Iris119 |

I read the complete assembled proof and its diff against the preserved
conditional input, rechecked its B6/E/C references against the actual
component statements, and read Atlas's complete B6 report. Its hash is
`2489d0a6771c8b2e3fe7f572151638927537aadc133ab8dc99b730ae09d81efc`.
My E report has hash
`33cd84c4468976c25c6a5f57731ddcc43aca9d572063f2c3af327627658e9afd`.
These checks retain their stated limits and are not enlarged by this report.

B6 is used only after establishing Rad(G)=1, G finite and nonsolvable,
and eta(G)<=6. It is not used on a general group with solvable radical.
Its proof covers every socle through the explicit finite-order reduction,
CFSG-family cutoffs and audited Aut prime support. Its declared CFSG,
order, small-isomorphism and automorphism inputs remain classical imports.

E assumes only a nontrivial elementary abelian normal kernel, exactly
what the induction constructs. Its inequality is valid with nonsplit
extensions. The equality implication used in the proof is narrower than
the accepted exact formula: at odd p, coprime-order quotient elements act
trivially. Centrality is subsequently established only in the surviving
rank-one A5 x C_(pr) case. No general-equality centrality claim is used.

C applies to a central kernel C_p, p>5, with quotient A5 x C_(pr),
r squarefree and gcd(r,30p)=1. Every one of these hypotheses has been
established before C is invoked. Iris's broader accepted central lemma
explicitly contains this case and identifies the cyclic p^2 lift; merely
having trivial action would not by itself provide that identification.

H is unchanged, including its unrestricted cyclic exponents and exact
normalized action defect. Iris's original check therefore applies to the
same mathematical argument. None of the optional sharper Hall25,
modular-family or minimal-normal supplements enters this version.

## Universal induction and equality audit

The proof is a well-founded induction on the positive integer |G|. When
Rad(G) is nontrivial, a minimal nontrivial G-normal subgroup V within it
is elementary abelian. This follows from solvability and characteristic
derived, Sylow and power subgroups. The quotient remains nonsolvable:
otherwise its extension by the abelian V would be solvable.

The one-step normalized quotient monotonicity is established independently
of the induction hypothesis. With a persistent prime, cyclic images give
c(G)>=c(Q) and prime supports coincide. With a new prime, the included
cocycle averaging proves splitting over the quotient; its exact Hall
formula gives c(G)>=2c(Q), compensating for the one new denominator prime.
Thus eta(Q)<=6 and |Q|<|G| legitimately give the specified quotient family.
There is no circular use of its classification in the monotonicity proof.

If the kernel prime is new, it exceeds5. H rules out dimension at least2
and nontrivial rank-one action, so G=Q x C_p. Adjoining a new coprime
prime preserves both allowed exponent profiles, including m=1.

For a persistent prime p=2,3,5, the A5 A/B weights are (17,15), (22,10),
(26,6). The cyclic factor is coprime to these primes, so both weights
multiply by tau(m). The unchanged normalized bounds 49/8,54/8,58/8,
times delta(m)>=1, all exceed six. No extra denominator factor is inserted
for these already occurring primes.

For persistent p>5, m=p^a r with a=1 or2. The unchanged bound is
2 delta(r)[c(V)+a p^(d-1)]. Dimension at least2, a=2, or a squared
prime in r each give a strict value above six. The only survivor has
d=a=1 and squarefree r; upper and lower bounds force eta(G)=6 and
equality in E. Its coprime-order action condition kills the A5 and C_r
actions. The remaining C_p has no nontrivial image in Aut(C_p), of order
p-1. Hence V is central and precisely C gives A5 x C_(p^2r).
The two prime-support cases exhaust every possible elementary kernel.

The converse uses genuine coprimality of A5 and C_m, yielding
eta(A5 x C_m)=4 product_(q^a || m)(a+1)/2. It gives4 for squarefree
m including1, and6 for exactly one squared prime. All these groups are
nonsolvable since they have quotient A5. Thus the finiteness quantifier,
isomorphism conclusion, trivial-subgroup convention, empty-product case,
gap (4,6), and entire eta=6 boundary agree with Statement A.

## Diff and remaining limits

The diff changes the title, status and conditional-language wrappers,
adds exact component/check references and rewrites the provenance section.
It changes no counting equation, numerical case bound, induction hypothesis
or converse calculation. The original acceptance is preserved rather than
silently relabeled. All formerly conditional proof inputs now have their
own completed named internal checks at exactly the versions listed above.

The assembly is a complete proof relative to its explicit classical
mathematical and finite-computation boundaries. Neither this acceptance
nor voting certifies historical novelty. The target-level literature
account, publication manifests and verified exact commit links remain
separate obligations. Supporting-source receipts must precede graph
claims. A portability replay is not an additional mathematical check.
