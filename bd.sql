-- Tabla para los usuarios que pueden iniciar sesión
CREATE TABLE Usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
    contraseña VARCHAR(255) NOT NULL,
);

-- Tabla para los autos disponibles para rentar
CREATE TABLE Autos (
    id_auto INT AUTO_INCREMENT PRIMARY KEY,
    clave_auto VARCHAR(50) NOT NULL UNIQUE,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    año INT NOT NULL,
    precio_por_dia DECIMAL(10, 2) NOT NULL,
    disponible BOOLEAN DEFAULT TRUE
);

-- Tabla para los clientes
CREATE TABLE Clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    direccion TEXT NOT NULL,
    telefono VARCHAR(10) NOT NULL,
    ine VARCHAR(20) NOT NULL UNIQUE,
    licencia VARCHAR(20) NOT NULL UNIQUE,
    tarjeta_credito VARCHAR(16) NOT NULL UNIQUE
);

-- Tabla para las compañías aseguradoras
CREATE TABLE CompaniasAseguradoras (
    id_compania INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    telefono VARCHAR(15) NOT NULL,
    direccion TEXT NOT NULL
);

-- Tabla para registrar las rentas
CREATE TABLE Rentas (
    id_renta INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
	id_auto INT NOT NULL,
	id_compania INT NOT NULL,
    fecha_renta DATE NOT NULL DEFAULT CURRENT_DATE,
    fecha_devolucion DATE,
    garantia DECIMAL(10, 2) NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente),
	FOREIGN KEY (id_auto) REFERENCES Autos(id_auto),
	FOREIGN KEY (id_compania) REFERENCES CompaniasAseguradoras(id_compania)
);