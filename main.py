from flask import Flask, jsonify, request
import pyodbc
import os

app = Flask(__name__)

# Configuración de la conexión a SQL Server
server = "localhost"
database = "AdventureWorks2019"
username = "sa"
password = "00lijereP"

# Ruta o conexión a la base de datos
connectionString = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=no"


def consulta_data(query):
    try:
        # Hace la conexion a la base de datos en sql server
        conn = pyodbc.connect(connectionString)
        # Crea un cursor para ejecutar la consulta
        cursor = conn.cursor()
        # Ejecuta la consulta
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()

        data_dict = [
            dict(zip([column[0] for column in cursor.description], row)) for row in data
        ]
        return jsonify(data_dict)

    except Exception as e:
        return str(e)


# FUNCION PARA VALIDAR QUE LA PERSONA EXISTA
def validar_persona(BusinessEntityID):
    estatus = False
    try:
        consulta = consulta_data(
            f"SELECT * FROM Person.Person WHERE BusinessEntityID = {BusinessEntityID}"
        )

        app.logger.info(consulta)

        if consulta != []:
            estatus = True
            return estatus
    except Exception as e:
        return str(e), 500

    return estatus


# RUTA DE PRUEBA
@app.route("/")
def hello_world():
    return "Hello world"


# GET 10 PERSONS
@app.route("/api/person", methods=["GET"])
def get_person():
    try:
        return consulta_data(
            "SELECT TOP 10 BusinessEntityID, FirstName, LastName, PersonType FROM Person.Person ORDER BY BusinessEntityID DESC"
        )
    except Exception as e:
        return str(e)


# RUTA PARA OBTENER UN DATO POR ID
@app.route("/api/person/<int:id>", methods=["GET"])
def obtener_por_id(id):
    try:
        return consulta_data(
            f"SELECT BusinessEntityID,FirstName,LastName,PersonType FROM Person.Person WHERE BusinessEntityID = {id}"
        )
    except Exception as e:
        return str(e)


# RUTA PARA OBTENER LOS DATOS DE UNA PERSONA POR NOMBRE
@app.route("/api/person/<string:FirstName>", methods=["GET"])
def obtener_por_nombre(FirstName):
    try:
        return consulta_data(
            f"SELECT * FROM Person.Person WHERE FirstName = '{FirstName}'"
        )
    except Exception as e:
        return str(e)


# INICIO POSTS
# RUTA PARA INSERTAR UNA PERSONA
@app.route("/api/create/person", methods=["POST"])
def create_person():
    try:
        data = request.json
        if not data:
            return "Bad request: No JSON payload provided", 400

        app.logger.info(data)

        # Hace la conexion a la base de datos en sql server
        connection = pyodbc.connect(connectionString)
        cursor = connection.cursor()

        # PRIMERO SE INSERTA EN LA TABLAS BusinessEntity
        query = """
        INSERT INTO Person.BusinessEntity(rowguid, ModifiedDate)
        OUTPUT INSERTED.BusinessEntityID
        VALUES (NEWID(), GETDATE())"""

        cursor.execute(query)
        # Obtener el id de la persona insertada
        customer_id = cursor.fetchone()[0]
        # INSERTAMOS NUEVA PERSONA CON EL ID DE LA TABLA BusinessEntity
        query = """
        INSERT INTO Person.Person(BusinessEntityID, PersonType, FirstName, LastName
        ,rowguid, ModifiedDate) VALUES(?, ?, ?, ?, NEWID(), GETDATE())"""

        cursor.execute(
            query,
            customer_id,
            data.get("PersonType"),
            data.get("FirstName"),
            data.get("LastName"),
        )
        # Confirmar cambios en la base de datos
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"BusinessEntityID": customer_id}), 201
    except Exception as e:
        print("\n")
        return str(e)


# RUTA PARA ACTUALIZAR UNA PERSONA
@app.route("/api/person/update/<int:BusinessEntityID>", methods=["PUT"])
def update_person(BusinessEntityID):
    try:
        data = request.json
        if not data:
            return "Bad request: No JSON payload provided", 400

        app.logger.info(data)

        connection = pyodbc.connect(connectionString)
        cursor = connection.cursor()

        query = """
        UPDATE Person.Person SET FirstName = ?, LastName = ?, PersonType=? WHERE BusinessEntityID = ?;"""

        cursor.execute(
            query,
            (
                data.get("FirstName"),
                data.get("LastName"),
                data.get("PersonType"),
                BusinessEntityID,
            ),
        )

        connection.commit()
    except Exception as e:
        return str(e), 500
    finally:
        cursor.close()
        connection.close()

    return "Person updated successfully", 200


# RUTA PARA BORRAR UNA PERSONA
@app.route("/api/person/delete/<int:BusinessEntityID>", methods=["DELETE"])
def delete_person(BusinessEntityID):
    try:
        connection = pyodbc.connect(connectionString)
        cursor = connection.cursor()

        # Inicia la transacción
        cursor.execute("BEGIN TRANSACTION")

        # Define la query completa
        query = f"""
        DECLARE @BusinessEntityID INT = {BusinessEntityID};

        DELETE FROM Person.Password WHERE BusinessEntityID = @BusinessEntityID;

        DELETE FROM Person.EmailAddress WHERE BusinessEntityID = @BusinessEntityID;

        DELETE so
        FROM Sales.SalesOrderHeader so
            INNER JOIN Sales.Customer sc ON so.CustomerID = sc.CustomerID
        WHERE PersonID = @BusinessEntityID;

        DELETE FROM Sales.Customer WHERE PersonID = @BusinessEntityID;

        DELETE pc
        FROM Sales.PersonCreditCard pc
            INNER JOIN Sales.CreditCard cc ON pc.CreditCardID = cc.CreditCardID
        WHERE BusinessEntityID = @BusinessEntityID;

        DELETE FROM Sales.PersonCreditCard WHERE BusinessEntityID = @BusinessEntityID;

        DELETE bea
        FROM Person.BusinessEntityAddress bea
            INNER JOIN Person.BusinessEntity be ON bea.BusinessEntityID = be.BusinessEntityID
        WHERE be.BusinessEntityID = @BusinessEntityID;

        DELETE pf
        FROM Person.PersonPhone pf
            INNER JOIN Person.Person pp ON pf.BusinessEntityID = pp.BusinessEntityID
        WHERE pp.BusinessEntityID = @BusinessEntityID;

        DELETE FROM Person.Person WHERE BusinessEntityID = @BusinessEntityID;

        DELETE FROM Person.BusinessEntity WHERE BusinessEntityID = @BusinessEntityID;
        
        COMMIT TRANSACTION;
        """

        # Ejecuta la query completa
        cursor.execute(query)
        connection.commit()

    except Exception as e:
        # En caso de error, se hace rollback
        connection.rollback()
        return f"Error al eliminar la persona: {e}", 500

    finally:
        cursor.close()
        connection.close()

    return "Person deleted successfully", 200

# FIN POSTS


if __name__ == "__main__":
    # host = IP de la maquina
    # Modificar la IP del la aplicacion
    #app.run(debug=True, host="192.168.3.205") #Empresa
    app.run(debug=True,host="192.168.1.9") #Casa
