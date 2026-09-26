// Enumerate weights of a 70-set projected along the intersection of two 6-planes.
// The deficit decomposition adapts Team A researcher 2's decision71 enumerator.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <string>
int main() {
    std::array<int,25> d{};std::array<int,5> rows{},cols{};
    std::uint64_t leaves=0,accepted=0;
    auto visit=[&](auto&& self,int at,int total)->void {
        if(at==16) {
            if(total<5||total>6)return;
            ++leaves;
            for(int i=1;i<5;++i) {
                d[5*i]=4-rows[i];d[i]=4-cols[i];
                if(d[5*i]<1||d[5*i]>4||d[i]<1||d[i]>4)return;
            }
            d[0]=total-2;
            for(int a=0;a<5;++a)for(int b=0;b<5;++b) {
                int sum=0;for(int x=0;x<5;++x)sum+=d[5*x+(a*x+b)%5];
                if(sum<4)return;
            }
            std::string word;for(int x:d)word+=static_cast<char>('0'+4-x);
            ++accepted;std::cout<<word<<'\n';return;
        }
        const int x=at/4+1,y=at%4+1;
        const int cap=std::min({4,3-rows[x],3-cols[y],6-total});
        for(int value=0;value<=cap;++value) {
            d[5*x+y]=value;rows[x]+=value;cols[y]+=value;
            self(self,at+1,total+value);
            rows[x]-=value;cols[y]-=value;
        }
    };
    visit(visit,0,0);
    std::cerr<<"{\"status\":\"TWO_SIX_QUOTIENT_ENUMERATION_COMPLETE\",\"leaves\":"<<leaves<<",\"accepted\":"<<accepted<<"}\n";
}
