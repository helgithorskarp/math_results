#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

constexpr unsigned kOrder = 43;
constexpr unsigned kDistanceCount = 21;
constexpr std::uint32_t kStateCount = std::uint32_t{1} << kDistanceCount;
constexpr std::uint32_t kFullMask = kStateCount - 1;

using Vertices = std::array<unsigned, 5>;

unsigned cyclic_length(unsigned x, unsigned y) {
    const unsigned forward = (x + kOrder - y) % kOrder;
    return std::min(forward, kOrder - forward);
}

std::uint32_t distance_mask(const Vertices& vertices) {
    std::uint32_t mask = 0;
    for (unsigned i = 0; i < vertices.size(); ++i) {
        for (unsigned j = i + 1; j < vertices.size(); ++j) {
            const unsigned length = cyclic_length(vertices[i], vertices[j]);
            if (length == 0 || length > kDistanceCount) {
                throw std::logic_error("invalid cyclic length");
            }
            mask |= std::uint32_t{1} << (length - 1);
        }
    }
    return mask;
}

std::vector<std::uint32_t> five_set_orbit_frequencies() {
    std::vector<std::uint32_t> frequency(kStateCount, 0);
    std::uint64_t anchored_count = 0;
    for (unsigned a = 1; a < kOrder; ++a) {
        for (unsigned b = a + 1; b < kOrder; ++b) {
            for (unsigned c = b + 1; c < kOrder; ++c) {
                for (unsigned d = c + 1; d < kOrder; ++d) {
                    ++frequency[distance_mask({0, a, b, c, d})];
                    ++anchored_count;
                }
            }
        }
    }
    if (anchored_count != 111930) {
        throw std::logic_error("anchored five-set count mismatch");
    }

    // Every translation orbit is free: a nonzero translation of Z_43 has
    // order 43 and cannot preserve a set of size five.  Each orbit therefore
    // has exactly five translates containing zero.
    std::uint64_t orbit_count = 0;
    for (std::uint32_t& value : frequency) {
        if (value % 5 != 0) {
            throw std::logic_error("distance-mask frequency not divisible by five");
        }
        value /= 5;
        orbit_count += value;
    }
    if (orbit_count != 22386) {
        throw std::logic_error("translation-orbit count mismatch");
    }
    return frequency;
}

std::vector<std::uint32_t> subset_zeta(std::vector<std::uint32_t> values) {
    for (unsigned bit = 0; bit < kDistanceCount; ++bit) {
        const std::uint32_t flag = std::uint32_t{1} << bit;
        for (std::uint32_t mask = 0; mask < kStateCount; ++mask) {
            if ((mask & flag) != 0) {
                values[mask] += values[mask ^ flag];
                if (values[mask] > 22386) {
                    throw std::overflow_error("zeta entry exceeds total orbit count");
                }
            }
        }
    }
    return values;
}

std::uint32_t mask_from_lengths(const std::vector<unsigned>& lengths) {
    std::uint32_t mask = 0;
    for (const unsigned length : lengths) {
        if (length == 0 || length > kDistanceCount) {
            throw std::invalid_argument("length outside 1,...,21");
        }
        mask |= std::uint32_t{1} << (length - 1);
    }
    return mask;
}

std::vector<unsigned> lengths_from_mask(std::uint32_t mask) {
    std::vector<unsigned> lengths;
    for (unsigned length = 1; length <= kDistanceCount; ++length) {
        if ((mask & (std::uint32_t{1} << (length - 1))) != 0) {
            lengths.push_back(length);
        }
    }
    return lengths;
}

std::uint32_t multiply_mask(std::uint32_t mask, unsigned multiplier) {
    std::uint32_t result = 0;
    for (unsigned length = 1; length <= kDistanceCount; ++length) {
        if ((mask & (std::uint32_t{1} << (length - 1))) == 0) {
            continue;
        }
        unsigned residue = (multiplier * length) % kOrder;
        residue = std::min(residue, kOrder - residue);
        result |= std::uint32_t{1} << (residue - 1);
    }
    if (std::popcount(result) != std::popcount(mask)) {
        throw std::logic_error("multiplier did not permute distance classes");
    }
    return result;
}

void write_lengths(std::ostream& output, std::uint32_t mask) {
    output << '[';
    bool first = true;
    for (const unsigned length : lengths_from_mask(mask)) {
        if (!first) {
            output << ',';
        }
        first = false;
        output << length;
    }
    output << ']';
}

void write_histogram(
    std::ostream& output,
    const std::map<std::uint32_t, std::uint64_t>& histogram,
    unsigned indent
) {
    output << "{\n";
    std::size_t emitted = 0;
    for (const auto& [key, value] : histogram) {
        output << std::string(indent + 2, ' ') << '\"' << key << "\": " << value;
        if (++emitted != histogram.size()) {
            output << ',';
        }
        output << '\n';
    }
    output << std::string(indent, ' ') << '}';
}

