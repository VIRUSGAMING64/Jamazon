# Diseño e Implementación de Jamazon

## Introducción

El proyecto Jamazon se diseñó con el objetivo de gestionar y optimizar la planificación de tareas. El dominio de la aplicación abarca la administración temporal de recursos limitados tales como 
freidoras, hornos, cocineros, repartidores
El problema central que resuelve el software es la asignación eficiente de intervalos de tiempo para realizar tareas (eventos). Cada evento, como "Preparar Pedido", requiere el bloqueo simultáneo de una cantidad específica de múltiples recursos 
durante una duración determinada. El sistema debe garantizar que, en ningún momento del intervalo propuesto, la demanda acumulada 
de un recurso supere su capacidad máxima instalada. Además, se manejan restricciones de dependencia jerárquica; por ejemplo, el uso 
de un equipo informático bloquea automáticamente una cuota del recurso "Electricidad" y "Internet".
La aplicación es capaz de sugerir al usuario el momento más próximo posible para iniciar una 
tarea cuando los recursos están ocupados, calculando "huecos" disponibles en la agenda que satisfagan todas las restricciones de 
recursos simultáneamente.

## Diseño

El proyecto abarca el  dominio de una tienda de comida, tiene recursos como repartidores, cocineros, agua, coca-cola, gerente entre otros,
existe una cantidad finita de cada recurso, dependencias entre recursos y restricciones de recursos los cuales no se pueden usar con otros por ejemplo el recurso gerente, este recurso necesita de los recursos `telefono` y `ordenador_gerente` y no puede esta en la misma terea que `concinero`, `repartidor`, `personal_limpieza` y `ayudante_cocina`, en fin los empleados

```txt
"gerente": {
    "count": 2,
    "need": [
        "ordenador_gerente",
        "telefono"
    ],
    "without": [
        "cocinero",
        "repartidor",
        "personal_limpieza",
        "ayudante_cocina"
    ]
}
```

aqui se representa la estrucutra de un recurso tiene un count que seria la cantidad de recursos de este tipo, los recursos que necesita y los recursos con los cual no puede estar, si una tarea necesita de ese recurso entonces  tambien necesita de los que ese recurso necesita
tambien se evidencia que si la tarea necesita de un cocinero entonces la tarea no puede contener un gerente porque el gerente no puede esta con el cocinero.
Las tareas del calendario:
```txt
"Entregar coca cola": {
    "resources": [
        {
        "name": "coca cola",
        "count": 1
        },
        {
        "name": "repartidor",
        "count": 1
        },
        {
        "name": "moto",
        "count": 1
        }
    ],
    "without": [
        "guantes_cocina",
        "personal_limpieza"
    ]
},
```
las tareas estan organizadas con los campos "resources" y "without", en el primero se guarda un array con "objetos" que vendria siendo los recursos que se necesita la tarea para ejecutarse, en el segundo campo se encuentra los recursos que no pueden estar en esa tarea

Tambien se decidio implementar la opcion de que el usuario pueda definir sus propias tareas y sus propios recursos asi como modificar la cantidad de recursos instalados agregandole o restandole una cantidad especifica, en el caso que se intente restar una cantidad mayor a la cantidad existente se reporta al usuario

## Arquitectura

### Estructura y Decisiones de Diseño

Para garantizar la mantenibilidad y la escalabilidad del sistema, se optó por una arquitectura modular que desacopla estrictamente la lógica de negocio de la interfaz de usuario.
Se decidió utilizar archivos JSON como mecanismo de persistencia de datos en lugar de una base de datos relacional. Esta decisión se tomó para simplificar la portabilidad del proyecto y eliminar la necesidad de servicios externos corriendo en segundo plano, dado que el volumen de datos esperado es pequeño y manejable en memoria.

## La estructura se divide en

* `main.py`: Punto de entrada de la aplicación.
* `modules` (Backend): Contiene la lógica y algoritmos.
* `gui_core` (Frontend): Gestiona la interacción con la librería gráfica, consumiendo los servicios del backend sin conocer su implementación interna.


### Entorno de Desarrollo

La implementación se ha llevado a cabo en un entorno Linux, utilizando Git y VSCode, se ha testeado la compatibilidad en sistemas Arch Linux, Ubuntu y Windows 11.

## Lógica de módulos

### `utils.py`

En este módulo solamente se encuentran las funciones útiles que se usan en todo el proyecto. Fue creado con el objetivo de evitar código repetido en el proyecto y tener más organizadas las funciones individuales utilizadas.

