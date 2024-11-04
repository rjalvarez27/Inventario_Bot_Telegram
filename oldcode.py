'''
Este apartado es solo para ver como se trabaja en el bot con lo botones inline y reply sin google sheet. 
'''

from config import * # Importo la configuracion 
import telebot # para menjar la API de Telegran 
import threading # para crear un hilo
from telebot.types import InlineKeyboardMarkup # para crear el esquema de los botones
from telebot.types import ReplyKeyboardMarkup # crear botones reply
from telebot.types import InlineKeyboardButton # crear botones inline


#<-------------------- Instancia del bot
bot = telebot.TeleBot(TELEGRAM_TOKEN) # instancia del bot

#<-------------------- varibale global en la que guardamos los productos
producto = {}

#<-------------------- Definir funcion de botonera y como se ve en el bot
def botonera():
  markup = InlineKeyboardMarkup(row_width=5)
   #Botones
  # 1 2 3 4 5
  # ⏮️ ❌ ⏭️
  # nuevo 🔁 
  # Emojis: win + .
  b1 = InlineKeyboardButton('✏️', callback_data='editar')
  b2 = InlineKeyboardButton('✏️', callback_data='editar')
  b3 = InlineKeyboardButton('✏️', callback_data='editar')
  b4 = InlineKeyboardButton('✏️', callback_data='editar')
  b5 = InlineKeyboardButton('✏️', callback_data='editar')
  b6 = InlineKeyboardButton('⏮️', callback_data='anterior')
  b7 = InlineKeyboardButton('❌', callback_data='eliminar')
  b8 = InlineKeyboardButton('⏭️', callback_data='siguiente')
  
  b9 = InlineKeyboardButton('➕', callback_data='nuevo')
  b10 = InlineKeyboardButton('🔁', callback_data='refrescar')
  
  markup.add(b1, b2, b3, b4, b5)
  markup.add(b6, b7, b8)
  markup.add(b9, b10)
  
  return markup 
  
#<--------------------  Funcion que se encarga de responder al comando /start
@bot.message_handler(commands=['start']) # responde al comando start
def inicio(message):
  markup = botonera()
  bot.reply_to(message, f'Hola {message.from_user.first_name}, bienvenido a mi bot') # marca el mensaje y responde 'Hola, bienvenido a mi bot'
  bot.reply_to(message, f'Que desea hacer?')
  bot.send_message(message.chat.id, 'Marque la opcion de su preferencia o escriba /new para introducir lo datos manualmente', reply_markup=markup)
  print(message.from_user.first_name + ' ' + message.from_user.last_name) # Imprime el nombre del usuario
  print(message.chat.id) # Imprime el ID del chat
  
#<-------------------- Funcion que se encarga de responder al comando /new
@bot.message_handler(commands=['new']) # responde al comando new
def new(message):
  producto[message.chat.id] = {} # crea un diccionario vacio dentro de productos
  msg = bot.send_message(message.chat.id, 'Cual es el nombre del producto?')
  bot.register_next_step_handler(msg, nuevo_producto_precio) # registra el siguiente paso de la respuesta

def nuevo_producto_precio(message):
  producto[message.chat.id]["Nombre"] = message.text # guardamos el nombre en el diccionario 
  msg = bot.send_message(message.chat.id, 'Cual es el precio del producto?') 
  bot.register_next_step_handler(msg, nuevo_precio_stock) 
  
def nuevo_precio_stock(message):
  producto[message.chat.id]["Precio"] = message.text # guardamos el precio en el diccionario
  msg = bot.send_message(message.chat.id, 'Cual es el stock del producto?')
  bot.register_next_step_handler(msg, nuevo_final)

def nuevo_final(message):
  producto[message.chat.id]["Stock"] = message.text # guardamos el stock en el diccionario
  #crear una variables de productos
  nuevo_producto = f'''
  Nombre: {producto[message.chat.id]["Nombre"]}
  Precio: {producto[message.chat.id]["Precio"]}
  Stock: {producto[message.chat.id]["Stock"]}
  '''
  bot.send_message(message.chat.id, 'Se ha registrado el nuevo producto')
  bot.send_message(message.chat.id, nuevo_producto)
  print(producto)
  return


