import os.path

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure


def plot_accessibility(columns: list[str], relevant_series: list[pd.Series]):
    accessibility_column: str = 'Wie zugänglich sind für Sie Informationen über Transparenz und Verlässlichkeit von Online-Quellen?'
    accessibility_values: list[str] = []
    relevant_indices: list[int] = [columns.index(accessibility_column) + 1]
    # every "unnamed" column directly after our target column contains one of the possible answers
    while True:
        next_idx: int = relevant_indices[-1] + 1
        if not columns[next_idx].startswith("Unnamed"):
            break
        relevant_indices.append(next_idx)
    for rs in relevant_series:
        for idx in relevant_indices:
            if not pd.isna(rs.values[idx]):
                accessibility_values.append(rs.values[idx])
                break
    keys, counts = np.unique(accessibility_values, return_counts=True)
    sort_list: list[str] = [
        "überhaupt nicht zugänglich", "nicht zugänglich", "teilweise zugänglich", "zugänglich", "sehr zugänglich"]
    sort_list_en: list[str] = [
        "not accessible at all", "not accessible", "partially accessible", "accessible", "very accessible"]
    zipped: list[tuple[str, int]] = list(zip(keys, counts))
    zipped.sort(key=lambda x: sort_list.index(x[0]))
    zipped.insert(0, (sort_list[0], 0))
    ax: Axes
    fig: Figure
    fig, ax = plt.subplots()
    rects = ax.bar(list(range(len(zipped))), [x[1] for x in zipped])
    for i in range(len(rects)):
        height = rects[i].get_height()
        ax.text(rects[i].get_x() + rects[i].get_width() / 2, height, sort_list_en[i].replace(" ", "\n"), ha="center",
                va="bottom")
    # hide x axis ticks and labels
    ax.tick_params(axis="x", which="both", labelbottom=False, top=False, bottom=False)
    # make room for the label of the largest bar
    plt.ylim(top=max(counts) + 5)
    plt.ylabel("Count")
    plt.xlabel("Response")
    plt.title("How accessible for you is information\nabout transparency and reliability of online sources?")
    fig.savefig(os.path.join(images_folder, "accessibility_of_information_about_transparency.png"), dpi=600)
    plt.show()


def plot_source_usage(interview_data: pd.DataFrame):
    columns: list[str] = interview_data.columns.to_list()
    relevant_columns: list[str] = columns[1:10]
    source_values: list[str] = []
    for idx, series in interview_data.iterrows():
        for relevant_column in relevant_columns:
            if not pd.isna(series[relevant_column]):
                source_values.append(series[relevant_column])
    keys, counts = np.unique(source_values, return_counts=True)
    sort_list_en: list[str] = [
        "social networks (like Face- book, Twitter etc.)", "conver- sations with friends and relatives",
        "online search engine (e.g. Google)", "public service television (ARD, ZDF etc.)",
        "private television channels (RTL, Pro7, etc.)", "podcasts (e.g. BBC World News)",
        "supraregional newspapers / news agencies (digital & analog)", "local news- papers (digital & analog",
        "radio (e.g. Deutschlandfunk)"]
    zipped: list[tuple[str, int]] = list(zip(keys, counts))
    zipped.sort(key=lambda x: relevant_columns.index(x[0]))
    ax: Axes
    fig: Figure
    fig, ax = plt.subplots()
    rects = ax.bar(list(range(len(zipped))), [x[1] for x in zipped])
    for i in range(len(rects)):
        height = rects[i].get_height()
        ax.text(rects[i].get_x() + rects[i].get_width() / 2, height, sort_list_en[i].replace(" ", "\n"), ha="center",
                va="bottom")
    # hide x axis ticks and labels
    ax.tick_params(axis="x", which="both", labelbottom=False, top=False, bottom=False)
    # make room for the label of the largest bar
    plt.ylim(top=max(counts) + 5)
    plt.ylabel("Count")
    plt.xlabel("Response")
    title: str = "Which sources do you use most frequently [to inform yourself\nabout various issues regarding the current COVID-19 crisis]?"
    plt.title(title)
    fig.savefig(os.path.join(images_folder, "source_usage.png"), dpi=600)
    plt.show()


second_study_folder: str = os.path.abspath("2nd-usability-study")
first_study_folder: str = os.path.abspath("1st-usability-study")
survey_data_path: str = os.path.join(second_study_folder, "survey_data.csv")
interview_data_path: str = os.path.join(first_study_folder, "interview_data.csv")
images_folder: str = os.path.abspath("images")
# # read the data file
# survey_data: pd.DataFrame = pd.read_csv(survey_data_path)
# desc_key: str = "collector_description"
# # choose only the data from SurveyMonkey, not from internal responses
# relevant_series: list[pd.Series] = [series for idx, series in survey_data.iterrows() if series[desc_key] == "broad-audience"]
# columns: list[str] = survey_data.columns.to_list()
# plot_accessibility(columns, relevant_series)
interview_data: pd.DataFrame = pd.read_csv(interview_data_path)
plot_source_usage(interview_data)
