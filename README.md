# facebook_ads_extractor

Objetivo: 
Crear un proceso automatizado para extraer métricas de rendimiento de campañas de Facebook Ads y cargarlas en un archivo .csv para su posterior análisis en Power BI, utilizando la API de Marketing de Facebook y un script de Python. 

Dirigido a todos aquellos profesionales del análisis de los datos que como yo tenemos el deseo de crecer profesionalmente en el maravilloso mundo de la información y los datos y se nos solicita generar soluciones que requieren años de experiencia dominar y que pocas empresas tienen la disponibilidad de facilitarte un Senior que les guie en este caminar; este conocimiento lo pude adquirir motivado a la necesidad de generar soluciones factibles a mis entornos de trabajo de datos, dando gracias primeramente a Dios por la sabiduría que nos permite emplear y potenciar nuestras habilidades mediante la investigación continua y el empleo de las herramientas actualmente disponibles, como por ejemplo el uso de la IA de Google "Gemini", el cual fue y aun es ese "Senior" que con paciencia me guía en mi aprendizaje continuo y considero respetuoso mencionar como un reconocimiento al arduo trabajo que realizan nuestros Colegas en las diversas empresas Tecnológicas para traer a la humanidad un faro de conocimiento continuo al alcance de todos aquellos que quieran y deseen alcanzarlo, gracias a Dios por habernos permitido vivir en este momento.

Versión: 1.02; Fecha: 8 de junio de 2024; Autor: Nestor Santos

Contenido:
Fase 0: Herramientas y Aplicativos que debes tener.
Fase 1: Configuración de la Aplicación en Facebook Developers.
Fase 2: Configuración del Activo "Cuenta Publicitaria".
Fase 3: Creación del Usuario del Sistema y Token Permanente (Método Profesional).
Fase 4: Configuración del Entorno de Desarrollo en Python.
Fase 5: El Script de Extracción en Python.
Fase 6: Conexión con Power BI.
Fase 7: Automatización de Extración por tarea programada.
Fase 8: Sincronización Automatica de tablero (Gateway de datos local)


Fase 0: Herramientas, aplicativos y consideraciones que debes tener
A continuación te listare las herramientas y programas que vamos a estar empleando, de forma que tengas todo preparado para este proyecto.
Cuenta de Facebook con sus credenciales y autentificadores para poder configurar el entorno de trabajo, tales como los celulares a los que le llegaran los mensajes de autentificación de acceso, correo abierto, etc.
Instalado en tu equipo un compilador de código, yo prefiero usar VS Code puedes usar el de tu preferencia, deberás tener al menos la nociones básicas tales como apertura del terminal, creación de documentos y carpetas, aunque me he esforzado en detallar como gestionar la mayor cantidad de eventos, sugiero repases estos topicos antes de continuar con el proceso para que puedas fluir sin mayor contratiempo.
Instalado en tu equipo Microsoft Power BI. Con el cual construirás el tablero.

Consideraciones: 

Las políticas de privacidad de Meta no permitirán que puedas descargar en un solo set de datos la información asociada a la demografía, geografía y canales (todo junto) con la finalidad de salvaguardar la integridad de la privacidad de sus usuarios, y evitar caídas de servicio por largos procesos de extracción de datos desde API externa, por lo que estaremos descargando en tres archivos formato .csv diferentes, con la finalidad de alimentar nuestro modelo de PBI mediante las configuraciones de Estrella o que sean requeridas.

No es parte del alcance de este manual el construir el tablero de PBI, para evitar hacerlo muy extenso, pero pretendo en este abarcar la mayor cantidad de retos y soluciones que por lo general me toca abordar para un proceso de extracción de este tipo, pues la finalidad es ayudarte a tener una guía con la cual con un nivel mínimo de programación puedas desenvolverte sin mayor contratiempo y con un buenas prácticas profesionales en la fascinante tarea de analizar la información que solicita tu empresa contratante o cliente.

Hice especial énfasis en detallar las ventanas de lo que "no es tan habitual" manejar para un usuario estándar, o un analista de datos general (salvo que este familiarizado con la gestión de mercadeo específicamente) tales como la ruta de gestión de cuentas de Facebook, o bien generación de Automatización de Tareas en Windows y otros aspectos a fines.

