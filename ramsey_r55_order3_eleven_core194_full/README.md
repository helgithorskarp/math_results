# Guarded Core194 full-extension checkpoint

**Core194 remains unresolved.** The complete unrestricted 43-vertex formula,
strengthened by the derived attachment bound at all ten fixed vertices,
returned **UNKNOWN at the 20-second solver cap**. No full-core exclusion,
target graph or Ramsey bound improvement is established.

This checkpoint completes the planned propagation of the preceding
[Core194 maximal-branch theorem](../ramsey_r55_order3_eleven_core194_maximal)
into a full-core test. That theorem applies to any empty fixed vertex,
so the new formula uses its full quantified scope, beyond the previously
planned first-row-only tail. The result is a reproducible necessary
constraint system and a bounded inconclusive test, not an UNSAT certificate
or evidence of satisfiability. No other full core was tested here.

The boundary remains **17 full classes / 9,153 labeled cores**:

```text
92,97,118,119,124,155,164,168,180,182,185,186,190,191,192,193,194.
```

All have the previously derived first-empty-vertex bound b<=3. Cumulative
full exclusions stay 180/197 classes / 106,390 of 115,543 labels, importing
the earlier exclusion chain and its review boundaries. Core194's 81 labels
remain in the unresolved set. Its maximal b=4 attachment branch stays
excluded by the preceding result.

## The complete guarded strengthening

Write L(f,i) for a red link from fixed vertex f to moving cycle i, with
full primary index `211+11*(f-33)+i`. For each f=33,...,42 and each
four-subset S of the seven blue cycles, add

```
L(f,0) OR L(f,1) OR L(f,2) OR L(f,3) OR OR_(j in S) L(f,j).
```

A nonempty red-core signature satisfies these clauses automatically. An
empty signature activates the bound b<=3, equivalently at least four red
links to the seven blue cycles. No other fixed vertex is presumed empty.
The first row already has its four guard bits fixed blue by the inherited
base, so its clauses reduce to the earlier positive four-subset form.
The [proof](PROOF.md) explains why the prior theorem permits every fixed
vertex, rather than silently generalizing a first-row-only statement.

The complete tail has **350 positive eight-literal clauses / 11,900 bytes**.
There are no new auxiliary variables, fixed-edge units or normalizers.
Every complete base clause is retained. The input is the unrestricted
Core194 case from [empty-signature propagation](../ramsey_r55_order3_eleven_empty_propagation),
with canonical core word `100110110110110100`, multiplicity 81, and all
four intrinsic complementary anchors. It is neither the old b=4 child,
the 117-variable local classifier, nor the 216-variable fixed-neighborhood
full test; those would impose different hypotheses.

| Artifact | Variables | Clauses | Bytes | SHA256 |
|---|---:|---:|---:|---|
| Unrestricted full base | 34,320 | 617,582 | 24,956,496 | `2df3017147bd8cb5ceb6f561b8014a5b808e77db14fc6d9f3d6978b53d8c6490` |
| Full formula with ten guarded bounds | 34,320 | 617,932 | 24,968,396 | `f7f9eab7a28f32f56bebd54349db8a0e06010274bb16df9f90cbbb9b982216bf` |

## Verification and observed outcome

The isolated reconstruction regenerates the complete inherited parent and
preparation, compares the full prior preparation entry by entry, and
reconstructs the single unrestricted Core194 base. Other historical bases
and full-core solver cases are not repeated. The independent auditor
imports no producer, derives all 320 primary meanings from physical edge
orbits on 43 vertices, and checks every base byte, new clause and EOF.

Truth tables check 20,480 row assignments: all 2,048 patterns at each of
ten fixed vertices. Each row retains exactly 1,984 patterns, comprising
all 1,920 nonempty-signature patterns and 64 empty-signature patterns.
The degree bridge additionally checks 65,536 moving/fixed incidences for
an empty vertex and retains all 17,728 admissible complementary assignments.
Sixteen malformed inputs are rejected, including wrong base types, lost
guards, wrong signs and an unguarded bound at another fixed vertex.
Normal and optimized Python control reports agree.

