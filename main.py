from config import * # Importo la configuracion 
from sheet import * # Importo la hoja de calculo

import telebot # para menjar la API de Telegran 
import threading # para crear un hilo
import numpy as np # usado para realizar operaciones o listas
import secrets # libreria para genrera codigo aleatorio

from telebot.types import InlineKeyboardMarkup # para crear el esquema de los botones
from telebot.types import ReplyKeyboardMarkup # crear botones reply
from telebot.types import InlineKeyboardButton # crear botones inline


#<-------------------- Instancia del bot
bot = telebot.TeleBot(TELEGRAM_TOKEN) # instancia del bot

#<-------------------- varibale global en la que guardamos los productos
producto = {}

#<-------------------- Definir funcion de botonera y como se ve en el bot
def botonera(anterior = 0, siguiente = 2,paginas = 0, ids = []):
  
  markup = InlineKeyboardMarkup(row_width = 5 )
  
  botones = []
  
   #Botones
  # 1 2 3 4 5
  # ⏮️ ❌ ⏭️
  # nuevo 🔁 
  # Emojis: win + .
  
  for i in ids:
    b1 = InlineKeyboardButton(f'✏️{i}'  , callback_data=f'editar {i}')
    botones.append(b1)
    # con el * add(b1, b2, b3, b4, b5)
    
  markup.add(*botones)

  b6 = InlineKeyboardButton('⏮️', callback_data=f'anterior {anterior} {siguiente} {paginas}')
  b7 = InlineKeyboardButton('❌', callback_data='eliminar')
  b8 = InlineKeyboardButton('⏭️', callback_data= f'siguiente {anterior} {siguiente} {paginas}')
  
  b9 = InlineKeyboardButton('➕', callback_data='nuevo')
  
  b10 = InlineKeyboardButton('🔁', callback_data= f'refrescar {anterior} {siguiente}')
  
  markup.add(b6, b7, b8)
  markup.add(b9, b10)
  
  return markup 
  
def mostrar_tabla(message,anterior = 0,siguiente =2): 
  # Obtener los datos de la hoja de Calculo
   headers = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="Hoja 1!1:1").execute()
   # Obtener el valor de los titulos
   valoresTitulos = headers.get('values', [])
   # Obtenemos el total de filas
   filas = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="Hoja 1!A2:A").execute()
   # Obtenemos el total de filas en numero
   total = len(filas.get('values', []))
   # Obtenemos el total de paginas (redondearlo)
   paginas = round(total/5 + 0.5)
   #obtener los datos(por paginas de 5(investigar mas))
   datos = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=f'Hoja 1!A{(2 + anterior*5)}:D{(6 + anterior*5)}').execute()
   # Obtenemos los valores
   DatosValores = datos.get('values', []) 
   # Convertimos a array de numpy
   values = np.array(DatosValores)
    
   #obtenemos una lista de ids
   
   ids = (values[:,0]).tolist()
    
   # ----------- Armamos la tabla
   tabla = f"_Resultados de la consulta {anterior*5 + 1} a {min(total,(anterior+1)*5)} de un total de {total}_ \n"
   tabla += "`Datos: \n\n{:<5} {:<15} {:<5} {:<5}\n".format(*valoresTitulos[0])
   
   for fila in values:
     tabla += "{:<5} {:<15} {:<5}   {:<5}\n".format(*fila)
     
   tabla += "`\n"
  # <------------------Enviar la tabla al chat
  
   botones = botonera(anterior, siguiente, paginas, ids)
   
   bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=tabla, parse_mode='MarkdownV2', reply_markup= botones)
     
     
#<--------------------  Funcion que se encarga de responder al comando /start
@bot.message_handler(commands=['start', 'help']) # responde al comando start
def inicio(message):
  msg = bot.send_message(message.chat.id, f'Hola {message.from_user.first_name}, bienvenido a mi bot. Espere un Momento ...')
  mostrar_tabla(msg)
  
  
#<-------------------- Funcion que se encarga de responder al comando /new
@bot.message_handler(commands=['new']) # responde al comando new
def new(message):
  producto[message.chat.id] = {} # crea un diccionario vacio dentro de productos
  msg = bot.send_message(message.chat.id, 'Cual es el nombre del producto?')
  bot.register_next_step_handler(msg, nuevo_producto_precio)
    
