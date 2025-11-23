-- ==========================================================
-- DML INICIAL PARA SISTEMA UniformesBambi POS
-- Crea usuarios, empleados y datos mínimos obligatorios
-- ==========================================================

USE `UniformesBambi`;
SET CHARACTER SET utf8mb4;
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------------------------------------
-- USUARIO(S) POR DEFECTO
-- ----------------------------------------------------------

-- ⚠ contrasena por defecto: "admin123"
-- Se recomienda cambiarla después
-- Hash generado ejemplo (BCrypt cost=12): 
-- $2b$12$wNWUuMlGHNirMRHkRkNvgeNFVQVw1Gc7YCOUMIqFZ3VAb9/T/jHhG

INSERT INTO Usuario (nombre_usuario, contrasena_hash, rol_usuario)
VALUES 
('admin', '$2b$12$wNWUuMlGHNirMRHkRkNvgeNFVQVw1Gc7YCOUMIqFZ3VAb9/T/jHhG', 'admin');

-- Obtener ID del usuario admin recién creado
SET @admin_id := LAST_INSERT_ID();

-- ----------------------------------------------------------
-- EMPLEADO LIGADO AL ADMIN
-- ----------------------------------------------------------
INSERT INTO Empleado (nombre_empleado, puesto_empleado, telefono_empleado, rol_empleado, Usuario_id_usuario)
VALUES
('Administrador General', 'Supervisor', '0000000000', 'admin', @admin_id);

-- ----------------------------------------------------------
-- CATEGORÍAS Y ESTADOS BASE PARA PRODUCTOS (OPCIONAL)
-- Solo se crean si quieres prellenar catálogo inicial
-- ----------------------------------------------------------

-- Ejemplo opcional: Productos base
INSERT INTO Producto (nombre_producto, descripcion_producto, categoria, precio, estado)
VALUES
('Playera Escolar Básica', 'Playera estándar para nivel primaria', 'escolar', 120.00, 'activo'),
('Short Deportivo Niño', 'Short ligero para actividades deportivas', 'deportiva', 150.00, 'activo');

-- Obtener IDs de productos base
SET @prod1 := 1;
SET @prod2 := 2;

-- Variaciones de ejemplo (tallas, colores)
INSERT INTO VariacionProducto (talla, color, stock, Producto_id_producto)
VALUES
('CH', 'Blanco', 10, @prod1),
('M', 'Blanco', 10, @prod1),
('G', 'Negro', 5, @prod2);

-- ----------------------------------------------------------
-- PROVEEDORES BASE (OPCIONAL PERO ÚTIL)
-- ----------------------------------------------------------
INSERT INTO Proveedor (nombre_proveedor, telefono_proveedor, correo_proveedor, direccion_proveedor)
VALUES
('Proveedor Genérico', '9999999999', 'contacto@proveedor.com', 'Dirección genérica s/n');

SET FOREIGN_KEY_CHECKS = 1;

-- Fin del DML inicial
