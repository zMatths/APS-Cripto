import random
from math import gcd  

def totient(p, q):
    return (p - 1) * (q - 1)

def prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_E(tot):
    while True:
        e = random.randrange(2, tot)
        if gcd(tot, e) == 1:
            return e

def generate_prime():
    while True:
        x = random.randrange(1, 100)
        if prime(x):
            return x

def mod(a, b):
    return a % b

def cipher(words, e, n):
    return [mod(ord(letter) ** e, n) for letter in words]

def descifra(cifra, n, d):
    return ''.join(chr(mod(num ** d, n)) for num in cifra)

def calculate_private_key(tot, e):
    d = 0
    while mod(d * e, tot) != 1:
        d += 1
    return d

def welcome():
    print("**********************************************")
    print("*****Entrando no programa de criptografia*****")
    print("**********************************************")

def register_user(users):
    print("Cadastro:")
    usuario_cadastrado = input("Digite seu nome para cadastro: ")
    senha_cadastrada = input("Crie uma senha: ")
    
    users.append((usuario_cadastrado, senha_cadastrada))
    print("Usuário cadastrado com sucesso!")

def login(users):
    print("Login:")
    usuario = input("Digite seu usuário: ")
    senha = input("Digite sua senha: ")

    # Check if user exists
    for registered_user, registered_password in users:
        if usuario == registered_user and senha == registered_password:
            print("Login realizado com sucesso!")
            return registered_user, registered_password

    print("Erro: Usuário ou senha incorretos.")
    return None, None

def main():
    users = []
    welcome()

    while True:
        action = input("Você deseja (c)adastrar um novo usuário ou (l)ogar? (c/l): ")
        
        if action.lower() == 'c':
            register_user(users)
        elif action.lower() == 'l':
            usuario, senha = login(users)
            if usuario and senha:
                # Generate keys and encrypt/decrypt messages
                p = generate_prime() 
                q = generate_prime()  
                n = p * q             
                tot = totient(p, q)  
                e = generate_E(tot) 

                public_key = (n, e)
                print('Sua chave pública:', public_key) 

                n_input = int(input("Digite o valor de N da chave pública: "))
                e_input = int(input("Digite o valor de E da chave pública: "))

                if n_input == n and e_input == e:
                    text = input("Insira a mensagem: ")
                    text_cipher = cipher(text, e_input, n_input)
                    print('Sua mensagem criptografada:', text_cipher)

                    d = calculate_private_key(tot, e)

                    senhax = input("Digite sua senha de login para a chave privada: ") 
                    if senhax == senha:
                        print('Sua chave privada é:', d)
                        d_input = int(input("Digite sua chave privada para descriptografar a mensagem: "))
                        if d_input == d: 
                            original_text = descifra(text_cipher, n_input, d_input)
                            print('Sua mensagem original:', original_text)
                        else:
                            print("Descriptografia cancelada: chave privada incorreta.")
                    else:
                        print("Senha incorreta. Acesso negado.")
                else:
                    print("Criptografia cancelada: chave pública incorreta.")
        else:
            print("Opção inválida! Tente novamente.")

        # Ask if the user wants to continue
        continuar = input("Deseja continuar? (s/n): ")
        if continuar.lower() != 's':
            print('Vejo você depois!')
            break

main()
