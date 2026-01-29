package juego;


// Imports de Swing (ventanas, panel)
import javax.swing.JPanel;
import javax.swing.Timer;


// Imports de AWT (gráficos, eventos, utilidades)
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;


// Imports de Util (listas, conjuntos)
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Set;


// Imports de ImageIO (imágenes)
import java.awt.image.BufferedImage;
import javax.imageio.ImageIO;
import java.io.IOException; // Necesario para ImageIO


public class Jugar extends JPanel {
    private boolean gameOver = false;
    private Tablero tablero;


    // --- LÓGICA DE JUGADORES (MODIFICADO A PLURAL) ---
    private ArrayList<Jugador> jugadores;


    private ArrayList<Enemigo> enemigo;
    private ArrayList<Bomba> bombas;
    private final Set<Integer> teclasPresionadas = new HashSet<>();


    // --- VARIABLES DE VELOCIDAD DE MOVIMIENTO ---
    private int contadorMovimientoJugador = 0;
    // (Puedes cambiar el 2 por 3 si quieres que sea más lento)
    private static final int TICKS_PARA_MOVER = 1;


    private static final int TAMANO_CELDA = 32;


    // --- Sprites del Tablero ---
    private BufferedImage spriteVacio;
    private BufferedImage spritePared;
    private BufferedImage spriteMuro;
    private BufferedImage spriteExplosion;
    private BufferedImage spriteBomba;


    // --- Arrays de sprites para el JUGADOR ---
    private BufferedImage[][] framesJugador_Idle = new BufferedImage[4][4];
    private BufferedImage[][] framesJugador_Walk = new BufferedImage[4][4];
    private BufferedImage[] framesJugador_Death = new BufferedImage[4];
    private BufferedImage[] framesJugador_Win = new BufferedImage[4];


    // --- Arrays de sprites para el ENEMIGO ---
    private BufferedImage[][] framesEnemigo_Fly = new BufferedImage[4][4];


    // --- CONSTRUCTOR ---
    public Jugar() {
        tablero = new Tablero(13, 15);
        enemigo = new ArrayList<>();
        bombas = new ArrayList<>();


        // --- INICIALIZACIÓN DE MULTIJUGADOR OPCIONAL ---
        jugadores = new ArrayList<>();
        jugadores.add(new Jugador(1, 7)); // Solo el Jugador 1 empieza


        int anchoPanel = tablero.getColumnas() * TAMANO_CELDA;
        int altoPanel = tablero.getFilas() * TAMANO_CELDA;
        setPreferredSize(new Dimension(anchoPanel, altoPanel));


        setFocusable(true);


        // --- KEY LISTENER (PARA MULTIJUGADOR) ---
        addKeyListener(new KeyAdapter() {
            @Override
            public void keyPressed(KeyEvent e) {
                int key = e.getKeyCode();
                if (!teclasPresionadas.contains(key)) {
                    teclasPresionadas.add(key);
                }


                // Acciones de un solo pulso (Bombas, Reinicio, Unirse)
                if (!gameOver) {
                    // Jugador 1 pone bomba con ESPACIO
                    if (key == KeyEvent.VK_SPACE && jugadores.get(0).isVivo()) {
                        colocarBomba(jugadores.get(0));
                    }


                    // Jugador 2 pone bomba con ENTER (si existe)
                    if (key == KeyEvent.VK_ENTER && jugadores.size() > 1 && jugadores.get(1).isVivo()) {
                        colocarBomba(jugadores.get(1));
                    }


                    // Jugador 2 se une con "B"
                    if (key == KeyEvent.VK_B) {
                        spawnJugador2();
                    }
                }


                if (key == KeyEvent.VK_R && gameOver) {
                    reiniciarJuego();
                }
            }


            @Override
            public void keyReleased(KeyEvent e) {
                teclasPresionadas.remove(e.getKeyCode());


                // Revisar IDLE para Jugador 1 (WASD)
                if (!teclasPresionadas.contains(KeyEvent.VK_W) &&
                        !teclasPresionadas.contains(KeyEvent.VK_S) &&
                        !teclasPresionadas.contains(KeyEvent.VK_A) &&
                        !teclasPresionadas.contains(KeyEvent.VK_D)) {


                    if (jugadores.get(0).isVivo()) {
                        jugadores.get(0).setIdle();
                    }
                }


                // Revisar IDLE para Jugador 2 (Flechas) (si existe)
                if (jugadores.size() > 1) {
                    if (!teclasPresionadas.contains(KeyEvent.VK_UP) &&
                            !teclasPresionadas.contains(KeyEvent.VK_DOWN) &&
                            !teclasPresionadas.contains(KeyEvent.VK_LEFT) &&
                            !teclasPresionadas.contains(KeyEvent.VK_RIGHT)) {


                        if (jugadores.get(1).isVivo()) {
                            jugadores.get(1).setIdle();
                        }
                    }
                }
            }
        });


        cargarSprites();
        generarEnemigos(3);
        timer.setDelay(150); // Velocidad general del juego (puedes subirla a 200 o 250)
        timer.start();
        t.start();
    }