#<-------------------- ver los diferentes formatos cuando se escriba algun texto. 
''' 
Se Comento por que esto es de uso informativo para darle formato a los mensajes. 
@bot.message_handler(content_types=['text']) 
def listadeFormatos (message):
  # Formart HTML
  text_html = 'Negrita <b>Megrita</b>' + '\n'
  text_html += 'Cursiva <i>Cursiva</i>' + '\n'
  text_html += 'Subrayado <u>Subrayado</u>' + '\n'
  bot.send_message(message.chat.id, text_html, parse_mode= 'HTML')
  # Formart Markdown
  text_markdown = 'Negrita **Megrita**' + '\n'
  text_markdown += 'Cursiva *Cursiva*' + '\n'
  text_markdown += 'Subrayado _Subrayado_' + '\n'
  bot.send_message(message.chat.id, text_markdown, parse_mode= 'MarkdownV2')
'''
#< ------------------- Funcion que se encarga de responder a los botones (inline)
@bot.callback_query_handler(func=lambda call:True)
def call_back(call):
  # si se presiona el emoji  de anterior '⏮️'
  if call.data.startswith('anterior'):
    print('anterior')
  # si se presiona el emoji  de siguiente '⏭️'
  elif call.data.startswith('siguiente'):
    print('siguiente')
  # si se presiona el emoji  de nuevo 'nuevo'
  elif call.data.startswith('nuevo'):
    bot.send_message(call.message.chat.id, 'Cual es el nombre del producto?')
    producto[call.message.chat.id] = {}
    bot.register_next_step_handler(call.message, nuevo_producto_precio)
  # si se presiona el emoji  de eliminar '❌'
  elif call.data.startswith('eliminar'):
    bot.delete_message(call.message.chat.id, call.message.message_id)
  elif call.data.startswith('refrescar'):
    print('refrescar')
  elif call.data.startswith('editar'):
    #botonera reply
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, is_persistent=False)
    markup.add("Nombre", "Precio", "Stock")
    msg = bot.send_message(call.message.chat.id, 'Que desea editar?', reply_markup=markup)
    bot.register_next_step_handler(msg, editar_producto)
    print(call.data)
  elif call.data.startswith('nuevo'):
    msg = bot.send_message(call.message.chat.id, 'Cual es el nombre del producto?')
    producto[call.message.chat.id] = {}
    bot.register_next_step_handler(msg, nuevo_producto_precio)
  
def editar_producto(message):
    # opciones disponibles 
    opciones = {
      'Nombre': 'Cual es el nuevo nombre del producto?',
      'Precio': 'Cual es el nuevo precio del producto?',
      'Stock': 'Cual es el nuevo stock del producto?'
    }
    # opcion seleccionada por el usuario. 
    opcion = message.text
    # validar que la opcion elegida por el usuario es valida. 
    if opcion in opciones:
       nuevo = opciones[opcion]
       msg = bot.send_message(message.chat.id, nuevo)
       bot.register_next_step_handler(msg, enviar_producto )
    else:
      # si la opcion no es valida mostrar un mensaje de error y volver a escoger la opcion valida.
      markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, is_persistent=False)
      markup.add("Nombre", "Precio", "Stock")
      msg = bot.send_message(message.chat.id, 'Opcion no valida, por favor escoja una de las 3 opciones', reply_markup=markup) 
      bot.register_next_step_handler(msg, editar_producto)
      
      
def enviar_producto(message):
  print(message.text)
  
  
#<-------------------- Funcion que se encarga de iniciar el bot
def inicioBot():
  bot.infinity_polling()# iniciamos un bucle infinito que comprueba si el bot recibe nuevos mensajes
  # a partir de aqui, no se ejecutaria ninguna otra linea debido al bucle infinito (bot.infinity_polling())
    
#< --------------------  Progama inicial 
if __name__ == '__main__':
  print('Iniciando el bot...') # mostramos un mensaje por la terminal
  hilo_inicio = threading.Thread(name = 'bot', target=inicioBot) # creamos un hilo para iniciar el bot
  hilo_inicio.start()
  bot.send_message(TELEGRAM_CHAT_ID, 'Bot iniciado')
  print ('Bot iniciado')
 

