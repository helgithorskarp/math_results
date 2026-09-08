# Independent review of the maximal-K4 global carrier

## Verdict

**ACCEPT**, with scope limited to the global carrier reduction in Discovery Net
artifact `bafkreihujya7ormfvza6jvm2xnly7bnbt5nsv3j6ispwz4pu34pp24dchu` (h3873)
and source commit `1884881efbf52a54bd3a30b1445c211da7caec27`.

The accepted result is not a 43-vertex Ramsey graph, a SAT decision, or a proof
of `R(5,5) >= 44`.  It is a complete, exactly counted family of SAT carriers:
if a good43 graph exists, a relabeling of it occurs in this family.

## Mathematical rederivation

Let red and blue denote the two edge colours of a hypothetical good43 graph.
Greedily remove red K4s.  The standard equality `R(4,5)=25` forces at least
five removals: while at least 25 vertices remain there is a red K4, since a
blue K5 is forbidden.  Then greedily remove blue K4s from the red-K4-free
remainder.  The final core has neither colour of K4.  Since `R(4,4)=18` and
its order is `n=43-4q`, necessarily

```
q in {7,8,9,10},   5 <= r <= q,   n in {15,11,7,3},
```

where `r` is the number of red blocks and `q-r` the number of blue blocks.
Relabel the final core to a representative in McKay's complete Ramsey(4,4,n)
catalog and put the red blocks first.  Permuting the vertices of each nonroot
block sorts its four columns to the first red block.  This yields every stated
normalization without changing the graph.

I independently enumerated all 65,536 cross-edge matrices.  Avoiding a
monochromatic K5 gives 37,823 same-colour and 35,714 opposite-colour matrices;
root-column sorting leaves 1,998 red-child and 1,931 blue-child matrices.  For
each block/core-vertex star exactly the all-block-colour column is forbidden,
leaving 15 choices.  Thus a fixed `(q,r)` core has exactly

```
1998^(r-1) * 1931^(q-r)
* 37823^(C(r-1,2)+C(q-r,2))
* 35714^((r-1)(q-r)) * 15^(q(43-4q))
```

carrier graphs.

The encoding is injective within a task because all digits control disjoint
edge sets.  Different catalog records fix different labeled core edges;
different `r` values change a block's internal colour; and different `q`
values cannot collide because the extra block for the larger `q` would be a
monochromatic K4 inside the smaller `q`'s Ramsey(4,4) core.  Summing all 18
classes therefore gives the exact distinct labeled-carrier count `N` recorded
in `REPRODUCTION_RESULT.json`, not merely a count of possibly duplicate codes.

The physical CNFs contain every red- and blue-K5 prohibition, the root column
ordering clauses, and the red-K4-free closure on the remainder after the red
packing.  The fixed final core is already K4-free in both colours.  I rebuilt
the fixed/variable edge partition and compared all 21,530,292 clauses in the
18 representative CNFs literal by literal.  This also confirms that the
instances represent the carrier reduction; no instance was solved here.

## Independent checks

`independent_check.py` imports no reviewed-package module.  It performs:

- checksum verification of the 20-file target package and 29-file accepted
  parent package;
- a third all-record catalog census using common-neighbour subgraphs to detect
  K4s, independently of the submitted recursive Python and literal C++
  checkers;
- semantic enumeration of the four relevant 4-by-4 matrix domains;
- exact recomputation of all task intervals, `N`, the imported comparison
  count `H`, `18767*N < H < 18768*N`, `4096*N < H`, and `N < 2^770`;
- literal-by-literal reconstruction of all 18 generated representative CNFs.

From a detached checkout of the reviewed commit, after downloading the pinned
catalogs and generating the representative formulas as documented by the
submission, run:

```bash
python3 -B ramsey_r55_global_maximal_packing_review1/independent_check.py \
  --source /path/to/reviewed-checkout \
  --cache /path/to/pinned-catalog-cache \
  --cnfs /path/to/generated-cnfs
```

The run used Python 3.11.2.  Before this independent pass, the submission's
own full validation was reproduced with GCC 12.2.0, including ordinary and
ASan/UBSan C++ catalog checkers.  Both normal and `python3 -O` formula audits
passed.  The 18 CNFs occupy 947,947,181 bytes.

## Imported trust boundaries

Catalog completeness and isomorphism-class coverage are imported from Brendan
McKay's [author data page](https://users.cecs.anu.edu.au/~bdm/data/ramsey.html),
which labels these as all Ramsey(4,4)-graphs and gives the used counts.  I
verified every downloaded record's pinned hash, graph6 transport, literal
uniqueness, and absence of red and blue K4s, but did not rerun an independent
isomorph-free catalog generation.

The cross-matrix files come from the previously accepted h3835 package; the
four domains used here were nevertheless re-enumerated semantically.  The
comparison `H` comes from previously accepted h3863 and is hash-pinned.  The
new family is not asserted to be a subset of h3863, so the factor comparison
is a comparison of complete-carrier sizes, not a measured fraction of one
search tree removed from another.
