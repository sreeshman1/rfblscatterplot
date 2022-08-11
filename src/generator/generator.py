import constants
import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter


def parse_csv():
    teams = []
    with open('../../data/stats.csv', 'r', newline='', encoding='utf-8-sig') as stats:
        reader = csv.DictReader(stats)

        for row in reader:
            teams.append(row)
    return teams


def calculate_league_totals(teams):
    chad_league = {
        "PA": 0, "R": 0, "wOBA": 0, "FIP": 0}
    virgin_league = {
        "PA": 0, "R": 0, "wOBA": 0, "FIP": 0}
    total_league = {
        "PA": 0, "R": 0, "wOBA": 0, "FIP": 0}
    for team in teams:
        if (team["Team"] in constants.CLTEAMS):
            chad_league["R"] += int(team["R"])
            chad_league["PA"] += int(team["PA"])
            chad_league["wOBA"] += float(team["wOBA"])
            chad_league["FIP"] += float(team["FIP"])
        else:
            virgin_league["R"] += int(team["R"])
            virgin_league["PA"] += int(team["PA"])
            virgin_league["wOBA"] += float(team["wOBA"])
            virgin_league["FIP"] += float(team["FIP"])
        total_league["R"] += int(team["R"])
        total_league["PA"] += int(team["PA"])
        total_league["wOBA"] += float(team["wOBA"])
        total_league["FIP"] += float(team["FIP"])
    chad_league["wOBA"] /= 12
    chad_league["FIP"] /= 12
    virgin_league["wOBA"] /= 12
    virgin_league["FIP"] /= 12
    total_league["wOBA"] /= 24
    total_league["FIP"] /= 24
    total_league["R/PA"] = total_league["R"] / total_league["PA"]
    chad_league["WRC"] = (((chad_league["wOBA"] - total_league["wOBA"]) /
                          constants.WOBASCALE)+total_league["R/PA"])*chad_league["PA"]
    virgin_league["WRC"] = (((virgin_league["wOBA"] - virgin_league["wOBA"]) /
                             constants.WOBASCALE)+total_league["R/PA"])*virgin_league["PA"]
    return chad_league, virgin_league, total_league


def calculate_team_values(team, cl, vl, ovl):
    if (team["Team"] in constants.CLTEAMS):
        wraa_pa = (float(team["wOBA"]) - ovl["wOBA"])/constants.WOBASCALE
        wrc_plus = ((wraa_pa + ovl["R/PA"] + (ovl["R/PA"] -
                    (float(team["PF"]) * ovl["R/PA"]))) / (cl["WRC"] / cl["PA"]))*100
        fip_minus = ((float(team["FIP"]) + (float(team["FIP"]) -
                     (float(team["FIP"])*float(team["PF"])))) / cl["FIP"]) * 100
    else:
        wraa_pa = (float(team["wOBA"]) - ovl["wOBA"])/constants.WOBASCALE
        wrc_plus = ((wraa_pa + ovl["R/PA"] + (ovl["R/PA"] -
                    (float(team["PF"]) * ovl["R/PA"]))) / (vl["WRC"] / vl["PA"]))*100
        fip_minus = ((float(team["FIP"]) + (float(team["FIP"]) -
                     (float(team["FIP"])*float(team["PF"])))) / vl["FIP"]) * 100
    return {
        "team_name": team["Team"],
        "wrc_plus": round(wrc_plus),
        "fip_minus": round(fip_minus)
    }


def plot_graph(teams):
    plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.0f}')) 
    plt.axvline(100, color='#D3D3D3')
    plt.axhline(100, color='#D3D3D3')
    for team in teams:
        plt.scatter(team["wrc_plus"], team["fip_minus"], s=5*team["wrc_plus"],
                    c="#000000",
                    marker=r"$ {} $".format(team["team_name"]), edgecolors='none')
    # plt.xlabel("WRC+")
    # plt.ylabel("FIP-")
    plt.show()


def main():
    teams = parse_csv()
    chad_league, virgin_league, total_league = calculate_league_totals(teams)
    calc_teams = []
    for team in teams:
        calc_teams.append(calculate_team_values(
            team, chad_league, virgin_league, total_league))
    plot_graph(calc_teams)


if __name__ == "__main__":
    main()
