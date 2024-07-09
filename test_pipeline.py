# test_pipeline.py

import unittest
import pandas as pd
from data_ingestion import fetch_api_data, read_csv_file
from data_processing import clean_and_transform_data

class TestDataPipeline(unittest.TestCase):

    def test_fetch_api_data(self):
        data = fetch_api_data()
        self.assertIsInstance(data, dict)

    def test_read_csv_file(self):
        df = read_csv_file('local_path_to_csv.csv')
        self.assertIsInstance(df, pd.DataFrame)

    def test_clean_and_transform_data(self):
        df = pd.DataFrame({'col1': [1, 2, None], 'col2': [3, 4, 5]})
        df_transformed = clean_and_transform_data(df)
        self.assertFalse(df_transformed.isnull().values.any())

if __name__ == "__main__":
    unittest.main()
