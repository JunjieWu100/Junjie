{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyOMc4bzFwaETrRLH06Q9yRE",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/JunjieWu100/Junjie/blob/main/Betting_odds.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 2,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "waOxnyENDN7U",
        "outputId": "e6b6706d-6955-4858-eaa6-f22dc0b53a8a"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Odds: [1.56, 4.8, 6.9]\n",
            "Bookmaker Margin: -0.57%\n",
            "Interpretation: Arbitrage opportunity! Margin is -0.57%.\n"
          ]
        }
      ],
      "source": [
        "# Betting Odds Fairness Checker\n",
        "\n",
        "def implied_probability(odds):\n",
        "    \"\"\"Convert decimal odds to implied probability.\"\"\"\n",
        "    return 1 / odds\n",
        "\n",
        "def calculate_margin(odds_list):\n",
        "    \"\"\"\n",
        "    Calculate the bookmaker margin.\n",
        "    Positive = unfair (bookmaker edge), 0 = fair, Negative = arbitrage.\n",
        "    \"\"\"\n",
        "    total_implied_prob = sum(implied_probability(o) for o in odds_list)\n",
        "    margin = (total_implied_prob - 1) * 100  # percentage\n",
        "    return round(margin, 2)\n",
        "\n",
        "def interpret_margin(margin):\n",
        "    if margin == 0:\n",
        "        return \"Fair odds (no margin).\"\n",
        "    elif margin > 0:\n",
        "        return f\"Unfair odds. Bookmaker margin is {margin}%.\"\n",
        "    else:\n",
        "        return f\"Arbitrage opportunity! Margin is {margin}%.\"\n",
        "\n",
        "# Example: Replace with your own odds\n",
        "odds = [1.56, 4.8, 6.9]\n",
        "\n",
        "# Run calculations\n",
        "margin = calculate_margin(odds)\n",
        "interpretation = interpret_margin(margin)\n",
        "\n",
        "# Output results\n",
        "print(f\"Odds: {odds}\")\n",
        "print(f\"Bookmaker Margin: {margin}%\")\n",
        "print(f\"Interpretation: {interpretation}\")\n",
        "\n"
      ]
    }
  ]
}