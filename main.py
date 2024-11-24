import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QWidget, QTextEdit, QPushButton, QLabel, QScrollArea, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from domain.token import lexer
from domain.parser import parser
from domain.parser import p_error
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
        line_number = 1  # Variable to track line number
        error_message = None  # Variable to capture any error message
    
        while True:
            tok = lexer.token()
            
            if not tok:
                break
            
            if isinstance(tok, str):  # If tok is a string, it means we got an error message
                error_message = tok  # Capture the error message
                break  # Exit the loop because we've encountered an error
            
            # Check if the token is invalid and call t_error
            if tok.type == 'ERROR':  # 'ERROR' should be the token type for invalid tokens
                error_message = tok.value  # Capture the error message from t_error
                break  # Exit the loop since we've encountered an error
            
            # Add normal token information to output with current line number
            output.append(f"Linea {line_number}: \t Tipo: {tok.type} \t Valor: {tok.value} \t Posicion: {tok.lexpos} \n ")
    
        if error_message:
            # If an error occurred, show the error message in the GUI
            self.analisisLexico.setText(error_message)
        else:
            # If no error occurred, display the normal token output
            self.analisisLexico.setText("\n".join(output))





    # Función para realizar el análisis sintáctico
    def ev_sintactico(self):
        self.analisisSintactico.clear()  # Limpiar salida previa
        data = self.codigoFuente.toPlainText()  # Obtener código fuente
    
        # Verificar si hay código fuente
        if not data.strip():
            self.analisisSintactico.setText("No se encontró código fuente para analizar.")
            return
    
        try:
            # Limpiar líneas vacías y concatenar todo el programa
            cleaned_data = "\n".join(line.strip() for line in data.splitlines() if line.strip())
    
            # Realizar análisis sintáctico completo
            result = parser.parse(cleaned_data, lexer=lexer)
    
            if result:
                # Formatear el resultado del AST y mostrarlo
                formatted_ast = self.format_ast(result)
                self.analisisSintactico.setText(f"Árbol Sintáctico:\n{formatted_ast}")
            else:
                self.analisisSintactico.setText("ERROR: Error sintáctico\nNo se pudo generar el resultado del análisis sintáctico.")
        except Exception as e:
            # Capturar errores inesperados y mostrarlos
            self.analisisSintactico.setText(f"ERROR: {e}")


    def format_ast(self, node, indent=0):
        """Formatea el AST de manera compacta por línea de código."""
        spaces = "  " * indent  # Genera espacios para la indentación
        if isinstance(node, list):
            # Si es una lista, pon todos los elementos en una línea con comas
            formatted = ", ".join(self.format_ast(child, indent) for child in node)
            return f"{spaces}[{formatted}]"
        elif isinstance(node, tuple):
            # Si es una tupla, pon el nombre del nodo y sus elementos en una línea
            formatted_children = ", ".join(self.format_ast(child, indent) for child in node[1:])
            return f"{spaces}({node[0]}: {formatted_children})"
        else:
            # Para valores simples, devuelve con el valor directo
            return f"{spaces}{repr(node)}"


    # Función para mostrar el árbol de derivación
    def mostrar_arbol(self):
        data = self.codigoFuente.toPlainText()  # Obtener el código fuente

        # Verificar si hay código fuente
        if not data.strip():
            print("No se encontró código fuente para analizar.")
            return
    
        try:
            # Limpiar y concatenar líneas no vacías
            cleaned_data = "\n".join(line.strip() for line in data.splitlines() if line.strip())
    
            # Parsear el código completo
            result = parser.parse(cleaned_data, lexer=lexer)
    
            if result:
                # Construir el árbol de derivación
                tree = build_tree(result)
    
                # Dibujar el árbol de derivación
                graph = draw_tree(tree)
                graph.write_png('arbol_derivacion.png')
    
                # Mostrar el árbol en una ventana
                self.mostrar_imagen('arbol_derivacion.png')
            else:
                print("Error al analizar el código fuente.")
        except Exception as e:
            print(f"Error al construir o dibujar el árbol: {e}")


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