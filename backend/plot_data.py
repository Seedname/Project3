import matplotlib.pyplot as plt
import pathlib
import pandas as pd
import math
from statistics import mean, stdev
import scipy
from collections import defaultdict

# function to perform a matched-pairs t-test
def t_test_matched_pairs(time_difference):
    print("Matched-pairs t-test:\n")
    print("Null hypothesis: The best first search algorithm is equally as fast as the breadth first search algorithm.")
    print("Alpha value (Level of significance): 0.01")
    
    # compute this test's degrees of freedom
    df = len(time_difference) - 1
    
    # compute this test's mean
    sample_mean = mean(time_difference)
    print(f"Mean difference: {sample_mean}")
    
    # compute this test's standard deviation for the sampling distribution, which is the standard deviation divided by the square root of the number of samples.
    sample_stdev = stdev(time_difference) / (len(time_difference) ** (1/2))
    print(f"Standard deviation of sampling distribution of differences: {sample_stdev}")
    
    # compute this test's t-statistic
    t_statistic = sample_mean / sample_stdev
    print(f"Value of t-statistic: {t_statistic}")
    
    # compute this test's p-value
    p_value = 1 - scipy.stats.t.cdf(t_statistic, df)
    print(f"P-value for statistical test: {p_value}")
    
    # reach a statistical conclusion
    if (p_value < 0.01):
        print(f"\nWe have reached a statistically significant result: Since our p-value of {p_value} is less than our previously stated alpha\nvalue of 0.01, we reject the null hypothesis: We can conclude the best-first search algorithm is faster\nthan the breadth-first search algorithm.")
    else:
        print(f"We have not reached a statistically significant result: Since our p-value of {p_value} is greater than our previously stated alpha\nvalue of 0.01, we fail to reject the null hypothesis.")

def t_test_two_sample(bfs_mean, best_first_mean, bfs_stddev, best_first_stdev, num_samples_bfs, num_samples_best_first):
    print("Two-sample t-test:\n")
    print("Null hypothesis: The best first search algorithm is equally as fast as the breadth first search algorithm.")
    print("Alpha value (Level of significance): 0.01")
    
    # compute this test's degrees of freedom
    df = min(num_samples_bfs - 1, num_samples_best_first - 1)
    
    # compute this test's mean
    difference_of_means = bfs_mean - best_first_mean
    print(f"Difference of means: {difference_of_means}")
    
    # compute this test's standard deviation for the sampling distribution, which is the standard deviation divided by the square root of the number of samples.
    combined_standard_deviation = (((bfs_stddev ** 2) / num_samples_bfs) + ((best_first_stdev ** 2) / num_samples_best_first)) ** (1/2)
    print(f"Combined sampling distribution standard deviation: {combined_standard_deviation}")
    
    # compute this test's t-statistic
    t_statistic = difference_of_means / combined_standard_deviation
    print(f"Value of t-statistic: {t_statistic}")
    
    # compute this test's p-value
    p_value = 1 - scipy.stats.t.cdf(t_statistic, df)
    print(f"P-value for statistical test: {p_value}")
    
    # reach a statistical conclusion
    if (p_value < 0.01):
        print(f"\nWe have reached a statistically significant result: Since our p-value of {p_value} is less than\nour previously stated alpha value of 0.01, we reject the null hypothesis: The best-first search algorithm is faster\nthan the breadth-first search algorithm.")
    else:
        print(f"We have not reached a statistically significant result: Since our p-value of {p_value} is greater than our previously stated\nalpha value of 0.01, we fail to reject the null hypothesis.")
    

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


                name, actor_id, best_first_path_len, time_best_first, bfs_path_len, time_bfs = line
                if int(best_first_path_len) >= 0:
                    
                    
                    best_first_times.append(float(time_best_first))
                    bfs_times.append(float(time_bfs))

                    best_first_lens.append(float(best_first_path_len))
                    bfs_lens.append(float(bfs_path_len))
                    
                time_difference.append(float(time_bfs) - float(time_best_first))


    x = list(range(1, 7))
    bfs_length_to_points = defaultdict(list)
    best_length_to_points = defaultdict(list)
    for i in range(len(bfs_times)):
        bfs_length_to_points[int(bfs_lens[i])].append(bfs_times[i])
        best_length_to_points[int(best_first_lens[i])].append(best_first_times[i])


    bfs_averages = [0] * 6
    best_first_averages = [0] * 6
    for key in bfs_length_to_points:
        bfs_averages[key-1] = mean(bfs_length_to_points[key]) * len(bfs_length_to_points[key]) / len(bfs_times)
        best_first_averages[key-1] = mean(best_length_to_points[key]) * len(best_length_to_points[key]) / len(bfs_times)

    plt.plot(x, bfs_averages)
    plt.plot(x, best_first_averages)
    plt.xlabel("Path Length")
    plt.ylabel("Mean Time by Relative Frequency (s)")
    plt.savefig(path / "data.png")
    plt.show()

    print("---------------------------------")
    t_test_matched_pairs(time_difference)
    
    # Compute all parameters necessary to perform the two-sample t-test
    bfs_mean = mean(bfs_times)
    best_first_mean = mean(best_first_times)
    
    bfs_stdev = stdev(bfs_times)
    best_first_stdev = stdev(best_first_times)
    
    num_samples_bfs = len(bfs_times)
    num_samples_best_first = len(best_first_times)
    
    print("---------------------------------")
    t_test_two_sample(bfs_mean, best_first_mean, bfs_stdev, best_first_stdev, num_samples_bfs, num_samples_best_first)
    
    print("---------------------------------")
    print(f"Average BFS Time: {bfs_mean}\nAverage Best First Times: {best_first_mean}")


if __name__ == "__main__":
    path = pathlib.Path(__file__).parent
    main()
