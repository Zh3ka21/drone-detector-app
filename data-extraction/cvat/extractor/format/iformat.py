from abc import ABC, abstractmethod
import zipfile

from .data.idata import IData


class IFormatter(ABC):
    TYPE = "None"

    @abstractmethod
    def formatting(self, zip_data: zipfile.ZipFile) -> IData:
        pass
