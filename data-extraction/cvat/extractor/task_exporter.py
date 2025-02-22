import os
import time
import zipfile
import threading
from concurrent.futures import ThreadPoolExecutor
from http import HTTPStatus
from io import BytesIO

import urllib3
from cvat_sdk.api_client import Configuration, ApiClient

from .format.data.idata import IData
from .format.format_fabric import FormatFabric
from .format.iformat import IFormatter


class TaskExporter:
    def __init__(self, count_thread: int = 4):
        self.format_fabric: FormatFabric = FormatFabric()
        self.formatter: IFormatter = None
        self.configuration: Configuration = None
        self.api_client: ApiClient = None
        self.org = None
        self.thread_pool = ThreadPoolExecutor(max_workers=count_thread)
        self.action = "download"
        self.sleep_time = 1  # seconds
        self.should_download_images = False
        self.lock = threading.Lock()
        self.log_file_path = "error.txt"
        self.max_retries = 20

    def __del__(self):
        self.api_client.close()

    def close_pool(self):
        self.thread_pool.shutdown()

    def __get_response(self, id: int) -> urllib3.HTTPResponse:
        while True:
            (_, response) = self.api_client.tasks_api.retrieve_dataset(
                id=id,
                format=self.formatter.TYPE,
                _parse_response=False,
            )

            if response.status in (HTTPStatus.CREATED, HTTPStatus.OK):
                break

            time.sleep(self.sleep_time)

        if response.status == HTTPStatus.CREATED:
            if self.should_download_images:
                # - POST /api/tasks/<task_id>/dataset/export?save_images=True
                (_, response) = self.api_client.tasks_api.retrieve_dataset(
                    id=id,
                    format=self.formatter.TYPE,
                    action=self.action,
                    _parse_response=False,
                )
            else:            
                # - POST /api/tasks/<task_id>/dataset/export?save_images=False
                (_, response) = self.api_client.tasks_api.retrieve_dataset(
                    id=id,
                    format=self.formatter.TYPE,
                    action=self.action,
                    _parse_response=False,
                )
        return response

    def __get_unzip_output(self, response: urllib3.HTTPResponse) -> IData:
        zip_data = BytesIO(response.data)
        with zipfile.ZipFile(zip_data) as zip:
            return self.formatter.formatting(zip)

    def __download(self, unzip_data: IData, output_dir: str) -> None:
        os.makedirs(output_dir, exist_ok=True)

        labels_dir = os.path.join(output_dir, "labels")
        os.makedirs(labels_dir, exist_ok=True)
        
        if self.should_download_images:
            images_dir = os.path.join(output_dir, "images")
            os.makedirs(images_dir, exist_ok=True)
            unzip_data.download_images(images_dir)

        unzip_data.download_data(labels_dir)

    def export_data(self,
                    task_ids: list[int],
                    output_dir: str = "./", ) -> None:

        def export_helper(export_task_id):
            try:
                task_output_dir = os.path.join(output_dir, f"task_{export_task_id}")
                os.makedirs(task_output_dir, exist_ok=True)
                cvat_output = self.__get_response(export_task_id)
                unzip_data = self.__get_unzip_output(cvat_output)
                self.__download(unzip_data, task_output_dir)
            except Exception as e:
                print(e)
                self.__log_error(export_task_id)

        self.thread_pool.map(export_helper, task_ids)
        # for id in task_ids:
        #    export_helper(id)

    def with_user(self, cvat_url, username, password, organization):
        self.configuration = Configuration(
            host=cvat_url,
            username=username,
            password=password,
        )
        self.org = organization
        self.api_client = ApiClient(self.configuration)
        return self

    def with_format(self, type: str):
        self.formatter = self.format_fabric.create(type)
        return self

    def with_images(self):
        self.should_download_images = not self.should_download_images
        return self

    def __log_error(self, id):
        with self.lock:
            with open(self.log_file_path, "a") as error_file:
                error_file.write(f"{id}\n")
