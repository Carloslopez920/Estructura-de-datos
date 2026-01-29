package juego; // Indica que esta clase pertenece al paquete "juego"

public class Jugador extends Personaje { 
    // La clase Jugador hereda de la clase Personaje
    // Esto significa que el jugador tiene todas las propiedades y métodos de Personaje (como x, y, moverArriba, etc.)

    // --- Constructor ---
    public Jugador(int x, int y) {
        // Llama al constructor de la clase padre (Personaje)
        // y le pasa las coordenadas iniciales del jugador
        super(x, y);
    }

    // --- Método para detectar colisiones con enemigos ---
    public boolean colisiona(Enemigo enemigo) {
        // Compara las coordenadas del jugador con las del enemigo
        // Si están en la misma posición (x e y iguales), hay colisión
        return this.x == enemigo.getX() && this.y == enemigo.getY();
    }
}
