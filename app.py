from flask import Flask, render_template, request, jsonify, redirect, session, url_for
from modelos.producto import Producto
from controladores.usuarios_dao import UsuariosDAO
from controladores.producto_dao import ProductoDAO
from controladores.carrito_dao import CarritoDAO
from controladores.carrito_dao import carrito
from datetime import timedelta


app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

productoDAO = ProductoDAO('juegos_de_compra.json')
usuarios_dao = UsuariosDAO('usuarios.json')
producto_dao = ProductoDAO('juegos_de_compra.json')
carrito_dao = CarritoDAO('juegos_de_compra.json')

app.permanent_session_lifetime = timedelta(days=1)

@app.route('/carrito')
def mostrar_pagina():
    total = carrito_dao.calcular_total()
    mensaje = carrito_dao.mensaje_carrito()
    return render_template('carrito.html', juegos_de_compra=producto_dao.listarProductos(), carrito=carrito, mensaje=mensaje, total=total)

@app.route('/carrito/agregar', methods=['POST'])
def agregar_producto_carrito():
    print("Se ha enviado el formulario para agregar un producto al carrito.")
    producto = request.form['idProducto']
    carrito_dao.agregar_al_carrito(producto)
    return redirect("/carrito")

@app.route('/carrito/eliminar', methods=['POST'])
def eliminar_producto_carrito():
    producto_index = request.form['index']
    print("Índice del producto a eliminar:", producto_index)
    carrito_dao.eliminar_del_carrito(producto_index)
    return redirect("/carrito")

@app.route('/carrito/limpiar', methods=['POST'])
def limpiar_carrito():
    carrito_dao.eliminar_todo_carrito()
    return redirect("/carrito")

@app.route('/carrito/checkout', methods=['POST'])
def checkout():
    total = session.get('total', 0.00)	
    compra = []
    carrito_dao.nueva_lista(carrito, compra)
    carrito_dao.eliminar_todo_carrito()
    return render_template('recibo.html', total=total, carrito=compra, juegos_de_compra=producto_dao.listarProductos())

@app.route('/carrito/descuento', methods=['POST'])
def descuento():
    mensaje = carrito_dao.mensaje_carrito()
    total_antiguo = carrito_dao.calcular_total()
    descuento = request.form['descuento']
    total = carrito_dao.aplicar_descuento(total_antiguo, descuento)
    session['total'] = total
    return render_template('carrito.html', juegos_de_compra=producto_dao.listarProductos(), carrito=carrito, total=total, mensaje=mensaje)

@app.route('/admin')
def admin_panel():
    if 'usuario' in session and session['usuario'] == 'admin':
        return render_template('admin_panel.html')
    else:
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usuario = usuarios_dao.obtener_usuario_por_credenciales(username, password)
        if usuario:
            session['usuario'] = usuario['username']
            if usuario['admin']:
                return redirect('/admin')
            else:
                return redirect('/usuarios')
        else:
            return render_template('login.html', error="Credenciales incorrectas. Inténtalo de nuevo.")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)  
    return jsonify({"mensaje": "Sesión cerrada exitosamente"})  

@app.route('/usuarios')
def usuario_panel():
    if 'usuario' in session:
        return render_template('usuario_panel.html')
    else:
        return redirect('/login')

@app.route('/')
def display_page():
    lista_productos = producto_dao.listarProductos()
    return render_template('index.html', lista_productos=lista_productos)

@app.route('/productos', methods=['GET'], endpoint='listar_productos')
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
    idProducto = data['idProducto'] 
    producto_actualizado = Producto(idProducto, data['nombre'], data['precio'], data['descripcion'], data['stock'])
    productoDAO.actualizarProducto(producto_actualizado)
    return jsonify({"mensaje": "Producto actualizado exitosamente"})

@app.route('/productos', methods=['DELETE'], endpoint='eliminar_producto')
def eliminar_producto():
    data = request.json
    idProducto = data['idProducto']
    productoDAO.eliminarProducto(idProducto)
    return jsonify({"mensaje": "Producto eliminado exitosamente"})

if __name__ == '__main__':
    app.run(host='www.juega3.com', port=80, debug=True)
