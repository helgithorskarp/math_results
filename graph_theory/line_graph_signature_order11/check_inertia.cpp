#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

using Wide = __int128_t;

static Wide absolute(Wide value) { return value < 0 ? -value : value; }

static Wide gcd_wide(Wide a, Wide b) {
    a = absolute(a);
    b = absolute(b);
    while (b != 0) {
        const Wide remainder = a % b;
        a = b;
        b = remainder;
    }
    return a;
}

struct Rational {
    Wide numerator = 0;
    Wide denominator = 1;

    Rational() = default;
    Rational(long long value) : numerator(value) {}
    Rational(Wide num, Wide den) : numerator(num), denominator(den) { normalize(); }

    void normalize() {
        if (denominator == 0) throw std::runtime_error("zero rational denominator");
        if (numerator == 0) {
            denominator = 1;
            return;
        }
        if (denominator < 0) {
            numerator = -numerator;
            denominator = -denominator;
        }
        const Wide divisor = gcd_wide(numerator, denominator);
        numerator /= divisor;
        denominator /= divisor;
    }

    Rational& operator-=(const Rational& other) {
        numerator = numerator * other.denominator - other.numerator * denominator;
        denominator *= other.denominator;
        normalize();
        return *this;
    }
};

static Rational operator*(const Rational& left, const Rational& right) {
    return {left.numerator * right.numerator, left.denominator * right.denominator};
}

static Rational operator+(const Rational& left, const Rational& right) {
    return {left.numerator * right.denominator + right.numerator * left.denominator,
            left.denominator * right.denominator};
}

static Rational operator/(const Rational& left, const Rational& right) {
    if (right.numerator == 0) throw std::runtime_error("rational division by zero");
    return {left.numerator * right.denominator, left.denominator * right.numerator};
}

static bool is_zero(const Rational& value) { return value.numerator == 0; }
static bool is_positive(const Rational& value) { return value.numerator > 0; }

struct Inertia {
    int positive = 0;
    int zero = 0;
    int negative = 0;

    bool operator==(const Inertia&) const = default;
};

struct Graph {
    int n = 0;
    int m = 0;
    std::array<std::array<int, 16>, 16> adjacency{};
};

static Graph decode_graph6(const std::string& input) {
    std::string line = input;
    if (!line.empty() && line.back() == '\r') line.pop_back();
    if (line.rfind(">>graph6<<", 0) == 0) line.erase(0, 10);
    if (line.empty()) throw std::runtime_error("empty graph6 record");
    const int n = static_cast<unsigned char>(line[0]) - 63;
    if (n < 0 || n > 16) throw std::runtime_error("only short graph6 records of order <=16 are supported");
    const std::size_t needed = 1 + (static_cast<std::size_t>(n) * (n - 1) / 2 + 5) / 6;
    if (line.size() != needed) throw std::runtime_error("malformed graph6 record length");

    Graph graph;
    graph.n = n;
    std::size_t char_index = 1;
    int bit_index = 5;
    int value = char_index < line.size() ? static_cast<unsigned char>(line[char_index]) - 63 : 0;
    for (int j = 1; j < n; ++j) {
        for (int i = 0; i < j; ++i) {
            if (value < 0 || value > 63) throw std::runtime_error("invalid graph6 character");
            const int edge = (value >> bit_index) & 1;
            if (edge) {
                graph.adjacency[i][j] = graph.adjacency[j][i] = 1;
                ++graph.m;
            }
            if (--bit_index < 0) {
                bit_index = 5;
                ++char_index;
                value = char_index < line.size() ? static_cast<unsigned char>(line[char_index]) - 63 : 0;
            }
        }
    }
    return graph;
}

static std::vector<std::vector<Wide>> shifted_signless_laplacian(const Graph& graph) {
    std::vector<std::vector<Wide>> matrix(graph.n, std::vector<Wide>(graph.n));
    for (int i = 0; i < graph.n; ++i) {
        int degree = 0;
        for (int j = 0; j < graph.n; ++j) {
            matrix[i][j] = graph.adjacency[i][j];
            degree += graph.adjacency[i][j];
        }
        matrix[i][i] = degree - 2;
    }
    return matrix;
}

