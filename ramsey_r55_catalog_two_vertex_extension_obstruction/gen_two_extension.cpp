#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

using Matrix = std::vector<std::vector<unsigned char>>;

static Matrix decode_graph6(const std::string& raw) {
    std::string s = raw;
    while (!s.empty() && (s.back() == '\n' || s.back() == '\r')) s.pop_back();
    if (s.empty()) throw std::runtime_error("empty graph6 record");
    const int n = static_cast<unsigned char>(s[0]) - 63;
    if (n < 0 || n > 62) throw std::runtime_error("only small graph6 records supported");
    std::vector<int> bits;
    for (size_t p = 1; p < s.size(); ++p) {
        int x = static_cast<unsigned char>(s[p]) - 63;
        if (x < 0 || x > 63) throw std::runtime_error("invalid graph6 byte");
        for (int shift = 5; shift >= 0; --shift) bits.push_back((x >> shift) & 1);
    }
    if (static_cast<int>(bits.size()) < n * (n - 1) / 2) throw std::runtime_error("truncated graph6 record");
    Matrix a(n, std::vector<unsigned char>(n));
    int at = 0;
    for (int j = 1; j < n; ++j) for (int i = 0; i < j; ++i) {
        a[i][j] = a[j][i] = static_cast<unsigned char>(bits[at++]);
    }
    return a;
}

static bool homogeneous(const Matrix& a, const std::vector<int>& ss, bool edge) {
    for (size_t i = 0; i < ss.size(); ++i) for (size_t j = i + 1; j < ss.size(); ++j)
        if (static_cast<bool>(a[ss[i]][ss[j]]) != edge) return false;
    return true;
}

static std::string record_at(const std::string& path, int wanted) {
    std::ifstream in(path);
    if (!in) throw std::runtime_error("cannot open input");
    std::string line;
    for (int i = 0; std::getline(in, line); ++i) if (i == wanted) return line;
    throw std::runtime_error("record index out of range");
}

int main(int argc, char** argv) try {
    if (argc != 4) {
        std::cerr << "usage: gen_two_extension CORE.g6 ZERO_BASED_INDEX OUTPUT.cnf\n";
        return 2;
    }
    const int index = std::stoi(argv[2]);
    const Matrix a = decode_graph6(record_at(argv[1], index));
    if (a.size() != 41) throw std::runtime_error("input record order is not 41");

    for (int v0 = 0; v0 < 41; ++v0) for (int v1 = v0 + 1; v1 < 41; ++v1)
    for (int v2 = v1 + 1; v2 < 41; ++v2) for (int v3 = v2 + 1; v3 < 41; ++v3)
    for (int v4 = v3 + 1; v4 < 41; ++v4) {
        std::vector<int> ss{v0,v1,v2,v3,v4};
        if (homogeneous(a, ss, true) || homogeneous(a, ss, false))
            throw std::runtime_error("input core contains a homogeneous 5-set");
    }

    std::vector<std::vector<int>> clauses;
    long k4 = 0, i4 = 0, k3 = 0, i3 = 0;
    for (int v0 = 0; v0 < 41; ++v0) for (int v1 = v0 + 1; v1 < 41; ++v1)
    for (int v2 = v1 + 1; v2 < 41; ++v2) for (int v3 = v2 + 1; v3 < 41; ++v3) {
        std::vector<int> ss{v0,v1,v2,v3};
        if (homogeneous(a, ss, true)) {
            ++k4;
            clauses.push_back({-(v0+1),-(v1+1),-(v2+1),-(v3+1)});
            clauses.push_back({-(42+v0),-(42+v1),-(42+v2),-(42+v3)});
        }
        if (homogeneous(a, ss, false)) {
            ++i4;
            clauses.push_back({v0+1,v1+1,v2+1,v3+1});
            clauses.push_back({42+v0,42+v1,42+v2,42+v3});
        }
    }
    for (int v0 = 0; v0 < 41; ++v0) for (int v1 = v0 + 1; v1 < 41; ++v1)
    for (int v2 = v1 + 1; v2 < 41; ++v2) {
        std::vector<int> ss{v0,v1,v2};
        if (homogeneous(a, ss, true)) {
            ++k3;
            clauses.push_back({-83,-(v0+1),-(v1+1),-(v2+1),-(42+v0),-(42+v1),-(42+v2)});
        }
        if (homogeneous(a, ss, false)) {
            ++i3;
            clauses.push_back({83,v0+1,v1+1,v2+1,42+v0,42+v1,42+v2});
        }
    }

    std::ofstream out(argv[3]);
    if (!out) throw std::runtime_error("cannot open output");
    out << "p cnf 83 " << clauses.size() << "\n";
    for (const auto& c : clauses) {
        for (int lit : c) out << lit << ' ';
        out << "0\n";
    }
    std::cout << "index=" << index << " k4=" << k4 << " i4=" << i4
              << " k3=" << k3 << " i3=" << i3 << " clauses=" << clauses.size() << "\n";
    return 0;
} catch (const std::exception& e) {
    std::cerr << "error: " << e.what() << "\n";
    return 1;
}
