from flask import jsonify
from app.models.doctor import ErrorResponseModel


def create_db_if_not_exists(mysql):
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
                        CREATE TABLE IF NOT EXISTS doctors (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        firstName VARCHAR(50) NOT NULL,
                        lastName VARCHAR(50) NOT NULL,
                        specialty VARCHAR(100) NOT NULL,
                        experienceYears INT NOT NULL,
                        contactNumber VARCHAR(15));
                    """)
        mysql.connection.commit()
        cur.close()
        return jsonify({
            "message": "Database created successfully or already existed",
            "welcome": "Welcome to doctor API :)"
        })
    except Exception as e:
        return jsonify(ErrorResponseModel(str(e), 500, "Database could not be created !!"))