* `log`: Esta función redirige los datos de entrada a un archivo, es utilizada para debug. Facilita el diagnóstico de problemas durante el desarrollo y la ejecución.
* `get_sources_dependency`: Esta función implementa un algoritmo de búsqueda en profundidad (DFS) para resolver las dependencias entre recursos. Es crucial para asegurar que, al asignar una tarea, todos los recursos indirectamente requeridos por otros recursos (ej: un horno requiere electricidad) estén disponibles. El DFS recorre un grafo de dependencias definido en los archivos de configuración, detectando ciclos y garantizando una asignación coherente.
* `CheckISODate`: Retorna True si el ISODate de entrada está correcto. Es vital para la validación de las fechas y horas proporcionadas por el usuario, asegurando la integridad de los datos temporales del sistema.
* `get_saved_json`: Devuelve un diccionario con los datos de un JSON especificado. Es una utilidad genérica para cargar configuraciones y estados persistidos.
* `read_file`: Carga un archivo directamente en memoria. Utilizado para leer archivos de configuración y datos.
* `tominute`: Convierte una fecha en su correspondiente en minutos.
* `add_to_dict`: Esta función agrega a un diccionario recursivamente un dato (más detalles en `utils.py`). Permite la construcción dinámica de estructuras de datos anidadas.
* `event_option_label`: Genera un pequeño texto descriptivo a partir de un evento. Se usa en la interfaz de usuario para mostrar opciones de eventos de forma legible.
* `build_event_option_labels`: Genera una lista con los datos retornados por la función anterior para cada evento. Prepara los datos para los menús desplegables y selectores de eventos en la GUI.
* `format_event_info`: Genera la información completa de un evento. Utilizada para presentar detalles de una tarea al usuario de manera estructurada.

### `iohandler.py`

Aquí se encuentra la clase `BasicHandler`, la cual se encarga de la mayoría de IO en archivos JSON. Esta clase es fundamental para la persistencia de datos, ya que abstrae la complejidad de leer y escribir en el formato JSON, que fue elegido por su portabilidad y simplicidad para un volumen de datos manejable.

* `_load_json`: Lee un archivo JSON y lo deserializa a un diccionario de Python. Es crucial para cargar el estado del sistema al inicio de la aplicación.
* `_ex_ext`: Una utilidad para obtener la extensión de un nombre de archivo, usada para validación o clasificación de archivos.
* ` _jsonstr_to_dict`: Transforma una cadena JSON directamente en un diccionario. Útil cuando los datos JSON provienen de fuentes distintas a archivos.
* ` _dict_to_jsonstr`: Transforma un diccionario Python en una cadena JSON. Utilizada para preparar datos para el almacenamiento

### `gvar.py`

Este módulo, su principal función es cargar los datos de JSON y se encarga de contener
los datos globales para todo el programa. Por ejemplo el calendario global que se encarga de agregar y eliminar tareas

### `events.py`

Se encuentra la clase `Event`; ésta hereda de `BasicHandler` y se encarga de guardar en ella una tarea específica,
guardando los datos de esta. Además, implementa transformaciones a los datos:

* Convierte una tarea a dict.
* Convierte una tarea a str.

### `calendar.py`

Como en este módulo hay mucho que explicar se dividió en varios puntos. Aquí se encuentra la clase `Calendar`, la que se encarga de:

* Agregar tareas.
Uno de los retos principales enfrentados durante el desarrollo fue el manejo de rangos de tiempo basados en timestamps de Unix, los cuales generan números muy grandes (e.g., 1000000007). Crear un arreglo de ese tamaño consumiría demasiada memoria.
Para solucionar esto, se implementó dentro de esta lógica una técnica de **Compresión de Coordenadas**. El algoritmo identifica los puntos de interés (inicios y finales de eventos existentes) y los mapea a índices secuenciales pequeños (0, 1, 2...), considerando solo los momentos donde el estado del sistema cambia, ignorando los periodos "vacíos" intermedios.

* Ordenar las fechas.
Este se encarga de matener las fechas ordenadas para su mejor manipulacion en el futuro

* Eliminar tareas viejas al iniciar. Cuando inicia el programa este elimina las fechas cullo final sea mayor a la fecha actual del sistema

### `add_event`

En el momento de hacer esta función se encontró el problema de que los rangos de tiempo
podían ser muy grandes, por lo que se necesitó implementar una compresión de coordenadas
para que (R - L) sea más pequeño para poder verificar más rápidamente si en ese rango se puede agregar la nueva tarea.

### `suggest_brute_lr`

