ETL - Desmatamento no Bioma Cerrado
Este projeto implementa um pipeline ETL para os dados de desmatamento do bioma Cerrado, extraídos do GeoServer do TerraBrasilis. O objetivo final é armazenar os dados em um banco PostgreSQL/PostGIS, permitindo consultas geoespaciais otimizadas.
Estrutura do Projeto:
etl-desmatamento/
 ├── GeoServerWFS.py
 ├── Processamento_Dados.py
 ├── Inserir_Dados.py
 ├── README.md
 ├── Relatorio de desenvolvimento.md
 └── desmatamento.geojson 
Pré-requisitos:
Python 3.8+
PostgreSQL 16+ com PostGIS habilitado
Docker (para rodar o PostgreSQL via container)
Bibliotecas Python (instalar via requirements.txt
Caso use Docker, suba o banco de dados com:
‘docker run --name pg_container -e POSTGRES_USER= -e POSTGRES_PASSWORD= -e POSTGRES_DB= -p 5434:5432 -d postgis/postgis’

Passo a passo:
Passo 1 > Baixar os dados do TerraBrasilis:
‘python GeoServerWFS.py’
Passo 2 > Processar os dados e corrigir geometrias:
‘python Processamento_Dados.py’
Passo 3 > Carregar os dados no PostgreSQL/PostGIS:
‘python Inserir_Dados.py’
Passo 4 > Validar os dados no banco [terminal]:
‘psql -h localhost -p 5434 -U admin -d geodata’
Comandos:
##Contar registros:
‘SELECT COUNT(*) FROM raw_data.deforestation;’

##Verificar SRID (deve ser 4326):
‘SELECT DISTINCT ST_SRID(geometry) FROM raw_data.deforestation;’

##Criar índice espacial para otimizar consultas:
‘CREATE INDEX deforestation_geom_idx ON raw_data.deforestation USING GIST (geometry);’

Exemplos de consultas espaciais no PostgreSQL:
Questão 01: Quantas áreas de desmatamento foram registradas por estado?
SELECT s."SIGLA_UF", COUNT(*) AS total_desmatamento
FROM raw_data.deforestation d
JOIN raw_data.states s
ON ST_Intersects(d.geometry, s.geometry)
GROUP BY s."SIGLA_UF"
ORDER BY total_desmatamento DESC;
Visualização 01: Visualizar uma amostra das geometrias
SELECT year, area_km, ST_AsText(geometry) FROM raw_data.deforestation LIMIT 5;
Possíveis Erros e Soluções

Conclusão
Com esse pipeline, um ETL eficiente e otimizado é processado para análise geoespacial de desmatamento no Cerrado.

