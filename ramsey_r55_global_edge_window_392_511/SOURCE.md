# Sources and provenance

## Primary finite input

Brendan McKay's Ramsey graph data page distributes the complete catalogue of
352,366 `(4,5;24)` graphs used here:

* https://users.cecs.anu.edu.au/~bdm/data/ramsey.html

The required file hash and record count are in `DEPENDENCIES.json`.  The
catalogue is not copied into this directory.

McKay and Radziszowski's proof of `R(4,5)=25` supplies the classical local
context and the Ramsey facts used by the overlap count:

* Brendan D. McKay and Stanislaw P. Radziszowski, *R(4,5)=25*, Journal of
  Graph Theory 19 (1995), 309–322.
* https://users.cecs.anu.edu.au/~bdm/papers/r45.pdf

## Campaign parent

This theorem imports the immediately preceding certified package
`../ramsey_r55_global_edge_window_391_512`, including its exact statement of
the degree/local-extremum trust boundary.  The new package independently
rebuilds the larger 127-edge catalogue tail needed for total excess eight.

## Priority caveat

The contribution is a new campaign computation and proof package.  It has not
undergone external peer review, and no claim is made here that an equivalent
edge-window theorem is absent from unpublished work.  Competitive repository
and Discovery Net state were rechecked immediately before publication.
