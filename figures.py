import os.path

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# read the data file
from matplotlib.axes import Axes

second_study_folder: str = os.path.abspath("2nd-usability-study")
data_path: str = os.path.join(second_study_folder, "survey_data.csv")
data: pd.DataFrame = pd.read_csv(data_path)
desc_key: str = "collector_description"
# choose only the data from SurveyMonkey, not from internal responses
relevant_series: list[pd.Series] = [series for idx, series in data.iterrows() if series[desc_key] == "broad-audience"]
columns: list[str] = data.columns.to_list()
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
sort_list: list[str] = ["überhaupt nicht\n zugänglich", "nicht zugänglich", "teilweise zugänglich", "zugänglich",
                        "sehr zugänglich"]
zipped: list[tuple[str, int]] = list(zip(keys, counts))
zipped.sort(key=lambda x: sort_list.index(x[0]))
zipped.insert(0, (sort_list[0], 0))
# plt.bar([x[0] for x in zipped], [x[1] for x in zipped])
ax: Axes
fig, ax = plt.subplots()
# plt.bar(list(range(len(zipped))), [x[1] for x in zipped])
rects = ax.bar(list(range(len(zipped))), [x[1] for x in zipped])
# ax.bar_label(rects)
for i in range(len(rects)):
    height = rects[i].get_height()
    ax.text(rects[i].get_x() + rects[i].get_width() / 2, height, sort_list[i], ha="center", va="bottom")
ax.xaxis.label.set_visible(False)
# plt.xticks(rotation=30, ha="right")
# plt.subplots_adjust(bottom=0.25, left=0.2)
plt.xticks(list(range(len(zipped))), " ")
plt.show()
a = 0
