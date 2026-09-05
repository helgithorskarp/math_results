# The point-613 Parts extension is closed through 508

**Theorem.** Let V={0,...,508} be the original Parts coordinates, and let
P={509,...,584} be its 76 first-level completion points with at least seven
unit neighbours in V. Put q=613=(-5/6,sqrt(11)/6) and

    H=UD(V union P union {q}).

Every subgraph of H on at most 508 vertices is four-colourable. H has
586 vertices and 3,089 exact unit edges. Its minimum five-chromatic subgraph
order is exactly **509**, attained by V.

This is a negative closure of one specified support. It constructs no
record graph and does not close arbitrary degree-six additions or a
simultaneous union of the previously studied extra points.

## Reduction and complete certificate

The [previous exact reduction](../hadwiger_nelson_parts509_degree6_point613_residual/README.md),
source 152be34db209976d79b5506af7cd02f949892105, proves the following.
A possible non-four-colourable J subset H with at most 508 vertices contains
q and 451 fixed original vertices F. With R=(V union P) minus F, of size
134, its free selection X is a subset of R with:

- |X|=56;
- 13, 24, 129 and 518 absent;
- X meeting 335 witnessed inclusion-minimal killing sets, namely all 337
  old minimal sets except D245={129,518} and D316={13,24}.

The reduction is also enough to close every subgraph through 507. It uses
786 directly checked lifted four-colourings, the older degree-seven
hitting theorem, and the earlier small-augmentation closures. Its two
repair arguments first force the omissions and then the exact size 56.
Five and subsequently seven disjoint required pool groups imply at least
seven old pool points. These pool conditions are already consequences of
the 335 hitting rows, so the present formula needs no extra pool constraint.

The complete direct pseudo-Boolean instance [residual.opb](residual.opb)
uses one Boolean x_i for each element of the published sorted R. Its
340 constraints are exactly:

1. The 335 hitting constraints, each with all coefficients +1 and RHS 1.
2. Four omission constraints -x_i>=0.
3. The budget -sum(x_i)>=-56.

The last budget is deliberately at most 56, a relaxation of the necessary
equality. There is no symmetry restriction, degree hypothesis or extra
geometric assumption. The source regenerates each row and separately
decodes it against the previous selector's metadata. After existentially
quantifying that selector's threshold variables, the OPB and the previous
CNF describe the same assignments to the 134 primary variables.

The [8,372-byte proof](closure.pb) refutes these 340 constraints.
**VeriPB 3.0.2 accepts it as UNSATISFIABLE.** Thus no X as above exists,
proving the closure through 508. The original Parts graph gives the
matching upper bound 509. The verifier also rechecks a proper five-colouring
of the full H.

Canonical identities:

| Artifact | SHA-256 |
|---|---|
| OPB, 13,455 bytes | 060ff2f0e3bb5c7cf904f6f3e064c2d301e6cf6f98d7582288f5e01ab65d3778 |
| Complete compact proof, 8,372 bytes | 51ff373e47a42fa8dc0f5b2d5bc7e493775d86843e2e43774585e2c7048a71be |
| Equivalent prior CNF | ec62944dd2b05b7b847038ff4f0f7ccd0fb9e470f6d670423c5ac39f0c90a948 |

## What the minimum-degree pilot established

The inherited order-508 boundary makes a possible obstruction
vertex-critical, hence of minimum degree at least four. An exact audit
found that all degree conditions reduce, under the proved fixed literals,
to a single clause x_14 OR x_126, where subscripts here are vertex labels.

There are 461 already selected vertices, four omitted vertices and 121
optional vertices. Of the 582 nonomitted vertices, 580 already have at
least four fixed selected neighbours. The only exceptions are:

| Vertex | Fixed neighbours | Optional neighbours | Requirement |
|---|---|---|---|
| 184, selected | {125,148,155} | {14,126} | retain 14 or 126 |
| 185, optional | {127,156,163} | {14,15,126} | if retained, retain at least one |

