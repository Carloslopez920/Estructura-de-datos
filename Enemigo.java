package juego; // Indica que esta clase pertenece al paquete "juego"

public class Enemigo extends Personaje { 
    // La clase Enemigo hereda de la clase Personaje.
    // Por lo tanto, tiene las propiedades x, y, vivo y los métodos de movimiento.

    // --- Constructor ---
    public Enemigo(int x, int y) {
        // Llama al constructor de la clase padre (Personaje)
        // y establece las coordenadas iniciales del enemigo
        super(x, y);
    }

    // --- Método para mover automáticamente al enemigo ---
    public void moverEnemigos(Tablero tablero) {
        // Genera un número aleatorio entre 1 y 4 (ambos inclusive)
        // Esto servirá para decidir en qué dirección se moverá el enemigo
        int movimiento = 1 + (int) (Math.random() * 4);

        // Dependiendo del número, el enemigo se moverá en una dirección diferente
        switch (movimiento) {
            case 1:
                // Movimiento hacia arriba
                moverArriba(tablero); // Usa el método heredado de Personaje
                break;
            case 2:
                // Movimiento hacia abajo
                moverAbajo(tablero);
                break;
            case 3:
                // Movimiento hacia la derecha
                moverDerecha(tablero);
                break;
            case 4:
                // Movimiento hacia la izquierda
                moverIzquierda(tablero);
                break;
        }
    }
}
