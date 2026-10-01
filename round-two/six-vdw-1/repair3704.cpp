// Untrusted construction heuristic. Positive cost is never an exclusion.
// Hard edit floors are guidance from the published uniform65 QR617 result.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <fstream>
#include <iostream>
#include <limits>
#include <numeric>
#include <random>
#include <stdexcept>
#include <string>
#include <vector>
#include "column-blocks/block12.hpp"

constexpr int N = 3704, E = 1141450;
struct Edge { std::array<int,7> p; int count=0, weight=1; };
struct Move { int x=-1, y=-1, raw=0; std::int64_t weighted=0; };
struct Macro { std::vector<int> points; int raw=0; std::int64_t weighted=0; int kind=0; };
int mono(int n) { return static_cast<int>(n==0 || n==7); }

struct Search {
    std::array<int,N> bits{}, best{}, reference{}, group{};
    std::array<int,N> gain{};
    std::array<std::int64_t,N> weighted_gain{};
    std::array<std::uint64_t,N> tabu{};
    std::vector<Edge> edge;
    std::vector<int> offsets, incidence, bad, slot;
    std::array<int,2> edits{};
    std::mt19937_64 rng;
    std::uint64_t iteration=0, penalties=0;
    int best_cost=std::numeric_limits<int>::max();
    std::int64_t weighted_cost=0;
    // Invocation diagnostics do not affect the resumable trajectory.
    std::uint64_t block_evaluations=0;
    std::array<std::uint64_t,4> moves{};
    std::array<std::uint64_t,13> move_sizes{};

