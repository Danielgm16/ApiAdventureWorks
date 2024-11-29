from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)

# Configuración de la base de datos
server = 'localhost\\MYSQL'
database = 'sakila'
username = 'root'
password = '00lijereP'

# Cadena de conexión con autenticación de SQL Server
connection_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password

# Endpoint para obtener todas las personas
@app.route('/api/person', methods=['GET'])
def get_all_persons():
    try:
        
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM dbo.Empleado")
        rows = cursor.fetchall()
        app.logger.info('Conexión exitosa')

        person = []
        for row in rows:
            person.append({
                'BusinessEntityID': row.BusinessEntityID,
                'PersonType': row.PersonType,
                'FirstName': row.FirstName,
                'LastName': row.LastName
            })

        cursor.close()
        connection.close()
        return jsonify(person)
    except Exception as e:
        return str(e), 500

# Endpoint para obtener una persona por ID
@app.route('/api/person/<int:id>', methods=['GET'])
def get_person_by_id(id):
    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM dbo.Empleado WHERE BusinessEntityID = ?", (id))
        row = cursor.fetchone()

        if row:
            person = {
                'BusinessEntityID': row.BusinessEntityID,
                'PersonType': row.PersonType,
                'FirstName': row.FirstName,
                'LastName': row.LastName
            }
            cursor.close()
            connection.close()
            return jsonify(person)
        else:
            cursor.close()
            connection.close()
            return 'Person not found', 404
    except Exception as e:
        return str(e), 500

# Endpoint para crear una nueva persona
@app.route('/api/person', methods=['POST'])
def create_person():
    try:
        data = request.json
        if not data:
            return 'Bad Request: No JSON payload', 400

        BusinessEntityID = data.get('BusinessEntityID')
        person_type = data.get('PersonType')
        first_name = data.get('FirstName')
        last_name = data.get('LastName')

        app.logger.info('Personas: ' + person_type + ' ' + first_name + ' ' + last_name +' '+ BusinessEntityID)
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        
        # Insertar en dbo.Empleado
        cursor.execute("INSERT INTO dbo.Empleado (BusinessEntityID,PersonType, FirstName, LastName) VALUES (?, ?, ?, ?);",
                       (BusinessEntityID,person_type, first_name, last_name))
        connection.commit()

        # Obtener el ID del nuevo registro
        business_entity_id = cursor.execute("SELECT SCOPE_IDENTITY()").fetchone()[0]

        cursor.close()
        connection.close()

    

        return jsonify({'id': business_entity_id}), 201
    except Exception as e:
        return str(e), 500

# Endpoint para actualizar una persona
@app.route('/api/person/<int:id>', methods=['PUT'])
def update_person(id):
    try:
        data = request.json
        if not data:
            return 'Bad Request: No JSON payload', 400

        person_type = data.get('PersonType')
        first_name = data.get('FirstName')
        last_name = data.get('LastName')

        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("UPDATE dbo.Empleado SET PersonType = ?, FirstName = ?, LastName = ? WHERE BusinessEntityID = ?", 
                       (person_type, first_name, last_name, id))
        connection.commit()

        cursor.close()
        connection.close()
        return '', 204
    except Exception as e:
        return str(e), 500

# Endpoint para eliminar una persona
@app.route('/api/person/<int:id>', methods=['DELETE'])
def delete_person(id):
    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        
        # Iniciar la transacción
        connection.autocommit = False
        
        try:
            # Eliminar la persona en la tabla dbo.Empleado
            cursor.execute("DELETE FROM dbo.Empleado WHERE BusinessEntityID = ?", (id,))
            
            # Confirmar la transacción
            connection.commit()
        except Exception as e:
            # Si ocurre un error, revertir la transacción
            connection.rollback()
            raise e
        
        cursor.close()
        connection.close()
        return '', 204
    except Exception as e:
        return str(e), 500

# Endpoint para agregar una tienda
@app.route('/api/store', methods=['POST'])
def create_store():
    try:
        data = request.json
        if not data:
            return 'Bad Request: No JSON payload', 400

        business_entity_id = data.get('BusinessEntityID')
        name = data.get('Name')

        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        # Insertar en Sales_Store
        cursor.execute("INSERT INTO Sales_Store (BusinessEntityID, Name) VALUES (?, ?);",
                       (business_entity_id, name))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({'id': business_entity_id}), 201
    except Exception as e:
        return str(e), 500

# Endpoint para obtener todas las tiendas
@app.route('/api/store', methods=['GET'])
def get_all_stores():
    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Sales_Store")
        rows = cursor.fetchall()

        stores = []
        for row in rows:
            stores.append({
                'BusinessEntityID': row.BusinessEntityID,
                'Name': row.Name
            })

        cursor.close()
        connection.close()
        return jsonify(stores)
    except Exception as e:
        return str(e), 500

