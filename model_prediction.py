import pandas as pd
import datetime
import argparse
import os

"""
Usage:
/usr/local/bin/python3 /Volumes/SSD/Documents/Code/Py/modelling.py --startdate "2014-01-01" --enddate "2024-12-31" --inputfile "/Volumes/SSD/Documents/Code/QQQ_historical_data.csv" --increment 1000
"""

def main():
    parser = argparse.ArgumentParser(description="Fetch historical stock data.")
    parser.add_argument("--startdate", type=str, help="Start date in YYYY-MM-DD format")
    parser.add_argument("--enddate", type=str, help="End date in YYYY-MM-DD format")
    parser.add_argument("--inputfile", type=str, help="Input file path")
    parser.add_argument("--increment", type=int, help="Weekly Increment")

    max_weeks = 260

    args = parser.parse_args()
    startdate = datetime.datetime.strptime(args.startdate, "%Y-%m-%d").date()
    enddate = datetime.datetime.strptime(args.enddate, "%Y-%m-%d").date()
    inputfile = args.inputfile
    increment = args.increment

    df = pd.read_csv(inputfile)
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    filtered_df = df[(df['Date'] >= startdate) & (df['Date'] <= enddate)].reset_index(drop=True)

    # Add Start Amount, End Amount, and Week columns
    filtered_df['Start Amount'] = 0.0
    filtered_df['End Amount'] = 0.0
    filtered_df['Week'] = filtered_df.index + 1

    # Initialize the first row's Start Amount and End Amount
    filtered_df.loc[filtered_df.index[0], 'Start Amount'] = float(increment)
    filtered_df.loc[filtered_df.index[0], 'End Amount'] = (filtered_df.loc[filtered_df.index[0], 'Start Amount'] * (1 + filtered_df.loc[filtered_df.index[0], 'Change%'] / 100))

    # Calculate Start Amount and End Amount for subsequent rows
    for i in range(1, len(filtered_df)):
        week_count = filtered_df.loc[filtered_df.index[i], 'Week']
        if week_count <= max_weeks:
            print(week_count)
            filtered_df.loc[filtered_df.index[i], 'Start Amount'] = filtered_df.loc[filtered_df.index[i - 1], 'End Amount'] + float(increment)
            filtered_df.loc[filtered_df.index[i], 'End Amount'] = (filtered_df.loc[filtered_df.index[i], 'Start Amount'] * (1 + filtered_df.loc[filtered_df.index[i], 'Change%'] / 100))
        else:
            print(week_count)
            filtered_df.loc[filtered_df.index[i], 'Start Amount'] = filtered_df.loc[filtered_df.index[i - 1], 'End Amount']
            filtered_df.loc[filtered_df.index[i], 'End Amount'] = (filtered_df.loc[filtered_df.index[i], 'Start Amount'] * (1 + filtered_df.loc[filtered_df.index[i], 'Change%'] / 100))

    print(filtered_df.info())

    filtered_df['Start Amount'] = filtered_df['Start Amount'].round(3)
    filtered_df['End Amount'] = filtered_df['End Amount'].round(3)

    savepath = inputfile.replace('.csv', f'_modelling_{startdate}_{enddate}.csv')
    filtered_df.to_csv(savepath, index=False)
    print(f"Modelling data saved to {savepath}")

if __name__ == "__main__":
    main()






