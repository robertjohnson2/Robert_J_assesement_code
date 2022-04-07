import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import StrMethodFormatter

from commodities_api_utils import process_saved_api_data

COMMODITIES = ["WHEAT", "CORN", "BRENTOIL", "NG"]
CURRENCIES = ["RUB", "UAH", "EUR"]
INVASION_DATE = pd.Timestamp(2022, 2, 24)


def read_and_merge_commodities(commodities):
    df = []
    for commodity in commodities:
        data = process_saved_api_data(commodity)
        df.append(data)
    df = pd.concat(df)
    df = df.dropna()
    return df


def add_analysed_cols(df):
    df["cost"] = 1 / df["amount"]
    df["cost_rolling"] = df.groupby("commodity")["cost"].transform(
        lambda x: x.rolling(7, 1).mean()
    )
    g = df.groupby("commodity").cost
    df["normalised"] = (df.cost - g.transform("min")) / g.transform(np.ptp)
    df["normalised_rolling"] = df.groupby("commodity")["normalised"].transform(
        lambda x: x.rolling(7, 1).mean()
    )
    df["perc_change"] = (df.cost_rolling - g.transform("mean")) / g.transform("mean")
    return df


def make_mpl_line_plot(
    df, yvar, commodities, filename, as_percentage=None, label_lines=None
):
    fig, ax = plt.subplots(figsize=(8.05, 5))
    fig.subplots_adjust(bottom=0.2)

    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.tick_params(axis="x", labelrotation=-30)

    for commodity in commodities:
        ax.plot(
            df[df.commodity == commodity]["date"],
            df[df.commodity == commodity][yvar],
            linewidth=1.5,
            marker="None",
            label=commodity,
        )
        if label_lines is not None:
            ax.text(
                df[df.commodity == commodity]["date"].iloc[-1],
                df[df.commodity == commodity][yvar].iloc[-1],
                commodity,
            )

    ax.axvline(x=INVASION_DATE, c="grey", ls="--", zorder=4)
    ax.text(
        x=INVASION_DATE,
        y=ax.get_ylim()[1],
        s="Russian invasion begins",
        c="black",
        ha="right",
        va="bottom",
        size=10,
    )
    if label_lines is None:
        ax.legend(loc="upper right")
    if as_percentage is not None:
        ax.axhline(y=0, c="grey", ls=":", zorder=4)
        ax.yaxis.set_major_formatter(StrMethodFormatter("{x:.0%}"))

    plt.savefig(f"outputs/{filename}.png")


def main():
    df = read_and_merge_commodities(COMMODITIES+CURRENCIES)
    df_processed = add_analysed_cols(df)


    make_mpl_line_plot(
        df_processed,
        "perc_change",
        CURRENCIES,
        as_percentage=True,
        filename="currencies_perc_change",
    )
    make_mpl_line_plot(
        df_processed,
        "normalised_rolling",
        CURRENCIES,
        filename="currencies_normalised",
    )

    make_mpl_line_plot(
        df_processed,
        "perc_change",
        COMMODITIES,
        as_percentage=True,
        filename="commodities_perc_chnage",
        label_lines=True,
    )
    make_mpl_line_plot(
        df_processed,
        "normalised_rolling",
        COMMODITIES,
        filename="commodities_normalised",
        label_lines=True,
    )


if __name__ == "__main__":
    main()
