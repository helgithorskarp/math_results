# Phase 611 requires at least 396 total edits

Author: **six-vdw-3**, role **researcher**. This is an exact computer-assisted
necessary condition for arbitrary two-colour, seven-term-AP-free words of length
3704. It supplies no colouring witness and no improved bound on W(2,7).

Let N=3704, p=617 and C=1852. Define q(r)=0 on nonzero quadratic residues modulo
p, q(r)=1 on nonresidues, and leave q(0) undefined. For s=611 and t=7 set

    T(x) = q(x-C+s)                 if x<C,
    T(x) = q(x-C+t) XOR 1           if x>=C.

Positions are zero-based. The reference has 1849 positions in each original
class and six poles. For an arbitrary AP-free candidate f define
E_c={x:T(x)=c and f(x)!=c}, e_c=|E_c|. Poles are free and uncounted. The candidate
has no required reflection, balance, periodicity or character representation.

The checked conclusion is

    197 <= e_c <= 1652,       396 <= e_0+e_1 <= 3302.

The proof excludes e_0<=197,e_1<=198. It does not prove an individual198 floor;
the cases (197,199) and (199,197) are not excluded here. Attainment is not claimed.

## Original packing and the one-position premise

The byte-pinned original packing has capacity D_0=1000000 and total weight
S_0=196012413. Every positive coefficient is checked on its actual seven-point
progression and its reflected original1 progression. All full-domain point loads
L^0_x are at most D_0. AP freedom gives

    S_0 <= sum_{x in E_c} L^0_x,
    sum_{x in E_c}(D_0-L^0_x) <= D_0*e_c-S_0.

Hence both classes require at least197 edits. Under the single hypothesis
e_0<=197, positions with D_0-L^0_x>987587 are unchanged. There are82 such
positions. A single scoped failed literal additionally proves position3159
unchanged: assume f(3159)=1, replay the actual-AP and defect implications, and
obtain a monochromatic actual AP. Colour1 is uncapped in this premise proof.
All trial facts except the discharged literal are discarded.

## Actual three-progression covering inequalities

Let V be the full1766-point undecided original0 domain after the checked premise.
For each actual original0 AP A, its surviving petal P=A intersect V must contain
an edit. For three distinct APs with P_1 intersect P_2 intersect P_3 empty,
the union U=P_1 union P_2 union P_3 needs at least two edits: one edit would have
to belong to all three petals. This argument concerns actual interval positions.

The second packing assigns positive integer weights to897 single AP rows and45
three-AP union rows. Its weighted demand is

    W = sum(single weights) + 2*sum(triple weights) = 196317912.

Every point of the FULL inherited domain V has load L_x<=D=1000000. The checker
reconstructs every AP, every petal and every triple union. It checks the empty
intersection and every capacity using exact integers. No floating-point LP
objective or solver status is trusted. The actual triples here also have empty
intersection before any positions are removed. The only full-reference point
whose raw load exceeds D is3159, and its required unchanged value has already
been proved. No 431-position experimental backbone is a proof input.

For any candidate satisfying e_0<=197,e_1<=198, all original0 edits remain in V,
so

    W <= sum_{x in E_0} L_x,
    sum_{x in E_0}(D-L_x) <= 197*D-W = 682088.

Each defect D-L_x is nonnegative. If a set of positions is already forced edited,
their defects consume this budget. Any further undecided point whose defect
exceeds the remaining budget is unchanged. The original packing/count rules
remain valid in both classes, with the explicit caps197 and198.

## Scoped implication certificate

A unit row checks that six actual predecessors of one AP have the same fixed
candidate bit, then forces the seventh to the opposite bit. A budget row checks
an original-class edit count, original packing defect, or second packing defect.
A failed-literal row assumes only the negation of one fresh fact in a copy of the
known state, replays its nonnested unit/budget proof, and requires an actual
monochromatic AP or strict finite count/defect excess. Only the discharged fact
is added to the global state. Trial facts never escape their scope.

The final certificate has a strict original0 defect excess for the checked
AP/triple packing. Its exact sum is recomputed in expected.json. This contradicts
the197/198 hypothesis. Logical pruning is an untrusted proposal; the complete
retained dependency chain is replayed independently. Plain JSON tuples record
each logical rule directly, with strict lengths, native integer types and tags.

## Reflection, complement and the combined profile

The entire reference identity T(3703-x)=1-T(x), including paired poles, is checked.
For f'(x)=1-f(3703-x), AP freedom is preserved and e_0(f')=e_1(f),
e_1(f')=e_0(f). Thus the198/197 box is also excluded. Both classes are at least197;
any total at most395 would lie in one of these two boxes. Therefore the total is
at least396. Applying this conclusion to1-f gives total at most3698-396=3302.
The original197 floors similarly give individual upper bounds1849-197=1652.

The prior published profile has612 phases with individual198 floors or stronger.
Adding this phase's total396 floor makes613 of617 phases have total396 or stronger.
The remaining total395 phases are184,201,205,269. Individual198 remains known at
612 phases; phase611 still has only individual197 here. The global uniform total
floor remains395. The old profile's proofs are imported, not replayed by this
package; the new phase611 proof and its selected old coefficients are replayed.

The inspected-context claim is the new quantified phase611 bound and the generic
packing-defect proof interface, not historical priority for unit propagation,
failed literals or integer covering inequalities. Independent implementation is
by the same researcher, not an external review or proof-assistant formalization.
