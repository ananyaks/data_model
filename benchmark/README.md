Benchmark
==

The values are average across 10 runs and in second.

Notes:
* For pandas, we do not acount for the time to load/dump data from/to disk. So the input format and output format represent the "in-memory format" only.

|**<br>Tool**|**<br>Queries**|**Input<br>Format**|**Output<br>Format**|**<br>Real**|**<br>User**|**<br>Sys**|
|:----------:|:---------------:|:-----------------:|:------------------:|-----------:|-----------:|----------:|
| `pandas` | `analytics` | dataframe | dataframe | 0.4164 | 0.41069 | 0.00563 |
| `pandas` | `search` | dataframe | rows | 1.15409 | 1.15203 | 0.00147 |
| `pandas` | `search w/ concat` | dataframe | dataframe | 4.55423 | 3.92687 | 0.62559 |
| `pandas` | `discovery` | dataframe | dataframe | 0.0015 | 0.00149 | 0.00001 |

