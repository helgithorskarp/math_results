# Core194's maximal attachment branch is excluded

**Core194 cannot occur with an empty fixed vertex blue to four internally
blue moving triangles** in a Ramsey(5,5;43) graph with action `1^10 3^11`
and a four-red/seven-blue moving-triangle split. This closes the last
remaining maximal `b=4` attachment branch. It represents **81 labeled
minority cores**, importing the established core cover.

The proof crosses from a complete local-family classification to an exact
**43-vertex extension refutation**. The local family has exactly **7,776
labeled graphs**, four canonical representatives, and one isomorphism type
under transformations commuting with the order-three action. Every member
is red 13-regular. None extends in the stated maximal attachment branch.
The local count fixes the canonical eighteen core bits; it is distinct
from the inherited count of 81 labeled minority cores.

This is **not a whole-Core194 exclusion**. The full boundary remains
**17 classes / 9,153 labels**, with cumulative full exclusions
180/197 classes / 106,390 of 115,543 labels and their imported review
boundaries. Every remaining full class now has `b<=3` for the first
normalized empty fixed vertex. No target graph or Ramsey bound improvement
is claimed. The new theorem and certificates await independent review.

## Classification followed by full extension

At `b=4`, the degree window gives `d_red(e)=18`, `d_blue(e)=24`. The blue
neighborhood H of e comprises four red and four blue moving triangles;
it has no red K5 or blue K4. Its twelve-vertex red core is Core194,
word `100110110110110100`, in pair order 01,02,03,12,13,23 and phase
order 0,1,2. The [preceding local witness](../ramsey_r55_order3_eleven_neighborhood24/c194.edges)
for this condition has an [accepted independent review](../ramsey_r55_order3_eleven_neighborhood24_review1).

For each blue cycle, form its twelve-bit contact word against the red
core. Independently choose its least cyclic phase, then sort the four
contact words. These are complete relabelings; they leave the red core
pointwise fixed and commute with the order-three generator. No full-graph
normalizer is imported. The [proof](PROOF.md) treats ties and the exact
prefix-equality auxiliary extension.

The normalized local formula has just four primary models, listed with
explicit pullback permutations in [representatives.json](representatives.json):

```text
7ddf8dd2a8c94eb7b48d9
7ddfaa8cdd094eb7b48d9
bf5fa5caa5498f37b48d9
bf5faa565c898f37b48d9
```

Bit `v-1` is primary v, in the phase order above on all pairs of eight
cycles. Each model is a checked image of the known witness. A complete
DRAT refutation after blocking exactly these four models proves coverage.
The independent checker also enumerates four disjoint, free blue-cycle
group orbits, each of size `4!*3^4=1,944`. Their union has 7,776 words.

For the full test, fix that witness on vertices 0..23. Add three internally
blue cycles on 24..32, the distinguished fixed e=33, and nine fixed vertices
34..42. Vertex e is blue to H and red to every vertex outside H. All other
incidences are free subject only to order-three invariance and the absence
of either color K5. There are **no degree constraints, auxiliary variables,
row orders, phase orders or inherited full normalizers** in this formula.
It is a complete 43-vertex test, not a test of selected added vertices.

Every classified H transforms to the witness by a permutation commuting
with the generator and preserving the red/blue cycle parts. Extending that
permutation by the identity on the nineteen other vertices preserves the
full test's hypotheses. Its refutation therefore excludes the entire
maximal branch, rather than just one arbitrarily fixed neighborhood.

## Exact evidence

| Formula | Variables | Clauses | Bytes | SHA256 |
|---|---:|---:|---:|---|
| Local classification with four blockers | 117 | 22,666 | 872,272 | `4702868099d8670de2bf989e0c87573ac22437adae6dd887dddb9693d6711eee` |
| Complete fixed-neighborhood extension | 216 | 131,652 | 4,904,963 | `847412ca901bafa697deca4011e5e21e68448c5b403bc473095436d93ff16f8d` |

The classifier consists of the exact 84-primary/11,584-clause local
Ramsey/core base, 10,880 phase clauses, 198 ordering/definition clauses
with 33 prefix-equality auxiliaries, and four full-primary blockers.
The complete extension has 216 primary variables and no auxiliaries.

