package juego; // Indica que esta clase pertenece al paquete "juego"

import java.util.ArrayList;
import java.util.function.BiConsumer; // Interfaz funcional (recibe dos parámetros)
import javax.swing.Timer; // Clase de temporizador para manejar eventos con retardo

public class Bomba {
    // --- Atributos ---
    private int x, y;                // Coordenadas de la bomba en el tablero
    private int tiempoRestante;      // Tiempo antes de la explosión

    // --- Constructor ---
    public Bomba(int x, int y, int tiempoRestante) {
        this.x = x;                        // Posición horizontal
        this.y = y;                        // Posición vertical
        this.tiempoRestante = tiempoRestante; // Tiempo inicial antes de explotar
    }

    // --- Método para disminuir el contador ---
    public void tiempoRestante() {
        // Si aún hay tiempo, lo reducimos en 1 unidad
        if (tiempoRestante > 0) { 
            tiempoRestante--;
        }
    }

    // --- Método que indica si ya debe explotar ---
    public boolean explosion() {
        // Retorna true cuando el tiempo llega a 0
        return tiempoRestante == 0;
    }

    // --- Método principal: lógica de la explosión ---
    public void explotar(Tablero tablero, ArrayList<Jugador> jugadores, ArrayList<Enemigo> enemigos) {
        int radio = 2; // Radio de expansión de la explosión (número de celdas)
        
        // Marcamos el centro de la explosión en el tablero
        tablero.setValor(y, x, Tablero.EXPLOSION);

        /*
         * --- Interfaz funcional BiConsumer ---
         * Sirve para ejecutar una acción que recibe dos parámetros (posY, posX)
         * En este caso, se usa una función lambda para verificar si el jugador o
         * los enemigos fueron alcanzados por la explosión.
         * 
         * BiConsumer<Integer, Integer> actúa como una "plantilla de acción"
         * sin necesidad de escribir una clase aparte.
         */
        BiConsumer<Integer, Integer> verificarColisiones = (posY, posX) -> {
            // --- Verificar si el jugador está en la posición afectada ---
            for (Jugador j : jugadores) {
                if (j.colisionaConBomba(posY,posX)) {
                    j.setVivo(false);
                }
            }

            // --- Verificar si algún enemigo fue alcanzado ---
            for (Enemigo ene : enemigos) {
                if (ene.colisionaConBomba(posY, posX)) {
                    ene.setVivo(false); // El enemigo muere
                }
            }
        };

        // --- Expansión de la explosión en las 4 direcciones ---

        // 🔼 Hacia arriba
        for (int i = 1; i <= radio; i++) {
            if (y - i >= 0) { // Limita dentro del tablero
                int valor = tablero.getValor(y - i, x);
                if (valor == Tablero.PARED) break; // La explosión se detiene en paredes
                verificarColisiones.accept(y - i, x); // Ejecuta la acción lambda
                tablero.setValor(y - i, x, Tablero.EXPLOSION);
            }
        }

        // 🔽 Hacia abajo
        for (int i = 1; i <= radio; i++) {
            if (y + i < tablero.getFilas()) {
                int valor = tablero.getValor(y + i, x);
                if (valor == Tablero.PARED) break;
                verificarColisiones.accept(y + i, x);
                tablero.setValor(y + i, x, Tablero.EXPLOSION);
            }
        }

        // ◀️ Hacia la izquierda
        for (int i = 1; i <= radio; i++) {
            if (x - i >= 0) {
                int valor = tablero.getValor(y, x - i);
                if (valor == Tablero.PARED) break;
                verificarColisiones.accept(y, x - i);
                tablero.setValor(y, x - i, Tablero.EXPLOSION);
            }
        }

        // ▶️ Hacia la derecha
        for (int i = 1; i <= radio; i++) {
            if (x + i < tablero.getColumnas()) {
                int valor = tablero.getValor(y, x + i);
                if (valor == Tablero.PARED) break;
                verificarColisiones.accept(y, x + i);
                tablero.setValor(y, x + i, Tablero.EXPLOSION);
            }
        }

        /*
         * --- Limpieza de la explosión ---
         * Usamos un Timer que espera 300 ms antes de limpiar las celdas afectadas.
         * Esto da el efecto visual de la explosión temporal.
         */
        Timer t = new Timer(300, e -> {
            // Centro
            tablero.setValor(y, x, Tablero.VACIO);

            // Direcciones
            for (int i = 1; i <= radio; i++) {
                if (y - i >= 0 && tablero.getValor(y - i, x) == Tablero.EXPLOSION)
                    tablero.setValor(y - i, x, Tablero.VACIO);
                if (y + i < tablero.getFilas() && tablero.getValor(y + i, x) == Tablero.EXPLOSION)
                    tablero.setValor(y + i, x, Tablero.VACIO);
                if (x - i >= 0 && tablero.getValor(y, x - i) == Tablero.EXPLOSION)
                    tablero.setValor(y, x - i, Tablero.VACIO);
                if (x + i < tablero.getColumnas() && tablero.getValor(y, x + i) == Tablero.EXPLOSION)
                    tablero.setValor(y, x + i, Tablero.VACIO);
            }
        });

        // Solo se ejecuta una vez (no repite)
        t.setRepeats(false);
        t.start();
    }

    // --- Getters ---
    public int getX() {
        return x;
    }

    public int getY() {
        return y;
    }

    public int getTiempoRestante() {
        return tiempoRestante;
    }
}
