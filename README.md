### Actividad Bases de Datos NoSQL
### Caso de uso
Queremos poder hacer el seguimiento de las jugadoras de futbal profesional para diferentes premios, incluyendo:
- El balon de oro
- El guante de oro
- Young Football Player of the Year (Womens Football Award)
- Best Club of the Year (Womens Football Award)

### Estrategia

#### Base de datos

La eleccion en mi caso para esta propuesta es MongoDB ya que entre otras cosas preveo patrones de lectura algo complejos y comparada con otras (por ejemplo Cassandra) MongoDB es mas adecuada. 

#### Esquemas
En las bases de datos NoSQL, el concepto de esquema puede parecer algo anacrónico, ya que estas bases de datos están diseñadas, en principio, para ser "sin esquema". Sin embargo, normalmente existen ciertos requisitos mínimos que deben cumplirse. Por ejemplo, en DynamoDB siempre se necesita una partition key y, si está definida, una sort key. Esto no significa que no debamos modelar nuestros datos siguiendo ciertos criterios. En el caso de MongoDB, surge el concepto de colecciones.

Las colecciones pueden compararse con las tablas en las bases de datos relacionales, aunque esto no implica que dividir los datos en múltiples colecciones sea siempre la mejor opción. MongoDB permite dos enfoques principales para organizar los datos:

Embedding: Agrupar todos los datos relacionados dentro de un mismo documento.
Referencing: Dividir los datos en colecciones lógicas basadas en su tipo o en patrones de acceso, conectándolos mediante referencias.
En nuestro caso, podríamos considerar crear colecciones basadas en criterios como la posición (por ejemplo, una colección para porteras bajo el identificador GK) o la edad (como una colección para Young Football Player of the Year). Sin embargo, en otros contextos, como el premio Balón de Oro o Player of the Year, se incluyen todas las posiciones, lo que plantea algunas preguntas importantes:

¿Nos conviene crear colecciones específicas, como una para porteras, otra para jugadoras jóvenes y otra por equipos?
¿Estamos dispuestos a aceptar cierta duplicación de datos entre colecciones si esto simplifica las consultas o mejora el rendimiento?
Estas decisiones dependen en gran medida de las necesidades específicas del caso de uso, incluyendo factores como el rendimiento, la facilidad de mantenimiento y los patrones de acceso a los datos.

Consideremos los patrones de acceso:
- WRITES:
  Resultado de partido, jugado en casa, rango de victoria (diferencia de goles) => Best Club of the Year (Womens Football Award) 

  Paradas, paradas de penalty, minutos jugados => El guante de oro

  Stadisticas generales de jugadoras => Otras competiciones

- READS:
  Mayor numero de partidos ganados, ordenados por la mayoria ganados fuera de casa, y rango de victoria (en caso de empate las dos ultimas deciden el orden)
  
  Mayor numero de paradas por porteras utilizando, usando minutos jugados, tiros normales y penalties se usaran para desenpates

  Mejores stats de jugadoras jovenes

  Mejores stats de jugadoras en general (menos las jugadoras jovenes)

Como partimos de 3 data sets: datos de jugadoras, datos de equipos y datos de porteras, crearemos 3 colecciones con un esquema/formato cada uno que se adapte a nuestro caso de uso.
##### Porteras:
```json
{
  "name": "string",
  "team": "string",
  "position": "string", // Siempre "GK"
  "debut": "int",       // Año de debut
  "statistics": {
    "general": {
      "minutes_played": "int"
    },
    "goalkeeper": {
      "saves": "int",
      "penalty_saves": "int"
    }
  }
}
```
##### Jugadoras:
```json
{
  "name": "string", 
  "nation": "string", 
  "position": "string", 
  "squad": "string", 
  "age": "integer", 
  "debut": "integer", 
  "statistics": {
    "general": {
      "matches_played": "integer", 
      "starts": "integer", 
      "minutes_played": "integer", 
      "goals": "integer", 
      "assists": "integer"
    }, 
    "advanced": {
      "offsides": "integer", 
      "crosses": "integer", 
      "tackles_won": "integer", 
      "penalties_won": "integer", 
      "penalties_conceded": "integer", 
      "own_goals": "integer", 
      "recoveries": "integer", 
      "aerial_duels": {
        "won": "integer", 
        "lost": "integer"
      }, 
      "completed_passes": "integer"
    }
  }
}
```
##### Equipos:
```json
{
  "name": "string",
  "league": "string",
  "statistics": {
    "general": {
      "goals": "int",
      "assists": "int",
      "victory_margin": "int"
    }
  }
}
```
Estos esquemas han sido creados a partir de los scripts de python en la carpeta load_and_transform