| Complete proof | Bytes | SHA256 |
|---|---:|---|
| Classification | 464,641 | `f1ec8b1b91feead05e56f04b066a17d9b5244ee0bda444dc893a2a995182a0ff` |
| Extension | 3,333,578 | `8f724078ce768c89ab2a41267097020b33a2a3578f497b4fa0b802b8a559c7a3` |

Both proofs passed full DRAT replay twice, with zero RAT core lemmas in
all four replays. The checker used its full mode. Production took
55.080570 seconds, including controls; fresh verification took 11.004580
seconds. Solver times were 0.131611 and 2.623299 seconds. Production's
largest child maximum RSS was 256,932 KiB; fresh verification's was
76,872 KiB. The two-worker run used 60-second solver caps and 300-second
replay caps; these are experimental resources, not runtime theorems.

The independent auditor imports no producer. It enumerates physical pair
orbits and reconstructs clique clauses by possible-color clique recursion,
compares every clause and the exact EOF, verifies every representative's
literal pullback, and checks the local clique conditions directly. Controls
check 504 gate truth rows, 4,096 lexicographic pairs, all 4,096 phase words,
2,074 small invariant graphs, and fourteen rejected malformed inputs.
Normal and optimized Python reports agree. Fresh verification rebuilds
both complete formulas, compares representative and orbit evidence, and
replays both original proofs again. All seven frozen source/input identities
still match. Compact evidence is in [result.json](result.json),
[verification.json](verification.json), [controls.json](controls.json)
and [boundary.json](boundary.json).

A preliminary formula blocking all 7,776 unnormalized witness images
returned UNKNOWN at 60 seconds. That trace is not evidence. The completed
proof uses the justified contact normalization above; it does not increase
that solver cap or infer completeness from the pilot.

## Reproduction and trust

Use CPython 3.11.2, Kissat 4.0.4 source
`8af8e56f174b778aef3aa45af9f739b2a5f492c2`, and drat-trim source
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. Pinned binary SHA256:

* Kissat: `2d185ea775f2c7c16d33a235ef852d2b69f0f3c8b437335b966b4a5aa6265b45`.
* drat-trim: `9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a`.

Set R55_KISSAT and R55_DRAT to those executable paths. From the repository
root, with fresh work directories outside the repository:

```bash
python3 -B ramsey_r55_order3_eleven_core194_maximal/run.py \
  --work /scratch/r55-core194-maximal/full \
  --kissat "$R55_KISSAT" --drat-trim "$R55_DRAT" \
  --solve-seconds 60 --replay-seconds 300
python3 -B ramsey_r55_order3_eleven_core194_maximal/verify.py \
  --source-work /scratch/r55-core194-maximal/full \
  --work /scratch/r55-core194-maximal/verification \
  --drat-trim "$R55_DRAT" --replay-seconds 300
```

Expected: both cases excluded, `maximal_branch_excluded=true`, four
canonical representatives, 7,776 labeled local graphs, no new whole-core
exclusion. `--resume` verifies the stored source/tool/resource contract and
case/formula/trace identities. A STOP file prevents unstarted solver cases;
active solve/replay units finish. No process remains running at publication.
Large CNFs, traces, logs and binaries remain outside Git and are regenerated
by the commands. Hashes alone are not refutations.

The seed and previous local transfer have accepted independent review.
The local classification and complete full-extension formulas here are
reconstructed afresh, and do not assume an old SAT/UNSAT verdict. The
maximal-branch implication imports R(4,5)=25 through the accepted parent
and the corresponding 18..24 degree window. The canonical Core194 count
and cumulative boundary import the [core cover](../ramsey_r55_order3_eleven_four_core)
and [previous full boundary](../ramsey_r55_order3_eleven_local_bound_propagation).
The latter's Core159 exclusion and older empty-signature-specific full
closures retain their independent-review boundaries. The new normalization,
classification, certificate transfer and full refutation await review.
Ordinary unformalized reductions, exact code, interpreter/hardware, SHA256
and the full DRAT checker remain trusted. Internal checking is not peer
review or proof-assistant formalization.

This milestone is complete. The next separate step is to apply the new
`b<=3` bound to the **unrestricted full Core194 base**: 35 positive
four-subset clauses on full variables 215..221, taking its
34,320-variable/617,582-clause base to 617,617 clauses. That base is not
this 216-variable fixed-neighborhood formula and is not the old b=4 child.
No such whole-core test is begun here. The three-versus-eight split and
other moving counts remain unchanged.