# Endpoint para obtener una tienda por ID
@app.route('/api/store/<int:id>', methods=['GET'])
def get_store_by_id(id):
    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Sales_Store WHERE BusinessEntityID = ?", (id,))
        row = cursor.fetchone()

        if row:
            store = {
                'BusinessEntityID': row.BusinessEntityID,
                'Name': row.Name
            }
            cursor.close()
            connection.close()
            return jsonify(store)
        else:
            cursor.close()
            connection.close()
            return 'Store not found', 404
    except Exception as e:
        return str(e), 500

# Endpoint para actualizar una tienda
@app.route('/api/store/<int:id>', methods=['PUT'])
def update_store(id):
    try:
        data = request.json
        if not data:
            return 'Bad Request: No JSON payload', 400

        name = data.get('Name')

        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("UPDATE Sales_Store SET Name = ? WHERE BusinessEntityID = ?", 
                       (name, id))
        connection.commit()

        cursor.close()
        connection.close()
        return '', 204
    except Exception as e:
        return str(e), 500

# Endpoint para eliminar una tienda
@app.route('/api/store/<int:id>', methods=['DELETE'])
def delete_store(id):
    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        
        # Iniciar la transacción
        connection.autocommit = False
        
        try:
            # Eliminar la tienda en la tabla Sales_Store
            cursor.execute("DELETE FROM Sales_Store WHERE BusinessEntityID = ?", (id,))
            
            # Finalmente, eliminar el registro en Person_BusinessEntityContact
            cursor.execute("DELETE FROM Person_BusinessEntityContact WHERE BusinessEntityID = ?", (id,))
            
            # Confirmar la transacción
            connection.commit()
        except Exception as e:
            # Si ocurre un error, revertir la transacción
            connection.rollback()
            raise e
        
        cursor.close()
        connection.close()
        return '', 204
    except Exception as e:
        return str(e), 500

# Endpoint para agregar un proveedor
@app.route('/api/vendor', methods=['POST'])
def create_vendor():
    try:
        data = request.json
        if not data:
            return 'Bad Request: No JSON payload', 400

        business_entity_id = data.get('BusinessEntityID')
        account_number = data.get('AccountNumber')
        name = data.get('Name')

        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        # Insertar en Purchasing_Vendor
        cursor.execute("INSERT INTO Purchasing_Vendor (BusinessEntityID, AccountNumber, Name) VALUES (?, ?, ?);",
                       (business_entity_id, account_number, name))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({'id': business_entity_id}), 201
    except Exception as e:
        return str(e), 500

# Endpoint para obtener todos los proveedores
@app.route('/api/vendor', methods=['GET'])
def get_all_vendors():
    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Purchasing_Vendor")
        rows = cursor.fetchall()

        vendors = []
        for row in rows:
            vendors.append({
                'BusinessEntityID': row.BusinessEntityID,
                'AccountNumber': row.AccountNumber,
                'Name': row.Name
            })

        cursor.close()
        connection.close()
        return jsonify(vendors)
    except Exception as e:
        return str(e), 500

# Endpoint para obtener un proveedor por ID
@app.route('/api/vendor/<int:id>', methods=['GET'])
def get_vendor_by_id(id):
    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Purchasing_Vendor WHERE BusinessEntityID = ?", (id,))
        row = cursor.fetchone()

        if row:
            vendor = {
                'BusinessEntityID': row.BusinessEntityID,
                'AccountNumber': row.AccountNumber,
                'Name': row.Name
            }
            cursor.close()
            connection.close()
            return jsonify(vendor)
        else:
            cursor.close()
            connection.close()
            return 'Vendor not found', 404
    except Exception as e:
        return str(e), 500

# Endpoint para actualizar un proveedor
@app.route('/api/vendor/<int:id>', methods=['PUT'])
def update_vendor(id):
    try:
        data = request.json
        if not data:
            return 'Bad Request: No JSON payload', 400

        account_number = data.get('AccountNumber')
        name = data.get('Name')

        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        cursor.execute("UPDATE Purchasing_Vendor SET AccountNumber = ?, Name = ? WHERE BusinessEntityID = ?", 
                       (account_number, name, id))
        connection.commit()

        cursor.close()
        connection.close()
        return '', 204
    except Exception as e:
        return str(e), 500

# Endpoint para eliminar un proveedor
@app.route('/api/vendor/<int:id>', methods=['DELETE'])
def delete_vendor(id):
    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        
        # Iniciar la transacción
        connection.autocommit = False
        
        try:
            # Eliminar el proveedor en la tabla Purchasing_Vendor
            cursor.execute("DELETE FROM Purchasing_Vendor WHERE BusinessEntityID = ?", (id,))
            
            # Finalmente, eliminar el registro en Person_BusinessEntityContact
            cursor.execute("DELETE FROM Person_BusinessEntityContact WHERE BusinessEntityID = ?", (id,))
            
            # Confirmar la transacción
            connection.commit()
        except Exception as e:
            # Si ocurre un error, revertir la transacción
            connection.rollback()
            raise e
        
        cursor.close()
        connection.close()
        return '', 204
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
