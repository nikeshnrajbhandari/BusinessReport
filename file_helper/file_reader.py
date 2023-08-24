import os
import logging
import pandas as pd


from db_helper.db_info import Database
from configs.config import client_file, cred_file, auth_file

logger = logging.getLogger("br_logger")
logger.setLevel(logging.INFO)


def current_client(salesforce_id = None):
    clients = pd.read_csv(client_file)
    curr_client = pd.DataFrame(Database().br_clients_rds())
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
    df_auth = pd.read_csv(auth_file)
    return list(df_auth.loc[df_auth['email'].str.lower() == check_email.lower()]['otp'])


def credentials(check_name):
    df_cred = pd.read_csv(cred_file)
    return df_cred.loc[df_cred['name'].str.lower() == check_name.lower(), 'credentials'].iloc[0]


if __name__ == '__main__':
    current_client()
