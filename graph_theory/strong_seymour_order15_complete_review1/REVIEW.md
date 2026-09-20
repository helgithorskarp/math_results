# Independent review: strong Seymour vertices through order 15

Review date: 2026-09-20 UTC

Target graph artifact:
`bafkreihvquktzhgyzkw56zsrbiontqntiojahwfqio6ggtghve7r3iqwcm`

Target source commit: `4732727080e36e62be2d35ea819db0ca7e83b9a7`

## Verdict

**Accept, high confidence, with one minor documentation correction.**  The
order-15 theorem is supported by a complete human reduction and exact checked
UNSAT certificates.  The statement for all orders at most 15 additionally
depends on the previously accepted order-at-most-14 result.  I found no omitted
order-15 case, unsafe symmetry, CNF polarity error, or failed certificate.

The documentation should not say that the auxiliary variables literally
encode every proper-subset condition of an inclusion-minimal Hall witness.
They encode an exact deficient set with deficiency one, double coverage, and,
where applicable, the Bai--Li--Park internal-degree consequence.  These are
necessary consequences of a genuine minimal witness but not sufficient for
literal minimality: the smallest counterexample has `|S|=3` and link row masks
`[3,3,0]`.  This is a harmless relaxation.  Every true nonstrong vertex has a
genuine minimal witness satisfying the encoded clauses, while every encoded
selected set is still Hall-deficient.  Thus the UNSAT argument remains sound.

## Human premises audited

1. **Definition and Hall translation.**  In a tournament, the exact second
   out-neighborhood of `x` is precisely the set of in-neighbors of `x` reached
   by an arc from `N+(x)`.  A strong Seymour matching is therefore a matching
   in this bipartite link, and Hall's theorem gives the displayed deficient-set
   criterion.  An augmenting-path matcher and direct Hall enumeration agree in
   every one of 202,013 vertex cases through order six.

2. **Existence of an ordinary root.**  The proof uses the theorem that every
   tournament has an ordinary Seymour vertex.  This is an external theorem,
   not a consequence of the SAT computation; Bai--Li--Park cite Fisher's proof
   of Dean's conjecture and the later median-order proof.

3. **Minimum-degree premise.**  Bai--Li--Park Theorem 1.5 states that an
   oriented graph with minimum out-degree at most five has a strong Seymour
   vertex.  Hence a hypothetical counterexample here has minimum out-degree at
   least six.  Their Lemma 2.5 gives positive internal out-degree for a minimal
   witness only when the root has minimum out-degree.  The encoder gates this
   condition to degree-six vertices (and to every vertex in regular mode),
   exactly where that hypothesis is available.

4. **Root-degree frontier.**  For an ordinary vertex in an order-15 tournament,
   `d+(x) <= |N++(x)| <= 14-d+(x)`, so its degree is at most seven.  The
   minimum-degree theorem leaves degrees six and seven.  Six regenerated
   frontier formulas exclude an ordinary degree-six root and a regular
   counterexample; the regular size-six witness has the direct two-vertex
   contradiction stated in the source.  Thus the remaining root has degree
   seven and both shores have size seven.

5. **Minimal-witness consequences.**  Choosing an actually inclusion-minimal
   deficient set gives `|Gamma(S)|=|S|-1`: deleting any member leaves a
   nondeficient set whose neighbor set is contained in `Gamma(S)`.  Every Hall
   neighbor has at least two predecessors, since a unique predecessor could be
   deleted to retain a deficiency.  The independent checker verifies these
   implications for all 248,660 minimal witnesses through order six.  It also
   explicitly exhibits why the converse of double coverage is not being used.

6. **Witness-size chain.**  At a degree-seven ordinary root, `S=A` cannot be
   deficient because `Gamma(A)=N++(x)=B`; hence `|S|<=6`.  Sizes one and two
   force an ordinary degree-six vertex directly.  Size three reduces to a
   directed triangle dominating both Hall neighbors, whose exact DRAT trace
   checks.  The size-four census covers all 262,144 local orientations, leaving
   472 patterns in ten relabeling orbits.  The size-five split covers one tight
   case and all eight five-tournament types of positive minimum out-degree.
   Their certificates all check.  Consequently size six is genuinely the only
   remaining branch.

