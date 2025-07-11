import pandas as pd
import numpy as np

def main():
    df = pd.read_csv("Energy Awareness in HPC_September 16, 2024_12.48.csv")

    # Drop columns that we don't want reported
    info_columns = [
        "StartDate",
        "EndDate",
        "Status",
        "IPAddress", # Collected inadvertantly
        "Duration (in seconds)",
        "ResponseId",
        "RecipientLastName", # Blank
        "RecipientFirstName", # Blank
        "RecipientEmail", # Blank
        "ExternalReference",
        "LocationLatitude",
        "LocationLongitude",
        "DistributionChannel",
        "UserLanguage",
    ]
    df = df.drop(info_columns, axis=1)

    #Extract questions
    questions = df.iloc[0, :]

    # Drop column meta-data
    df = df.drop([0,1], axis=0)

    # Filter out data recorded before we distributed the survey - these were internal responses
    df["RecordedDate"] = pd.to_datetime(df["RecordedDate"])
    df = df[df["RecordedDate"] >= pd.to_datetime("2024-8-15")]

    df = df.drop(["RecordedDate",], axis=1)

    numeric_columns = {
        "Progress",
        "Q48_1",
        "Q50_1",
        "Q37_4",
    }

    text_columns = {
        "Q11",
        "Q51",
        "Q45",
        "Q31",
    }

    categorical_columns = set(df.columns) - numeric_columns - text_columns - {"RecordedDate",}

    data = []
    for col in categorical_columns:
        question = questions[col]
        value_counts = df[col].value_counts()
        for response, count in value_counts.items():
            data.append((col, question, response, count))

    for col in numeric_columns:
        question = questions[col]
        mean = df[col].dropna().astype(np.int64).mean()
        data.append((col, question, "<mean>", mean))
        median = df[col].dropna().astype(np.int64).median()
        data.append((col, question, "<median>", median))
        
    aggregate_data = pd.DataFrame.from_records(data, columns=["QuestionId", "Question", "Response", "Count"])
    aggregate_data.to_csv("EnergyAwarenessAggregatedResponses.csv", index=False)

if __name__ == "__main__":
    main()