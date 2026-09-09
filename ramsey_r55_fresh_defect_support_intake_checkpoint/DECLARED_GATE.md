# Fresh unrestricted candidates and complete defect-support repair families

This is one bounded candidate/construction-and-certificate milestone for
R(5,5), independent of every parked source and of the q10 survivor inputs.

Candidate intake: exactly32 fresh deterministic random starts on all903
physical pairs of43 vertices, with524288 edge proposals per start in eight
temperature cycles, followed by strict improving descent. No prescribed
degree, symmetry, catalog, historical graph, or fixed neighborhood is used.
Retain the eight best distinct complete physical graphs with at most16
monochromatic five-sets; ties are broken by seed index. If fewer than eight
qualify, checkpoint the failed intake gate without enlarging the schedule
or loosening the quality threshold. A zero-defect graph is independently
checked immediately and is a target outcome instead.

For each retained graph G, let U(G) be the union of the ten physical edges
of every monochromatic five-set of G, in either color. Its complete target
family consists of EVERY43-vertex graph agreeing with G off U(G), with all
edges in U(G) independently free. There is no restriction on the number or
direction of changed edges. Seal the eight centers/supports before solving.
Require disjoint repair subcubes, witnessed by an oppositely colored pair
fixed in both for each pair of centers; otherwise checkpoint intake failure.
The exact whole-family size is then sum_G 2^|U(G)|.

First coherent output gate: a certified good43, or checked exclusion of
the entire union of all eight complete physical repair families. Individual
local witnesses, a partial exclusion roster, or UNKNOWN does not satisfy
this gate. An exclusion means every good43 differs from the corresponding
center on at least one pair outside its original defect support. It says
nothing about an edit ball, all43 graphs, isomorphism classes or global
nonexistence.

Encoding: one Boolean red-edge variable for every pair in U(G), all other
pairs fixed to G. For every physical five-set and each color, simplify the
clause forbidding that monochromatic five-set. Record a physical premise
for each remaining clause. SAT is decoded and checked on all five-sets;
UNSAT requires an independently checked proof and a separate premise audit.
Use a single plain CaDiCaL call per sealed family, seed0, at most60 seconds
and100000 conflicts. No higher cap, alternative solver, widened support or
nearby family is launched if this bounded block leaves UNKNOWN. Any work
already in flight is finished and checkpointed first.

These numerical intake and solve limits delimit a falsifiable experiment;
they are not claims of exhaustive search over the random-start domain.
The mathematical family becomes exact once the center registry is sealed.
All q10 decisions and h4021 integration remain with team-r55-1. h4009,
h4015, h4029/h4037 and h4035 remain preserved but are not computation inputs.