static void symmetric_swap(std::vector<std::vector<Wide>>& matrix, int a, int b) {
    if (a == b) return;
    std::swap(matrix[a], matrix[b]);
    for (auto& row : matrix) std::swap(row[a], row[b]);
}

// Fraction-free symmetric elimination.  At step k the stored pivot is the
// determinant of the current leading principal minor.  A nonzero 1x1 pivot
// therefore contributes the sign of pivot/previous_pivot to the inertia.
// The routine declines matrices that require a 2x2 pivot; exact_inertia()
// handles those with arbitrary-precision rationals.
static bool fast_inertia(const Graph& graph, Inertia& answer) {
    auto matrix = shifted_signless_laplacian(graph);
    Wide previous_pivot = 1;
    int k = 0;
    while (k < graph.n) {
        int pivot_index = k;
        while (pivot_index < graph.n && matrix[pivot_index][pivot_index] == 0) ++pivot_index;
        if (pivot_index == graph.n) {
            bool any_nonzero = false;
            for (int i = k; i < graph.n; ++i) {
                for (int j = k; j < graph.n; ++j) any_nonzero |= matrix[i][j] != 0;
            }
            if (any_nonzero) return false;
            answer.zero += graph.n - k;
            return true;
        }
        symmetric_swap(matrix, k, pivot_index);
        const Wide pivot = matrix[k][k];
        if ((pivot > 0) == (previous_pivot > 0)) ++answer.positive;
        else ++answer.negative;

        for (int i = k + 1; i < graph.n; ++i) {
            for (int j = i; j < graph.n; ++j) {
                const Wide numerator = matrix[i][j] * pivot - matrix[i][k] * matrix[k][j];
                if (numerator % previous_pivot != 0) {
                    throw std::runtime_error("fraction-free division was not exact");
                }
                matrix[i][j] = matrix[j][i] = numerator / previous_pivot;
            }
        }
        previous_pivot = pivot;
        ++k;
    }
    return true;
}

static void symmetric_swap(std::vector<std::vector<Rational>>& matrix, int a, int b) {
    if (a == b) return;
    std::swap(matrix[a], matrix[b]);
    for (auto& row : matrix) std::swap(row[a], row[b]);
}

static Inertia exact_inertia(const Graph& graph) {
    const auto integer_matrix = shifted_signless_laplacian(graph);
    std::vector<std::vector<Rational>> matrix(graph.n, std::vector<Rational>(graph.n));
    for (int i = 0; i < graph.n; ++i) {
        for (int j = 0; j < graph.n; ++j) matrix[i][j] = static_cast<long long>(integer_matrix[i][j]);
    }

    Inertia answer;
    int k = 0;
    while (k < graph.n) {
        int pivot_index = k;
        while (pivot_index < graph.n && is_zero(matrix[pivot_index][pivot_index])) ++pivot_index;
        if (pivot_index < graph.n) {
            symmetric_swap(matrix, k, pivot_index);
            const Rational pivot = matrix[k][k];
            if (is_positive(pivot)) ++answer.positive;
            else ++answer.negative;
            for (int i = k + 1; i < graph.n; ++i) {
                for (int j = i; j < graph.n; ++j) {
                    matrix[i][j] -= matrix[i][k] * matrix[k][j] / pivot;
                    matrix[j][i] = matrix[i][j];
                }
            }
            ++k;
            continue;
        }

        int row = -1;
        int column = -1;
        for (int i = k; i < graph.n && row < 0; ++i) {
            for (int j = i + 1; j < graph.n; ++j) {
                if (!is_zero(matrix[i][j])) {
                    row = i;
                    column = j;
                    break;
                }
            }
        }
        if (row < 0) {
            answer.zero += graph.n - k;
            break;
        }
        symmetric_swap(matrix, k, row);
        if (column == k) column = row;
        symmetric_swap(matrix, k + 1, column);
        const Rational off_diagonal = matrix[k][k + 1];
        if (!is_zero(matrix[k][k]) || !is_zero(matrix[k + 1][k + 1]) || is_zero(off_diagonal)) {
            throw std::runtime_error("invalid 2x2 pivot state");
        }
        ++answer.positive;
        ++answer.negative;
        for (int i = k + 2; i < graph.n; ++i) {
            for (int j = i; j < graph.n; ++j) {
                matrix[i][j] -= (matrix[i][k] * matrix[k + 1][j]
                               + matrix[i][k + 1] * matrix[k][j]) / off_diagonal;
                matrix[j][i] = matrix[i][j];
            }
        }
        k += 2;
    }
    return answer;
}

