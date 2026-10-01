"""Full entry comparison; this validation is separate from verify.py."""
import json
import census
import verify


def main():
    star_masks = set(census.enumerate_stars())
    edge_masks = verify.binary_census()
    verify.need(star_masks == edge_masks, 'Complete labeled domains disagree')
    for mask in star_masks:
        direct_graph, direct_matrix, triangles = verify.literal_core(mask)
        adjacency = census.neighbors(mask)
        formula_matrix = census.pair_upper(adjacency)
        verify.need(formula_matrix == direct_matrix, 'A literal matrix entry differs')
        verify.need(all(direct_graph[i][j] == (j in adjacency[i])
                        for i in range(10) for j in range(10)), 'A core edge differs')
        verify.need(triangles == sum(len(adjacency[i] & adjacency[j])
                                    for i in range(10) for j in adjacency[i]) // 6,
                    'Triangle counts disagree')
    print(json.dumps({'complete_mask_sets_equal': True,
                      'labeled_graphs': len(star_masks),
                      'pair_matrix_entries_compared': 100 * len(star_masks),
                      'adjacency_entries_compared': 100 * len(star_masks)}, sort_keys=True))


if __name__ == '__main__':
    main()
