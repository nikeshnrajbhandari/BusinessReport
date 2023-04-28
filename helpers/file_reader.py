import os
import logging
import pandas as pd

from helpers.db_info import br_clients_rds
from config import config_files, salesforce_id

logger = logging.getLogger("br_logger")
logger.setLevel(logging.INFO)


def current_client():
    clients = pd.read_csv(os.path.join(config_files, 'All_clients.csv'))
    # curr_client = pd.read_csv(os.path.join(config_files, 'Client_list.csv'))
    curr_client = pd.DataFrame(br_clients_rds())
    # curr_client = [{'ID': '0015000001rCn3RAAS'},
    #                ]
    df_clients_main = pd.DataFrame(clients)
    df_clients_list = pd.DataFrame(curr_client)

    if salesforce_id is not None:

        client_dict = {'salesforce_id': f'{salesforce_id}'}
        curr_client_record = df_clients_main.loc[
            df_clients_main['salesforce_id'] == client_dict.get('salesforce_id')].to_dict('records')
        if len(curr_client_record) == 0:
            logger.info(f"Setting for {client_dict.get('salesforce_id')} not found!")
    else:
        df_no_setting = df_clients_list[~df_clients_list.ID.isin(df_clients_main.salesforce_id)]
        if len(df_no_setting) != 0:
            logger.warning('No setting for following:')
            logger.warning(df_no_setting.to_dict('records'))
        df_curr_client = df_clients_main[df_clients_main.salesforce_id.isin(df_clients_list.ID)]
        curr_client_record = df_curr_client.to_dict('records')
    return curr_client_record


def authentication(check_email):
    auth = pd.read_csv(os.path.join(config_files, 'Authentication.csv'))
    df_auth = pd.DataFrame(auth)
    return list(df_auth.loc[df_auth['email'].str.lower() == check_email.lower()]['otp'])


def credentials(check_name):
    cred = pd.read_csv(os.path.join(config_files, 'Credentials.csv'))
    df_cred = pd.DataFrame(cred)
    return df_cred.loc[df_cred['name'].str.lower() == check_name.lower()]['credentials'].to_string(index=False)


if __name__ == '__main__':
    current_client()
    # client = current_client().to_dict('records')
    # for row in client:
    #     print(row['email'] + " " + row['name'])
    #     print(authentication(row['email']))
    #     print(credentials(row['name']))
    pass
