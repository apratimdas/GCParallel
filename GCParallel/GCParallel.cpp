// GCParallel.cpp : Defines the entry point for the application.
//

#include<fstream>
#include<iostream>
#include<algorithm>
#include<vector>
#include<utility>
#include<chrono>
#include<omp.h>
#include "GCParallel.h"
#include<thread>

using namespace std;
using namespace std::chrono;

// Helper types
using uint = unsigned int;
using int64 = long long;
using intpair = pair<int, int>;

// Custom pair a<b
struct mpair
{
	int a, b;

	mpair() : a(0), b(0) {}
	mpair(int a0, int b0) : a(std::min(a0, b0)), b(std::max(a0, b0)) {}
};

fstream fin;
uint n;	// Number of Nodes
uint m;	// Number of Edges
uint dmax; // Maximum degree in Graph

vector<mpair> edges;
vector<uint> deg;

int **adj; // adj[x] - adjacency list of node x
intpair **inc; // inc[x] - incidence list of node x: (y, edge id)
bool adjacent_list(int x, int y) { return binary_search(adj[x], adj[x] + deg[x], y); }
int *adj_matrix; // compressed adjacency matrix
const int adj_chunk = 8 * sizeof(int);
bool adjacent_matrix(int x, int y) { return adj_matrix[(x*n + y) / adj_chunk] & (1 << ((x*n + y) % adj_chunk)); }
bool(*adjacent)(int, int);

int64 **orbit; // orbit[x][o] - how many times does node x participate in orbit o

int threads;

bool operator<(const mpair &x, const mpair &y) 
{
	if (x.a == y.a) return x.b<y.b;
	else return x.a<y.a;
}
bool operator==(const mpair &x, const mpair &y) 
{
	return x.a == y.a && x.b == y.b;
}

void printorbit3();
void rageTriangleCountSerial();
void rageTriangleCountParallel();
void TriGraphletSerial();
void TriGraphletCountParallel();


int main(int argc, char** argv)
{
	if (argc < 2) 
	{
		std::cerr << "Incorrect number of arguments.\n";
		std::cerr << "Usage: GCParallel [graph - input file] [(opt)threads - number of threads to use]\n";
		return 0;
	}

	fin.open(argv[2], fstream::in);
	if (fin.fail()) 
	{
		cerr << "Failed to open file " << argv[2] << endl;
		return 0;
	}
	fin >> n >> m;
	edges.resize(m);
	deg.resize(n);

	threads = atoi(argv[3]); // Thread count change here (testing)

	for (uint i = 0; i<m; i++) 
	{
		int a, b;
		fin >> a >> b;
		if (!(0 <= a && a<n) || !(0 <= b && b<n)) {
			cerr << "Node ids should be between 0 and n-1." << endl;
			return 0;
		}
		if (a == b) {
			cerr << "Self loops (edge from x to x) are not allowed." << endl;
			return 0;
		}
		deg[a]++; deg[b]++;
		edges[i] = mpair(a, b);
	}
	for (int i = 0; i<n; i++) 
		dmax = max(dmax, deg[i]);

	printf("nodes: %d\n", n);
	printf("edges: %d\n", m);
	printf("max degree: %d\n", dmax);
	fin.close();
	
	// set up adjacency matrix if it's smaller than 100MB
	if ((int64)n*n < 100LL * 1024 * 1024 * 8)
	{
		adjacent = adjacent_matrix;
		adj_matrix = (int*)calloc((n*n) / adj_chunk + 1, sizeof(int));
		for (int i = 0; i<m; i++)
		{
			int a = edges[i].a, b = edges[i].b;
			adj_matrix[(a*n + b) / adj_chunk] |= (1 << ((a*n + b) % adj_chunk));
			adj_matrix[(b*n + a) / adj_chunk] |= (1 << ((b*n + a) % adj_chunk));
		}
	}
	else
		adjacent = adjacent_list;

	// set up adjacency, incidence lists
	adj = (int**)malloc(n * sizeof(int*));
	for (int i = 0; i<n; i++) 
		adj[i] = (int*)malloc(deg[i] * sizeof(int));

	inc = (intpair **)malloc(n * sizeof(intpair*));
	for (int i = 0; i<n; i++) 
		inc[i] = (intpair*)malloc(deg[i] * sizeof(intpair));

	int *d = (int*)calloc(n, sizeof(int));
	for (int i = 0; i<m; i++) 
	{
		int a = edges[i].a, b = edges[i].b;
		adj[a][d[a]] = b; adj[b][d[b]] = a;
		inc[a][d[a]] = intpair(b, i); inc[b][d[b]] = intpair(a, i);
		d[a]++; d[b]++;
	}

	for (int i = 0; i<n; i++) 
	{
		sort(adj[i], adj[i] + deg[i]);
		sort(inc[i], inc[i] + deg[i]);
	}

	// initialize orbit counts
	orbit = (int64**)malloc(n * sizeof(int64*));
	for (int i = 0; i < n; i++)
		orbit[i] = (int64*)calloc(73, sizeof(int64));

	// Begin Algorithm

	rageTriangleCountSerial();

	//printorbit3();

	return 0;
}

void rageParallelBreak(int a, int b)
{
	for (int v = a; v < b; v++)
	{
		for (int i = 0; i < deg[v]; i++)
		{
			int u = adj[v][i];
			if (v < u)
			{
				for (int u_i = 0; u_i < deg[u]; u_i++)
				{
					int w = adj[u][u_i];
					if (adjacent(v, w))
					{
						orbit[v][3]++;
						orbit[u][3]++;
						orbit[w][3]++;
					}
					else
					{
						orbit[v][1]++;
						orbit[u][2]++;
						orbit[w][1]++;
					}
				}
			}
		}
	}
}

void rageTriangleCountSerial()
{
	auto start = high_resolution_clock::now();


//#pragma omp parallel for

	vector<thread> tvec;
	tvec.reserve(threads);
	
	for (int i = 0; i < threads; i++)
	{
		tvec.push_back(thread(rageParallelBreak,(i*n / threads),(int(i*n / threads) + int(n / threads))));
	}
	for (int i = 0; i < threads; i++)
	{
		tvec[i].join();
	}

	auto stop = high_resolution_clock::now();

	duration<float> secs = stop - start;
	//auto secs = duration_cast<duration<float>>(stop - start);

	cout << "Time taken: " << secs.count()<<"\n";
}

void printorbit3()
{
	for (int i = 0; i < n; i++)
		cout << orbit[i][1] << " " << orbit[i][2] << " " << orbit[i][3] << "\n";
}