### Tareas
Definir las siguientes consultas:

a. Consulta por una jugadora especifico

He creado un endpoint para hacer consultas generales, en base a field (o fields) y algunas condiciones:

i. Filtrando por el año de comienzo en el football mayor de 2020

curl "http://localhost:8000/api/players/query?field=debut&condition=bigger&value=2020"
```json
{
    "data": [
        {
            "_id": "674e460c3d74dc129e69126e",
            "age": 21,
            "debut": 2021.0,
            "name": "Albeta",
            "nation": NaN,
            "position": "DF",
            "squad": "Villarreal",
            "statistics": {
                "advanced": {
                    "aerial_duels": {
                        "lost": 0.0,
                        "won": 0.0
                    },
                    "completed_passes": 0.0,
                    "crosses": 0.0,
                    "offsides": 0.0,
                    "own_goals": 0,
                    "penalties_conceded": 0.0,
                    "penalties_won": 0.0,
                    "recoveries": 0.0,
                    "tackles_won": 0.0
                },
                "general": {
                    "assists": 0,
                    "goals": 0,
                    "matches_played": 1,
                    "minutes_played": 7,
                    "starts": 0
                }
            }
        },
        {
            "_id": "674e460c3d74dc129e69126f",
            "age": 16,
            "debut": 2024.0,
            "name": "Ainhoa Alguacil",
            "nation": NaN,
            "position": "MF,FW",
            "squad": "Valencia",
            "statistics": {
                "advanced": {
                    "aerial_duels": {
                        "lost": 1.0,
                        "won": 0.0
                    },
                    "completed_passes": 0.0,
                    "crosses": 3.0,
                    "offsides": 0.0,
                    "own_goals": 0,
                    "penalties_conceded": 0.0,
                    "penalties_won": 0.0,
                    "recoveries": 26.0,
                    "tackles_won": 2.0
                },
                "general": {
                    "assists": 1,
                    "goals": 0,
                    "matches_played": 6,
                    "minutes_played": 296,
                    "starts": 4
                }
            }
        },
        {
            "_id": "674e460c3d74dc129e691271",
            "age": 19,
            "debut": 2024.0,
            "name": "Carmen Álvarez",
            "nation": NaN,
            "position": "FW,MF",
            "squad": "Real Betis",
            "statistics": {
                "advanced": {
                    "aerial_duels": {
                        "lost": 18.0,
                        "won": 14.0
                    },
                    "completed_passes": 0.0,
                    "crosses": 0.0,
                    "offsides": 3.0,
                    "own_goals": 0,
                    "penalties_conceded": 0.0,
                    "penalties_won": 0.0,
                    "recoveries": 13.0,
                    "tackles_won": 1.0
                },
                "general": {
                    "assists": 0,
                    "goals": 0,
                    "matches_played": 11,
                    "minutes_played": 495,
                    "starts": 6
                }
            }
        },
        {
            "_id": "674e460c3d74dc129e691273",
            "age": 17,
            "debut": 2023.0,
            "name": "Jone Amezaga",
            "nation": NaN,
            "position": "FW",
            "squad": "Athletic Club",
            "statistics": {
                "advanced": {
                    "aerial_duels": {
                        "lost": 4.0,
                        "won": 2.0
                    },
                    "completed_passes": 0.0,
                    "crosses": 4.0,
                    "offsides": 2.0,
                    "own_goals": 0,
                    "penalties_conceded": 0.0,
                    "penalties_won": 0.0,
                    "recoveries": 19.0,
                    "tackles_won": 6.0
                },
                "general": {
                    "assists": 0,
                    "goals": 3,
                    "matches_played": 6,
                    "minutes_played": 384,
                    "starts": 5
                }
            }
        },
        {
            "_id": "674e460c3d74dc129e69127e",
            "age": 16,
            "debut": 2025.0,
            "name": "Daniela Arques",
            "nation": NaN,
            "position": "MF",
            "squad": "Alhama",
            "statistics": {
                "advanced": {
                    "aerial_duels": {
                        "lost": 7.0,
                        "won": 5.0
                    },
                    "completed_passes": 0.0,
                    "crosses": 4.0,
                    "offsides": 0.0,
                    "own_goals": 0,
                    "penalties_conceded": 0.0,
                    "penalties_won": 0.0,
                    "recoveries": 58.0,
                    "tackles_won": 16.0
                },
                "general": {
                    "assists": 0,
                    "goals": 0,
                    "matches_played": 10,
                    "minutes_played": 570,
                    "starts": 6
                }
            }
        },
        {
            "_id": "674e460c3d74dc129e691292",
            "age": 19,
            "debut": 2021.0,
            "name": "Laura Blasco",
            "nation": NaN,
            "position": "DF",
            "squad": "Sporting Huelva",
            "statistics": {
                "advanced": {
                    "aerial_duels": {
                        "lost": 0.0,
                        "won": 0.0
                    },
                    "completed_passes": 0.0,
                    "crosses": 0.0,
                    "offsides": 0.0,
                    "own_goals": 0,
                    "penalties_conceded": 0.0,
                    "penalties_won": 0.0,
                    "recoveries": 1.0,
                    "tackles_won": 0.0
                },
                "general": {
                    "assists": 0,
                    "goals": 0,
                    "matches_played": 1,
                    "minutes_played": 45,
                    "starts": 0
                }
            }
        },
        {
            "_id": "674e460c3d74dc129e69129f",
            "age": 19,
            "debut": 2022.0,
            "name": "Alba Caño",
            "nation": NaN,
            "position": "MF",
            "squad": "Barcelona",
            "statistics": {
                "advanced": {
                    "aerial_duels": {
                        "lost": 0.0,
                        "won": 0.0
                    },
                    "completed_passes": 0.0,
                    "crosses": 0.0,
                    "offsides": 0.0,
                    "own_goals": 0,
                    "penalties_conceded": 0.0,
                    "penalties_won": 0.0,
                    "recoveries": 4.0,
                    "tackles_won": 1.0
                },
                "general": {
                    "assists": 0,
                    "goals": 0,
                    "matches_played": 1,
                    "minutes_played": 45,
                    "starts": 0
                }
            }
        },
        {
            "_id": "674e460c3d74dc129e6912a2",
            "age": 18,
            "debut": 2022.0,
            "name": "Estela Carbonell",
            "nation": "es ESP",
            "position": "DF",
            "squad": "Levante",
            "statistics": {
                "advanced": {
                    "aerial_duels": {
                        "lost": 1.0,
                        "won": 4.0
                    },
                    "completed_passes": 0.0,
                    "crosses": 15.0,
                    "offsides": 1.0,
                    "own_goals": 0,
                    "penalties_conceded": 0.0,
                    "penalties_won": 1.0,
                    "recoveries": 23.0,
                    "tackles_won": 4.0
                },
                "general": {
                    "assists": 0,
                    "goals": 0,
                    "matches_played": 5,
                    "minutes_played": 261,
                    "starts": 4
                }
            }
        },
        {
            "_id": "674e460c3d74dc129e6912a7",
            "age": 20,
            "debut": 2021.0,
            "name": "Raiderlin Carrasco",
            "nation": "ve VEN",
            "position": "DF",
            "squad": "Sporting Huelva",
            "statistics": {
                "advanced": {
                    "aerial_duels": {
                        "lost": 7.0,
                        "won": 3.0
                    },
                    "completed_passes": 0.0,
                    "crosses": 13.0,
                    "offsides": 2.0,
                    "own_goals": 0,
                    "penalties_conceded": 0.0,
                    "penalties_won": 0.0,
                    "recoveries": 55.0,
                    "tackles_won": 17.0
                },
                "general": {
                    "assists": 1,
                    "goals": 0,
                    "matches_played": 10,
                    "minutes_played": 715,
                    "starts": 8
                }
            }
        },
        {
            "_id": "674e460c3d74dc129e6912a8",
            "age": 20,
            "debut": 2023.0,
            "name": "Sara Carrillo",
            "nation": NaN,
            "position": "FW,MF",
            "squad": "Alavés",
            "statistics": {
                "advanced": {
                    "aerial_duels": {
                        "lost": 19.0,
                        "won": 15.0
                    },
                    "completed_passes": 0.0,
                    "crosses": 7.0,
                    "offsides": 1.0,
                    "own_goals": 0,
                    "penalties_conceded": 0.0,
                    "penalties_won": 0.0,
                    "recoveries": 22.0,
                    "tackles_won": 3.0
                },
                "general": {
                    "assists": 0,
                    "goals": 2,
                    "matches_played": 11,
                    "minutes_played": 610,
                    "starts": 7
                }
            }
        }
    ],
    "execution_time": 0.0031998157501220703
}
```
ii. Filtrando que el equipo que empiece “Machester…..”

