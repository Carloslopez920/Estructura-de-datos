package juego; // Indica que esta clase pertenece al paquete "juego"

import javax.swing.*; // Importa todas las clases del paquete javax.swing (para crear interfaces gráficas)

public class Main { // Declaración de la clase pública Main

    public static void main(String[] args) { // Método principal: punto de entrada del programa

        JFrame ventana = new JFrame("Bomberman"); 
        // Crea una ventana (objeto JFrame) con el título "Bomberman"

        Jugar juego = new Jugar(); 
        // Crea una instancia de la clase Jugar (donde está la lógica y gráficos del juego)

        ventana.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); 
        // Indica que al cerrar la ventana, el programa finaliza completamente

        ventana.add(juego); 
        // Agrega el panel del juego (objeto 'juego') al contenedor de la ventana

        ventana.pack(); 
        // Ajusta automáticamente el tamaño de la ventana al contenido interno (en este caso, el panel 'juego')

        ventana.setVisible(true); 
        // Hace visible la ventana en pantalla (por defecto está oculta)
    }
}
