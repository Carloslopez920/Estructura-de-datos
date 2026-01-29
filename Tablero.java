package juego; // Indica que la clase pertenece al paquete "juego"

public class Tablero {

    // Constantes que representan los tipos de celdas posibles en el mapa
    public static final int PARED = 1;       // Celda que representa una pared indestructible
    public static final int MURO = 2;        // Celda que representa un muro destruible
    public static final int VACIO = 0;       // Celda vacía, donde el jugador puede moverse
    public static final int EXPLOSION = 3;   // Celda donde ocurrió una explosión

    // Matriz que representa el mapa del tablero
    private int[][] mapa;

    // Constructor que recibe el número de filas y columnas del tablero
    public Tablero(int filas, int columnas) {
        mapa = new int[filas][columnas]; // Se crea la matriz que contendrá el mapa
        inicializarMapa(); // Se llama al método que llena el mapa con los valores iniciales
    }

    // Método que inicializa el contenido del mapa con paredes, muros y espacios vacíos
    private void inicializarMapa() {
        // Recorremos todas las posiciones de la matriz (filas y columnas)
        for (int i = 0; i < mapa.length; i++) {
            for (int j = 0; j < mapa[i].length; j++) {

                // --- Bordes del mapa ---
                // Las celdas de los bordes (primeras y últimas filas/columnas) son paredes fijas
                if (i == 0 || j == 0 || i == mapa.length - 1 || j == mapa[i].length - 1) {
                    mapa[i][j] = PARED;

                // --- Muros interiores "fijos" ---
                // Se colocan paredes en posiciones pares para formar un patrón ajedrezado
                } else if (i % 2 == 0 && j % 2 == 0) {
                    mapa[i][j] = PARED;

                // --- Muros aleatorios ---
                // Con una probabilidad del 20% se coloca un muro destruible
                } else if (Math.random() < 0.2) {
                    mapa[i][j] = MURO;

                // --- Espacios vacíos ---
                // Si no se cumple ninguna condición anterior, se deja el espacio vacío
                } else {
                    mapa[i][j] = VACIO;
                }
            }
        }

        // --- Zona inicial del jugador ---
        // Estas celdas se dejan vacías para que el jugador pueda moverse al comenzar el juego
        mapa[7][1] = VACIO;
        mapa[6][1] = VACIO;
        mapa[8][1] = VACIO;
        mapa[7][2] = VACIO;
    }

    // --- Métodos de acceso (Getters y Setters) ---

    // Devuelve el valor de una celda específica del mapa
    public int getValor(int fila, int columna) {
        return mapa[fila][columna];
    }

    // Cambia el valor de una celda específica del mapa
    public void setValor(int fila, int columna, int valor) {
        mapa[fila][columna] = valor;
    }

    // Devuelve el número total de filas del mapa
    public int getFilas() {
        return mapa.length;
    }

    // Devuelve el número total de columnas del mapa
    public int getColumnas() {
        return mapa[0].length;
    }
}
