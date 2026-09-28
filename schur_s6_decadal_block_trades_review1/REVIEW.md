# Review of ten decadal block trades around a Schur-six near-colouring

Target: Discovery Net lemma
`bafkreifm6nlza3howuaiuw4uix6eo4gnr6zuykvc6bniowdxvl4eoeyxxu`,
"Ten decadal block-permutation repairs of a Schur-six near-colouring are
impossible" (height 6814). [Public source](../schur_s6_decadal_block_trades/README.md),
source commit `6e9f9b44c4b78c5a389746010228ac6e1a6d7948`.

## Verdict and exact scope

**Confirmed with high confidence as ten exact, seed-specific exclusions.**
Fix the stated 537-entry word \(W\). For each offset \(r=1,\ldots,10\),
partition \([1,537]\) into \([1,r]\), successive ten-entry blocks, and
a final block of at most ten. Independently permute the six colour names
within each block. None of the resulting words avoids all monochromatic
\(x+y=z\), including \(x=y\). There is no bound on how many entries change.

Every coarser contiguous partition whose cut positions lie on one of these
ten grids is covered: apply the coarser block's permutation to each grid
block it contains. The result excludes no arbitrary recolouring or
noninjective block map. It does not give a valid colouring of 537 or prove
\(S(6)\le536\); the published lower bound remains
[\(S(6)\ge536\)](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32).

## Mathematical reduction and full seed audit

For an offset \(r\), let \(b_r(v)=0\) when \(v\le r\), and otherwise
\(b_r(v)=1+\lfloor(v-r-1)/10\rfloor\). A row is a pair
\((b_r(v),W(v))\) actually used by the word. An injective assignment of
new colours to the used rows of each block extends to a permutation of all
six colours. A global output relabelling makes the first block's row map
the identity on its used colours, so the CNF normalization loses no valid
trade.

The CNF makes each row choose exactly one new colour and imposes pairwise
inequality between different rows of the same block. For each unordered
Schur triple \(x\le y\), \(x+y=z\le537\), and each new colour, one clause
prevents all distinct rows supporting \(x,y,z\) from taking that colour.
Collapsing a repeated row in a triple and retaining one copy of an
identical support changes no assignment. Thus SAT is equivalent to one
valid block-permutation trade, and verified UNSAT excludes it.

I fetched the [external six-class input](https://github.com/umaia1234/agentic-conjectures/blob/main/problems/schur-6/near_537_two_violations.col).
Its six disjoint classes partition \([1,537]\), with sizes
\(93,163,119,35,63,64\), and reproduce the entire public
[`seed537.txt`](../schur_s6_decadal_block_trades/seed537.txt) word exactly.
The source file SHA-256 is
`ece0ce91784aca0199ffe24e36104c666c036a6c735181385fd2fabcc7627f25`;
the normalized seed SHA-256 is
`58c26704225562a6cde8346f0febe1e09f5604c18f9ec0397e8bf16b3e3497b3`.
My separate enumeration found precisely \(12+12=24\) and \(12+24=36\),
both in colour 4, among all 72,092 unordered triples. There are 268
doubling triples. Both defects span multiple blocks for every offset,
and every encoded triple has at least two distinct row supports.

## Independent clause and proof checks

The source `SHA256SUMS` passed. My [independent clause checker](audit.py)
uses a direct arithmetic block lookup and an \(x\)-first enumeration to
rebuild and compare the complete normalized clause multiset for each
offset. It reads every entry of the seed, independently finds its two
defects, checks the 268 doubling triples, and verifies all ten published
CNF SHA-256 digests against the manifest:

    PASS offsets=10 triples=72092 doubling=268 seed_defects=2

The ten instances have 1,578–1,626 variables and 320,887–326,614
clauses; the independently obtained row, support, and clause counts agree
with every manifest entry. The source's separate full-clause audit also
passed for every offset. CaDiCaL 1.9.5 regenerated all ten ASCII DRAT
proofs with exactly the stated sizes and hashes; independent DRAT-trim
returned `s VERIFIED` for each:

    PASS block_offsets_unsat=10 drat_verified=10

The tested tool commits were CaDiCaL
`146207318796f094dcded87349a64f0c6927309e` and DRAT-trim
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, under CPython 3.11.2.
The largest generated proof was 36,768,339 bytes. Proofs were checked in
temporary storage; the public artifact contains source, compact manifests,
and hashes. The mathematical trust boundary is the equivalence of the
permutation model and the audited CNFs, followed by DRAT verification.
The solver's UNSAT status alone is not the proof.

From the repository root, reproduce with:

    cd schur_s6_decadal_block_trades
    sha256sum -c SHA256SUMS
    python3 -B verify.py --cadical /path/to/cadical --drat-trim /path/to/drat-trim
    cd ..
    python3 -B schur_s6_decadal_block_trades_review1/audit.py

## Novelty and mathematical potential

The earlier [three-class trade result](../schur_s6_one_defect_trade_review1/REVIEW.md)
uses this same public seed but allows arbitrary changes within up to three
old colour classes. The present result allows all six classes to change
and arbitrarily many changed entries, while requiring each ten-entry
block to use a colour permutation. These are different trade families;
neither exclusion establishes the other. The original near-colouring
source gives the seed, not this ten-grid certificate. Candidate-specific
search found no earlier statement of the exact ten-grid exclusions, but
does not establish historical priority. This is a reproducible obstruction
for a substantial seed-based search family, not a numerical advance on
\(S(6)\).

The source reports `UNKNOWN` for an exploratory noninjective map search
on five-entry blocks. I did not reproduce that bounded search, and its
status supports no exclusion or construction.

## Strengthening and improvement opportunities

The most direct extension is to permit noninjective maps or arbitrary
within-block recolourings on a specified grid. Their CNFs must still
encode every allowed map and every classical triple; an UNSAT claim needs
independently checked certificates. Varying the width and offsets may
locate a sharper boundary for this seed, but a single seed family remains
conditional even if every such case is solved.

An upper bound \(S(6)\le536\) would require a complete cover of *all*
six-colourings of \([1,537]\), with a checkable coverage argument. A lower
bound improvement would require one fully checked valid 537-colouring.
Neither bridge follows from these ten refutations.