void write_certificate(
    const std::string& path,
    const std::vector<std::uint32_t>& frequency,
    const std::vector<std::uint32_t>& zeta,
    const std::map<std::uint32_t, std::uint64_t>& objective_histogram,
    const std::vector<std::uint32_t>& minimizers,
    std::uint32_t canonical,
    std::uint32_t exoo
) {
    std::map<std::uint32_t, std::uint64_t> frequency_histogram;
    for (const std::uint32_t value : frequency) {
        if (value != 0) {
            ++frequency_histogram[value];
        }
    }
    std::map<std::uint32_t, std::uint64_t> size_histogram;
    for (const std::uint32_t mask : minimizers) {
        ++size_histogram[std::popcount(mask)];
    }

    std::ofstream output(path);
    if (!output) {
        throw std::runtime_error("could not open output certificate");
    }
    output << "{\n";
    output << "  \"format\": \"circulant43-k5-classification-v1\",\n";
    output << "  \"order\": 43,\n";
    output << "  \"distance_class_count\": 21,\n";
    output << "  \"coloring_count\": 2097152,\n";
    output << "  \"five_set_count\": 962598,\n";
    output << "  \"five_set_translation_orbit_count\": 22386,\n";
    output << "  \"distinct_distance_masks\": "
           << std::count_if(frequency.begin(), frequency.end(), [](std::uint32_t x) {
                  return x != 0;
              })
           << ",\n";
    output << "  \"distance_mask_orbit_multiplicity_histogram\": ";
    write_histogram(output, frequency_histogram, 2);
    output << ",\n";
    output << "  \"minimum_monochromatic_five_set_orbits\": 1,\n";
    output << "  \"minimum_monochromatic_K5_count\": 43,\n";
    output << "  \"minimizing_coloring_count\": " << minimizers.size() << ",\n";
    output << "  \"minimizing_red_length_count_histogram\": ";
    write_histogram(output, size_histogram, 2);
    output << ",\n";
    output << "  \"effective_multiplier_color_swap_group_order\": 42,\n";
    output << "  \"minimizing_symmetry_orbit_count\": 1,\n";
    output << "  \"canonical_minimizer_red_lengths\": ";
    write_lengths(output, canonical);
    output << ",\n";
    output << "  \"exoo_red_lengths\": ";
    write_lengths(output, exoo);
    output << ",\n";
    output << "  \"canonical_from_exoo\": {\"multiplier\": 20, \"color_swapped\": true},\n";
    output << "  \"exoo_red_orbits\": " << zeta[exoo] << ",\n";
    output << "  \"exoo_blue_orbits\": " << zeta[kFullMask ^ exoo] << ",\n";
    output << "  \"objective_orbit_histogram\": ";
    write_histogram(output, objective_histogram, 2);
    output << ",\n";
    output << "  \"minimizers\": [\n";
    for (std::size_t index = 0; index < minimizers.size(); ++index) {
        const std::uint32_t mask = minimizers[index];
        output << "    {\"red_lengths\": ";
        write_lengths(output, mask);
        output << ", \"red_orbits\": " << zeta[mask]
               << ", \"blue_orbits\": " << zeta[kFullMask ^ mask] << '}';
        if (index + 1 != minimizers.size()) {
            output << ',';
        }
        output << '\n';
    }
    output << "  ]\n";
    output << "}\n";
    if (!output) {
        throw std::runtime_error("failed while writing output certificate");
    }
}

}  // namespace

int main(int argc, char** argv) {
    try {
        if (argc != 2) {
            std::cerr << "usage: " << argv[0] << " OUTPUT.json\n";
            return 2;
        }

        const auto frequency = five_set_orbit_frequencies();
        const auto zeta = subset_zeta(frequency);
        std::map<std::uint32_t, std::uint64_t> objective_histogram;
        std::uint32_t minimum = 22387;
        std::vector<std::uint32_t> minimizers;
        for (std::uint32_t mask = 0; mask < kStateCount; ++mask) {
            const std::uint32_t objective = zeta[mask] + zeta[kFullMask ^ mask];
            ++objective_histogram[objective];
            if (objective < minimum) {
                minimum = objective;
                minimizers.assign(1, mask);
            } else if (objective == minimum) {
                minimizers.push_back(mask);
            }
        }
        if (minimum != 1 || minimizers.size() != 42) {
            throw std::logic_error("unexpected minimum classification");
        }

        const std::uint32_t exoo = mask_from_lengths({1, 2, 7, 10, 12, 13, 14, 16, 18, 20, 21});
        std::set<std::uint32_t> exoo_orbit;
        for (unsigned multiplier = 1; multiplier <= kDistanceCount; ++multiplier) {
            const std::uint32_t image = multiply_mask(exoo, multiplier);
            exoo_orbit.insert(image);
            exoo_orbit.insert(kFullMask ^ image);
        }
        const std::set<std::uint32_t> minimum_set(minimizers.begin(), minimizers.end());
        if (exoo_orbit.size() != 42 || exoo_orbit != minimum_set) {
            throw std::logic_error("minimizers are not the full Exoo symmetry orbit");
        }
        const std::uint32_t canonical = *minimum_set.begin();
        if ((kFullMask ^ multiply_mask(exoo, 20)) != canonical) {
            throw std::logic_error("declared canonical Exoo map is incorrect");
        }

        write_certificate(
            argv[1], frequency, zeta, objective_histogram, minimizers, canonical, exoo
        );
        std::cout << "PASS complete circulant K_43 classification\n";
        std::cout << "colorings=2097152 five_set_orbits=22386 distance_masks=10437\n";
        std::cout << "minimum_orbits=1 minimum_K5=43 minimizers=42 symmetry_orbits=1\n";
        std::cout << "canonical_red_lengths=";
        write_lengths(std::cout, canonical);
        std::cout << "\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "ERROR: " << error.what() << '\n';
        return 1;
    }
}
