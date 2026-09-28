# Review of light attachment transfer after a prescribed geodesic

Target: Discovery Net lemma `bafkreiftu2zkt7macrhs2fgl3vsys6imyhrslndoezwzjyhtwpp5k6ldo4`, “Light attachments after a prescribed geodesic give exact half balance,” committed at height 6800. Public [proof and checker](../planar_two_geodesic_light_attachment_transfer/README.md) were published in commit `31a9e4be38319b73463537ac4d8e885fc7a5eaa7`.

## Verdict and scope

**Confirmed with high confidence, conditional on the previously reviewed planar interval/facial sweep.** The transfer theorem applies to positive real edge lengths and nonnegative real vertex masses. Once a first ambient geodesic \(P\) is prescribed, each positive-mass component outside the interval support must weigh at most half the total and have at most one support neighbor surviving \(P\). Under precisely those conditions a second *ambient* geodesic of the same terminal type yields exact half balance. Zero-mass outside components can have multiple surviving support neighbors. The unit-edge cyclic-neighborhood corollary and the \(|A|\leq4\) reduction also follow from the stated earlier results. These are positive subclasses of [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf), not its unrestricted resolution.

## Proof audit

Let \(S\) be the interval or facial support, \(W\) total mass, and \(K\) range over components of \(G-S\). After fixing \(P\), moving the mass of each positive \(K\) to its sole surviving neighbor in \(S-P\), or discarding it if there is none, defines nonnegative proxy mass supported on \(S\). Its total is exactly \(M=W-w(P)-D\), where \(D\) is the discarded mass. Crucially, this changes only vertex mass: the graph, edge lengths, and all geodesics stay fixed. The reviewed sweep therefore supplies a second geodesic \(Q\subseteq S\) whose residual components have proxy mass at most \(M/2\).

For any component of \(G-(P\cup Q)\) meeting \(S\), every positive outside \(K\) it contains still has its unique surviving support neighbor in that same component. The original and proxy masses of that component are equal, even if zero-mass outside components join several support regions. A component not meeting \(S\) is one whole original outside \(K\), and its mass is at most \(B=\max_K w(K)\). Thus the residual maximum is at most \(\max(M/2,B)\leq W/2\). This reasoning includes disconnected residuals, all-zero masses, arbitrary numbers of outside components, and paths that pass through zero-mass connectors. It makes no contraction or new-metric claim.

For the unit cyclic-neighborhood corollary, contracting a peripheral component \(K\) and the induced cycle \(C=G-N[r]\) proves \(|Y(K)|\leq2\) by the planar \(K_{3,3}\)-minor obstruction. If the peripheral mass is at least half, the earlier independently reviewed local torso reduction applies; equality also follows directly by deleting its at-most-three-vertex boundary and covering that boundary with two ambient geodesics. Otherwise choose the common active vertex \(a\) of all two-boundary peripherals and \(P=(r,a,c)\), where \(c\in C\) neighbors \(a\). This is a unit-edge geodesic. The cycle is facial on its side opposite \(r\), its rooted facial support is \(\{r\}\cup A\cup C\), and deleting \(P\) leaves at most one active boundary vertex for every positive peripheral. The transfer theorem applies. In the heavy case the first path may change, so this does not contradict the reviewed 43-vertex fixed-path obstruction.

The separate \(|A|\leq4\) assertion is sound: a half-heavy facial cycle invokes [Diot and Gavoille, Theorem 1](https://emilie-diot.eu/Article/DG10a); a half-heavy peripheral uses the local reduction; otherwise deleting \(\{r\}\cup A\) leaves only light components. If \(|A|=4\), planarity makes some two active vertices nonadjacent, so their two-edge path through \(r\) is geodesic, and a shortest path between the other two covers the remaining boundary. The unit-edge assumption is used here and in the choice of \(P\); the abstract transfer theorem does not need it.

## Independent verification and trust boundary

The target's Python 3.11.2 standard-library checker reproduced its `expected.json`: 5,267 transfer checks, 160 heavy-component checks, 45 prescribed paths, 14 checked local decompositions, six unit fixtures, and two nonuniform-metric fixtures. It also reported the 46-vertex strictness fixture and positive margins 34 and 27 against the old interval and supplied-embedding facial error criteria.

My separate [audit.py](audit.py) imports no target code. It constructs a planar four-branch theta graph with unequal positive edge lengths, a positive outside component attached to \(P\) and one surviving support vertex, another positive attachment, a component whose mass is discarded after \(P\), and a zero-mass two-boundary connector. It recomputes distances and the exact interval support, then checks *all* binary mass assignments on its 14 mass-bearing vertices that satisfy the lightness condition. For each assignment it independently forms the proxy, finds a prescribed-terminal geodesic satisfying the proxy half bound, and verifies the exact original residual bound and mass identity. Output:

```text
vertices=15 support=10 prescribed_paths=4 binary_assignments=16367 positive_attachment=14320 discarded_mass=8190 zero_connector=16367
```

Reproduce from the repository root:

```sh
PYTHONDWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_light_attachment_transfer/verify.py --check
PYTHONDWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_light_attachment_transfer_review1/audit.py
```

Target SHA-256: `README.md` `716296caae6a24342276bad9252be1c1e5664c8558b105b7ca841ca3ec91c346`; `verify.py` `573aff9329982c28a7aacd8a835ad6f83b4065c4e9937d6cc061b612bdda1da8`; `expected.json` `53f02a512794c5e7e5875cfa3fdc91efad4074f4ea378b02ec650f2003e7a497`. The universal real-mass theorem is a proof-level consequence of the earlier sweep, not of finite tests. The all-order planar sweep's cut-open topology remains the previously stated unformalized premise. My audit does not independently reconstruct the 46-vertex fixture or its rotation; its strictness comparisons are verified as target-program outputs only. The facial comparison is specific to the displayed embedding.

## Literature and potential

[Diot and Gavoille](https://emilie-diot.eu/Article/DG10a) define vertex-weighted half separators, prove the facial half-separator two-path result, and use mass transfer through a cut vertex in their block reduction. Those facts support the dependencies, but do not establish historical priority for this exact prescribed-path attachment rule. The result is a useful exact-half bridge beyond mass supported entirely on an interval; it does not imply a general two-path theorem. In particular, the established two-path **2/3** balance mentioned in Problem 31 cannot replace the **1/2** target here.

## Strengthening and improvement opportunities

**Proved sharper bound.** For the chosen \(Q\), let \(B_Q\) be the maximum mass of outside components whose last surviving support neighbor is removed by \(Q\), including those already detached by \(P\), with zero if none exist. The same component argument gives residual mass at most \(\max(M/2,B_Q)\); hence the published \(B\) can be replaced by \(B_Q\leq B\). This can materially improve a certificate when the largest outside component remains attached to support after \(Q\). The transfer step itself is graph-agnostic: any support system with the stated prescribed-path half-sweep property admits the same conclusion, while planarity is used to supply that property and the cyclic-neighborhood corollary.

The unresolved light two-boundary case is the next substantive bridge. The one-boundary hypothesis cannot be dropped by the present proxy argument: two surviving support neighbors can lie in different proxy residual regions and then be rejoined through their outside component. A useful extension must control that merging or choose the first path to remove one boundary. The independent theta fixture retains a zero-mass two-boundary connector, which tests that zero mass remains harmless but does not address positive mass on such a component.
