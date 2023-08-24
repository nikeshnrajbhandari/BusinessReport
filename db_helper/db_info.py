"""Generates clients eligible for Business Report pull"""

import os
import logging
import pymysql.cursors

from dotenv import load_dotenv
from helpers.utils import decrypt_token


class Database:
    def __init__(self):
        self.logger = logging.getLogger("br_logger")
        self.logger.setLevel(logging.INFO)
        load_dotenv()
        conn = pymysql.connect(database=os.environ.get("database"),
                               host=os.environ.get("host"),
                               port=int(os.environ.get("port")),
                               user=decrypt_token(os.environ.get("user")),
                               password=decrypt_token(os.environ.get("password")),
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)
        self.cursor = conn.cursor()

    def br_clients_rds(self):
        try:

            sql = """ 
                    select
                        main.ID
                    from
                        (
                            select
                                A.name as Account_name,
                                A.id as ID,
                                A.active as Active,
                                if(
                                    amazon.amazon_Contracted_Service = 1,
                                    "Yes",
                                    "No"
                                ) as amazon_Contracted_Service,
                                CASE
                                    amazon.amazon_Daily_status
                                    WHEN 4 THEN "Not Used"
                                    WHEN 3 THEN "Turned Off"
                                    WHEN 2 THEN "Access Issue"
                                    WHEN 1 THEN "Configured"
                                    WHEN 0 THEN "Not Configured"
                                    ELSE "N/A"
                                END as amazon_Daily_status,
                                CASE
                                    amazon.amazon_Daily_status
                                    WHEN 1 THEN amazon.amazon_Historical_status
                                    ELSE "N/A"
                                END as amazon_Historical_status
                            from
                                (
                                    select
                                        distinct id,
                                        name,
                                        if(active = 1, "Yes", "No") as active
                                    from
                                        accounts as accounts
                                        left join account_service on account_service.account_id = accounts.id
                                        left join account_user on account_user.account_id = accounts.id
                                    where
                                        CASE
                                            WHEN -1 = -1 Then TRUE
                                            WHEN -1 = 0 Then account_service.account_id not in (
                                                Select
                                                    distinct account_id
                                                from
                                                    account_service
                                                where
                                                    specialist_id != 0
                                            )
                                            ELSE account_service.specialist_id = -1
                                        END
                                        AND accounts.status != 3
                                        AND CASE
                                            WHEN -1 = -1 Then TRUE
                                            WHEN -1 = 0 Then account_user.user_id IS NULL
                                            ELSE account_user.user_id = -1
                                        END
                                        and (
                                            accounts.status = 1
                                            or accounts.status = 4
                                        )
                                ) as A
                                left join (
                                    -- amazon ads -5
                                    SELECT
                                        aa.id,
                                        his.contracted_service amazon_Contracted_Service,
                                        CASE
                                            IFNULL(his.data_source_config_id, 0)
                                            WHEN 0 THEN if(his.contracted_service = 1, 0, -1)
                                            ELSE CASE
                                                his.status
                                                WHEN 1 THEN CASE
                                                    WHEN his.contracted_service = 1 THEN if(his.not_using = 1, 4, 1)
                                                    WHEN his.contracted_service = 0 THEN -1
                                                END
                                                WHEN 0 THEN CASE
                                                    WHEN his.error_message = "API access denied" Then if(his.contracted_service = 1, 2, -1)
                                                    WHEN his.error_message is not null
                                                    and length(his.error_message) Then if(his.contracted_service = 1, 3, -1)
                                                    ELSE if(his.contracted_service = 1, 0, -1)
                                                END
                                                ELSE if(his.contracted_service = 1, his.status, -1)
                                            END
                                        END as amazon_Daily_status,
                                        if(hp.bi_data_source_id = 5, "Present", "In Queue") as amazon_Historical_status
                                    FROM
                                        `account_bi_data_source` his
                                        inner join accounts aa on aa.id = his.account_id
                                        left join account_datasource_historical_data_pull hp on aa.id = hp.account_id
                                        AND his.bi_data_source_id = hp.bi_data_source_id
                                    where
                                        his.bi_data_source_id = 5
                                ) as amazon on A.id = amazon.id
                                left join (
                                    -- Account Status - 1
                                    SELECT
                                        aa.id,
                                        if(IFNULL(his.data_source_config_id, 0) = 0, 0, 1) as astat_Daily_status
                                    FROM
                                        `account_bi_data_source` his
                                        inner join accounts aa on aa.id = his.account_id
                                    where
                                        his.bi_data_source_id = 1
                                ) astat on A.id = astat.id
                            where
                                A.active = "Yes"
                        ) AS main
                    WHERE
                        main.amazon_Contracted_Service = 'Yes'
                        AND main.amazon_Daily_status = 'Configured' --     1 = 1
                    order by
                        lower(account_name) ASC
                    -- limit
                    --     10000 offset 0
                """
            self.cursor.execute(sql)
            clients = (self.cursor.fetchall())
            client_list = []
            for client in clients:
                client_list.append({'ID': client['ID']})
                print(client)
            return client_list

        except pymysql.Error as err:
            self.logger.exception(err)


if __name__ == '__main__':
    pass
