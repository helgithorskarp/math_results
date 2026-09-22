# Sources and attribution

Checked 2026-09-22. The new claim is the full height-at-most-three
construction with coordinatewise optimal move counts, for bounded posets
of arbitrary order. Its sharp-height consequences use prior existence
results. Novelty is relative to the sources inspected, not a priority
certification.

* **[AMS]** Antoine Amarilli, Mikaël Monet and Dan Suciu,
  [The Non-Cancelling Intersections Conjecture](https://arxiv.org/html/2401.16210).
  Proposition 4.7 gives the signed multiplicity identity in the full
  intersection-lattice representation. Section 7 discusses sign coherence
  and left linearity as strengthenings. The lower-bound argument and these
  objectives are prior work.
* **[AM]** Antoine Amarilli's 2019 question and Mikaël Monet's 2020 answer,
  [Lighting up all elements of a poset by toggling upsets](https://cstheory.stackexchange.com/questions/45679/lighting-up-all-elements-of-a-poset-by-toggling-upsets).
  This uses the dual orientation. The answer proves deletion/insertion
  reductions and a crown-free/dismantlable sufficient condition. Its
  single-element substitution is a predecessor of the splicing technique;
  it does not state the full height-three theorem proved here.
* **[AJM]** Antoine Amarilli, Louis Jachiet and Mikaël Monet,
  [Which Sets Can be Expressed as Disjoint Union and Subset Complement Without Möbius Cancellations?](https://mikael-monet.net/share/note.pdf).
  This author-hosted note formulates cancellation-free expressions and
  cone-reachability and reports finite Boolean-lattice experiments. These
  are context, not dependencies of our construction.
* **[W1]** Hermann Wilhelm,
  [The Non-Cancelling-Intersections Conjecture Fails for Left-Linear Trees](https://arxiv.org/html/2608.19414).
  Definition 3.1 fixes the game used here. Section 5.1 explicitly describes
  a depth-four family, and Corollary 7.4 proves unwinnability for suitable
  members. It supplies the upper side of the sharp-height corollary.
* **[W2]** Hermann Wilhelm,
  [Refutation of the Non-Cancelling Intersections Conjecture](https://arxiv.org/html/2608.27416).
  Section 2 identifies the same depth-four family. Theorem 1.1 (proved in
  Section 8) excludes unrestricted winning dot-algebra trees for suitable
  markings. Thus the general NCI conjecture is refuted; it is not presented
  here as an open conjecture.

The Discovery Net selection point was the structural-pruning frontier of
the finite order-15 audit, artifact
`bafkreie3n2ri6fqrssazh634e6pfzkqlerlbtyoviam5asx34i3jpwucdm`, under the
minimum-order unwinnable-lattice problem
`bafkreiekhqdhv76zckh7tv4twtazwyhrjwjwrtha27a54lodtkxkx4nr2i`.
That enumeration is not used in this proof. The earlier shellable-complex
and stellar-subdivision results give different sufficient classes.

Targeted graph, author-discussion, primary-paper, and height/rank searches
found no matching full theorem. They do not establish exhaustive historical
coverage. In particular the Möbius identity, cancellation-free objective,
single-element substitution and height-four counterexample existence must
not be attributed to this package.