7. **Size-six partition.**  For `|S|=6`, deficiency one gives `|R|=5`; the two
   seven-vertex shores then give `|C|=1` and `|D|=2`, with `D->S`.  Because the
   root is ordinary, `N++(x)=B`; members of `D` cannot be reached from `S`, so
   the sole member of `C` must dominate both.  No coverage condition has been
   omitted.

8. **Local inequality and exhaustive split.**  A witness vertex can send arcs
   only into `S`, `R`, and the single member of `C`.  Minimum degree six gives
   `p(v)+q(v)>=5`.  If equality occurs, one such vertex can be labelled 1 and
   `p(1)=0,...,5` gives exactly six cases.  If it never occurs, every
   `p(v)+q(v)>=6`; since `q(v)<=5`, all six internal scores are positive.
   Direct enumeration recovers exactly the thirteen stated score sequences and
   their 26,624 labelled realizations.  The two branches are disjoint and
   exhaustive.

9. **Score signatures and symmetry.**  A strict formula fixes internal degrees,
   not one tournament representative, so all realizations of a score sequence
   remain.  Sorting by score is legitimate.  Within each equal-score block the
   vertices obey identical remaining constraints, so any directed edge can be
   moved to the normalized pair.  The same argument applies to the five
   unlabelled witness vertices in a tight case and independently to `R` and
   `D`.  All 26,624 positive-score six-tournaments pass this normalization
   check.

10. **Base encoder.**  I inspected every clause family.  One variable per
    unordered pair has the stated polarity.  Sequential counters give exact
    degree-seven/eight threshold flags and global minimum degree six.  Product
    variables are exact conjunctions of selection and an arc; neighbor
    variables are exact on the root's in-shore.  The cardinality equation is
    algebraically `|Gamma(S)|=|S|-1`.  Double coverage and the gated internal
    outdegree condition have the correct polarities.  Degree-at-least-eight
    vertices are automatically nonstrong because their in-shore has at most
    six vertices.  The bound of at most seven such vertices follows safely from
    the degree-sum excess.  Fixed-tournament SAT probes agreed with direct Hall
    enumeration on 144 adversarial degree-six/seven roots, including both
    strong and nonstrong roots.

11. **Case extensions.**  The final generator adds only `C->D`, exact tight or
    strict signature counters, and the audited symmetries.  Its local literals
    count precisely the five internal and five `S->R` arcs.  End cases
    `p=0,q=5` and `p=5,q=0` are present.  No unencoded `S`--`R` pattern or
    six-tournament type is assumed away.

12. **Certificate implication.**  `drat-trim` proves UNSAT for each exact
    hashed CNF, not for an informal theorem.  Because the human reductions map
    every hypothetical counterexample into at least one formula and the
    formulas may only relax literal witness minimality, all formulas being
    UNSAT contradicts the hypothetical counterexample.

13. **Bounds on the minimum counterexample order.**  The new proof gives the
    lower bound 16 after combining with the accepted order-14 theorem.  The
    upper bound 36 is explicitly supplied by the transitive-fiber tournament
    in Bai--Li--Park Remark 3.1.  These two dependencies are separate from the
    new order-15 exclusion.

## Completeness reductions checked

- orders at most 14 versus exactly 15;
- ordinary root degree six versus degree seven, and regular versus nonregular;
- minimal witness sizes one through six, with size seven ruled out by
  ordinaryness;
- equality at a witness vertex versus strict inequality at every witness
  vertex;
- every tight score `0,...,5` and every positive six-tournament score sequence;
- all labelled local patterns at size four and all isomorphism types at size
  five;
- every degree class six, seven, and at least eight in the all-vertex encoder;
- ordinary-root coverage of all vertices in `D`;
- relabeling within the chosen tight vertex complement, equal-score blocks,
  `C`, `R`, and `D`;
- formula generation, solver output, proof checking, and manifest comparison;
  and
- the exact order-15 theorem versus the corollary through order 15 and the
  separate 36-vertex upper bound.

No case remains outside the checked formulas under the stated external
theorems.

## Adversarial finite checks

The independent standard-library `audit.py` does not import the target code.

- It enumerates all 33,867 labelled tournaments through order six, checking
  Hall against matching, strong and ordinary vertices, and 248,660 minimal
  Hall witnesses.
