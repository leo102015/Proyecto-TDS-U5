from PyQt5 import uic, QtWidgets
import sys
import mysql
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QPixmap
import mysql.connector
import subprocess
from PyQt5.QtCore import QTimer

# Conexión a la base de datos
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Previus22",
        database="TDS_db"
    )


# Clase principal de la aplicación
class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('autos.ui', self)  # Cargar el archivo .ui        

        # Configuración inicial
        self.setWindowTitle("Rentas de Autos")
        self.load_clients()
        self.load_autos()
        self.load_companies()

        # Configuración del temporizador para actualizaciones automáticas
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.load_clients)  # Llama a load_clients periódicamente
        self.timer.start(5000)  # Intervalo de 5 segundos (ajústalo según sea necesario)

        # Validaciones de entrada
        self.lineEdit_2.setValidator(QDoubleValidator(0.0, 999999.99, 2, self))
        self.spinBox.valueChanged.connect(self.update_total)
        self.lineEdit_2.textChanged.connect(self.update_total)
        self.comboBox_2.currentTextChanged.connect(self.update_price)

        # Conexión de botones
        self.pushButton.clicked.connect(self.on_button_click)  # Espacio para código adicional
        self.pushButton_3.clicked.connect(self.save_rental)

    def load_clients(self):
        try:
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT CONCAT(nombre, ' ', apellido) AS cliente FROM Clientes")
            clients = cursor.fetchall()
            self.comboBox.clear()  # Limpia el ComboBox antes de agregar nuevos elementos
            self.comboBox.addItems([client[0] for client in clients])
        except Exception as e:
            print("Error cargando clientes:", e)
        finally:
            connection.close()

    def load_autos(self):
        try:
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT clave_auto FROM Autos WHERE disponible = 1")
            autos = cursor.fetchall()
            self.comboBox_2.addItems([auto[0] for auto in autos])
        except Exception as e:
            print("Error cargando autos:", e)
        finally:
            connection.close()

    def load_companies(self):
        try:
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT nombre FROM CompaniasAseguradoras")
            companies = cursor.fetchall()
            self.comboBox_3.addItems([company[0] for company in companies])
        except Exception as e:
            print("Error cargando compañías aseguradoras:", e)
        finally:
            connection.close()

    def update_price(self):
        """Actualiza el precio del auto seleccionado."""
        try:
            connection = create_connection()
            cursor = connection.cursor()
            auto_key = self.comboBox_2.currentText()
            cursor.execute("SELECT precio_por_dia FROM Autos WHERE clave_auto = %s", (auto_key,))
            price = cursor.fetchone()
            if price:
                self.lineEdit.setText(str(price[0]))  # Actualiza el precio en lineEdit
            else:
                self.lineEdit.clear()
            self.update_total()  # Recalcular el total inmediatamente
        except Exception as e:
            print("Error actualizando precio:", e)
        finally:
            connection.close()

    def update_total(self):
        """Calcula el total con base en el precio, días y cargo extra."""
        try:
            # Obtener datos
            price = float(self.lineEdit.text()) if self.lineEdit.text() else 0.0
            days = self.spinBox.value()
            extra_charge = float(self.lineEdit_2.text()) if self.lineEdit_2.text() else 0.0

            # Calcular total
            total = (price * days) + extra_charge
            self.lineEdit_3.setText(f"{total:.2f}")  # Actualiza el total
        except ValueError:
            self.lineEdit_3.clear()  # Limpia si hay un error en los datos

    def on_button_click(self):
        # Ejecutar el archivo clientes.py
        subprocess.run(['python', 'Clientes.py'])   

    def save_rental(self):
        client = self.comboBox.currentText()
        auto_key = self.comboBox_2.currentText()
        company = self.comboBox_3.currentText()
        price = self.lineEdit.text()
        days = self.spinBox.value()
        extra_charge = self.lineEdit_2.text()
        total = self.lineEdit_3.text()

        if not (client and auto_key and company and price and days and extra_charge and total):
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor llena todos los campos.")
            return

        try:
            connection = create_connection()
            cursor = connection.cursor()

            # Obtener IDs necesarios
            cursor.execute("SELECT id_cliente FROM Clientes WHERE CONCAT(nombre, ' ', apellido) = %s", (client,))
            client_id = cursor.fetchone()[0]
            cursor.execute("SELECT id_auto FROM Autos WHERE clave_auto = %s", (auto_key,))
            auto_id = cursor.fetchone()[0]
            cursor.execute("SELECT id_compania FROM CompaniasAseguradoras WHERE nombre = %s", (company,))
            company_id = cursor.fetchone()[0]

            # Insertar en la tabla Rentas
            cursor.execute("""
                INSERT INTO Rentas (id_cliente, id_auto, id_compania, fecha_devolucion, garantia, total)
                VALUES (%s, %s, %s, DATE_ADD(CURRENT_DATE, INTERVAL %s DAY), %s, %s)
            """, (client_id, auto_id, company_id, days, extra_charge, total))
            connection.commit()
            QtWidgets.QMessageBox.information(self, "Éxito", "Renta guardada correctamente.")
        except Exception as e:
            print("Error guardando renta:", e)
            QtWidgets.QMessageBox.critical(self, "Error", "No se pudo guardar la renta.")
        finally:
            connection.close()



# Inicialización de la aplicación
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
