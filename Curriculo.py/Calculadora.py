#Faça uma calculadora que tenha adição,subtração,  multiplicação e divisão 
 #Quais serão as operações?
def calculadora():
    print("Selecione a operação:")
    print("+ para Adição")
    print("- para Subtração")
    print("* para Multiplicação")
    print("/ para Divisão")

    operacao = input("Digite a operação (+, -, *, /): ")
    
    # Verifica se a operação é válida
    if operacao not in ['+', '-', '*', '/']:
        print("Operação inválida!")
        return

    try:
        num1 = float(input("Digite o primeiro número: "))
        num2 = float(input("Digite o segundo número: "))
    except ValueError:
        print("Erro: Entrada inválida. Digite números.")
        return

    if operacao == '+':
        resultado = num1 + num2
    elif operacao == '-':
        resultado = num1 - num2
    elif operacao == '*':
        resultado = num1 * num2
    elif operacao == '/':
        # Tratamento para divisão por zero
        if num2 == 0:
            print("Erro: Divisão por zero!")
            return
        resultado = num1 / num2
        
    print("Resultado: {} {} {} = {}".format(num1, operacao, num2, resultado))

# Executar a calculadora
calculadora()
