// Exact native port of the independent whole-point-star completion search.
#include <array>
#include <algorithm>
#include <bit>
#include <cstdint>
#include <functional>
#include <iostream>
#include <limits>
#include <memory>
#include <stdexcept>
#include <vector>

template<std::size_t W> struct Bits {
    std::array<std::uint64_t,W> a{};
    void set(int i) { a[static_cast<unsigned>(i)/64] |= std::uint64_t(1)<<(i%64); }
    void clear(int i) { a[static_cast<unsigned>(i)/64] &= ~(std::uint64_t(1)<<(i%64)); }
    bool any() const { for(auto x:a) if(x) return true; return false; }
    int count() const { int n=0;for(auto x:a)n+=std::popcount(x);return n; }
    int first() const { for(std::size_t w=0;w<W;++w) if(a[w])return int(w*64)+std::countr_zero(a[w]);return -1; }
    Bits& operator&=(const Bits& b) { for(std::size_t i=0;i<W;++i)a[i]&=b.a[i];return *this; }
    Bits& operator|=(const Bits& b) { for(std::size_t i=0;i<W;++i)a[i]|=b.a[i];return *this; }
    void remove(const Bits& b) { for(std::size_t i=0;i<W;++i)a[i]&=~b.a[i]; }
    friend Bits operator&(Bits a,const Bits& b){return a&=b;}
};
using Domain=Bits<8>;
using Coverage=Bits<5>;
using Bundle=std::vector<int>;
using Bundles=std::vector<Bundle>;

std::vector<int> combinations(const std::vector<int>& vertices,int size) {
    std::vector<int> out;
    std::function<void(int,int,int)> go=[&](int start,int left,int mask){
        if(!left){out.push_back(mask);return;}
        for(int i=start;i<=int(vertices.size())-left;++i)go(i+1,left-1,mask|(1<<vertices[i]));
    };
    go(0,size,0);return out;
}

struct Universal {
    std::vector<int> vertices,triples,pairs;
    std::array<Coverage,8192> cover{};
    Coverage universe;
    Universal(){
        for(int p=0;p<13;++p)vertices.push_back(p);
        triples=combinations(vertices,3);pairs=combinations(vertices,2);
        for(int t=0;t<286;++t)universe.set(t);
        for(int b:combinations(vertices,6))
            for(int t=0;t<286;++t)if((b&triples[t])==triples[t])cover[b].set(t);
    }
};
const Universal& universal(){static const Universal u;return u;}

struct Space {
    std::vector<int> vertices,blocks,pairs,pair_ids;
    std::array<std::vector<int>,462> member,pair_member;
    std::array<Coverage,462> cover;
    std::array<Domain,11> through;
    std::array<Domain,55> through_pair;
    std::array<Domain,286> through_triple;
    std::array<Coverage,11> star;
    std::array<int,8192> block_id;
    Domain all;
    Space(int p,int r){
        const auto& u=universal();block_id.fill(-1);
        for(int x=0;x<13;++x)if(x!=p&&x!=r)vertices.push_back(x);
        blocks=combinations(vertices,6);pairs=combinations(vertices,2);
        if(blocks.size()!=462||pairs.size()!=55)throw std::runtime_error("space cardinality");
        for(int t:pairs){
            auto it=std::find(u.pairs.begin(),u.pairs.end(),t);
            pair_ids.push_back(int(it-u.pairs.begin()));
        }
        for(int i=0;i<462;++i){
            int b=blocks[i];block_id[b]=i;all.set(i);cover[i]=u.cover[b];
            for(int j=0;j<11;++j)if(b&(1<<vertices[j])){member[i].push_back(j);through[j].set(i);}
            for(int j=0;j<55;++j)if((b&pairs[j])==pairs[j]){pair_member[i].push_back(j);through_pair[j].set(i);}
            for(int j=0;j<286;++j)if((b&u.triples[j])==u.triples[j])through_triple[j].set(i);
        }
        for(int p0=0;p0<11;++p0)
            for(int t=0;t<286;++t)if(u.triples[t]&(1<<vertices[p0]))star[p0].set(t);
    }
};

struct Result {
    int status;
    int witness_size;
    std::uint64_t point_states;
    std::uint64_t bundle_states;
    std::uint16_t witness[21];
};

