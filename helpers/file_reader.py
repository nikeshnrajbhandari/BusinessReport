import pandas as pd
import os

from config import config_files


def current_client():
    clients = pd.read_csv(os.path.join(config_files, 'All_clients.csv'))
    curr_client = pd.read_csv(os.path.join(config_files, 'Client_list.csv'))

    df_clients_main = pd.DataFrame(clients)
    df_clients_list = pd.DataFrame(curr_client)

    df_curr_client = df_clients_main[df_clients_main.salesforce_id.isin(df_clients_list.salesforce_id)]
    return df_curr_client


def authentication(check_email):
    auth = pd.read_csv(os.path.join(config_files, 'Authentication.csv'))
    df_auth = pd.DataFrame(auth)
    return list(df_auth.loc[df_auth['email'].str.lower() == check_email.lower()]['otp'])


def credentials(check_name):
    cred = pd.read_csv(os.path.join(config_files, 'Credentials.csv'))
    df_cred = pd.DataFrame(cred)
    return df_cred.loc[df_cred['name'].str.lower() == check_name.lower()]['credentails'].to_string(index=False)


if __name__ == '__main__':
    client = current_client().to_dict('records')
    for row in client:
        print(authentication(row['email']))
        print(credentials(row['name']))
