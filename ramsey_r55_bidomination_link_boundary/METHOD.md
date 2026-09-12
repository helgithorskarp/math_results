# Mathematical attempt and its boundary

Let B4 be the class of graphs G with no K5 or I5 and with gamma(G)=gamma(complement(G))=4. The retained finite target is B4 at order 43. As proved in the previous pass, membership requires a common neighbor in each color for every triple. The exact full-class formula from that pass remains UNKNOWN.

## 1. Attempted local edge loss

Fix a vertex v and one color, called red, and let H be the red graph on its red neighborhood. Then H has no K4 or I5. For any two distinct vertices x,y of H, a common red neighbor of v,x,y lies in H and is adjacent to x,y. Thus H satisfies

    P2: every pair of distinct vertices has a common neighbor.

The first attempted closing step was to improve the upper edge bound for these local graphs. If U_P2(d) were sufficiently smaller than the ordinary extremal bound U(d), summing local bounds against the global monochromatic-triangle identity could exclude the entire B4 class. This attempt uses no prescribed candidate degree sequence or fixed catalog neighborhood.

The seven witnessed pairs (d,e) are

    (18,85), (19,92), (20,100), (21,107),
    (22,114), (23,122), (24,132).

Each is an actual (4,5) graph with P2. These edge counts are the classical upper bounds U(d). Hence, within that imported extremal-bound trust boundary,

    U_P2(d) = U(d), for every d=18,...,24.

One witness per order proves the failure of this proposed improvement. The optional complete top-edge replay additionally finds that all 74,210,1,31,133,2,2 supplied extremal records, respectively, have P2. This is not an exclusion of any possible good43 neighborhood. No stronger statement about all lower edge levels is inferred.

The fact that every color-degree of good43 is between 18 and 24 is the standard R(4,5)=25 implication. The witness verification itself needs no Ramsey-number theorem or catalog completeness.

## 2. Incidence strengthening attempted

Write A=N_R(v), B=N_B(v), H=G_R[A]. For b in B define its actual attachment support S_b=N_R(b) intersect A. The triple condition and I5 exclusion imply:

1. S_b intersects N_H(a) for every a in A: it is a total dominating set of H. Use a common red neighbor of v,a,b.
2. S_b intersects every independent four-set in H, or that set together with b is I5.
3. S_b and S_c intersect for distinct b,c in B. Use a common red neighbor of v,b,c.

Together with P2, these conditions are exactly the requirements that all triples containing v have a common red neighbor, plus the one-attachment I5 test. They are necessary conditions on literal individual incidences, rather than just edge totals.

They do not by themselves bound the number of outside attachments. Here is a general reason, applying to every H with no K4 or I5 and with P2, not only the seven fixtures.

### Closed-neighborhood lemma

For h in H, put C_h=N_H(h) union {h}. Then:

- C_h intersects every independent four-set I. If it did not, I union {h} would be I5.
- C_h is a total dominating set. For a different from h, P2 gives a vertex in N_H(a) intersect N_H(h); for a=h, use any neighbor of h. Such a neighbor exists by P2 when |H|>=2.
- Any two C_h,C_k intersect, by P2 for h != k and by nonemptiness for h=k.

Consequently, an arbitrary multiset of these supports meets all three conditions above. Repetition is allowed in this relaxed support system. In particular, there is no bound on the number of columns using just these conditions.

Each individual column has a literal Ramsey-valid realization: add v red to all of H, add b blue to v and red exactly to C_h inside H. This graph has no K5: one containing v or b would need a K4 in H, and one containing both v,b is prevented by their blue pair. It has no I5: one containing b would need an independent four-set disjoint from C_h; one containing v cannot use H. The remaining cases lie in H. The verifier directly checks all 147 such physical graphs for the seven witnesses.

This is a limitation of the stated fixed-root relaxation only. It is not a model of B4 on 43 vertices, not simultaneous realizability of several columns, and not a limitation on every possible incidence argument. In particular it is not a proof that all-root constraints are feasible.

## 3. The unclosed physical obligation

For two outside vertices b,c, the color of bc must be compatible with their supports and H. If bc is red, H[S_b intersect S_c] must have no triangle. If bc is blue, H[A minus (S_b union S_c)] must have no independent triple. Three and four outside vertices produce the remaining mixed K5/I5 conditions. The actual graph on B and the analogous conditions at all other roots must also agree.

Repeated supports from the lemma can violate both pair-color tests. Thus the lemma is not a construction of an arbitrarily large Ramsey graph. The missing compatibility is precisely why individual attachment validity cannot be promoted to whole-class feasibility or nonexistence.

No contradiction for these simultaneous constraints over all admissible H was obtained. No bounded attachment census, selected link pair, or new solver timeout is substituted for that obligation. The pass38 full formula remains the exact resumable target. The generally unrestricted point-link factorization already exists elsewhere in the repository; rebuilding its interface would not supply a new feasibility result.

## 4. Trial decision and portfolio comparison

Pass38 gave an exact complete-class formula but no proof. Pass39 supplies a decisive negative answer to the proposed local edge-loss step and a general limitation of the individual-attachment strengthening. Neither pass closes B4, proves a new unrestricted feasibility theorem, or retires a physical task. Both trial gates therefore fail, and there is no authorized automatic third pass.

The difficulty is now simultaneous realization, with neither a proved order bound nor a short complete obstruction. The local extremal witnesses prevent claiming a triangle-budget shortcut, while the support lemma prevents a capacity claim from the stated column conditions. More local profiles or a longer unchanged SAT run have no demonstrated route to the required result.

The campaign's R2 maximum-codegree cover has a complete finite outer normalization, although its initial physical runs are still UNKNOWN. R3 has source-certified endpoint edge exclusions using catalog overlaps and final exact proofs. Compared with those approaches, this structural trial has no measured class closure and no short route to one. The appropriate high-level recommendation is to reassign the structural slot within R(5,5), preserving this exact B4 checkpoint as a dormant dependency. This does not prescribe another researcher's execution method or operate its queue.

No fourth trial, adjacent profile campaign, new problem selection, or mathematical Discovery Net claim follows from this checkpoint. The earlier core-exchange, mixed-q7 redirect, monotone-chain, Property B, critical-graph, and order-54 archives remain intact.
