# Aligned one-pivot EI17 clouds are four-colourable

## Scope

Let \(P=\{p_0,\ldots,p_{16}\}\) be the exact 17-point Exoo--Ismailescu
seed certified in `hadwiger_nelson_ei17_common_pair`.  For any set
\(A\subseteq\{0,\ldots,16\}\), form the physical plane support

\[
S_A=\bigcup_{a\in A}(P-p_a).
\]

These are aligned translated copies of the seed whose selected pivot is at
the common origin.  The unit-distance graph here is the **complete physical
support graph**: every pair of distinct points of \(S_A\) at distance one is
an edge, including contacts not inherited from the seed copies.

## Theorem

Every complete physical unit-distance graph on \(S_A\) is four-colourable.
The full cloud \(S_{\{0,\ldots,16\}}=P-P\) has at most
\(1+17\cdot16=273\) distinct points.  Consequently every subassembly in this
aligned one-pivot family is four-colourable.

This is a restricted-family exclusion.  It says nothing about independently
rotated or reflected one-pivot copies, other seeds, or arbitrary plane
unit-distance graphs.

## Colouring and exact certificate

The seed has the checked proper colour word

```
00110231213003232
```

with its four colours identified with the two-bit group.  On formal
difference labels define

\[
C(p_i-p_a)=C_P(p_i)\mathbin{\mathtt{XOR}}C_P(p_a).
\]

There are two issues beyond checking the visibly inherited seed edges:

1. two difference labels may denote the same physical point, so the rule must
   be independent of the label;
2. the completed physical graph can have additional unit contacts.

`verify.py` resolves both against the already certified root box for \(P\).
For every pair of the 289 formal labels it checks one of the following with
exact rational outward intervals:

- if their proposed colours differ, one coordinate interval is disjoint, so
  the labels cannot coincide;
- if their proposed colours agree, their squared-distance interval excludes
  one, so they cannot form a monochromatic unit edge.

The root-box existence and uniqueness proof, including faithfulness of the
17-point seed, is rerun as a dependency.  No floating-point value participates
in the certificate.

## Reproduction

From the repository root:

```bash
python3 hadwiger_nelson_ei17_aligned_pivot_cloud/verify.py
```

The computation uses only the Python standard library and exact integers and
rationals.

## Construction-lane consequence

The contact-rich aligned realization of all 17 pivot choices cannot be the
source of a sub-509 five-chromatic graph, even after complete all-pairs
unit-edge reconstruction.  Further work in the one-pivot lane would need
genuinely non-aligned relative placements and a stricter colour-interface
signal before exact expansion.
