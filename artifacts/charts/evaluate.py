from pathlib import Path
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd


def get_count(df, key, lower, upper):
    return df[(lower < df[key]) & (df[key] <= upper)].count().values[0]


def get_distribution(df):
    dist_df = pd.DataFrame({'Size (Bytes)': ['<=10\N{SUPERSCRIPT TWO}',
                                             '10\N{SUPERSCRIPT TWO}-10\N{SUPERSCRIPT THREE}',
                                             '10\N{SUPERSCRIPT THREE}-10\N{SUPERSCRIPT FOUR}',
                                             '10\N{SUPERSCRIPT FOUR}-10\N{SUPERSCRIPT FIVE}',
                                             '10\N{SUPERSCRIPT FIVE}-10\N{SUPERSCRIPT SIX}'],
                            'Number of Schemas': [get_count(df, "inSize", 0, 100),
                                                  get_count(df, "inSize", 100, 1000),
                                                  get_count(df, "inSize", 1000, 10000),
                                                  get_count(df, "inSize", 10000, 100000),
                                                  get_count(df, "inSize", 100000, 1000000)]})
    dist_df = dist_df.reset_index()

    return dist_df


def get_corpus_summary(results_path, digits, plot_path, add_distribution=False):
    df = pd.read_csv(results_path)
    dist_df = get_distribution(df)
    res_str = ""
    # Print distirbution
    if add_distribution:
        for index, row in dist_df.iterrows():
            res_str += f'{row["Size (Bytes)"]}: {row["Number of Schemas"]}\n'
    res_str += f'\tMin Size: {round(df["inSize"].min(), digits)}\n' \
               f'\tMax Size: {round(df["inSize"].max(), digits)}\n'\
               f'\tAverage Size: {round(df["inSize"].mean(), digits)}\n'\
               f"\tMedian Size: {round(df['inSize'].median(), digits)}\n"

    # Plot distribution
    plt.rcParams["font.family"] = ["Liberation Sans", "Arial"]
    matplotlib.style.use('fivethirtyeight')

    ax = dist_df.plot.bar(x="Size (Bytes)", y="Number of Schemas", figsize=(9.91, 7.71))

    ax.set_yscale("log")
    ax.grid(linewidth=1)

    plt.title("Distribution of schema size", fontsize=22)
    plt.legend(["Count"], prop={'size': 12})

    plt.xlabel("Size (Bytes)", fontsize=18)
    plt.ylabel("Number of schemas", fontsize=18)

    plt.yticks(fontname=["Liberation Sans", "Arial"], fontsize=12)
    plt.xticks(fontname="DejaVu Sans", fontsize=12, rotation=0)
    plt.savefig(plot_path)

    return res_str


# Set common styles for plots
def set_plot_style(ax, ylim_low):
    ticks = (1, 10, 100, 1000, 10000, 100000)
    ax.set_yscale("log")
    ax.set_yticks(ticks)
    ax.set_ylim(ylim_low, 500000)

    ax.set_xscale("log")
    ax.set_xticks(ticks)
    ax.set_xlim(1, 500000)

    ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())


def get_runtime(time_path, size_path, digits, plot_path, plot_title):
    time_df = pd.read_csv(time_path)
    size_df = pd.read_csv(size_path)
    time_data = pd.DataFrame({"objectId": time_df["objectId"]})
    time_data["Time"] = (time_df["2Witness"] + time_df["notElim"])
    data = pd.merge(time_data, size_df[["objectId", "2Full"]], on="objectId", how="left")

    res_str = "runtime (ms)\n"\
              f'\tavg: {round(data["Time"].mean(), digits)}\n'\
              f'\tmedian: {round(data["Time"].median(), digits)}\n'\
              f'\tmax: {round(data["Time"].max(), digits)}\n'\
              f'\tmin: {round(data["Time"].min(), digits)}\n'

    plt.style.use('default')
    ax = data.plot.scatter(x="2Full", y="Time", figsize=(15, 10), marker="s", s=30,
                           color="#AAAAAA", edgecolor="#0433FF")

    set_plot_style(ax, 0.1)

    plt.title(plot_title, fontsize=18)
    plt.xlabel("Size of the input schema (Bytes)", fontsize=18)
    plt.ylabel("Time (ms)", fontsize=18)
    plt.savefig(plot_path)

    return res_str


def get_ratio_stats(path, digits, plot_path, plot_title):
    data = pd.read_csv(path)
    data = data[["2Full", "notElim"]].copy()
    data["Ratio"] = (data["notElim"] / data["2Full"])

    res_str = "size ratio\n" + \
              f'\tavg: {round(data["Ratio"].mean(), digits)}\n' + \
              f'\tmedian: {round(data["Ratio"].median(), digits)}\n' + \
              f'\tmax: {round(data["Ratio"].max(), digits)}\n' + \
              f'\tmin: {round(data["Ratio"].min(), digits)}\n'

    plt.style.use('default')
    ax = data.plot.scatter(x="2Full", y="notElim", figsize=(15, 10), marker="s", s=30,
                           color="#AAAAAA", edgecolor="#0433FF")

    set_plot_style(ax, 1)
    ax.grid(linewidth=1)

    plt.xlabel("Size of the input schema (Bytes)", fontsize=18)
    plt.ylabel("Size of the schema after not-elimination (Bytes)", fontsize=18)
    plt.title(plot_title, fontsize=18)
    plt.savefig(plot_path)

    return res_str


if __name__ == '__main__':
    res_dir = "results"
    Path(res_dir).mkdir(parents=True, exist_ok=True)

    # Print and Plot size distribution of original data
    time_pos_sample = "data/positive_sample/results.csv"
    size_pos_sample = "data/positive_sample/size.csv"
    size_dist = get_distribution(pd.read_csv(time_pos_sample))

    results_string = "--- Summary information about the corpus ---\n"
    results_string += get_corpus_summary(time_pos_sample, 2, res_dir + "/" + "size_distribution.pdf", add_distribution=False)

    # Print and plot runtime and size of positive sample
    results_string += "\n--- Summary of experimental results for original schemas ---\n"
    results_string += get_runtime(time_pos_sample, size_pos_sample, 3, res_dir + "/" + "runtime_original.pdf",
                                  "Not-elimination runtime for original schemas")
    results_string += get_ratio_stats(size_pos_sample, 2, res_dir + "/" + "size_ratio_original.pdf",
                                      "Size increase after not-elimination for original schemas.")

    # Print and plot runtime and size of negated sample
    results_string += "\n--- Summary of experimental results for negation-injected schemas ---\n"
    time_neg_sample = "data/negated_sample/results.csv"
    size_neg_sample = "data/negated_sample/size.csv"
    results_string += get_runtime(time_neg_sample, size_neg_sample, 3, res_dir + "/" + "runtime_negated.pdf",
                                  "Not-elimination runtime for negation-injected schemas")
    results_string += get_ratio_stats(size_neg_sample, 3, res_dir + "/" + "size_ratio_negated.pdf",
                                      "Size increase after not-elimination for negation-injected schemas.")

    print(results_string)
    with open("results/summary.txt", 'w') as f:
        f.write(results_string)
