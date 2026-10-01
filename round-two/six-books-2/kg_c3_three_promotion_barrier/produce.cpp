// Exact three-promotion single/pair-clique census. C++17, one thread.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using Edge = std::pair<int,int>;
using Orbit = std::array<Edge,3>;
using Rows = std::array<std::uint32_t,22>;
constexpr std::uint32_t FULL = (std::uint32_t(1)<<22)-1;

void need(bool value, const std::string& message) {
    if (!value) throw std::runtime_error(message);
}
int count(std::uint32_t x) { return __builtin_popcount(x); }
Edge ordered(int u, int v) { return std::minmax(u,v); }

struct Input {
    std::vector<unsigned> labels;
    std::array<int,21> action;
    std::vector<Orbit> red, blue;
    Rows baseline{};
    Input() {
        std::array<int,7> ground{1,2,0,4,5,3,6};
        std::set<Edge> unused;
        for (int u=0;u<7;++u) for (int v=u+1;v<7;++v) unused.insert({u,v});
        while (!unused.empty()) {
            Edge start=*unused.begin(), step=start;
            for (int k=0;k<3;++k) {
                need(unused.erase(step)==1,"ground vertex orbit coverage");
                labels.push_back((1u<<step.first)|(1u<<step.second));
                step=ordered(ground[step.first],ground[step.second]);
            }
            need(step==start,"ground vertex orbit length");
        }
        need(labels.size()==21,"ground labels");
        for (int u=0;u<21;++u) {
            unsigned image=0;
            for (int i=0;i<7;++i) if (labels[u]>>i&1u) image|=1u<<ground[i];
            auto position=std::find(labels.begin(),labels.end(),image);
            need(position!=labels.end(),"vertex action image");
            action[u]=int(position-labels.begin());
        }
        unused.clear();
        for (int u=0;u<21;++u) for (int v=u+1;v<21;++v) unused.insert({u,v});
        while (!unused.empty()) {
            Edge start=*unused.begin(), step=start;
            Orbit orbit;
            bool disjoint=(labels[start.first]&labels[start.second])==0;
            for (int k=0;k<3;++k) {
                need(unused.erase(step)==1,"ground edge orbit coverage");
                need(((labels[step.first]&labels[step.second])==0)==disjoint,"edge orbit color");
                orbit[k]=step;
                step=ordered(action[step.first],action[step.second]);
            }
            need(step==start,"ground edge orbit length");
            (disjoint?red:blue).push_back(orbit);
        }
        need(red.size()==35 && blue.size()==35,"edge orbit counts");
        for (int u=0;u<21;++u) for (int v=0;v<21;++v)
            if (!(labels[u]&labels[v])) baseline[u]|=1u<<v;
        for (int u=0;u<21;++u) {
            need(count(baseline[u])==10,"KG degree control");
            for (int v=u+1;v<21;++v) {
                bool r=baseline[u]>>v&1u;
                std::uint32_t pages=r?(baseline[u]&baseline[v]):
                    ((1u<<21)-1)&~(baseline[u]|baseline[v]|(1u<<u)|(1u<<v));
                int literal=0;
                for (int w=0;w<21;++w) if (w!=u && w!=v)
                    literal+=r?((baseline[u]>>w&1u)&&(baseline[v]>>w&1u)):
                        (!(baseline[u]>>w&1u)&&!(baseline[v]>>w&1u));
                need(count(pages)==literal && literal==(r?3:5),"KG page control");
            }
        }
    }
};

void add(Rows& rows, const Orbit& orbit) {
    for (auto [u,v]:orbit) { rows[u]|=1u<<v; rows[v]|=1u<<u; }
}
void toggle(Rows& rows, const Orbit& orbit) {
    for (auto [u,v]:orbit) { rows[u]^=1u<<v; rows[v]^=1u<<u; }
}
bool blue_valid(const Rows& rows) {
    // Endpoints are explicitly excluded; no degree or red-book premise.
    for (int u=0;u<22;++u) {
        std::uint32_t blue_u=FULL&~(rows[u]|(1u<<u));
        std::uint32_t later=blue_u&~((1u<<(u+1))-1);
        while (later) {
            int v=__builtin_ctz(later); later&=later-1;
            if (count(blue_u&~(rows[v]|(1u<<v)))>6) return false;
        }
    }
    return true;
}

#include <fstream>
#include <limits>
template<class T> void print_vector(const std::vector<T>& v) {
    std::cout<<'[';
    for (std::size_t i=0;i<v.size();++i) { if(i) std::cout<<','; std::cout<<v[i]; }
    std::cout<<']';
}

struct Case {
    int index, weight;
    std::array<int,3> J,P;
};

