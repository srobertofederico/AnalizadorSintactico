import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QWidget, QTextEdit, QPushButton, QLabel, QScrollArea, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from domain.token import lexer
from domain.parser import parser
from domain.tree import build_tree, draw_tree
from domain.graph import graficar_afd, graficar_afn

# Define la clase principal de la aplicación
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Configura la ventana principal
        self.setWindowTitle("Compilador")
        self.setGeometry(100, 100, 800, 600)

        # Layout principal
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)

        # Botón para cargar un archivo
        self.uploadButton = QPushButton('Subir Archivo', self)
        self.uploadButton.clicked.connect(self.ev_archivo)
        self.layout.addWidget(self.uploadButton)

        # Área de texto para el código fuente
        self.codigoFuente = QTextEdit(self)
        self.layout.addWidget(QLabel('Codigo Fuente', self))
        self.layout.addWidget(self.codigoFuente)

        # Área de texto para el análisis léxico
        self.analisisLexico = QTextEdit(self)
        self.analisisLexico.setReadOnly(True)
        self.layout.addWidget(QLabel('Analisis Lexico', self))
        self.layout.addWidget(self.analisisLexico)

        # Área de texto para el análisis sintáctico
        self.analisisSintactico = QTextEdit(self)
        self.analisisSintactico.setReadOnly(True)
        self.layout.addWidget(QLabel('Analisis Sintactico', self))
        self.layout.addWidget(self.analisisSintactico)

        # Botón para iniciar el análisis léxico 
        self.analizarLexicoButton = QPushButton('Analizar Lexico', self)
        self.analizarLexicoButton.clicked.connect(self.ev_lexico)
        self.layout.addWidget(self.analizarLexicoButton)

        # Botón para iniciar el análisis sintáctico
        self.analizarSintacticoButton = QPushButton('Analisis Sintactico', self)
        self.analizarSintacticoButton.clicked.connect(self.ev_sintactico)
        self.layout.addWidget(self.analizarSintacticoButton)

        # Botón para generar el árbol de derivación
        self.generarArbolButton = QPushButton('Generar Árbol de Derivación', self)
        self.generarArbolButton.clicked.connect(self.mostrar_arbol)
        self.layout.addWidget(self.generarArbolButton)

        # Botón para graficar AFD
        self.graficarAFDButton = QPushButton('Graficar AFD', self)
        self.graficarAFDButton.clicked.connect(self.graficar_afd)
        self.layout.addWidget(self.graficarAFDButton)

        # Botón para graficar AFN
        self.graficarAFNButton = QPushButton('Graficar AFN', self)
        self.graficarAFNButton.clicked.connect(self.graficar_afn)
        self.layout.addWidget(self.graficarAFNButton)
        
        # Función para manejar la carga de un archivo
    def ev_archivo(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Subir Archivo", "", "Text Files (*.txt);;All Files (*)", options=options)
        if fileName:
            with open(fileName, 'r') as file:
                data = file.read()
                self.codigoFuente.setText(data)
                
     # Función para realizar el análisis léxico
    def ev_lexico(self):
        self.analisisLexico.clear()
        data = self.codigoFuente.toPlainText()
        lexer.input(data)

        output = []
        line_number = 1  # Variable para llevar el número de línea
        while True:
            tok = lexer.token()
            if not tok:
                break
            # Si encontramos el token BREVE, incrementamos el número de línea
            if tok.type == 'BREVE':
                line_number += 1
            # Agregamos la información del token a la salida con el número de línea actual
            output.append(f"Linea {line_number}: \t Tipo: {tok.type} \t Valor: {tok.value} \t Posicion: {tok.lexpos} \n ")

        self.analisisLexico.setText("\n".join(output))



    # Función para realizar el análisis sintáctico
    def ev_sintactico(self):
        self.analisisSintactico.clear()
        data = self.codigoFuente.toPlainText()
        lexer.input(data)

        valores = []
        while True:
            tok = lexer.token()
            if not tok:
                break
            if tok.type in ['NUMBER', 'REAL', 'STRING', 'CHAR']:
                valores.append(str(tok.value))

        self.analisisSintactico.setText("\n".join(valores))

    # Función para mostrar el árbol de derivación
    def mostrar_arbol(self):
        data = self.codigoFuente.toPlainText()

        # Obtener solo la primera línea no vacía del código fuente
        first_line = ""
        for line in data.splitlines():
            if line.strip():
                first_line = line.strip()
                break

        if not first_line:
            print("No se encontró una línea válida para analizar.")
            return

        result = parser.parse(first_line, lexer=lexer)

        if result:
            # Construir el árbol de derivación
            tree = build_tree(result)

            # Dibujar el árbol de derivación
            graph = draw_tree(tree)
            graph.write_png('arbol_derivacion.png')

            # Mostrar el árbol en una ventana
            self.mostrar_imagen('arbol_derivacion.png')
        else:
            print("Error al analizar la línea para generar el árbol de derivación.")

    # Función para construir el AFD basado en la entrada
    def construir_afd(self, data):
        lexer.input(data)
        estados = ['q0']
        transiciones = []
        estado_actual = 'q0'
        estado_id = 1

        while True:
            tok = lexer.token()
            if not tok:
                break
            estado_siguiente = f'q{estado_id}'
            estados.append(estado_siguiente)
            transiciones.append((estado_actual, tok.type, estado_siguiente))
            estado_actual = estado_siguiente
            estado_id += 1

        afd = {
            'estados': estados,
            'estados_finales': [estado_actual],
            'transiciones': transiciones
        }
        return afd

    # Función para construir el AFN basado en la entrada
    def construir_afn(self, data):
        lexer.input(data)
        estados = ['q0']
        transiciones = []
        estado_actual = 'q0'
        estado_id = 1

        while True:
            tok = lexer.token()
            if not tok:
                break
            estado_siguiente_1 = f'q{estado_id}'
            estado_siguiente_2 = f'q{estado_id + 1}'
            estados.extend([estado_siguiente_1, estado_siguiente_2])
            transiciones.append((estado_actual, tok.type, estado_siguiente_1))
            transiciones.append((estado_actual, tok.type, estado_siguiente_2))
            estado_actual = estado_siguiente_1
            estado_id += 2

        afn = {
            'estados': estados,
            'estados_finales': [estado_actual],
            'transiciones': transiciones
        }
        return afn

    # Función para graficar AFD
    def graficar_afd(self):
        data = self.codigoFuente.toPlainText()
        afd = self.construir_afd(data)
        graficar_afd(afd, 'afd')
        self.mostrar_imagen('afd.png')

    # Función para graficar AFN
    def graficar_afn(self):
        data = self.codigoFuente.toPlainText()
        afn = self.construir_afn(data)
        graficar_afn(afn, 'afn')
        self.mostrar_imagen('afn.png')

    # Función para mostrar una imagen en una nueva ventana con scroll
    def mostrar_imagen(self, archivo_imagen):
        imagen_window = QMainWindow(self)
        imagen_window.setWindowTitle(archivo_imagen)

        scroll_area = QScrollArea(imagen_window)
        scroll_area.setWidgetResizable(True)

        imagen_label = QLabel()
        pixmap = QPixmap(archivo_imagen)
        imagen_label.setPixmap(pixmap)

        scroll_area.setWidget(imagen_label)
        imagen_window.setCentralWidget(scroll_area)
        imagen_window.resize(800, 600)
        imagen_window.show()

# Función principal para iniciar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())