    // --- MÉTODOS DE UTILIDAD (Sprites) ---


    private void cortarFrames(BufferedImage[] arrayDestino, String path) throws IOException {
        BufferedImage hoja = ImageIO.read(getClass().getResource(path));
        for (int i = 0; i < arrayDestino.length; i++) {
            if (i * TAMANO_CELDA < hoja.getWidth()) {
                arrayDestino[i] = hoja.getSubimage(i * TAMANO_CELDA, 0, TAMANO_CELDA, TAMANO_CELDA);
            } else {
                arrayDestino[i] = arrayDestino[i - 1];
            }
        }
    }


    private void cargarSprites() {
        try {
            spriteVacio = ImageIO.read(getClass().getResource("/juego/Sprites/terrain/grass.png"));
            spritePared = ImageIO.read(getClass().getResource("/juego/Sprites/terrain/rock.png"));
            spriteMuro = ImageIO.read(getClass().getResource("/juego/Sprites/terrain/wall.png"));
            spriteBomba = ImageIO.read(getClass().getResource("/juego/Sprites/items/dynamite.png"));
            spriteExplosion = ImageIO.read(getClass().getResource("/juego/Sprites/fxs/explosion.png"));


            cortarFrames(framesJugador_Idle[0], "/juego/Sprites/character/idle-front.png"); // 0: abajo
            cortarFrames(framesJugador_Idle[1], "/juego/Sprites/character/idle-left.png"); // 1: izquierda
            cortarFrames(framesJugador_Idle[2], "/juego/Sprites/character/idle-right.png"); // 2: derecha
            cortarFrames(framesJugador_Idle[3], "/juego/Sprites/character/idle-back.png"); // 3: arriba


            cortarFrames(framesJugador_Walk[0], "/juego/Sprites/character/walk-front.png"); // 0: abajo
            cortarFrames(framesJugador_Walk[1], "/juego/Sprites/character/walk-left.png"); // 1: izquierda
            cortarFrames(framesJugador_Walk[2], "/juego/Sprites/character/walk-right.png"); // 2: derecha
            cortarFrames(framesJugador_Walk[3], "/juego/Sprites/character/walk-back.png"); // 3: arriba


            cortarFrames(framesJugador_Death, "/juego/Sprites/character/death-front.png");
            cortarFrames(framesJugador_Win, "/juego/Sprites/character/win-front.png");


            cortarFrames(framesEnemigo_Fly[0], "/juego/Sprites/bat/fly-front.png"); // 0: abajo
            cortarFrames(framesEnemigo_Fly[1], "/juego/Sprites/bat/fly-left.png"); // 1: izquierda
            cortarFrames(framesEnemigo_Fly[2], "/juego/Sprites/bat/fly-right.png"); // 2: derecha
            cortarFrames(framesEnemigo_Fly[3], "/juego/Sprites/bat/fly-back.png"); // 3: arriba


        } catch (Exception e) {
            System.err.println("Error fatal al cargar los sprites: " + e.getMessage());
            System.err.println("Verifica que la carpeta 'Sprites' esté dentro de 'src/juego'");
            e.printStackTrace();
            System.exit(1);
        }
    }


    // --- MÉTODOS DE LÓGICA DEL JUEGO ---


    private void generarEnemigos(int cantidad) {
        for (int i = 0; i < cantidad; i++) {
            int x, y;
            do {
                x = (int) (Math.random() * tablero.getColumnas());
                y = (int) (Math.random() * tablero.getFilas());
            } while (tablero.getValor(y, x) != Tablero.VACIO || (x == 1 && y == 7)); // Evitar spawn en jugador
            enemigo.add(new Enemigo(x, y));
        }
    }


    private void colocarBomba(Jugador j) { // Recibe qué jugador la pone
        if (j.isVivo())
            bombas.add(new Bomba(j.getX(), j.getY(), 3));
    }


    /**
     * Añade al Jugador 2 al juego si aún no existe.
     */
    private void spawnJugador2() {
        if (gameOver || jugadores.size() >= 2) {
            return;
        }
        System.out.println("¡Jugador 2 se ha unido!");
        int spawnX = tablero.getColumnas() - 2;
        int spawnY = tablero.getFilas() - 2;
        jugadores.add(new Jugador(spawnX, spawnY));
    }