Con la finalidad de crear una solución que sea lo más dirigido posible a un usuario final que no posee (ni tendría por qué poseer) conocimiento de programación o Python, este manual estará culminando con la creación de un archivo .bat que al hacer "doble clic" ayudara al usuario final a descargar o extraer la información de la cuenta configurada cada vez que lo desee para actualizar el reporte de PBI que se le ha solicitado, adicionalmente estaremos aprendiendo como automatizar la tarea de "Ejecutar" este Script para poder tener la información disponible para su procesamiento.

Los códigos los encontraras en mi repositorio de Github, el cual podrás copiar e implementar prácticamente de forma directa, los mismos están adaptados para correr contra variables del entorno local del sistema, ya verás más adelante que trato de decir con eso en la Fase 5.

Para este articulo emplee una cuenta de marca personal llamada "Médico a Bordo Venezuela" la cual pertenece a mi esposa y muy genilmente me facilitó para fines de esta practica.


Fase 1: Configuración de la Aplicación en Facebook Developers
El primer paso es obtener las credenciales para que nuestro script pueda comunicarse con Facebook.

Crear Cuenta de Desarrollador: Ve a https://developers.facebook.com/ y regístrate con la cuenta de Facebook que tiene acceso al Business Manager de la empresa.

Crear una Nueva App: En el panel, ve a "Mis apps" > "Crear app". Selecciona el tipo de app: "Negocio" el cual se encuentra en el apartado de "Otros".

Dale un nombre descriptivo (ej. Extractor_PBI_Marketing).

Crucial: Asocia la app a tu Business Manager seleccionándolo en el menú desplegable.

Obtener Credenciales de la App: En el panel de tu nueva app, ve a Configuración -> Básica. Copia y guarda en un lugar seguro el Identificador de la app (App ID) y el Secreto de la app (App Secret). Link de Acceso: https://developers.facebook.com/tools/explorer/


Fase 2: Configuración del Activo "Cuenta Publicitaria"
1.- Abrir una cuenta publicitaria mediante la activación del Portafolio Comercial y Accede con las credenciales. Link de Acceso: https://business.facebook.com/
Ubica la Opción: "Portfolio Comercial" con la que vas a poder crear una "Cuenta Publicitaria", necesaria para acceder a la información de tus ads
Hacer clic en el botón "Ir a la configuración del negocio" lo que te va a redirigir al menú de configuración de cuentas publicitarias y podrás crear una.
Haz clic en Agregar y sigue las instrucciones.

Esto que hemos creado es lo que se conoce como "Activo Digital"; una cuenta publicitaria es un activo que te permite gestionar de manera profesional y centralizada las actividades publicitarias de tu cuenta de Facebook, es importante que registres el identificador de este activo el cual es el que nos vinculará a las acciones de consulta.

Fase 3: Creación del Usuario del Sistema y Token Permanente
En esta fase estaremos creando un Usuario Virtual, con este usuario vamos a Crear "Tokens" o contraseñas de permisos especiales, que nos permitirán acceder al aplicativo, por lo general estos "Tokens" son temporales, pero en esta oportunidad lo configuraremos para que sea de forma permanente cada vez que necesitemos extraer y consultar la información de las cuentas publicitarias.

Posteriormente vamos a Necesitar crear "Usuarios del Sistema" Estos Usuarios son los encargados de administrar los activos, permitiéndonos asignar roles como si se tratasen de "personas dentro de la compañía". Esto lo vamos a lograr al dirigirnos al menú izquierdo en la sección "Usuarios" y en el modulo "Usuarios del Sistema"

Vamos a Proceder a "Agregar" un nuevo usuario, en este caso lo llamaremos Admin_BI el cual tendrá control total sobre los activos Estratégicos de nuestro Interés.

Una vez creado, vamos a proceder a asignar los activos: "Cuenta Publicitaria" y "Aplicativo"; Es importante que le des "Control Total" Sobre la gestión de estos Activos.
Crear el Usuario del Sistema: Ve a business.facebook.com/settings. En el menú izquierdo, ve a Usuarios -> Usuarios del sistema. Haz clic en "Añadir". Dale un nombre (ej.Admin_BI) y asigna el rol "Empleado".

Asignar Activos al Usuario del Sistema: Selecciona el usuario recién creado y haz clic en "Añadir activos". Elige el tipo de activo "Cuentas publicitarias". Selecciona la cuenta publicitaria de la que quieres extraer datos. Activa el permiso de "Gestionar cuenta publicitaria" (Control total). Guarda los cambios.

