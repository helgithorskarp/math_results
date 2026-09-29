// CEGIS search for a shorter contiguous replacement. Exploratory until checked.
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

struct Limit {};
struct Rewrite {
    int n=0,width=0,budget=0,start=0;
    std::vector<std::pair<int,int>> net,alphabet,path;
    std::vector<std::vector<unsigned>> transform;
    std::vector<unsigned> witness,prefix;
    std::vector<std::vector<unsigned>> states;
    std::vector<unsigned char> accept,distance;
    std::uint64_t nodes=0,limit=100000000;
    unsigned restarts=0;
    static unsigned step(unsigned x,std::pair<int,int> c) {
        const auto [a,b]=c;
        return ((x>>a)&1U) && !((x>>b)&1U)? x^((1U<<a)|(1U<<b)):x;
    }
    bool sorted(unsigned x) const {
        const unsigned k=static_cast<unsigned>(std::popcount(x));
        return x==((1U<<k)-1U)<<(static_cast<unsigned>(n)-k);
    }
    bool disjoint(int a,int b) const {
        const auto x=alphabet[static_cast<std::size_t>(a)], y=alphabet[static_cast<std::size_t>(b)];
        return x.first!=y.first && x.first!=y.second && x.second!=y.first && x.second!=y.second;
    }
    // 0: excluded on current fixed witness set; 1: true construction; -1: restart.
    int dfs(int depth,int last) {
        if(++nodes>limit) throw Limit{};
        const auto& here=states[static_cast<std::size_t>(depth)];
        bool success=true;
        for(unsigned x:here) {
            if(distance[x]>budget-depth) return 0;
            if(!accept[x]) success=false;
        }
        if(success) {
            for(unsigned input=0;input<prefix.size();++input) {
                unsigned x=prefix[input];
                for(auto c:path) x=step(x,c);
                if(!accept[x]) {
                    if(std::find(witness.begin(),witness.end(),input)!=witness.end()) throw std::runtime_error("witness inconsistency");
                    witness.push_back(input);
                    return -1;
                }
            }
            return 1;
        }
        if(depth==budget) return 0;
        auto& child=states[static_cast<std::size_t>(depth+1)];
        for(int c=0;c<static_cast<int>(alphabet.size());++c) {
            if(last>c && disjoint(last,c)) continue;
            bool changed=false,pruned=false;
            for(std::size_t k=0;k<here.size();++k) {
                child[k]=transform[static_cast<std::size_t>(c)][here[k]];
                if(distance[child[k]]>budget-depth-1) {pruned=true;break;}
                changed|=child[k]!=here[k];
            }
            if(pruned || !changed) continue;
            path.push_back(alphabet[static_cast<std::size_t>(c)]);
            const int result=dfs(depth+1,c);
            if(result==1) return 1;
            path.pop_back();
            if(result==-1) return -1;
        }
        return 0;
    }
    void prepare(int s) {
        start=s;prefix.resize(1U<<n);accept.resize(prefix.size());distance.resize(prefix.size());
        for(unsigned x=0;x<prefix.size();++x) {
            unsigned p=x,t=x;
            for(int k=0;k<start;++k) p=step(p,net[static_cast<std::size_t>(k)]);
            for(int k=start+width;k<static_cast<int>(net.size());++k) t=step(t,net[static_cast<std::size_t>(k)]);
            prefix[x]=p;accept[x]=static_cast<unsigned char>(sorted(t));
        }
        for(int x=static_cast<int>(prefix.size())-1;x>=0;--x) {
            const auto u=static_cast<unsigned>(x);
            unsigned d=accept[u]?0U:255U;
            if(d) for(const auto& t:transform) if(t[u]>u) d=std::min(d,1U+distance[t[u]]);
            if(d==255) throw std::runtime_error("unreachable accepting state");
            distance[u]=static_cast<unsigned char>(d);
        }
    }
    int run() {
        for(;;) {
            states.assign(static_cast<std::size_t>(budget+1),std::vector<unsigned>(witness.size()));
            for(std::size_t k=0;k<witness.size();++k) states[0][k]=prefix[witness[k]];
            path.clear();
            const int status=dfs(0,-1);
            if(status>=0) return status;
            ++restarts;
        }
    }
};
int main(int argc,char** argv) try {
    if(argc!=8) throw std::runtime_error("usage: rewrite FIXTURE WITNESSES WIDTH BUDGET START END NODE_LIMIT");
    Rewrite r;std::ifstream f(argv[1]),w(argv[2]);int m=0,wn=0,h=0;
    if(!(f>>r.n>>m) || r.n<2 || r.n>16 || m<2) throw std::runtime_error("invalid fixture");
    for(int k=0;k<m;++k) {int a=0,b=0;if(!(f>>a>>b)||a<0||a>=b||b>=r.n)throw std::runtime_error("invalid comparator");r.net.emplace_back(a,b);}
    if(!(w>>wn>>h) || wn!=r.n || h<1) throw std::runtime_error("invalid witnesses");
    for(int k=0;k<h;++k) {unsigned x=0;if(!(w>>x)||x>=(1U<<r.n))throw std::runtime_error("invalid input");r.witness.push_back(x);}
    r.width=std::stoi(argv[3]);r.budget=std::stoi(argv[4]);const int begin=std::stoi(argv[5]),end=std::stoi(argv[6]);r.limit=std::stoull(argv[7]);
    if(r.width<1 || r.budget<0 || r.budget>=r.width || r.budget>8 || begin<0 || end<begin || end+r.width>m) throw std::runtime_error("invalid search range");
    for(int a=0;a<r.n;++a)for(int b=a+1;b<r.n;++b)r.alphabet.emplace_back(a,b);
    for(auto c:r.alphabet) {std::vector<unsigned> t(1U<<r.n);for(unsigned x=0;x<t.size();++x)t[x]=Rewrite::step(x,c);r.transform.push_back(std::move(t));}
    for(int s=begin;s<=end;++s) {
        r.prepare(s);
        const int status=r.run();
        std::cout<<"window="<<s<<" width="<<r.width<<" budget="<<r.budget<<" excluded="<<(status==0)<<" nodes="<<r.nodes<<" witnesses="<<r.witness.size()<<" restarts="<<r.restarts<<std::endl;
        if(status==1) {
            std::ofstream out(std::string(argv[2])+".rewrite-sorting-network.txt");
            out<<r.n<<' '<<m-r.width+r.path.size()<<'\n';
            for(int k=0;k<s;++k)out<<r.net[static_cast<std::size_t>(k)].first<<' '<<r.net[static_cast<std::size_t>(k)].second<<'\n';
            for(auto c:r.path)out<<c.first<<' '<<c.second<<'\n';
            for(int k=s+r.width;k<m;++k)out<<r.net[static_cast<std::size_t>(k)].first<<' '<<r.net[static_cast<std::size_t>(k)].second<<'\n';
            return 3;
        }
    }
    std::ofstream out(std::string(argv[2])+".rewrite-final.txt");out<<r.n<<' '<<r.witness.size()<<'\n';for(unsigned x:r.witness)out<<x<<'\n';
    return 0;
} catch(const Limit&) {std::cerr<<"INCOMPLETE: node limit reached\n";return 2;}
catch(const std::exception& e) {std::cerr<<e.what()<<'\n';return 1;}