curl "http://localhost:8000/api/players/query?field=squad&condition=contains&value=Manchester"
```json
{
    "data": [
        {
            "_id": "674e460c3d74dc129e6913d0",
            "age": 22,
            "debut": 2018.0,
            "name": "Laia Aleixandri",
            "nation": "es ESP",
            "position": "DF,MF",
            "squad": "Manchester City",
            "statistics": {
                "advanced": {
                    "aerial_duels": {
                        "lost": 5.0,
                        "won": 6.0
                    },
                    "completed_passes": 543.0,
                    "crosses": 1.0,
                    "offsides": 0.0,
                    "own_goals": 0,
                    "penalties_conceded": 0.0,
                    "penalties_won": 0.0,
                    "recoveries": 65.0,
                    "tackles_won": 0.0
                },
                "general": {
                    "assists": 0,
                    "goals": 0,
                    "matches_played": 8,
                    "minutes_played": 679,
                    "starts": 8
                }
            }
        },
        {
            "_id": "674e460c3d74dc129e6913d1",
            "age": 25,
            "debut": 2017.0,
            "name": "Filippa Angeldal",
            "nation": "se SWE",
            "position": "MF",
            "squad": "Manchester City",
            "statistics": {
                "advanced": {
                    "aerial_duels": {
                        "lost": 0.0,
                        "won": 0.0
                    },
                    "completed_passes": 55.0,
                    "crosses": 0.0,
                    "offsides": 0.0,
                    "own_goals": 0,
                    "penalties_conceded": 0.0,
                    "penalties_won": 0.0,
                    "recoveries": 7.0,
                    "tackles_won": 0.0
                },
                "general": {
                    "assists": 0,
                    "goals": 0,
                    "matches_played": 4,
                    "minutes_played": 111,
                    "starts": 1
                }
            }
        },
        {
            "_id": "674e460c3d74dc129e6913d9",
            "age": 23,
            "debut": 2019.0,
            "name": "Ona Batlle",
            "nation": "es ESP",
            "position": "DF",
            "squad": "Manchester Utd",
            "statistics": {
                "advanced": {
                    "aerial_duels": {
                        "lost": 3.0,
                        "won": 2.0
                    },
                    "completed_passes": 274.0,
                    "crosses": 20.0,
                    "offsides": 0.0,
                    "own_goals": 0,
                    "penalties_conceded": 0.0,
                    "penalties_won": 0.0,
                    "recoveries": 32.0,
                    "tackles_won": 8.0
                },
                "general": {
                    "assists": 4,
                    "goals": 1,
                    "matches_played": 5,
                    "minutes_played": 449,
                    "starts": 5
                }
            }
        },
        {
            "_id": "674e460c3d74dc129e6913e0",
            "age": 21,
            "debut": 2019.0,
            "name": "Julie Blakstad",
            "nation": "no NOR",
            "position": "FW",
            "squad": "Manchester City",
            "statistics": {
                "advanced": {
                    "aerial_duels": {
                        "lost": 2.0,
                        "won": 3.0
                    },
                    "completed_passes": 74.0,
                    "crosses": 6.0,
                    "offsides": 2.0,
                    "own_goals": 0,
                    "penalties_conceded": 0.0,
                    "penalties_won": 0.0,
                    "recoveries": 15.0,
                    "tackles_won": 4.0
                },
                "general": {
                    "assists": 1,
                    "goals": 2,
                    "matches_played": 6,
                    "minutes_played": 210,
                    "starts": 2
                }
            }
        },
        {
            "_id": "674e460c3d74dc129e6913e2",
            "age": 28,
            "debut": 2014.0,
            "name": "Hannah Blundell",
            "nation": "eng ENG",
            "position": "DF",
            "squad": "Manchester Utd",
            "statistics": {
                "advanced": {
                    "aerial_duels": {
                        "lost": 2.0,
                        "won": 3.0
                    },
                    "completed_passes": 416.0,
                    "crosses": 6.0,
                    "offsides": 0.0,
                    "own_goals": 0,
                    "penalties_conceded": 0.0,
                    "penalties_won": 0.0,
                    "recoveries": 25.0,
                    "tackles_won": 8.0
                },
                "general": {
                    "assists": 0,
                    "goals": 1,
                    "matches_played": 8,
                    "minutes_played": 608,
                    "starts": 8
                }
            }
        },
        {
            "_id": "674e460c3d74dc129e6913ee",
            "age": 27,
            "debut": 2016.0,
            "name": "Vilde Bøe Risa",
            "nation": "no NOR",
            "position": "FW,MF",
            "squad": "Manchester Utd",
            "statistics": {
                "advanced": {
                    "aerial_duels": {
                        "lost": 0.0,
                        "won": 0.0
                    },
                    "completed_passes": 18.0,
                    "crosses": 1.0,
                    "offsides": 0.0,
                    "own_goals": 0,
                    "penalties_conceded": 0.0,
                    "penalties_won": 0.0,
                    "recoveries": 3.0,
                    "tackles_won": 0.0
                },
                "general": {
                    "assists": 0,
                    "goals": 0,
                    "matches_played": 4,
                    "minutes_played": 56,
                    "starts": 0
                }
            }
        },
        {
            "_id": "674e460c3d74dc129e6913f5",
            "age": 22,
            "debut": 2018.0,
            "name": "Kerstin Casparij",
            "nation": "nl NED",
            "position": "DF",
            "squad": "Manchester City",
            "statistics": {
                "advanced": {
                    "aerial_duels": {
                        "lost": 3.0,
                        "won": 0.0
                    },
                    "completed_passes": 351.0,
                    "crosses": 11.0,
                    "offsides": 0.0,
                    "own_goals": 0,
                    "penalties_conceded": 0.0,
                    "penalties_won": 0.0,
                    "recoveries": 36.0,
                    "tackles_won": 12.0
                },
                "general": {
                    "assists": 1,
                    "goals": 0,
                    "matches_played": 7,
                    "minutes_played": 595,
                    "starts": 7
                }
            }
        },
        {
            "_id": "674e460c3d74dc129e6913f6",
            "age": 23,
            "debut": 2017.0,
            "name": "Deyna Castellanos",
            "nation": "ve VEN",
            "position": "MF",
            "squad": "Manchester City",
            "statistics": {
                "advanced": {
                    "aerial_duels": {
                        "lost": 4.0,
                        "won": 3.0
                    },
                    "completed_passes": 206.0,
                    "crosses": 5.0,
                    "offsides": 1.0,
                    "own_goals": 0,
                    "penalties_conceded": 0.0,
                    "penalties_won": 0.0,
                    "recoveries": 29.0,
                    "tackles_won": 4.0
                },
                "general": {
                    "assists": 0,
                    "goals": 0,
                    "matches_played": 8,
                    "minutes_played": 612,
                    "starts": 7
                }
            }
        },
        {
            "_id": "674e460c3d74dc129e6913fc",
            "age": 31,
            "debut": 2010.0,
            "name": "Laura Coombs",
            "nation": "eng ENG",
            "position": "MF",
            "squad": "Manchester City",
            "statistics": {
                "advanced": {
                    "aerial_duels": {
                        "lost": 4.0,
                        "won": 3.0
                    },
                    "completed_passes": 228.0,
                    "crosses": 2.0,
                    "offsides": 1.0,
                    "own_goals": 0,
                    "penalties_conceded": 0.0,
                    "penalties_won": 0.0,
                    "recoveries": 34.0,
                    "tackles_won": 8.0
                },
                "general": {
                    "assists": 2,
                    "goals": 3,
                    "matches_played": 8,
                    "minutes_played": 633,
                    "starts": 8
                }
            }
        },
        {
            "_id": "674e460c3d74dc129e691405",
            "age": 29,
            "debut": 2014.0,
            "name": "Mary Earps",
            "nation": "eng ENG",
            "position": "GK",
            "squad": "Manchester Utd",
            "statistics": {
                "advanced": {
                    "aerial_duels": {
                        "lost": 0.0,
                        "won": 0.0
                    },
                    "completed_passes": 325.0,
                    "crosses": 0.0,
                    "offsides": 0.0,
                    "own_goals": 0,
                    "penalties_conceded": 0.0,
                    "penalties_won": 0.0,
                    "recoveries": 18.0,
                    "tackles_won": 0.0
                },
                "general": {
                    "assists": 0,
                    "goals": 0,
                    "matches_played": 8,
                    "minutes_played": 720,
                    "starts": 8
                }
            }
        }
    ],
    "execution_time": 0.014238834381103516
}
```

### Recursos usados
Me he valido tanto de la documentación oficial como de Chatgpt para completar esta tarea. Algunas de las cosas con la que me ha ayudado Chatgpt son:

Implementar consultas avanzadas y dinámicas que permiten filtrar datos por diversos criterios, como años de debut o nombres de equipos.

Depurar problemas relacionados con configuraciones de contenedores Docker, conexiones a la base de datos y la ejecución de consultas desde una API.

Automatizar la inserción de datos desde datasets complejos, garantizando su correcta transformación al esquema diseñado.

Proporcionar herramientas de diagnóstico, como logs y pruebas directas, para identificar problemas en la ejecución de las consultas.

Refinar la API para incluir funcionalidades dinámicas y adaptables, mejorando la flexibilidad del sistema.
