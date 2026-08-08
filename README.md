\# CognoDB Cloud Benchmark



\## Overview



This project benchmarks CognoDB Cloud against Neo4j, Memgraph, FalkorDB and ArangoDB using the same graph dataset and logical workloads.



The benchmark measures traversal latency, point/indexed lookups, aggregation latency and concurrent mixed read/write performance.



\## Databases



\- CognoDB Cloud

\- Neo4j Community

\- Memgraph

\- FalkorDB

\- ArangoDB



\## Dataset



The same graph dataset was loaded into all five databases.



\- Nodes: 22,470

\- Start nodes sampled randomly for query benchmarks: 100

\- Query iterations: 100 per workload

\- Warm-up: performed before measurement



>- Relationships: 171,002

\- Dataset files:

&#x20; - `datasets/raw/facebook\_large/musae\_facebook\_target.csv`

&#x20; - `datasets/raw/facebook\_large/musae\_facebook\_edges.csv`.



\## Methodology



\- Same client machine was used for all benchmarks.

\- Each read workload used 100 iterations after warm-up.

\- Randomly selected node IDs were used for point and traversal workloads.

\- Reported latency metrics include average, minimum, maximum, p50 and p95.

\- Mixed workload used 10 concurrent clients.

\- Mixed workload used an 80% read / 20% write mix.

\- Mixed workload duration was approximately 30 seconds.

\- Failed runs were corrected and the final reported runs contain zero errors.



\## Query Workloads



\### Point Lookup



Lookup a Page node by its ID.



\### Indexed / Filtered Lookup



Lookup/filter Page nodes using the `page\_type` property.



\### 1-Hop



Traverse one `LINKS\_TO` relationship.



\### 2-Hop



Traverse two `LINKS\_TO` relationships.



\### 3-Hop



Traverse three `LINKS\_TO` relationships.



\### Aggregation



Group/count Page nodes by `page\_type`.



\## Indexed Properties



The benchmark creates/uses an index on:



`Page.page\_type`



Platform-specific index creation is handled by the corresponding benchmark scripts.



\## Indexed Query Results



| Database | Query | Average (ms) | P50 (ms) | P95 (ms) |

|---|---|---:|---:|---:|

| CognoDB | aggregation | 12.285 | 10.198 | 24.089 |

| CognoDB | one\_hop | 7.129 | 6.928 | 8.744 |

| CognoDB | point\_lookup | 8.570 | 8.344 | 11.368 |

| CognoDB | two\_hop | 9.409 | 9.117 | 12.110 |

| CognoDB | three\_hop | 11.550 | 10.579 | 18.774 |

| Neo4j | aggregation | 22.227 | 22.717 | 27.035 |

| Neo4j | one\_hop | 19.992 | 19.398 | 27.404 |

| Neo4j | point\_lookup | 20.553 | 21.332 | 26.555 |

| Neo4j | two\_hop | 19.722 | 20.226 | 26.445 |

| Neo4j | three\_hop | 20.459 | 19.745 | 31.570 |

| Memgraph | aggregation | 11.640 | 11.610 | 12.743 |

| Memgraph | one\_hop | 10.449 | 10.285 | 13.157 |

| Memgraph | point\_lookup | 9.617 | 9.518 | 11.567 |

| Memgraph | two\_hop | 10.470 | 10.323 | 12.930 |

| Memgraph | three\_hop | 9.351 | 8.473 | 12.521 |

| FalkorDB | aggregation | 6.994 | 6.595 | 10.271 |

| FalkorDB | one\_hop | 2.982 | 2.752 | 4.455 |

| FalkorDB | point\_lookup | 3.167 | 2.970 | 4.789 |

| FalkorDB | two\_hop | 3.325 | 3.221 | 4.484 |

| FalkorDB | three\_hop | 3.266 | 3.111 | 4.600 |

| ArangoDB | aggregation | 52.049 | 52.113 | 57.208 |

| ArangoDB | one\_hop | 47.634 | 47.841 | 51.401 |

| ArangoDB | point\_lookup | 56.088 | 55.343 | 62.682 |

| ArangoDB | two\_hop | 47.212 | 47.335 | 52.233 |

| ArangoDB | three\_hop | 56.496 | 48.124 | 87.978 |



\## Mixed Workload Results



Configuration:



\- Clients: 10

\- Duration: \~30 seconds

\- Reads: 80%

\- Writes: 20%

\- Errors: 0 for all final runs



| Database | Throughput (queries/s) | P50 (ms) | P95 (ms) | Errors |

|---|---:|---:|---:|---:|

| FalkorDB | 798.78 | 10.320 | 26.241 | 0 |

| Memgraph | 587.35 | 15.976 | 26.735 | 0 |

| CognoDB | 429.38 | 21.498 | 39.613 | 0 |

| Neo4j | 402.21 | 20.538 | 47.809 | 0 |

| ArangoDB | 183.97 | 50.879 | 68.638 | 0 |



\## Analysis



FalkorDB achieved the highest throughput in the mixed workload and the lowest latency across the indexed query workloads in this benchmark.



CognoDB achieved 429.38 queries/sec in the mixed workload with zero errors. It outperformed Neo4j in mixed-workload throughput while remaining competitive in latency.



The results should not be interpreted as a universal ranking. Database performance depends on workload, deployment configuration, resource allocation, query implementation and network conditions.



