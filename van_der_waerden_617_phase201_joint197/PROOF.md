# Complete phase201 closure

Author: six-vdw-3, researcher. Use the definitions and edit counts in the
README. All statements quantify over arbitrary AP-free binary colorings
`f` of `0,...,3703`; all six pole colors are unrestricted.

## Replayed premises

The unchanged phase201 base packing has denominator1000000, total weight
195802847 and capacities at most1000000 in each original class. Its zero-load
mask `K_c` has78 positions. The published two-leaf class196 cover splits
reference0 at2065 and its reflected reference1 at1638. Its old positive
margins806996 and315425 exclude `e_c<=196`: nonnegative defects first put
all edits into the base residual screen, and both membership branches are
checked. Hence each `e_c>=197`.

Removing any trial zero-load edit under `e_c<=197` leaves at most196 edits
in that same screen. The two leaves lose at most574772 and101686 units over
**every** candidate in `K_c`, respectively. The surviving positive margins
232224 and213739 prove

```
e_c <= 197  implies  E_c intersects K_c in the empty set.
```

The other edit class is unrestricted. This source replays the unchanged
zero-loss checker and its complete tree in both actual reference colors;
the base certificate, tree and all actual AP losses are checked. The
unchanged root1427 certificate, also replayed, proves under `f(1427)=1`
and `e_1<=197` that the full domain1771 shrinks to1023 points, using weight
196892545 and denominator1000000. Its exact frozen hash is recorded in
provenance; no numerical proposal is trusted as a premise.

## Actual activation and bundle inequalities

Assume `f(r)=1` at an original reference0 root `r`, and `e_1<=197`. Then
`E_1` avoids `K_1`. An original reference1 AP must meet `E_1`. An actual AP
with `r` as its sole reference0 point and six reference1 terms must meet
`E_1` among the other six terms, since otherwise it becomes monochromatic1.
Given a proved domain `V` containing `E_1`, use the petal `A intersects V`.
The new checker explicitly validates both sorts of actual seven-term AP.

Three nonempty mandatory petals with empty common intersection require
at least two edits in their union: one point cannot hit all three. Thus
positive integer AP weights contribute their weight to the right side,
and positive triple weights contribute twice their weight. Let `W` be the
sum of these weighted requirements and `L(x)` the sum of row weights
containing `x`. Then `sum_{x in E_1} L(x)>=W`.

## Safe refinement by nonnegative defects

For denominator `D`, every point of the **full inherited domain** must
satisfy `L(x)<=D+nu_x`, with nonnegative integer surcharges. Put
`Gamma=sum_{x in V} nu_x`, `Lbar(x)=min(L(x),D)` and `S=W-Gamma`.
Since `Lbar(x)>=L(x)-nu_x`,

```
sum_{x in E_1} Lbar(x) >= S,
sum_{x in E_1} (D-Lbar(x)) <= 197*D-S.
```

If `S>197*D`, contradiction follows. Otherwise every nonnegative summand
is at most `197*D-S`, proving the next necessary domain

```
V_next = {x in V: D-min(L(x),D) <= 197*D-S}.
```

This refinement requires no assumed opposite-class trial edit. Numerical
generation may optimize a residual problem at a chosen point; the actual
certificate is checked on the full unforced inherited domain. Its complete
domain SHA256 is checked before capacities, so no point can be silently
removed. All eight frozen stages below have `Gamma=0` and maximum load
`D-1`.

| Root | Stage | Input domain | D | W | Result |
|---:|---|---:|---:|---:|---|
|1427|zero2382|1023|1000000|196267921|1022; excludes2382|
|1427|closure|1022|1000000|197795475|gap795475/1000000|
|1662|closure|1771|1000000|198069143|gap1069143/1000000|
|1897|closure|1771|1000000|197458887|gap458887/1000000|
|2132|first screen|1771|1000000|196659635|1243|
|2132|second screen|1243|10000000|1960003758|1241; excludes462,1790|
|2132|closure|1241|1000000|197185230|gap185230/1000000|
|2367|closure|1771|1000000|198840106|gap1840106/1000000|

The second root2132 screen has defect bound9996242, which is smaller than
its denominator10000000. Zero-load points462 and1790 therefore cannot be
edits. At denominator1000000 the initial rounding of that proposal had
weight195999963 and gave no such refinement; it is not used in the proof.
Larger exact integer denominator changes rounding precision, not solver
time, threads or resource limits. The eight stages check7543 actual AP
occurrences, including125 activated occurrences and124 triples. Full
integer results and derived domains are in `expected.json`.

## Complete anchor and consequences

The original reference0 AP `(957,235)` consists of

```
957,1192,1427,1662,1897,2132,2367.
```

Its intersection with `K_0` is exactly `{957,1192}`. Under `e_1<=197`,
the five remaining points cannot be edited, by the five rooted certificate
chains. AP-freeness therefore forces `E_0` to contain957 or1192, without
any bound on `e_0`. If also `e_0<=197`, zero-load rigidity forbids both:
the entire original edit-class197/197 box is impossible.

The exact reference satisfies `T(3703-x)=1-T(x)` at nonpoles and pairs its
poles. Applying the proved conditional statement to `g(x)=1-f(3703-x)`
gives the reflected condition `e_0<=197` implies `E_1` meets `{2511,2746}`.
This transforms arbitrary colorings; it does not impose symmetry on them.

Thus `max(e_0,e_1)>=198`. Combining with the replayed individual floor197
gives total at least395. Color-complementing any AP-free `f` replaces
each count by1849 minus that count, so each count is at most1652,
`min(e_0,e_1)<=1651`, and the total is at most3303. These inequalities
do not imply either individual class is always at least198.

## Trust boundary

The new exact checker imports only the explicit unchanged predecessor
checkers, never numerical proposal code. It verifies actual AP bounds,
colors, bundle multiplicities, integer capacities, domain chains, and all
five roots. Complete coverage follows from the seven-point anchor and
the two zero-load fixed points, not from search exhaustion. The generator
and checker have the same author but use different mechanisms. Python
execution and the displayed proof bridges are unformalized; no external
review or proof-assistant formalization is claimed. UNKNOWN, timeout,
incomplete enumeration and failure to find a coloring prove no exclusion.
