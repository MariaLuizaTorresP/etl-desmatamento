Last login: Wed Feb 26 14:10:29 on ttys010
(base) malutorres@MacBook-Air-de-Maria ~ % nano README.md






















  UW PICO 5.09                    File: README.md                     Modified  

FROM raw_data.deforestation d
JOIN raw_data.states s
ON ST_Intersects(d.geometry, s.geometry)
GROUP BY s."SIGLA_UF"
ORDER BY total_desmatamento DESC;
Visualização 01: Visualizar uma amostra das geometrias
SELECT year, area_km, ST_AsText(geometry) FROM raw_data.deforestation LIMIT 5;
Possíveis Erros e Soluções

Conclusão
Com esse pipeline, um ETL eficiente e otimizado é processado para análise geoes$









^G Get Help  ^O WriteOut  ^R Read File ^Y Prev Pg   ^K Cut Text  ^C Cur Pos   
^X Exit      ^J Justify   ^W Where is  ^V Next Pg   ^U UnCut Text^T To Spell  
