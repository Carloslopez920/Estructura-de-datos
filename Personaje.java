package juego;


public class Personaje {
    protected int x, y;
    protected boolean vivo = true;


    // Campos para animación
    protected int direccion = 0; // 0: abajo, 1: izquierda, 2: derecha, 3: arriba
    protected int frameAnimacion = 0;
    protected boolean isMoving = false;


    public Personaje(int x, int y) {
        this.x = x;
        this.y = y;
        this.direccion = 0; // Inicia mirando al frente (abajo)
    }
   
    // --- MÉTODOS DE MOVIMIENTO (CON 'isMoving = true') ---


    private void setDireccion(int nuevaDireccion) {
        if (this.direccion != nuevaDireccion) {
            this.direccion = nuevaDireccion;
            this.frameAnimacion = 0; // Reiniciar animación al cambiar dirección
        }
    }


    public void moverArriba(Tablero tablero) {
        int nuevaY = y - 1;
        if (isVivo() && nuevaY >= 0) {
            int celda = tablero.getValor(nuevaY, x);
            if (celda != Tablero.PARED && celda != Tablero.MURO) {
                this.setY(nuevaY);
                setDireccion(3); // 3: arriba
                this.isMoving = true;
            }
        }
    }


    public void moverAbajo(Tablero tablero) {
        int nuevaY = y + 1;
        if (isVivo() && nuevaY < tablero.getFilas()) {
            int celda = tablero.getValor(nuevaY, x);
            if (celda != Tablero.PARED && celda != Tablero.MURO) {
                this.setY(nuevaY);
                setDireccion(0); // 0: abajo
                this.isMoving = true;
            }
        }
    }


    public void moverDerecha(Tablero tablero) {
        int nuevaX = x + 1;
        if (isVivo() && nuevaX < tablero.getColumnas() ) {
            int celda = tablero.getValor(y, nuevaX);
            if (celda != Tablero.PARED && celda != Tablero.MURO) {
                this.setX(nuevaX);
                setDireccion(2); // 2: derecha
                this.isMoving = true;
            }
        }
    }
   
    public void moverIzquierda(Tablero tablero) {
        int nuevaX = x - 1;
        if (isVivo() && nuevaX >= 0) {
            int celda = tablero.getValor(y, nuevaX);
            if (celda != Tablero.PARED && celda != Tablero.MURO) {
                this.setX(nuevaX);
                setDireccion(1); // 1: izquierda
                this.isMoving = true;
            }
        }
    }


    // --- GETTERS Y SETTERS ---


    public int getX() {
        return x;
    }


    public int getY() {
        return y;
    }


    public void setX(int x) {
        this.x = x;
    }


    public void setY(int y) {
        this.y = y;
    }


    public boolean isVivo() {
        return vivo;
    }


    public void setVivo(boolean vivo) {
        this.vivo = vivo;
        if (!vivo) {
             this.frameAnimacion = 0; // Reiniciar animación (para muerte)
        }
    }


    public boolean colisionaConBomba(int fila, int columna) {
        return this.x == columna && this.y == fila;
    }
   
    // --- MÉTODOS DE ANIMACIÓN ---


    public int getDireccion() {
        return direccion;
    }


    public int getFrameAnimacion() {
        return frameAnimacion;
    }


    public boolean isMoving() {
        return isMoving;
    }


    public void setIdle() {
        this.isMoving = false;
        this.frameAnimacion = 0; // Reinicia al primer frame de "idle"
    }


    public void siguienteFrame() {
        // Asumiendo 4 frames por animación
        frameAnimacion = (frameAnimacion + 1) % 4;
    }
}

