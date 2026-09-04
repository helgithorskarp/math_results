// Reuse the audited exact field and geometry routines, keeping the earlier
// finite-stratum program and its source digest unchanged.
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wreturn-type"
#pragma GCC diagnostic ignored "-Wunused-function"
#define main prior_census_main
#include "../hadwiger_nelson_parts509_two_overlap_cross_census/census.cpp"
#undef main
#pragma GCC diagnostic pop
#include "witness_masks.hpp"

using Histogram = std::map<std::size_t, std::pair<std::uint64_t, std::uint64_t>>;

static void emit_histogram(const Histogram& histogram) {
    std::cout << '[';
    bool first = true;
    for (const auto& [edges, counts] : histogram) {
        if (!first) std::cout << ',';
        first = false;
        std::cout << '[' << edges << ',' << counts.first << ',' << counts.second << ']';
    }
    std::cout << ']';
}

static void emit_field(std::ostream& output, const Field& field) {
    output << '[';
    for (std::size_t i = 0; i < field.size(); ++i) {
        if (i) output << ',';
        output << field[i];
    }
    output << ']';
}

static Constraints overlap_constraints(const std::vector<std::uint32_t>& overlaps) {
    Constraints result;
    for (auto pair : overlaps) result.emplace_back(pair / 136, pair % 136);
    return result;
}

static Constraints edge_constraints(const std::vector<std::uint32_t>& edges) {
    Constraints result;
    for (auto edge : edges) {
        const std::size_t p = edge / 510, labelled_q = edge % 510;
        if (p >= 374 || labelled_q < 374) {
            throw std::runtime_error("genuinely new edge has an identified endpoint");
        }
        result.emplace_back(p, labelled_q - 374);
    }
    return result;
}

