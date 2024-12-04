import sys
import os
import mysql.connector
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QWidget
from PyQt5 import uic


class AseguradoraWindow(QMainWindow):
    def __init__(self):
        super(AseguradoraWindow, self).__init__()
        current_dir = os.path.dirname(__file__)
        ui_file = os.path.join(current_dir, "aseguradora.ui")  # Archivo .ui de la ventana principal
        uic.loadUi(ui_file, self)

        # Conectar botones a las funciones
        self.insertar.clicked.connect(self.open_insert_window)
        self.listar.clicked.connect(self.open_list_window)
        self.actualizar.clicked.connect(self.open_update_window)
        self.eliminar.clicked.connect(self.open_delete_window)

    def open_insert_window(self):
        self.insert_window = InsertAsWindow()
        self.insert_window.show()

    def open_list_window(self):
        self.list_window = ListASWindow()
        self.list_window.show()

    def open_update_window(self):
        self.update_window = UpdateASWindow()
        self.update_window.show()

    def open_delete_window(self):
        self.delete_window = DeleteAsWindow()
        self.delete_window.show()


class InsertAsWindow(QMainWindow):
    def __init__(self):
        super(InsertAsWindow, self).__init__()
        current_dir = os.path.dirname(__file__)
        ui_file = os.path.join(current_dir, "insertAs.ui")  # Archivo .ui para insertar
        uic.loadUi(ui_file, self)

        # Conectar botón a la función
        self.btn_insertar.clicked.connect(self.insert_company)

    def insert_company(self):
        nombre = self.input_nombre.text()
        telefono = self.input_telefono.text()
        direccion = self.input_direccion.text()

     
        if not nombre or not telefono or not direccion:
            QMessageBox.warning(self, "Advertencia", "Todos los campos son obligatorios.")
            return

        try:
            with mysql.connector.connect(host="localhost", user="root", password="Previus22", database="TDS_db") as con:
                query = "INSERT INTO companiasaseguradoras (nombre, telefono, direccion) VALUES (%s, %s, %s)"
                cursor = con.cursor()
                cursor.execute(query, (nombre, telefono, direccion))
                con.commit()
            QMessageBox.information(self, "Éxito", "Compañía aseguradora insertada exitosamente.")

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Error al insertar la compañía: {e}")


class ListASWindow(QMainWindow):
    def __init__(self):
        super(ListASWindow, self).__init__()
        current_dir = os.path.dirname(__file__)
        ui_file = os.path.join(current_dir, "listAs.ui")  # Archivo .ui para listar
        uic.loadUi(ui_file, self)

        self.btn_listar.clicked.connect(self.list_companies)

    def list_companies(self):
        try:
            with mysql.connector.connect(host="localhost", user="root", password="Previus22", database="TDS_db") as con:
                query = "SELECT * FROM companiasaseguradoras"
                cursor = con.cursor()
                cursor.execute(query)
                companias = cursor.fetchall()

            output = "ID | Nombre               | Teléfono      | Dirección\n"
            output += "-" * 70 + "\n"
            for compania in companias:
                output += f"{compania[0]:<3} | {compania[1]:<20} | {compania[2]:<13} | {compania[3]}\n"


            self.text_area.setText(output)

        except mysql.connector.Error as e:

            QMessageBox.critical(self, "Error", f"Error al listar compañías: {e}")


class UpdateASWindow(QMainWindow): 
    def __init__(self):
        super(UpdateASWindow, self).__init__()
        current_dir = os.path.dirname(__file__)
        ui_file = os.path.join(current_dir, "actualizarAs.ui")  # Archivo .ui para actualizar
        uic.loadUi(ui_file, self)

        self.btn_actualizar.clicked.connect(self.update_company)

    def update_company(self):
        id_compania = self.input_id.text()
        nuevo_nombre = self.input_nombre.text()
        nuevo_telefono = self.input_telefono.text()
        nueva_direccion = self.input_direccion.text()


        if not id_compania or not nuevo_nombre or not nuevo_telefono or not nueva_direccion:
            QMessageBox.warning(self, "Advertencia", "Los campos no pueden estar vacíos.")
            return


        if not id_compania.isdigit():
            QMessageBox.warning(self, "Advertencia", "El ID debe ser un número entero.")
            return

        try:

            with mysql.connector.connect(host="localhost", user="root", password="Previus22", database="TDS_db") as con:
                query = "UPDATE CompaniasAseguradoras SET nombre = %s, telefono = %s, direccion = %s WHERE id_compania = %s"
                cursor = con.cursor()
                cursor.execute(query, (nuevo_nombre, nuevo_telefono, nueva_direccion, int(id_compania)))
                con.commit()

            QMessageBox.information(self, "Éxito", "Compañía actualizada exitosamente.")
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar compañía: {e}")


class DeleteAsWindow(QMainWindow):
    def __init__(self):
        super(DeleteAsWindow, self).__init__()
        current_dir = os.path.dirname(__file__)
        ui_file = os.path.join(current_dir, "eliminarAs.ui")  # Archivo .ui para eliminar
        uic.loadUi(ui_file, self)


        self.btn_eliminar.clicked.connect(self.delete_user)

    def delete_user(self):
        id_compania = self.input_id.text()

        if not id_compania:
            QMessageBox.warning(self, "Advertencia", "El campo ID no puede estar vacío.")
            return

        try:
            con = mysql.connector.connect(host="localhost", user="root", password="Previus22", database="TDS_db")
            query = "DELETE FROM companiasaseguradoras WHERE id = %s"
            cursor = con.cursor()
            cursor.execute(query, (id_compania))
            con.commit()
            con.close()
            QMessageBox.information(self, "Éxito", "Usuario eliminado exitosamente.")
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Error al eliminar usuario: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AseguradoraWindow()
    window.show()
    sys.exit(app.exec_())
