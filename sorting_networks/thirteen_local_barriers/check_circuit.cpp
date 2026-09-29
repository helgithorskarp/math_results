// Independent verifier: reconstruct wire paths and evaluate the event circuit.
// No reachability-based schedule from generate.cpp is used here.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using Bits=std::uint64_t;
struct Source { int event=-1; int wire=-1; };
struct Event {
    std::array<int,2> wires{};
    std::array<Source,2> parents{};
};
struct Circuit {
    int n=0,words=0;
    std::vector<Event> events;
    std::array<Source,16> outputs{};
    std::array<std::vector<Bits>,16> inputs;
    std::vector<std::array<std::vector<Bits>,2>> values;
    std::vector<int> colors;
    const std::vector<Bits>& from(Source p) const {
        if(p.event<0) return inputs[static_cast<std::size_t>(p.wire)];
        const auto& e=events[static_cast<std::size_t>(p.event)];
        const int port=e.wires[0]==p.wire?0:(e.wires[1]==p.wire?1:-1);
        if(port<0) throw std::runtime_error("invalid circuit port");
        return values[static_cast<std::size_t>(p.event)][static_cast<std::size_t>(port)];
    }
    bool visit(int g) {
        int& color=colors[static_cast<std::size_t>(g)];
        if(color==1) return false;
        if(color==2) return true;
        color=1;
        const Event& e=events[static_cast<std::size_t>(g)];
        for(Source p:e.parents) if(p.event>=0 && !visit(p.event)) return false;
        const auto& a=from(e.parents[0]);
        const auto& b=from(e.parents[1]);
        auto& z=values[static_cast<std::size_t>(g)];
        for(int w=0;w<words;++w) {
            const std::size_t t=static_cast<std::size_t>(w);
            z[0][t]=a[t]&b[t]; z[1][t]=a[t]|b[t];
        }
        color=2;
        return true;
    }
    // 0 = cyclic; 1 = acyclic with a failing witness; 2 = certificate insufficient.
    int classify() {
        std::fill(colors.begin(),colors.end(),0);
        for(std::size_t g=0;g<events.size();++g) if(!visit(static_cast<int>(g))) return 0;
        for(int i=0;i+1<n;++i) {
            const auto& a=from(outputs[static_cast<std::size_t>(i)]);
            const auto& b=from(outputs[static_cast<std::size_t>(i+1)]);
            for(int w=0;w<words;++w) if(a[static_cast<std::size_t>(w)]&~b[static_cast<std::size_t>(w)]) return 1;
        }
        return 2;
    }
};

