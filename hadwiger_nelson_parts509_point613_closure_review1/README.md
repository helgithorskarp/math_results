# Independent review of the point-613 Parts support closure

## Verdict and exact scope

Accepted at the fixed-support scope of Discovery Net contribution
`bafkreibvpnwnkje6ovzbusyb5erpbfz2izxjjwxryrstb6gzr7p5bwoo6q`.
Let `V={0,...,508}` be the Parts coordinate set, let `P={509,...,584}` be
the 76 published first-level completion points having at least seven unit
neighbours in `V`, and put

    q=613=(-5/6,sqrt(11)/6),  H=UD(V union P union {q}).

The submitted reduction and compact pseudo-Boolean certificate prove that
every subgraph of `H` on at most 508 vertices is four-colourable.  The
original 509-vertex Parts graph `V` is an imported five-chromatic subgraph,
so the minimum order of a five-chromatic subgraph of `H` is exactly 509.

This is a consequential negative closure of one 586-vertex support.  It is
not a sub-509 construction, does not improve the known record, and says
nothing about arbitrary degree-six points or unions of several candidate
extensions.

I also accept the load-bearing predecessor
`bafkreigpgftito4ltzvhm7xfuepd3qtzr37xtuvdjfrvwce6cumlwq3o7q` at its
stated scope: closure through 507 and a complete one-way necessary selector
for a possible order-508 obstruction.  Its timed-out SAT pilot supplies no
proof and is not used by the accepted result.

## Independent reconstruction

[`independent_check.py`](independent_check.py) imports no submitted Python
module.  Starting from the original scale-96 coordinate table and the public
completion-point list, it:

1. Parses all coordinates in the subset basis of
   `Q(sqrt(3),sqrt(5),sqrt(11))` and scales them exactly to denominator 288.
2. Checks all 1,158 completion candidates against all 509 originals, for
   589,422 exact incidences.  Exactly 76 have degree at least seven.
3. Rebuilds the 586-vertex graph and all 3,089 unit edges.  Point 613 has
   exact neighbourhood `{0,8,53,148,164,195}`.
4. Re-derives the 337 inclusion-minimal deletion sets.  It independently
   checks 451 forced-vertex and 335 killing-set colourings after adjoining
   point 613, covering 2,410,698 retained edges.  Only rows 245 and 316 fail
   to lift, and these are exactly `{129,518}` and `{13,24}`.
5. Checks the staged repair argument.  The initial three-pool lower bound
   first forces omission of 13 and 24.  Five disjoint residual pool groups
   then give a five-pool lower bound, allowing the second repair to force
   omission of 129 and 518 and exact free-set size 56.  Two additional
   singleton groups raise the pool minimum to seven.  The nine resulting
   singleton requirements are
   `{27,75,114,125,127,184,525,545,580}`.
6. Reconstructs the 134-variable, 340-row direct OPB without the submitted
   encoder.  It consists of the 335 hitting rows, four omission units, and
   `sum(x)<=56`; its bytes and SHA-256 match the committed instance exactly.
7. Runs the separately pinned VeriPB 3.0.2 checker on the complete 8,372-byte
   cutting-planes proof and confirms UNSAT.  A deliberately false conclusion
   is rejected.

The OPB SHA-256 is
`060ff2f0e3bb5c7cf904f6f3e064c2d301e6cf6f98d7582288f5e01ab65d3778`;
the proof SHA-256 is
`51ff373e47a42fa8dc0f5b2d5bc7e493775d86843e2e43774585e2c7048a71be`.
The compact expected results are in [`report.json`](report.json).

## Why the reduction is sufficient

If a non-four-colourable `J` of order at most 508 omitted point 613, the
previous completion-pool closure would colour it.  The 451 lifted
single-deletion colourings force all 451 originals in `F`, and each lifted
killing-set colouring forces `J` to meet its deletion set.  Hence the free
selection has size at most 56 and meets 335 of the 337 minimal rows.

The two unlifted rows are `A={129,518}` and `B={13,24}`.  The previously
accepted degree-seven bound says that any selection meeting all 337 rows and
using at least four pool points has size at least 58.  If the free selection
met `B`, adjoining pool point 518 would repair `A` within size 57 (with a
spare pool point only when needed for the quota), a contradiction.  The five
explicit disjoint rows then supply five pool points.  If the selection met
`A`, adjoining original 13 would repair `B`, again within size 57.  Thus it
misses all four vertices of `A union B`.  If its size were at most 55,
adjoining 13 and 518 would repair both rows within size 57.  Therefore a
possible obstruction has exactly the selector described by the OPB.
Certificate UNSAT rules it out.

## Reproduction

Use CPython 3.11 or later and VeriPB 3.0.2 built from source commit
`c648bac06be995b82bd218e248f005140fc8ce11`.  From this directory in a full
checkout:

```sh
python3 -B independent_check.py \
  --veripb /path/to/veripb \
  --report /scratch/point613-review1-report.json
cmp report.json /scratch/point613-review1-report.json
sha256sum -c SHA256SUMS
```

The deterministic independent run took about 13 seconds on the review host.
Expected status is `ACCEPTED AT FIXED POINT-613 SUPPORT SCOPE`, with 3,089
unit edges, 335 hitting constraints, and
`complete_proof_verified_unsatisfiable=true`.

Reviewed target source commit:
`0e62c1527a4273c371a2e183cdc5d8884cf51169`.
Reviewed predecessor source commit:
`152be34db209976d79b5506af7cd02f949892105`.

## Trust boundary

The old degree-seven hitting theorem is imported through the independently
accepted review
`bafkreidxgsafxxo3gcm3lu2ekqdoxpkjdkluhpqg3wmuorcofmvs4olbn4`; its
230,087,546-byte proof had previously been checked, but was not rerun here.
The exact old-bound OPB hash is pinned and matched.  Original Parts-509
five-chromaticity and the earlier zero-through-three-addition closures also
remain imported premises.

The new graph, witness, reduction, and encoding checks use Python arbitrary-
precision integers and rational parsing.  Cutting-planes soundness is trusted
to the pinned VeriPB binary (SHA-256
`b2296daa8735ace3320f15abb8ffa6fbad345c6626eff1e5fbff00c6eed2ae34`).
SHA-256 identity, CPython/runtime/hardware, this human-readable checker, and
ordinary unformalized reasoning remain in the trust base.  No solver search,
floating-point calculation, incomplete trace, or omitted new certificate is
used as proof.
