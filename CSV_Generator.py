import argparse
import pandas as pd
import glob
import os

def merge_csv(pr_directories, ghi_directories):
    PR_df = pd.DataFrame()        # Empty PR dataframe
    GHI_df = pd.DataFrame()       # Empty GHI dataframe
    final_df = pd.DataFrame()     # DataFrame to be saved as CSV
    
    # Adding all PR data to PR_df:
    pr_files = glob.glob(os.path.join(pr_directories, '**', '*.csv'), recursive=True)
    for pr_file in pr_files:
        pr_df = pd.read_csv(pr_file)
        PR_df = pd.concat([PR_df, pr_df], ignore_index=True)

    # Adding all GHI data to GHI_df:
    ghi_files = glob.glob(os.path.join(ghi_directories, '**', '*.csv'), recursive=True)
    for ghi_file in ghi_files:
        ghi_df = pd.read_csv(ghi_file)
        GHI_df = pd.concat([GHI_df, ghi_df], ignore_index=True)

    # Merging the two dataframes into one:
    final_df = pd.merge(PR_df, GHI_df, on='Date')
    final_df = final_df.sort_values(by='Date')

    # Saving the File:
    final_df.to_csv('pv_plant.csv', index=False)
    return final_df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge PR and GHI CSV files into a single CSV file")
    parser.add_argument("--data_directory", type=str, required=True, help="Path to the data directory containing 'pr' and 'ghi' subdirectories")

    args = parser.parse_args()

    pr_directory = os.path.join(args.data_directory, 'pr')
    ghi_directory = os.path.join(args.data_directory, 'ghi')

    merge_csv(pr_directory, ghi_directory)