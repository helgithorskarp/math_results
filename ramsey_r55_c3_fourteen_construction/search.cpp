// Exact weighted monochromatic-five-set objective; bounded heuristic search.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>
namespace fs = std::filesystem;
constexpr int N = 43, V = 287;
void need(bool b, const std::string& s) { if (!b) throw std::runtime_error(s); }
// Fourteen moving triples 0..41 and one fixed vertex 42.
// IDs 0..272: three phase orbits for each pair of triples;
// IDs 273..286: contacts to vertex 42. Internal colors are fixed.
int var(int a, int b) {
    if (a > b) std::swap(a,b);
    if (b == 42) return 273+a/3;
    int i=a/3,j=b/3;
    if (i==j) return i<7 ? -2 : -1;
    return 3*(i*(27-i)/2+j-i-1)+(b%3-a%3+3)%3;
}
struct Clause {
    std::array<int,10> vars{};
    int n=0, badcolor=0, weight=1;
    bool operator<(const Clause& o) const {
        if (badcolor!=o.badcolor) return badcolor<o.badcolor;
        if (n!=o.n) return n<o.n;
        return vars<o.vars;
    }
};
struct Model {
    std::vector<Clause> clauses;
    std::array<std::vector<int>,V> occur;
    std::uint64_t possible_red=0,possible_blue=0;
    Model() {
        std::vector<Clause> raw;
        for(int a=0;a<N;++a) for(int b=a+1;b<N;++b)
        for(int c=b+1;c<N;++c) for(int d=c+1;d<N;++d)
        for(int e=d+1;e<N;++e) {
            std::array<int,5> q{a,b,c,d,e};
            Clause x; bool red=false,blue=false;
            for(int i=0;i<5;++i) for(int j=i+1;j<5;++j) {
                int v=var(q[i],q[j]);
                if(v==-1) blue=true; else if(v==-2) red=true;
                else x.vars[x.n++]=v;
            }
            if(red && blue) continue;
            // Insertion sort on at most ten entries; avoids GCC12's spurious
            // array-bounds diagnostic in the generic heap-sort fallback.
            for(int i=1;i<x.n;++i) {
                int v=x.vars[i],j=i;
                while(j>0 && x.vars[j-1]>v) {x.vars[j]=x.vars[j-1];--j;}
                x.vars[j]=v;
            }
            x.n=static_cast<int>(std::unique(x.vars.begin(),x.vars.begin()+x.n)-x.vars.begin());
            std::fill(x.vars.begin()+x.n,x.vars.end(),0);
            need(x.n>0,"constant forbidden five-set");
            if(!red) {x.badcolor=0;raw.push_back(x);++possible_blue;}
            if(!blue) {x.badcolor=1;raw.push_back(x);++possible_red;}
        }
        std::sort(raw.begin(),raw.end());
        for(const auto& x:raw) {
            if(!clauses.empty() && !(clauses.back()<x) && !(x<clauses.back())) ++clauses.back().weight;
            else clauses.push_back(x);
        }
        for(int i=0;i<static_cast<int>(clauses.size());++i)
            for(int j=0;j<clauses[i].n;++j) occur[clauses[i].vars[j]].push_back(i);
    }
};
// Fully specified generator: SplitMix64, unsigned arithmetic modulo 2^64.
struct Random {
    std::uint64_t state;
    std::uint64_t next() {
        std::uint64_t z=(state+=UINT64_C(0x9e3779b97f4a7c15));
        z=(z^(z>>30))*UINT64_C(0xbf58476d1ce4e5b9);
        z=(z^(z>>27))*UINT64_C(0x94d049bb133111eb);
        return z^(z>>31);
    }
    int pick(int n) {need(n>0,"empty sample");return static_cast<int>(next()%static_cast<unsigned>(n));}
};
struct State {
    const Model& m;
    std::array<int,V> bits{},make{},brk{};
    std::vector<int> sat,xors,bad,pos;
    int score=0;
    explicit State(const Model& model, const std::array<int,V>& x):m(model),bits(x),
        sat(m.clauses.size()),xors(m.clauses.size()),pos(m.clauses.size(),-1) {
        for(int i=0;i<static_cast<int>(m.clauses.size());++i) {
            const auto& c=m.clauses[i];
            for(int j=0;j<c.n;++j) if(bits[c.vars[j]]!=c.badcolor) {++sat[i];xors[i]^=c.vars[j];}
            add(i);
        }
    }
    void add(int i) {
        const auto& c=m.clauses[i];
        if(sat[i]==0) {
            score+=c.weight;pos[i]=static_cast<int>(bad.size());bad.push_back(i);
            for(int j=0;j<c.n;++j) make[c.vars[j]]+=c.weight;
        } else if(sat[i]==1) brk[xors[i]]+=c.weight;
    }
    void remove(int i) {
        const auto& c=m.clauses[i];
        if(sat[i]==0) {
            score-=c.weight;
            int j=pos[i],last=bad.back();bad[j]=last;pos[last]=j;bad.pop_back();pos[i]=-1;
            for(int k=0;k<c.n;++k) make[c.vars[k]]-=c.weight;
        } else if(sat[i]==1) brk[xors[i]]-=c.weight;
    }
    void flip(int v) {
        for(int i:m.occur[v]) {
            if(sat[i]<=1) remove(i);
            sat[i]+=bits[v]==m.clauses[i].badcolor ? 1 : -1;
            xors[i]^=v;
            if(sat[i]<=1) add(i);
        }
        bits[v]^=1;
    }
    void check() const {
        State other(m,bits);
        need(score==other.score && make==other.make && brk==other.brk && sat==other.sat && xors==other.xors,"incremental objective drift");
        auto a=bad,b=other.bad;std::sort(a.begin(),a.end());std::sort(b.begin(),b.end());need(a==b,"bad list drift");
        for(int i=0;i<static_cast<int>(bad.size());++i) need(pos[bad[i]]==i,"position drift");
    }
};
std::string word(const std::array<int,V>& x) {std::string s;for(int v:x)s+=static_cast<char>('0'+v);return s;}
void save(const fs::path& p,const std::string& s) {
    fs::path t=p.string()+".tmp";std::ofstream f(t);need(static_cast<bool>(f),"output");f<<s;f.close();need(static_cast<bool>(f),"output close");fs::rename(t,p);
}
void edges(const fs::path& p,const std::array<int,V>& x) {
    std::string s="43\n";
    for(int a=0;a<N;++a) for(int b=a+1;b<N;++b) {int v=var(a,b);if(v==-2 || (v>=0 && x[v]))s+=std::to_string(a)+" "+std::to_string(b)+"\n";}
    save(p,s);
}
int main(int argc,char** argv) {
  try {
    need(argc==6,"usage: search OUT RESTARTS STEPS SEED CHECK_INTERVAL");
    fs::path out=argv[1];
    int restarts=std::stoi(argv[2]),steps=std::stoi(argv[3]);
    auto seed=std::stoull(argv[4]);int interval=std::stoi(argv[5]);
    need(restarts>0 && restarts<=1000 && steps>0 && steps<=10000000 && interval>=0,"limits");
    need(!fs::exists(out),"fresh output required");fs::create_directories(out);
    auto start=std::chrono::steady_clock::now();Model model;
    std::string modeltext="{\"variables\":287,\"clauses\":"+std::to_string(model.clauses.size())+",\"possible_red\":"+std::to_string(model.possible_red)+",\"possible_blue\":"+std::to_string(model.possible_blue)+"}\n";
    save(out/"model.json",modeltext);std::cout<<modeltext<<std::flush;
    std::array<bool,V> frozen{};std::vector<int> free;
    for(int v=0;v<V;++v) free.push_back(v);
    need(free.size()==287,"free variable count");
    std::string records="restart\tseed\tinitial\tbest\tbest_step\tsteps_done\tbits\n";
    int jobs=0;
    {
        int corebest=std::numeric_limits<int>::max();
        for(int r=0;r<restarts;++r) {
            if(fs::exists(out/"STOP")) {save(out/"status.json","{\"complete\":false,\"stopped\":true}\n");return 0;}
            std::uint64_t rs=seed+static_cast<unsigned>(r);
            Random rng{rs};std::array<int,V> bits{};
            for(int& b:bits)b=rng.pick(2);
            State state(model,bits);int initial=state.score,best=initial,beststep=0,done=0;
            auto bestbits=bits;std::array<int,V> last{};last.fill(-100);
            for(int step=1;step<=steps && state.score>0;++step) {
                int chosen=-1;
                if(rng.pick(100)==0) chosen=free[rng.pick(static_cast<int>(free.size()))];
                else {
                    int delta=std::numeric_limits<int>::max();std::vector<int> tie;
                    for(int v:free) {
                        int d=state.brk[v]-state.make[v];
                        if(step-last[v]<=7 && state.score+d>=best)continue;
                        if(d<delta){delta=d;tie.clear();}if(d==delta)tie.push_back(v);
                    }
                    need(!tie.empty(),"no eligible move");
                    chosen=tie[rng.pick(static_cast<int>(tie.size()))];
                    if(delta>=0 && rng.pick(100)<20) {
                        const auto& c=model.clauses[state.bad[rng.pick(static_cast<int>(state.bad.size()))]];
                        std::vector<int> cand;
                        for(int j=0;j<c.n;++j)if(!frozen[c.vars[j]])cand.push_back(c.vars[j]);
                        need(!cand.empty(),"bad fixed-only clause");
                        chosen=cand[rng.pick(static_cast<int>(cand.size()))];
                    }
                }
                int expected=state.score+state.brk[chosen]-state.make[chosen];
                state.flip(chosen);last[chosen]=step;done=step;need(state.score==expected,"gain drift");
                if(interval && step%interval==0)state.check();
                if(state.score<best) {best=state.score;bestbits=state.bits;beststep=step;}
            }
            state.check();State beststate(model,bestbits);need(beststate.score==best,"best score");
            records+=std::to_string(r)+"\t"+std::to_string(rs)+"\t"+std::to_string(initial)+"\t"+std::to_string(best)+"\t"+std::to_string(beststep)+"\t"+std::to_string(done)+"\t"+word(bestbits)+"\n";
            save(out/"restarts.tsv",records);++jobs;
            if(best<corebest) {corebest=best;edges(out/"best.edges",bestbits);}
            std::cout<<"restart "<<r<<" initial "<<initial<<" best "<<best<<" step "<<beststep<<"\n"<<std::flush;
            if(best==0) {save(out/"status.json","{\"complete\":false,\"candidate_target\":true}\n");return 0;}
        }
    }
    double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
    save(out/"status.json","{\"complete\":true,\"candidate_target\":false,\"jobs\":"+std::to_string(jobs)+",\"seconds\":"+std::to_string(sec)+"}\n");
    return 0;
  } catch(const std::exception& e) {std::cerr<<e.what()<<"\n";return 1;}
}
