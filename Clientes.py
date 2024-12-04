import sys
import os
import mysql.connector
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QWidget,QTreeWidget, QTreeWidgetItem
from PyQt5 import uic



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        current_dir = os.path.dirname(__file__)
        ui_file = os.path.join(current_dir, "menu_clientes.ui")  
        uic.loadUi(ui_file, self)

        
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
        ui_file = os.path.join(current_dir, "insertar_clientes.ui")
        uic.loadUi(ui_file, self)

        
        self.btn_insertar.clicked.connect(self.insert_user)

    def insert_user(self):
        nombre = self.input_nombre.text()
        apellidos = self.input_apellidos.text()
        fecha = self.input_fecha.text()
        direccion = self.input_direccion.text()
        telefono = self.input_telefono.text()
        ine = self.input_ine.text()
        licencia = self.input_licencia.text()
        tarjeta_credito = self.input_tarjeta.text()
        

        if not nombre or not apellidos or not fecha or not direccion or not telefono or not ine or not licencia or not tarjeta_credito:
            QMessageBox.warning(self, "Advertencia", "Los campos no pueden estar vacíos.")
            return

        try:
            con = mysql.connector.connect(host="localhost", user="root", password="Previus22", database="TDS_db")
            query = "INSERT INTO Clientes (nombre,apellido,fecha_nacimiento,direccion,telefono,ine,licencia,tarjeta_credito) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor = con.cursor()
            cursor.execute(query, (nombre, apellidos, fecha, direccion, telefono, ine, licencia,tarjeta_credito))
            con.commit()
            con.close()
            QMessageBox.information(self, "Éxito", "Cliente insertado exitosamente.")
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Error al insertar cliente: {e}")


class ListWindow(QWidget):
    def __init__(self):
        super(ListWindow, self).__init__()
        current_dir = os.path.dirname(__file__)
        ui_file = os.path.join(current_dir, "list_clientes.ui")  
        uic.loadUi(ui_file, self)

        
        self.btn_listar.clicked.connect(self.list_clients)

    def list_clients(self):
        try:
            
            con = mysql.connector.connect(host="localhost", user="root", password="Previus22", database="TDS_db")
            query = "SELECT * FROM Clientes"
            cursor = con.cursor()
            cursor.execute(query)
            clientes = cursor.fetchall()
            con.close()

         
            self.treeView.clear()
            self.treeView.setHeaderLabels(["ID Cliente", "Nombre", "Apellido", "Fecha de Nacimiento", "Dirección", "Teléfono", "INE", "Licencia", "Tarjeta de Crédito"])

           
            for cliente in clientes:
               
                cliente_item = QTreeWidgetItem([
                    str(cliente[0]),    
                    cliente[1],         
                    cliente[2],         
                    str(cliente[3]),    
                    cliente[4],         
                    cliente[5],         
                    cliente[6],         
                    cliente[7],         
                    cliente[8]          
                ])
                self.treeView.addTopLevelItem(cliente_item)

           
             

        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Error al listar clientes: {e}")


