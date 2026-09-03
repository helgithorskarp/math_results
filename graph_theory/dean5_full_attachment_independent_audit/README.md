# Independent audit of the Dean-5 full-attachment census

## Result

The full-attachment finite proposition in Appendix B.3 of Elias Botsford,
*Cycles of length divisible by five in graphs of minimum degree five*, v1.0.1
(<https://doi.org/10.5281/zenodo.22182448>), is correct.  The independent
verifier in this directory reproduces every displayed maximum and finds no
surviving structural scenario.

This is a scoped result, not an inference from the authors' certificate.  The
program neither reads the distributed JSON certificate nor imports or invokes
the supplement's verifier.  It uses a different internal representation:
simple paths are subset/endpoint dynamic-programming states, linkages are
intersections of vertex bitmasks, and compatible component families are found
by an exact maximum-coverage clique search.

I also audited the mathematical map from a hypothetical graph to this finite
state space.  It is sound.  In particular, the census retains the *complete*
set of core feet of every component; independent phases at different feet and
the optional coincidence of a secondary foot with one of two root feet only
enlarge the finite state space.  Pair rejection combines internal paths from
distinct exterior components with two vertex-disjoint core links, so each
rejection expands to a simple cycle.  The finite result therefore proves the
multiple-component, tetragonal-parameter-four subcase to which the manuscript
applies it.

## State space checked

The displayed cores are

```text
T_A = C8 + {03,36}
T_B = C8 + {03,47},
X = {0,2,4,6},  Y = {1,3,5,7}.
```

For component type `d`, the selected roots are one core vertex when `d=1`
and a same-color pair when `d=2`.  The reservoir increments are respectively
`{0,2,4}` and `{0,2}`.  For every root set, port, and base phase modulo five,
the verifier enumerates all simple paths in the genuinely augmented core and
retains the atomic row exactly when

```text
phase + increment + 2 + core-path length != 0 (mod 5)
```

for every permitted choice.  For two retained rows it enumerates both
terminal bijections and all pairs of vertex-disjoint core paths, retaining
the pair exactly when

```text
phase1 + increment1 + phase2 + increment2
       + 4 + linkage total != 0 (mod 5)
```

for all choices.  A component configuration independently chooses absence or
one phase at every eligible port and at least one port.  The global search
then exhausts all pairwise-compatible families with at least two components.
It permits two copies of a self-compatible configuration; larger
multiplicities cannot change compatibility or coverage.

The program checks 54 structural rows for each displayed core: Type I with
empty or singleton `R`, and Type II with zero, one, or two members of `R`, in
both all-`d=2` and mixed modes.  It inserts precisely the actual forced
`R`/theta edges.  In the Type-II empty-`R` case it tries all 12 possible
same-color uncovered pairs, forbids components from covering that pair, and
does not insert the deleted smoothing edge.

## Completeness of the implementation

- A path state records its used-vertex mask and last vertex.  Extending it by
  each unused neighbor generates every simple path; states with the same mask
  and last vertex have identical possible continuations, so merging them is
  lossless for path existence and disjointness.
- Disjointness of two paths is exactly a zero intersection of their vertex
  masks.  Both terminal bijections are tested.
- Cartesian products over the surviving phase choices enumerate every
  relaxed complete-attachment configuration.
- The recursive global search visits every clique in increasing index order.
  Its only bound is the union of coverage of all remaining candidates, an
  upper bound on every continuation.  Stopping at the number of nonforbidden
  core vertices is exact.

These observations cover the program's enumeration claims without relying on
the agreement of its output with the distributed certificate.

## Reproduction

Python 3.10 or later is sufficient; there are no third-party dependencies.

```bash
python3 verify_full_attachment_bitmask.py
```

The complete output is:

```text
T_A
  locally allowed atoms: d1=8, d2=34
  displayed maxima: all-d2=6, mixed=6, all-d2+A>=3=6, mixed+A>=3=-1
  Type I, R empty / all-d2: 6
  Type I, R empty / mixed: -1
  Type II, R empty / all-d2: -1
  Type II, R empty / mixed: -1
  Type I, |R|=1 / all-d2: 6
  Type I, |R|=1 / mixed: -1
  Type II, |R|=1 / all-d2: 6
  Type II, |R|=1 / mixed: -1
  Type II, |R|=2 / all-d2: -1
  Type II, |R|=2 / mixed: -1
  structural rows checked: 54
T_B
  locally allowed atoms: d1=8, d2=32
  displayed maxima: all-d2=6, mixed=4, all-d2+A>=3=6, mixed+A>=3=-1
  Type I, R empty / all-d2: 6
  Type I, R empty / mixed: -1
  Type II, R empty / all-d2: -1
  Type II, R empty / mixed: -1
  Type I, |R|=1 / all-d2: 6
  Type I, |R|=1 / mixed: -1
  Type II, |R|=1 / all-d2: 6
  Type II, |R|=1 / mixed: -1
  Type II, |R|=2 / all-d2: -1
  Type II, |R|=2 / mixed: -1
  structural rows checked: 54
FINAL SURVIVORS: []
```

Here `-1` means that no family with the required component multiplicity
exists.  The v1.0.1 source and computational-supplement upload used in the
broader audit had SHA-256 values

```text
5e06b1e307b0b48c463bddf2880fdb3e9185e9b51f2740f5057e3f14e7aad7e2  dean5-source-v1.0.1.tex
75b604acc53a38622e0fffddebcb27e3e883f5836d7da7e7ddb45c8378eebed5  dean5-computational-supplement-v1.0.1-upload.zip
```

The computational supplement is archived at
<https://doi.org/10.5281/zenodo.22167084>.  Agreement with its reported
counts is a useful differential check, but is not an input to this verifier.

## Scope

This contribution validates the full-attachment census and its one-way
graph-to-state reduction.  The theorem also depends on the reductions to
5-weak graphs, the other tetragonal and trigonal cases, Type-I end-block
arguments, Type-II carrier arguments, the split-apex theorem, and cited
external graph-theoretic results.  Those are outside this program's finite
claim and must be audited separately.
