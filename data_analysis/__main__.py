import argparse

from data_analysis.heatpump import heatpump_analysis
from data_analysis.solar_vs_p1 import solar_vs_p1


analyses = {
    "heatpump": heatpump_analysis,
    "solar": solar_vs_p1,
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("analysis", choices=analyses.keys())
    args = parser.parse_args()

    print(f"You selected analysis: {args.analysis}")
    analyses[args.analysis]()
