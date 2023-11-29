import pandas as pd


def load_event_log(path: str) -> pd.DataFrame:
    """Load the event log from the given path.

    Args:
        path (str): The path to the event log.

    Returns:
        pd.DataFrame: The event log.
    """
    # Load the event log
    df = pd.read_csv(path, sep=',')

    # Convert the time columns to datetime
    df['time:timestamp'] = pd.to_datetime(df['time:timestamp'], format='ISO8601')

    # Get the columns currently stored as objects and remove the columns that are not categorical
    object_columns = df.select_dtypes(include=['object']).columns
    object_columns = object_columns.drop(['concept:name', 'case:concept:name'])

    # Convert the object columns to categorical columns
    df[object_columns] = df[object_columns].astype('category')

    return df
