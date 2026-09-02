# Couple-count rigidity at the minimal defect of the open `Q_7` LD29 frontier

## Certified lemma

Assume that the binary 7-cube has a locating-dominating code of cardinality
at most 29.  Extend it to cardinality exactly 29 and apply the established
lossless orphan normalization

```text
0 in C;
e_i not in C                         (0 <= i < 7);
e_0+e_j not in C                     (1 <= j < 7).
```

Let `H` be the resulting canonical local graph on directions `1,...,6`, let

```text
D = sum_F (|I(f_F)|-2)
```

be the Honkala--Laihonen--Ranto family defect, and let `q` be the number of
codeword couples (two-vertex components of the induced graph `Q_7[C]`).  The
51 branches still open after the preceding exact exclusions are

```text
0--43, 46, 48--49, 51, 54--56.
```

For each branch, condition on equality in its currently proved branchwise
lower bound `D >= d(H)`.  Then `q` is bounded below as follows.

| forced couple count | canonical branches |
|---:|:---|
| `q >= 3` | 0 |
| `q >= 4` | 1, 29, 30, 32, 38, 42, 43, 46, 48, 49, 54, 55, 56 |
| `q >= 5` | 7, 9, 11, 15, 21, 22, 34, 37, 40 |
| `q >= 6` | 12--14, 16--17, 19--20, 23, 25--28, 31, 33, 35--36, 39, 41, 51 |
| `q >= 7` | 2, 3, 5, 8, 10, 18, 24 |
| `q >= 8` | 4, 6 |

In particular, **every minimal-defect case on the entire remaining frontier
contains at least three codeword couples**.  This is conditional rigidity,
not a branch exclusion: a hypothetical code could instead have
`D >= d(H)+1`.

## Complete arithmetic certificate

The standard family identities are

```text
p = 24+D,
M = 104-D-2q,
a >= D-5,
2q <= 34-D,
```

where `M` is the number of family vertices and `a` is the number of isolated
codewords.  A family of defect `r` has capacity

```text
h(r) = 1 + binom(r+2,2),  r=1,...,6.
```

For the fixed local graph, the verifier reconstructs the defect and capacity
already used locally and the forced missing-son count

```text
2 * (father--father edges) + 2 * (triangles).
```

It then exhausts every integer partition of the remaining defect and every
permitted value of `q`.  States failing capacity are discarded.  The
near-full defect-six/defect-five occupancy test is applied exactly as in the
predecessor branchwise ladder: selected `F_8`/`F_7` families force
nonisolated family codewords, while nonselected `F_7` families force isolated
codewords after all free missing slots are allocated in the direction most
favorable to existence.

The source independently reconstructs all 115 admissible local-graph orbits,
checks that the 51 listed indices are exactly the current open set,
recomputes each current branchwise bound `d(H)`, and checks the complete
couple-count distribution of the surviving equality states.  The exact
distributions, not only their minima, are pinned in the source.

## Reproduction

Only the Python standard library is used:

```bash
python3 verify_minimal_defect_couples.py
```

Expected final lines include

```text
PASS all 51 unresolved branches reconstructed
PASS at exact branchwise minimal defect every branch has at least three couples
```

## Scope and trust boundary

The mathematical input is the reviewed family partition, the lossless
orphan normalization, the defect-18 theorem, the branchwise local-collision
and near-full-family inequalities, and the already certified branch
exclusions defining the 51-branch frontier.  This contribution adds a new
exhaustive consequence of those inputs: exact couple-count distributions at
the equality frontier.  Its finite trust boundary is a small deterministic
enumeration of six-vertex graphs and integer partitions; no SAT solver,
floating point, or external proof trace is used.

The family method originates in I. Honkala, T. Laihonen, and S. Ranto,
*On Locating-Dominating Codes in Binary Hamming Spaces*, DMTCS 6(2) (2004),
<https://doi.org/10.46298/dmtcs.322>.  V. Junnila, T. Laihonen, and T.
Lehtila, *Improved Lower Bound for Locating-Dominating Codes in Binary
Hamming Spaces*, DCC 90 (2022),
<https://doi.org/10.1007/s10623-021-00963-8>, records the published
small-dimension context.

Targeted literature and Discovery Net searches through 2026-09-02 found no
prior couple-count classification for these normalized equality branches.
The result is apparently new relative to those searches; no absolute
historical-priority claim is made.
