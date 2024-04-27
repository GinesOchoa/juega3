from flask import Flask, render_template, request, jsonify, redirect, session, url_for, json, flash
from modelos.producto import Producto
from controladores.usuarios_dao import UsuariosDAO
from controladores.producto_dao import ProductoDAO
from controladores.carrito_dao import CarritoDAO
from controladores.carrito_dao import carrito
from controladores.venta_dao import VentaDAO
from modelos.venta import Venta
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

productoDAO = ProductoDAO('juegos_de_compra.json')
usuarios_dao = UsuariosDAO('usuarios.json')
producto_dao = ProductoDAO('juegos_de_compra.json')
carrito_dao = CarritoDAO('juegos_de_compra.json')
ventaDAO = VentaDAO('ventas.json')

app.permanent_session_lifetime = timedelta(days=1)

@app.route('/venta')
def venta():
    return render_template('venta.html')

@app.route('/ventas', methods=['GET'])
def listar_ventas():
    ventas = ventaDAO.cargar_ventas()
    return jsonify(ventas)

@app.route('/ventas', methods=['POST'])
def agregar_venta():
    data = request.json
    venta_id = ventaDAO.generar_id_venta()
    venta = Venta(venta_id, data['usuario'], data['productos'], data['precio_total'])
    ventaDAO.guardar_venta(venta)
    return jsonify({"mensaje": "Venta agregada exitosamente"})

@app.route('/ventas', methods=['PUT'])
def actualizar_venta():
    data = request.json
    venta_id = data['id']
    nuevos_datos = {
        "usuario": data['usuario'],
        "productos": data['productos'],
        "precio_total": data['precio_total']
    }
    ventaDAO.actualizar_venta(venta_id, nuevos_datos)
    return jsonify({"mensaje": "Venta actualizada exitosamente"})

@app.route('/ventas', methods=['DELETE'])
def eliminar_venta():
    data = request.json
    venta_id = data['id']
    ventaDAO.eliminar_venta(venta_id)
    return jsonify({"mensaje": "Venta eliminada exitosamente"})

@app.route('/carrito/procesar_venta', methods=['POST'])
def procesar_venta():
    usuario = session.get('usuario')
    
    if usuario:
        compra = []
        
        if 'total_con_descuento' in session:
            total = session.pop('total_con_descuento')
            print("Total if",total)
        else:
            total = carrito_dao.calcular_total()
            print("Total else",total)

        carrito_dao.nueva_lista(carrito, compra)
        carrito_dao.eliminar_todo_carrito()
        
        for item in carrito:
            compra.append(item[1])
        
        carrito.clear()
        venta_id = ventaDAO.generar_id_venta()
        venta = Venta(venta_id, usuario, compra, total)
        ventaDAO.guardar_venta(venta)
        return render_template('recibo.html', total=total, carrito=compra, juegos_de_compra=producto_dao.listarProductos())
    else:
        flash('Debes iniciar sesión para realizar una compra', 'error')
        return redirect(url_for('login'))

@app.route('/carrito')
def mostrar_pagina():
    total = carrito_dao.calcular_total()
    mensaje = carrito_dao.mensaje_carrito()
    return render_template('carrito.html', juegos_de_compra=producto_dao.listarProductos(), carrito=carrito, mensaje=mensaje, total=total)

@app.route('/carrito/agregar', methods=['POST'])
def agregar_producto_carrito():
    producto = request.form['idProducto']
    carrito_dao.agregar_al_carrito(producto)
    return redirect("/carrito")

@app.route('/carrito/eliminar', methods=['POST'])
def eliminar_producto_carrito():
    producto_index = request.form['index']
    carrito_dao.eliminar_del_carrito(producto_index)
    return redirect("/carrito")

@app.route('/carrito/limpiar', methods=['POST'])
def limpiar_carrito():
    carrito_dao.eliminar_todo_carrito()
    return redirect("/carrito")

@app.route('/carrito/descuento', methods=['POST'])
def descuento():
    mensaje = carrito_dao.mensaje_carrito()
    total_sin_descuento = carrito_dao.calcular_total()
    descuento = request.form['descuento']
    total_con_descuento = carrito_dao.aplicar_descuento(total_sin_descuento, descuento)
    session['total_con_descuento'] = total_con_descuento
    return render_template('carrito.html', juegos_de_compra=producto_dao.listarProductos(), carrito=carrito, total=total_con_descuento, mensaje=mensaje)

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
