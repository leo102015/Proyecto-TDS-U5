import sys
import os
import mysql.connector
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QWidget
from PyQt5 import uic
from prettytable import PrettyTable
import subprocess
class InicioWindow(QMainWindow):
    def __init__(self):
        super(InicioWindow, self).__init__()
        current_dir = os.path.dirname(__file__)
        ui_file = os.path.join(current_dir, "inicio.ui")  # Archivo .ui de la ventana principal
        uic.loadUi(ui_file, self)
        self.setStyleSheet(f"background-color: rgb(11, 200, 143);")

        self.inicio.clicked.connect(self.validar_usuario)
        self.registrarse.clicked.connect(self.open_registrarse_window)

        self.db_host = "localhost"  
        self.db_user = "root"       
        self.db_password = "Previus22"       
        self.db_name = "TDS_db"  

    def conectar_db(self):
        try:
            conexion = mysql.connector.connect(
                host=self.db_host,
                user=self.db_user,
                password=self.db_password,
                database=self.db_name
            )
            return conexion
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"No se pudo conectar a la base de datos: {e}")
            sys.exit(1)


    def validar_usuario(self):
        usuario = self.usuario.text()  
        contrasena = self.contrasena.text()  

        if not usuario or not contrasena:
            QMessageBox.warning(self, "Advertencia", "Por favor, ingresa tu usuario y contraseña.")
            return

        try:
            conexion = self.conectar_db()
            cursor = conexion.cursor()

            query = "SELECT * FROM usuarios WHERE nombre_usuario = %s AND contraseña = %s"
            cursor.execute(query, (usuario, contrasena))
            usuario = cursor.fetchone()

            if usuario:
                QMessageBox.information(self, "Éxito", "Inicio de sesión exitoso.")
                self.open_menu_window()
                window.close()
            else:
                QMessageBox.warning(self, "Error", "Correo o contraseña incorrectos.")

            cursor.close()
            conexion.close()

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"No se pudo realizar la consulta: {e}")


    def open_registrarse_window(self):
        self.reg_window = RegistroWindow()
        self.reg_window.show()        

    def open_menu_window(self):
        self.menu_window = MenuWindow()
        self.menu_window.show()


class RegistroWindow(QMainWindow):
    def __init__(self):
        super(RegistroWindow, self).__init__()
        current_dir = os.path.dirname(__file__)
        ui_file = os.path.join(current_dir, "registro.ui") 
        uic.loadUi(ui_file, self)
        self.insertar.clicked.connect(self.insert_user)

    def insert_user(self):
        nombre = self.usuario.text()
        contraseña = self.contrasena.text()
        
        if not nombre or not contraseña:
            QMessageBox.warning(self, "Advertencia", "Los campos no pueden estar vacíos.")
            return

        try:
            con = mysql.connector.connect(host="localhost", user="root", password="Previus22", database="TDS_db")
            query = "INSERT INTO usuarios(nombre_usuario, contraseña) VALUES (%s, %s)"
            cursor = con.cursor()
            cursor.execute(query, (nombre, contraseña))
            con.commit()
            con.close()
            QMessageBox.information(self, "Éxito", "Usuario insertado exitosamente.")            

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Error al insertar usuario: {e}")

    def open_menu_window(self):
        self.menu_window = MenuWindow()
        self.menu_window.show()

class MenuWindow(QMainWindow):
    def __init__(self):
        super(MenuWindow, self).__init__()
        current_dir = os.path.dirname(__file__)
        ui_file = os.path.join(current_dir, "menu.ui")  
        uic.loadUi (ui_file, self)

        self.usuarios.clicked.connect(self.open_main_window) #Referencia proyecto Paco
        self.renta.clicked.connect(self.open_rentas) #Referencia proyecto Paco
        self.clientes.clicked.connect(self.open_clientes)

    def open_main_window(self):
        subprocess.run(['python', 'usuario.py']) 
    
    def open_clientes(self):
        subprocess.run(['python', 'Clientes.py'])    

    def open_rentas(self):
        subprocess.run(['python', 'autos.py'])    


        



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InicioWindow()
    window.show()
    sys.exit(app.exec_())
