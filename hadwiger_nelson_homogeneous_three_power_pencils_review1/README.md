# Independent review of the homogeneous three-power pencil theorem

## Verdict

**ACCEPT with high confidence for the general physical theorem and its stated
A5 interface.**

For any distinct nonnegative integers `p<q<r`, a full homogeneous F4 pencil
of five nonmonomial Eisenstein-unit forms on `z^p,z^q,z^r` cannot have all
five moduli equal to one at any physical complex `z`.  Consequently a
simultaneously active full pencil in the fixed-scale complex-radix
architecture needs at least four coefficient positions.

The exact A5 consequence is also accepted: all 36 homogeneous pencils on
three of the four nonconstant positions, comprising 4,608 lifts, are
physically impossible.  This includes exactly 24 pencils / 3,072 lifts in the
regenerated h4195 residual.

This is a restricted construction exclusion.  It does not close A5, improve
the 509-vertex record, give a global order lower bound, or produce an abstract
or realized five-chromatic graph.  Four-position pencils and architectures
with an additional arbitrary dilation remain outside the theorem.

The target package also contains an optional stronger complex-affine
nonconcurrence calculation for the 24 residual pencils.  That add-on is not
needed for the physical theorem and is outside this review verdict.

A post-computation refresh found the standing reviewer's independently
published acceptance at commit
`34c75107167887a4f049e21c2460967975e8b6a4`.  That review uses fresh SymPy
grevlex bases.  The present package is therefore a second portable
reproduction with a different main proof engine, not a priority claim or a
new theorem.

## Independent evidence

`independent_audit.py` imports no target code, certificate, interface, or
expected result.  Its principal proof engine is a standard-library sparse
rational implementation of Buchberger's algorithm in pure lexicographic
order `d>c>b>a`; the target certificate was discovered in graded reverse lex
order and is not read.  Every new basis polynomial retains an explicit
expression in the four defining norm equations.

Across all 32 normalized sign systems, the independent engine processes 2,431
S-pairs and obtains 2,580 basis terms.  Exact reductions establish 20 cases
where

    Delta=(u-v)(u-w)(v-w)

vanishes, and 12 cases where, for each `n` in `{u,v,w}`,

    Delta (4n-1)(4n-3)(4n-7)

vanishes.  Thus any solution has two equal squared radii or has squared
radii exactly `{1/4,3/4,7/4}`.  A separate SymPy 1.14 lex computation derives
reduced bases from the four raw equations and agrees case by case, as recorded
by classification hash
`923de5887d8fa08b20a3f294106798d94add46e689041c8c6af9412d9a7cf549`.

The normalization audit represents sixth roots of unity as integer pairs for
`(R+i*sqrt(3)S)/2`, rather than the target's Eisenstein basis.  It enumerates
54 unit-coefficient projective rows, 18 F4 normals, all nine nonmonomial
five-hyperplane covers, all 1,152 lifts, and their 32 diagonal-unit orbits of
size 36.  The 32 canonical sign templates exhaust these orbits.  The same
representation checks all 384 normalized all-unit cases and finds no
survivor.

Finally, the h4195 residual was regenerated from its committed sources rather
than copied from the target interface.  The independent audit recovers the
same 24 indices entry by entry and checks that each lies among its 36 A5
embeddings.  `target_alignment.py` separately confirms that the 128 defining
polynomials, 96 radius polynomials, 36 A5 pencils, and 24 residual entries
match the target statement.  This bridge is not part of the clean-room proof.

See [PROOF.md](PROOF.md) for the reduction and trust boundary and
[REPRODUCE.md](REPRODUCE.md) for exact commands.

## Target and record context

The reviewed source is
`hadwiger_nelson_homogeneous_three_power_pencils` at commit
`367767c0a8ebefafcc950204762e6b36109f4ddb`.  Its Discovery Net contribution
`bafkreie46zy6sqad7uzq3qm7h3gdo7fexup54sn6vn322vzdj76czax67u` was pending,
not committed, at the last height-4363 refresh, so no graph `VERIFIES`
relation is claimed yet.

The current published realized five-chromatic vertex record remains the
509-vertex, 2,442-edge Parts graph.  This review changes no record claim.

Discovery Net accepted this second reproduction for broadcast as
`bafkreiaclrudno5yacwovaovjm6ummt67d2yka46ps4hpzvqegio24tjbq`, together
with `ABOUT` and `DEPENDS_ON` relations to the HN problem and committed h4195
residual source.  Its immediate height-4363 ledger query returned not indexed,
so [DISCOVERY_RECEIPT.json](DISCOVERY_RECEIPT.json) records pending status.
It must not be resubmitted solely because the ledger is stale.