Asignar Activos a la App: En el menú izquierdo, ve a Cuentas -> Apps. Selecciona tu app (Extractor_PBI_Marketing). Haz clic en "Añadir activos", selecciona la misma cuenta publicitaria y dale el permiso de "Gestionar cuenta publicitaria".

Generar Token Permanente: Vuelve a la sección Usuarios del sistema, selecciona tu usuario. Haz clic en "Generar nuevo token". App: Selecciona tu app. Vencimiento del token: Asegúrate de que dice "Nunca". Permisos: Marca las casillas ads_management, ads_read y read_insights. Haz clic en "Generar token". ¡COPIA Y GUARDA ESTE TOKEN! Es la única vez que lo verás.


Fase 4: Configuración del Entorno de Desarrollo en Python
Crearemos un entorno aislado para mantener nuestro proyecto limpio y ordenado.
Crear Carpeta del Proyecto: Crea una carpeta en tu ordenador para el proyecto (ej. C:\Proyectos\ExtractorFacebook).
Crear y Activar Entorno Virtual: Abre una terminal (como la de VS Code) en la carpeta del proyecto. 
Ejecuta:  python -m venv venv para crear el entorno. 
Activa el entorno (caso Windows): .\venv\Scripts\activate 
Activa el entorno (caso Mac/Linux): source venv/bin/activate 
Tu terminal deberá mostrar (venv) al principio.
Instalar Librerías Necesarias: Con el entorno activado, 
ejecuta: pip install facebook-business pandas

Fase 5: El Script de Extracción en Python y manejo de variables seguras
Este script se conecta a la API, extrae los datos y los guarda en 03 archivos CSV. (facebook_ads_data; facebook_data_demographics; facebook_data_geographics)
Guardar Credenciales de Forma Segura 

Opción 01: Archivo "config.py": Crea un archivo "config.py" en la carpeta de tu proyecto para guardar las credenciales. Asegúrate de añadir "config.py" a tu archivo .gitignore para no subirlo a repositorios públicos en caso que uses git para la gestión de versiones. 

# config.py 
APP_ID = 'TU_APP_ID' 
APP_SECRET = 'TU_APP_SECRET' 
ACCESS_TOKEN = 'TU_TOKEN_PERMANENTE_DEL_USUARIO_DEL_SISTEMA' 
AD_ACCOUNT_ID = 'act_TU_ID_DE_CUENTA_PUBLICITARIA' # ¡Importante el prefijo 'act_'! 

Opción 02: Crea Variables del Entorno del sistema (aplica solo para usarse en el PC donde estarás corriendo la rutina de conexión y descarga de los datos):

En caso que esta rutina de extracción la vayas a realizar desde un computador en particular (como lo es en mi caso) es mas seguro aun preparar las variables desde el Entorno del Sistema, esto evitara que bajo cualquier circunstancia se filtren los datos de los TOKENS, ID's y Contraseñas de acceso de tu plataforma publicitaria de Facebook.

Busca en el Icono de Inicio "Variables del Entorno del Sistema"
Haz clic en "Nueva"

Procede a Rgistrar cada una de las variables del entorno que usaremos en el Script
APP_ID = 'TU_APP_ID' 
APP_SECRET = 'TU_APP_SECRET' 
ACCESS_TOKEN = 'TU_TOKEN_PERMANENTE_DEL_USUARIO_DEL_SISTEMA' 
AD_ACCOUNT_ID = 'act_TU_ID_DE_CUENTA_PUBLICITARIA' # ¡Importante el prefijo 'act_'!

Crear el Script "extractor.py": Crea un archivo "extractor.py" en la misma carpeta. Copia el Script que tendras en mi repositorio de Github en el mismo hay comentarios que te ayudaran a entender el desarrollo del Script. Ver repositorio en Git Hub

Crearemos un Extractor para ejecutar el entorno y que cualquier usuario pueda descargar la data "ejecutar_extractor.bat": Crea un archivo "ejecutar_extractor.bat" en la misma carpeta. Copia el Script que tendras en mi repositorio de Github en el mismo hay comentarios que te ayudaran a entender el desarrollo del Script Ver repositorio en Git Hub
Dirigete a la carpeta donde tienes el proyecto y haz doble clic en el .bat para ejecutar el Script


Fase 6: Conexión con Power BI
Conectar a Power BI: Abre Power BI Desktop. Obtener Datos -> Texto o CSV. Selecciona los archivos csv generados por el script. Carga los datos y comienza a construir tu dashboard.

