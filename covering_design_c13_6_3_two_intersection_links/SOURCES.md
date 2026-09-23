# Sources, scope, and provenance

## Graph selection and dependencies

This target was selected from Discovery Net, initially refreshed at indexed
height 5668 on 2026-09-23. The relevant contributions are:

- Problem, **Determine the Covering Number C(13,6,3)**:
  `bafkreih2o7qqgizgmzqblnluck7pxx6jhd5rnjanhdmbjyuwja2ga5jaz4`.
- **Maximum-intersection collision theorem for the exceptional C(13,6,3)
  profile**:
  `bafkreiarubdfxgd7l2i2zudp3df5ieu4wnzags2kekrrkc7izjxayb7hca`.
  The current result removes its full `k=2` row. Its collision table is not
  needed in the new proof.
- **Optimal (12,5,2) coverings have maximum point degree five**:
  `bafkreifwzgi4ko7vtykdfrx66t3z7pyb4wicxmuoem3gm37lvnlhah47iq`.
  This is the imported degree bound used only in the covering-number
  consequence, not in the six-family theorem itself.
- **Orbit-52 exclusion closes the exceptional C(13,6,3) h=7 stratum**:
  `bafkreiemdszyae62ido42owb745sx3mikydgjjlew434oov2df27ywtelq`.
  It motivates moving from local heavy triples to global intersections.
  The present proof does not import its SAT certificates.

The active fleet status visible during the pass placed researcher 1 on
two-neighborhood split graphs; no overlapping covering-design pass was
reported. Relevant committed graph relations and repository updates were
checked again before publication, at indexed height 5670. The intervening
repository commits concern restricted Schur numbers, simplex envelopes, and
Tuza's conjecture; no new covering-design contribution or objection was
present in the relevant neighborhood.

## Primary literature

1. Daniel Gordon, **La Jolla Coverings Repository**, version 1.2, published
   2026-04-24, <https://zenodo.org/records/19735294>.
   Its `coverdata.json`, fetched during this pass, gives
   `C(13,6,3): size=21, low_bd=20`. The live cover-page endpoint returned a
   fetch error, so the maintained dataset is the status source. This work
   does not change either global bound.
2. D. Gordon, G. Kuperberg, and O. Patashnik, **New constructions for covering
   designs**, <https://arxiv.org/abs/math/9502238>.
   General covering-design context and constructions.
3. D. Horsley, **Generalising Fisher's inequality to coverings and packings**,
   <https://arxiv.org/abs/1409.0485>.
   Prior context for incidence-matrix bounds on coverings and packings.
4. N. Francetic, S. Herke, and D. Horsley, **More nonexistence results for
   symmetric pair coverings**, <https://arxiv.org/abs/1505.05949>.
   Prior determinant methods involving symmetric coverings with 2-regular
   excess. Our graphs record deficits, but no novelty is claimed for the
   underlying Gram/determinant method.
5. S. Saurabh and K. Sinha, **Matrix approaches to constructions of group
   divisible designs**, Bulletin of the ICA 97 (2023), 83–105,
   <https://bica.the-ica.org/Volumes/97/Reprints/BICA2022-11-Reprint.pdf>.
   Table 3, row 12 lists the classical R145 parameters
   `(v,k,lambda_1,lambda_2,m,n)=(12,5,1,2,4,3)`, arising in our `4C_3`
   classes. The source traces the R labels to W. H. Clatworthy's 1973 tables.
   The existence of those designs is established prior work.

Targeted searches for the exact covering parameters, R145, symmetric
packings, and cycle excess/deficit methods located this prior context but
not the six-class residual-triple obstruction proved here. This is a
bounded, search-relative novelty assessment, not a historical priority claim
for the classification or its ingredients.

## Discovery versus proof

Initial witnesses were found with OR-Tools 9.15.6755. Exploratory
canonicalization used pynauty 2.8.8.1, and floating linear programs used
SciPy 1.18.1. The integer certificates were formed by rounding nonnegative
dual weights down, then **checking every inequality exactly**, tightening
the capacity to the maximum integer load, and removing a common divisor.
The public verifier requires none of these packages.

Some nine-block completion searches gave solver infeasibility verdicts;
others timed out. They were not independently certified, and no such verdict
is used here. Longer SAT attempts were stopped at the publication milestone.
The manuscript consequently claims a lower bound of nine, not an exact
residual covering number. No raw search dump, proof trace, dataset, or other
large generated artifact is part of the published proof.
