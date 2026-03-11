class EvaluadorExpresiones:
    def __init__(self):
        self.pila = []
    
    def evaluar_posfija(self, expresion):
        """
        Evalúa una expresión en notación posfija (RPN)
        Ejemplo: "3 4 + 2 *" = (3+4)*2 = 14
        """
        self.pila = []
        tokens = expresion.split()
        
        for token in tokens:
            if token.replace('.', '').replace('-', '').isdigit():
                # Es un número
                if '.' in token:
                    self.pila.append(float(token))
                else:
                    self.pila.append(int(token))
            else:
                # Es un operador
                if len(self.pila) < 2:
                    raise ValueError("Expresión posfija inválida: operandos insuficientes")
                
                b = self.pila.pop()  # Segundo operando
                a = self.pila.pop()  # Primer operando
                
                resultado = self.aplicar_operador(token, a, b)
                self.pila.append(resultado)
        
        if len(self.pila) != 1:
            raise ValueError("Expresión posfija inválida: demasiados operandos")
        
        return self.pila[0]
    
    def evaluar_prefija(self, expresion):
        """
        Evalúa una expresión en notación prefija (polaca)
        Ejemplo: "* + 3 4 2" = (3+4)*2 = 14
        """
        self.pila = []
        tokens = expresion.split()
        
        # Recorremos de derecha a izquierda para prefija
        for token in reversed(tokens):
            if token.replace('.', '').replace('-', '').isdigit():
                # Es un número
                if '.' in token:
                    self.pila.append(float(token))
                else:
                    self.pila.append(int(token))
            else:
                # Es un operador
                if len(self.pila) < 2:
                    raise ValueError("Expresión prefija inválida: operandos insuficientes")
                
                a = self.pila.pop()  # Primer operando
                b = self.pila.pop()  # Segundo operando
                
                resultado = self.aplicar_operador(token, a, b)
                self.pila.append(resultado)
        
        if len(self.pila) != 1:
            raise ValueError("Expresión prefija inválida: demasiados operandos")
        
        return self.pila[0]
    
    def aplicar_operador(self, operador, a, b):
        """Aplica un operador a dos operandos"""
        if operador == '+':
            return a + b
        elif operador == '-':
            return a - b
        elif operador == '*':
            return a * b
        elif operador == '/':
            if b == 0:
                raise ZeroDivisionError("División por cero")
            return a / b
        elif operador == '^':
            return a ** b
        else:
            raise ValueError(f"Operador no soportado: {operador}")


class ProgramaPrincipal:
    @staticmethod
    def mostrar_menu():
        print("\n" + "="*50)
        print("EVALUADOR DE EXPRESIONES CON PILAS")
        print("="*50)
        print("1. Evaluar expresión en notación POSFIJA (1 1 +)")
        print("2. Evaluar expresión en notación PREFIJA (+ 1 1)")
        print("3. Salir")
        print("-"*50)
    
    @staticmethod
    def ejecutar():
        evaluador = EvaluadorExpresiones()
        
        while True:
            ProgramaPrincipal.mostrar_menu()
            opcion = input("Seleccione una opción (1-3): ").strip()
            
            if opcion == '1':
                expresion = input("\nIngrese expresión en notación POSFIJA: ").strip()
                try:
                    resultado = evaluador.evaluar_posfija(expresion)
                    print(f"\n✅ Resultado: {resultado}")
                except Exception as e:
                    print(f"\n❌ Error: {e}")
                    
            elif opcion == '2':
                expresion = input("\nIngrese expresión en notación PREFIJA: ").strip()
                try:
                    resultado = evaluador.evaluar_prefija(expresion)
                    print(f"\n✅ Resultado: {resultado}")
                except Exception as e:
                    print(f"\n❌ Error: {e}")
                
            elif opcion == '3':
                print("\n¡Hasta luego!")
                break
                
            else:
                print("\n❌ Opción no válida. Intente nuevamente.")
            
            input("\nPresione Enter para continuar...")


# Programa principal
if __name__ == "__main__":
    ProgramaPrincipal.ejecutar()