int main(int argc, char** argv) {
    if (argc != 4 && argc != 6) {
        std::cerr << "usage: census_all POINTS.tsv COLOUR_LIBRARIES.txt RESIDUAL.jsonl"
                     " [FIRST_ORIENTATION END_ORIENTATION]\n";
        return 2;
    }
    const std::size_t first = argc == 6 ? std::stoull(argv[4]) : 0;
    const std::size_t end = argc == 6 ? std::stoull(argv[5]) : 2840;
    if (first >= end || end > 2840) throw std::runtime_error("invalid orientation range");
    std::ofstream residual(argv[3]);
    if (!residual) throw std::runtime_error("cannot open residual output");
    check_radical_bounds();
    const auto all = read_points(argv[1]);
    const std::vector<Point> left(all.begin(), all.begin() + 374);
    std::vector<Point> small{all[0]};
    small.insert(small.end(), all.begin() + 374, all.end());
    if (std::set<Point>(left.begin(), left.end()).size() != 374
        || std::set<Point>(small.begin(), small.end()).size() != 136) {
        throw std::runtime_error("gadget point census mismatch");
    }
    const auto left_edges = internal_edges(left), small_edges = internal_edges(small);
    if (edge_count(left_edges) != 1860 || edge_count(small_edges) != 564) {
        throw std::runtime_error("gadget edge census mismatch");
    }
    const auto libraries = read_colour_libraries(argv[2]);
    validate_colour_library(libraries.left, left_edges);
    validate_colour_library(libraries.small, small_edges);
    if (libraries.left.size() != 135 || libraries.small.size() != 194) {
        throw std::runtime_error("colour library census mismatch");
    }
    const WitnessMasks masks(libraries.small);
    if (masks.expanded.size() != 4656 || masks.words != 73) {
        throw std::runtime_error("expanded library census mismatch");
    }
    const auto lv = directed_vectors(left), sv = directed_vectors(small);
    if (vector_count(lv) != 11650 || vector_count(sv) != 1666) {
        throw std::runtime_error("directed vector census mismatch");
    }
    const auto orientation_set = enumerate_orientations(lv, sv);
    const std::vector<Orientation> orientations(orientation_set.begin(), orientation_set.end());
    if (orientations.size() != 2840) throw std::runtime_error("orientation census mismatch");
    std::vector<std::pair<i64, i64>> offsets;
    for (i64 dx = -6; dx <= 6; ++dx) {
        for (i64 dy = -6; dy <= 6; ++dy) {
            if (bucket_offset_can_be_unit(dx, dy)) offsets.emplace_back(dx, dy);
        }
    }
    if (offsets.size() != 68) throw std::runtime_error("bucket offset census mismatch");
    std::cout << "{\"type\":\"header\",\"first\":" << first << ",\"end\":" << end
              << ",\"orientations\":2840,\"left_colourings\":135,\"small_colourings\":194"
                 ",\"expanded_small_colourings\":4656}\n";
    Histogram totals;
    std::uint64_t total_multi = 0, total_pairs = 0, total_checks = 0;
    std::uint64_t total_dense = 0, total_coloured = 0, total_unresolved = 0;
    for (std::size_t index = first; index < end; ++index) {
        const auto& orientation = orientations[index];
        std::vector<Point> image;
        for (const auto& point : small) image.push_back(transformed_numerator(orientation, point));
        std::unordered_map<Difference, std::vector<std::uint32_t>, DifferenceHash> differences;
        differences.reserve(left.size() * small.size() * 2);
        for (std::size_t p = 0; p < left.size(); ++p) {
            for (std::size_t q = 0; q < image.size(); ++q) {
                differences[cross_difference(left[p], image[q], orientation.denominator)]
                    .push_back(static_cast<std::uint32_t>(136 * p + q));
            }
        }
        std::uint64_t multi = 0, pairs = 0, checks = 0, coloured = 0, unresolved = 0;
        std::vector<const Difference*> translations;
        for (const auto& [difference, overlaps] : differences) {
            if (overlaps.size() >= 2) {
                ++multi;
                pairs += overlaps.size() * (overlaps.size() - 1) / 2;
            }
            if (overlaps.size() == 2) translations.push_back(&difference);
        }
        std::sort(translations.begin(), translations.end(), [](auto a, auto b) {
            return std::tie(a->x, a->y) < std::tie(b->x, b->y);
        });
        std::unordered_map<Bucket, std::vector<BucketNode>, BucketHash> grid;
        grid.reserve(differences.size() * 2);
        for (const auto& [difference, overlaps] : differences) {
            const auto x = radical_interval(difference.x), y = radical_interval(difference.y);
            grid[bucket(x, y, orientation.denominator)].push_back(
                BucketNode{&difference, &overlaps, x, y});
        }
        Histogram histogram;
        std::size_t dense_checks = 0;
        for (const Difference* translation_ptr : translations) {
            const auto& translation = *translation_ptr;
            const auto& overlaps = differences.at(translation);
            const auto tx = radical_interval(translation.x), ty = radical_interval(translation.y);
            const auto centre = bucket(tx, ty, orientation.denominator);
            std::vector<std::uint32_t> edges;
            for (const auto& [dx, dy] : offsets) {
                const auto found = grid.find(Bucket{centre.x + dx, centre.y + dy});
                if (found == grid.end()) continue;
                for (const auto& node : found->second) {
                    if (!interval_can_be_unit(tx, ty, node.x, node.y, orientation.denominator)) continue;
                    ++checks;
                    if (!unit_separated(translation, *node.difference, orientation.denominator)) continue;
                    for (auto pair : *node.pairs) {
                        const auto key = new_strict_edge_key(pair, overlaps, left_edges, small_edges);
                        if (key) edges.push_back(*key);
                    }
                }
            }
            std::sort(edges.begin(), edges.end());
            edges.erase(std::unique(edges.begin(), edges.end()), edges.end());
            // These samples bypass both spatial filters and test all 50,864 pairs.
            if (index % 137 == 0 && dense_checks == 0) {
                std::set<std::uint32_t> dense_edges;
                for (std::size_t p = 0; p < left.size(); ++p) {
                    for (std::size_t q = 0; q < image.size(); ++q) {
                        const auto difference = cross_difference(left[p], image[q], orientation.denominator);
                        if (!unit_separated(translation, difference, orientation.denominator)) continue;
                        const auto key = new_strict_edge_key(
                            static_cast<std::uint32_t>(136 * p + q), overlaps,
                            left_edges, small_edges);
                        if (key) dense_edges.insert(*key);
                    }
                }
                if (std::vector<std::uint32_t>(dense_edges.begin(), dense_edges.end()) != edges) {
                    throw std::runtime_error("dense cross-edge reconstruction mismatch");
                }
                ++dense_checks;
            }
            const auto witness = masks.find(libraries.left, overlap_constraints(overlaps),
                                            edge_constraints(edges));
            ++histogram[edges.size()].first;
            if (witness) {
                ++coloured;
                ++histogram[edges.size()].second;
            } else {
                ++unresolved;
                residual << "{\"orientation\":" << index << ",\"denominator\":"
                         << orientation.denominator << ",\"x\":";
                emit_field(residual, translation.x);
                residual << ",\"y\":";
                emit_field(residual, translation.y);
                residual << ",\"overlaps\":[" << overlaps[0] << ',' << overlaps[1]
                         << "],\"edges\":[";
                for (std::size_t i = 0; i < edges.size(); ++i) {
                    if (i) residual << ',';
                    residual << edges[i];
                }
                residual << "]}\n";
            }
        }
        for (const auto& [edges, count] : histogram) {
            totals[edges].first += count.first;
            totals[edges].second += count.second;
        }
        total_multi += multi; total_pairs += pairs; total_checks += checks;
        total_coloured += coloured; total_unresolved += unresolved; total_dense += dense_checks;
        std::cout << "{\"type\":\"orientation\",\"orientation\":" << index
                  << ",\"reflected\":" << (orientation.reflected ? "true" : "false")
                  << ",\"multi\":" << multi << ",\"pairs\":" << pairs
                  << ",\"two\":" << translations.size() << ",\"checks\":" << checks
                  << ",\"coloured\":" << coloured << ",\"unresolved\":" << unresolved
                  << ",\"dense_checks\":" << dense_checks << ",\"histogram\":";
        emit_histogram(histogram);
        std::cout << "}\n" << std::flush;
        if ((index + 1) % 100 == 0) {
            std::cerr << "processed=" << index + 1 << '/' << end
                      << " coloured=" << total_coloured << " unresolved=" << total_unresolved << '\n';
        }
    }
    if (first == 0 && end == 2840 && (total_multi != 2992078 || total_pairs != 17658256
        || total_coloured + total_unresolved != 2373802)) {
        throw std::runtime_error("full geometry census mismatch");
    }
    residual.flush();
    if (!residual) throw std::runtime_error("residual write failed");
    std::cout << "{\"type\":\"complete\",\"first\":" << first << ",\"end\":" << end
              << ",\"multi\":" << total_multi << ",\"pairs\":" << total_pairs
              << ",\"two\":" << total_coloured + total_unresolved
              << ",\"checks\":" << total_checks << ",\"coloured\":" << total_coloured
              << ",\"unresolved\":" << total_unresolved << ",\"dense_checks\":" << total_dense
              << ",\"histogram\":";
    emit_histogram(totals);
    std::cout << "}\n";
    return std::cout ? 0 : 1;
}