    explicit Search(std::uint64_t seed):rng(seed) {}
    static void require(bool ok,const char* message) {
        if(!ok) throw std::runtime_error(message);
    }
    bool admissible(int x) const {
        const int g=group[x];
        if(g<0 || bits[x]==reference[x]) return true;
        return edits[g]>30 && edits[0]+edits[1]>65;
    }
    void recount_edits() {
        edits={};
        for(int x=0;x<N;++x) if(group[x]>=0 && bits[x]!=reference[x]) ++edits[group[x]];
        require(edits[0]>=30 && edits[1]>=30 && edits[0]+edits[1]>=65,"edit floor violated");
    }
    void set_bad(int id) {
        const bool wanted=mono(edge[id].count)!=0;
        if(wanted && slot[id]<0) { slot[id]=static_cast<int>(bad.size()); bad.push_back(id); }
        else if(!wanted && slot[id]>=0) {
            const int i=slot[id], last=bad.back();
            bad[i]=last; slot[last]=i; bad.pop_back(); slot[id]=-1;
        }
    }
    void rebuild() {
        gain={}; weighted_gain={}; weighted_cost=0;
        slot.assign(E,-1); bad.clear();
        for(int id=0;id<E;++id) {
            Edge& e=edge[id]; e.count=0;
            for(int x:e.p) e.count+=bits[x];
            weighted_cost+=static_cast<std::int64_t>(e.weight)*mono(e.count);
            for(int x:e.p) {
                const int d=mono(e.count+1-2*bits[x])-mono(e.count);
                gain[x]+=d; weighted_gain[x]+=static_cast<std::int64_t>(e.weight)*d;
            }
            set_bad(id);
        }
        recount_edits();
    }
    int count(const std::array<int,N>& word) const {
        int total=0;
        for(const Edge& e:edge) {
            int ones=0; for(int x:e.p) ones+=word[x]; total+=mono(ones);
        }
        return total;
    }
    void initialize(const std::string& path,const std::string& start_word="") {
        std::array<int,617> qr{}; qr.fill(1); qr[0]=0;
        for(int x=1;x<617;++x) qr[x*x%617]=0;
        group.fill(-1);
        for(int x=0;x<N;++x) {
            reference[x]=qr[x%617];
            if(x<3703 && x%617) group[x]=reference[x];
        }
        bits=reference; bits[3702]=1;
        std::array<std::vector<int>,2> classes;
        for(int x=0;x<N;++x) if(group[x]>=0) classes[group[x]].push_back(x);
        for(auto& c:classes) {
            std::shuffle(c.begin(),c.end(),rng);
            for(int j=0;j<30;++j) bits[c[j]]^=1;
        }
        for(int j=30;j<35;++j) bits[classes[0][j]]^=1;
        // Seed the unavoidable endpoint-zero 617-step progression with an edit.
        if(bits[1]==reference[1]) {
            bits[classes[0][34]]^=1; bits[1]^=1;
        }
        if(!start_word.empty()) {
            require(!std::ifstream(path),"start-word requires a fresh checkpoint path");
            std::ifstream seed(start_word); std::string word,extra;
            seed>>word; require(static_cast<bool>(seed) && word.size()==N,"invalid start-word length");
            for(int x=0;x<N;++x) {
                require(word[x]=='0' || word[x]=='1',"nonbinary start word");
                bits[x]=word[x]-'0';
            }
            require(!(seed>>extra),"trailing start-word data");
        }
        edge.reserve(E);
        offsets.assign(N+1,0);
        for(int d=1;6*d<N;++d) for(int a=0;a+6*d<N;++a) {
            Edge e;
            for(int j=0;j<7;++j) { e.p[j]=a+j*d; ++offsets[e.p[j]+1]; }
            edge.push_back(e);
        }
        require(edge.size()==E,"AP coverage mismatch");
        std::partial_sum(offsets.begin(),offsets.end(),offsets.begin());
        incidence.resize(static_cast<std::size_t>(7)*E);
        auto next=offsets;
        for(int id=0;id<E;++id) for(int x:edge[id].p) incidence[next[x]++]=id;
        std::vector<int> saved_bad;
        bool restored=false;
        std::ifstream in(path);
        if(in) {
            std::string header, current, saved_best;
            in>>header>>iteration>>penalties>>best_cost>>current>>saved_best;
            require((header=="VDW3704PAWS1" || header=="VDW3704PAWS2" || header=="VDW3704PAWS3") &&
                    iteration<=1000000000000ULL && penalties<=1000000000000ULL,
                    "invalid checkpoint header");
            require(current.size()==N && saved_best.size()==N,"wrong checkpoint word length");
            for(int x=0;x<N;++x) {
                require((current[x]=='0'||current[x]=='1') && (saved_best[x]=='0'||saved_best[x]=='1'),
                        "nonbinary checkpoint word");
                bits[x]=current[x]-'0'; best[x]=saved_best[x]-'0';
            }
            for(auto& t:tabu) in>>t;
            int n=-1, old_id=-1;
            in>>n; require(n>=0 && n<=E,"invalid weighted edge count");
            for(int j=0;j<n;++j) {
                int id=-1,w=-1; in>>id>>w;
                require(id>old_id && id<E && w>1 && w<=1000000,"invalid edge weight");
                edge[id].weight=w; old_id=id;
            }
            in>>n; require(n>=0 && n<=E,"invalid bad-list size");
            saved_bad.resize(static_cast<std::size_t>(n)); for(int& id:saved_bad) in>>id;
            in>>rng; require(static_cast<bool>(in),"truncated checkpoint");
            std::string extra; require(!(in>>extra),"trailing checkpoint data");
            restored=true;
        }
        rebuild();
        if(restored) {
            require(saved_bad.size()==bad.size(),"bad-list coverage mismatch");
            std::vector<int> seen(E,0);
            for(int id:saved_bad) require(id>=0 && id<E && slot[id]>=0 && !seen[id]++,"bad-list record");
            bad=saved_bad; std::fill(slot.begin(),slot.end(),-1);
            for(int i=0;i<static_cast<int>(bad.size());++i) slot[bad[i]]=i;
            require(best_cost>=0 && count(best)==best_cost,"best checkpoint cost mismatch");
            const auto current=bits; bits=best; recount_edits(); bits=current; recount_edits();
        } else { best=bits; best_cost=static_cast<int>(bad.size()); }
    }
    void audit() const {
        std::array<int,N> fresh_gain{};
        std::array<std::int64_t,N> fresh_weighted{};
        std::array<int,2> fresh_edits{};
        std::int64_t fresh_cost=0;
        for(int x=0;x<N;++x) if(group[x]>=0 && bits[x]!=reference[x]) ++fresh_edits[group[x]];
        for(int id=0;id<E;++id) {
            const Edge& e=edge[id]; int sum=0; for(int x:e.p) sum+=bits[x];
            require(sum==e.count && (slot[id]>=0)==(mono(sum)!=0),"AP cache mismatch");
            fresh_cost+=static_cast<std::int64_t>(e.weight)*mono(sum);
            for(int x:e.p) {
                const int d=mono(sum+1-2*bits[x])-mono(sum);
                fresh_gain[x]+=d; fresh_weighted[x]+=static_cast<std::int64_t>(e.weight)*d;
            }
        }
        require(fresh_gain==gain && fresh_weighted==weighted_gain && fresh_cost==weighted_cost &&
                fresh_edits==edits && count(bits)==static_cast<int>(bad.size()),"score/cost cache mismatch");
        require(edits[0]>=30 && edits[1]>=30 && edits[0]+edits[1]>=65,"audit edit floors");
    }
    void flip(int x) {
        const int old=bits[x], delta=gain[x];
        const auto weighted_delta=weighted_gain[x];
        for(int k=offsets[x];k<offsets[x+1];++k) {
            const int id=incidence[k]; Edge& e=edge[id];
            const int before=e.count, after=before+1-2*old;
            require(after>=0 && after<=7,"invalid AP count");
            for(int y:e.p) if(y!=x) {
                const int difference=(mono(after+1-2*bits[y])-mono(after))-
                                     (mono(before+1-2*bits[y])-mono(before));
                gain[y]+=difference;
                weighted_gain[y]+=static_cast<std::int64_t>(e.weight)*difference;
            }
            e.count=after; set_bad(id);
        }
        if(group[x]>=0) edits[group[x]]+=(old==reference[x]?1:-1);
        bits[x]^=1; gain[x]=-delta; weighted_gain[x]=-weighted_delta;
        weighted_cost+=weighted_delta;
        tabu[x]=iteration+3+rng()%8;
        if(static_cast<int>(bad.size())<best_cost) {
            best_cost=static_cast<int>(bad.size()); best=bits;
            std::cout<<"best "<<best_cost<<" iteration "<<iteration<<" edits "<<edits[0]<<' '<<edits[1]<<'\n'<<std::flush;
        }
    }
    void penalize() {
        ++penalties;
        for(int id:bad) {
            Edge& e=edge[id]; require(e.weight<1000000,"weight cap reached");
            ++e.weight; ++weighted_cost; for(int x:e.p) --weighted_gain[x];
        }
        // PAWS-style smoothing: positive weights remain positive.
        if(rng()%100==0) for(Edge& e:edge) if(e.weight>1) {
            --e.weight; weighted_cost-=mono(e.count);
            for(int x:e.p) weighted_gain[x]-=mono(e.count+1-2*bits[x])-mono(e.count);
        }
    }
    Move joint_delta(int x,int y) const {
        require(x!=y,"duplicate pair point");
        Move result{x,y,gain[x]+gain[y],weighted_gain[x]+weighted_gain[y]};
        const int lower=std::min(x,y), upper=std::max(x,y), difference=upper-lower;
        const int dx=1-2*bits[x], dy=1-2*bits[y];
        // An AP containing both points chooses their slot gap 1..6. At most
        // sum_(gap=1)^6 (7-gap)=21 shared windows need interaction corrections.
        for(int gap=1;gap<=6;++gap) if(difference%gap==0) {
            const int d=difference/gap;
            for(int j=0;j+gap<7;++j) {
                const int a=lower-j*d;
                if(a<0 || a+6*d>=N) continue;
                const int id=(d-1)*N-3*d*(d-1)+a;
                require(id>=0 && id<E,"shared AP index");
                const Edge& e=edge[id];
                const int correction=mono(e.count+dx+dy)-mono(e.count+dx)-mono(e.count+dy)+mono(e.count);
                result.raw+=correction;
                result.weighted+=static_cast<std::int64_t>(e.weight)*correction;
            }
        }
        return result;
    }
    Move choose(const Edge& selected) {
        std::array<std::vector<int>,2> replacement;
        for(int y=0;y<N;++y) if(group[y]>=0 && bits[y]==reference[y]) replacement[group[y]].push_back(y);
        for(auto& row:replacement) {
            const auto size=std::min<std::size_t>(12,row.size());
            std::partial_sort(row.begin(),row.begin()+static_cast<std::ptrdiff_t>(size),row.end(),
                              [&](int a,int b){return weighted_gain[a]==weighted_gain[b]?a<b:weighted_gain[a]<weighted_gain[b];});
            row.resize(size);
        }
        Move chosen; std::uint64_t ties=0;
        for(int pass=0;pass<2 && chosen.x<0;++pass) {
            auto consider=[&](Move candidate) {
                if(pass==0 && (tabu[candidate.x]>iteration ||
                   (candidate.y>=0 && tabu[candidate.y]>iteration)) &&
                   static_cast<int>(bad.size())+candidate.raw>=best_cost) return;
                if(chosen.x<0 || candidate.weighted<chosen.weighted) { chosen=candidate; ties=0; }
                if(candidate.weighted==chosen.weighted && rng()%(++ties)==0) chosen=candidate;
            };
            for(int x:selected.p) {
                if(admissible(x)) consider(Move{x,-1,gain[x],weighted_gain[x]});
                if(group[x]>=0 && bits[x]!=reference[x])
                    for(int y:replacement[group[x]]) consider(joint_delta(x,y));
            }
        }
        require(chosen.x>=0,"no admissible move on bad progression");
        return chosen;
    }
    vdw::Block12 block(int r,int s) const {
        vdw::Block12 result(r,s);
        for(int i=0;i<12;++i) result.linear[i]={gain[result.point[i]],weighted_gain[result.point[i]]};
        for(int i=0;i<6;++i) for(int j=0;j<6;++j) {
            const auto pair=joint_delta(result.point[i],result.point[j+6]);
            result.cross[i][j]={pair.raw-gain[result.point[i]]-gain[result.point[j+6]],
                               pair.weighted-weighted_gain[result.point[i]]-weighted_gain[result.point[j+6]]};
        }
        return result;
    }
    vdw::Minimum minimum(const vdw::Block12& model) const {
        std::array<int,2> classes{group[model.point[0]],group[model.point[6]]};
        std::array<int,12> edited{}; auto outside=edits;
        for(int i=0;i<12;++i) {
            edited[i]=bits[model.point[i]]!=reference[model.point[i]];
            outside[classes[i/6]]-=edited[i];
        }
        return model.minimum(classes,outside,edited);
    }
    void sweep(double seconds,const std::string& path) {
        // Freeze the word and enumerate ordinary-column pairs. Dynamic
        // weights play no part in this raw-count construction move.
        const auto begin=std::chrono::steady_clock::now();
        std::uint64_t visited=0; bool stopped=false;
        int selected_r=2,selected_s=3; vdw::Minimum chosen{true,0,{}};
        const int before=static_cast<int>(bad.size());
        std::string word; for(int b:bits) word.push_back(static_cast<char>('0'+b));
        const std::string state_path=path+".sweep-state";
        std::ifstream state(state_path);
        if(state) {
            std::string version,saved_word;
            state>>version>>visited>>selected_r>>selected_s>>chosen.mask>>chosen.value.raw>>saved_word;
            require(static_cast<bool>(state) && version=="VDWSWEEP1" && visited<=188805 &&
                    chosen.mask<4096 && chosen.value.raw<=0,"invalid sweep-state record");
            if(saved_word!=word) {
                require(visited==188805,"partial sweep belongs to a different word");
                visited=0; selected_r=2; selected_s=3; chosen={true,0,{}};
            } else {
                const auto gain=block(selected_r,selected_s).evaluate(chosen.mask);
                require(gain.raw==chosen.value.raw,"saved sweep move gain mismatch");
                chosen.value.weighted=chosen.value.raw;
            }
        }
        auto checkpoint=[&]() {
            std::ofstream out(state_path+".partial");
            out<<"VDWSWEEP1 "<<visited<<' '<<selected_r<<' '<<selected_s<<' '<<chosen.mask<<' '
               <<chosen.value.raw<<'\n'<<word<<'\n';
            out.close(); require(static_cast<bool>(out),"sweep-state write failed");
            require(std::rename((state_path+".partial").c_str(),state_path.c_str())==0,"sweep-state rename failed");
        };
        const auto resume_at=visited; std::uint64_t pair_index=0;
        for(int r=2;r<617 && !stopped;++r) for(int s=r+1;s<617;++s) {
            if(pair_index++<resume_at) continue;
            auto model=block(r,s);
            for(auto& cost:model.linear) cost.weighted=cost.raw;
            for(auto& row:model.cross) for(auto& cost:row) cost.weighted=cost.raw;
            const auto candidate=minimum(model); ++visited;
            require(candidate.feasible,"identity should satisfy guidance floors");
            if(candidate.value.raw<chosen.value.raw) {
                chosen=candidate; selected_r=r; selected_s=s;
            }
            if(visited%256==0) checkpoint();
            if(visited%256==0 &&
               std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count()>seconds) {
                stopped=true; break;
            }
        }
        checkpoint();
        const auto selected=block(selected_r,selected_s);
        std::vector<int> increasing,decreasing;
        for(int i=0;i<12;++i) if(chosen.mask&(1U<<i)) {
            const int x=selected.point[i];
            (bits[x]==reference[x]?increasing:decreasing).push_back(x);
        }
        if(visited==188805) {
            ++iteration;
            for(const auto* list:{&increasing,&decreasing}) for(int x:*list) flip(x);
            require(static_cast<std::int64_t>(bad.size())-before==chosen.value.raw,"sweep move gain mismatch");
        }
        std::ofstream report(path+".sweep.json");
        report<<"{\"column_pairs_visited\":"<<visited<<",\"complete\":"<<(visited==188805?"true":"false")
              <<",\"before_cost\":"<<before<<",\"delta\":"<<chosen.value.raw<<",\"r\":"<<selected_r
              <<",\"s\":"<<selected_s<<",\"mask\":"<<chosen.mask<<",\"after_cost\":"<<bad.size()<<"}\n";
        report.close(); require(static_cast<bool>(report),"sweep report write failed");
        std::cout<<"sweep pairs "<<visited<<" complete "<<(visited==188805)<<" gain "<<chosen.value.raw
                 <<" columns "<<selected_r<<' '<<selected_s<<" mask "<<chosen.mask<<'\n';
    }
    bool macro_admissible(const std::vector<int>& points) const {
        auto fresh=edits;
        for(int x:points) if(group[x]>=0) fresh[group[x]]+=bits[x]==reference[x]?1:-1;
        return fresh[0]>=30 && fresh[1]>=30 && fresh[0]+fresh[1]>=65;
    }
    Macro choose_block(int r,int s) {
        ++block_evaluations;
        const auto model=block(r,s);
        Macro chosen; chosen.weighted=std::numeric_limits<std::int64_t>::max();
        std::uint64_t ties=0;
        model.all([&](unsigned mask,vdw::Cost cost) {
            if(mask==0 || cost.weighted>chosen.weighted) return;
            std::vector<int> points;
            for(int i=0;i<12;++i) if(mask&(1U<<i)) points.push_back(model.point[i]);
            if(!macro_admissible(points)) return;
            if(static_cast<std::int64_t>(bad.size())+cost.raw>=best_cost &&
               std::any_of(points.begin(),points.end(),[&](int x){return tabu[x]>iteration;})) return;
            require(cost.raw>=-E && cost.raw<=E,"block raw gain range");
            if(cost.weighted<chosen.weighted) { chosen={points,static_cast<int>(cost.raw),cost.weighted,1}; ties=0; }
            if(cost.weighted==chosen.weighted && rng()%(++ties)==0)
                chosen={points,static_cast<int>(cost.raw),cost.weighted,1};
        });
        return chosen;
    }
    void step() {
        ++iteration;
        const Edge selected=edge[bad[rng()%bad.size()]];
        int r=-1,s=-1;
        if(rng()%4==0) {
            std::vector<int> residues;
            for(int x:selected.p) if(x%617>=2) residues.push_back(x%617);
            std::sort(residues.begin(),residues.end());
            residues.erase(std::unique(residues.begin(),residues.end()),residues.end());
            if(residues.size()>=2) {
                std::shuffle(residues.begin(),residues.end(),rng); r=residues[0]; s=residues[1];
            }
        }
        auto selection=[&]() {
            const Move small=choose(selected);
            Macro chosen{{small.x},small.raw,small.weighted};
            if(small.y>=0) chosen.points.push_back(small.y);
            if(r>=0) {
                Macro candidate=choose_block(r,s);
                if(!candidate.points.empty() && candidate.weighted<chosen.weighted) chosen=candidate;
            }
            return chosen;
        };
        Macro chosen=selection();
        if(chosen.weighted>=0) { penalize(); chosen=selection(); }
        // Occasional unbiased legal moves prevent purely greedy trapping.
        if(rng()%100<2) {
            std::uint64_t ties=0;
            for(int x:selected.p) if(admissible(x) && rng()%(++ties)==0)
                chosen=Macro{{x},gain[x],weighted_gain[x],3};
            // A coherent uphill column move crosses several coordinate
            // barriers in one iteration. Its exact gain is additive.
            if(rng()%2==0) {
                const int column=selected.p[rng()%7]%617;
                if(column>=2) {
                    Macro coherent;
                    coherent.kind=2;
                    for(int k=0;k<6;++k) {
                        const int x=column+617*k; coherent.points.push_back(x);
                        coherent.raw+=gain[x]; coherent.weighted+=weighted_gain[x];
                    }
                    if(macro_admissible(coherent.points)) chosen=coherent;
                }
            }
        }
        const int old_cost=static_cast<int>(bad.size()); const auto old_weighted=weighted_cost;
        ++moves.at(static_cast<std::size_t>(chosen.kind));
        ++move_sizes.at(chosen.points.size());
        // Add edits before reverting edits. Every intermediate word obeys
        // the lower guidance floors, so intermediate best words are valid
        // proposals in the same heuristic domain.
        std::vector<int> increasing,decreasing;
        for(int x:chosen.points)
            (group[x]<0 || bits[x]==reference[x]?increasing:decreasing).push_back(x);
        for(const auto* list:{&increasing,&decreasing}) for(int x:*list) {
            flip(x); if(bad.empty()) return;
        }
        require(static_cast<int>(bad.size())-old_cost==chosen.raw &&
                weighted_cost-old_weighted==chosen.weighted,"macro move gain mismatch");
    }
    void save(const std::string& path) const {
        std::ofstream out(path+".partial");
        out<<"VDW3704PAWS3 "<<iteration<<' '<<penalties<<' '<<best_cost<<'\n';
        for(int b:bits) { out<<b; } out<<'\n';
        for(int b:best) { out<<b; } out<<'\n';
        for(auto t:tabu) { out<<t<<' '; } out<<'\n';
        int n=0; for(const Edge& e:edge) n+=e.weight>1;
        out<<n<<'\n';
        for(int id=0;id<E;++id) if(edge[id].weight>1) out<<id<<' '<<edge[id].weight<<'\n';
        out<<bad.size()<<' '; for(int id:bad) out<<id<<' '; out<<'\n'<<rng<<'\n';
        out.close(); require(static_cast<bool>(out),"checkpoint write failed");
        require(std::rename((path+".partial").c_str(),path.c_str())==0,"checkpoint rename failed");
        std::ofstream word(path+".best.bits"); for(int b:best) word<<b; word<<'\n';
        word.close(); require(static_cast<bool>(word),"best word write failed");
        std::ofstream stats(path+".gains");
        stats<<bad.size()<<' '<<weighted_cost<<' '<<edits[0]<<' '<<edits[1]<<'\n';
        for(int d:gain) { stats<<d<<' '; } stats<<'\n';
        for(auto d:weighted_gain) { stats<<d<<' '; } stats<<'\n';
        stats.close(); require(static_cast<bool>(stats),"gain audit write failed");
        std::ofstream pairs(path+".pairs");
        for(const auto& point:std::array<std::array<int,2>,8>{{{{1,618}},{{3703,3086}},{{0,1}},{{1000,1060}},
                    {{1800,1861}},{{1900,1960}},{{0,3703}},{{2,4}}}}) {
            const auto delta=joint_delta(point[0],point[1]);
            pairs<<delta.x<<' '<<delta.y<<' '<<delta.raw<<' '<<delta.weighted<<'\n';
        }
        pairs.close(); require(static_cast<bool>(pairs),"pair audit write failed");
        const auto model=block(2,3);
        std::array<vdw::Cost,4096> values{};
        model.all([&](unsigned mask,vdw::Cost cost){ values[mask]=cost; });
        std::ofstream blocks(path+".block.json");
        blocks<<"{\"r\":2,\"s\":3,\"raw\":[";
        for(unsigned mask=0;mask<4096;++mask) {
            if(mask) { blocks<<','; }
            blocks<<static_cast<std::int64_t>(bad.size())+values[mask].raw;
        }
        blocks<<"],\"weighted\":[";
        for(unsigned mask=0;mask<4096;++mask) {
            if(mask) { blocks<<','; }
            blocks<<weighted_cost+values[mask].weighted;
        }
        const auto optimum=minimum(model);
        blocks<<"],\"minimum\":{\"feasible\":"<<(optimum.feasible?"true":"false")
              <<",\"mask\":"<<optimum.mask<<",\"raw\":"<<static_cast<std::int64_t>(bad.size())+optimum.value.raw
              <<",\"weighted\":"<<weighted_cost+optimum.value.weighted<<"}}\n";
        blocks.close(); require(static_cast<bool>(blocks),"block audit write failed");
    }
};

