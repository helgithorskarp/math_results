#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using Word = std::uint64_t;
using Gate = std::pair<int,int>;
struct Fixture { int n=0; std::vector<Gate> gates; };
Fixture read_fixture(const std::string& path) {
    std::ifstream f(path); int m=0; Fixture z;
    if (!(f >> z.n >> m) || z.n<2 || z.n>16 || m<2 || m>60)
        throw std::runtime_error("invalid fixture dimensions");
    for (int k=0;k<m;++k) {
        int a=0,b=0;
        if (!(f>>a>>b) || a<0 || a>=b || b>=z.n)
            throw std::runtime_error("invalid gate");
        z.gates.emplace_back(a,b);
    }
    std::string extra;
    if (f>>extra) throw std::runtime_error("trailing fixture data");
    return z;
}
struct Inputs {
    int n; std::vector<unsigned> values;
    std::vector<std::vector<Word>> wires, targets;
    explicit Inputs(int n_):n(n_),wires(static_cast<std::size_t>(n_)),targets(static_cast<std::size_t>(n_)) {}
    void add(unsigned x) {
        if (x >= (1U<<n)) throw std::runtime_error("input out of range");
        const std::size_t pos=values.size(), word=pos/64;
        const Word bit=Word{1}<<(pos%64);
        values.push_back(x);
        for(int i=0;i<n;++i) {
            if (wires[static_cast<std::size_t>(i)].size()<=word) {
                wires[static_cast<std::size_t>(i)].push_back(0);
                targets[static_cast<std::size_t>(i)].push_back(0);
            }
            if((x>>i)&1U) wires[static_cast<std::size_t>(i)][word]|=bit;
            if(std::popcount(x)>=n-i) targets[static_cast<std::size_t>(i)][word]|=bit;
        }
    }
    // Return witness-list index, or -1 if every listed input sorts.
    int first_failure(const std::vector<Gate>& sequence) const {
        const std::size_t words=(values.size()+63)/64;
        for(std::size_t t=0;t<words;++t) {
            std::array<Word,16> state{};
            for(int i=0;i<n;++i) state[static_cast<std::size_t>(i)]=wires[static_cast<std::size_t>(i)][t];
            for(const auto& [a,b]:sequence) {
                const Word lo=state[static_cast<std::size_t>(a)]&state[static_cast<std::size_t>(b)];
                const Word hi=state[static_cast<std::size_t>(a)]|state[static_cast<std::size_t>(b)];
                state[static_cast<std::size_t>(a)]=lo; state[static_cast<std::size_t>(b)]=hi;
            }
            Word bad=0;
            for(int i=0;i<n;++i) bad|=state[static_cast<std::size_t>(i)]^targets[static_cast<std::size_t>(i)][t];
            if (bad) return static_cast<int>(64*t+std::countr_zero(bad));
        }
        return -1;
    }
};