    // --- GAME LOOP (TIMER) ---
    Timer timer = new Timer(250, e -> {


        if (gameOver) {
            // --- LÓGICA DE GAME OVER ---
            for (Jugador j : jugadores) {
                if (!j.isVivo() || todosEnemigosMuertos()) {
                    j.siguienteFrame();
                }
            }


        } else {
            // --- LÓGICA DEL JUEGO ACTIVO ---


            // 1. Revisa el input del jugador (con velocidad controlada)
            contadorMovimientoJugador++;


            if (contadorMovimientoJugador >= TICKS_PARA_MOVER) {
                // Movimiento Jugador 1 (WASD)
                Jugador j1 = jugadores.get(0);
                if (j1.isVivo()) {
                    if (teclasPresionadas.contains(KeyEvent.VK_W)) {
                        j1.moverArriba(tablero);
                        contadorMovimientoJugador = 0;
                    } else if (teclasPresionadas.contains(KeyEvent.VK_S)) {
                        j1.moverAbajo(tablero);
                        contadorMovimientoJugador = 0;
                    } else if (teclasPresionadas.contains(KeyEvent.VK_A)) {
                        j1.moverIzquierda(tablero);
                        contadorMovimientoJugador = 0;
                    } else if (teclasPresionadas.contains(KeyEvent.VK_D)) {
                        j1.moverDerecha(tablero);
                        contadorMovimientoJugador = 0;
                    }
                }


                // Movimiento Jugador 2 (Flechas) (si existe)
                if (jugadores.size() > 1) {
                    Jugador j2 = jugadores.get(1);
                    if (j2.isVivo()) {
                        if (teclasPresionadas.contains(KeyEvent.VK_UP)) {
                            j2.moverArriba(tablero);
                            contadorMovimientoJugador = 0;
                        } else if (teclasPresionadas.contains(KeyEvent.VK_DOWN)) {
                            j2.moverAbajo(tablero);
                            contadorMovimientoJugador = 0;
                        } else if (teclasPresionadas.contains(KeyEvent.VK_LEFT)) {
                            j2.moverIzquierda(tablero);
                            contadorMovimientoJugador = 0;
                        } else if (teclasPresionadas.contains(KeyEvent.VK_RIGHT)) {
                            j2.moverDerecha(tablero);
                            contadorMovimientoJugador = 0;
                        }
                    }
                }
            }


            // 2. Actualiza la animación de TODOS los jugadores
            for (Jugador j : jugadores) {
                if (j.isMoving()) {
                    j.siguienteFrame();
                }
            }


            // 4. Lógica de Enemigos (revisa colisión con TODOS)
            for (Enemigo en : enemigo) {
                if (en.isVivo()) {
                    en.moverEnemigos(tablero);
                    for (Jugador j : jugadores) {
                        if (j.isVivo() && j.colisiona(en)) {
                            j.setVivo(false);
                        }
                    }
                }
            }


            // 5. Lógica de Victoria / Game Over
            int jugadoresVivos = 0;
            for (Jugador j : jugadores) {
                if (j.isVivo()) {
                    jugadoresVivos++;
                }
            }


            if (jugadoresVivos == 0) {
                gameOver = true;
            } else if (todosEnemigosMuertos() && jugadoresVivos > 0) {
                gameOver = true;
            }


        } // <-- Cierre del 'else'


        repaint(); // Llama a repaint al final de cada tick


    }); // <-- Cierre del 'Timer'


    // 3. Lógica de Bombas (pasa la LISTA de jugadores)
    Timer t = new Timer(500, event -> {
        ArrayList<Bomba> bombasAEliminar = new ArrayList<>(); // Lista temporal de bombas que van a desaparecer


        for (Bomba bomba : bombas) {
            bomba.tiempoRestante();
            if (bomba.explosion()) {
                bomba.explotar(tablero, jugadores, enemigo); // <- MODIFICADO
                bombasAEliminar.add(bomba);
            }
        }
        bombas.removeAll(bombasAEliminar);
    });




    private boolean todosEnemigosMuertos() {
        for (Enemigo en : enemigo) {
            if (en.isVivo()) {
                return false;
            }
        }
        return true;
    }


    // --- MÉTODOS DE PANTALLA Y REINICIO ---


