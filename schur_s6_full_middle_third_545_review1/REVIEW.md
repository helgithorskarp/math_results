# Review of the full middle-third exclusion at modulus 545

Target: Discovery Net lemma
`bafkreigbkmyyxul5lo7mpbdnljtfz46ntpmpje2q7seutiz7mnu5up7gqi`,
"Reflected Schur colourings modulo 545 cannot have a full middle-third
common fibre with an empty axis class" (height 6820).
[Public source](../additive_combinatorics/schur6_full_middle_third_545/README.md),
source commit `62f24d4bda8b3eef15a18f2ec0b6a0bc09ee5c94`.

## Verdict and exact scope

**Confirmed with high confidence as a finite exclusion in the reflected-fibre
family.** Let \(A=\mathbb Z/109\mathbb Z\) and
\(I=\{37,\ldots,72\}\). There is no valid reflected-fibre six-colouring
of the punctured product \(A\times\mathbb Z/5\mathbb Z\) for which some
common fibre \(C_i\), \(i\in\{2,3,4,5\}\), equals \(kI\) for a unit
\(k\in A\) and the corresponding axis class \(E_i\) is empty. The other
axis classes and fibres are free within the construction; no value of
\(E(1)\) or fibre-asymmetry condition is imposed.

The equality \(C_i=kI\) is essential to the tested family. The result
does not exclude \(C_i\subseteq kI\), merely
\(C_i\cup(-C_i)=kI\), other reflected-fibre choices, or arbitrary
six-colourings of \([1,537]\). It proves no new bound on \(S(6)\).
A valid complete modular word at modulus 545 would instead give a
classical colouring through 544, improving the current
[536 lower bound](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32).

## Reduction and symmetry audit

The [reflected-fibre criterion](../schur_s6_reflected_fibres_review1/REVIEW.md)
requires every symmetric axis class \(E_j\) and every
\(B_j=C_j\cup(-C_j)\) to be sum-free, \(E_0\cup E_1\) to avoid
\(R-R\), and each common \(E_j\) to avoid \(C_j-C_j\).
A unit automorphism of \(A\) and a permutation of the four common labels
reduce any claimed counterexample to \(C_2=I\), \(E_2=\varnothing\).
The complement of \(I\) is \(\{0\}\cup\pm[1,36]\), so the remaining
first-fibre states are \(R,C_3,C_4,C_5\) there; zero lies in \(R\).

For \(j=3,4,5\), let \(P_j\subseteq[1,36]\) record which signed pairs
meet \(C_j\). Then \(B_j=\pm P_j\). Since \(3(36)=108<109\), a signed
modular Schur equation within \(\pm[1,36]\) cannot wrap; rearranging
signs makes it an ordinary positive equation in \(P_j\). My independent
enumeration confirmed that the 324 distinct signed supports and 324
ordinary supports coincide. The fixed middle third is itself symmetric
and modular sum-free.

The CNF's palette clauses put common labels 3,4,5 in order of first
occurrence across the fibre and axis states. Relabelling those three
colours globally within the common part always produces this order,
including when some are unused. The first axis occurrence of special
colour 0 or 1 can be made 0 by swapping \(E_0\) and \(E_1\) alone:
each is separately sum-free and only their union meets the \(R-R\)
condition. The two relabellings commute. Thus the 306 palette clauses
do not discard a valid construction. The source additionally checked
all 32,000 complete reduced assignments at \(a=7\); every one of its
2,988 valid assignments has a palette-normalized representative.

## Independent clause and witness checks

