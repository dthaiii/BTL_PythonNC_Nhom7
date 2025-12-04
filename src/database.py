import mysql.connector
from config import MYSQL_CONFIG

def initialize_database():
    try:
        # Kết nối tới MySQL server (chưa cần chọn database)
        connection = mysql.connector.connect(
            user=MYSQL_CONFIG["user"],
            password=MYSQL_CONFIG["password"],
            host=MYSQL_CONFIG["host"],
            port=MYSQL_CONFIG["port"]
        )
        cursor = connection.cursor()

        # Tạo database nếu chưa tồn tại
        cursor.execute(f'''CREATE DATABASE IF NOT EXISTS {MYSQL_CONFIG["database"]};''')
        cursor.execute(f'''USE {MYSQL_CONFIG["database"]}''')
        print(f'''Database '{MYSQL_CONFIG["database"]}' đã được tạo (nếu chưa tồn tại).''')
        create_tables()
        
    except mysql.connector.Error as err:
        print(f"Lỗi khi tạo database: {err}")

def get_db_connection():
    # Kết nối tới database library_management
    connection = mysql.connector.connect(**MYSQL_CONFIG)
    return connection

def create_tables():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        # Tạo bảng Sách
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Sach (
                ma_sach INT PRIMARY KEY,
                ten_sach VARCHAR(255) NOT NULL,
                tac_gia VARCHAR(255),
                the_loai VARCHAR(100),
                ngay_xuat_ban DATE,
                so_luong INT
            );
        """)

        # Tạo bảng Độc giả
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Doc_gia (
                ma_doc_gia INT AUTO_INCREMENT PRIMARY KEY,
                ten_doc_gia VARCHAR(255) NOT NULL,
                ngay_sinh DATE,
                email VARCHAR(255),
                sdt VARCHAR(15)
            );
        """)

        # Tạo bảng Mượn trả
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Muon_tra (
                ma_muon_tra INT AUTO_INCREMENT PRIMARY KEY,
                ma_sach INT,
                ma_doc_gia INT,
                ngay_muon DATE,
                ngay_tra DATE,
                ngay_tra_du_kien DATE,
                trang_thai BIT DEFAULT 0,
                FOREIGN KEY (ma_sach) REFERENCES Sach(ma_sach),
                FOREIGN KEY (ma_doc_gia) REFERENCES Doc_gia(ma_doc_gia)
            );
        """)

        connection.commit()
        print("Các bảng đã được tạo thành công.")
    except mysql.connector.Error as err:
        print(f"Lỗi khi tạo bảng: {err}")
    # finally:
    #     cursor.close()
    #     connection.close()

if __name__ == "__main__":
    initialize_database()  # Tạo database nếu chưa có
    create_tables()        # Tạo các bảng nếu chưa có
