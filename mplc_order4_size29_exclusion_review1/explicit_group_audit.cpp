#include <algorithm>
#include <array>
#include <cctype>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

using Mask64 = std::uint64_t;
using Count = std::uint64_t;

unsigned popcount64(Mask64 value) {
    unsigned result = 0;
    while (value != 0) {
        value &= value - 1;
        ++result;
    }
    return result;
}

unsigned popcount16(unsigned value) {
    unsigned result = 0;
    while (value != 0) {
        value &= value - 1;
        ++result;
    }
    return result;
}

class LevelsParser {
  public:
    explicit LevelsParser(std::string input) : input_(std::move(input)) {}

    std::array<std::vector<Mask64>, 8> parse() {
        const std::string marker = "\"levels\"";
        const auto marker_position = input_.find(marker);
        if (marker_position == std::string::npos ||
            input_.find(marker, marker_position + marker.size()) != std::string::npos) {
            throw std::runtime_error("expected exactly one levels field");
        }
        position_ = marker_position + marker.size();
        skip_space();
        expect(':');
        skip_space();
        expect('[');
        std::array<std::vector<Mask64>, 8> levels;
        for (unsigned level = 0; level < levels.size(); ++level) {
            skip_space();
            expect('[');
            skip_space();
            if (peek() != ']') {
                while (true) {
                    levels[level].push_back(parse_unsigned());
                    skip_space();
                    if (peek() != ',') {
                        break;
                    }
                    ++position_;
                    skip_space();
                }
            }
            expect(']');
            skip_space();
            if (level + 1 != levels.size()) {
                expect(',');
            }
        }
        skip_space();
        expect(']');
        return levels;
    }

  private:
    char peek() const {
        if (position_ >= input_.size()) {
            throw std::runtime_error("unexpected end of JSON");
        }
        return input_[position_];
    }

    void skip_space() {
        while (position_ < input_.size() &&
               std::isspace(static_cast<unsigned char>(input_[position_])) != 0) {
            ++position_;
        }
    }

    void expect(char wanted) {
        if (peek() != wanted) {
            throw std::runtime_error(std::string("expected '") + wanted + "'");
        }
        ++position_;
    }

    Mask64 parse_unsigned() {
        if (!std::isdigit(static_cast<unsigned char>(peek()))) {
            throw std::runtime_error("expected an unsigned integer");
        }
        Mask64 value = 0;
        while (position_ < input_.size() &&
               std::isdigit(static_cast<unsigned char>(input_[position_])) != 0) {
            const unsigned digit = static_cast<unsigned>(input_[position_] - '0');
            if (value > (std::numeric_limits<Mask64>::max() - digit) / 10) {
                throw std::runtime_error("integer overflow in input");
            }
            value = 10 * value + digit;
            ++position_;
        }
        return value;
    }

    std::string input_;
    std::size_t position_ = 0;
};

std::vector<std::array<unsigned, 4>> permutations4() {
    std::vector<std::array<unsigned, 4>> result;
    std::array<unsigned, 4> permutation{0, 1, 2, 3};
    do {
        result.push_back(permutation);
    } while (std::next_permutation(permutation.begin(), permutation.end()));
    return result;
}

std::vector<std::array<unsigned, 3>> permutations3() {
    std::vector<std::array<unsigned, 3>> result;
    std::array<unsigned, 3> permutation{0, 1, 2};
    do {
        result.push_back(permutation);
    } while (std::next_permutation(permutation.begin(), permutation.end()));
    return result;
}

using PointMap = std::array<unsigned char, 64>;

