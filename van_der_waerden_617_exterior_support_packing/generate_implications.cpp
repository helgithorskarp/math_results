// Bounded deterministic AP implication search with shared exact geometry.
// This is a generator, not a checker. A consistent closure implies no
// extendibility, optimum edit count, or unrestricted coloring exclusion.
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

namespace {
constexpr int P=617,N=3704,C=1852,H=565,LO=C-H,HI=C+H;
struct AP {std::uint16_t a,d;};
struct Step {int x,color;std::uint32_t ap;};
struct Input {int s,t,g;std::vector<int> erased;};
void demand(bool b,const char* m) {if(!b)throw std::runtime_error(m);}
int residue(int x) {x%=P;return x<0?x+P:x;}
void write_ap(std::ostream& out,const AP& ap) {out<<'['<<ap.a<<','<<ap.d<<']';}
}

int main(int argc,char**argv) {
 try {
    demand(argc==5,"usage: residual_unit_generate INPUT.txt OUTPUT_DIR SECONDS MAX_CASES(0=all)");
    std::size_t used=0;const double limit=std::stod(argv[3],&used);
    demand(used==std::string(argv[3]).size()&&limit>0&&limit<=90,"budget must be in (0,90]");
    used=0;const int maximum=std::stoi(argv[4],&used);
    demand(used==std::string(argv[4]).size()&&maximum>=0,"max cases must be nonnegative");
    const std::filesystem::path dir(argv[2]);std::filesystem::create_directories(dir);
    const auto start=std::chrono::steady_clock::now();
    const auto seconds=[&]{return std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();};
    std::ifstream input(argv[1]);demand(static_cast<bool>(input),"input open");
    std::vector<Input> cases;Input row;int count;
    while(input>>row.s>>row.t>>row.g>>count) {
        demand(0<=row.s&&row.s<P&&0<=row.t&&row.t<P&&(row.g==0||row.g==1)&&(row.s!=row.t||row.g),"phase key");
        demand(0<count&&count<=22,"erasure count");row.erased.clear();
        for(int j=0;j<count;++j) {int x;demand(static_cast<bool>(input>>x),"truncated erasure list");row.erased.push_back(x);}
        cases.push_back(row);
    }
    demand(input.eof(),"malformed input");
    std::array<int,P> q;q.fill(1);q[0]=-1;for(int x=1;x<P;++x)q[x*x%P]=0;
    std::vector<AP> aps;aps.reserve(1141450);
    std::vector<std::uint32_t> offsets(N+1,0);
    for(int d=1;6*d<N;++d)for(int a=0;a+6*d<N;++a) {
        aps.push_back({static_cast<std::uint16_t>(a),static_cast<std::uint16_t>(d)});
        for(int j=0;j<7;++j)++offsets[static_cast<std::size_t>(a+j*d+1)];
    }
    demand(aps.size()==1141450,"AP geometry count");
    for(int x=1;x<=N;++x)offsets[x]+=offsets[x-1];
    demand(offsets[N]==7*aps.size(),"incidence coverage");
    std::vector<std::uint32_t> incidence(offsets[N],0),cursor=offsets;
    for(std::size_t id=0;id<aps.size();++id) {
        const auto& ap=aps[id];
        for(int j=0;j<7;++j)incidence[cursor[ap.a+j*ap.d]++]=static_cast<std::uint32_t>(id);
    }
    std::uint32_t processed=0,resumed=0,refuted=0,unrefuted=0;
    std::vector<std::array<int,3>> not_refuted;
    const double geometry_seconds=seconds();
    for(const auto& key:cases) {
        const auto path=dir/("proof-565-"+std::to_string(key.s)+"-"+std::to_string(key.t)+"-"+std::to_string(key.g)+".json");
        if(std::filesystem::exists(path)) {++resumed;continue;}
        if(seconds()>=limit||(maximum>0&&processed>=static_cast<std::uint32_t>(maximum)))break;
        std::array<int,N> word;word.fill(-1);
        for(int x=0;x<N;++x)if(x<LO||x>=HI) {
            const int b=q[residue(x-C+(x<LO?key.s:key.t))];
            if(b>=0)word[x]=b^(x<LO?0:key.g);
        }
        std::array<bool,N> was_erased{};
        for(int x:key.erased) {
            demand(0<=x&&x<N&&word[x]>=0&&!was_erased[x],"erasure must be distinct protected nonpole");
            was_erased[x]=true;word[x]=-1;
        }
        // Low three bits count color0; next three count color1. Bit7 marks
        // permanently mixed APs. Counts never exceed7 and indices fit u32.
        std::vector<std::uint8_t> state(aps.size(),0);
        std::vector<std::uint32_t> queue;queue.reserve(4096);
        std::uint32_t conflict=std::numeric_limits<std::uint32_t>::max();
        const auto none=conflict;
        for(std::size_t id=0;id<aps.size();++id) {
            const auto& ap=aps[id];int n0=0,n1=0;
            for(int j=0;j<7;++j) {
                const int b=word[ap.a+j*ap.d];n0+=b==0;n1+=b==1;
                if(n0&&n1)break;
            }
            if(n0&&n1) {state[id]=128;continue;}
            state[id]=static_cast<std::uint8_t>(n0|(n1<<3));
            if(n0==7||n1==7) {conflict=static_cast<std::uint32_t>(id);break;}
            if(n0==6||n1==6)queue.push_back(static_cast<std::uint32_t>(id));
        }
        std::vector<Step> steps;
        for(std::size_t head=0;head<queue.size()&&conflict==none;++head) {
            const auto id=queue[head];const auto st=state[id];
            if(st&128)continue;
            const int n0=st&7,n1=(st>>3)&7;
            demand((n0==6&&n1==0)||(n1==6&&n0==0),"invalid unit state");
            const int b=n0==6?0:1,value=1-b;const auto& ap=aps[id];int x=-1;
            for(int j=0;j<7;++j) {
                const int y=ap.a+j*ap.d;
                if(word[y]<0) {demand(x<0,"multiple uncolored unit points");x=y;}
                else demand(word[y]==b,"unit premise mismatch");
            }
            demand(x>=0,"missing uncolored unit point");word[x]=value;steps.push_back({x,value,id});
            for(std::uint32_t ix=offsets[x];ix<offsets[x+1];++ix) {
                const auto other=incidence[ix];auto& state2=state[other];if(state2&128)continue;
                const int count0=state2&7,count1=(state2>>3)&7;
                if((value==0&&count1>0)||(value==1&&count0>0)) {state2=128;continue;}
                state2=static_cast<std::uint8_t>(state2+(value==0?1:8));
                const int updated=(state2>>(3*value))&7;
                if(updated==7) {conflict=other;break;}
                if(updated==6)queue.push_back(other);
            }
        }
        const auto partial=std::filesystem::path(path.string()+".partial");
        demand(!std::filesystem::exists(partial),"refusing to overwrite partial proof");
        std::ofstream out(partial);demand(static_cast<bool>(out),"proof output open");
        out<<"{\"key\":["<<key.s<<','<<key.t<<','<<key.g<<"],\"erased_positions\":[";
        for(std::size_t j=0;j<key.erased.size();++j) {if(j)out<<',';out<<key.erased[j];}
        out<<"],\"status\":\""<<(conflict!=none?"UNIT_CONTRADICTION_CERTIFICATE":"NOT_REFUTED_BY_UNIT_PROPAGATION")<<"\",\"steps\":[";
        if(conflict!=none) {
            std::array<bool,N> needed{};const auto& final=aps[conflict];
            for(int j=0;j<7;++j)needed[final.a+j*final.d]=true;
            std::vector<Step> kept;
            for(auto it=steps.rbegin();it!=steps.rend();++it)if(needed[it->x]) {
                kept.push_back(*it);const auto& ap=aps[it->ap];for(int j=0;j<7;++j)needed[ap.a+j*ap.d]=true;
            }
            std::reverse(kept.begin(),kept.end());
            for(std::size_t j=0;j<kept.size();++j) {
                if(j)out<<',';
                const auto& step=kept[j];const auto& ap=aps[step.ap];
                out<<'['<<step.x<<','<<step.color<<','<<ap.a<<','<<ap.d<<']';
            }
            out<<"],\"final_ap\":";write_ap(out,final);++refuted;
        } else {out<<"],\"final_ap\":null";++unrefuted;not_refuted.push_back({key.s,key.t,key.g});}
        out<<",\"unpruned_forced_steps\":"<<steps.size()<<"}\n";out.close();demand(static_cast<bool>(out),"proof write failed");
        std::filesystem::rename(partial,path);++processed;
    }
    std::cout<<"{\"status\":\"BOUNDED_GENERATION_REQUIRES_INDEPENDENT_CHECK\",\"input_cases\":"<<cases.size()
             <<",\"processed\":"<<processed<<",\"resumed\":"<<resumed<<",\"refuted\":"<<refuted<<",\"not_refuted\":"<<unrefuted
             <<",\"pending\":"<<cases.size()-processed-resumed<<",\"interval_AP_geometry\":"<<aps.size()<<",\"incidences\":"<<incidence.size()
             <<",\"geometry_seconds\":"<<geometry_seconds<<",\"seconds\":"<<seconds()<<",\"not_refuted_keys\":[";
    for(std::size_t j=0;j<not_refuted.size();++j) {if(j)std::cout<<',';const auto& k=not_refuted[j];std::cout<<'['<<k[0]<<','<<k[1]<<','<<k[2]<<']';}
    std::cout<<"]}\n";return 0;
 } catch(const std::exception& e) {std::cerr<<"generation failed: "<<e.what()<<'\n';return 1;}
}