The first requirement implies the second. It is not implied by the
monotone hitting rows alone: selecting every allowed free vertex except
14 and 126 meets those rows and leaves vertex 184 at degree three. That
128-free-vertex assignment violates the budget and is not a model of the
full residual.

One bounded native query used the OPB instance with this additional degree
clause. RoundingSat 2 returned UNSAT after 0.254 wall seconds, producing a
471,082-byte complete proof, independently accepted by VeriPB. Dependency
slicing retained 27 proof constraints in 23 top-level blocks, including
one redundancy subproof.

**The retained proof never references the degree clause.** Removing the
unused input constraint and renumbering the derivation gives the committed
8,372-byte certificate of the original 340-constraint residual. VeriPB
accepted this stronger certificate too. The closure therefore requires
no added degree assumption. No second native query was run.

The earlier 300-second threshold-CNF timeout is mathematically superseded,
not extended. Both the representation and the initial pilot formula
changed, and the final proof establishes the stronger original claim.

## Reproduce

Use Python 3.11 or later and VeriPB 3.0.2, source commit
c648bac06be995b82bd218e248f005140fc8ce11. In a full checkout, from this
directory:

    python3 verify.py --veripb /path/to/veripb
    python3 controls.py --veripb /path/to/veripb
    sha256sum -c SHA256SUMS

For certificate checking alone:

    /path/to/veripb residual.opb closure.pb

Expected result: CLOSED THROUGH 508; MINIMUM FIVE-CHROMATIC SUBGRAPH ORDER 509.
The checker replays all 786 inherited four-colour witnesses on 2,410,698
retained edges, reconstructs the OPB, and checks the complete proof.
A separate coordinate-dictionary parse and exhaustive pair scan reproduce
the prior exact edge digest and the degree audit; this shares the reviewed
integer field routine and is not a claim of independent external review.

Controls evaluate 16 assignments of the four locally relevant optional
vertices with two choices for all other optional vertices, giving 32
degree cases and 16,688 direct vertex-degree checks. They verify the
monotone counterexample's exact limited scope. VeriPB rejects both a false
UNSAT claim for a satisfiable one-variable formula and a modified real
proof whose stated conclusion is a tautology.

Optional regeneration of the recorded native run uses RoundingSat 2 at
d4edbf7908a9bb951fd181940919e0f3ac7ab1ee:

    python3 encoding.py --out /scratch/fresh-degree.opb --with-degree
    /path/to/roundingsat /scratch/fresh-degree.opb --time-limit=300 \
      --print-sol=1 --proof-log=/scratch/fresh-degree.pb

The run used one worker and a 4 GiB Linux address-space limit.
The original proof's SHA-256 is
79a0ee677663e2ed78dde76df5704c729fc1995bf7c6aa7b8518ffcdf1f12810.
It remains local; the compact complete proof is sufficient for checking.

For that pinned native trace, the exact extraction is:

    python3 extract.py --input /scratch/fresh-degree.pb --output /scratch/extracted.pb
    cmp closure.pb /scratch/extracted.pb

The extractor refuses a different input hash. Native proof details may
vary with a different solver or LP build; any resulting proof must be
checked independently. The extractor itself is not trusted for soundness:
the resulting complete certificate is checked by VeriPB.

## Trust boundary and disposition

The old degree-seven hitting theorem, the small-augmentation closures and
original Parts five-chromaticity remain imported premises. The matching
old bound was freshly verified in the
[independent point-610 review](../hadwiger_nelson_parts509_degree7_extension610_closure_review1/README.md);
its large proof was not replayed in this pass. The new compact proof is
fully checked here. Solver floating-point LP work supplies discovery
information only; exact integer proof checking establishes infeasibility.

Remaining trust is in the pinned inputs and imported theorems, the
ordinary reduction argument, Python integer arithmetic, SHA-256 and VeriPB.
This is not a proof-assistant formalization or a new external review.

The fixed point-613 support is finished for the <=508 objective. No
additional colouring query, other support, or subsequent family pilot
was started. The teammate's latest dense506 two-arbitrary-point theorem
concerns distinct geometric supports and does not overlap this closure.
