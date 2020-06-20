import pandas as pd
import numpy as np


# A simple function to easily get the data for exchange rates
def set_up():
    # Taking in the most current quarterly rates
    all_data = pd.read_csv('https://www.bis.org/statistics/full_webstats_xru_current_dataflow_csv.zip')

    # Get only the important information
    columns_to_keep = np.array(['CURRENCY', '2020-Q1'])
    all_data = all_data[columns_to_keep].dropna()
    data = pd.DataFrame(columns=['currency', 'rate'])

    i = 0
    for index, row in all_data.iterrows():
        # check if the name is already in the list
        if not any(data['currency'].isin([row['CURRENCY']])):
            append = {'currency': row['CURRENCY'],
                      'rate': row['2020-Q1']}
            data = data.append(append, ignore_index=True)
            i += 1

    return data.set_index('currency')


def show_currencies(data):
    print('That is not a currency we accept.')
    print('Would you like to see a list of currencies we accept? Y/n')
    response = input()
    if response == 'y' or response == 'Y':
        # in writing, the data had 114 sets
        if len(data) == 114:
            print(np.asarray(data.index.to_list()).reshape(19, 6))
        # however, if the data changes in the future, we can still print
        else:
            print(*(data.index.to_list()), sep='\n')
    exit(1)


def main():
    print('Please wait while the program sets up...')
    data = set_up()

    print('Type the three-letter all-caps code for the currency you want to convert from: ')
    convert_from = input()
    if not any(data.index.isin([convert_from])):
        show_currencies(data)

    print('Type the three-letter all-caps code for the currency you want to convert to: ')
    convert_to = input()
    if not any(data.index.isin([convert_to])):
        show_currencies(data)

    print('How much do you have in', convert_from, end='? \n')
    amount = input()
    try:
        amount = float(amount)
    except all:
        print('That is not a number we can convert, input is of type', type(amount))
        exit(2)

    # conversion factor
    factor = data.loc[convert_to] / data.loc[convert_from]
    amount *= factor

    print('You have', "{:.2f}".format(amount.iloc[0]), 'in', convert_to)


if __name__ == "__main__":
    main()