struct Search {
    const Input& input;
    const std::vector<int>& pool;
    const std::vector<std::uint64_t>& compatibility;
    int target, index;
    std::uint64_t cliques=0, blue_good=0, two_good=0, degree_good=0;
    int best_red_bad=1000;
    std::vector<int> prefix, best;
    std::ofstream& critical;
    Search(const Input& in,const std::vector<int>& po,const std::vector<std::uint64_t>& co,
           int q,int i,std::ofstream& out):input(in),pool(po),compatibility(co),target(q),index(i),critical(out) {}
    void visit(Rows& rows, std::uint64_t available, int left) {
        if (!left) {
            ++cliques;
            bool blue=blue_valid(rows);
            if(blue) {
                ++blue_good;
                bool degrees=true;
                for(auto r:rows) if(count(r)<7 || count(r)>10) degrees=false;
                degree_good+=degrees;
                int red_bad=0;
                for(int u=0;u<22;++u) for(int v=u+1;v<22;++v)
                    if((rows[u]>>v&1u) && count(rows[u]&rows[v])>3) ++red_bad;
                if(red_bad<best_red_bad) { best_red_bad=red_bad; best=prefix; }
                if(!red_bad) {
                    ++two_good;
                    std::cerr<<"TWO_COLOR_WITNESS index="<<index<<" q="<<target<<'\n';
                }
            }
            critical<<index<<' '<<target<<' '<<int(blue);
            for(int d:prefix)critical<<' '<<d;
            critical<<'\n';
            need(bool(critical),"critical stream write");
            return;
        }
        while(available && __builtin_popcountll(available)>=left) {
            int bit=__builtin_ctzll(available);
            available&=available-1;
            prefix.push_back(pool[bit]);
            toggle(rows,input.red[pool[bit]]);
            visit(rows, available&compatibility[bit], left-1);
            toggle(rows,input.red[pool[bit]]);
            prefix.pop_back();
        }
    }
};

int main(int argc,char**argv) {
    try {
        std::string manifest, output;
        int first=0, limit=std::numeric_limits<int>::max();
        double seconds=25;
        for(int i=1;i<argc;++i) {
            std::string key=argv[i];
            need(i+1<argc,"missing option value");
            std::string value=argv[++i];
            if(key=="--manifest")manifest=value;
            else if(key=="--critical")output=value;
            else if(key=="--first")first=std::stoi(value);
            else if(key=="--limit")limit=std::stoi(value);
            else if(key=="--seconds")seconds=std::stod(value);
            else throw std::runtime_error("unknown option");
        }
        need(!manifest.empty() && !output.empty() && first>=0 && limit>0 && seconds>0 && seconds<=25,"options");
        std::ifstream source(manifest);
        need(bool(source),"manifest open");
        std::vector<Case> cases;
        Case entry;
        while(source>>entry.index>>entry.J[0]>>entry.J[1]>>entry.J[2]
              >>entry.P[0]>>entry.P[1]>>entry.P[2]>>entry.weight) {
            need(entry.index==int(cases.size()),"consecutive manifest indices");
            need(entry.J[0]>=0 && entry.J[0]<entry.J[1] && entry.J[1]<entry.J[2] && entry.J[2]<7,"J domain");
            need(entry.P[0]>=0 && entry.P[0]<entry.P[1] && entry.P[1]<entry.P[2] && entry.P[2]<35,"P domain");
            need(entry.weight>0 && 6%entry.weight==0,"case orbit weight");
            cases.push_back(entry);
        }
        need(source.eof() && first<=int(cases.size()),"manifest parse/first range");
        std::ofstream critical(output);
        need(bool(critical),"critical output open");
        Input input;
        auto started=std::chrono::steady_clock::now();
        int next=first;
        for(;next<int(cases.size()) && next-first<limit;++next) {
            if(next>first && std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count()>=seconds)break;
            auto c=cases[next];
            Rows rows=input.baseline;
            for(int p:c.P)add(rows,input.blue[p]);
            for(int j:c.J)for(int t=0;t<3;++t) {
                int u=3*j+t; rows[u]|=1u<<21; rows[21]|=1u<<u;
            }
            bool base=blue_valid(rows);
            std::vector<int> pool;
            if(base)for(int d=0;d<35;++d) {
                toggle(rows,input.red[d]);bool good=blue_valid(rows);toggle(rows,input.red[d]);
                if(good)pool.push_back(d);
            }
            std::vector<std::uint64_t> co(pool.size(),0);
            for(int i=0;i<int(pool.size());++i)for(int j=i+1;j<int(pool.size());++j) {
                toggle(rows,input.red[pool[i]]);toggle(rows,input.red[pool[j]]);
                bool good=blue_valid(rows);
                toggle(rows,input.red[pool[j]]);toggle(rows,input.red[pool[i]]);
                if(good) {co[i]|=std::uint64_t(1)<<j;co[j]|=std::uint64_t(1)<<i;}
            }
            std::uint64_t all=(std::uint64_t(1)<<pool.size())-1;
            Search seven(input,pool,co,7,next,critical),eight(input,pool,co,8,next,critical);
            seven.visit(rows,all,7);eight.visit(rows,all,8);
            std::cout<<"{\"index\":"<<next<<",\"weight\":"<<c.weight<<",\"base_blue_valid\":"<<(base?"true":"false")<<",\"pool\":";
            print_vector(pool);
            std::cout<<",\"compatibility\":";print_vector(co);
            std::cout<<",\"targets\":{";
            bool comma=false;
            for(auto* s:{&seven,&eight}) {
                if(comma)std::cout<<',';
                comma=true;
                std::cout<<'\"'<<s->target<<"\":{\"cliques\":"<<s->cliques<<",\"blue_valid\":"<<s->blue_good
                         <<",\"degree_valid\":"<<s->degree_good<<",\"two_color_valid\":"<<s->two_good
                         <<",\"best_red_bad\":"<<(s->best_red_bad==1000?-1:s->best_red_bad)<<",\"best\":";
                print_vector(s->best);std::cout<<'}';
            }
            std::cout<<"}}\n";
        }
        critical.flush();need(bool(critical),"critical flush");
        std::cout<<"{\"segment\":true,\"first\":"<<first<<",\"next\":"<<next<<",\"total\":"<<cases.size()
                 <<",\"complete\":"<<(next==int(cases.size())?"true":"false")<<",\"seconds\":"
                 <<std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count()<<"}\n";
        return 0;
    }catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 1;}
}