Esta función implementa a fuerza bruta la lógica detrás de sugerir un rango de fechas al usuario.
Lo que hace es que por cada recurso verifica si el rango de tiempo esta disponible, de no estarlo el rango de tiempo pasa a tener como inicio el minimo tiempo final de las tareas actuales tal que ese tiempo es mayor que el inicio del intervalo que se esta verificando y reincia procesos, si se verifican todos los recursos y estan disponibles en con el inicio dado entonces nos retorna ese inicio

### `check_available`

Verifica si un rango de fecha dado está disponible para asignar recursos.
Esta función revisa si, para el intervalo de tiempo especificado, la cantidad de recursos solicitados 
no excede la capacidad total disponible, asegurando que no existan conflictos con otras tareas ya programadas.

### `remove`

Esta función elimina una tarea específica del calendario, liberando los recursos que estaban asignados
a dicha tarea y actualizando la estructura de datos (los datos en Calendar) para reflejar la eliminación.

### `sort`

Esta función ordena las fechas (claves del diccionario) por tiempo de inicio.

### `remove_old_events`

Esta función se encarga de recorrer todas las tareas registradas y eliminar aquellas cuya
fecha de finalización es anterior a la fecha y hora actual del sistema. Esto permite mantener el calendario limpio y optimizado,
reduciendo el tamaño del árbol de segmentos necesario para futuros cálculos.

## Problemas y Soluciones

Durante el ciclo de desarrollo se enfrentaron varios obstáculos técnicos que definieron la arquitectura final:

* **Validación de Dependencias**: Gestionar recursos que dependen de otros (ej: Internet requiere Electricidad) complicó la lógica de verificación. Se resolvió implementando una búsqueda en profundidad (DFS) en `utils.py` que recorre recursivamente el grafo de dependencias para asegurar que todos los recursos base estén disponibles antes de confirmar una tarea.
* **Persistencia de Datos**: Mantener la consistencia entre los archivos JSON y los objetos en memoria fue complejo. Se estandarizaron métodos en `iohandler.py` para serializar y deserializar objetos automáticamente, evitando la corrupción de datos al cerrar el programa inesperadamente.

* **Creacion de la gui**: de todas las opciones que estaban disponibles se decidio usar CustomTkinter pues era puramente python y los conocimientos en desarrollo web eran bajos en el momento de desarrollar la interfaz

### `gui_core`

En esta carpeta se encapsulan todas las clases que heredan de `CTkToplevel` o componentes de la biblioteca gráfica,
actuando como puente entre la interacción del usuario y la lógica.

* `EventCreator`
Esta clase gestiona la interfaz para la definición de **tipos de eventos** en el sistema.
Permite al usuario especificar el nombre de una nueva actividad operativa (ej. "Freír Papas")
y asociarla con una lista de recursos necesarios para su ejecución.
* `TaskCreator`
Esta clase implementa la interfaz de **agendamiento**. Proporciona campos para ingresar 
la fecha y hora de inicio y fin, así como un selector de las actividades definidas previamente.
Interactúa directamente con el módulo `calendar` para verificar la disponibilidad de recursos en el intervalo solicitado 
y confirma la creación de la instancia del evento en el cronograma.

* `ResAdder`
Clase responsable de la gestión del inventario de recursos base.
Permite al administrador registrar nuevos recursos en el sistema (ej. "Freidora", "Personal", "Electricidad"), 
definiendo su capacidad máxima inicial. Actualiza la estructura de datos de recursos globales,
haciéndolos disponibles para ser requeridos por futuras tareas.

* `EventShower`
Visualizador de eventos activos y programados. Genera una lista dinámica de botones que representan cada tarea en la cola de ejecución del sistema, mostrando su ID, nombre y el intervalo de tiempo asignado. Al interactuar con un elemento, despliega información detallada sobre el evento específico, facilitando el monitoreo de las operaciones del local en tiempo real.

* `ResourceShower`
Interfaz de consulta de recursos. Muestra un listado de todos los recursos registrados en el sistema junto con su cantidad total disponible. Permite a los administradores tener una visión clara de la capacidad instalada del local y verificar las propiedades de cada recurso.

* `TaskRemover`
Herramienta de gestión para la cancelación de tareas. Proporciona una interfaz donde se listan los eventos programados en un menú desplegable, permitiendo al usuario seleccionar y eliminar una tarea específica. Al confirmar la acción, invoca los métodos de limpieza del backend para liberar los recursos reservados por dicho evento en el Segment Tree, actualizando inmediatamente la disponibilidad del sistema.

## bibliografía

[Python 3.12.1 Documentation](https://docs.python.org/3/)

[CustomTkinter: Official Documentation And Tutorial](https://customtkinter.tomschimansky.com/)

[CP-Algorithms: Competitive Programming Library](https://cp-algorithms.com/)

---
