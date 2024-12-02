### Actividad Bases de Datos NoSQL
![ETL DIAGRAM](./img/etl_small.png)
### Caso de uso
Queremos poder hacer el seguimiento de las jugadoras de futbal profesional para diferentes premios, incluyendo:
- El balon de oro
- El guante de oro
- Player of the year (Womens Football Award)
- Young Football Player of the Year (Womens Football Award)
- Best Club of the Year (Womens Football Award)
### Esquemas
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
  
  Mayor numero de paradas por porteras utilizando 
### Tareas
Las tareas que se piden son las siguientes:
1. Explicar las ventajas y desventajas de la BD NOSQL seleccionada, en resumen, el por
qué.
2. Definir el esquema, y las sentencias de creación de este, ya sean generación de tablas,
grafos o documentos…
3. Definir las sentencias de inserción para 100 registros del dataset. Si es necesario
utilizar un script para adaptar la inserción desde el csv o usar un API (por ejemplo, de
Python), adjuntar el script y explicar el por qué y cómo se ejecutaría.
4. Definir (si se puede) sentencias de modificación para dos de los registros, cambiando
el nombre de la jugadora a Mayúsculas.
5. Definir las siguientes consultas:
a. Consulta por una jugadora especifico
i. Filtrando por el año de comienzo en el football mayor de 2020
ii. Filtrando que el equipo que empiece “Machester…..”
b. Consulta por un país concreto donde juega una jugadora
