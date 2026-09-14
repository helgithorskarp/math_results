#!/usr/bin/env python3
import json
import verify as v


def main():
    # Exactly representable points above, below and on the declared fold axis.
    zero = (0,)*8
    centre = tuple(x//2 for x in v.TWICE_C)
    above = (288,)+centre[1:]
    below = (-288,)+centre[1:]
    points, mapping, sides = v.fold([(zero, above), (zero, below), (zero, centre)])
    v.require(sides == [1, -1, 0] and mapping[0] == mapping[1] != mapping[2], 'fold control')
    v.require(len(points) == 2, 'collision control')
    for a, s in [(zero, 0), ((1,)+(0,)*7, 1), ((0, 1)+(0,)*6, 1),
                 ((-2, 1)+(0,)*6, -1), ((2, -1)+(0,)*6, 1)]:
        v.require(v.sign(a) == s, 'sign control')
    failures = 0
    for word in ['0', '00', '05', '01\n']:
        try:
            v.check_word(word, 2, [(0, 1)])
        except ValueError:
            failures += 1
        else:
            raise ValueError('bad colour word accepted')
    v.require(failures == 4, 'corruption controls')
    try:
        v.compute({})
    except ValueError:
        pass
    else:
        raise ValueError('empty certificate accepted')
    print(json.dumps(dict(all_checks=True, fold_collision_control=True,
                          sign_controls=5, rejected_bad_words=failures,
                          rejected_empty_certificate=True), sort_keys=True))


if __name__ == '__main__':
    main()
