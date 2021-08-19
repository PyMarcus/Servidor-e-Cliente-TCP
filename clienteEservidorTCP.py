import socket, sys, argparse


def cliente(ip, porta):
    """Um cliente  para conectar ao servidor"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('Erro ao criar o socket')
        sys.exit(1)
    else:
        try:
            sock.connect((ip, porta))  # tenta a conexão
        except socket.error:
            print('Conexão não estabelecida')
            sys.exit(1)
        else:
            print(f'Conectado ao host {ip} na porta {porta}')
            msg: str = 'Hallo! Wie geht es dir?'  # msg a ser enviada
            sock.sendall(msg.encode())
            sys.stdout.flush()  # limpa o buffer(q por padrão é limpo ao terminar da execução)
            # fecha o loop
            sock.shutdown(socket.SHUT_WR)
            while True:
                resposta = sock.recv(1024)
                if resposta:
                    print(f"O servidor respondeu: {resposta.decode()}")
                else:
                    break 
            sock.close()



def servidor(ip, porta):
    """Servidor tcp que recebe 1"""
    try:
        serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as erroConexao:
        print('Erro ao criar o socket')
        sys.exit(1)
    else:
        serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        serv.bind((ip, porta)) # atribui ao servidor o ip e a porta
        print(f"Escutando na porta {serv.getsockname()}")
        serv.listen(1)
        while True:
            sock, endCliente = serv.accept()
            print(f"Conectado ao cliente: {endCliente}")
            while True:
                recebido = sock.recv(1024)
                if not recebido:
                    break
                else:
                    print(f"O cliente {endCliente} diz: {recebido}")
                    sock.sendall(b"recebido")
                    sys.stdout.flush()
            print('Conexão encerrada.')
            sock.close()
            serv.close()
            break


if __name__ == '__main__':
    opcoes = {'cliente':cliente, 'servidor':servidor}
    parser = argparse.ArgumentParser(description='serv and client tcp')
    parser.add_argument('role', choices=opcoes, help='Void')
    parser.add_argument('host', help='void')
    parser.add_argument('-p', metavar='porta', type=int, default=6666, help='Porta padrão 666 + 6')

    arg = parser.parse_args()
    funcao = opcoes[arg.role]
    funcao(arg.host, arg.p)
