from flask import Flask, request, jsonify
import mysql.connector


app = Flask(__name__)

# Configura la conexión a la base de datos MySQL
try:
    db = mysql.connector.connect( 
         # url = mysql://root:e1YlKyWP6IxkFKe1OmNp@containers-us-west-50.railway.app:5937/railway,
        host="containers-us-west-50.railway.app",       
        user="root",         
        password="e1YlKyWP6IxkFKe1OmNp",   
        database="railway",  
        port="5937"
    )

except mysql.connector.Error as e:
    app.logger.error("Error al conectar a la base de datos: %s", str(e))



@app.route('/products', methods=['GET'])
def obtener_productos():
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Products")
        productos = cursor.fetchall()
        cursor.close()
        return jsonify(productos)
    
    except mysql.connector.Error as e:

        app.logger.error("Error al obtener productos de la base de datos: %s", str(e))
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/productosP', methods=['POST'])
def agregar_producto():
    try:
        id = request.form['id']
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        categoria = request.form['categoria']
  
        print(id,nombre, cantidad, categoria)
   
        if not nombre or not cantidad or not categoria or not id :
            return jsonify({"error": "Debes proporcionar nombre, cantidad, id y categoria del producto."}), 400

        cursor = db.cursor()
        cursor.execute("INSERT INTO Products (id,nombre, cantidad,categoria) VALUES (%s, %s, %s , %s)", (id, nombre, cantidad, categoria))
        db.commit()
        cursor.close()
        return jsonify({'nombre' : nombre, 'cantidad' : cantidad, 'id' : id, 'categoria' : categoria}, "Producto agregado con exito") 
    
    except mysql.connector.Error as e:
        app.logger.error("Error al agregar un producto a la base de datos: %s", str(e))
        return jsonify({"error": "Error interno del servidor"}), 500
    

@app.route('/productsUp/<int:id>', methods=['PUT'])
def actualizar_producto(id):

    try:

        nueva_cantidad = request.form['cantidad']

        if not nueva_cantidad:
            return jsonify({"error": "Debes proporcionar la nueva cantidad del producto."}), 400

        cursor = db.cursor()
        cursor.execute("SELECT * FROM Products WHERE id = %s", (id,))
        producto = cursor.fetchone()
        cursor.close()

        if not producto:
            return jsonify({"error": "Producto no encontrado"}), 404

        cursor = db.cursor()
        cursor.execute("UPDATE Products SET cantidad = %s WHERE id = %s", (nueva_cantidad, id))
        db.commit()
        cursor.close()
        return jsonify({"mensaje": "Producto actualizado con exito"})
    except mysql.connector.Error as e:
        app.logger.error("Error al actualizar un producto en la base de datos: %s", str(e))
        return jsonify({"error": "Error interno del servidor"}), 500


@app.route('/productosD/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM Products WHERE id = %s", (id,))
        db.commit()
        cursor.close()
        return jsonify({"mensaje": "Producto eliminado con exito"})
    except mysql.connector.Error as e:
        app.logger.error("Error al eliminar un producto de la base de datos: %s", str(e))
        return jsonify({"error": "Error interno del servidor"}), 500
    
if __name__ == '__main__':
    app.run(debug=True)

