// six-reviewer-2: fresh quota branch kernel, exact unsigned arithmetic only.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using Bits = unsigned __int128;
struct Column { unsigned word; Bits pairs; int hh; };
struct Search {
    std::vector<Column> columns;
    unsigned high;
    std::uint64_t nodes=0, cap=200000;
    std::chrono::steady_clock::time_point start;
    std::vector<unsigned> chosen, witness;
    bool visit(std::array<int,15> q, Bits mandatory, int budget,
               const std::vector<int>& available) {
        if (++nodes>cap || std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()>10.0)
            throw std::runtime_error("INCOMPLETE native quota guard");
        int sum=0; for(int t:q) sum+=t;
        if(sum==0) {
            if(mandatory || budget!=0) return false;
            witness=chosen; return true;
        }
        if(sum%4 || budget<0) throw std::runtime_error("invalid recursive quota state");
        std::vector<int> active;
        std::array<std::vector<int>,15> at;
        for(int i:available) {
            const auto& c=columns[i];
            bool ok=c.hh<=budget;
            for(int z=0;z<15;++z) if((c.word>>z&1U) && q[z]==0) ok=false;
            if(ok) { active.push_back(i); for(int z=0;z<15;++z) if(c.word>>z&1U) at[z].push_back(i); }
        }
        if(active.size()<static_cast<std::size_t>(sum/4)) return false;
        std::vector<int> choices;
        std::size_t best=1000;
        for(int z=0;z<15;++z) if(q[z]) {
            if(at[z].size()<static_cast<std::size_t>(q[z])) return false;
            if(at[z].size()<best) { best=at[z].size(); choices=at[z]; }
        }
        for(int r=0;r<105;++r) if((mandatory>>r)&1U) {
            std::vector<int> list;
            for(int i:active) if((columns[i].pairs>>r)&1U) list.push_back(i);
            if(list.empty()) return false;
            if(list.size()<best) { best=list.size(); choices=std::move(list); }
        }
        if(choices.empty()) throw std::runtime_error("missing branch choices");
        for(int i:choices) {
            const auto& c=columns[i]; auto nextq=q;
            for(int z=0;z<15;++z) if(c.word>>z&1U) --nextq[z];
            std::vector<int> next;
            for(int j:active) if(!(columns[j].pairs&c.pairs)) next.push_back(j);
            chosen.push_back(c.word);
            if(visit(nextq,mandatory&~c.pairs,budget-c.hh,next)) return true;
            chosen.pop_back();
        }
        return false;
    }
};
static Bits pairs(unsigned w) {
    Bits result=0; int r=0;
    for(int u=0;u<15;++u) for(int v=u+1;v<15;++v,++r)
        if((w>>u&1U)&&(w>>v&1U)) result |= Bits(1)<<r;
    return result;
}
int main(int argc,char** argv) {
    try {
        if(argc!=3 && argc!=4) throw std::runtime_error("usage: quota INPUT OUTPUT [cap<=200000]");
        std::uint64_t cap=200000;
        if(argc==4) { std::size_t used=0; cap=std::stoull(argv[3],&used);
            if(used!=std::string(argv[3]).size() || cap>200000) throw std::runtime_error("invalid/raised cap"); }
        std::ifstream in(argv[1]); std::ofstream out(argv[2]);
        if(!in || !out) throw std::runtime_error("input/output failure");
        long long count; if(!(in>>count)||count<0||count>300000) throw std::runtime_error("invalid case count");
        for(long long k=0;k<count;++k) {
            long long n,h,b; std::uint64_t lo,hi;
            if(!(in>>n>>h>>b>>lo>>hi)||n<0||n>96||h<0||h>=32768||b<0||b>10||hi>>41)
                throw std::runtime_error("malformed case header");
            Search s; s.high=static_cast<unsigned>(h); s.cap=cap;
            std::array<int,15> q{};
            for(int& t:q) if(!(in>>t)||t<0||t>5) throw std::runtime_error("malformed quota");
            if(!std::all_of(q.begin(),q.end(),[](int t){return t>=0;})) throw std::runtime_error("negative quota");
            std::vector<int> available;
            for(int i=0;i<n;++i) {
                long long w; if(!(in>>w)||w<=0||w>=32768||__builtin_popcount(static_cast<unsigned>(w))!=4)
                    throw std::runtime_error("malformed column");
                for(const auto& c:s.columns) if(c.word==static_cast<unsigned>(w)) throw std::runtime_error("duplicate column");
                s.columns.push_back({static_cast<unsigned>(w),pairs(static_cast<unsigned>(w)),
                    __builtin_popcount(static_cast<unsigned>(w)&s.high)*(__builtin_popcount(static_cast<unsigned>(w)&s.high)-1)/2});
                available.push_back(i);
            }
            int sum=0;for(int t:q)sum+=t;
            if(sum%4) throw std::runtime_error("nonintegral word quota");
            s.start=std::chrono::steady_clock::now();
            bool sat=s.visit(q,Bits(lo)|(Bits(hi)<<64),static_cast<int>(b),available);
            out<<k<<' '<<sat<<' '<<s.nodes<<' '<<s.witness.size();
            for(unsigned w:s.witness)out<<' '<<w;
            out<<'\n';
            if(!out) throw std::runtime_error("output failure");
        }
        std::string extra;if(in>>extra)throw std::runtime_error("trailing input");
        if(!in.eof())throw std::runtime_error("input parse failure");
    } catch(const std::exception& e) { std::cerr<<e.what()<<'\n';return 2; }
}