\## Reproducibility



Install the required Python dependencies and configure credentials through environment variables.



Secrets and connection credentials must never be committed to the repository.



Benchmark scripts are located in `scripts/`.



Results are written to `results/`.



\## Scripts



Important benchmark scripts include:



\- `run\_neo4j\_indexed.py`

\- `run\_mixed\_cypher.py`

\- `run\_mixed\_falkor.py`

\- `run\_mixed\_arango.py`

\- `run\_benchmark.py`

\- `analyze\_results.py`

\- `analyze\_mixed\_results.py`

\- `plot\_comparison.py`

\- `plot\_mixed\_results.py`



\## Generated Charts



\- `results/database\_average\_latency.png`

\- `results/database\_p50\_latency.png`

\- `results/database\_p95\_latency.png`

\- `results/mixed\_throughput.png`

\- `results/mixed\_p50\_latency.png`

\- `results/mixed\_p95\_latency.png`



\## Caveats



\- Database deployment tiers and resource specifications should be documented explicitly before interpreting the results as a strict apples-to-apples hardware comparison.

\- Network latency can affect managed-cloud results.

\- Query languages and database execution engines differ, although the logical workloads were kept equivalent.

\- Warm-up was performed before measured workloads.

\- The final mixed-workload runs for all five databases completed with zero errors.

\- An earlier ArangoDB mixed-workload run contained benchmark-script errors; the script was corrected and the final ArangoDB result was rerun successfully.

\- Neo4j authentication required local password configuration before benchmarking.



\## Data Loading Performance



Data loading was performed separately for each platform using the corresponding loader scripts in `scripts/`.



\### Dataset



\- Source: Facebook Pages graph dataset used by this benchmark

\- Nodes: 22,470

\- Relationships: 171,002

\- Relationship requirement: exceeds 100,000



\### Loading Metrics



| Database | Node Load Time | Nodes/sec | Relationship Load Time | Relationships/sec | Status |

| -------- | -------------: | --------: | ----------------------: | ----------------: | ------ |

| CognoDB | N/A | N/A | N/A | N/A | Remote connection was interrupted during timing |

| Neo4j | N/A | N/A | N/A | N/A | Fresh loading timing was not captured |

| Memgraph | N/A | N/A | N/A | N/A | Fresh loading timing was not captured |

| FalkorDB | 56.634 s | 396.5 | 1475.471 s | 115.90 | Measured and verified |

| ArangoDB | N/A | N/A | 6.668 s | 25,638.9 | Relationship reload timing completed |



\### FalkorDB Loading Details



FalkorDB loaded 22,470 nodes in 56.634 seconds, corresponding to approximately 396.5 nodes/sec.



The complete 171,002 relationships were subsequently loaded in 1,475.471 seconds, corresponding to 115.90 relationships/sec.



The final database state was verified after loading:



\- Nodes: 22,470

\- Relationships: 171,002



Relationship loading was substantially slower than node loading because each relationship requires matching its source and destination nodes before creating the `LINKS\_TO` relationship.



The relationship timing was measured using a separate batched measurement script:



`scripts/measure\_falkor\_relationship\_load.py`



The existing query and mixed-workload benchmark results were not modified.



\### Loading Measurement Caveats



Only completed and reliable measurements are reported. `N/A` is used where a complete timing measurement was not captured rather than estimating or fabricating values.



The CognoDB loading measurement was interrupted by a remote connection failure. Fresh loading timings for Neo4j and Memgraph were not captured. The ArangoDB relationship reload timing was successfully measured.



These limitations are explicitly documented to keep the benchmark results transparent and reproducible.



\## Resource / Footprint



The benchmark was executed from the same client machine for all database systems.



\- Host environment: Windows with WSL2/Docker used for local database containers.

\- Available CPU observed: 12 cores.

\- Available physical memory observed: approximately 8 GB.

\- Memgraph, FalkorDB and ArangoDB were run as local Docker containers.

\- Neo4j was run locally.

\- CognoDB was accessed as a remote/cloud database.

\- Exact CognoDB cloud resource allocation was not observable from the benchmark client.

\- No explicit Docker CPU or memory limits were imposed on the local database containers.



Because deployment models and resource allocations were not identical, the results should be interpreted as measurements of the tested configurations rather than a universal hardware-normalized comparison.



\## Reproducibility



To reproduce the benchmark:



1\. Clone the repository.

2\. Create and activate a Python virtual environment.

3\. Install the pinned dependencies from `requirements.txt`.

4\. Configure database credentials through environment variables.

5\. Load the dataset using the appropriate loader scripts.

6\. Run the benchmark scripts in `scripts/`.

7\. Run the analysis scripts to generate summary CSV files.

8\. Run the plotting scripts to generate comparison charts.



Secrets and database credentials must not be committed to the repository.



\## Conclusion



Under the measured workloads, FalkorDB showed the strongest overall latency and mixed-workload throughput.



CognoDB achieved 429.38 queries/sec in the final mixed workload with zero errors and outperformed Neo4j's 402.21 queries/sec in mixed-workload throughput.



These results describe the tested benchmark environment and should not be interpreted as a universal ranking of database systems. Performance can vary with workload, deployment configuration, hardware resources, query implementation and network conditions.