std::vector<PointMap> make_group() {
    const auto p4 = permutations4();
    const auto p3 = permutations3();
    std::vector<PointMap> group;
    group.reserve(6 * 24 * 24 * 24);
    for (const auto &coordinate_permutation : p3) {
        for (const auto &symbols0 : p4) {
            for (const auto &symbols1 : p4) {
                for (const auto &symbols2 : p4) {
                    const std::array<std::array<unsigned, 4>, 3> symbols{
                        symbols0, symbols1, symbols2};
                    PointMap mapping{};
                    for (unsigned point = 0; point < 64; ++point) {
                        const std::array<unsigned, 3> old{
                            point / 16, (point / 4) % 4, point % 4};
                        std::array<unsigned, 3> transformed{};
                        for (unsigned axis = 0; axis < 3; ++axis) {
                            transformed[axis] =
                                symbols[axis][old[coordinate_permutation[axis]]];
                        }
                        mapping[point] = static_cast<unsigned char>(
                            16 * transformed[0] + 4 * transformed[1] + transformed[2]);
                    }
                    group.push_back(mapping);
                }
            }
        }
    }
    if (group.size() != 82944) {
        throw std::runtime_error("wrong residual group order");
    }
    return group;
}

bool independent(Mask64 mask) {
    std::vector<unsigned> points;
    for (unsigned point = 0; point < 64; ++point) {
        if (((mask >> point) & Mask64{1}) != 0) {
            points.push_back(point);
        }
    }
    for (std::size_t i = 0; i < points.size(); ++i) {
        const std::array<unsigned, 3> left{
            points[i] / 16, (points[i] / 4) % 4, points[i] % 4};
        for (std::size_t j = i + 1; j < points.size(); ++j) {
            const std::array<unsigned, 3> right{
                points[j] / 16, (points[j] / 4) % 4, points[j] % 4};
            const unsigned distance = static_cast<unsigned>(left[0] != right[0]) +
                                      static_cast<unsigned>(left[1] != right[1]) +
                                      static_cast<unsigned>(left[2] != right[2]);
            if (distance < 2) {
                return false;
            }
        }
    }
    return true;
}

struct OrbitAudit {
    std::array<Count, 8> mass{};
    std::array<unsigned, 8> orbit_counts{};
    std::array<unsigned, 8> minimum_stabilizer{};
    std::array<unsigned, 8> maximum_stabilizer{};
};

OrbitAudit audit_orbits(const std::array<std::vector<Mask64>, 8> &levels,
                        const std::vector<PointMap> &group) {
    OrbitAudit result;
    for (unsigned level = 0; level < levels.size(); ++level) {
        std::set<Mask64> orbit_identifiers;
        result.orbit_counts[level] = static_cast<unsigned>(levels[level].size());
        result.minimum_stabilizer[level] = static_cast<unsigned>(group.size());
        for (const Mask64 mask : levels[level]) {
            if (popcount64(mask) != level || !independent(mask)) {
                throw std::runtime_error("invalid representative");
            }
            std::array<unsigned, 7> selected{};
            unsigned selected_count = 0;
            for (unsigned point = 0; point < 64; ++point) {
                if (((mask >> point) & Mask64{1}) != 0) {
                    selected[selected_count++] = point;
                }
            }
            unsigned stabilizer = 0;
            Mask64 orbit_identifier = std::numeric_limits<Mask64>::max();
            for (const auto &mapping : group) {
                Mask64 image = 0;
                for (unsigned i = 0; i < selected_count; ++i) {
                    image |= Mask64{1} << mapping[selected[i]];
                }
                orbit_identifier = std::min(orbit_identifier, image);
                stabilizer += static_cast<unsigned>(image == mask);
            }
            if (stabilizer == 0 || group.size() % stabilizer != 0) {
                throw std::runtime_error("invalid explicit stabilizer count");
            }
            if (!orbit_identifiers.insert(orbit_identifier).second) {
                throw std::runtime_error("two representatives are in the same orbit");
            }
            result.minimum_stabilizer[level] =
                std::min(result.minimum_stabilizer[level], stabilizer);
            result.maximum_stabilizer[level] =
                std::max(result.maximum_stabilizer[level], stabilizer);
            result.mass[level] += static_cast<Count>(group.size() / stabilizer);
        }
    }
    return result;
}