int main(int argc, char** argv) {
    bool crosscheck = false;
    bool signatures_only = false;
    for (int argument = 1; argument < argc; ++argument) {
        const std::string option = argv[argument];
        if (option == "--crosscheck") crosscheck = true;
        else if (option == "--signatures-only") signatures_only = true;
        else {
            std::cerr << "usage: check_inertia [--crosscheck] [--signatures-only]\n";
            return 2;
        }
    }

    std::uint64_t graphs = 0;
    std::uint64_t fallbacks = 0;
    std::uint64_t counterexamples = 0;
    std::uint64_t sharp_bound_violations = 0;
    int maximum_signature = -1000000;
    std::string first_maximizer;
    std::map<std::pair<int, int>, std::uint64_t> edge_counts;
    std::map<int, std::uint64_t> signature_counts;
    std::map<int, std::pair<int, std::uint64_t>> cyclomatic_maxima;

    std::string line;
    while (std::getline(std::cin, line)) {
        if (line.empty()) continue;
        const Graph graph = decode_graph6(line);
        if (graph.m < graph.n) {
            std::cerr << "the line-signature reduction requires m >= n for " << line << '\n';
            return 5;
        }
        Inertia inertia;
        if (!fast_inertia(graph, inertia)) {
            ++fallbacks;
            inertia = exact_inertia(graph);
        } else if (crosscheck) {
            const Inertia reference = exact_inertia(graph);
            if (!(inertia == reference)) {
                std::cerr << "inertia mismatch for " << line << '\n';
                return 3;
            }
        }
        if (inertia.positive + inertia.zero + inertia.negative != graph.n) {
            std::cerr << "invalid inertia dimension for " << line << '\n';
            return 4;
        }
        const int signature = 2 * inertia.positive + inertia.zero - graph.m;
        const int cyclomatic_number = graph.m - graph.n + 1;
        if (signatures_only) std::cout << line << '\t' << signature << '\n';
        ++graphs;
        ++edge_counts[{graph.n, graph.m}];
        ++signature_counts[signature];
        auto [iterator, inserted] = cyclomatic_maxima.try_emplace(
            cyclomatic_number, std::make_pair(signature, std::uint64_t{0})
        );
        if (!inserted && signature > iterator->second.first) {
            iterator->second = {signature, 0};
        }
        if (signature == iterator->second.first) ++iterator->second.second;
        if (signature > maximum_signature) {
            maximum_signature = signature;
            first_maximizer = line;
        }
        if (signature > 1) {
            ++counterexamples;
            std::cout << "COUNTEREXAMPLE graph6=" << line << " n=" << graph.n << " m=" << graph.m
                      << " shifted_inertia=(" << inertia.positive << ',' << inertia.zero << ','
                      << inertia.negative << ") line_signature=" << signature << '\n';
        }
        if (2 * signature > cyclomatic_number + 1) {
            ++sharp_bound_violations;
            std::cout << "SHARP_BOUND_VIOLATION graph6=" << line << " n=" << graph.n
                      << " m=" << graph.m << " cyclomatic=" << cyclomatic_number
                      << " line_signature=" << signature << '\n';
        }
    }

    if (signatures_only) return 0;
    std::cout << "graphs=" << graphs << " fallbacks=" << fallbacks
              << " counterexamples=" << counterexamples
              << " sharp_bound_violations=" << sharp_bound_violations << '\n';
    for (const auto& [key, count] : edge_counts) {
        std::cout << "order_edges n=" << key.first << " m=" << key.second << " count=" << count << '\n';
    }
    for (const auto& [signature, count] : signature_counts) {
        std::cout << "signature value=" << signature << " count=" << count << '\n';
    }
    for (const auto& [cyclomatic, maximum] : cyclomatic_maxima) {
        std::cout << "cyclomatic c=" << cyclomatic << " maximum_signature=" << maximum.first
                  << " maximizers=" << maximum.second
                  << " inequality_slack=" << cyclomatic + 1 - 2 * maximum.first << '\n';
    }
    std::cout << "maximum_signature=" << maximum_signature << " first_maximizer=" << first_maximizer << '\n';
    return 0;
}
