// Exhaustive AGL(2,5) audit of the submitted cross-type orbit partition.
//
// Input files are deliberately plain text.  catalogue.txt contains the
// independently enumerated keys "type word"; representatives.tsv contains
// "type word claimed_orbit_size".  This program does not use the reviewed
// Python canonicalizer or its selected-low-line parametrization.
#include <array>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <string>
#include <unordered_set>
#include <vector>

namespace {

using Permutation = std::array<unsigned char, 25>;

[[noreturn]] void fail(const std::string& message) {
    std::cerr << message << '\n';
    std::exit(1);
}

std::string key(int type, const std::string& word) {
    return std::to_string(type) + " " + word;
}

bool profile_a(const std::array<int, 5>& profile) {
    return profile == std::array<int, 5>{8, 16, 16, 16, 16};
}

bool profile_b(const std::array<int, 5>& profile) {
    return profile == std::array<int, 5>{9, 15, 16, 16, 16};
}

}  // namespace

int main(int argc, char** argv) {
    if (argc != 3) fail("usage: full_affine_check catalogue.txt representatives.tsv");

    std::ifstream catalogue_source(argv[1]);
    std::set<std::string> catalogue;
    int type = -1;
    std::string word;
    while (catalogue_source >> type >> word) {
        if (type < 0 || type > 2 || word.size() != 25) fail("bad catalogue record");
        catalogue.insert(key(type, word));
    }
    if (!catalogue_source.eof() || catalogue.size() != 16192) fail("bad catalogue file");

    struct Representative { int type; std::string word; int orbit_size; };
    std::ifstream representative_source(argv[2]);
    std::vector<Representative> representatives;
    int orbit_size = 0;
    while (representative_source >> type >> word >> orbit_size) {
        if (type < 0 || type > 2 || word.size() != 25 || orbit_size <= 0)
            fail("bad representative record");
        representatives.push_back({type, word, orbit_size});
    }
    if (!representative_source.eof() || representatives.size() != 4332)
        fail("bad representative file");

    // Each permutation stores the old index supplying a given new index.
    std::vector<Permutation> permutations;
    std::set<Permutation> distinct_permutations;
    for (int a = 0; a < 5; ++a)
    for (int b = 0; b < 5; ++b)
    for (int c = 0; c < 5; ++c)
    for (int d = 0; d < 5; ++d) {
        if ((a*d-b*c) % 5 == 0) continue;
        for (int u = 0; u < 5; ++u)
        for (int v = 0; v < 5; ++v) {
            Permutation inverse{};
            inverse.fill(255);
            for (int x = 0; x < 5; ++x)
            for (int y = 0; y < 5; ++y) {
                const int nx = (a*x+b*y+u) % 5;
                const int ny = (c*x+d*y+v) % 5;
                inverse[5*nx+ny] = static_cast<unsigned char>(5*x+y);
            }
            for (unsigned char entry : inverse)
                if (entry == 255) fail("singular affine permutation");
            permutations.push_back(inverse);
            distinct_permutations.insert(inverse);
        }
    }
    if (permutations.size() != 12000 || distinct_permutations.size() != 12000)
        fail("incorrect affine group order");

    std::set<std::string> covered;
    std::map<int, int> histogram;
    for (std::size_t index = 0; index < representatives.size(); ++index) {
        const auto& representative = representatives[index];
        const std::string representative_key = key(representative.type, representative.word);
        if (!catalogue.contains(representative_key)) fail("representative absent from catalogue");
        std::set<std::string> images;
        for (const auto& inverse : permutations) {
            std::array<int, 5> rows{}, columns{};
            for (int position = 0; position < 25; ++position) {
                const int value = representative.word[inverse[position]]-'0';
                rows[position/5] += value;
                columns[position%5] += value;
            }
            int image_type = -1;
            if (profile_a(rows) && profile_a(columns)) image_type = 0;
            else if (profile_a(rows) && profile_b(columns)) image_type = 1;
            else if (profile_b(rows) && profile_b(columns)) image_type = 2;
            else continue;
            std::string image(25, '0');
            for (int position = 0; position < 25; ++position)
                image[position] = representative.word[inverse[position]];
            const std::string image_key = key(image_type, image);
            if (!catalogue.contains(image_key)) fail("normalized affine image absent from catalogue");
            images.insert(image_key);
        }
        if (static_cast<int>(images.size()) != representative.orbit_size)
            fail("orbit-size mismatch at representative " + std::to_string(index));
        if (images.empty() || *images.begin() != representative_key)
            fail("canonical-minimum mismatch at representative " + std::to_string(index));
        for (const std::string& image : images)
            if (!covered.insert(image).second)
                fail("orbit overlap at representative " + std::to_string(index));
        ++histogram[representative.orbit_size];
        if ((index+1) % 500 == 0)
            std::cerr << "checked affine representative " << index+1 << "/4332\n";
    }
    if (covered != catalogue) fail("full affine orbits do not cover catalogue");

    std::cout << "{\n  \"affine_group_order\": 12000,\n"
              << "  \"covered_typed_quotients\": " << covered.size() << ",\n"
              << "  \"representatives\": " << representatives.size() << ",\n"
              << "  \"orbit_histogram\": {";
    bool first = true;
    for (const auto& [size, count] : histogram) {
        if (!first) std::cout << ',';
        std::cout << "\n    \"" << size << "\": " << count;
        first = false;
    }
    std::cout << "\n  }\n}\n";
}
