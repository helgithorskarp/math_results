# The exact EI17 difference body is four-chromatic

Let `E={p_0,...,p_16}` be the exact triangle-free four-chromatic realization
certified in the sibling
[`hadwiger_nelson_ei17_common_pair`](../hadwiger_nelson_ei17_common_pair/README.md)
package.  Form the complete physical difference body

```text
E-E = {p_i-p_j : 0 <= i,j < 17}.
```

Repeated points are identified and every strict unit-distance edge is included.
The graph has chromatic number exactly **four**.  In particular this frozen
bottom-up support does not improve the 509-point record.

There are 289 formal addresses.  The 17 diagonal addresses all equal zero, so
the physical support has at most 273 points, well below the 508-point target.
The proof does not need to decide every additional equality: outward rational
boxes conservatively merge all addresses whose coordinates could coincide,
giving 205 colour groups, and conservatively include every pair whose squared
distance could equal one, giving 786 edges.  The stored word properly
four-colours that entire supergraph.

This is stronger than colouring a numerically reconstructed graph.  Every
actual collision lies inside one colour group, while every actual unit pair is
one of the conservative edges.  Thus the word descends to a proper colouring
of the complete physical graph even if further undecided identities exist.
The translate `{p_i-p_16}` is exactly the source `E`, because `p_16=(0,0)`.
The source's exhaustive three-colour contradiction therefore gives the lower
bound four.

## Exact input and interval proof

The source coordinates are the unique root of 30 unit equations in the
published rational box of radius `10^-18`.  The sibling contraction proof is
replayed, including the inverse-Jacobian identity, distinctness, faithful
31-edge graph, triangle-freeness, and 84-node three-colour contradiction.

Every interval endpoint is an integer divided by `2^100`.  Addition,
subtraction, multiplication, and squaring use outward integer rounding.  The
verifier examines all `C(289,2)=41,616` formal address pairs.  Between different
colour groups, at least one coordinate interval is disjoint; within a colour
group, squared distance one is excluded.  Every remaining possible unit pair
is placed in the conservative graph.  The certified margins are

```text
coordinate separation >= 2781598141881073959391426979 / 633825300114114700748351602688
squared-unit exclusion gap >= 152871387373449227668469689 / 158456325028528675187087900672
```

The verifier pins the four source files it imports by SHA-256.  A corrupted
colour word is rejected.  The SAT solver used to discover the positive word is
not a theorem premise.

## Reproduction

Python 3.11 or later and the standard library suffice.  From the repository
root run

```bash
python3 hadwiger_nelson_ei17_difference_body_fourcolour/verify.py
python3 -O hadwiger_nelson_ei17_difference_body_fourcolour/verify.py
sha256sum -c hadwiger_nelson_ei17_difference_body_fourcolour/SHA256SUMS
```

The first two commands end with

```text
EXACT EI17 DIFFERENCE-BODY FOUR-COLOUR STOP VERIFIED
```

This closes only the fixed difference-body support.  It does not cover added
points, rotations between factors, other EI17 realizations, other algebraic
operations, or arbitrary plane unit-distance graphs.  The architecture is
retired without a shell, completion, phase, or host sweep.

The exact input is public at the
[EI17 common-pair package](https://github.com/helgithorskarp/math_results/tree/main/hadwiger_nelson_ei17_common_pair),
source commit `9724508c76581b2283bbe65e02be77433a0146a4`.  Parts'
[509-point, 2,442-edge graph](https://arxiv.org/abs/2010.12665) remains the
unrestricted record; [Haugland's August 2026
revision](https://arxiv.org/html/2608.04542v4) likewise identifies 509 as
current, while its 2,131-point construction is spindle-free restricted work.