def nuevo_producto_precio(message):
  producto[message.chat.id]["Nombre"] = message.text # guardamos el nombre en el diccionario
  msg =bot.send_message(message.chat.id, 'Cual es el precio del producto?') 
  bot.register_next_step_handler(msg, nuevo_precio_stock)
 
def nuevo_precio_stock(message):
  producto[message.chat.id]["Precio"] = message.text # guardamos el precio en el diccionario
  msg = bot.send_message(message.chat.id, 'Cual es el stock del producto?')
  bot.register_next_step_handler(msg, nuevo_final)
    
def nuevo_final(message):
  producto[message.chat.id]["Stock"] = message.text # guardamos el stock en el diccionario
  #crear una variables de productos
  id = secrets.token_hex(2) # Generamos un id aleatorio de 4 caracteres, ejm: 3a4f
  
  nombre = (producto[message.chat.id]["Nombre"])
  precio = (producto[message.chat.id]["Precio"])
  stock = (producto[message.chat.id]["Stock"])
   
  nuevo_producto = [[id, nombre, precio, stock]]
  
  sheet.values().append(spreadsheetId=SPREADSHEET_ID, range='Hoja 1!A1:D', valueInputOption='USER_ENTERED', body={'values': nuevo_producto}).execute()
  
  bot.send_message(message.chat.id, 'Producto creado con exito ✅')
 
  print(producto[message.chat.id])
    
#<-------------------- ver los diferentes formatos cuando se escriba algun texto. 
''' 
Se Comento por que esto es de uso informativo para darle formato a los mensajes. 
@bot.message_handler(content_types=['text']) 
def listadeFormatos (message):
  # Formart HTML
  text_html = 'Negrita: <b>NEGRITA</b>' + '\n'
  text_html += 'Cursiva: <i>CURSIVA</i>' + '\n'
  text_html += 'Subrayado: <u>SUBRAYADO</u>' + '\n'
  text_html += 'Tachado: <s>TACHADO</s>' + '\n'
  text_html += 'Codigo: <code>CODE</code>' + '\n'
  text_html += 'Copiado: <pre>COPY</pre>' + '\n'
  text_html += 'Enlace: <a href="https://www.google.com">LINK</a>' + '\n'
  text_html += 'Spoiler: <span class="tg-spoiler">SPOILER</span>' + '\n
  bot.send_message(message.chat.id, text_html, parse_mode= 'HTML')
  # Formart Markdown
  text_markdown = 'Negrita: *NEGRITA*' + '\n'
  text_markdown += 'Cursiva: _CURSIVA_' + '\n'
  text_markdown += 'Subrayado: __SUBRAYADO__' + '\n'
  text_markdown += 'Tachado: ~TACHADO~' + '\n'
  text_markdown += 'Codigo: `CODE`' + '\n'
  text_markdown += 'Copiado: ```COPY```' + '\n'
  text_markdown += 'Enlace: [Google](https://www.google.com)' + '\n'
  text_markdown += 'Spoiler: ||SPOILER||' + '\n'
  bot.send_message(message.chat.id, text_markdown, parse_mode= 'MarkdownV2')
'''
#< ------------------- Funcion que se encarga de responder a los botones (inline)
@bot.callback_query_handler(func=lambda call:True)
def call_back(call):
  # si se presiona el emoji  de anterior '⏮️'
  if call.data.startswith('anterior'):
    
    _, anterior, siguiente, paginas = call.data.split(' ')
    
    anterior = int(anterior)
    siguiente = int(siguiente)
    paginas = int(float(paginas))
    
    if anterior == 0:
      anterior = paginas - 1
      siguiente= paginas + 1
    else:
      anterior -= 1
      siguiente -= 1
    
    mostrar_tabla(call.message, anterior, siguiente)
    
  # si se presiona el emoji  de siguiente '⏭️'
  elif call.data.startswith("siguiente"):
    # Desempaquetar los valores de call.data
    _, anterior, siguiente, paginas = call.data.split(' ')
    
    # Convertir los valores a enteros
    anterior = int(anterior)
    siguiente = int(siguiente)
    paginas = int(float(paginas))

    # Verificar si 'siguiente' supera el número de páginas
    if siguiente > paginas:
        anterior = 0
        siguiente = 2
    else:
        # Incrementar los valores de 'anterior' y 'siguiente'
        anterior += 1
        siguiente += 1

    # Mostramos la tabla
    mostrar_tabla(call.message, anterior, siguiente)

  # si se presiona el emoji  de nuevo 'nuevo'
  elif call.data.startswith('nuevo'):
    bot.send_message(call.message.chat.id, 'Cual es el nombre del producto?')
    producto[call.message.chat.id] = {}
    bot.register_next_step_handler(call.message, nuevo_producto_precio)
    
  # si se presiona el emoji  de eliminar '❌'
  elif call.data.startswith('eliminar'):
    
    bot.delete_message(call.message.chat.id, call.message.message_id)
    
  elif call.data.startswith('refrescar'):
    # Desempaquetar los valores de call.data
    _, anterior, siguiente = call.data.split(' ')
    
    # Intentar mostrar la tabla    
    anterior = int(anterior)
    siguiente = int(siguiente) 
    
    try:
      mostrar_tabla(call.message, anterior , siguiente )
    except: # En caso de error
      bot.answer_callback_query(call.id, text="Tabla Actualizada")
    
  elif call.data.startswith('editar'):
    _,id = call.data.split(' ')
    #botonera reply
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, is_persistent=False)
    markup.add("Nombre", "Precio", "Stock")
    msg = bot.send_message(call.message.chat.id, 'Que desea editar?', reply_markup=markup)
    bot.register_next_step_handler(msg, editar_producto, id)
    print(call.data)
    
  elif call.data.startswith('nuevo'):
    msg = bot.send_message(call.message.chat.id, 'Cual es el nombre del producto?')
    producto[call.message.chat.id] = {}
    bot.register_next_step_handler(msg, nuevo_producto_precio)
  
