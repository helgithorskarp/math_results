# Independent audit: four-power no-binomial pencils

## Verdict

**ACCEPT with high confidence** at mathematical target commit
`5799dfd83ddcc127f3a53ecd8c35787e7bb291f6`.

This package is a clean-room exact review of
`hadwiger_nelson_four_power_no_binomial_pencils`.  It verifies the bounded
claim that all 54 homogeneous full pencils in the four-power `A5(z)` interface
whose five directions have support at least three are nonconcurrent, and that
every one of the 2,988 real anchor parameters has physical chromatic number
exactly three.

The checker imports no target-package code.  It independently:

1. enumerates `PG(3,4)` and its 357 projective lines, obtaining exactly the 54
   support-`(3,3,3,3,4)` pencils and their 110,592 Eisenstein-unit lifts;
2. rebuilds all 2,801 displacement classes, 2,797 unit-distance event curves,
   29,403 labelled pairs, and 243 universal edges from the definition of
   `A5(z)`;
3. eliminates `x`, whereas both target generators eliminate `y`, and computes
   exact fibre gcds over quotient fields;
4. matches all reverse-elimination components to all 864 target anchor pairs;
5. uses a standard-library rational Sturm chain to recount real roots;
6. reconstructs collision quotients and complete physical unit-distance graphs
   exactly, then checks a descended 3-colouring and the surviving unit triangle.

This is **not** a smaller five-chromatic plane construction.  It is a verified
restricted-family exclusion.  It says nothing about binomial-containing or
nonhomogeneous pencils, other `A5` interfaces, or arbitrary plane unit-distance
graphs.

See `PROOF.md`, `REPRODUCE.md`, and `VALIDATION.md` for the trust boundary and
the replay transcript.