The one Kissat run exited 0 with an explicit `s UNKNOWN` after 20.163771
seconds. Production, including complete preparation and controls, took
90.898757 seconds; its largest child maximum RSS was 261,676 KiB. The
configured cap describes the bounded attempt, not a runtime theorem.
The 26,032,940-byte partial trace has SHA256
`bedd05880b78cfe6db1a9cf39f73d46ee8b1736cbf85d59a0982a1300c47194c`.
It is **not a refutation or a saved solver state**. The inherited report
schema stores its identity under `proof`; the status is explicitly open,
and the number of completed proof replays is zero.

Fresh verification took 69.730746 seconds. It reconstructs the complete
base and strengthened formula again, repeats normal/optimized controls, matches all input identities,
and confirms the stored explicit UNKNOWN status. It does not repeat the
solver or treat a timeout as proof. All 110 transitive source identities
were frozen before production. Exact compact evidence is in
[result.json](result.json), [verification.json](verification.json),
[controls.json](controls.json), [cases.json](cases.json) and
[boundary.json](boundary.json).

## Reproduction and trust

Use CPython 3.11.2; inherited base reconstruction also uses GCC 12.2.0
(Debian 12.2.0-14+deb12u1). The pinned binaries are:

* Kissat 4.0.4, source `8af8e56f174b778aef3aa45af9f739b2a5f492c2`,
  binary SHA256 `2d185ea775f2c7c16d33a235ef852d2b69f0f3c8b437335b966b4a5aa6265b45`.
* drat-trim source `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`,
  binary SHA256 `9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.

Set R55_KISSAT and R55_DRAT to those executable paths. From the repository
root, using fresh directories outside the repository:

```bash
python3 -B ramsey_r55_order3_eleven_core194_full/run.py \
  --work /scratch/r55-core194-full/full \
  --kissat "$R55_KISSAT" --drat-trim "$R55_DRAT" \
  --solve-seconds 20 --replay-seconds 300
python3 -B ramsey_r55_order3_eleven_core194_full/verify.py \
  --source-work /scratch/r55-core194-full/full \
  --work /scratch/r55-core194-full/verification \
  --drat-trim "$R55_DRAT" --replay-seconds 300
python3 -B ramsey_r55_order3_eleven_core194_full/summarize.py \
  --source-work /scratch/r55-core194-full/full \
  --verification-work /scratch/r55-core194-full/verification \
  --output /scratch/r55-core194-full/boundary.json
```

The observed outcome is `open=[194]`, `excluded=[]`, zero proof replays.
Time-limited outcomes are machine-dependent. A later UNSAT run would need
a complete checked proof; a SAT target would need a literal edge-list check
on every five-set. The 300-second replay cap is available for an UNSAT
outcome and was unused in the observed run.

`--resume` checks the same source/tool/resource contract and stored
case/base/formula/trace identities. It preserves a completed UNKNOWN case
rather than silently starting a longer run. STOP prevents unstarted cases,
while active solve/replay units finish. No background process remains.
Large formulas, partial traces, logs and binaries stay outside Git.

The parent, core cover, intrinsic-anchor and forced-empty results have
accepted reviews at their stated scopes. The previous full Core159 result
now has [accepted independent review](../ramsey_r55_order3_eleven_core159_review1),
source `ea63f4e70350f661b5629ec2651249ba12ecc843`, graph
`bafkreif5r5x6lx5djdy6mfdf5ic6tlmv76ekrnxpkcatzogmq7pwmljfuu`.
The Core194 maximal-branch premise and this guarded propagation await
independent review. Older empty-signature-specific full closures retain
the cumulative-count review boundary. The degree window imports
R(4,5)=25 through the parent. Ordinary reductions, exact code, compiler,
interpreter/hardware and SHA256 remain trusted; a future refutation also
requires the full proof checker. Internal checking is not peer review
or formalization.

This bounded decision checkpoint is complete. It supplies no reason to
repeat the same cap or claim a completed core exclusion. A next distinct
full-extension direction is to check whether the independently accepted
local neighborhood obstructions for cores 124,155,168,180 also justify
guarded bounds at every empty fixed vertex, then test that stronger scope.
Such a transfer must establish the universal quantifier explicitly; bounds
known only for the first normalized row cannot be copied automatically.
No other core or larger cap is tested here.
