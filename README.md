### Hacer cambios en la base de datos con usuario

- CRUD: Create, Read, Update, Delete
- Crear clientes

## DIAGRAMA DE BASE DE DATOS
https://dataedo.com/samples/html/AdventureWorks/doc/AdventureWorks_2/modules/Business_Entities_82/module.html

## Ultimo borrado

```python
@app.route("/person", methods=["POST"])
def create_person():
    try:
        data = request.json
        if not data:
            return "Bad request: No JSON payload provided", 400

        """ {
  "BusinessEntityID": 1234,
  "FirstName": "Juan",
  "LastName": "Pérez",
  "PersonType": "EM",
  "NameStyle": 0,
  "EmailPromotion": 1
}
 """
        BusinessEntityID = data.get("BusinessEntityID")
        FirstName = data.get("FirstName")
        LastName = data.get("LastName")
        PersonType = data.get("PersonType")
        NameStyle = data.get("NameStyle")
        EmailPromotion = data.get("EmailPromotion")

        app.logger.info(data)

        connection = pyodbc.connect(connectionString)
        cursor = connection.cursor()

        query = """
      INSERT INTO Person.Person (BusinessEntityID,FirstName, LastName, PersonType, NameStyle, EmailPromotion)
      VALUES (?, ?, ?, ?, ?,?)"""

        cursor.execute(
            query,
            BusinessEntityID,
            FirstName,
            LastName,
            PersonType,
            NameStyle,
            EmailPromotion,
        )

        connection.commit()

        businnes_entity_id = cursor.execute("SELECT SCOPE_IDENTITY()").fetchone()[0]

        cursor.close()
        connection.close()

        return jsonify({"BusinessEntityID": businnes_entity_id}), 201
    except Exception as e:
        print("\n")
        return str(e)
```


``` xml

        <EditText
            android:id="@+id/etPersonType"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_margin="8dp"
            android:hint="Person Type"
            app:layout_constraintEnd_toEndOf="parent"
            app:layout_constraintStart_toStartOf="parent"
            app:layout_constraintTop_toTopOf="parent" />
    

        <EditText
            android:id="@+id/etFirstName"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_margin="8dp"
            android:hint="First Name"
            app:layout_constraintEnd_toEndOf="parent"
            app:layout_constraintStart_toStartOf="parent"
            app:layout_constraintTop_toBottomOf="@+id/etPersonType" />

            
        <com.google.android.material.textfield.TextInputLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_margin="4dp"
            android:hint="PersonType"
            tools:ignore="MissingConstraints">
            
            <com.google.android.material.textfield.TextInputEditText
                android:layout_width="match_parent"
                android:layout_height="wrap_content"/>
            
        </com.google.android.material.textfield.TextInputLayout>


        <EditText
            android:id="@+id/etLastName"
            android:layout_width="0dp"
            android:layout_height="wrap_content"
            android:layout_margin="8dp"
            android:hint="Last Name"
            app:layout_constraintEnd_toEndOf="parent"
            app:layout_constraintStart_toStartOf="parent"
            app:layout_constraintTop_toBottomOf="@+id/etFirstName" />

        <Button
            android:id="@+id/btnSave"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_margin="8dp"
            android:text="Save"
            app:layout_constraintBottom_toBottomOf="parent"
            app:layout_constraintEnd_toEndOf="parent"
            app:layout_constraintStart_toStartOf="parent" />

```