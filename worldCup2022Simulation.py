{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/JayJung98/2022WorldCupWinner/blob/main/worldCup2022Simulation.ipynb\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "0e1c94e7",
      "metadata": {
        "id": "0e1c94e7"
      },
      "source": [
        "# <strong>Introduction: 2022 Qatar World Cup Power Ranking and Winner(Simulation)</strong><br>\n",
        "Introduction: Predicting the winner of 2022 Qatar World Cup<br>\n",
        "Method:\n",
        "- 1. Read Data\n",
        "- 2. Feature Selection:\n",
        "    - Goal Difference = AVG(Offense Score) - AVG(Diffense Score)\n",
        "    - Current Rank\n",
        "    - Average Rank for 10 years\n",
        "    - Not Friendly Game\n",
        "\n",
        "- 3. Model Selection: Logistic Regresion, XGBoost, Gradinet Boosting, Ada Boosting\n",
        "- 4. Simulation\n",
        "- 5. Visualization\n",
        "\n",
        "\n",
        "This project was based on the following project: https://www.kaggle.com/code/agostontorok/soccer-world-cup-2018-winner/notebook<br>\n",
        "Data Source:\n",
        "- results: https://www.kaggle.com/datasets/martj42/international-football-results-from-1872-to-2017 (modified by Jay Jung)\n",
        "- Qatar2022-teams: Written by Jay Jung\n",
        "- fifaRanking2020-10-06: https://www.kaggle.com/datasets/cashncarry/fifaworldranking (modified by Jay Jung)<br>\n",
        "\n",
        "Data Modification: Modified data because the affecting data for this World Cup are up to 10 years. <br>\n",
        "Wokred with Goolge Colab and Jupyter Notebook"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "## 1. Read Data"
      ],
      "metadata": {
        "id": "TRIr2vvO5F_n"
      },
      "id": "TRIr2vvO5F_n"
    },
    {
      "cell_type": "code",
      "execution_count": 194,
      "id": "85c47c43",
      "metadata": {
        "id": "85c47c43"
      },
      "outputs": [],
      "source": [
        "import numpy as np\n",
        "import pandas as pd\n",
        "import warnings\n",
        "warnings.filterwarnings(action = 'ignore')\n",
        "\n",
        "rankings = pd.read_csv('./worldCupData/fifaRanking2020-10-06.csv', encoding='windows-1252')\n",
        "matches = pd.read_csv('./worldCupData/results.csv', encoding='windows-1252')\n",
        "groups = pd.read_csv('./worldCupData/Qatar2022-teams.csv')"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 195,
      "id": "24ce2f9f",
      "metadata": {
        "scrolled": true,
        "id": "24ce2f9f"
      },
      "outputs": [],
      "source": [
        "# Unified countries name\n",
        "rankings = rankings.replace({\"IR Iran\": \"Iran\"})\n",
        "rankings = rankings.replace({\"Korea Republic\": \"South Korea\"})\n",
        "rankings['rank_date'] = pd.to_datetime(rankings['rank_date'])\n",
        "matches['date'] = pd.to_datetime(matches['date'])\n",
        "matches = matches.replace({\"United States\": \"USA\"})"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 196,
      "id": "e2ff33ed",
      "metadata": {
        "id": "e2ff33ed"
      },
      "outputs": [],
      "source": [
        "#rankings.head()"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "8f9e8cc9",
      "metadata": {
        "id": "8f9e8cc9"
      },
      "source": [
        "## 2. Feature Engineering"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "e905505c",
      "metadata": {
        "id": "e905505c"
      },
      "source": [
        "### 2.1 Extract team list for 2022 Qatar World Cup"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 197,
      "id": "7116a09f",
      "metadata": {
        "id": "7116a09f"
      },
      "outputs": [],
      "source": [
        "country_list = groups['Team'].values.tolist()\n",
        "country_list = sorted(country_list)\n",
        "# country_list"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 198,
      "id": "f3efd74b",
      "metadata": {
        "id": "f3efd74b"
      },
      "outputs": [],
      "source": [
        "# Get Average rankings for 10 years for each country\n",
        "avgRanking = rankings.groupby(['country_full']).mean()\n",
        "avgRanking = avgRanking.reset_index()"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 199,
      "id": "b29c941c",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "b29c941c",
        "outputId": "8a2f9170-9087-4e7a-a44f-ae87b9f2594d"
      },
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "Index(['date', 'home_team', 'away_team', 'home_score', 'away_score',\n",
              "       'tournament', 'country', 'neutral'],\n",
              "      dtype='object')"
            ]
          },
          "metadata": {},
          "execution_count": 199
        }
      ],
      "source": [
        "matches.columns"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "0b0cda60",
      "metadata": {
        "id": "0b0cda60"
      },
      "source": [
        "Different number of data <br>\n",
        "so extract countries which join the 2022 Qatar World Cup <br><br>\n",
        "Countries: ['Senegal', 'Qatar', 'Netherlands', 'Ecuador', 'Iran', 'England', 'USA', 'Wales', 'Argentina', 'Saudi Arabia', 'Mexico', 'Poland', 'Denmark', 'Tunisia', 'France', 'Australia', 'Germany', 'Japan', 'Spain', 'Costa Rica', 'Morocco', 'Croatia', 'Belgium', 'Canada', 'Switzerland', 'Cameroon', 'Brazil', 'Serbia', 'Uruguay', 'South Korea', 'Portugal', 'Ghana']"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 200,
      "id": "882ad2f5",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "882ad2f5",
        "outputId": "87b9ac29-dff6-4094-d9b8-8972b40ad21f"
      },
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "283"
            ]
          },
          "metadata": {},
          "execution_count": 200
        }
      ],
      "source": [
        "# Different number of data\n",
        "home_offense = matches.groupby(['home_team']).mean()['home_score'].fillna(0)\n",
        "len(home_offense)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 201,
      "id": "d6990116",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "d6990116",
        "outputId": "b39f019b-5240-40fd-d086-b1b6e8cdbbd9"
      },
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "278"
            ]
          },
          "metadata": {},
          "execution_count": 201
        }
      ],
      "source": [
        "# Different number of data\n",
        "away_offense = matches.groupby(['away_team']).mean()['away_score'].fillna(0)\n",
        "len(away_offense)"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "e73a5e02",
      "metadata": {
        "id": "e73a5e02"
      },
      "source": [
        "### 2.2 Goal Difference(GD) for each team\n",
        "Offense Score = avg(home score) * 0.3 + avg(away score) * 0.7\n",
        "(Additional points are given because it is more difficult to score in away games.)<br>\n",
        "Defense Score = avg(away score) + avg(home score)<br>\n",
        "GD = Offense Score - Deffense Score"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 202,
      "id": "5e4293cc",
      "metadata": {
        "id": "5e4293cc"
      },
      "outputs": [],
      "source": [
        "home = home_offense.to_frame().reset_index()\n",
        "away = away_offense.to_frame().reset_index()"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 203,
      "id": "5a9136d8",
      "metadata": {
        "id": "5a9136d8"
      },
      "outputs": [],
      "source": [
        "home = home[home['home_team'].isin(country_list)].reset_index()\n",
        "home = home.drop(['index'], axis = 1)\n",
        "#home"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 204,
      "id": "10e76546",
      "metadata": {
        "id": "10e76546"
      },
      "outputs": [],
      "source": [
        "away = away[away['away_team'].isin(country_list)].reset_index()\n",
        "away = away.drop(['index'], axis = 1)\n",
        "# away"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 205,
      "id": "3434e417",
      "metadata": {
        "id": "3434e417"
      },
      "outputs": [],
      "source": [
        "wc_score = pd.DataFrame()\n",
        "wc_score['country_name'] = country_list\n",
        "wc_score['offense_score'] = round((home['home_score'] * 0.3 + away['away_score'] * 0.7), 2) # Most gmaes are away game so I weighted more in away_score\n",
        "# wc_score"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 206,
      "id": "4cee2218",
      "metadata": {
        "id": "4cee2218"
      },
      "outputs": [],
      "source": [
        "home_diffense = matches.groupby(['home_team']).mean()['away_score'].fillna(0)\n",
        "away_diffense = matches.groupby(['away_team']).mean()['home_score'].fillna(0)\n",
        "home = home_diffense.to_frame().reset_index()\n",
        "away = away_diffense.to_frame().reset_index()\n",
        "home = home[home['home_team'].isin(country_list)].reset_index()\n",
        "home = home.drop(['index'], axis = 1)\n",
        "away = away[away['away_team'].isin(country_list)].reset_index()\n",
        "away = away.drop(['index'], axis = 1)\n",
        "wc_score['diffense_score'] = round(home['away_score'] * 0.3 + away['home_score'] * 0.7, 2) # most games are away\n",
        "wc_score['GD'] = (wc_score['offense_score'] - wc_score['diffense_score']) # Goals Difference\n",
        "# wc_score"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "51d6a905",
      "metadata": {
        "id": "51d6a905"
      },
      "source": [
        "### 2.3 Average Rankings for 10 years"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 207,
      "id": "4d71f2a5",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 206
        },
        "id": "4d71f2a5",
        "outputId": "08537433-6ce1-4c1b-b354-9e4e55b31dad"
      },
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "     country_full        rank\n",
              "0     Afghanistan  146.207921\n",
              "1         Albania   56.524752\n",
              "2         Algeria   37.930693\n",
              "3  American Samoa  190.396040\n",
              "4         Andorra  173.128713"
            ],
            "text/html": [
              "\n",
              "  <div id=\"df-1f74c69e-21fd-4726-b787-f66851e1d283\">\n",
              "    <div class=\"colab-df-container\">\n",
              "      <div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>country_full</th>\n",
              "      <th>rank</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>Afghanistan</td>\n",
              "      <td>146.207921</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>Albania</td>\n",
              "      <td>56.524752</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>Algeria</td>\n",
              "      <td>37.930693</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>American Samoa</td>\n",
              "      <td>190.396040</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>Andorra</td>\n",
              "      <td>173.128713</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>\n",
              "      <button class=\"colab-df-convert\" onclick=\"convertToInteractive('df-1f74c69e-21fd-4726-b787-f66851e1d283')\"\n",
              "              title=\"Convert this dataframe to an interactive table.\"\n",
              "              style=\"display:none;\">\n",
              "        \n",
              "  <svg xmlns=\"http://www.w3.org/2000/svg\" height=\"24px\"viewBox=\"0 0 24 24\"\n",
              "       width=\"24px\">\n",
              "    <path d=\"M0 0h24v24H0V0z\" fill=\"none\"/>\n",
              "    <path d=\"M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z\"/><path d=\"M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z\"/>\n",
              "  </svg>\n",
              "      </button>\n",
              "      \n",
              "  <style>\n",
              "    .colab-df-container {\n",
              "      display:flex;\n",
              "      flex-wrap:wrap;\n",
              "      gap: 12px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert {\n",
              "      background-color: #E8F0FE;\n",
              "      border: none;\n",
              "      border-radius: 50%;\n",
              "      cursor: pointer;\n",
              "      display: none;\n",
              "      fill: #1967D2;\n",
              "      height: 32px;\n",
              "      padding: 0 0 0 0;\n",
              "      width: 32px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert:hover {\n",
              "      background-color: #E2EBFA;\n",
              "      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);\n",
              "      fill: #174EA6;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert {\n",
              "      background-color: #3B4455;\n",
              "      fill: #D2E3FC;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert:hover {\n",
              "      background-color: #434B5C;\n",
              "      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);\n",
              "      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));\n",
              "      fill: #FFFFFF;\n",
              "    }\n",
              "  </style>\n",
              "\n",
              "      <script>\n",
              "        const buttonEl =\n",
              "          document.querySelector('#df-1f74c69e-21fd-4726-b787-f66851e1d283 button.colab-df-convert');\n",
              "        buttonEl.style.display =\n",
              "          google.colab.kernel.accessAllowed ? 'block' : 'none';\n",
              "\n",
              "        async function convertToInteractive(key) {\n",
              "          const element = document.querySelector('#df-1f74c69e-21fd-4726-b787-f66851e1d283');\n",
              "          const dataTable =\n",
              "            await google.colab.kernel.invokeFunction('convertToInteractive',\n",
              "                                                     [key], {});\n",
              "          if (!dataTable) return;\n",
              "\n",
              "          const docLinkHtml = 'Like what you see? Visit the ' +\n",
              "            '<a target=\"_blank\" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'\n",
              "            + ' to learn more about interactive tables.';\n",
              "          element.innerHTML = '';\n",
              "          dataTable['output_type'] = 'display_data';\n",
              "          await google.colab.output.renderOutput(dataTable, element);\n",
              "          const docLink = document.createElement('div');\n",
              "          docLink.innerHTML = docLinkHtml;\n",
              "          element.appendChild(docLink);\n",
              "        }\n",
              "      </script>\n",
              "    </div>\n",
              "  </div>\n",
              "  "
            ]
          },
          "metadata": {},
          "execution_count": 207
        }
      ],
      "source": [
        "avgRanking = avgRanking[['country_full', 'rank']]\n",
        "avgRanking.head()"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 208,
      "id": "a12fe904",
      "metadata": {
        "id": "a12fe904"
      },
      "outputs": [],
      "source": [
        "avgRank = avgRanking[avgRanking['country_full'].isin(country_list)].reset_index()\n",
        "avgRank = avgRank.drop(['index'], axis = 1)\n",
        "# avgRank"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "4caf54de",
      "metadata": {
        "id": "4caf54de"
      },
      "source": [
        "### 2.4 Win Rate for each Team"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 209,
      "id": "4f1fd366",
      "metadata": {
        "id": "4f1fd366"
      },
      "outputs": [],
      "source": [
        "matches['score_difference_home'] = matches['home_score'] - matches['away_score']\n",
        "matches['score_difference_away'] = matches['away_score'] - matches['home_score']\n",
        "matches['home win'] = ((matches['score_difference_home'] > 0) & (matches['tournament'] != 'Friendly'))\n",
        "matches['away win'] = ((matches['score_difference_away'] > 0) & (matches['tournament'] != 'Friendly'))\n",
        "matches = matches[(matches['home_team'].isin(country_list)) | matches['away_team'].isin(country_list)]\n",
        "# matches"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 210,
      "id": "09ad919d",
      "metadata": {
        "id": "09ad919d"
      },
      "outputs": [],
      "source": [
        "winRate = {'country' : [], 'winrate': []}\n",
        "for i in country_list:\n",
        "    count = matches[(matches['home_team'] == i) | (matches['away_team'] == i) == True]\n",
        "    winRate['country'].append(i)\n",
        "    winRate['winrate'].append((len(count[count['home win']] == True) + len(count[count['away win']] == True)) / len(count))\n",
        "    \n",
        "winRate = pd.DataFrame(winRate)\n",
        "#winRate"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 211,
      "id": "ba318f75",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 1000
        },
        "id": "ba318f75",
        "outputId": "e49480e1-0c72-4063-9427-7f8b66b88e37"
      },
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "    country_name  current_rank  avgRank    GD  winRate\n",
              "0         Brazil             1     5.06  1.63     0.47\n",
              "1        Belgium             2     4.49  1.40     0.65\n",
              "2      Argentina             3     4.47  0.97     0.49\n",
              "3         France             4     9.69  0.86     0.47\n",
              "4        England             5     9.68  1.28     0.54\n",
              "5          Spain             7     6.72  1.18     0.55\n",
              "6    Netherlands             8    14.15  0.98     0.54\n",
              "7       Portugal             9     6.43  1.05     0.53\n",
              "8        Denmark            10    23.78  0.75     0.51\n",
              "9        Germany            11     5.98  1.17     0.56\n",
              "10       Croatia            12    13.71  0.54     0.55\n",
              "11        Mexico            13    16.49  0.42     0.45\n",
              "12       Uruguay            14    10.92  0.41     0.54\n",
              "13   Switzerland            15    11.40  0.56     0.55\n",
              "14           USA            16    23.20  0.29     0.50\n",
              "15       Senegal            18    37.26  0.70     0.54\n",
              "16         Wales            19    25.69  0.06     0.56\n",
              "17          Iran            20    35.85  1.23     0.48\n",
              "18        Serbia            21    37.39  0.38     0.48\n",
              "19       Morocco            22    57.43  0.64     0.45\n",
              "20         Japan            24    42.30  0.72     0.61\n",
              "21        Poland            26    31.25  0.73     0.54\n",
              "22   South Korea            28    47.90  0.28     0.40\n",
              "23       Tunisia            30    33.86  0.31     0.52\n",
              "24    Costa Rica            31    32.92 -0.06     0.45\n",
              "25     Australia            38    50.19  0.46     0.52\n",
              "26        Canada            41    88.90  0.76     0.52\n",
              "27      Cameroon            43    50.97  0.14     0.46\n",
              "28       Ecuador            44    37.77  0.01     0.45\n",
              "29         Qatar            50    82.69  0.25     0.45\n",
              "30  Saudi Arabia            51    73.40  0.24     0.54\n",
              "31         Ghana            61    41.77  0.31     0.50"
            ],
            "text/html": [
              "\n",
              "  <div id=\"df-84297cc8-7367-489b-bb1c-a60567dd3969\">\n",
              "    <div class=\"colab-df-container\">\n",
              "      <div>\n",
              "<style scoped>\n",
              "    .dataframe tbody tr th:only-of-type {\n",
              "        vertical-align: middle;\n",
              "    }\n",
              "\n",
              "    .dataframe tbody tr th {\n",
              "        vertical-align: top;\n",
              "    }\n",
              "\n",
              "    .dataframe thead th {\n",
              "        text-align: right;\n",
              "    }\n",
              "</style>\n",
              "<table border=\"1\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr style=\"text-align: right;\">\n",
              "      <th></th>\n",
              "      <th>country_name</th>\n",
              "      <th>current_rank</th>\n",
              "      <th>avgRank</th>\n",
              "      <th>GD</th>\n",
              "      <th>winRate</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th>0</th>\n",
              "      <td>Brazil</td>\n",
              "      <td>1</td>\n",
              "      <td>5.06</td>\n",
              "      <td>1.63</td>\n",
              "      <td>0.47</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>1</th>\n",
              "      <td>Belgium</td>\n",
              "      <td>2</td>\n",
              "      <td>4.49</td>\n",
              "      <td>1.40</td>\n",
              "      <td>0.65</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>2</th>\n",
              "      <td>Argentina</td>\n",
              "      <td>3</td>\n",
              "      <td>4.47</td>\n",
              "      <td>0.97</td>\n",
              "      <td>0.49</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>3</th>\n",
              "      <td>France</td>\n",
              "      <td>4</td>\n",
              "      <td>9.69</td>\n",
              "      <td>0.86</td>\n",
              "      <td>0.47</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>4</th>\n",
              "      <td>England</td>\n",
              "      <td>5</td>\n",
              "      <td>9.68</td>\n",
              "      <td>1.28</td>\n",
              "      <td>0.54</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>5</th>\n",
              "      <td>Spain</td>\n",
              "      <td>7</td>\n",
              "      <td>6.72</td>\n",
              "      <td>1.18</td>\n",
              "      <td>0.55</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>6</th>\n",
              "      <td>Netherlands</td>\n",
              "      <td>8</td>\n",
              "      <td>14.15</td>\n",
              "      <td>0.98</td>\n",
              "      <td>0.54</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>7</th>\n",
              "      <td>Portugal</td>\n",
              "      <td>9</td>\n",
              "      <td>6.43</td>\n",
              "      <td>1.05</td>\n",
              "      <td>0.53</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>8</th>\n",
              "      <td>Denmark</td>\n",
              "      <td>10</td>\n",
              "      <td>23.78</td>\n",
              "      <td>0.75</td>\n",
              "      <td>0.51</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>9</th>\n",
              "      <td>Germany</td>\n",
              "      <td>11</td>\n",
              "      <td>5.98</td>\n",
              "      <td>1.17</td>\n",
              "      <td>0.56</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>10</th>\n",
              "      <td>Croatia</td>\n",
              "      <td>12</td>\n",
              "      <td>13.71</td>\n",
              "      <td>0.54</td>\n",
              "      <td>0.55</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>11</th>\n",
              "      <td>Mexico</td>\n",
              "      <td>13</td>\n",
              "      <td>16.49</td>\n",
              "      <td>0.42</td>\n",
              "      <td>0.45</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>12</th>\n",
              "      <td>Uruguay</td>\n",
              "      <td>14</td>\n",
              "      <td>10.92</td>\n",
              "      <td>0.41</td>\n",
              "      <td>0.54</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>13</th>\n",
              "      <td>Switzerland</td>\n",
              "      <td>15</td>\n",
              "      <td>11.40</td>\n",
              "      <td>0.56</td>\n",
              "      <td>0.55</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>14</th>\n",
              "      <td>USA</td>\n",
              "      <td>16</td>\n",
              "      <td>23.20</td>\n",
              "      <td>0.29</td>\n",
              "      <td>0.50</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>15</th>\n",
              "      <td>Senegal</td>\n",
              "      <td>18</td>\n",
              "      <td>37.26</td>\n",
              "      <td>0.70</td>\n",
              "      <td>0.54</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>16</th>\n",
              "      <td>Wales</td>\n",
              "      <td>19</td>\n",
              "      <td>25.69</td>\n",
              "      <td>0.06</td>\n",
              "      <td>0.56</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>17</th>\n",
              "      <td>Iran</td>\n",
              "      <td>20</td>\n",
              "      <td>35.85</td>\n",
              "      <td>1.23</td>\n",
              "      <td>0.48</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>18</th>\n",
              "      <td>Serbia</td>\n",
              "      <td>21</td>\n",
              "      <td>37.39</td>\n",
              "      <td>0.38</td>\n",
              "      <td>0.48</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>19</th>\n",
              "      <td>Morocco</td>\n",
              "      <td>22</td>\n",
              "      <td>57.43</td>\n",
              "      <td>0.64</td>\n",
              "      <td>0.45</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>20</th>\n",
              "      <td>Japan</td>\n",
              "      <td>24</td>\n",
              "      <td>42.30</td>\n",
              "      <td>0.72</td>\n",
              "      <td>0.61</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>21</th>\n",
              "      <td>Poland</td>\n",
              "      <td>26</td>\n",
              "      <td>31.25</td>\n",
              "      <td>0.73</td>\n",
              "      <td>0.54</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>22</th>\n",
              "      <td>South Korea</td>\n",
              "      <td>28</td>\n",
              "      <td>47.90</td>\n",
              "      <td>0.28</td>\n",
              "      <td>0.40</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>23</th>\n",
              "      <td>Tunisia</td>\n",
              "      <td>30</td>\n",
              "      <td>33.86</td>\n",
              "      <td>0.31</td>\n",
              "      <td>0.52</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>24</th>\n",
              "      <td>Costa Rica</td>\n",
              "      <td>31</td>\n",
              "      <td>32.92</td>\n",
              "      <td>-0.06</td>\n",
              "      <td>0.45</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>25</th>\n",
              "      <td>Australia</td>\n",
              "      <td>38</td>\n",
              "      <td>50.19</td>\n",
              "      <td>0.46</td>\n",
              "      <td>0.52</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>26</th>\n",
              "      <td>Canada</td>\n",
              "      <td>41</td>\n",
              "      <td>88.90</td>\n",
              "      <td>0.76</td>\n",
              "      <td>0.52</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>27</th>\n",
              "      <td>Cameroon</td>\n",
              "      <td>43</td>\n",
              "      <td>50.97</td>\n",
              "      <td>0.14</td>\n",
              "      <td>0.46</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>28</th>\n",
              "      <td>Ecuador</td>\n",
              "      <td>44</td>\n",
              "      <td>37.77</td>\n",
              "      <td>0.01</td>\n",
              "      <td>0.45</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>29</th>\n",
              "      <td>Qatar</td>\n",
              "      <td>50</td>\n",
              "      <td>82.69</td>\n",
              "      <td>0.25</td>\n",
              "      <td>0.45</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>30</th>\n",
              "      <td>Saudi Arabia</td>\n",
              "      <td>51</td>\n",
              "      <td>73.40</td>\n",
              "      <td>0.24</td>\n",
              "      <td>0.54</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th>31</th>\n",
              "      <td>Ghana</td>\n",
              "      <td>61</td>\n",
              "      <td>41.77</td>\n",
              "      <td>0.31</td>\n",
              "      <td>0.50</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n",
              "</div>\n",
              "      <button class=\"colab-df-convert\" onclick=\"convertToInteractive('df-84297cc8-7367-489b-bb1c-a60567dd3969')\"\n",
              "              title=\"Convert this dataframe to an interactive table.\"\n",
              "              style=\"display:none;\">\n",
              "        \n",
              "  <svg xmlns=\"http://www.w3.org/2000/svg\" height=\"24px\"viewBox=\"0 0 24 24\"\n",
              "       width=\"24px\">\n",
              "    <path d=\"M0 0h24v24H0V0z\" fill=\"none\"/>\n",
              "    <path d=\"M18.56 5.44l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94zm-11 1L8.5 8.5l.94-2.06 2.06-.94-2.06-.94L8.5 2.5l-.94 2.06-2.06.94zm10 10l.94 2.06.94-2.06 2.06-.94-2.06-.94-.94-2.06-.94 2.06-2.06.94z\"/><path d=\"M17.41 7.96l-1.37-1.37c-.4-.4-.92-.59-1.43-.59-.52 0-1.04.2-1.43.59L10.3 9.45l-7.72 7.72c-.78.78-.78 2.05 0 2.83L4 21.41c.39.39.9.59 1.41.59.51 0 1.02-.2 1.41-.59l7.78-7.78 2.81-2.81c.8-.78.8-2.07 0-2.86zM5.41 20L4 18.59l7.72-7.72 1.47 1.35L5.41 20z\"/>\n",
              "  </svg>\n",
              "      </button>\n",
              "      \n",
              "  <style>\n",
              "    .colab-df-container {\n",
              "      display:flex;\n",
              "      flex-wrap:wrap;\n",
              "      gap: 12px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert {\n",
              "      background-color: #E8F0FE;\n",
              "      border: none;\n",
              "      border-radius: 50%;\n",
              "      cursor: pointer;\n",
              "      display: none;\n",
              "      fill: #1967D2;\n",
              "      height: 32px;\n",
              "      padding: 0 0 0 0;\n",
              "      width: 32px;\n",
              "    }\n",
              "\n",
              "    .colab-df-convert:hover {\n",
              "      background-color: #E2EBFA;\n",
              "      box-shadow: 0px 1px 2px rgba(60, 64, 67, 0.3), 0px 1px 3px 1px rgba(60, 64, 67, 0.15);\n",
              "      fill: #174EA6;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert {\n",
              "      background-color: #3B4455;\n",
              "      fill: #D2E3FC;\n",
              "    }\n",
              "\n",
              "    [theme=dark] .colab-df-convert:hover {\n",
              "      background-color: #434B5C;\n",
              "      box-shadow: 0px 1px 3px 1px rgba(0, 0, 0, 0.15);\n",
              "      filter: drop-shadow(0px 1px 2px rgba(0, 0, 0, 0.3));\n",
              "      fill: #FFFFFF;\n",
              "    }\n",
              "  </style>\n",
              "\n",
              "      <script>\n",
              "        const buttonEl =\n",
              "          document.querySelector('#df-84297cc8-7367-489b-bb1c-a60567dd3969 button.colab-df-convert');\n",
              "        buttonEl.style.display =\n",
              "          google.colab.kernel.accessAllowed ? 'block' : 'none';\n",
              "\n",
              "        async function convertToInteractive(key) {\n",
              "          const element = document.querySelector('#df-84297cc8-7367-489b-bb1c-a60567dd3969');\n",
              "          const dataTable =\n",
              "            await google.colab.kernel.invokeFunction('convertToInteractive',\n",
              "                                                     [key], {});\n",
              "          if (!dataTable) return;\n",
              "\n",
              "          const docLinkHtml = 'Like what you see? Visit the ' +\n",
              "            '<a target=\"_blank\" href=https://colab.research.google.com/notebooks/data_table.ipynb>data table notebook</a>'\n",
              "            + ' to learn more about interactive tables.';\n",
              "          element.innerHTML = '';\n",
              "          dataTable['output_type'] = 'display_data';\n",
              "          await google.colab.output.renderOutput(dataTable, element);\n",
              "          const docLink = document.createElement('div');\n",
              "          docLink.innerHTML = docLinkHtml;\n",
              "          element.appendChild(docLink);\n",
              "        }\n",
              "      </script>\n",
              "    </div>\n",
              "  </div>\n",
              "  "
            ]
          },
          "metadata": {},
          "execution_count": 211
        }
      ],
      "source": [
        "curRank = rankings[rankings['country_full'].isin(country_list)]\n",
        "curRank = curRank.loc[curRank['rank_date'] == '2022-10-06'][['country_full', 'rank']]\n",
        "curRank = curRank.sort_values('country_full')\n",
        "wc_score['current_rank']= curRank['rank'].values.tolist()\n",
        "wc_score['avgRank'] = round(avgRank['rank'], 2)\n",
        "wc_score['winRate'] = round(winRate['winrate'], 2)\n",
        "wc_score = wc_score[['country_name', 'current_rank', 'avgRank', 'GD', 'winRate']]\n",
        "wc_score = wc_score.sort_values('current_rank').reset_index().drop(['index'], axis = 1)\n",
        "wc_score"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 212,
      "id": "30165fd1",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 175
        },
        "id": "30165fd1",
        "outputId": "8e891cd2-6c59-40cb-fd5d-3a7d7b9bbfc2"
      },
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "<pandas.io.formats.style.Styler at 0x7f41cc09bc90>"
            ],
            "text/html": [
              "<style type=\"text/css\">\n",
              "#T_a0eb8_row0_col0, #T_a0eb8_row1_col1, #T_a0eb8_row2_col2, #T_a0eb8_row3_col3 {\n",
              "  background-color: #023858;\n",
              "  color: #f1f1f1;\n",
              "}\n",
              "#T_a0eb8_row0_col1 {\n",
              "  background-color: #045788;\n",
              "  color: #f1f1f1;\n",
              "}\n",
              "#T_a0eb8_row0_col2, #T_a0eb8_row1_col3, #T_a0eb8_row2_col0, #T_a0eb8_row2_col1 {\n",
              "  background-color: #fff7fb;\n",
              "  color: #000000;\n",
              "}\n",
              "#T_a0eb8_row0_col3 {\n",
              "  background-color: #fef6fa;\n",
              "  color: #000000;\n",
              "}\n",
              "#T_a0eb8_row1_col0 {\n",
              "  background-color: #045483;\n",
              "  color: #f1f1f1;\n",
              "}\n",
              "#T_a0eb8_row1_col2 {\n",
              "  background-color: #f0eaf4;\n",
              "  color: #000000;\n",
              "}\n",
              "#T_a0eb8_row2_col3 {\n",
              "  background-color: #65a3cb;\n",
              "  color: #f1f1f1;\n",
              "}\n",
              "#T_a0eb8_row3_col0 {\n",
              "  background-color: #d6d6e9;\n",
              "  color: #000000;\n",
              "}\n",
              "#T_a0eb8_row3_col1 {\n",
              "  background-color: #ece7f2;\n",
              "  color: #000000;\n",
              "}\n",
              "#T_a0eb8_row3_col2 {\n",
              "  background-color: #348ebf;\n",
              "  color: #f1f1f1;\n",
              "}\n",
              "</style>\n",
              "<table id=\"T_a0eb8_\" class=\"dataframe\">\n",
              "  <thead>\n",
              "    <tr>\n",
              "      <th class=\"blank level0\" >&nbsp;</th>\n",
              "      <th class=\"col_heading level0 col0\" >current_rank</th>\n",
              "      <th class=\"col_heading level0 col1\" >avgRank</th>\n",
              "      <th class=\"col_heading level0 col2\" >GD</th>\n",
              "      <th class=\"col_heading level0 col3\" >winRate</th>\n",
              "    </tr>\n",
              "  </thead>\n",
              "  <tbody>\n",
              "    <tr>\n",
              "      <th id=\"T_a0eb8_level0_row0\" class=\"row_heading level0 row0\" >current_rank</th>\n",
              "      <td id=\"T_a0eb8_row0_col0\" class=\"data row0 col0\" >1.000000</td>\n",
              "      <td id=\"T_a0eb8_row0_col1\" class=\"data row0 col1\" >0.827994</td>\n",
              "      <td id=\"T_a0eb8_row0_col2\" class=\"data row0 col2\" >-0.675269</td>\n",
              "      <td id=\"T_a0eb8_row0_col3\" class=\"data row0 col3\" >-0.299605</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th id=\"T_a0eb8_level0_row1\" class=\"row_heading level0 row1\" >avgRank</th>\n",
              "      <td id=\"T_a0eb8_row1_col0\" class=\"data row1 col0\" >0.827994</td>\n",
              "      <td id=\"T_a0eb8_row1_col1\" class=\"data row1 col1\" >1.000000</td>\n",
              "      <td id=\"T_a0eb8_row1_col2\" class=\"data row1 col2\" >-0.502896</td>\n",
              "      <td id=\"T_a0eb8_row1_col3\" class=\"data row1 col3\" >-0.313125</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th id=\"T_a0eb8_level0_row2\" class=\"row_heading level0 row2\" >GD</th>\n",
              "      <td id=\"T_a0eb8_row2_col0\" class=\"data row2 col0\" >-0.675269</td>\n",
              "      <td id=\"T_a0eb8_row2_col1\" class=\"data row2 col1\" >-0.502896</td>\n",
              "      <td id=\"T_a0eb8_row2_col2\" class=\"data row2 col2\" >1.000000</td>\n",
              "      <td id=\"T_a0eb8_row2_col3\" class=\"data row2 col3\" >0.383654</td>\n",
              "    </tr>\n",
              "    <tr>\n",
              "      <th id=\"T_a0eb8_level0_row3\" class=\"row_heading level0 row3\" >winRate</th>\n",
              "      <td id=\"T_a0eb8_row3_col0\" class=\"data row3 col0\" >-0.299605</td>\n",
              "      <td id=\"T_a0eb8_row3_col1\" class=\"data row3 col1\" >-0.313125</td>\n",
              "      <td id=\"T_a0eb8_row3_col2\" class=\"data row3 col2\" >0.383654</td>\n",
              "      <td id=\"T_a0eb8_row3_col3\" class=\"data row3 col3\" >1.000000</td>\n",
              "    </tr>\n",
              "  </tbody>\n",
              "</table>\n"
            ]
          },
          "metadata": {},
          "execution_count": 212
        }
      ],
      "source": [
        "corr = wc_score.corr()\n",
        "corr.style.background_gradient()"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "180fa02a",
      "metadata": {
        "id": "180fa02a"
      },
      "source": [
        "current_rank and avgRank have high correlation."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 213,
      "id": "eaeaf46c",
      "metadata": {
        "id": "eaeaf46c"
      },
      "outputs": [],
      "source": [
        "# Merge matches and rankings data for the simulation\n",
        "rankings = rankings.set_index(['rank_date'])\\\n",
        "            .groupby(['country_full'], group_keys=False)\\\n",
        "            .resample('D').first()\\\n",
        "            .fillna(method='ffill')\\\n",
        "            .reset_index()\n",
        "\n",
        "# join the ranks\n",
        "matches = matches.merge(rankings, \n",
        "                        left_on=['date', 'home_team'], \n",
        "                        right_on=['rank_date', 'country_full'])\n",
        "matches = matches.merge(rankings, \n",
        "                        left_on=['date', 'away_team'], \n",
        "                        right_on=['rank_date', 'country_full'], \n",
        "                        suffixes=('_home', '_away'))"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 214,
      "id": "7040a1f6",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "7040a1f6",
        "outputId": "8fac3030-386c-41e6-c049-2e5664be0287"
      },
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "Index(['date', 'home_team', 'away_team', 'home_score', 'away_score',\n",
              "       'tournament', 'country', 'neutral', 'score_difference_home',\n",
              "       'score_difference_away', 'home win', 'away win', 'rank_date_home',\n",
              "       'rank_home', 'country_full_home', 'country_abrv_home',\n",
              "       'total_points_home', 'previous_points_home', 'rank_change_home',\n",
              "       'confederation_home', 'rank_date_away', 'rank_away',\n",
              "       'country_full_away', 'country_abrv_away', 'total_points_away',\n",
              "       'previous_points_away', 'rank_change_away', 'confederation_away'],\n",
              "      dtype='object')"
            ]
          },
          "metadata": {},
          "execution_count": 214
        }
      ],
      "source": [
        "matches.tail().columns"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 215,
      "id": "97c67e7f",
      "metadata": {
        "id": "97c67e7f"
      },
      "outputs": [],
      "source": [
        "matches['score_diff'] = matches['home_score'] - matches['away_score']\n",
        "matches['win'] = matches['score_diff'] > 0 # draw is not win\n",
        "matches['is_stake'] = matches['tournament'] != 'Friendly'\n",
        "matches['rank_diff'] = matches['rank_home'] - matches['rank_away']\n",
        "matches['avg_rank'] = (matches['rank_home'] + matches['rank_away'])/2\n",
        "matches['avg_diff'] = -(matches['total_points_home'] - matches['total_points_away'])/10"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "cdc5f47f",
      "metadata": {
        "id": "cdc5f47f"
      },
      "source": [
        "## 3. Modeling"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 216,
      "id": "b86c6966",
      "metadata": {
        "id": "b86c6966"
      },
      "outputs": [],
      "source": [
        "from sklearn import ensemble\n",
        "from sklearn.model_selection import train_test_split\n",
        "from sklearn.metrics import confusion_matrix, roc_curve, roc_auc_score\n",
        "from sklearn.pipeline import Pipeline\n",
        "from sklearn.preprocessing import PolynomialFeatures\n",
        "from matplotlib import pyplot as plt"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 217,
      "id": "3d8b321d",
      "metadata": {
        "id": "3d8b321d"
      },
      "outputs": [],
      "source": [
        "from xgboost import XGBClassifier\n",
        "from sklearn import linear_model\n",
        "from sklearn.ensemble import GradientBoostingClassifier\n",
        "from sklearn.ensemble import AdaBoostClassifier\n",
        "from sklearn.svm import SVC"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "a5a63f30",
      "metadata": {
        "id": "a5a63f30"
      },
      "source": [
        "### 3.1 Model Selection"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 218,
      "id": "9835d4e4",
      "metadata": {
        "id": "9835d4e4"
      },
      "outputs": [],
      "source": [
        "X, y = matches.loc[:,['avg_rank', 'rank_diff', 'avg_diff', 'is_stake']], matches['win']\n",
        "X_train, X_test, y_train, y_test = train_test_split(\n",
        "    X, y, test_size=0.2, random_state = 42)\n",
        "acc_score = {'model_name' : [], 'score': []}"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 219,
      "id": "9f45d4cd",
      "metadata": {
        "id": "9f45d4cd"
      },
      "outputs": [],
      "source": [
        "clf = linear_model.LogisticRegression(random_state = 42, max_iter = 1000)\n",
        "clf.fit(X_train, y_train)\n",
        "clf_acc = clf.score(X_test, y_test)\n",
        "acc_score['model_name'].append('logistic regression')\n",
        "acc_score['score'].append(clf_acc)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 220,
      "id": "9b0432b0",
      "metadata": {
        "id": "9b0432b0"
      },
      "outputs": [],
      "source": [
        "xgb = XGBClassifier(n_estimators = 100, learning_rate = 0.1)\n",
        "xgb.fit(X_train, y_train)\n",
        "xgb_acc = xgb.score(X_test, y_test)\n",
        "acc_score['model_name'].append('XGB')\n",
        "acc_score['score'].append(xgb_acc)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 221,
      "id": "1086dc3e",
      "metadata": {
        "id": "1086dc3e"
      },
      "outputs": [],
      "source": [
        "gbdt = GradientBoostingClassifier(random_state = 42)\n",
        "gbdt.fit(X_train, y_train)\n",
        "gbdt_acc = gbdt.score(X_test, y_test)\n",
        "acc_score['model_name'].append('GBDT')\n",
        "acc_score['score'].append(gbdt_acc)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 222,
      "id": "799f9623",
      "metadata": {
        "id": "799f9623"
      },
      "outputs": [],
      "source": [
        "ada = AdaBoostClassifier(random_state = 42)\n",
        "ada.fit(X_train, y_train)\n",
        "ada_acc = ada.score(X_test, y_test)\n",
        "acc_score['model_name'].append('ADA')\n",
        "acc_score['score'].append(ada_acc)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 223,
      "id": "b36d7fef",
      "metadata": {
        "id": "b36d7fef"
      },
      "outputs": [],
      "source": [
        "acc_score = pd.DataFrame(acc_score)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 224,
      "id": "0fb0328f",
      "metadata": {
        "id": "0fb0328f"
      },
      "outputs": [],
      "source": [
        "acc_score = acc_score.sort_values(['score'], ascending = False)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 225,
      "id": "9801a22c",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 346
        },
        "id": "9801a22c",
        "outputId": "128ba90b-878d-4cf2-e4a4-ce015eac47ff"
      },
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "text/plain": [
              "<Figure size 216x288 with 1 Axes>"
            ],
            "image/png": "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\n"
          },
          "metadata": {
            "needs_background": "light"
          }
        }
      ],
      "source": [
        "plt.figure(figsize=(3,4))\n",
        "plt.bar(acc_score['model_name'], acc_score['score'])\n",
        "plt.xticks(rotation = 90)\n",
        "plt.show()"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "a3243f71",
      "metadata": {
        "id": "a3243f71"
      },
      "source": [
        "Best accuracy is lositic regression for this data"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "cac41711",
      "metadata": {
        "id": "cac41711"
      },
      "source": [
        "### 3.2 Performance of Model "
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 226,
      "id": "bad23173",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 324
        },
        "id": "bad23173",
        "outputId": "4db30522-d45f-4331-d7ec-733759a35856"
      },
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "text/plain": [
              "<Figure size 1080x360 with 3 Axes>"
            ],
            "image/png": "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\n"
          },
          "metadata": {
            "needs_background": "light"
          }
        }
      ],
      "source": [
        "clf = linear_model.LogisticRegression()\n",
        "\n",
        "features = PolynomialFeatures(degree=2)\n",
        "model = Pipeline([\n",
        "    ('polynomial_features', features),\n",
        "    ('logistic_regression', clf)\n",
        "])\n",
        "model = model.fit(X_train, y_train)\n",
        "\n",
        "# figures \n",
        "fpr, tpr, _ = roc_curve(y_test, model.predict_proba(X_test)[:,1])\n",
        "plt.figure(figsize=(15,5))\n",
        "ax = plt.subplot(1,3,1)\n",
        "ax.plot([0, 1], [0, 1], 'k--')\n",
        "ax.plot(fpr, tpr)\n",
        "ax.set_title('AUC score is {0:0.3}%'.format(100 * roc_auc_score(y_test, model.predict_proba(X_test)[:,1])))\n",
        "ax.set_aspect(1)\n",
        "\n",
        "ax = plt.subplot(1,3,2)\n",
        "cm = confusion_matrix(y_test, model.predict(X_test))\n",
        "ax.imshow(cm, cmap='Greens', clim = (0, cm.max())) \n",
        "\n",
        "ax.set_xlabel('Predicted label')\n",
        "ax.set_title('Performance on the Test set')\n",
        "\n",
        "ax = plt.subplot(1,3,3)\n",
        "cm = confusion_matrix(y_train, model.predict(X_train))\n",
        "ax.imshow(cm, cmap='Blues', clim = (0, cm.max())) \n",
        "ax.set_xlabel('Predicted label')\n",
        "ax.set_title('Performance on the Training set')\n",
        "pass"
      ]
    },
    {
      "cell_type": "markdown",
      "id": "0863e7bc",
      "metadata": {
        "id": "0863e7bc"
      },
      "source": [
        "## 4. Simulation"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 227,
      "id": "4ae0f315",
      "metadata": {
        "id": "4ae0f315"
      },
      "outputs": [],
      "source": [
        "wc_score = wc_score.set_index('country_name')"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 228,
      "id": "dea81cbb",
      "metadata": {
        "id": "dea81cbb"
      },
      "outputs": [],
      "source": [
        "wc_score['country_abrv'] = ['BRA', 'BEL', 'ARG', 'FRA', 'ENG', 'ESP', 'NED', 'POR', 'DEN', 'GER', 'CRO', 'MEX',\n",
        "                            'URU','SUI', 'USA', 'SEN', 'WAL', 'IRN', 'SER','MAR', 'JPN', 'POL', 'KOR', 'TUN',\n",
        "                           'CRC', 'AUS', 'CAN', 'CMR', 'ECU', 'QAT', 'KSA', 'GHA']"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 229,
      "id": "940ffff3",
      "metadata": {
        "id": "940ffff3"
      },
      "outputs": [],
      "source": [
        "from itertools import combinations\n",
        "margin = 0.05\n",
        "groups['points'] = 0\n",
        "groups['total_prob'] = 0\n",
        "groups = groups.set_index('Team')\n",
        "opponents = ['First match \\nagainst', 'Second match\\n against', 'Third match\\n against']"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 230,
      "id": "29c3c1f3",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "29c3c1f3",
        "outputId": "ca5f8a7d-d33e-4c24-baba-fcea8ec0a100"
      },
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "{'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'}"
            ]
          },
          "metadata": {},
          "execution_count": 230
        }
      ],
      "source": [
        "set(groups['Group'])"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 231,
      "id": "fe7cdbee",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "fe7cdbee",
        "outputId": "250e00bc-47fb-40a2-c067-46ebf838c28b"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "----------------------Group C----------------------\n",
            "Argentina vs. Saudi Arabia: Argentina wins with 0.76\n",
            "Argentina vs. Mexico: Argentina wins with 0.58\n",
            "Argentina vs. Poland: Argentina wins with 0.67\n",
            "Saudi Arabia vs. Mexico: Mexico wins with 0.79\n",
            "Saudi Arabia vs. Poland: Poland wins with 0.69\n",
            "Mexico vs. Poland: Mexico wins with 0.58\n",
            "----------------------Group H----------------------\n",
            "Uruguay vs. South Korea: Uruguay wins with 0.56\n",
            "Uruguay vs. Portugal: Portugal wins with 0.56\n",
            "Uruguay vs. Ghana: Uruguay wins with 0.77\n",
            "South Korea vs. Portugal: Portugal wins with 0.71\n",
            "South Korea vs. Ghana: South Korea wins with 0.68\n",
            "Portugal vs. Ghana: Portugal wins with 0.80\n",
            "----------------------Group D----------------------\n",
            "Denmark vs. Tunisia: Denmark wins with 0.63\n",
            "Denmark vs. France: France wins with 0.59\n",
            "Denmark vs. Australia: Denmark wins with 0.68\n",
            "Tunisia vs. France: France wins with 0.73\n",
            "Tunisia vs. Australia: Draw\n",
            "France vs. Australia: France wins with 0.73\n",
            "----------------------Group B----------------------\n",
            "Iran vs. England: England wins with 0.67\n",
            "Iran vs. USA: USA wins with 0.57\n",
            "Iran vs. Wales: Draw\n",
            "England vs. USA: England wins with 0.58\n",
            "England vs. Wales: England wins with 0.61\n",
            "USA vs. Wales: Draw\n",
            "----------------------Group F----------------------\n",
            "Morocco vs. Croatia: Croatia wins with 0.68\n",
            "Morocco vs. Belgium: Belgium wins with 0.77\n",
            "Morocco vs. Canada: Morocco wins with 0.58\n",
            "Croatia vs. Belgium: Belgium wins with 0.60\n",
            "Croatia vs. Canada: Croatia wins with 0.56\n",
            "Belgium vs. Canada: Belgium wins with 0.67\n",
            "----------------------Group E----------------------\n",
            "Germany vs. Japan: Germany wins with 0.57\n",
            "Germany vs. Spain: Draw\n",
            "Germany vs. Costa Rica: Germany wins with 0.63\n",
            "Japan vs. Spain: Spain wins with 0.70\n",
            "Japan vs. Costa Rica: Draw\n",
            "Spain vs. Costa Rica: Spain wins with 0.66\n",
            "----------------------Group A----------------------\n",
            "Senegal vs. Qatar: Senegal wins with 0.65\n",
            "Senegal vs. Netherlands: Netherlands wins with 0.63\n",
            "Senegal vs. Ecuador: Senegal wins with 0.64\n",
            "Qatar vs. Netherlands: Netherlands wins with 0.82\n",
            "Qatar vs. Ecuador: Ecuador wins with 0.56\n",
            "Netherlands vs. Ecuador: Netherlands wins with 0.73\n",
            "----------------------Group G----------------------\n",
            "Switzerland vs. Cameroon: Switzerland wins with 0.65\n",
            "Switzerland vs. Brazil: Brazil wins with 0.63\n",
            "Switzerland vs. Serbia: Draw\n",
            "Cameroon vs. Brazil: Brazil wins with 0.82\n",
            "Cameroon vs. Serbia: Serbia wins with 0.69\n",
            "Brazil vs. Serbia: Brazil wins with 0.66\n"
          ]
        }
      ],
      "source": [
        "for group in set(groups['Group']):\n",
        "    print('----------------------Group {}----------------------'.format(group))\n",
        "    for home, away in combinations(groups.query('Group == \"{}\"'.format(group)).index, 2):\n",
        "        print(\"{} vs. {}: \".format(home, away), end='')\n",
        "        row = pd.DataFrame(np.array([[np.nan, np.nan, np.nan, True]]), columns=X_test.columns)\n",
        "        #row = row.fillna(0)\n",
        "        home_rank = wc_score.loc[home, 'current_rank']\n",
        "        home_avg = wc_score.loc[home, 'avgRank']\n",
        "        opp_rank = wc_score.loc[away, 'current_rank']\n",
        "        opp_avg = wc_score.loc[away, 'avgRank']\n",
        "        row['avg_rank'] = (home_rank + opp_rank) / 2\n",
        "        row['rank_diff'] = home_rank - opp_rank\n",
        "        row['avg_diff'] = home_avg - opp_avg\n",
        "        home_win_prob = model.predict_proba(row)[:,1][0]\n",
        "        groups.loc[home, 'total_prob'] += home_win_prob\n",
        "        groups.loc[away, 'total_prob'] += 1-home_win_prob\n",
        "        \n",
        "        points = 0\n",
        "        if home_win_prob <= 0.5 - margin:\n",
        "            print(\"{} wins with {:.2f}\".format(away, 1-home_win_prob))\n",
        "            groups.loc[away, 'points'] += 3\n",
        "        if home_win_prob > 0.5 - margin:\n",
        "            points = 1\n",
        "        if home_win_prob >= 0.5 + margin:\n",
        "            points = 3\n",
        "            groups.loc[home, 'points'] += 3\n",
        "            print(\"{} wins with {:.2f}\".format(home, home_win_prob))\n",
        "        if points == 1:\n",
        "            print(\"Draw\")\n",
        "            groups.loc[home, 'points'] += 1\n",
        "            groups.loc[away, 'points'] += 1"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 232,
      "id": "98adfd9f",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "98adfd9f",
        "outputId": "fd40f5fc-fed2-4e7f-c00b-1c56c0996775"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "----------------------Round_of_16----------------------\n",
            "Netherlands vs. USA: Netherlands wins with probability 0.56\n",
            "Argentina vs. Denmark: Argentina wins with probability 0.57\n",
            "Spain vs. Croatia: Spain wins with probability 0.53\n",
            "Brazil vs. Uruguay: Brazil wins with probability 0.59\n",
            "Senegal vs. England: England wins with probability 0.62\n",
            "Mexico vs. France: France wins with probability 0.58\n",
            "Germany vs. Belgium: Belgium wins with probability 0.58\n",
            "Switzerland vs. Portugal: Portugal wins with probability 0.56\n",
            "\n",
            "\n",
            "----------------------Quarterfinal----------------------\n",
            "Netherlands vs. Argentina: Argentina wins with probability 0.55\n",
            "Spain vs. Brazil: Brazil wins with probability 0.55\n",
            "England vs. France: France wins with probability 0.51\n",
            "Belgium vs. Portugal: Belgium wins with probability 0.54\n",
            "\n",
            "\n",
            "----------------------Semifinal----------------------\n",
            "Argentina vs. Brazil: Brazil wins with probability 0.52\n",
            "France vs. Belgium: Belgium wins with probability 0.52\n",
            "\n",
            "\n",
            "----------------------Final----------------------\n",
            "Brazil vs. Belgium: Brazil wins with probability 0.50\n",
            "\n",
            "\n"
          ]
        }
      ],
      "source": [
        "pairing = [0, 3, 4, 7, 8, 11, 12, 15, 1, 2, 5, 6, 9, 10, 13, 14]\n",
        "\n",
        "groups = groups.sort_values(by=['Group', 'points', 'total_prob'], ascending=False).reset_index()\n",
        "next_round_wc = groups.groupby('Group').nth([0, 1]) # select the top 2\n",
        "next_round_wc = next_round_wc.reset_index()\n",
        "next_round_wc = next_round_wc.loc[pairing]\n",
        "next_round_wc = next_round_wc.set_index('Team')\n",
        "\n",
        "finals = ['Round_of_16', 'Quarterfinal', 'Semifinal', 'Final']\n",
        "\n",
        "labels = list()\n",
        "odds = list()\n",
        "\n",
        "for f in finals:\n",
        "    print(\"----------------------{}----------------------\".format(f))\n",
        "    iterations = int(len(next_round_wc) / 2)\n",
        "    winners = []\n",
        "\n",
        "    for i in range(iterations):\n",
        "        home = next_round_wc.index[i*2]\n",
        "        away = next_round_wc.index[i*2+1]\n",
        "        print(\"{} vs. {}: \".format(home,\n",
        "                                   away), \n",
        "                                   end='')\n",
        "        row = pd.DataFrame(np.array([[np.nan, np.nan, np.nan, True]]), columns=X_test.columns)\n",
        "        home_rank = wc_score.loc[home, 'current_rank']\n",
        "        avgRank = wc_score.loc[home, 'avgRank']\n",
        "        opp_rank = wc_score.loc[away, 'current_rank']\n",
        "        opp_avg = wc_score.loc[away, 'avgRank']\n",
        "        row['avg_rank'] = (home_rank + opp_rank) / 2\n",
        "        row['rank_diff'] = home_rank - opp_rank\n",
        "        row['avg_diff'] = home_avg - opp_avg\n",
        "        home_win_prob = model.predict_proba(row)[:,1][0]\n",
        "        if model.predict_proba(row)[:,1] <= 0.5:\n",
        "            print(\"{0} wins with probability {1:.2f}\".format(away, 1-home_win_prob))\n",
        "            winners.append(away)\n",
        "        else:\n",
        "            print(\"{0} wins with probability {1:.2f}\".format(home, home_win_prob))\n",
        "            winners.append(home)\n",
        "\n",
        "        labels.append(\"{}({:.2f}) vs. {}({:.2f})\".format(wc_score.loc[home, 'country_abrv'], \n",
        "                                                        1/home_win_prob, \n",
        "                                                        wc_score.loc[away, 'country_abrv'], \n",
        "                                                        1/(1-home_win_prob)))\n",
        "        odds.append([home_win_prob, 1-home_win_prob])\n",
        "                \n",
        "    next_round_wc = next_round_wc.loc[winners]\n",
        "    print(\"\\n\")"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "## 5. Visualization of result"
      ],
      "metadata": {
        "id": "x1ZZntj50CYI"
      },
      "id": "x1ZZntj50CYI"
    },
    {
      "cell_type": "code",
      "source": [
        "# ## using graphviz \n",
        "# !apt-get -qq install -y graphviz && pip install -q pydot\n",
        "# import pydot\n",
        "# ## Those are not necessary but for the safe compile \n",
        "# !apt-get install graphviz libgraphviz-dev pkg-config\n",
        "# !pip install pygraphviz"
      ],
      "metadata": {
        "id": "_zZG3DvF05KM"
      },
      "id": "_zZG3DvF05KM",
      "execution_count": 233,
      "outputs": []
    },
    {
      "cell_type": "code",
      "execution_count": 234,
      "id": "3513641c",
      "metadata": {
        "id": "3513641c"
      },
      "outputs": [],
      "source": [
        "import networkx as nx\n",
        "import pydot\n",
        "from networkx.drawing.nx_pydot import graphviz_layout"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 235,
      "id": "83269a10",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 596
        },
        "id": "83269a10",
        "outputId": "74b20585-29a6-4da5-ec94-84040462605a"
      },
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "text/plain": [
              "<Figure size 720x720 with 1 Axes>"
            ],
            "image/png": "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GzdubJQz7tSpU/D5fO1aVmsKPlN/w09GRkab0pMo7r4bwYICBI8fB8JMnNuNVArr449D2sJ9kSwkXPDwhe0qKytDMgw3JOu2m1F35AjKvv42pqKHYhjI09MxePnLbbrBtFothgwZgiFDhgjfORwOoaozL4IKCwtblS68Nfzzn//EoEGDMHToUDAMg1WrVqGurk7w02mOq666Cm+88YYgbGprazFmzBj85S9/iSi89ZlnnsHq1auxbdu2Rj407777bojVZPLkybj22msxq4EZdMuWLbi1GS//q666CrfccguWLFmCqVOnCgJ5165dYFkWgwcPhlKphEwma1O9Mb7QqVwuR1ZWVpP7zJw5E48++ig+++wzHDhwAL1798Z3330Xss+wYcOwZs0a3HXXXY36FKgPVecjFP1+PzweT9gaaRdeeCHeeustIRx6xYoVGDBggLCdr7/FsiwCgQA8Hg8YhhHKk2zZsqVVPj9dkezsbEydOhWvvPIK+vfv3+rjA4EAjhw5gqVLl6K0tBT33XcfgHqn4ezsbOzcuVOYGK1atQoPPfQQvvvuu7D3GM+pU6cE62VTfm8tnevUqVOoqqpq1qo6ffp0PPvssygqKsK3334rfP+f//wHF198seD4TFFURM9Ufn4+Hn300ZD27ty5E9ddd13YYIcHHngAs2fPxpw5c6DT6fDoo49i7ty54DgOY8aMgVKpxL59+0JSCFx11VW4/vrrQ87T0rPQkAsvvBArV67EqFGjoFAokJeXB5vNJgRT3HHHHTh48CC+/vrrJstEbNmyBZdddlm78jvp9fqQEkQ5OTlITU2NWu41SiaDatky1N15J9jiYiDaKT+kUmjvvReGa6+N7nljSOIT3QDC7JMNk0OAoigM/MeTsFw2KmZOzBTDQNEtAxetegeMShW186pUKsEc+cQTT+A///lPiDly/Pjx6NWrV6tf0OPHjw/JDzJp0iQA9ebPBQsWwGq1wmQy4bXXXsOHH37Y4uDKn7NhivOPP/4Yu3btwjvvvBNyrRMnTgCoH3AbOvI99NBDOHHiBLKzs4V9n376aQD1SypWq1X4SCQSIfIIAE6fPo0DBw40mgU2RCqVYvLkyfj6668FXwOgXpjddttt0Ov16N69O4xGo5D35umnn27xhT9w4ECoVCro9Xrk5+fj448/DluGQCKR4O6778YTTzyB/Px8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\n"
          },
          "metadata": {}
        }
      ],
      "source": [
        "node_sizes = pd.DataFrame(list(reversed(odds)))\n",
        "scale_factor = 0.3 # for visualization\n",
        "G = nx.balanced_tree(2, 3)\n",
        "pos = nx.nx_agraph.graphviz_layout(G, prog='twopi', args='')\n",
        "centre = pd.DataFrame(pos).mean(axis=1).mean()\n",
        "\n",
        "plt.figure(figsize=(10, 10))\n",
        "ax = plt.subplot(1,1,1)\n",
        "# add circles \n",
        "circle_positions = [(235, 'black'), (180, 'blue'), (120, 'red'), (60, 'yellow')]\n",
        "[ax.add_artist(plt.Circle((centre, centre), \n",
        "                          cp, color='grey', \n",
        "                          alpha=0.2)) for cp, c in circle_positions]\n",
        "\n",
        "# draw first the graph\n",
        "nx.draw(G, pos, \n",
        "        node_color=node_sizes.diff(axis=1)[1].abs().pow(scale_factor), \n",
        "        node_size=node_sizes.diff(axis=1)[1].abs().pow(scale_factor)*2000, \n",
        "        alpha=1, \n",
        "        cmap='Reds',\n",
        "        edge_color='black',\n",
        "        width=10,\n",
        "        with_labels=False)\n",
        "\n",
        "# draw the custom node labels\n",
        "shifted_pos = {k:[(v[0]-centre)*0.9+centre,(v[1]-centre)*0.9+centre] for k,v in pos.items()}\n",
        "nx.draw_networkx_labels(G, \n",
        "                        pos=shifted_pos, \n",
        "                        bbox=dict(boxstyle=\"round,pad=0.3\", fc=\"white\", ec=\"black\", lw=.5, alpha=1),\n",
        "                        labels=dict(zip(reversed(range(len(labels))), labels)))\n",
        "\n",
        "texts = ((10, 'Best 16', 'black'), (70, 'Quarter-\\nfinal', 'blue'), (130, 'Semifinal', 'red'), (190, 'Final', 'yellow'))\n",
        "[plt.text(p, centre+20, t, \n",
        "          fontsize=12, color='grey', \n",
        "          va='center', ha='center') for p,t,c in texts]\n",
        "plt.axis('equal')\n",
        "plt.title('2022 Qatar World Cup Simulation', fontsize=20)\n",
        "plt.show()"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "<strong>The Winner of my 2022 Qatar World Cup Simulation is Brazil"
      ],
      "metadata": {
        "id": "VwcSuOvO8mWX"
      },
      "id": "VwcSuOvO8mWX"
    }
  ],
  "metadata": {
    "kernelspec": {
      "display_name": "Python 3 (ipykernel)",
      "language": "python",
      "name": "python3"
    },
    "language_info": {
      "codemirror_mode": {
        "name": "ipython",
        "version": 3
      },
      "file_extension": ".py",
      "mimetype": "text/x-python",
      "name": "python",
      "nbconvert_exporter": "python",
      "pygments_lexer": "ipython3",
      "version": "3.9.13"
    },
    "colab": {
      "provenance": [],
      "include_colab_link": true
    }
  },
  "nbformat": 4,
  "nbformat_minor": 5
}
