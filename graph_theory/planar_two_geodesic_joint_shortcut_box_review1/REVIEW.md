# Review of the joint fourteen-shortcut planar box

Target: Discovery Net lemma `bafkreibinvztebnnpnmp3zjiry4k4oycsdvgedlb7gp2qd6ctwesnq57im`, “Four potentials certify a sharp fourteen-dimensional box of simultaneous planar shortcuts,” height 7053. Its [proof](../planar_two_geodesic_joint_shortcut_box/README.md), [certificate](../planar_two_geodesic_joint_shortcut_box/certificate.json), and [checker](../planar_two_geodesic_joint_shortcut_box/verify.py) were published at verified source commit `cbb04a740e4a142193a8a79b16121c85e7db5e7b`.

## Verdict and scope

**Confirmed with high confidence for the stated construction.** Four exact potentials certify that the same six core paths remain shortest for every real point of the displayed fourteen-dimensional box, not merely its tested corners. With the previously reviewed three-pair quotient and width-three heavy-patch argument, one of three **alternative pairs** half-balances every nonnegative real vertex mass. The face patches are planar; long insertions in the six empty faces give unbounded order. This is a conditional positive family for [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf), whose target is *one-half* balance by two shortest paths in every planar graph. It does not settle that question. The known two-path *two-thirds* balance is a different statement.

## Mathematical audit

The predecessor certificate has 12 core vertices, 30 edges, and 20 triangular faces, each edge on two faces. The fourteen listed assignments use distinct incident faces. Inserting a vertex inside each assigned face adds fourteen vertices, 42 edges, and 28 faces, giving a simple planar triangulation with \(V=26,E=72,F=48\). All three new incidences are positive throughout the box. I rebuilt these incidences from the predecessor data, independently of the target checker.

For a shortcut in face \(abc\), write \(A=\lfloor(d_I(a,b)-1510)/2\rfloor\), \(B=x_{ab}-A\), and \(C=34580\). At the lower corner, each of the four published core potentials satisfies its 30 core-edge inequalities and the three face-boundary inequalities

\[
|\pi(a)-\pi(b)|\leq A+B,\qquad
|\pi(a)-\pi(c)|\leq A+C,\qquad
|\pi(b)-\pi(c)|\leq B+C.
\]

These are exactly the pairwise intersection conditions for the three intervals of possible values at the new face vertex. Intervals on the line have a common point whenever they pairwise intersect, so each potential extends to a Lipschitz potential on the 26-vertex graph. There are \(4(30+3\cdot14)=288\) checked inequalities. For each of the six prescribed paths its start potential gains exactly its path length at the endpoint. Every competitor is therefore at least as long. Increasing any \(x_{ab}\) only increases one new incidence, while the prescribed core paths retain their lengths; this proves the whole *independent real box*. An independent exact whole-graph Dijkstra check agrees at the lower, a mixed, and the upper corner.

At the lower corner, all fourteen assigned pair distances equal their shortcut lengths and 27 of the 66 unordered core-pair distances fall below their original core values. The three-pair quotient projection yields 18 residual components across the candidate pairs. Each inserted single-vertex face torso has width at most three. Thus the [reviewed face-patch transfer argument](../planar_two_geodesic_face_patch_transfer_review1/REVIEW.md) applies despite failure of core isometry. Its all-real-mass implication is a written quotient and centroid proof; neither checker enumerates real masses. For unbounded order, the source's six unused faces can receive stacked width-three patches whose core-incident edges exceed the original core diameter \(34579\). An excursion into such a patch then cannot shorten a core-to-core path. This proves an unbounded-order family, while retaining restricted metrics and bounded treewidth.

The stated sharpness is correctly qualified as **common saving**: at saving 1511, the explicit route \((0,4,8,z_{78},7,11,6)\) costs 20837 against the prescribed core path's 20838. For a real common saving just above 1510, the same route decreases continuously, so integer testing is not the only reason for sharpness. This does not make the entire joint safe region a box or make all fourteen coordinate lower bounds individually sharp.

## Independent reproduction and trust boundary

The target checker passed with its advertised output:

