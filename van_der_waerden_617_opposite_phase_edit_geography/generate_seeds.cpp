// Direct per-phase opposed-AP generator. No phase rectangles or old transcript.
// Generated records require exact checking; a missing second pair is UNKNOWN.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdlib>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>

namespace {
constexpr int P=617,N=3704,C=1852,H=565,LO=C-H,HI=C+H;
using Record=std::array<int,3>;
int residue(int x) {x%=P;return x<0?x+P:x;}
void demand(bool ok,const char* message) {if(!ok)throw std::runtime_error(message);}
Record find_pair(int s,const std::array<int,P>& q,const std::vector<int>& centers,
                 const std::array<bool,N>& erased) {
    for(int v:centers) {
        std::array<int,2> known{};
        const int first=std::max({1,v-LO+1,HI-v});
        const int last=std::min(v/3,(N-1-v)/3);
        for(int d=first;d<=last;++d) {
            const int b=q[residue(v-d-C+s)];
            if(b<0||known[b])continue;
            bool valid=true;
            for(int j:{-3,-2,-1,1,2,3}) {
                const int x=v+j*d;
                const int raw=q[residue(x-C+s)];
                if(erased[x]||raw<0||(raw^(j>0?1:0))!=b) {valid=false;break;}
            }
            if(!valid)continue;
            known[b]=d;
            if(known[1-b])return {v,known[0],known[1]};
        }
    }
    return {};
}
void write_record(std::ostream& out,const Record& r) {
    if(r==Record{})out<<"null";
    else out<<'['<<r[0]<<','<<r[1]<<','<<r[2]<<']';
}
}

int main(int argc,char** argv) {
    try {
        demand(argc==2,"usage: generate_equal_phase_seeds OUTPUT.json");
        const std::filesystem::path output(argv[1]),partial(output.string()+".partial");
        demand(!std::filesystem::exists(output)&&!std::filesystem::exists(partial),"refusing to overwrite output");
        const auto start=std::chrono::steady_clock::now();
        std::array<int,P> q;q.fill(1);q[0]=-1;
        for(int x=1;x<P;++x)q[x*x%P]=0;
        std::vector<int> centers;
        const int first=std::max(LO,(3*HI+3)/4);
        const int last=std::min(HI-1,(N-1+3*(LO-1))/4);
        for(int v=first;v<=last;++v)centers.push_back(v);
        std::sort(centers.begin(),centers.end(),[](int a,int b) {
            const int da=std::abs(2*a-(N-1)),db=std::abs(2*b-(N-1));
            return da!=db?da<db:a<b;
        });
        std::ofstream out(partial);demand(static_cast<bool>(out),"output open");
        out<<"{\"format\":\"QR617_EQUAL_PHASE_SEEDS_V1\",\"length\":"<<N
           <<",\"half_width\":"<<H<<",\"records\":[";
        int first_count=0,second_count=0;
        for(int s=0;s<P;++s) {
            std::array<bool,N> erased{};
            const auto a=find_pair(s,q,centers,erased);
            demand(a!=Record{},"first opposed pair missing");++first_count;
            for(int b=0;b<2;++b)for(int j:{-3,-2,-1,1,2,3})erased[a[0]+j*a[1+b]]=true;
            const auto b=find_pair(s,q,centers,erased);second_count+=b!=Record{};
            if(s)out<<',';
            out<<"{\"key\":["<<s<<','<<s<<",1],\"first\":";
            write_record(out,a);out<<",\"second\":";write_record(out,b);out<<'}';
        }
        out<<"]}\n";out.close();demand(static_cast<bool>(out),"incomplete output write");
        std::filesystem::rename(partial,output);
        const double elapsed=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
        std::cout<<"{\"status\":\"GENERATED_REQUIRES_INDEPENDENT_CHECK\",\"phase_values\":"<<P
                 <<",\"first_opposed_pairs\":"<<first_count<<",\"second_opposed_pairs\":"<<second_count
                 <<",\"second_pair_holes\":"<<P-second_count<<",\"seconds\":"<<elapsed<<"}\n";
        return 0;
    } catch(const std::exception& e) {
        std::cerr<<"generation failed: "<<e.what()<<'\n';return 1;
    }
}
