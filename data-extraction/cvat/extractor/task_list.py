from cvat_sdk.api_client import Configuration, ApiClient


class TaskList:
    def __init__(self):
        self.configuration: Configuration = None
        self.api_client: ApiClient = None
        self.org = None
        self.sleep_time = 1
        self.should_download_images = False
        self.tasks: list[int] = None
        self.batched_tasks: list[list[int]] = None

    def with_user(self, cvat_url, username, password, organization):
        self.configuration = Configuration(
            host=cvat_url,
            username=username,
            password=password,
        )
        self.org = organization
        self.api_client = ApiClient(self.configuration)
        return self

    def update(self):
        page = 1
        page_size = 100
        task_ids = []

        while True:
            (data, response) = self.api_client.tasks_api.list(
                page=page,
                org=self.org,
                page_size=page_size
            )
            task_ids.extend(task["id"] for task in data["results"])

            if not data["next"]:
                break
            page += 1

        self.tasks = task_ids
        return self

    def batched_on(self, size=4):
        self.batched_tasks = [self.tasks[i:i + size] for i in range(0, len(self.tasks), size)]
        return self

    def load_from(self, path):
        task_array = []

        with open(path, "r") as file:
            for line in file:
                task_array.extend(map(int, line.split()))

        self.tasks = task_array
        return self

    def save_to(self, path):
        with open(path, "w") as file:
            for sublist in self.batched_tasks:
                file.write(" ".join(map(str, sublist)) + "\n")
        return self
