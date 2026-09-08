"""Small independent controls for the finite normalization and set argument."""
from itertools import product
import model


def expect_error(action):
    try:
        action()
    except (TypeError, ValueError):
        return
    raise ValueError('malformed control was accepted')


def main():
    g40, g49, _, _, _ = model.inputs()
    x = g40[1]
    y, ybar = model.spindle_targets(x)
    if model.assembly.norm(x) != model.assembly.scalar(9216):
        raise ValueError('wrong terminal radius')
    for candidate in (y, ybar):
        if model.assembly.norm(candidate) != model.assembly.scalar(9216):
            raise ValueError('wrong second terminal radius')
        if model.assembly.distance(x, candidate) != model.assembly.scalar(1296):
            raise ValueError('outer terminals are not unit-separated')
    if y == ybar:
        raise ValueError('the two circle intersections coincide')

    choices = list(product((False, True), repeat=5))
    cases = list(model.outer_cases())
    if len(choices) != 32 or [c for c, _, _ in cases] != choices:
        raise ValueError('outer normalization is incomplete')

    kernel, copies = model.normalized_g49_kernel(g49)
    if not all(kernel <= copy for copy in copies):
        raise ValueError('intersection is not contained in every option')
    brute = {p for p in set.union(*(set(copy) for copy in copies))
             if all(p in copy for copy in copies)}
    if brute != set(kernel):
        raise ValueError('definition-level intersection mismatch')

    expect_error(lambda: model.assembly.frame(g49[0], g49[1], g49[0], g49[0], 4752))
    expect_error(lambda: model.canonical_union(0))
    print('controls passed: 32 outer cases, four-option kernel, two rejected malformed inputs')


if __name__ == '__main__':
    main()
