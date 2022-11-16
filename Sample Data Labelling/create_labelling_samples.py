import pandas as pd

# import csv file
# input file was generated using the GitHub API via githubCsvTools
# https://github.com/gavinr/github-csv-tools
all_issues = pd.read_csv("./issues.csv", low_memory=False)

# filter for closed issues starting in 2018, and filter out pull requests which are categorized as issues by the API.
closed_issues = all_issues[
    (all_issues["pull_request.url"].isna())
    & (all_issues["state"] == "closed")
    & (pd.to_datetime(all_issues["created_at"]).dt.year >= 2018)
]

# pick specific columns only (There are 111 in the original)
closed_issues = closed_issues[
    [
        "html_url",
        "number",
        "title",
        "labels",
        "state",
        "locked",
        "milestone",
        "comments",
        "created_at",
        "updated_at",
        "closed_at",
        "author_association",
        "state_reason",
        "assignee.login",
        "body",
    ]
]
# add a new column to represent the time_period of the comment (year and month)
closed_issues["time_period"] = pd.to_datetime(closed_issues["created_at"]).dt.to_period(
    "M"
)

# We want 1000 samples. Determine the required fraction out of the total.
fraction = 1000 / len(closed_issues)
# groupby our time_period and sample a proportional sample of each
sample = closed_issues.groupby("time_period", group_keys=False).apply(
    lambda x: x.sample(frac=fraction, random_state=0)
)

# clean up the time_period column and add a new column for each labeller to add their manual classification
sample = sample.drop(columns=["time_period"])
sample.insert(0, "Graeme", "")
sample.insert(0, "Steve", "")
sample.insert(0, "Dave", "")

# export to xlsx
sample.to_excel("ENSF 612 - Label Samples.xlsx", index=False, engine="xlsxwriter")
