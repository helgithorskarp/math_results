#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <functional>
#include <iostream>
#include <utility>
#include <vector>
using namespace std;
using Mask = uint32_t;
constexpr int INF = 1000;

int m, n;
vector<pair<int,int>> edges;
using Graph = vector<vector<pair<int,int>>>;

void add(Graph& g, int u, int v, int w) {
    g[u].push_back({v,w}); g[v].push_back({u,w});
}
Graph make_graph(Mask mask, int x, int y, int z) {
    Graph g(n);
    for (int i=0;i<m+1;i++) if (mask&(Mask(1)<<i)) add(g,edges[i].first,edges[i].second,1);
    if (x<INF) add(g,1,3,x);
    if (y<INF) add(g,1,5,y);
    if (z<INF) add(g,3,5,z);
    return g;
}
vector<Mask> large_components(Mask mask) {
    auto g=make_graph(mask,INF,INF,INF);
    Mask remaining=(Mask(1)<<n)-1;
    vector<Mask> answer;
    while (remaining) {
        int u=__builtin_ctz(remaining);
        Mask part=0;
        vector<int> todo{u};
        remaining &= ~(Mask(1)<<u);
        while (!todo.empty()) {
            u=todo.back(); todo.pop_back(); part|=Mask(1)<<u;
            for (auto [v,w]:g[u]) {
                (void)w;
                if (remaining&(Mask(1)<<v)) { remaining &= ~(Mask(1)<<v); todo.push_back(v); }
            }
        }
        if (__builtin_popcount(part)>=6) answer.push_back(part);
    }
    return answer;
}
bool coverable(const Graph& g, Mask target) {
    int dist[20][20];
    for (int i=0;i<n;i++) {
        for (int j=0;j<n;j++) dist[i][j]=i==j?0:INF;
        for (auto [j,w]:g[i]) dist[i][j]=min(dist[i][j],w);
    }
    for (int k=0;k<n;k++) for (int i=0;i<n;i++) for (int j=0;j<n;j++)
        dist[i][j]=min(dist[i][j],dist[i][k]+dist[k][j]);
    vector<unsigned char> seen(Mask(1)<<n,0);
    vector<Mask> traces;
    for (int s=0;s<n;s++) if (target&(Mask(1)<<s)) {
        function<void(int,Mask)> visit=[&](int u, Mask mask) {
            if (target&(Mask(1)<<u)) {
                Mask trace=mask&target;
                if (!seen[trace]) {seen[trace]=1;traces.push_back(trace);}
            }
            for (auto [v,w]:g[u]) if (dist[s][u]+w==dist[s][v]) visit(v,mask|(Mask(1)<<v));
        };
        visit(s,Mask(1)<<s);
    }
    for (Mask a:traces) for (Mask b:traces) if ((a|b)==target) return true;
    return false;
}
int main(int argc,char**argv) {
    if (argc!=2) return 3;
    m=atoi(argv[1]); n=m+1;
    if (m<8||m>17) return 4;
    for (int i=0;i<m;i++) edges.push_back({i,(i+1)%m});
    edges.push_back({0,m});
    vector<vector<Mask>> targets(Mask(1)<<(m+1));
    int relevant=0;
    for (Mask f=0;f<targets.size();f++) {
        targets[f]=large_components(f);
        relevant+=!targets[f].empty();
    }
    uint64_t profiles=0,states=0;
    int xlow=max(2,m-8),ylow=max(2,m-8),zlow=max(2,m-10),cross=max(2,m-6);
    for (int x=xlow;x<=m+1;x++) for (int y=ylow;y<=m+1;y++)
        for (int z=zlow;z<=m+1;z++) {
            if (max(x,y)<cross) continue;
            profiles++;
            int xx=x==m+1?INF:x, yy=y==m+1?INF:y, zz=z==m+1?INF:z;
            for (Mask f=0;f<targets.size();f++) {
                if (targets[f].empty()) continue;
                auto g=make_graph(f,xx,yy,zz);
                for (Mask target:targets[f]) {
                    if (!coverable(g,target)) {
                        cerr<<"FAIL m="<<m<<" x="<<x<<" y="<<y<<" z="<<z<<" mask="<<f<<" target="<<target<<'\n';
                        return 1;
                    }
                    states++;
                }
            }
        }
    cout<<"m="<<m<<" relevant="<<relevant<<" profiles="<<profiles<<" states="<<states<<" PASS\n";
}
