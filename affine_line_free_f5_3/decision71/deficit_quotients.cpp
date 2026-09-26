#include <algorithm>
#include <array>
#include <chrono>
#include <iostream>
#include <set>
#include <string>
#include "profiles.hpp"

int main(int argc,char**argv) {
    const int start=argc>1?std::stoi(argv[1]):0,stop=argc>2?std::stoi(argv[2]):20;
    if(start<0 || start>=stop || stop>20)return 2;
    for(int type=start;type<stop;++type) {
        auto begun=std::chrono::steady_clock::now();
        const auto profileR=PROFILES[PAIRS[type][0]],profileC=PROFILES[PAIRS[type][1]];
        std::array<int,5> R{},C{};
        for(int i=0;i<5;++i){R[i]=20-profileR[i];C[i]=20-profileC[i];}
        const int cap=(profileR[0]+profileC[0]+64-N)/5;
        const int low=100-N-R[0]-C[0]+4-cap,high=100-N-R[0]-C[0]+4;
        std::array<int,25>d{};std::array<int,5> rows{},cols{};
        std::set<std::string> words;
        auto visit=[&](auto&&self,int at,int total)->void {
            if(at==16) {
                if(total<low || total>high)return;
                for(int i=1;i<5;++i){
                    d[5*i]=R[i]-rows[i];d[i]=C[i]-cols[i];
                    if(d[5*i]<1 || d[5*i]>4 || d[i]<1 || d[i]>4)return;
                }
                d[0]=R[0]+C[0]-(100-N)+total;
                for(int a=0;a<5;++a)for(int b=0;b<5;++b){
                    int sum=0;for(int x=0;x<5;++x)sum+=d[5*x+(a*x+b)%5];
                    if(sum<4)return;
                }
                std::string word;for(int x:d)word+=static_cast<char>('0'+4-x);
                words.insert(word);return;
            }
            const int x=at/4+1,y=at%4+1;
            const int maximum=std::min({4,R[x]-1-rows[x],C[y]-1-cols[y],high-total});
            for(int value=0;value<=maximum;++value){
                d[5*x+y]=value;rows[x]+=value;cols[y]+=value;
                self(self,at+1,total+value);
                rows[x]-=value;cols[y]-=value;
            }
        };
        visit(visit,0,0);
        for(const auto&word:words)std::cout<<type<<' '<<word<<'\n';
        std::cerr<<type<<' '<<words.size()<<' '<<std::chrono::duration<double>(std::chrono::steady_clock::now()-begun).count()<<'\n';
    }
}
