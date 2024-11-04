Sistema de Gestion de inventario con Telegram + Google Cloud + Google Sheet 

Proyecto realizado mediante un bot de telegran para almacenar datos relacionado con un inventario de productos. 

NOta: En config.py van todas las password que se necesitan agregue las suyas. 

Modulo 1 

1 - BotFather

BotFather es el bot oficial de Telegram para crear y gestionar otros
bots. 

@BotFather (Telegram)

2 - Token

Un token es una cadena de caracteres que actúa como una clave
única para identificar y autenticar a tu bot cuando interactúa con la
API de Telegram.

3 - Creacion de Bot en Telegran 

a) Buscar a BotFather en telegram.
b) Nombramiento del bot puede ser: rj_Bot o rjBot (siempre especificar el Bot al final).
c) Creacion del Bot que generara un token.

4 -  Creacion de entorno Virtual

comando en la terminal: python -m venv mi_entorno o (nombre que desea del entorno)

nota: para verificar si estamos en un entorno virtual comando: pip list 

Librerias: 

- PyTelegramBotAPI
- Numpy
- Google Api Python Client
- Google Auth HTTPLib2
- Google Auth Oauthlib

Instalación:
pip install pytelegrambotapi numpy google-api-python-client
google-auth-httplib2 google-auth-oauthlib

Modulo 2  (Creacion de sistema de gestión)

1 =  Creacion de main.py en el se importa el config y telebot 

ver main.py

Decoradores: agarra un fincion annadirle cosas y devolver la funcion. 

Threading: Se refiere a la capacidad de ejecutar varias tareas simultáneamente
dentro de un solo programa.(HILOS)

Ver la descripcion en el codigo para entender lo que hace.


Modulo 3 (Botones(Telegran) y Google Cloud)

1 Botones(inline)
  
  a) def Botonera (main.py line 16)
  b) def call_back (main.py line 100 )

2 Botones (Reply)

  a) def call_back (main.py line 118 )

3 Google Cloud 

  a) Crear un cuenta y el proyecto
  b) Habilitar google sheets API 
  c) Generar Clave JSON de la Api y descargar 

Modulo 4 conexion a base de datos (api)

 a) Documnetacion Google sheets (apartado excel)
 b) creacion y visualizacion de tabla por el bot de telegram. 

Modulo 5 Metodos 
   
a) buscar en nota.

nota: https://pickled-boater-07d.notion.site/Documentaci-n-de-Curso-Gratuito-de-Sistema-de-Gesti-n-Python-y-Telegram-1158c0d98b1d80d4965dcc60a322e1b0#1228c0d98b1d80fea81beb4e0708e52b
  
  
  




