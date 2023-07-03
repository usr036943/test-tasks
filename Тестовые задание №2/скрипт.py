import pandas as pd
import argparse

def main(path):
    print(path)
    df = pd.read_excel(path)
    df['date'] = df['Date&Time'].dt.date
    df_grouped = df.groupby('date').agg({'qg_sc': ['mean', 'std']})
    df_grouped.columns = ['_'.join(col) for col in df_grouped.columns.values]
    df_grouped = df_grouped.reset_index()
    df = df.merge(df_grouped)
    df['Outlier'] = (
                ~(df.qg_sc > (df.qg_sc_mean - 3 * df.qg_sc_std)) & (df.qg_sc < (df.qg_sc_mean + 3 * df.qg_sc_std))).astype(
        int)
    df[['Date&Time', 'qg_sc', 'Outlier']].to_excel(path, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Outliers detector')
    parser.add_argument('filename')

    args = parser.parse_args()
    main(args.filename)