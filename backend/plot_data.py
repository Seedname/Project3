import matplotlib.pyplot as plt
import pathlib
import pandas as pd
import math
from statistics import mean, stdev
import scipy

def t_test_matched_pairs(time_difference):
    df = len(time_difference) - 1
    
    sample_mean = mean(time_difference)
    print(f"Mean difference: {sample_mean}")
    
    sample_stdev = stdev(time_difference) / (len(time_difference) ** (1/2))
    print(f"Standard deviation of sampling distribution of differences: {sample_stdev}")
    
    t_statistic = sample_mean / sample_stdev
    print(f"Value of t-statistic: {t_statistic}")
    
    print(f"P-value for statistical test: {1 - scipy.stats.t.cdf(t_statistic, df)}")

def t_test_two_sample(bfs_mean, best_first_mean, bfs_stddev, best_first_stdev, num_samples_bfs, num_samples_best_first):
    df = min(num_samples_bfs - 1, num_samples_best_first - 1)
    
    difference_of_means = bfs_mean - best_first_mean
    print(f"Difference of means: {difference_of_means}")
    
    combined_standard_deviation = (((bfs_stddev ** 2) / num_samples_bfs) + ((best_first_stdev ** 2) / num_samples_best_first)) ** (1/2)
    print(f"Combined sampling distribution standard deviation: {combined_standard_deviation}")
    
    t_statistic = difference_of_means / combined_standard_deviation
    print(f"Value of t-statistic: {t_statistic}")
    
    print(f"P-value for statistical test: {1 - scipy.stats.t.cdf(t_statistic, df)}")
    

def main() -> None:
    best_first_times = []
    bfs_times = []
    
    time_difference = []

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
                    
                time_difference.append(float(time_bfs) - float(time_best_first))

    x = list(range(10_000))
    # for i, length in enumerate(bfs_lens):
    #     if best_first_lens[i] != length:
    #         print(i, best_first_lens[i], length)
    # print(max(bfs_times))
    
    print("---------------------------------")
    t_test_matched_pairs(time_difference)
    
    bfs_mean = mean(bfs_times)
    best_first_mean = mean(best_first_times)
    
    bfs_stdev = mean(bfs_times)
    best_first_stdev = mean(best_first_times)
    
    num_samples_bfs = len(bfs_times)
    num_samples_best_first = len(best_first_times)
    
    print("---------------------------------")
    t_test_two_sample(bfs_mean, best_first_mean, bfs_stdev, best_first_stdev, num_samples_bfs, num_samples_best_first)
    
    print("---------------------------------")
    print(f"Average BFS Time: {bfs_mean}\nAverage Best First Times: {best_first_mean}")


if __name__ == "__main__":
    path = pathlib.Path(__file__).parent
    main()