def editar_producto(message, id):
    # opciones disponibles 
    opciones = {
      'Nombre': ('Cual es el nuevo nombre del producto?', 'B'),
      'Precio': ('Cual es el nuevo precio del producto?', 'C'),
      'Stock': ('Cual es el nuevo stock del producto?', 'D')
    }
    # opcion seleccionada por el usuario. 
    opcion = message.text
    print (opcion)
    
    # validar que la opcion elegida por el usuario es valida. 
    if opcion in opciones:
      
       nuevo, columna = opciones[opcion]
       
       msg = bot.send_message(message.chat.id, nuevo)
       
       bot.register_next_step_handler(msg, enviar_producto, id , columna)
    else:
      # si la opcion no es valida mostrar un mensaje de error y volver a escoger la opcion valida.
      msg = bot.send_message(message.chat.id, 'Opcion no valida, por favor escoja una de las 3 opciones') 
      bot.register_next_step_handler(msg, editar_producto)
      
      
def enviar_producto(mensaje, id, columna):
  
  # Enviamos el valor a editar

  resultados = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='Hoja 1!A2:A').execute()

  valores = resultados.get('values', [])

  flat_list = np.array(valores).flatten()

  indice = np.where(flat_list == id)[0]

  if len(indice) == 0:
    msg = bot.send_message(mensaje.chat.id, 'No se encontro el id ingresado')
    bot.register_next_step_handler(msg, editar_producto)
    return
  
  fila = indice[0] + 2

  ubicacion = f'Hoja 1!{columna}{fila}:{columna}{fila}' # Ejemplo Hoja 1!B2:B2
  
  sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=ubicacion, valueInputOption='USER_ENTERED', body={'values': [[mensaje.text]]}).execute()

  bot.send_message(mensaje.chat.id, 'Se actualizo correctamente el dato ✅')

  
  
#<-------------------- Funcion que se encarga de iniciar el bot
def inicioBot():
  bot.infinity_polling()# iniciamos un bucle infinito que comprueba si el bot recibe nuevos mensajes
  # a partir de aqui, no se ejecutaria ninguna otra linea debido al bucle infinito (bot.infinity_polling())
  print(__name__)
    
#< --------------------  Progama inicial 
if __name__ == '__main__':
  print('Iniciando el bot...') # mostramos un mensaje por la terminal
  hilo_inicio = threading.Thread(name = 'bot', target=inicioBot) # creamos un hilo para iniciar el bot
  hilo_inicio.start()
  bot.send_message(TELEGRAM_CHAT_ID, 'Bot iniciado')
  print ('Bot iniciado')






