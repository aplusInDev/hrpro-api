#!/usr/bin/env python3
""" This module defines a function that takes an excel file as input
and returns the file content in JSON serializable format
"""
import pandas as pd
from datetime import datetime



def df_to_json(file):
    """Converts an excel file to a JSON serializable string

    Args:
        file (str): The name of the file to be converted

    Returns:
        str: A JSON serializable string

    Exceptions:
        Exception: If an error occurs while converting the file
    """
    try:
        df = pd.read_excel(file, skiprows=1, usecols="B:F", names=[
            "date", "name", "check_in", "check_out", "absent"])

        for col in df.columns:
            df[col] = df[col].astype(str)
        # convert each row from str to datetime
        df['check_in'] = df['check_in']\
            .apply(lambda x: datetime.strptime(x, '%H:%M:%S').time()
                    if x != "nan" else "00:00:00")
        df['check_out'] = df['check_out']\
            .apply(lambda x: datetime.strptime(x, '%H:%M:%S').time()
                    if x != "nan" else "00:00:00")
        df['absent'] = df['absent']\
            .apply(lambda x: 'No' if x == "False" else 'Yes')

        # Serialize DataFrame to JSON
        df_json = df.to_json(orient='split', date_format='iso')
        return df_json
    except Exception as e:
        print("Error converting DataFrame to JSON", e)
