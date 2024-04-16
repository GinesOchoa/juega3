from flask import Flask, render_template, request, jsonify
from modelos.producto import Producto
from controladores.producto_dao import ProductoDAO

app = Flask(__name__)
productoDAO = ProductoDAO('juegos_de_compra.json')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/productos', methods=['GET'])
def listar_productos():
    productos = productoDAO.listarProductos()
    return jsonify(productos)

@app.route('/productos', methods=['POST'])
def agregar_producto():
    data = request.json
    producto = Producto(data['idProducto'], data['nombre'], data['precio'], data['descripcion'], data['stock'])
    productoDAO.agregarProducto(producto)
    return jsonify({"mensaje": "Producto agregado exitosamente"})

@app.route('/productos', methods=['PUT'])
def actualizar_producto():
    data = request.json
    idProducto = data['idProducto'] # Obtener el ID del producto del cuerpo de la solicitud
    producto_actualizado = Producto(idProducto, data['nombre'], data['precio'], data['descripcion'], data['stock'])
    productoDAO.actualizarProducto(producto_actualizado)
    return jsonify({"mensaje": "Producto actualizado exitosamente"})

@app.route('/productos', methods=['DELETE'])
def eliminar_producto():
    data = request.json
    idProducto = data['idProducto']
    productoDAO.eliminarProducto(idProducto)
    return jsonify({"mensaje": "Producto eliminado exitosamente"})

if __name__ == '__main__':
    app.run(debug=True)
