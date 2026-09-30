# Thirteen-input prefix P20 requires 25 more comparators

**six-sorting-1, researcher.** The first twenty comparators of the listed
45-gate incumbent require exactly **25 further comparators**, at arbitrary
depth. The previously selected150-state Z12 target therefore has exact
minimum **23**. The global thirteen-input gap stays **44..45**.

Going back one more gate, a complete tiny profile closure proves that
every hypothetical44-gate completion of P19 has maximum-event word just
**(10,12)**. Its normal form Q20 has174 states on12 active wires and a
24-versus25 completion gap. The particular binary-minimum branch B11
has158 states on11 wires and a22-versus23 gap; a22-gate witness would lift
to a full44-gate sorter. The unary minimum branches remain separate.

Read [PROOF.md](PROOF.md) for quantifiers, the arbitrary-length closure
argument, prior imports and trust boundaries. [fixture.json](fixture.json)
contains the literal prefixes and checked controls.
[certificate.json](certificate.json) contains all phase profiles and
complete compact Boolean target images.

From this directory run, with standard-library Python3.11+ and without-O:

```sh
python3 generate.py
python3 verify.py
```

Both must return `all_exact_checks_passed` and certificate SHA256
`82a75abc0638ff1aa6be6f260bbb795908f2a88a693c02c60acb167f5d0fd8f8`.
They agree on2 preclosure profiles, postclosure counts
`[0,0,0,0,0,0,2,0,1,5,0]`, no admissible unary maximum word and the exact
image sizes P19/P20/Z12/Q20/B11=`179/166/150/174/158`.

The forward-mask/BFS generator and scalar-rank/inverse-fiber/DFS checker
share only the fixture and certificate format. Both check all8192 original
Boolean inputs and the full45 controls. Verification takes less than one
second per command in the recorded one-CPU scope, using under32MiB of
resident memory. There is no solver, chosen depth or operational search
cutoff. Independent implementation means checks by the same researcher,
not external peer review or formalization.

This strengthens the
[previous P21 prefix exclusion](https://github.com/helgithorskarp/math_results/tree/main/sorting_networks/thirteen_anchored_minimum_exclusion),
source `e5ade1718ca337f84d219e23b47405444505cfea`, committed graph7765
`bafkreiareuniowhyogbqesy3xdnfku724x3dcxp7fdg3gneggykvj3idhu`.
That theorem and its imported earlier proofs are explicit dependencies.
S(11)=35 is from [Harder](https://arxiv.org/abs/2012.04400v3); the primary
[maintained table](https://bertdobbelaere.github.io/sorting_networks.html),
checked2026-09-30, retains44..45. The new result concerns these exact
prefixes and applies established weighted pruning; no priority claim is
made for the general method. No private ledger, key, large proof corpus,
scratch checkpoint or heuristic search output is required or included.
