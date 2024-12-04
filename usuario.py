import sys
import os
import mysql.connector
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QWidget
from PyQt5 import uic


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        current_dir = os.path.dirname(__file__)
        ui_file = os.path.join(current_dir, "us.ui")  # Archivo .ui de la ventana principal
        uic.loadUi(ui_file, self)

        # Conectar botones a las funciones
        self.btn_insertar.clicked.connect(self.open_insert_window)
        self.btn_listar.clicked.connect(self.open_list_window)
        self.btn_actualizar.clicked.connect(self.open_update_window)
        self.btn_eliminar.clicked.connect(self.open_delete_window)

    def open_insert_window(self):
        self.insert_window = InsertWindow()
        self.insert_window.show()

    def open_list_window(self):
        self.list_window = ListWindow()
        self.list_window.show()

    def open_update_window(self):
        self.update_window = UpdateWindow()
        self.update_window.show()

    def open_delete_window(self):
        self.delete_window = DeleteWindow()
        self.delete_window.show()


class InsertWindow(QWidget):
    def __init__(self):
        super(InsertWindow, self).__init__()
        current_dir = os.path.dirname(__file__)
        ui_file = os.path.join(current_dir, "insertar.ui")  # Archivo .ui para insertar
        uic.loadUi(ui_file, self)

        # Conectar botón a la función
        self.btn_insertar.clicked.connect(self.insert_user)

    def insert_user(self):
        nombre = self.input_nombre.text()
        contraseña = self.input_contraseña.text()

        if not nombre or not contraseña:
            QMessageBox.warning(self, "Advertencia", "Los campos no pueden estar vacíos.")
            return

        try:
            con = mysql.connector.connect(host="localhost", user="root", password="Previus22", database="TDS_db")
            query = "INSERT INTO usuarios (nombre_usuario, contraseña) VALUES (%s, %s)"
            cursor = con.cursor()
            cursor.execute(query, (nombre, contraseña))
            con.commit()
            con.close()
            QMessageBox.information(self, "Éxito", "Usuario insertado exitosamente.")
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Error al insertar usuario: {e}")


class ListWindow(QWidget):
    def __init__(self):
        super(ListWindow, self).__init__()
        current_dir = os.path.dirname(__file__)
        ui_file = os.path.join(current_dir, "list.ui")  # Archivo .ui para listar
        uic.loadUi(ui_file, self)

        # Conectar botón a la función
        self.btn_listar.clicked.connect(self.list_users)

    def list_users(self):
        try:
            con = mysql.connector.connect(host="localhost", user="root", password="Previus22", database="TDS_db")
            query = "SELECT * FROM usuarios"
            cursor = con.cursor()
            cursor.execute(query)
            usuarios = cursor.fetchall()
            con.close()

            output = "ID | Nombre de Usuario | Contraseña\n"
            output += "-" * 30 + "\n"
            for usuario in usuarios:
                output += f"{usuario[0]} | {usuario[1]} | {usuario[2]}\n"

            self.text_area.setText(output)
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Error al listar usuarios: {e}")


class UpdateWindow(QWidget):
    def __init__(self):
        super(UpdateWindow, self).__init__()
        current_dir = os.path.dirname(__file__)
        ui_file = os.path.join(current_dir, "actualizar.ui")  # Archivo .ui para actualizar
        uic.loadUi(ui_file, self)

        # Conectar botón a la función
        self.btn_actualizar.clicked.connect(self.update_user)

    def update_user(self):
        id_usuario = self.input_id.text()
        nuevo_nombre = self.input_nombre.text()
        nueva_contraseña = self.input_contraseña.text()

        if not id_usuario or not nuevo_nombre or not nueva_contraseña:
            QMessageBox.warning(self, "Advertencia", "Los campos no pueden estar vacíos.")
            return

        try:
            con = mysql.connector.connect(host="localhost", user="root", password="Previus22", database="TDS_db")
            query = "UPDATE usuarios SET nombre_usuario = %s, contraseña = %s WHERE id_usuario = %s"
            cursor = con.cursor()
            cursor.execute(query, (nuevo_nombre, nueva_contraseña, id_usuario))
            con.commit()
            con.close()
            QMessageBox.information(self, "Éxito", "Usuario actualizado exitosamente.")
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar usuario: {e}")


class DeleteWindow(QWidget):
    def __init__(self):
        super(DeleteWindow, self).__init__()
        current_dir = os.path.dirname(__file__)
        ui_file = os.path.join(current_dir, "eliminar.ui")  # Archivo .ui para eliminar
        uic.loadUi(ui_file, self)

        # Conectar botón a la función
        self.btn_eliminar.clicked.connect(self.delete_user)

    def delete_user(self):
        id_usuario = self.input_id.text()

        if not id_usuario:
            QMessageBox.warning(self, "Advertencia", "El campo ID no puede estar vacío.")
            return

        try:
            con = mysql.connector.connect(host="localhost", user="root", password="Previus22", database="TDS_db")
            query = "DELETE FROM usuarios WHERE id_usuario = %s"
            cursor = con.cursor()
            cursor.execute(query, (id_usuario,))
            con.commit()
            con.close()
            QMessageBox.information(self, "Éxito", "Usuario eliminado exitosamente.")
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Error al eliminar usuario: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