std::array<Count, 8> labeled_counts() {
    std::vector<unsigned> row_matchings;
    for (unsigned mask = 0; mask < (1U << 16); ++mask) {
        bool valid = true;
        for (unsigned column = 0; column < 4; ++column) {
            valid = valid && popcount16((mask >> (4 * column)) & 15U) <= 1;
        }
        for (unsigned symbol = 0; symbol < 4; ++symbol) {
            unsigned appearances = 0;
            for (unsigned column = 0; column < 4; ++column) {
                appearances += (mask >> (4 * column + symbol)) & 1U;
            }
            valid = valid && appearances <= 1;
        }
        if (valid) {
            row_matchings.push_back(mask);
        }
    }
    if (row_matchings.size() != 209) {
        throw std::runtime_error("wrong row-matching count");
    }

    std::vector<Count> states(1U << 16, 0);
    std::vector<Count> updated(1U << 16, 0);
    states[0] = 1;
    for (unsigned row = 0; row < 4; ++row) {
        std::fill(updated.begin(), updated.end(), 0);
        for (unsigned used = 0; used < states.size(); ++used) {
            if (states[used] == 0) {
                continue;
            }
            for (const unsigned matching : row_matchings) {
                if ((used & matching) != 0) {
                    continue;
                }
                const unsigned combined = used | matching;
                if (popcount16(combined) > 7) {
                    continue;
                }
                if (updated[combined] >
                    std::numeric_limits<Count>::max() - states[used]) {
                    throw std::runtime_error("count overflow");
                }
                updated[combined] += states[used];
            }
        }
        states.swap(updated);
    }

    std::array<Count, 8> result{};
    for (unsigned used = 0; used < states.size(); ++used) {
        if (states[used] != 0) {
            const unsigned size = popcount16(used);
            if (size > 7) {
                throw std::runtime_error("transfer retained an oversized state");
            }
            result[size] += states[used];
        }
    }
    return result;
}

template <class T, std::size_t N>
void print_array(const std::array<T, N> &values) {
    std::cout << '[';
    for (std::size_t i = 0; i < values.size(); ++i) {
        if (i != 0) {
            std::cout << ',';
        }
        std::cout << values[i];
    }
    std::cout << ']';
}

} // namespace

int main(int argc, char **argv) {
    try {
        if (argc != 2) {
            throw std::runtime_error("usage: explicit_group_audit ORBITS.json");
        }
        std::ifstream input(argv[1]);
        if (!input) {
            throw std::runtime_error("cannot open orbit file");
        }
        const std::string encoded((std::istreambuf_iterator<char>(input)),
                                  std::istreambuf_iterator<char>());
        const auto levels = LevelsParser(encoded).parse();
        const auto group = make_group();
        const auto orbit_audit = audit_orbits(levels, group);
        const auto direct_counts = labeled_counts();
        if (orbit_audit.mass != direct_counts) {
            throw std::runtime_error("explicit orbit masses do not exhaust labeled sets");
        }

        std::cout << "{\n  \"status\":\"VERIFIED\",\n"
                  << "  \"group_order\":" << group.size() << ",\n"
                  << "  \"orbit_counts\":";
        print_array(orbit_audit.orbit_counts);
        std::cout << ",\n  \"explicit_orbit_masses\":";
        print_array(orbit_audit.mass);
        std::cout << ",\n  \"direct_labeled_counts\":";
        print_array(direct_counts);
        std::cout << ",\n  \"minimum_stabilizers\":";
        print_array(orbit_audit.minimum_stabilizer);
        std::cout << ",\n  \"maximum_stabilizers\":";
        print_array(orbit_audit.maximum_stabilizer);
        std::cout << "\n}\n";
        return 0;
    } catch (const std::exception &error) {
        std::cerr << "ERROR: " << error.what() << '\n';
        return 1;
    }
}
