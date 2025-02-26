import geopandas as gpd
import logging
from shapely.geometry import MultiPolygon, Polygon

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def convert_geometry(geom):
    if geom.geom_type == "GeometryCollection":
        polygons = [g for g in geom.geoms if isinstance(g, (Polygon, MultiPolygon))]
        return MultiPolygon(polygons) if polygons else None
    return geom  

def process_data(input_file="desmatamento.geojson", output_file="desmatamento_processado.geojson"):
    logging.info("Carregando dados...")
    gdf = gpd.read_file(input_file)

    if "area_km" in gdf.columns:
        gdf = gdf[["year", "area_km", "geometry"]]
    elif "area_km2" in gdf.columns:
        gdf = gdf[["year", "area_km2", "geometry"]]
    else:
        logging.error("Nenhuma coluna de área encontrada")
        return None

    gdf["geometry"] = gdf["geometry"].apply(convert_geometry)
    gdf = gdf[gdf["geometry"].notnull()]
    gdf.set_crs(epsg=4326, inplace=True)

    gdf.to_file(output_file, driver="GeoJSON")
    logging.info(f"Análise realizada e dados salvos em {output_file}")
    return output_file

if __name__ == "__main__":
    process_data()