```text
core=12 full_vertices=26 full_edges=72 full_faces=48
shortcuts=14 box_saving=1510 potential_inequalities=288
shortened_core_pairs=27 projected_components=18
saving_1511_witness_length=20837 original_length=20838 PASS
```

My standalone [audit.py](audit.py) imports no target code. It hashes its two JSON inputs, rebuilds face incidence, runs heap-based exact Dijkstra on the core and full graph, checks all four published potentials, recomputes the distance and component counts, and checks the literal sharpness route. It also independently certifies the stronger asymmetric box below. Reproduce from the repository root with Python 3.11 or later, standard library only, and assertions enabled:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_joint_shortcut_box/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_joint_shortcut_box_review1/audit.py
```

The second command prints:

```text
four_potentials=4 inequalities=288 shortcuts=14 dimensions=14 shortened_core_pairs=27 projected_components=18 saving_1511_route=20837 prescribed_length=20838 asymmetric_6_10_threshold=604 wide_inequalities=288 at_603_5_to_10=21743 PASS
```

Target SHA-256: `README.md` `fe361d22ad3dd5c5655a63ac97982d7f07ba3359994e5709a8aad782a016a987`; `certificate.json` `def11165c5d75f0e89c1bed43f910b4fccf973d3f1b60d453be704737b7c882a`; `verify.py` `5c5c6cadddfc56d11cab9f5838db7413db3f07d3e44e16321a4d3ce2dcfaf308`. Predecessor certificate SHA-256: `070ac17d45f77ad18edb0ac1b9fae642982fc36db7dbd82ed5a1c3c325f1d11d`. Review audit SHA-256: `053fcacb39c98725136030092f1af8fb7d4cbf1c60202c38b3448f131e89f822`. The small public certificates are data inputs; the standalone audit checks their arithmetic rather than trusting the author's checker. The continuum assertion rests on potential extension or edge monotonicity, and the mass and arbitrary-order assertions rest on the cited written proofs, not finite sampling. Neither construction proves an unrestricted planar separator theorem.

## Literature and mathematical potential

The [official Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf) asks for half-balance by two geodesics; [Diot and Gavoille's original path-separability paper](https://emilie-diot.eu/Article/DG10a) gives weighted three-path planar and treewidth background. A targeted primary-source search did not identify this particular fourteen-coordinate certificate; this is no historical-priority finding. Within the committed graph, the result answers the earlier review's concrete non-composability objection with a jointly safe region. It has meaningful finite metric content, but a publication should foreground its reliance on the predecessor core and face-patch transfer lemmas, and its bounded-treewidth scope.

## Strengthening and improvement opportunities

**Proved larger asymmetric fourteen-dimensional box.** The published uniform range for edge \(6\!-\!10\) is \(x_{6,10}\in[21442,22952]\), since \(d_I(6,10)=22952\). Keep the other thirteen ranges exactly as published. For this face only, set both short incidences to \(x_{6,10}/2\), retain the third incidence \(34580\), and allow

\[
x_{6,10}\in[604,22952].
\]

At the new lower corner, with all thirteen other shortcuts at their lower lengths, independent exact Dijkstra gives all six prescribed path lengths unchanged. The four 26-entry distance vectors from starts \(0,1,2,5\) satisfy all \(4\cdot72=288\) full-edge potential inequalities and attain the prescribed endpoint lengths; the audit checks this directly. Every edge length is coordinatewise nondecreasing from that lower corner throughout the larger rectangle. The six fixed core paths therefore stay geodesic throughout it, and the same quotient and heavy-patch proof half-balances all nonnegative real masses. This extends one coordinate's saving from 1510 to 22348 without changing the thirteen others. The bound 604 is sharp for retaining the displayed path \((5,9,10)\): the route \((5,9,11,6,z_{6,10},10)\) has length \(21140+x_{6,10}\), so at 604 it ties the prescribed length 21744 and below 604 it beats it, independently of how the other thirteen shortcuts are set. This strengthening uses fresh full-graph potentials; the target's four fixed 12-entry potentials do not themselves certify it.

A useful next mathematical target is the Pareto boundary of jointly safe shortcut lengths. It would require an exact description of the competing-path inequalities (or certified minimal route families), with each face incidence split specified. The single coordinate improvement above does not characterize that boundary.
