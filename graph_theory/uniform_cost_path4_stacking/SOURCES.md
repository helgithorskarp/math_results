# Sources and dependencies

## Primary literature

- Tamas Csernak and Lajos Soukup, *Stacking and clearing in graph pebbling*,
  arXiv:2604.22341v1 (2026), <https://arxiv.org/abs/2604.22341>.
  This defines the ordinary cost-two stacking problem and proves
  `stack(P_n)=2^n-1`.

## Discovery Net dependencies

- `bafkreigcl7n5fvmcv3voxn43tipwwit4457btjkjduz3kzx3zmekkjcnt4`,
  *Uniform-cost tree stacking has an exact signed-message criterion*.
  The present proof uses its necessary-and-sufficient target-score theorem.
- `bafkreib46bthe4tw3b3rcfmnfachhnpxy2iiljgkeyukklracv2xrqebca`,
  *Sharp eventual stacking threshold and all largest obstructions for
  uniform-cost stars*.  The `P3` upper bound used here is also reproved in
  the README so that the new reduction can be checked locally.
- `bafkreibtvcodpo5ig5sgyqllazw7mco4rxhzk3nhgotmrwqkupjjxoqwz4`,
  *A universal non-stackable configuration for every uniform-cost tree*.
  Its path obstruction motivates the equality example; the README verifies
  the needed messages directly.

## Search boundary

Targeted searches on 20 September 2026 covered the title/abstract and
available versions of the primary paper above, and searches for uniform-cost
or higher-cost stacking on paths.  They exposed ordinary graph pebbling and
`t`-pebbling literature, but no source stating the chosen-target uniform
move-cost result proved here.  No global priority claim is made.
