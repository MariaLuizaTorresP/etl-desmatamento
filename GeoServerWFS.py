import requests
import geopandas as gpd
import logging
import time
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class GeoServerDownloader:
    BASE_URL = "https://terrabrasilis.dpi.inpe.br/geoserver"

    def __init__(self, bioma="prodes-cerrado-nb", layer="yearly_deforestation", max_retries=5, max_features=10000):
        self.bioma = bioma
        self.layer = layer
        self.workspace = f"{self.BASE_URL}/{self.bioma}/wfs"
        self.max_retries = max_retries
        self.max_features = max_features

    def build_url(self):
        return f"{self.workspace}?service=WFS&version=1.0.0&request=GetFeature&typeName={self.bioma}:{self.layer}&outputFormat=application/json"

    def download_data(self, output_file="desmatamento.geojson"):
        url = self.build_url()
        retries = 0
        start_index = 0
        max_features = 10000  
        all_gdf = []

        while True:
            try:
                logging.info(f"Baixando dados com startIndex={start_index}, maxFeatures={self.max_features})...")
                params = {
                    "startIndex": start_index,
                    "maxFeatures": max_features
                }
                response = requests.get(url, params=params, timeout=30)
                response.raise_for_status()  
                data = response.json()

                if not data["features"]:
                    logging.info("Todos os dados foram baixados")
                    break 

                gdf = gpd.GeoDataFrame.from_features(data["features"])
                all_gdf.append(gdf)
                start_index += max_features 

            except requests.exceptions.ConnectionError:
                logging.error("Erro de conexão! Novo teste...")
            except requests.exceptions.Timeout:
                logging.warning("Tempo de resposta excedido! Novo teste...")
            except requests.exceptions.HTTPError as e:
                logging.error(f"Erro HTTP {response.status_code}: {e}")
                return None
            retries += 1
            if retries >= self.max_retries:
                logging.error("Falha ao baixar os dados após testes")
                return None
            time.sleep(5)  

        final_gdf = gpd.GeoDataFrame(pd.concat(all_gdf, ignore_index=True))
        final_gdf.to_file(output_file, driver="GeoJSON")
        logging.info(f"Dados salvos em {output_file}")
        return output_file