struct Solver {
    const Space& s;
    int h,q;
    std::array<int,11> remain;
    std::array<int,55> caps;
    std::uint64_t nodes=0,bundle_nodes=0;
    Bundle selected,witness;
    Solver(const Space& space,int high,int other):s(space),h(high),q(other){}
    static void bump(std::uint64_t& n){
        if(n==std::numeric_limits<std::uint64_t>::max())throw std::overflow_error("state count");
        ++n;
    }
    bool fits(int i) const {
        for(int p:s.member[i])if(remain[p]<=0)return false;
        for(int t:s.pair_member[i])if(caps[t]<=0)return false;
        return true;
    }
    void extend(Coverage missing,int left,Domain choices,Bundle& chosen,Bundles& answers){
        bump(bundle_nodes);
        if(!left){if(!missing.any())answers.push_back(chosen);return;}
        if(choices.count()<left||missing.count()>10*left)return;
        if(left==1){
            Domain possible=choices;
            while(missing.any()){
                int t=missing.first();missing.clear(t);possible&=s.through_triple[t];
            }
            while(possible.any()){
                int i=possible.first();possible.clear(i);
                if(fits(i)){chosen.push_back(i);answers.push_back(chosen);chosen.pop_back();}
            }
            return;
        }
        Domain candidates=choices;
        if(missing.any()){
            int best=463;Coverage todo=missing;
            while(todo.any()){
                int t=todo.first();todo.clear(t);Domain options=choices&s.through_triple[t];
                int n=options.count();if(n<best){best=n;candidates=options;}
            }
        }
        while(candidates.any()){
            int i=candidates.first();candidates.clear(i);choices.clear(i);
            if(!fits(i))continue;
            Domain future=choices;
            for(int p:s.member[i])if(--remain[p]==0)future.remove(s.through[p]);
            for(int t:s.pair_member[i])if(--caps[t]==0)future.remove(s.through_pair[t]);
            chosen.push_back(i);Coverage rest=missing;rest.remove(s.cover[i]);
            extend(rest,left-1,future,chosen,answers);chosen.pop_back();
            for(int t:s.pair_member[i])++caps[t];
            for(int p:s.member[i])++remain[p];
        }
    }
    Bundles all_bundles(int point,int degree,Coverage need,Domain domain){
        Domain available=domain&s.through[point];Bundles answers;
        if(degree<=2){
            Domain first=available;
            while(first.any()){
                int i=first.first();first.clear(i);bump(bundle_nodes);
                Coverage rest=need;rest.remove(s.cover[i]);
                if(degree==1){if(!rest.any())answers.push_back(Bundle{i});continue;}
                Domain possible=first;
                while(rest.any()){
                    int t=rest.first();rest.clear(t);possible&=s.through_triple[t];
                }
                for(int p:s.member[i])if(remain[p]==1)possible.remove(s.through[p]);
                for(int t:s.pair_member[i])if(caps[t]==1)possible.remove(s.through_pair[t]);
                while(possible.any()){
                    int j=possible.first();possible.clear(j);answers.push_back(Bundle{i,j});
                }
            }
            return answers;
        }
        Bundle chosen;extend(need,degree,available,chosen,answers);return answers;
    }
    bool visit(Coverage todo,int left,Domain domain){
        bump(nodes);
        for(int d:remain)if(d<0||d>left)return false;
        if(!left){
            if(todo.any()||std::any_of(remain.begin(),remain.end(),[](int d){return d!=0;}))return false;
            witness=selected;return true;
        }
        for(int p=0;p<11;++p){
            if(!remain[p])domain.remove(s.through[p]);
            if(remain[p]==left)domain&=s.through[p];
        }
        for(int t=0;t<55;++t){if(caps[t]<0)return false;if(!caps[t])domain.remove(s.through_pair[t]);}
        if(domain.count()<left)return false;
        std::vector<int> active;int degree=22;
        for(int p=0;p<11;++p)if(s.vertices[p]!=h&&s.vertices[p]!=q&&remain[p]){
            active.push_back(p);degree=std::min(degree,remain[p]);
        }
        if(active.empty())return false;
        int pivot=-1;Bundles best;
        for(int p:active){
            if(remain[p]!=degree)continue;
            Coverage need=todo&s.star[p];if(need.count()>10*degree)return false;
            Bundles bundles=all_bundles(p,degree,need,domain);if(bundles.empty())return false;
            if(pivot<0||bundles.size()<best.size()){pivot=p;best=std::move(bundles);}
            if(degree>2)break;
        }
        Domain future=domain;future.remove(s.through[pivot]);
        for(const Bundle& bundle:best){
            Coverage rest=todo;
            for(int i:bundle){
                rest.remove(s.cover[i]);
                for(int p:s.member[i])--remain[p];
                for(int t:s.pair_member[i])--caps[t];
            }
            selected.insert(selected.end(),bundle.begin(),bundle.end());
            bool found=visit(rest,left-degree,future);
            selected.resize(selected.size()-bundle.size());
            for(int i:bundle){for(int t:s.pair_member[i])++caps[t];for(int p:s.member[i])++remain[p];}
            if(found)return true;
        }
        return false;
    }
};

