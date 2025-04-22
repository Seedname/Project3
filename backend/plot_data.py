import matplotlib.pyplot as plt
import pathlib
import pandas as pd
import math
from statistics import mean

def main() -> None:
    best_first_times = []
    bfs_times = []

    best_first_lens = []
    bfs_lens = []

    for name in path.joinpath("bench_chunks").glob("results_*"):
        with open(name) as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if not line: continue
                line = line.split(",")
                length = len(line)
                if length > 6:
                    line = [' '.join(line[:length-6])] + line[length-6+1:]
                # print(line)
                name, actor_id, best_first_path_len, time_best_first, bfs_path_len, time_bfs = line
                if int(best_first_path_len) >= 0:
                    if int(best_first_path_len) == 6:
                        print(name)
                    best_first_times.append(float(time_best_first))
                    bfs_times.append(float(time_bfs))

                    best_first_lens.append(float(best_first_path_len))
                    bfs_lens.append(float(bfs_path_len))

    x = list(range(10_000))
    # for i, length in enumerate(bfs_lens):
    #     if best_first_lens[i] != length:
    #         print(i, best_first_lens[i], length)
    # print(max(bfs_times))
    print(f"Average BFS Time: {mean(bfs_times)}\nAverage Best First Times: {mean(best_first_times)}")


if __name__ == "__main__":
    path = pathlib.Path(__file__).parent
    main()