Fase 7: Automatización de Extración por tarea programada
Automatizar la Ejecución del Script: Usa el Programador de Tareas de Windows para ejecutar el script ejecutar_extractor.bat diariamente a una hora temprana (ej. 6:00 AM). En caso que quieras automatizar y no depender de hacer clic en el archivo .bat que hemos creado 
Paso 1: Abrir el Programador de Tareas Hay varias formas de abrirlo:
Opción A (Búsqueda): Ve al menú de Inicio y escribe "Programador de Tareas". Haz clic en el resultado que aparezca.
Opción B (Ejecutar): Presiona las teclas Win + R para abrir la ventana de "Ejecutar". Escribe taskschd.msc y presiona Enter.
Paso 2: Crear una Tarea Básica: En el panel de Acciones a la derecha, haz clic en "Crear tarea básica...". Esto iniciará un asistente sencillo.
Paso 3: Darle un Nombre y Descripción a la Tarea:Nombre: Escribe un nombre descriptivo para tu tarea (ej. "Backup Diario de Documentos"). Descripción (Opcional): Añade una breve explicación de lo que hace la tarea. Haz clic en Siguiente.
Paso 4: Definir el Desencadenador (Cuándo se ejecutará) Aquí eliges la frecuencia. Para una hora específica, la opción más común es "Diariamente". También puedes elegir "Semanalmente", "Mensualmente" o "Una vez". Selecciona la opción que necesites y haz clic en Siguiente. Ahora, establece la hora exacta. Fecha de inicio: La fecha a partir de la cual comenzará a ejecutarse. Hora: La hora del día en la que se ejecutará (ej. 06:00:00 para las 06 AM). Repetir cada: Déjalo en 1 días para que se ejecute todos los días. Haz clic en Siguiente.
Paso 5: Definir la Acción (Qué se ejecutará) Selecciona "Iniciar un programa". Esta es la opción que necesitas para ejecutar un archivo .bat. Haz clic en Siguiente. Aquí es donde le dices a Windows qué archivo ejecutar.Haz clic en el botón "Examinar...". Navega hasta la carpeta donde guardaste tu archivo .bat, selecciónalo y haz clic en "Abrir". La ruta completa aparecerá en el campo "Programa o script".
Paso 6: Finalizar y Guardar la TareaVerás una pantalla de resumen con toda la configuración. Revisa que todo esté correcto. Importante: Marca la casilla "Abrir el diálogo de Propiedades para esta tarea cuando haga clic en Finalizar". Esto te permitirá configurar opciones avanzadas. Haz clic en "Finalizar".
Paso 7 (Opcional pero Recomendado): Configuración Avanzada Al finalizar, se abrirá la ventana de propiedades de la tarea. Aquí hay algunas opciones clave: Ejecutar con los privilegios más altos: Marca esta casilla si tu script necesita permisos de administrador para funcionar correctamente (por ejemplo, si modifica archivos del sistema). Ejecutar tanto si el usuario ha iniciado sesión como si no: Esta opción es fundamental si quieres que la tarea se ejecute aunque hayas cerrado sesión o reiniciado el PC. Al seleccionarla, es posible que te pida tu contraseña de usuario para guardarla. ¡Y listo! Tu tarea está programada. Para probarla, puedes buscarla en la "Biblioteca del Programador de Tareas", hacer clic derecho sobre ella y seleccionar "Ejecutar".

Fase 8: Sincronización Automatica de tablero (Gateway de datos local)
En Power BI Service (la nube): Publica tu informe de Power BI. Necesitarás instalar un "Gateway de datos local" en tu PC. Este programa actúa como un puente seguro entre Power BI en la nube y los archivos en tu ordenador. Configura una actualización programada en Power BI Service para tu conjunto de datos, diciéndole que se actualice cada día a las 7:00 AM (después de que tu script se haya ejecutado).

Si en tu empresa u organización se presenta el caso que se menciona en líneas anteriores y deseas agregar valor a tu organización mediante este tipo de herramientas, para facilitar la gestión de tus operaciones, implementar indicadores o mejorar el análisis de los que ya posees, no dudes en contactarme y con todo gusto te estaré brindado el apoyo que necesitas.

Ing. Nestor Santos Paredes
"Business Intelligence Consultant"
Whatsapp: +58 412-8672812 | e-mail: nsantos.ks@gmail.com