int main(int argc,char** argv) {
    try {
        Search::require(argc==5 || argc==6,"usage: repair3704 CHECKPOINT (STEPS|sweep) SECONDS SEED [START_WORD]");
        const bool sweep=std::string(argv[2])=="sweep";
        const auto steps=sweep?1ULL:std::stoull(argv[2]); const double seconds=std::stod(argv[3]);
        Search::require(steps>0 && steps<=1000000 && seconds>0 && seconds<=55,"invocation limit");
        Search search(std::stoull(argv[4])); search.initialize(argv[1],argc==6?argv[5]:""); search.audit();
        const auto begin=std::chrono::steady_clock::now(); const auto first=search.iteration;
        std::cout<<"initial "<<search.bad.size()<<" best "<<search.best_cost<<'\n'<<std::flush;
        if(sweep) { search.save(argv[1]); search.sweep(seconds,argv[1]); }
        while(!sweep && search.iteration-first<steps && !search.bad.empty()) {
            search.step();
            if(search.iteration%1000==0) search.audit();
            if(search.iteration%100==0 && std::chrono::duration<double>(std::chrono::steady_clock::now()-begin).count()>seconds) break;
        }
        search.audit(); search.save(argv[1]);
        std::cout<<"finished "<<search.iteration<<" current "<<search.bad.size()<<" best "<<search.best_cost
                 <<" weighted "<<search.weighted_cost<<" penalties "<<search.penalties
                 <<" edits "<<search.edits[0]<<' '<<search.edits[1]<<'\n';
        std::cout<<"block_evaluations "<<search.block_evaluations<<" moves";
        for(auto n:search.moves) std::cout<<' '<<n;
        std::cout<<" move_sizes";
        for(auto n:search.move_sizes) std::cout<<' '<<n;
        std::cout<<'\n';
    } catch(const std::exception& e) { std::cerr<<"error: "<<e.what()<<'\n'; return 1; }
}
