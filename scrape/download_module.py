import logging

from base_class import DriverInit
from configs import headless
from error_helper.custom_error import NoBusinessReport
from file_helper.file_reader import authentication, credentials
from scrape import Login, Navigation, Scraper


class DownloadModule:
    def __init__(self):
        self.logger = logging.getLogger("br_logger")
        self.logger.setLevel(logging.INFO)

    def br_download(self, client, dates, download_dir, driver_dir):
        if client['active'] == 1:
            driver_init = DriverInit(download_dir, driver_dir, headless)

            try:
                parameters = {
                    "driver": driver_init,
                    "name":client['name'],
                    "email": client['email'],
                    "creds": credentials(client['name']),
                    "otp": authentication(client['email']),
                    "marketplace": client['marketplace_id'],

                }
                Login(**parameters).asc_login()

                parameters = {
                    "driver": driver_init,
                    "name": client['name'],
                    "col1": client['col1'],
                    "col2": client['col2'],
                    "col3": client['col3'],
                }
                Navigation(**parameters).navigate()

                parameters = {
                    "driver": driver_init,
                    "seller_id": client['seller_id'],
                    "marketplace_id": client['marketplace_id'],
                    "name": client['name'],
                    "fraction": client['fraction'],
                    "start_date": dates[0],
                    "end_date": dates[1],
                    "stage_dir": download_dir
                }
                Scraper(**parameters).scrape()

                self.logger.info(f"Download complete for {str(client['name'])}")
            except NoBusinessReport as err:
                # When there is no business report section, will not flag as failed.
                raise
            except Exception as err:
                self.logger.error(f"Failed to download for {str(client['name'])}")
                raise
