// Independent parameterization by complete weight rows, not interior deficits.
#include <array>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>
int main() {
    std::vector<std::array<int,5>> rows;
    for(int a=0;a<=3;++a)for(int b=0;b<=4;++b)for(int c=0;c<=4;++c)
    for(int d=0;d<=4;++d)for(int e=0;e<=4;++e)
        if(a+b+c+d+e==16)rows.push_back({a,b,c,d,e});
    std::array<int,25>w{};std::array<int,5>sums{};
    constexpr std::array<int,5> target{6,16,16,16,16};
    std::uint64_t accepted=0;
    auto visit=[&](auto&&self,int at)->void {
        if(at==5) {
            int total=0;
            for(int y=0;y<5;++y) {
                w[y]=target[y]-sums[y];
                if(w[y]<0||w[y]>3)return;
                total+=w[y];
            }
            if(total!=6||w[0]>1)return;
            for(int a=0;a<5;++a)for(int b=0;b<5;++b) {
                int n=0;for(int x=0;x<5;++x)n+=w[5*x+(a*x+b)%5];
                if(n>16)return;
            }
            std::string word;for(int x:w)word+=static_cast<char>('0'+x);
            ++accepted;std::cout<<word<<'\n';return;
        }
        for(const auto& row:rows) {
            bool possible=true;
            for(int y=0;y<5;++y)if(sums[y]+row[y]>target[y])possible=false;
            if(!possible)continue;
            for(int y=0;y<5;++y){w[5*at+y]=row[y];sums[y]+=row[y];}
            self(self,at+1);
            for(int y=0;y<5;++y)sums[y]-=row[y];
        }
    };
    visit(visit,1);
    std::cerr<<"{\"status\":\"ROW_ENUMERATION_COMPLETE\",\"accepted\":"<<accepted<<"}\n";
}