- It enumerates every abstract `S`--`R` link for `|S|<=4`.  This finds the
  smallest nonminimal set satisfying the encoder's necessary consequences,
  `|S|=3` with rows `[3,3,0]`, confirming both the documentation caveat and the
  safe direction of the relaxation.
- A separately implemented size-four orbit action gives 22,368 feasible local
  patterns, 21,896 forced-ordinary patterns, and ten survivor orbits of total
  size 472.
- Independent canonicalization of all 1,024 five-tournaments gives the same
  eight strict types and 704 labelled realizations.
- All 32,768 six-tournaments give the same thirteen positive score sequences,
  labelled counts, and sequence digest.

`encoding_probe.py` imports the target encoder only as the object under test.
It fixes complete tournaments and compares SAT with an independent Hall
oracle.  The sample contains 48 minimum-degree-six roots (24 strong, 24
nonstrong), 48 random degree-seven roots (44 strong, 4 nonstrong), and 48
forced nonstrong degree-seven roots covering witness sizes one through six.
All 144 agree.  Exact threshold flags are also forced correctly for every
root degree zero through fourteen.

## Exact certificate replay

I used CaDiCaL 3.0.1 at commit
`c60730422e758ef1cebe7aeddf2dda31c996bf04` and `drat-trim` at commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.

- The six older frontier CNFs were freshly regenerated.  Every CNF and newly
  generated DRAT file reproduced its published SHA-256 exactly, and every
  trace checked (`90,080,658` proof bytes).
- The size-three rigid trace checked (`2,527,866` bytes).
- All ten size-four traces checked with manifest
  `4bdfd9d33ecac18c36224720177c391d2153a38c0d328d81771b173da804a829`
  (`22,674,389` bytes).
- All nine size-five traces checked with manifest
  `0358a8f0b7280141575039a7a5b6a6827121695ff242f788300ba44bb9034e13`
  (`88,525,488` bytes).
- The 19 final CNFs were regenerated with the published hashes, and all 19
  traces checked with manifest
  `41cc552e669658832e5e4010e813f75ee173c3334097dfc70cf1e35e0c2cae4e`
  (`733,799,202` bytes).

This is 45 checked formulas and 937,607,603 proof bytes across the complete
order-15 chain.  Program agreement is corroboration; the premise and
completeness audit above is what connects those formulas to the theorem.

## Literature and source integrity

- Bai, Li, and Park, *Towards a strengthening of the second neighborhood
  conjecture*, arXiv:2607.18047v2, states the minimum-outdegree theorem,
  Lemma 2.5, the tournament ordinary-Seymour background, and the 36-vertex
  counterexample: <https://arxiv.org/abs/2607.18047v2>.
- Austin Gibbons's independent `ssnc` project remained at commit
  `cbed58e369cfd868a84010f252671cc3c766c6fd` dated 2026-07-23 during this
  review: <https://github.com/AustinBGibbons/ssnc>.  It provides regular
  tournaments with a controlled set of strong vertices, not an order-15
  counterexample or universal proof.

The arXiv API still reported version 2, updated 2026-07-24, on the review date.
A bounded graph refresh and live primary-source search found no earlier
order-15 theorem.  That supports the target's search-relative novelty wording;
it does not establish historical priority.

The target source manifest passes.  The imported base generator has SHA-256
`5dda45c3e5e9aeeb286bfa6844e911bf8d9cb47918e2cf21f0fb00e2482d0517`.
The public repository intentionally omits the 938 MB of generated proof traces;
the compact source, exact hashes, and reproduction commands are present, and
the campaign copies were preserved under `/scratch`.

## Caveats

- Replace descriptions of the selected auxiliary witness as literally
  inclusion-minimal by “a deficient witness satisfying the necessary
  minimal-witness consequences,” or explicitly call this a safe relaxation.
- The proof trusts the cited ordinary-Seymour and Bai--Li--Park theorems,
  PySAT's sequential counters, CaDiCaL, and `drat-trim`; it is not a formal
  proof-assistant development.
- The public repository contains hashes and generators rather than the large
  DRAT files.  Rechecking from source therefore requires the stated external
  tool commits and substantial generated scratch space.
- Acceptance covers correctness and stated scope, not historical priority.
