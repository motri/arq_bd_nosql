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
En las bases de datos no sql el concepto de esquema es un tanto anacronista ya que en principio son bases de datos sin esquema (aunque normalmente hay que cumplir unos minimos como en Dynamodb, en la que siempre hara falta un partition key, y si ha sido definida, un sort key). Pero ello no quiere decir que no modelemos nuestros datos en base a ciertos criterios. En el caso de MongoDB tenemos el concepto de colecciones.
Las colecciones se pueden entender como tablas, pero eso no quiere decir que dividir los datos en colecciones no siempre es util. MongoDB permite agrupar todos los datos en sus documentos, lo que se conoce como Embedding o dividirlos en colecciones logicas agrupadas por el tipo de datos (teniendo en cuenta cosas como patrones de acceso), conocido como Referencing.
Para nuestra problematica, podriamos crear colecciones basandonos en posición (GK para porteras por ejemplo) o edad (Young Football Player of the Year). Sin embargo en otros casos como Balon de oro y Player of the Year se consideran todas las posiciones, por lo que quedaría considerar: ¿Nos interesa una colección que solo abarque las porteras, otra jugadoras menores de cierta edad y una por equipos? Nos importa la duplicacion de datos en varias colecciones?
Consideremos los patrones de acceso:

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
