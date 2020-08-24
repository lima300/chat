# Python program to implement server side of chat room. 
import socket 
import select 
import sys 
from _thread import *


HOST = '' 
PORT = 5000

# Criação do socket TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

# Atribui endereço e porta ao socket
server.bind((HOST, PORT)) 

# Abre socket para conexão com até 7 clients na fila
server.listen(100) 

# Lista para armazenar todos os clientes
client_list = [] 


def clientthread(connection, addr): 

	# Manda uma menssagem de boas vindas ao cliente recem conectado
	connection.send(("Seja bem Vindo ao chat!").encode()) 

	while True: 
			try: 
				message = connection.recv(2048) 
				if message and message.decode() != "sair\n": 
					"""Imprime a menssagem e o endereço do cliente no  terminal do servidor"""
					print ("<" + addr[0] + "> " + message.decode()) 

					"""Trata a mensagem a ser enviada para que ela tenha o mesmo formato impresso no terminal do servidor
					e em seguida chama a função que realiza o broadcast para todos os clientnes conectados"""
					message_to_send = "<" + addr[0] + "> " + message.decode() 
					broadcast(message_to_send, connection) 

				else: 
					"""A menssagem não tem conteúdo se a conexão com o cliente foi perdida, então ness caso
					removemos ele da lista de clientes, enviamos uma menssagem dizendo que o cliente deixou a sala
					e retornamos false para que a sua thread possa ser excluida"""
					message_to_send = "<" + addr[0] + "> deixou a sala ..."
					broadcast(message_to_send, connection) 
					remove(connection)
					return False

			except: 
				continue

""" A função abaixo é utilizada para realizar o broadcast de uma menssagem para todos os clientes
pertencentes na client_list cujo o objeto  seja diferente do objeto do emissor da menssagem"""
def broadcast(message, connection): 
	for client in client_list: 
		if client != connection: 
			try: 
				client.send(message.encode()) 
			except:
				#caso haja erro de envio para determinado cliente, fechamos a conexão 
				client.close() 
				remove(client)

"""A função a seguir simplesmente remove o objeto
da lista que foi criada no início de
o programa"""
def remove(connection): 
	if connection in client_list: 
		client_list.remove(connection) 

while True: 

	"""Aceita uma solicitação de conexão e armazena dois parâmetros,
	connection, que é um objeto socket para aquele usuário, e address
	que contém o endereço IP do cliente que acabou de conectar"""
	connection, address = server.accept() 

	"""aciona o socket do cliente que acabou de conectar para facilitar o broadcast das menssagens"""
	client_list.append(connection) 

	# imprime o endereço do cliente que acabou de conectar 
	print (address[0] + " connected")

	broadcast((address[0] + " connected"), connection)

	# cria uma thread individual para cada cliente conectado
	start_new_thread(clientthread,(connection,address))	 

connection.close() 
server.close() 
