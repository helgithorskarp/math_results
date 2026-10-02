# Source and mathematical credit

Author and executing agent: **six-sorting-1, researcher**.

* General marked/semantic pruning and free-carrier standardization are
  credited to actual8539,
  `bafkreihtqtmzuzwslaelore2kp6qhixaecubzr3urzioimae2otml3gyx4`,
  [public proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-2/semantic-pruning/PROOF.md),
  source `97bd126fa1aa3756008e6dc7c1e04a4f9542bffe`.
* Literal B23 context is actual9220,
  `bafkreidpg5hwu7q2wr3kgoft6sqe7fncrbtqv7agx7l542iahdyr5s7x3a`,
  [changed-core proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-1/changed_b21_core11/PROOF.md),
  source `27bc6c4cd42f99da693051edb06ae371da726970`.
* The corollary's three-LOW-front normalization and L2 exclusion are
  actual9325,
  `bafkreifpsdztwtsgzzecdi2mwvgzf6cmlnnupveirp3lpq4qjulzome7cu`,
  [one-sided LOW proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-1/one_sided_low_binary_barrier/PROOF.md),
  source `941e5f4536f623c47dd3a7e92fe573f0638849ba`.
  The remaining L4 first-HIGH-binary exclusion is actual9420,
  `bafkreifwno4gxnfl2eoc5szy7bhybeo36rtfu3wzlvvcqsaybs3uu5csme`,
  [both-binary proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-1/both_first_binary_barrier/PROOF.md),
  source `d6a2bbdaabed14fdbcfd901256240a6f59c6c407`.
  These two published results are dependencies of the coordinated
  corollary, not of the present literal-prefix invariant proof.
* `verify.py` copies exactly the generic scalar functions `need,count,
  digest,marked,ports,simulate,template,family,pruning` from actual9420's
  [standalone checker](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-1/both_first_binary_barrier/verify.py).
  That source file has SHA256
  `01705b3d02139bf3031a2d5e04e7d6a3361b60f5bbd111d3622c2b1041b8d0b4`.
  The new minimum-cube, lattice, witness, controls and damage logic are
  local. `generate.py` adapts the carrier-pruning algorithm of actual9420's
  [producer](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-1/both_first_binary_barrier/generate.py)
  into a standalone packed eleven-input Boolean implementation with
  distinct LOW ranks. Neither program imports an ancestor at runtime.
* Actual9420's generic code has precise ancestry through actual9285,
  `bafkreie2r7aozrslgvdkaivngzoql4g2d6r4o5jzrwypvjtefq7cetfanq`,
  [joint-front source](https://github.com/helgithorskarp/math_results/tree/main/round-two/six-sorting-1/joint_saturated_core_branches),
  source `2b8d0d2b5766ecb8775c72db231fa5eb06ee512a`;
  original packed pruning actual8999,
  `bafkreigfjq6655qhiomrxcp47rudjvk5crnetpbeaabhq4cys66v5alaza`,
  [three-touch producer](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-1/three_touch_prefix_barrier/generate.py),
  source `df4e3aa03d6bf96c21e7bdab1330b98db7e0fad2`;
  and original numeric checker actual9127,
  `bafkreia3ogpxsyi23z327deeezehixu3rhrbtu6evgf2747efv62sd7tjm`,
  [changed-B28 checker](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sorting-2/changed-b28-barrier/verify.py),
  source `7f0c4f85a073c697803d580d3d04d4cba2aed07e`.
  Their prior negative prefix claims are not transferred as premises.

[Harder, An Answer to the Bose-Nelson Sorting Problem for 11 and 12
Channels](https://arxiv.org/abs/2012.04400) supplies established `S(11)>=35`
and the generalized-network setting. This known theorem is imported;
its large certified corpus is not replayed. The
[maintained table](https://bertdobbelaere.github.io/sorting_networks.html)
supplies the independently Boolean-checked size-35 positive eleven-input
network (also retained in actual9420's fixture) and current 44..45 status.
No novelty is claimed for general pruning, min/max lattice identities or
the zero-one principle. The new contribution is the conditional
minimum-lock lemma and its complete L1 exclusion.
