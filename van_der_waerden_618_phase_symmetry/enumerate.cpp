// Exhaustive constructive H17-invariant CRT103x6 phase family.
// Native direct geometry produces one cyclic obstruction per normalized word.
// Budget exhaustion means INCOMPLETE, never a mathematical exclusion.
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>

int power(int a,int e,int p) {
    int value=1;
    while (e) { if (e&1) value=value*a%p; a=a*a%p; e/=2; }
    return value;
}
void ensure(bool ok,const char *message) { if (!ok) throw std::runtime_error(message); }
void little16(std::ofstream &out,int value) {
    ensure(value>=0 && value<65536,"certificate integer out of range");
    out.put(static_cast<char>(value&255)); out.put(static_cast<char>((value>>8)&255));
}
int main(int argc,char **argv) {
    try {
        ensure(argc==3,"usage: program certificate-path seconds");
        const double seconds=std::stod(argv[2]);
        ensure(seconds>0 && seconds<=30,"budget must be in(0,30]");
        ensure(power(5,51,103)!=1 && power(5,34,103)!=1 && power(5,6,103)!=1,"invalid primitive root");
        std::array<int,103> group;
        group.fill(-1); group[0]=6;
        const int h=power(5,6,103);
        for (int i=0; i<6; ++i) {
            const int representative=power(5,i,103);
            int x=representative;
            for (int j=0; j<17; ++j) {
                ensure(group[static_cast<std::size_t>(x)]==-1,"overlapping explicit cosets");
                group[static_cast<std::size_t>(x)]=i;
                x=x*h%103;
            }
            ensure(x==representative,"subgroup order mismatch");
        }
        for (int v : group) ensure(v>=0,"incomplete explicit coset partition");
        std::ofstream certificate(argv[1],std::ios::binary);
        ensure(certificate.good(),"cannot open certificate");
        certificate.write("VDW618H17_1\n",12);
        std::uint64_t aps=0;
        unsigned checked=0;
        const auto start=std::chrono::steady_clock::now();
        for (unsigned code=0; code<46656; ++code) {
            if (std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()>=seconds) {
                std::cout << "{\"status\":\"INCOMPLETE\",\"checked\":" << checked << ",\"mathematical_exclusion\":false}\n";
                return 2;
            }
            std::array<int,7> phase{};
            unsigned value=code;
            for (int i=0; i<6; ++i) { phase[static_cast<std::size_t>(i)]=static_cast<int>(value%6); value/=6; }
            ensure(value==0 && phase[6]==0,"invalid normalized parameter word");
            std::array<int,618> colors{};
            for (int t=0; t<618; ++t)
                colors[static_cast<std::size_t>(t)]=int((t%6-phase[static_cast<std::size_t>(group[static_cast<std::size_t>(t%103)])]+6)%6>=3);
            int bad_a=-1,bad_d=-1;
            for (int d=1; d<618 && bad_a<0; ++d) for (int a=0; a<618; ++a) {
                ++aps;
                bool mono=true;
                for (int j=1; j<7; ++j)
                    if (colors[static_cast<std::size_t>((a+j*d)%618)]!=colors[static_cast<std::size_t>(a)]) { mono=false; break; }
                if (mono) { bad_a=a; bad_d=d; break; }
            }
            if (bad_a<0) {
                std::ofstream witness(std::string(argv[1])+".candidate3704.bits");
                for (int t=0; t<3704; ++t) witness << colors[static_cast<std::size_t>(t%618)];
                witness << '\n'; ensure(witness.good(),"cannot save candidate");
                std::cout << "{\"status\":\"MODEL_CANDIDATE\",\"code\":" << code << ",\"checked\":" << checked
                          << ",\"mathematical_exclusion\":false,\"independent_checker_required\":true}\n";
                return 0;
            }
            little16(certificate,bad_a); little16(certificate,bad_d);
            ++checked;
        }
        ensure(certificate.good(),"certificate write failed");
        const double elapsed=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
        std::cout << "{\"status\":\"COMPLETE_H17_PHASE_FAMILY_OBSTRUCTIONS\",\"checked\":" << checked
                  << ",\"progression_pairs_tested\":" << aps << ",\"seconds\":" << elapsed
                  << ",\"independent_checker_required\":true,\"unrestricted_exclusion\":false}\n";
        return 0;
    } catch (const std::exception &e) { std::cerr << "ERROR: " << e.what() << '\n'; return 3; }
}
