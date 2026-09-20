#include <algorithm>
#include <array>
#include <boost/multiprecision/cpp_int.hpp>
#include <cstdint>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>

using Wide = __int128_t;
using Big = boost::multiprecision::cpp_int;

static Big abs_big(Big x) { return x < 0 ? -x : x; }

static Big gcd_big(Big a, Big b) {
    a = abs_big(a);
    b = abs_big(b);
    while (b != 0) {
        Big r = a % b;
        a = b;
        b = r;
    }
    return a;
}

struct Rational {
    Big numerator = 0;
    Big denominator = 1;

    Rational() = default;
    Rational(long long value) : numerator(value) {}
    Rational(Wide value) : numerator(static_cast<long long>(value)) {}
    Rational(Big num, Big den) : numerator(std::move(num)), denominator(std::move(den)) {
        normalize();
    }

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
        const Big divisor = gcd_big(numerator, denominator);
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

static Rational operator*(const Rational& a, const Rational& b) {
    return {a.numerator * b.numerator, a.denominator * b.denominator};
}

static Rational operator+(const Rational& a, const Rational& b) {
    return {a.numerator * b.denominator + b.numerator * a.denominator,
            a.denominator * b.denominator};
}

static Rational operator/(const Rational& a, const Rational& b) {
    if (b.numerator == 0) throw std::runtime_error("rational division by zero");
    return {a.numerator * b.denominator, a.denominator * b.numerator};
}

static bool is_zero(const Rational& x) { return x.numerator == 0; }
static bool is_positive(const Rational& x) { return x.numerator > 0; }

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

static Graph decode_graph6(std::string line) {
    if (!line.empty() && line.back() == '\r') line.pop_back();
    if (line.rfind(">>graph6<<", 0) == 0) line.erase(0, 10);
    if (line.empty()) throw std::runtime_error("empty graph6 record");
    const int n = static_cast<unsigned char>(line[0]) - 63;
    if (n < 0 || n > 16) throw std::runtime_error("only graph6 order <=16 is supported");
    const std::size_t needed = 1 + (static_cast<std::size_t>(n) * (n - 1) / 2 + 5) / 6;
    if (line.size() != needed) throw std::runtime_error("malformed graph6 record");

    Graph graph;
    graph.n = n;
    std::size_t character = 1;
    int bit = 5;
    int value = character < line.size() ? static_cast<unsigned char>(line[character]) - 63 : 0;
    for (int j = 1; j < n; ++j) {
        for (int i = 0; i < j; ++i) {
            if (value < 0 || value > 63) throw std::runtime_error("invalid graph6 character");
            if ((value >> bit) & 1) {
                graph.adjacency[i][j] = graph.adjacency[j][i] = 1;
                ++graph.m;
            }
            if (--bit < 0) {
                bit = 5;
                ++character;
                value = character < line.size()
                    ? static_cast<unsigned char>(line[character]) - 63 : 0;
            }
        }
    }
    return graph;
}

static std::vector<std::vector<Wide>> shifted_q(const Graph& graph) {
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

template <typename Scalar>
static void symmetric_swap(std::vector<std::vector<Scalar>>& matrix, int a, int b) {
    if (a == b) return;
    std::swap(matrix[a], matrix[b]);
    for (auto& row : matrix) std::swap(row[a], row[b]);
}

// Bareiss symmetric elimination. It accepts exactly the cases admitting a
// nonzero diagonal pivot at every nonsingular step. At order 12, Hadamard's
// bound gives |minor| <= 92^(12/2); every product below is <92^12<2^79.
static bool fast_inertia(const Graph& graph, Inertia& answer) {
    auto matrix = shifted_q(graph);
    Wide previous_pivot = 1;
    int k = 0;
    while (k < graph.n) {
        int pivot_index = k;
        while (pivot_index < graph.n && matrix[pivot_index][pivot_index] == 0) ++pivot_index;
        if (pivot_index == graph.n) {
            bool nonzero = false;
            for (int i = k; i < graph.n; ++i) {
                for (int j = k; j < graph.n; ++j) nonzero |= matrix[i][j] != 0;
            }
            if (nonzero) return false;
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
                    throw std::runtime_error("nonexact Bareiss division");
                }
                matrix[i][j] = matrix[j][i] = numerator / previous_pivot;
            }
        }
        previous_pivot = pivot;
        ++k;
    }
    return true;
}

static Inertia exact_inertia(const Graph& graph) {
    const auto integers = shifted_q(graph);
    std::vector<std::vector<Rational>> matrix(graph.n, std::vector<Rational>(graph.n));
    for (int i = 0; i < graph.n; ++i) {
        for (int j = 0; j < graph.n; ++j) matrix[i][j] = Rational(integers[i][j]);
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
        if (!is_zero(matrix[k][k]) || !is_zero(matrix[k + 1][k + 1]) ||
            is_zero(off_diagonal)) {
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
    const bool crosscheck = argc == 2 && std::string(argv[1]) == "--crosscheck";
    if (argc > 2 || (argc == 2 && !crosscheck)) {
        std::cerr << "usage: check_order12 [--crosscheck]\n";
        return 2;
    }

    std::uint64_t graphs = 0;
    std::uint64_t fallbacks = 0;
    std::uint64_t counterexamples = 0;
    int maximum_signature = -1000000;
    std::string first_maximizer;
    std::map<int, std::uint64_t> edge_counts;
    std::map<int, std::uint64_t> signature_counts;

    std::string line;
    while (std::getline(std::cin, line)) {
        if (line.empty()) continue;
        const Graph graph = decode_graph6(line);
        Inertia inertia;
        if (!fast_inertia(graph, inertia)) {
            ++fallbacks;
            inertia = exact_inertia(graph);
        } else if (crosscheck) {
            const Inertia reference = exact_inertia(graph);
            if (!(inertia == reference)) throw std::runtime_error("inertia mismatch");
        }
        if (inertia.positive + inertia.zero + inertia.negative != graph.n) {
            throw std::runtime_error("invalid inertia dimension");
        }
        const int signature = 2 * inertia.positive + inertia.zero - graph.m;
        ++graphs;
        ++edge_counts[graph.m];
        ++signature_counts[signature];
        if (signature > maximum_signature) {
            maximum_signature = signature;
            first_maximizer = line;
        }
        if (signature >= 2) {
            ++counterexamples;
            std::cout << "WITNESS graph6=" << line << " n=" << graph.n << " m=" << graph.m
                      << " shifted_inertia=(" << inertia.positive << ',' << inertia.zero << ','
                      << inertia.negative << ") line_signature=" << signature << '\n';
        }
    }

    std::cout << "graphs=" << graphs << " fallbacks=" << fallbacks
              << " counterexamples=" << counterexamples << '\n';
    for (const auto& [edges, count] : edge_counts) {
        std::cout << "edges m=" << edges << " count=" << count << '\n';
    }
    for (const auto& [signature, count] : signature_counts) {
        std::cout << "signature value=" << signature << " count=" << count << '\n';
    }
    std::cout << "maximum_signature=" << maximum_signature
              << " first_maximizer=" << first_maximizer << '\n';
}
