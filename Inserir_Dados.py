from sqlalchemy import create_engine
import geopandas as gpd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

DB_CONNECTION = "postgresql://admin:admin@localhost:5434/geodata"
engine = create_engine(DB_CONNECTION)

logging.info("Carregando dados processados...")
gdf = gpd.read_file("desmatamento_processado.geojson")

logging.info("Inserindo dados na tabela `deforestation`...")
gdf.to_postgis("deforestation", engine, schema="raw_data", if_exists="replace", index=False)

logging.info("Dados carregados no PostgreSQL com sucesso!")
