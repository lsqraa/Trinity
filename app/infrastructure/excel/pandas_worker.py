from __future__ import annotations
from pathlib import Path
from typing import Any
import pandas as pd


class ExcelWorkerError(Exception):
    pass


class FileNotFoundExcelError(ExcelWorkerError):
    pass


class EmptyExcelError(ExcelWorkerError):
    pass


class InvalidExcelError(ExcelWorkerError):
    pass


class PandasWorker:
    def __init__(self, engine: str = "openpyxl") -> None:
        self.engine = engine

    def read_file(self, file_path: str | Path) -> pd.DataFrame:
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundExcelError(f"El archivo especificado no existe: {path}")

        try:
            df = pd.read_excel(path, dtype=str, engine=self.engine)
        except Exception as e:
            raise InvalidExcelError(f"No se pudo procesar el archivo Excel: {e}") from e

        df = df.dropna(how="all")

        if df.empty:
            raise EmptyExcelError(f"El archivo Excel no contiene filas de datos: {path}")

        return df

    def extract_raw_records(self, file_path: str | Path) -> list[dict[str, Any]]:
        df = self.read_file(file_path)
        return df.to_dict(orient="records")

    def get_row_count(self, file_path: str | Path) -> int:
        df = self.read_file(file_path)
        return len(df)
