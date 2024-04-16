from flask import Flask, render_template, request, jsonify
from modelos.producto import Producto
from controladores.producto_dao import ProductoDAO

app = Flask(__name__)
productoDAO = ProductoDAO('juegos_de_compra.json')

@app.route('/juega3')
def index():
    return render_template('index.html')

@app.route('/login_registro')
def login():
    return render_template('login.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/usuario') #Solo logueado
def usuario():
    return render_template('usuario.html')

@app.route('/usuario/carrito') #Solo logueado
def carrito():
    return render_template('carrito.html')

@app.route('/alquilar') #Solo logueado
def alquilar():
    return render_template('alquilar.html')

@app.route('/mesas') #Solo logueado
def mesas():
    return render_template('mesas.html')

@app.route('/productos', methods=['GET']) #Lista de productos (juegos)
def listar_productos():
    productos = productoDAO.listarProductos()
    return jsonify(productos)

@app.route('/productos', methods=['POST']) #Administrador
def agregar_producto():
    data = request.json
    producto = Producto(data['idProducto'], data['nombre'], data['precio'], data['descripcion'], data['stock'])
    productoDAO.agregarProducto(producto)
    return jsonify({"mensaje": "Producto agregado exitosamente"})

@app.route('/productos', methods=['PUT']) #Administrador
def actualizar_producto():
    data = request.json
    idProducto = data['idProducto'] # Obtener el ID del producto del cuerpo de la solicitud
    producto_actualizado = Producto(idProducto, data['nombre'], data['precio'], data['descripcion'], data['stock'])
    productoDAO.actualizarProducto(producto_actualizado)
    return jsonify({"mensaje": "Producto actualizado exitosamente"})

@app.route('/productos', methods=['DELETE']) #Administrador
def eliminar_producto():
    data = request.json
    idProducto = data['idProducto']
    productoDAO.eliminarProducto(idProducto)
    return jsonify({"mensaje": "Producto eliminado exitosamente"})

if __name__ == '__main__':
    app.run(debug=True)
