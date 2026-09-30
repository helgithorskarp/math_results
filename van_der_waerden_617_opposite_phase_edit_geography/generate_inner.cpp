// Direct disjoint monochromatic AP packing inside the 1130-point seam region.
// This generates positive certificates only; the final checker is independent.
#include <array>
#include <chrono>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>
namespace {
constexpr int P=617,N=3704,C=1852,H=565,LO=C-H,HI=C+H;
int residue(int x) {x%=P;return x<0?x+P:x;}
void demand(bool b,const char* message) {if(!b)throw std::runtime_error(message);}
}
int main(int argc,char** argv) {
    try {
        demand(argc==2,"usage: generate_inner OUTPUT.json");
        const std::filesystem::path output(argv[1]),partial(output.string()+".partial");
        demand(!std::filesystem::exists(output)&&!std::filesystem::exists(partial),"refusing to overwrite output");
        const auto start=std::chrono::steady_clock::now();
        std::array<int,P> q;q.fill(1);q[0]=-1;for(int x=1;x<P;++x)q[x*x%P]=0;
        std::ofstream out(partial);demand(static_cast<bool>(out),"output open");
        out<<"{\"format\":\"QR617_OPPOSITE_PHASE_INNER_PACKING_V1\",\"region\":["<<LO<<','<<HI<<"],\"records\":[";
        int minimum=H,maximum=0;
        for(int s=0;s<P;++s) {
            std::array<int,N> word;word.fill(-1);std::array<bool,N> used{};
            for(int x=LO;x<HI;++x) {
                const int b=q[residue(x-C+s)];if(b>=0)word[x]=b^(x>=C?1:0);
            }
            std::vector<std::array<int,2>> aps;
            for(int d=1;6*d<2*H;++d)for(int a=LO;a+6*d<HI;++a) {
                const int b=word[a];if(b<0||used[a])continue;bool valid=true;
                for(int j=1;j<7;++j)if(used[a+j*d]||word[a+j*d]!=b) {valid=false;break;}
                if(!valid)continue;
                aps.push_back({a,d});for(int j=0;j<7;++j)used[a+j*d]=true;
            }
            minimum=std::min(minimum,static_cast<int>(aps.size()));maximum=std::max(maximum,static_cast<int>(aps.size()));
            if(s)out<<',';
            out<<"{\"key\":["<<s<<','<<s<<",1],\"aps\":[";
            for(std::size_t i=0;i<aps.size();++i) {if(i)out<<',';out<<'['<<aps[i][0]<<','<<aps[i][1]<<']';}
            out<<"]}";
        }
        out<<"]}\n";out.close();demand(static_cast<bool>(out),"incomplete output");
        std::filesystem::rename(partial,output);
        const double elapsed=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
        std::cout<<"{\"status\":\"GENERATED_REQUIRES_INDEPENDENT_CHECK\",\"phase_values\":"<<P
                 <<",\"minimum_greedy_inner_APs\":"<<minimum<<",\"maximum_greedy_inner_APs\":"<<maximum
                 <<",\"seconds\":"<<elapsed<<"}\n";
        return 0;
    } catch(const std::exception& e) {std::cerr<<"generation failed: "<<e.what()<<'\n';return 1;}
}
