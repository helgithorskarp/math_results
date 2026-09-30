// Exact phase-rectangle generator for opposed symmetric AP completions.
// Each binary record has an implicit (s,t,g) key. (0,0,0) requires a
// separately checked AP-implication supplement; it is never an exclusion.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {
constexpr int P=617, N=3704, C=1852, U=2*P, W=(U+63)/64;
using Mask=std::array<std::uint64_t,W>;
using Witness=std::array<std::uint16_t,3>;

int residue(int x) { x%=P; return x<0 ? x+P : x; }
int checked_int(const char* arg) {
    const std::string text(arg);
    std::size_t used=0;
    int value=std::stoi(text,&used);
    if (used!=text.size()) throw std::runtime_error("invalid integer");
    return value;
}
void put16(std::ostream& out, std::uint16_t value) {
    out.put(static_cast<char>(value&255U));
    out.put(static_cast<char>((value>>8U)&255U));
}
void put32(std::ostream& out, std::uint32_t value) {
    for (unsigned j=0;j<4;++j) out.put(static_cast<char>((value>>(8U*j))&255U));
}
}

int main(int argc,char** argv) {
    try {
        if (argc!=3) throw std::runtime_error("usage: generate HALF_WIDTH OUTPUT.bin");
        const int h=checked_int(argv[1]);
        if (h<1 || h>=C) throw std::runtime_error("half width outside [1,1851]");
        const std::filesystem::path output(argv[2]);
        const auto partial=std::filesystem::path(output.string()+".partial");
        if (std::filesystem::exists(output) || std::filesystem::exists(partial))
            throw std::runtime_error("refusing to overwrite output or partial output");
        const auto start=std::chrono::steady_clock::now();
        const int lo=C-h, hi=C+h;
        std::array<int,P> q;
        q.fill(1); q[0]=-1;
        for (int x=1;x<P;++x) q[(x*x)%P]=0;

        // Each row is indexed by left phase s; bit u=g*617+t is the right
        // phase and relative color. Compatible diagonal keys are skipped.
        std::vector<Mask> covered(P,Mask{});
        for (int s=0;s<P;++s) covered[s][s/64]|=std::uint64_t{1}<<(s%64);
        std::vector<Witness> witnesses(static_cast<std::size_t>(P*U),Witness{});
        const std::uint32_t target=static_cast<std::uint32_t>(P*(U-1));
        std::uint32_t total=0, geometric=0;
        int points_processed=0;
        std::vector<int> centers;
        // v +/- d must be outside the bridge, and v +/- 3d in [0,N).
        const int first=std::max(lo,(3*hi+3)/4);
        const int last=std::min(hi-1,(N-1+3*(lo-1))/4);
        for (int v=first;v<=last;++v) centers.push_back(v);
        std::sort(centers.begin(),centers.end(),[](int a,int b){
            const int da=std::abs(2*a-(N-1)), db=std::abs(2*b-(N-1));
            return da!=db ? da<db : a<b;
        });
        std::vector<std::array<std::uint32_t,3>> point_counts;
        for (int v:centers) {
            std::array<std::vector<Mask>,2> known{
                std::vector<Mask>(P,Mask{}),std::vector<Mask>(P,Mask{})};
            std::array<std::vector<std::uint16_t>,2> source{
                std::vector<std::uint16_t>(static_cast<std::size_t>(P*U),0),
                std::vector<std::uint16_t>(static_cast<std::size_t>(P*U),0)};
            const int dmin=std::max({1,v-lo+1,hi-v});
            const int dmax=std::min(v/3,(N-1-v)/3);
            const std::uint32_t before=total;
            for (int d=dmin;d<=dmax;++d) {
                ++geometric;
                std::array<std::vector<int>,2> left;
                std::array<Mask,2> right{};
                for (int s=0;s<P;++s) {
                    const int b=q[residue(v-d-C+s)];
                    if (b>=0 && q[residue(v-2*d-C+s)]==b
                             && q[residue(v-3*d-C+s)]==b)
                        left[b].push_back(s);
                }
                for (int t=0;t<P;++t) {
                    const int b=q[residue(v+d-C+t)];
                    if (b>=0 && q[residue(v+2*d-C+t)]==b
                             && q[residue(v+3*d-C+t)]==b) {
                        right[b][t/64]|=std::uint64_t{1}<<(t%64);
                        const int u=P+t;
                        right[1-b][u/64]|=std::uint64_t{1}<<(u%64);
                    }
                }
                for (int b=0;b<2;++b) for (int s:left[b]) {
                    for (int w=0;w<W;++w) {
                        std::uint64_t fresh=right[b][w]&~covered[s][w]&~known[b][s][w];
                        const std::uint64_t save=fresh;
                        while (fresh) {
                            const unsigned bit=static_cast<unsigned>(__builtin_ctzll(fresh));
                            const std::uint64_t one=std::uint64_t{1}<<bit;
                            fresh&=fresh-1;
                            const int u=64*w+static_cast<int>(bit);
                            if (u>=U) throw std::runtime_error("invalid phase bit");
                            const auto index=static_cast<std::size_t>(s*U+u);
                            source[b][index]=static_cast<std::uint16_t>(d);
                            if ((known[1-b][s][w]&one)!=0) {
                                const auto other=source[1-b][index];
                                if (other==0 || witnesses[index][0]!=0)
                                    throw std::runtime_error("invalid witness state");
                                auto& witness=witnesses[index];
                                witness[0]=static_cast<std::uint16_t>(v);
                                witness[1+b]=static_cast<std::uint16_t>(d);
                                witness[2-b]=other;
                                covered[s][w]|=one;
                                ++total;
                            }
                        }
                        known[b][s][w]|=save;
                    }
                }
            }
            ++points_processed;
            point_counts.push_back({static_cast<std::uint32_t>(v),total-before,total});
            if (total==target) break;
        }
        // Fixed little-endian header: 8-byte magic, p,k,n,h,begin,end (u16),
        // count (u32), then (v,d0,d1) (three u16) in s,t,g order, skipping
        // s=t,g=0. Zero records are explicit holes for implication proofs.
        std::ofstream out(partial,std::ios::binary);
        if (!out) throw std::runtime_error("cannot open certificate output");
        out.write("QRD617P1",8);
        for (int x:{P,7,N,h,0,P}) put16(out,static_cast<std::uint16_t>(x));
        put32(out,target);
        std::uint32_t written=0;
        for (int s=0;s<P;++s) for (int t=0;t<P;++t) for (int g=0;g<2;++g) {
            if (s==t && g==0) continue;
            const auto& witness=witnesses[static_cast<std::size_t>(s*U+g*P+t)];
            for (auto x:witness) put16(out,x);
            ++written;
        }
        out.close();
        if (!out || written!=target) throw std::runtime_error("incomplete certificate write");
        std::filesystem::rename(partial,output);
        const double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
        std::cout << "{\"status\":\"GENERATED_REQUIRES_INDEPENDENT_CHECK\",\"half_width\":" << h
                  << ",\"length\":" << N << ",\"incompatible_cases\":" << target
                  << ",\"opposed_ap_records\":" << total << ",\"supplement_required\":" << target-total
                  << ",\"eligible_centers\":" << centers.size() << ",\"centers_processed\":" << points_processed
                  << ",\"symmetric_ap_frames_processed\":" << geometric << ",\"seconds\":" << seconds
                  << ",\"per_center\":[";
        for (std::size_t i=0;i<point_counts.size();++i) {
            if (i) std::cout << ',';
            const auto& r=point_counts[i];
            std::cout << '[' << r[0] << ',' << r[1] << ',' << r[2] << ']';
        }
        std::cout << "]}\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "generation failed: " << error.what() << '\n';
        return 1;
    }
}