    private void gameOverFunction(Graphics g) {
        if (gameOver) {
            g.setColor(new Color(0, 0, 0, 150));
            g.fillRect(0, 0, getWidth(), getHeight());


            int jugadoresVivos = 0;
            for (Jugador j : jugadores) {
                if (j.isVivo()) {
                    jugadoresVivos++;
                }
            }


            String msg = "GAME OVER";
            if (jugadoresVivos > 0) { // Si al menos 1 sobrevivió, ganan
                msg = "¡VICTORIA!";
                g.setColor(Color.YELLOW);
            } else {
                g.setColor(Color.RED);
            }


            g.setFont(new Font("Arial", Font.BOLD, 40));
            FontMetrics fm = g.getFontMetrics();
            int msgX = (getWidth() - fm.stringWidth(msg)) / 2;
            int msgY = (getHeight() - fm.getHeight()) / 2 + fm.getAscent();
            g.drawString(msg, msgX, msgY);


            String restartMsg = "Presiona R para reiniciar";
            fm = g.getFontMetrics(new Font("Arial", Font.PLAIN, 20));
            int restartMsgX = (getWidth() - fm.stringWidth(restartMsg)) / 2;
            int restartMsgY = msgY + fm.getHeight() + 20;
            g.setColor(Color.WHITE);
            g.setFont(new Font("Arial", Font.PLAIN, 20));
            g.drawString(restartMsg, restartMsgX, restartMsgY);
        }
    }


    private void reiniciarJuego() {
        tablero = new Tablero(13, 15);


        // Vuelve a empezar solo con el Jugador 1
        jugadores.clear();
        jugadores.add(new Jugador(1, 7));


        enemigo.clear();
        generarEnemigos(3);
        bombas.clear();
        gameOver = false;
        repaint();
    }


    // --- MÉTODOS DE DIBUJADO ---


    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        dibujarTablero(g);
        dibujarBombas(g);
        dibujarJugadores(g); // <-- PLURAL
        dibujarEnemigos(g);
        gameOverFunction(g);
    }


    private void dibujarTablero(Graphics g) {
        for (int i = 0; i < tablero.getFilas(); i++) {
            for (int j = 0; j < tablero.getColumnas(); j++) {
                int x = j * TAMANO_CELDA;
                int y = i * TAMANO_CELDA;
                int valor = tablero.getValor(i, j);


                g.drawImage(spriteVacio, x, y, null);


                switch (valor) {
                    case Tablero.PARED:
                        g.drawImage(spritePared, x, y, null);
                        break;
                    case Tablero.MURO:
                        g.drawImage(spriteMuro, x, y, null);
                        break;
                    case Tablero.EXPLOSION:
                        g.drawImage(spriteExplosion, x, y, null);
                        break;
                }
            }
        }
    }


    // --- MÉTODO DE DIBUJADO EN PLURAL ---
    private void dibujarJugadores(Graphics g) {
        // Itera y dibuja a CADA jugador
        for (Jugador j : jugadores) {
            int x = j.getX() * TAMANO_CELDA;
            int y = j.getY() * TAMANO_CELDA;
            int dir = j.getDireccion();
            int frame = j.getFrameAnimacion();


            BufferedImage spriteADibujar = null;


            if (!j.isVivo()) {
                spriteADibujar = framesJugador_Death[frame];
            } else if (gameOver && j.isVivo()) { // Si el juego acabó y este jugador está vivo
                spriteADibujar = framesJugador_Win[frame];
            } else if (j.isMoving()) {
                spriteADibujar = framesJugador_Walk[dir][frame];
            } else {
                spriteADibujar = framesJugador_Idle[dir][frame];
            }


            if (spriteADibujar != null) {
                g.drawImage(spriteADibujar, x, y, null);
            } else {
                g.setColor(Color.MAGENTA);
                g.fillRect(x, y, TAMANO_CELDA, TAMANO_CELDA);
            }
        }
    }


    private void dibujarEnemigos(Graphics g) {
        for (Enemigo e : enemigo) {
            if (e.isVivo()) {
                int x = e.getX() * TAMANO_CELDA;
                int y = e.getY() * TAMANO_CELDA;
                int dir = e.getDireccion();
                int frame = e.getFrameAnimacion();


                BufferedImage spriteADibujar = framesEnemigo_Fly[dir][frame];


                if (spriteADibujar != null) {
                    g.drawImage(spriteADibujar, x, y, null);
                }
            }
        }
    }


    private void dibujarBombas(Graphics g) {
        g.setColor(Color.RED);
        for (Bomba bomba : bombas) {
            int x = bomba.getX() * TAMANO_CELDA;
            int y = bomba.getY() * TAMANO_CELDA;
            g.drawImage(spriteBomba, x, y, null);
        }
    }


} // <-- LLAVE FINAL DE LA CLASE JUGAR

