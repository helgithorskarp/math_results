// Enumerate fixed-size planar sets by backtracking with line-occupancy pruning.
#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <set>
#include <vector>

int main(){
    std::set<std::array<int,5>> lines;
    for(int p=0;p<25;++p)for(int q=p+1;q<25;++q){
        std::array<int,5> line{};
        for(int t=0;t<5;++t){
            const int x=(p/5+t*(q/5-p/5)+100)%5;
            const int y=(p%5+t*(q%5-p%5)+100)%5;
            line[t]=5*x+y;
        }
        // Small independent sorting network via insertion sort.
        for(int i=1;i<5;++i)for(int j=i;j>0 && line[j]<line[j-1];--j){int a=line[j];line[j]=line[j-1];line[j-1]=a;}
        lines.insert(line);
    }
    if(lines.size()!=30)return 2;
    std::array<std::vector<int>,25> incident;
    int index=0;for(const auto&line:lines){for(int p:line)incident[p].push_back(index);++index;}
    for(const auto&v:incident)if(v.size()!=6)return 3;
    std::map<std::array<int,6>,uint64_t> spectra;
    for(int target=7;target<=17;++target){
        std::array<int,30> counts{};
        const int cap=target<=10?3:4;
        auto visit=[&](auto&&self,int first,int selected)->void{
            if(selected==target){
                std::array<int,6>s{};s[0]=target;
                for(int k:counts)++s[k+1];
                ++spectra[s];return;
            }
            for(int point=first;point<=25-(target-selected);++point){
                bool okay=true;for(int line:incident[point])if(counts[line]==cap)okay=false;
                if(!okay)continue;
                for(int line:incident[point])++counts[line];
                self(self,point+1,selected+1);
                for(int line:incident[point])--counts[line];
            }
        };
        visit(visit,0,0);
    }
    for(const auto&[s,count]:spectra){
        if(s[0]==17)return 4;
        for(int x:s)std::cout<<x<<' ';
        std::cout<<count<<'\n';
    }
}