extern "C" int cover_solve(int p,int r,int total,int h,int q,int fixed_count,
                            const std::uint16_t* fixed,const int* targets,
                            const int* pair_bounds,Result* result){
    try {
        *result=Result{};
        if(p<0||p>=13||r<0||r>=13||p==r||h<0||h>=13||q<0||q>=13||
           total<0||total>21||fixed_count<0||fixed_count>total)throw std::runtime_error("invalid dimensions");
        std::array<bool,8192> seen{};
        for(int i=0;i<fixed_count;++i){
            unsigned b=fixed[i];if(b>=8192||std::popcount(b)!=6||seen[b])throw std::runtime_error("invalid block");seen[b]=true;
        }
        for(int x=0;x<13;++x)if(targets[x]<0||targets[x]>21)throw std::runtime_error("invalid target");
        for(int t=0;t<78;++t)if(pair_bounds[t]<0||pair_bounds[t]>21)throw std::runtime_error("invalid pair bound");
        static std::array<std::unique_ptr<Space>,169> cache;
        auto& entry=cache[p*13+r];if(!entry)entry=std::make_unique<Space>(p,r);
        const Space& space=*entry;Solver solver(space,h,q);
        for(int x=0;x<11;++x){
            solver.remain[x]=targets[space.vertices[x]];
            for(int j=0;j<fixed_count;++j)solver.remain[x]-=(fixed[j]>>space.vertices[x])&1;
        }
        for(int t=0;t<55;++t){
            solver.caps[t]=pair_bounds[space.pair_ids[t]];
            for(int j=0;j<fixed_count;++j)solver.caps[t]-=((fixed[j]&space.pairs[t])==space.pairs[t]);
        }
        Coverage missing=universal().universe;Domain domain=space.all;
        for(int j=0;j<fixed_count;++j){
            missing.remove(universal().cover[fixed[j]]);
            int index=space.block_id[fixed[j]];if(index>=0)domain.clear(index);
        }
        bool found=solver.visit(missing,total-fixed_count,domain);
        result->status=found?1:0;result->point_states=solver.nodes;result->bundle_states=solver.bundle_nodes;
        result->witness_size=int(solver.witness.size());
        for(int i=0;i<result->witness_size;++i)result->witness[i]=std::uint16_t(space.blocks[solver.witness[i]]);
        return 0;
    } catch(...) { if(result)result->status=-1;return -1; }
}

#ifdef COVER_AUDIT_MAIN
int main(){
    int p,r,total,h,q,n;
    while(std::cin>>p>>r>>total>>h>>q>>n){
        if(n<0||n>21)return 2;
        std::array<int,13> targets{};std::array<int,78> bounds{};std::array<std::uint16_t,21> fixed{};
        for(int& x:targets)if(!(std::cin>>x))return 2;
        for(int& x:bounds)if(!(std::cin>>x))return 2;
        for(int i=0;i<n;++i){unsigned b;if(!(std::cin>>b)||b>=8192)return 2;fixed[i]=std::uint16_t(b);}
        Result out{};if(cover_solve(p,r,total,h,q,n,fixed.data(),targets.data(),bounds.data(),&out))return 3;
        std::cout<<out.status<<' '<<out.point_states<<' '<<out.bundle_states;
        for(int i=0;i<out.witness_size;++i)std::cout<<' '<<out.witness[i];
        std::cout<<'\n';
    }
    return std::cin.eof()?0:2;
}
#endif
