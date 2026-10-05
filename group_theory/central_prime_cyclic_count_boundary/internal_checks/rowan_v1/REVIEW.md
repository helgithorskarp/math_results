# Internal check of Iris's central boundary, version1

Checker: Rowan / **studio-researcher-4**, researcher.
Date: 2026-10-05. Board task8; primary authorship is Iris / studio-researcher-2.
This is an internal mathematical and computational check, not external
peer review, formal verification, or a novelty verdict.

## Exact artifact and conclusion

I read Iris's complete proof, README, sources and checker. All transferred
files matched the hashes in research-room112. The mathematical version is:

    PROOF.md SHA256
    ea938c7b0313e008db5e7632a144d06c4a8038576f24714a99fdec294a59a769

The source directory is
`group_theory/central_prime_cyclic_count_boundary` in Iris's workspace.
The independently reproduced fixture input is preserved here as
`IRIS_FIXTURES_v1.json`, SHA256
`707fbaf9de8a012d4d4cda68a51a10c3406fae8a3a2953ab27244a451f08705d`.

**Conclusion:** I accept this exact conditional central-extension lemma
and its finite count evidence. I found no mathematical defect requiring
revision. Its assumptions remain essential: a CENTRAL kernel C_p,
p>5, and quotient A5 x C_m with gcd(m,30)=1. The claim allows arbitrary
exponents in m. It does not establish those assumptions for arbitrary
groups and does not close the radical-free base or the full target.

## Independent structural reconstruction

I reconstructed the argument in terms of the derived subgroup of the
inverse image H of A5, and a commutator map from that subgroup. This
also checks Iris's normal-complement and centralizer interfaces.

1. The central C_p extension of H/N=A5 splits by averaging its section
   cocycle over60 elements. The denominator is invertible precisely
   because p>5. Summing the cocycle identity gives
   alpha(x,y)=t(x)+t(y)-t(xy), so modifying the section by -t makes a
   homomorphism. Therefore H=C_p x A, A is isomorphic to A5.

2. A5 is perfect, so A=H'. H is normal and H' characteristic in H,
   proving A is normal in G. This establishes the needed normality;
   no assertion that an arbitrary Hall complement is normal is used.
   Iris's elementary 3-cycle proof is correct: the displayed involutions
   have a 3-cycle commutator, all20 3-cycles form one A5 conjugacy class,
   and they generate A5. The generating-cycle intersection argument also
   proves its center is trivial.

3. For any g, choose a in A with the same A5 component in the quotient.
   Then b=a^(-1)g commutes with A modulo N. For u in A, [b,u] lies in
   N and is central; hence u -> [b,u] is a homomorphism A -> N.
   Perfectness makes it trivial. Thus b centralizes A. This is an
   alternate verification of Iris's injective-quotient conjugation
   calculation. With K=C_G(A), G=AK and A intersect K=Z(A)=1,
   so G=A x K. No table of Aut(A5) or Schur multipliers is needed.

4. The quotient of K by N is exactly C_m. A generator lift v, together
   with central N, generates K, so K is abelian. It is the CYCLIC
   quotient, rather than a merely abelian quotient, that justifies this.

5. The q-Sylow factors for q!=p inject into the cyclic quotient and
   are cyclic. For the p-part, if m=p^a r with a>=1, choose commuting
   generators x,z with z generating N and x projecting to a generator
   of C_(p^a). The sole obstruction is x^(p^a)=z^t. If t is nonzero,
   z is a power of x and the p-part is C_(p^(a+1)). If t=0, x has
   order p^a and its subgroup intersects N trivially, giving
   C_(p^a) x C_p. This exhausts the possibilities and does not invoke
   a classification of all p-groups. At a=0 the whole K is cyclic C_(pm).

6. Counting orders in C_(p^a) x C_p gives p+1 subgroups of order p
   and p of each order p^j for2<=j<=a, hence c=ap+2. Coprime factors
   multiply their counts. The denominator counts p only once:
   eta=2(a+2)delta(r) in the cyclic case and
   eta=2(ap+2)delta(r) in the split case. For a=0 it is4delta(m).
   For p>=7 the split case is at least18. The cyclic case is at most6
   only when a=1 and r squarefree. In the new-prime case,
   delta(m)<=3/2 permits only all exponent1 or one exponent2; two
   squares contribute9/4, and an exponent>=3 contributes at least2.

This validates all central lemma cases, including m=1, a>1 and arbitrary
r exponents. In the surviving persistent-prime interface from Rowan,
the split p-squared lift is excluded and the group is A5 x C_(p^2 r).
The computation below is corroboration, not the reason this structural
classification is universal under its stated assumptions.

## Independent finite method and coverage

I did not execute Iris's checker. `independent_counts.py` represents
permutation orders by cycle decomposition and modular-coordinate orders
by n/gcd(n,a), then combines them by lcm. It sums reciprocal totients
exactly, with a direct coprime-count totient implementation. Iris instead
walked every generator's literal powers and deduplicated subgroup sets.
Both methods rest on elementary group facts; neither is a formal verifier.

The independent script reproduces all mathematical fields for all seven
author fixtures, including every element-order histogram, total count,
eta, omega, exact generator-weight sum and both sampled lift cosets:

| Fixture | c | eta |
| --- | ---: | ---: |
| A5 |32|4|
| A5 x C7 |64|4|
| A5 x C49 |96|6|
| A5 x C7 x C7 |288|18|
| A5 x C77 |128|4|
| A5 x C343 |128|8|
| A5 x C49 x C7 |512|32|

The respective order7 quotient-generator cosets have seven lifts of
order49 and seven lifts of order7. The independent structural finite
control generates A5 from the20 conjugates of one commutator, obtaining
derived-subgroup size60 and center size1 by centralizing those generators.
Iris used all pairwise commutators and full-group center comparisons.

Six changed inputs also pass, including the new prime11, higher exponent,
and a second squared prime: cyclic C121 (eta6), split C11 x C11 (eta26),
cyclic C1331 (eta8), split C121 x C11 (eta48), C49 x C121 (eta9),
and C7 x C7 x C121 (eta27), each multiplied by A5. These illustrate
the broader formulas and do not stand for enumeration of all extensions.

Run from Rowan's repository root:

```sh
python3 internal_checks/rowan_iris_central_v1/independent_counts.py
```

Tested with Python3.12.14, standard library only, one process, exact
integers and Fraction. Expected output is `RESULT.json`, status
`INDEPENDENT_FINITE_CONTROLS_PASS`, seven author comparisons and six
changed inputs. The preserved author input hash is checked first.

## Limits and remaining interfaces

I checked the self-contained mathematical argument and finite evidence;
I did not claim historical novelty for its classical ingredients or
independently audit every bibliographic statement in SOURCES.md. The
Milne splitting reference is contextual, since the necessary splitting
argument and A5 facts are supplied and checked directly.

The prior centrality/quotient restrictions, the simple/almost-simple base,
the noncentral new-prime branch, and the global induction are distinct
dependencies. This acceptance verifies Iris's interface C under exactly
its stated hypotheses, not the campaign's unconditional classification.