int main(int argc,char** argv) try {
    if(argc<4 || argc>5) throw std::runtime_error("usage: generate FIXTURE WITNESSES SUMMARY [PAIR_LIMIT]");
    const Fixture f=read_fixture(argv[1]);
    const int m=static_cast<int>(f.gates.size());
    const std::uint64_t limit=argc==5?std::stoull(argv[4]):std::numeric_limits<std::uint64_t>::max();
    Inputs all(f.n), witnesses(f.n);
    for(unsigned x=0;x<(1U<<f.n);++x) all.add(x);
    if(all.first_failure(f.gates)>=0) throw std::runtime_error("incumbent is not a sorting network");
    std::uint64_t pairs=0,parameters=0,acyclic=0,cyclic=0;
    bool incomplete=false;
    std::vector<Gate> sequence; sequence.reserve(static_cast<std::size_t>(m-1));
    for(int d0=0;d0<m && !incomplete;++d0) for(int d1=d0+1;d1<m;++d1) {
        if(pairs==limit) {incomplete=true;break;}
        ++pairs;
        std::array<std::vector<int>,16> paths;
        Word active=0;
        for(int g=0;g<m;++g) if(g!=d0 && g!=d1) {
            active|=Word{1}<<g;
            const auto [a,b]=f.gates[static_cast<std::size_t>(g)];
            paths[static_cast<std::size_t>(a)].push_back(g);
            paths[static_cast<std::size_t>(b)].push_back(g);
        }
        std::array<Word,60> descendants{};
        std::array<std::array<int,2>,60> successors{};
        for(auto& s:successors) s={-1,-1};
        for(int w=0;w<f.n;++w) {
            const auto& p=paths[static_cast<std::size_t>(w)];
            for(std::size_t k=0;k+1<p.size();++k) {
                const int g=p[k];
                const int port=f.gates[static_cast<std::size_t>(g)].first==w?0:1;
                successors[static_cast<std::size_t>(g)][static_cast<std::size_t>(port)]=p[k+1];
            }
        }
        for(int g=m-1;g>=0;--g) if((active>>g)&1U) {
            Word reach=Word{1}<<g;
            for(int s:successors[static_cast<std::size_t>(g)]) if(s>=0) reach|=descendants[static_cast<std::size_t>(s)];
            descendants[static_cast<std::size_t>(g)]=reach;
        }
        for(int a=0;a<f.n;++a) for(int b=a+1;b<f.n;++b) {
            const auto& pa=paths[static_cast<std::size_t>(a)];
            const auto& pb=paths[static_cast<std::size_t>(b)];
            for(std::size_t ia=0;ia<=pa.size();++ia) for(std::size_t ib=0;ib<=pb.size();++ib) {
                ++parameters;
                const int pred_a=ia?pa[ia-1]:-1, pred_b=ib?pb[ib-1]:-1;
                Word after=0;
                if(ia<pa.size()) after|=descendants[static_cast<std::size_t>(pa[ia])];
                if(ib<pb.size()) after|=descendants[static_cast<std::size_t>(pb[ib])];
                if((pred_a>=0 && ((after>>pred_a)&1U)) || (pred_b>=0 && ((after>>pred_b)&1U))) {
                    ++cyclic;continue;
                }
                ++acyclic;
                sequence.clear();
                Word before=active&~after;
                while(before) {const int g=std::countr_zero(before);before&=before-1;sequence.push_back(f.gates[static_cast<std::size_t>(g)]);}
                sequence.emplace_back(a,b);
                Word rest=after;
                while(rest) {const int g=std::countr_zero(rest);rest&=rest-1;sequence.push_back(f.gates[static_cast<std::size_t>(g)]);}
                if(sequence.size()!=static_cast<std::size_t>(m-1)) throw std::runtime_error("schedule size mismatch");
                if(witnesses.first_failure(sequence)>=0) continue;
                const int bad=all.first_failure(sequence);
                if(bad<0) {
                    std::ofstream candidate(std::string(argv[2])+".sorting-network.txt");
                    candidate<<f.n<<' '<<sequence.size()<<'\n';
                    for(const auto& [i,j]:sequence) candidate<<i<<' '<<j<<'\n';
                    std::cerr<<"SORTING NETWORK: "<<d0<<' '<<d1<<' '<<a<<' '<<b<<' '<<ia<<' '<<ib<<'\n';
                    return 3;
                }
                const unsigned value=all.values[static_cast<std::size_t>(bad)];
                if(std::find(witnesses.values.begin(),witnesses.values.end(),value)!=witnesses.values.end())
                    throw std::runtime_error("witness regression");
                witnesses.add(value);
            }
        }
        if(pairs%100==0) std::cerr<<"deletion pairs "<<pairs<<", acyclic "<<acyclic<<", witnesses "<<witnesses.values.size()<<'\n';
    }
    std::ofstream wf(argv[2]);
    wf<<f.n<<' '<<witnesses.values.size()<<'\n';
    for(unsigned x:witnesses.values) wf<<x<<'\n';
    std::ofstream sf(argv[3]);
    sf<<"{\n  \"complete\": "<<(incomplete?"false":"true")
      <<",\n  \"inputs\": "<<f.n<<",\n  \"incumbent_comparators\": "<<m
      <<",\n  \"deletion_pairs\": "<<pairs<<",\n  \"labelled_parameters\": "<<parameters
      <<",\n  \"acyclic_parameters\": "<<acyclic<<",\n  \"cyclic_parameters\": "<<cyclic
      <<",\n  \"witness_count\": "<<witnesses.values.size()<<",\n  \"sorting_candidates\": 0\n}\n";
    if(!wf || !sf) throw std::runtime_error("output write failed");
    std::cout<<"complete="<<!incomplete<<" pairs="<<pairs<<" parameters="<<parameters<<" acyclic="<<acyclic<<" cyclic="<<cyclic<<" witnesses="<<witnesses.values.size()<<'\n';
    return incomplete?2:0;
} catch(const std::exception& e) {std::cerr<<e.what()<<'\n';return 1;}