The source manifest passed `sha256sum -c SHA256SUMS`. I generated the
exact 666-variable, 20,574-clause CNF, then used my
[independent literal auditor](audit.py) to derive its variable numbering
and all 306 palette clauses separately. Removing those clauses and the
324 checked auxiliary OR-definition clauses, the auditor expands the
remaining support clauses into first-fibre literals. It also projects
every modular sum equation directly from the 545-word definition,
including all 544 doubling pairs. Mutual clause subsumption establishes
equivalence of the projected and expanded reduced constraints. The
108 additional projected clauses are redundant; no reduced clause is
left unmatched:

    PASS modulus=545 variables=666 clauses=20574 palette=306 pairs=147968 projected=26640 expanded=26532 subsumed_projected=108 subsumed_reduced=0

My checker also read both complete 234-entry control words, rebuilt their
CRT fibres, and checked every modular sum including doubling. The first
has \(C_2=\{16,\ldots,31\}\), \(E_2=\varnothing\), and class sizes
\(24,24,64,36,42,44\), showing the hypothesized shape is feasible at
the smaller factor 47. The second has \(E_5=\varnothing\), while its
\(C_5\) lies in no unit dilation of that factor's middle third
\(I_{47}=\{16,\ldots,31\}\). Its other three common supports lie in
\(I_{47},4I_{47},23I_{47}\). Both pass the independent
full-word check:

    PASS controls=2 endpoints=234,234 modular_sum_free=yes full_middle_third=yes noninterval_branch=yes

The source's separate full-word verifier passed both factor-47 controls;
its encoding audit passed at factors 7, 47, and 109. CaDiCaL 1.9.5
regenerated the 52,312,176-byte binary proof with SHA-256
`622c570d13299c138f8131877ef1445d564239fbb080fe76c3ff733ed8b8e4f5`.
DRAT-trim independently returned `s VERIFIED` for the CNF with SHA-256
`0b2b8adecfdd9f5f6e9144fcad75449ea9355e3afb6454beb873c3a8c6d55886`.
The tested tool source commits were CaDiCaL
`146207318796f094dcded87349a64f0c6927309e` and DRAT-trim
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, under CPython 3.11.2.
The proof is regenerated in temporary storage, not published as a large
file. The trust boundary is the finite reduction, palette-normalization
argument, literal-clause equivalence, and DRAT checker; the solver's
UNSAT status or matching hash alone is insufficient.

From the repository root, reproduce with:

    cd additive_combinatorics/schur6_full_middle_third_545
    sha256sum -c SHA256SUMS
    python3 -B verify.py
    python3 -B audit.py
    python3 -B model.py /tmp/schur-middle545.cnf
    python3 -B prove.py --cadical /path/to/cadical --drat-trim /path/to/drat-trim
    cd ../..
    python3 -B schur_s6_full_middle_third_545_review1/audit.py /tmp/schur-middle545.cnf

## Novelty and mathematical potential

The prior reflected-fibre review established the all-parameter
construction criterion and checked examples through 234. This new
certificate excludes a concrete, symmetric full-support candidate at
the potentially bound-improving factor 109. A targeted literature search
found no exact earlier exclusion for \(C_i=kI\), \(E_i=\varnothing\),
but does not establish historical priority. The
[July 2026 shifted-template paper](https://arxiv.org/abs/2607.15034)
still cites \(S(6)\ge536\); this conditional exclusion does not change
that numerical status.

The second control word shows a plausible structural escape from the
full-interval hypothesis at factor 47. Its analogue at factor 109 has
neither been constructed nor excluded by this certificate.

## Strengthening and improvement opportunities

The most consequential extension is to test factor 109 with a common
axis class empty but its fibre only *contained* in a unit dilation of
\(I\), or with \(C_i\cup(-C_i)=kI\). Either changes the fixed-fibre
reduction and requires a fresh complete encoding audit and checked proof.
Allowing a nonempty \(E_i\) would broaden the search further.

A constructive alternative is the noninterval branch represented by the
second 234-word: seek a valid factor-109 reflected word, then check every
integer sum through 544. An exclusion of the entire reflected family
would require covering those branches as well. Neither path yields a
global upper bound on \(S(6)\) without an argument covering colourings
outside the reflected construction.