class UpdateWindow(QWidget):
    def __init__(self):
        super(UpdateWindow, self).__init__()
        current_dir = os.path.dirname(__file__)
        ui_file = os.path.join(current_dir, "actualizar_clientes.ui")  
        uic.loadUi(ui_file, self)

        self.fill_client_id_combo()

        self.combo_cliente.currentIndexChanged.connect(self.load_client_data)

        self.btn_actualizar.clicked.connect(self.update_user)

    def fill_client_id_combo(self):
        """Llenar el ComboBox con los ID de los clientes."""
        try:
            con = mysql.connector.connect(host="localhost", user="root", password="Previus22", database="TDS_db")
            cursor = con.cursor()
            cursor.execute("SELECT id_cliente FROM Clientes")
            result = cursor.fetchall()
            self.combo_cliente.clear()  

            for row in result:
                self.combo_cliente.addItem(str(row[0]))  

            con.close()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Error al cargar los clientes: {e}")

    def load_client_data(self):
        """Cargar los datos del cliente en los QLineEdit cuando se selecciona un ID del ComboBox."""
        client_id = self.combo_cliente.currentText()

        if not client_id:
            return 

        try:
            con = mysql.connector.connect(host="localhost", user="root", password="Previus22", database="TDS_db")
            cursor = con.cursor()
            cursor.execute("SELECT nombre, apellido, fecha_nacimiento, direccion, telefono, ine, licencia, tarjeta_credito FROM Clientes WHERE id_cliente = %s", (client_id,))
            result = cursor.fetchone()

            if result:
                nombre, apellido, fecha_nacimiento, direccion, telefono, ine, licencia, tarjeta_credito = result
                
                
                if fecha_nacimiento:
                  fecha_nacimiento_str = fecha_nacimiento.strftime('%Y-%m-%d')  
                else:
                    fecha_nacimiento_str = ''
                
                self.input_nombre.setText(nombre)
                self.input_apellidos.setText(apellido)
                self.input_fecha.setText(fecha_nacimiento_str)
                self.input_direccion.setText(direccion)
                
                self.input_telefono.setText(telefono)
                self.input_ine.setText(ine)
                self.input_licencia.setText(licencia)
                self.input_tarjeta.setText(tarjeta_credito)
            else:
                QMessageBox.warning(self, "Advertencia", "Cliente no encontrado.")

            con.close()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Error al cargar los datos del cliente: {e}")

    def update_user(self):
        """Actualizar los datos del cliente seleccionado en la base de datos."""
        client_id = self.combo_cliente.currentText()
        nuevo_nombre = self.input_nombre.text()
        nuevo_apellido = self.input_apellidos.text()
        nueva_fecha_nacimiento = self.input_fecha.text()
        nueva_direccion = self.input_direccion.text()
        nuevo_telefono = self.input_telefono.text()
        nuevo_ine = self.input_ine.text()
        nueva_licencia = self.input_licencia.text()
        nueva_tarjeta_credito = self.input_tarjeta.text()

        if not client_id or not nuevo_nombre or not nuevo_apellido or not nueva_fecha_nacimiento or not nueva_direccion or not nuevo_telefono or not nuevo_ine or not nueva_licencia or not nueva_tarjeta_credito:
            QMessageBox.warning(self, "Advertencia", "Todos los campos deben ser completados.")
            return

      
        reply = QMessageBox.question(self, 'Confirmar actualización',
                                     f"¿Estás seguro de que deseas actualizar los datos del cliente con ID {client_id}?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return

        try:
            con = mysql.connector.connect(host="localhost", user="root", password="Previus22", database="TDS_db")
            cursor = con.cursor()
            query = """
                UPDATE Clientes
                SET nombre = %s, apellido = %s, fecha_nacimiento = %s, direccion = %s, telefono = %s, ine = %s, licencia = %s, tarjeta_credito = %s
                WHERE id_cliente = %s
            """
            cursor.execute(query, (nuevo_nombre, nuevo_apellido, nueva_fecha_nacimiento, nueva_direccion, nuevo_telefono, nuevo_ine, nueva_licencia, nueva_tarjeta_credito, client_id))
            con.commit()

            
            self.input_nombre.clear()
            self.input_apellidos.clear()
            self.input_fecha.clear()
            self.input_direccion.clear()
            self.input_telefono.clear()
            self.input_ine.clear()
            self.input_licencia.clear()
            self.input_tarjeta.clear()

            QMessageBox.information(self, "Éxito", "Cliente actualizado exitosamente.")
            con.close()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar el cliente: {e}")


class DeleteWindow(QWidget):
    def __init__(self):
        super(DeleteWindow, self).__init__()
        current_dir = os.path.dirname(__file__)
        ui_file = os.path.join(current_dir, "eliminar_clientes.ui") 
        uic.loadUi(ui_file, self)

        
        self.fill_client_id_combo()

       
        self.combo_cliente.currentIndexChanged.connect(self.load_client_data)

       
        self.btn_eliminar.clicked.connect(self.delete_user)

    def fill_client_id_combo(self):
        """Llenar el ComboBox con los ID de los clientes."""
        try:
            con = mysql.connector.connect(host="localhost", user="root", password="Previus22", database="TDS_db")
            cursor = con.cursor()
            cursor.execute("SELECT id_cliente FROM Clientes")
            result = cursor.fetchall()
            self.combo_cliente.clear() 

            for row in result:
                self.combo_cliente.addItem(str(row[0]))  

            con.close()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Error al cargar los clientes: {e}")

    def load_client_data(self):
        """Cargar los datos del cliente en los QLineEdit cuando se selecciona un ID del ComboBox."""
        client_id = self.combo_cliente.currentText()

        if not client_id:
            return  

        try:
            con = mysql.connector.connect(host="localhost", user="root", password="Previus22", database="TDS_db")
            cursor = con.cursor()
            cursor.execute("SELECT nombre, apellido FROM Clientes WHERE id_cliente = %s", (client_id,))
            result = cursor.fetchone()

            if result:
                nombre, apellido = result
                self.input_nombre.setText(nombre)
                self.input_apellido.setText(apellido)
            else:
                QMessageBox.warning(self, "Advertencia", "Cliente no encontrado.")

            con.close()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Error al cargar los datos del cliente: {e}")

    def delete_user(self):
        """Eliminar el cliente seleccionado de la base de datos."""
        client_id = self.combo_cliente.currentText()

        if not client_id:
            QMessageBox.warning(self, "Advertencia", "Por favor selecciona un cliente.")
            return

       
        reply = QMessageBox.question(self, 'Confirmar eliminación',
                                     f"¿Estás seguro de que deseas eliminar al cliente con ID {client_id}?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return

        try:
            con = mysql.connector.connect(host="localhost", user="root", password="Previus22", database="TDS_db")
            cursor = con.cursor()
            cursor.execute("DELETE FROM Clientes WHERE id_cliente = %s", (client_id,))
            con.commit()

           
            self.combo_cliente.clear()
            self.input_nombre.clear()
            self.input_apellido.clear()

            self.fill_client_id_combo() 
            QMessageBox.information(self, "Éxito", "Cliente eliminado exitosamente.")
            con.close()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Error", f"Error al eliminar el cliente: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
