from flask import Flask, render_template, request, jsonify, redirect, session
from modelos.producto import Producto
from controladores.usuarios_dao import UsuariosDAO
from controladores.producto_dao import ProductoDAO

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

productoDAO = ProductoDAO('juegos_de_compra.json')
usuarios_dao = UsuariosDAO('usuarios.json')

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

@app.route('/usuarios')
def usuario_panel():
    if 'usuario' in session:
        return render_template('usuario_panel.html')
    else:
        return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('usuario', None)  
    return jsonify({"mensaje": "Sesión cerrada exitosamente"})  

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
    idProducto = data['idProducto'] 
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
    app.run(host='www.juega3.com', port=80, debug=True)
