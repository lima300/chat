import socket 
import select 
import sys 
  
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

HOST = input("Digite o IP do servidor: ")
PORT = 5000
server.connect((HOST, PORT)) 
  
while True: 
  
    # lista para guardar as opções de input strems.
    socket_list = [sys.stdin, server] 
  
    """ Existem duas situações de entrada possíveis. Tanto o
    o usuário deseja fornecer dados manuais para enviar para outras pessoas,
    ou o servidor está enviando uma mensagem para ser impressa na
    tela. A função select então seleciona os retornos de sockets_list, o input stream a ser tratado.
    Por exemplo, se o servidor quiser
    para enviar uma mensagem, então a condição if se manterá verdadeira
    abaixo. Se o usuário deseja enviar uma mensagem, a condição else será avaliada como verdadeira"""
    read_sockets,write_socket, error_socket = select.select(socket_list,[],[]) 
    
    """ Para cada entrada presente na lista read_sockets tratar se é uma menssagem recebida pelo servidor 
    ou se é uma entrada manual realizada pelo usuário"""
    for sock in read_sockets:
        if sock == server: 
            message = sock.recv(2048) 
            print (message.decode()) 
        else:
            # lê a mensagem digitada pelo usuário
            message = sys.stdin.readline()
            #checa se o usuário quer sair. Em caso negativo imprime a menssagem na tela e a envia para o servidor
            #em caso positivo para o loop for.
            if message != "sair\n":
                server.send(message.encode())
                sys.stdout.write("<YOU> " + message )
            else:
                break
    # caso o usuário tenha digitado sair encerra o programa.      
    if message == "sair\n":
        break
server.close() 