int main(int argc,char** argv) try {
    if(argc<3 || argc>4) throw std::runtime_error("usage: check FIXTURE WITNESSES [PAIR_LIMIT]");
    std::ifstream nf(argv[1]),wf(argv[2]);
    int n=0,m=0,wn=0,h=0;
    if(!(nf>>n>>m) || n<2 || n>16 || m<2 || m>60) throw std::runtime_error("invalid network header");
    std::vector<std::array<int,2>> gates;
    for(int k=0;k<m;++k) {
        int a=-1,b=-1;
        if(!(nf>>a>>b) || a<0 || a>=b || b>=n) throw std::runtime_error("invalid network gate");
        gates.push_back({a,b});
    }
    std::string extra;
    if(nf>>extra) throw std::runtime_error("trailing network data");
    if(!(wf>>wn>>h) || wn!=n || h<1 || h>(1<<n)) throw std::runtime_error("invalid witness header");
    Circuit circuit; circuit.n=n; circuit.words=(h+63)/64;
    for(int i=0;i<n;++i) circuit.inputs[static_cast<std::size_t>(i)].resize(static_cast<std::size_t>(circuit.words));
    std::set<unsigned> unique;
    for(int k=0;k<h;++k) {
        unsigned x=0;
        if(!(wf>>x) || x>=(1U<<n) || !unique.insert(x).second) throw std::runtime_error("invalid or duplicate witness");
        for(int i=0;i<n;++i) if((x>>i)&1U)
            circuit.inputs[static_cast<std::size_t>(i)][static_cast<std::size_t>(k/64)]|=Bits{1}<<(k%64);
    }
    if(wf>>extra) throw std::runtime_error("trailing witness data");
    circuit.events.resize(static_cast<std::size_t>(m-1));
    circuit.values.resize(static_cast<std::size_t>(m-1));
    circuit.colors.resize(static_cast<std::size_t>(m-1));
    for(auto& v:circuit.values) for(auto& port:v) port.resize(static_cast<std::size_t>(circuit.words));
    std::uint64_t pairs=0,parameters=0,acyclic=0,cyclic=0;
    const std::uint64_t limit=argc==4?std::stoull(argv[3]):UINT64_MAX;
    bool incomplete=false;
    for(int d0=0;d0<m && !incomplete;++d0) for(int d1=d0+1;d1<m;++d1) {
        if(pairs==limit) {incomplete=true;break;}
        ++pairs;
        const int inserted=m-2;
        std::array<std::vector<int>,16> paths;
        int id=0;
        for(int g=0;g<m;++g) if(g!=d0 && g!=d1) {
            Event& e=circuit.events[static_cast<std::size_t>(id)];
            e.wires=gates[static_cast<std::size_t>(g)];
            for(int port=0;port<2;++port) {
                const int wire=e.wires[static_cast<std::size_t>(port)];
                auto& path=paths[static_cast<std::size_t>(wire)];
                e.parents[static_cast<std::size_t>(port)]={path.empty()?-1:path.back(),wire};
                path.push_back(id);
            }
            ++id;
        }
        const std::vector<Event> base=circuit.events;
        for(int a=0;a<n;++a) for(int b=a+1;b<n;++b) {
            const auto& pa=paths[static_cast<std::size_t>(a)];
            const auto& pb=paths[static_cast<std::size_t>(b)];
            for(std::size_t ia=0;ia<=pa.size();++ia) for(std::size_t ib=0;ib<=pb.size();++ib) {
                ++parameters;
                circuit.events=base;
                for(int wire=0;wire<n;++wire) {
                    const auto& p=paths[static_cast<std::size_t>(wire)];
                    circuit.outputs[static_cast<std::size_t>(wire)]={p.empty()?-1:p.back(),wire};
                }
                Event& fresh=circuit.events[static_cast<std::size_t>(inserted)];
                fresh.wires={a,b};
                fresh.parents={Source{ia?pa[ia-1]:-1,a},Source{ib?pb[ib-1]:-1,b}};
                for(int port=0;port<2;++port) {
                    const int wire=port==0?a:b;
                    const auto& path=port==0?pa:pb;
                    const std::size_t cut=port==0?ia:ib;
                    if(cut==path.size()) circuit.outputs[static_cast<std::size_t>(wire)]={inserted,wire};
                    else {
                        Event& next=circuit.events[static_cast<std::size_t>(path[cut])];
                        const int input=next.wires[0]==wire?0:1;
                        next.parents[static_cast<std::size_t>(input)]={inserted,wire};
                    }
                }
                const int status=circuit.classify();
                if(status==0) ++cyclic;
                else if(status==1) ++acyclic;
                else {
                    std::cerr<<"certificate insufficient at "<<d0<<' '<<d1<<' '<<a<<' '<<b<<' '<<ia<<' '<<ib<<'\n';
                    return 4;
                }
            }
        }
    }
    std::cout<<"certified="<<!incomplete<<" pairs="<<pairs<<" parameters="<<parameters<<" acyclic="<<acyclic<<" cyclic="<<cyclic<<" witnesses="<<h<<'\n';
    return incomplete?2:0;
} catch(const std::exception& e) {std::cerr<<e.what()<<'\n';return 1;}
