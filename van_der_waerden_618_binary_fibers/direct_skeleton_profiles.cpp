// Independent finite table from the three literal six-bit phase columns.
// All shifts and counters are bounded by127 and36 respectively.
#include <algorithm>
#include <array>
#include <iostream>
#include <stdexcept>

int main() {
    try {
        constexpr std::array<unsigned,3> columns={56U,49U,35U};
        std::cout << "2187 64\n";
        for (unsigned code=0;code<2187;++code) {
            std::array<unsigned,7> tau{};
            unsigned remaining=code;
            for (int j=6;j>=0;--j) {
                tau[static_cast<std::size_t>(j)]=remaining%3;
                remaining/=3;
            }
            std::array<unsigned,64> counts{};
            for (unsigned step=0;step<6;++step) {
                for (unsigned start=0;start<6;++start) {
                    unsigned pattern=0;
                    for (unsigned j=0;j<7;++j) {
                        const unsigned y=(start+j*step)%6;
                        pattern|=((columns[tau[j]]>>y)&1U)<<j;
                    }
                    ++counts[std::min(pattern,pattern^127U)];
                }
            }
            unsigned classes=0,total=0;
            for (auto &value : counts) {
                if (value%2!=0) throw std::runtime_error("unpaired complement pattern");
                value/=2;
                if (value>3) throw std::runtime_error("multiplicity exceeds3");
                classes+=unsigned(value>0);total+=value;
            }
            bool period_three=true;
            for (unsigned j=0;j<4;++j) period_three=period_three && tau[j]==tau[j+3];
            if (total!=18 || (classes==8)!=period_three || classes>18 || (classes!=8 && classes<12))
                throw std::runtime_error("local profile assertion failed");
            std::cout << code;
            for (auto value : counts) std::cout << ' ' << value;
            std::cout << '\n';
        }
        if (!std::cout.good()) throw std::runtime_error("output failure");
        return 0;
    } catch (const std::exception &e) {
        std::cerr << "ERROR: " << e.what() << '\n';
        return 2;
    }
}
