from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
import os
from pydantic import ValidationError
from app.models.doctor import DoctorSchema, UpdateDoctorModel, ResponseModel, ErrorResponseModel
from .create_db import create_db_if_not_exists


app = Flask(__name__)

app.config['MYSQL_HOST'] = os.environ['MYSQL_HOST']
app.config['MYSQL_USER'] = os.environ['MYSQL_USER']
app.config['MYSQL_PASSWORD'] = os.environ['MYSQL_PASSWORD']
app.config['MYSQL_DB'] = os.environ['MYSQL_DB']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


@app.route('/')
def home():
    db_response = create_db_if_not_exists(mysql)

    return db_response


@app.route('/doctors/new-doctor', methods=['POST'])
def create_doctor():

    create_db_if_not_exists(mysql)

    data = request.get_json()
    doctor_data = DoctorSchema(**data)
    response_data = doctor_data.model_dump()

    conn = mysql.connection
    cur = conn.cursor()
    cur.execute("INSERT INTO doctors (firstName, lastName, specialty, experienceYears, contactNumber) VALUES (%s, %s, %s, %s, %s)", 
                (doctor_data.firstName, doctor_data.lastName, doctor_data.specialty, doctor_data.experienceYears, doctor_data.contactNumber))
    conn.commit()
    cur.close()

    return ResponseModel(response_data, "Doctor added successfully !")


@app.route('/doctors/list', methods=['GET'])
def get_doctors():

    create_db_if_not_exists(mysql)

    conn = mysql.connection
    cur = conn.cursor()
    cur.execute("SELECT * FROM doctors")
    doctors = cur.fetchall()
    cur.close()
    if doctors:
        return ResponseModel(doctors, "Doctors data retrieved successfully !")
    return ResponseModel(doctors, "Empty list returned")


@app.route('/doctors/<int:id>', methods=['GET'])
def get_doctor(id):

    create_db_if_not_exists(mysql)

    conn = mysql.connection
    cur = conn.cursor()
    cur.execute("SELECT * FROM doctors WHERE id = %s", (id,))
    doctor = cur.fetchone()
    cur.close()

    if doctor:
        return ResponseModel(doctor, "Doctor retrieved successfully.")
    else:
        return jsonify(ErrorResponseModel("Doctor not found.", 404, "The doctor doesn't exist."))



@app.route('/doctors/edit/<int:id>', methods=['PATCH'])
def update_doctor(id):

    create_db_if_not_exists(mysql)

    try:
        data = request.json

        update_data = UpdateDoctorModel(**data)

        update_fields = []
        if update_data.firstName is not None:
            update_fields.append(("firstName", update_data.firstName))
        if update_data.lastName is not None:
            update_fields.append(("lastName", update_data.lastName))
        if update_data.contactNumber is not None:
            update_fields.append(("contactNumber", update_data.contactNumber))
        if update_data.experienceYears is not None:
            update_fields.append(("experienceYears", update_data.experienceYears))

        conn = mysql.connection
        cur = conn.cursor()
        
        for field, value in update_fields:
            cur.execute(f"UPDATE doctors SET {field} = %s WHERE id = %s", (value, id))
        conn.commit()
        
        if cur.rowcount == 0:
            cur.close()
            return jsonify(ErrorResponseModel("Not found", 404, f"Doctor with id {id} not found"))
        
        cur.close()
        return jsonify(ResponseModel(dict(update_fields), "Doctor updated successfully"))
    
    except ValidationError as e:
        return ErrorResponseModel(str(e), 400, "Invalid data")
    
    except Exception as e:
        return jsonify(ErrorResponseModel(str(e), 500, "An internal error occurred"))



@app.route('/doctors/delete/<int:id>', methods=['DELETE'])
def delete_doctor(id):

    create_db_if_not_exists(mysql)

    conn = mysql.connection
    cur = conn.cursor()
    cur.execute("SELECT * FROM doctors WHERE id = %s", [id])
    doctor = cur.fetchone()

    if not doctor:
        return jsonify(ErrorResponseModel("An error occurred", 404, f"doctor with id {id} doesn't exist"))

    cur.execute("DELETE FROM doctors WHERE id = %s", [id])
    conn.commit()
    cur.close()

    return ResponseModel(f"Doctor with ID {id} removed", "Doctor deleted successfully.")

if __name__ == '__main__':
    app.run(debug=True)