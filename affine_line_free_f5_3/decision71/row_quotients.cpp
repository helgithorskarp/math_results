#include <array>
#include <iostream>
#include <set>
#include <string>
#include <vector>
#include "profiles.hpp"

int main(){
    std::array<std::vector<std::array<int,5>>,17> rows;
    for(int a=0;a<=3;++a)for(int b=0;b<=4;++b)for(int c=0;c<=4;++c)
    for(int d=0;d<=4;++d)for(int e=0;e<=4;++e){
        const int n=a+b+c+d+e;if(13<=n && n<=16)rows[n].push_back({a,b,c,d,e});
    }
    for(int kind=0;kind<20;++kind){
        const auto R=PROFILES[PAIRS[kind][0]],C=PROFILES[PAIRS[kind][1]];
        std::array<int,25>w{};std::array<int,5>sums{};std::set<std::string>words;
        auto visit=[&](auto&&self,int at)->void{
            if(at==5){
                int total=0;
                for(int j=0;j<5;++j){w[j]=C[j]-sums[j];if(w[j]<0 || w[j]>3)return;total+=w[j];}
                if(total!=R[0] || w[0]>(R[0]+C[0]+64-N)/5)return;
                for(int a=0;a<5;++a)for(int b=0;b<5;++b){
                    int sum=0;for(int x=0;x<5;++x)sum+=w[5*x+(a*x+b)%5];if(sum>16)return;
                }
                std::string word;for(int x:w)word+=static_cast<char>('0'+x);words.insert(word);return;
            }
            for(const auto&row:rows[R[at]]){
                bool okay=true;for(int j=0;j<5;++j)if(sums[j]+row[j]>C[j])okay=false;
                if(!okay)continue;
                for(int j=0;j<5;++j){w[5*at+j]=row[j];sums[j]+=row[j];}
                self(self,at+1);
                for(int j=0;j<5;++j)sums[j]-=row[j];
            }
        };
        visit(visit,1);
        for(const auto&word:words)std::cout<<kind<<' '<<word<<'\n';
    }
}
