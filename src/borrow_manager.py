import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from tkcalendar import DateEntry
from tkinter. font import Font
from datetime import date, datetime
from database import get_db_connection

class BorrowManagerScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý Mượn")
        self.root.configure(bg="#babfbb")
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()
        self.create_gui()
        self.load_muon_tra()
        
    def create_gui(self):
        # Giao diện nhập liệu
        self. style = ttk.Style()
        self.style.theme_use('clam')
        self.create_fonts()
        
        self.frame_borrow_manager = ttk.Frame(self.root)
        self.frame_borrow_manager.grid(row=0, column=0, sticky="nsew")
        
        # Nút trở về
        btn_back = ttk.Button(self.frame_borrow_manager, text="← Trở về", command=self.tro_ve)
        btn_back.grid(row=0, column=0, sticky="W", padx=10, pady=10)
        
        self.frame_inputs = ttk.Frame(self. frame_borrow_manager, padding=(10, 10))
        self. frame_inputs.grid(row=1, column=0, sticky="W")
        
        self.create_input_fields()
        self.create_buttons()
        self.create_treeview()
        
    def create_fonts(self):
        # Font tùy chỉnh
        self.header_font = Font(family="Arial", size=14, weight="bold")
        self.label_font = Font(family="Arial", size=10)
        self.button_font = Font(family="Arial", size=10)
        self.label_bg_color = "#dcdad5"
        
    def create_input_fields(self):
        # Tạo các input field với label
        labels = ["Mã mượn trả:", "Mã sách:", "Mã đọc giả:", "Ngày mượn:", "Ngày trả:", "Ngày trả dự kiến:", "Trạng thái:", "Tìm kiếm:"]
        self.entries = {}

        for i, label in enumerate(labels):
            ttk.Label(self.frame_inputs, text=label, background=self.label_bg_color, font=self.label_font).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            
            if label in ["Ngày mượn:", "Ngày trả:", "Ngày trả dự kiến:"]:
                entry = DateEntry(self.frame_inputs, width=18, background="darkblue", foreground="white", date_pattern='yyyy-mm-dd')
            elif label == "Trạng thái:":
                # CHỈ 2 LỰA CHỌN: "Chưa trả" và "Đã trả"
                entry = ttk.Combobox(
                    self.frame_inputs,
                    values=["Chưa trả", "Đã trả"],
                    state="readonly",
                    width=18
                )
                entry.set("Chưa trả")
            else:
                entry = ttk.Entry(self.frame_inputs)
            
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[label] = entry
            
    def create_buttons(self):
        # Tạo các nút điều khiển
        frame_buttons = ttk.Frame(self.frame_inputs, padding=(10, 10))
        frame_buttons.grid(row=11, columnspan=2, pady=(10, 0))

        btn_names = [("Thêm", self.them_muon_tra), ("Sửa", self.sua_muon_tra), ("Xóa", self.xoa_muon_tra), ("Tìm Kiếm", self.tim_kiem)]
        for idx, (text, command) in enumerate(btn_names):
            btn = ttk.Button(frame_buttons, text=text, command=command, style="TButton")
            btn.grid(row=0, column=idx, padx=5, pady=5, ipadx=10)
            
    def create_treeview(self):
        # Tạo Treeview để hiển thị danh sách
        columns = ("Mã mượn trả", "Mã Sách", "Mã đọc giả", "Ngày mượn", "Ngày trả", "Ngày trả dự kiến", "Trạng thái")
        self.tree = ttk. Treeview(self.frame_borrow_manager, columns=columns, show="headings", height=15)
        self.tree.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Định nghĩa tiêu đề cột
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        # Liên kết sự kiện chọn dòng
        self.tree. bind('<<TreeviewSelect>>', self.chon_item)
        
    def load_muon_tra(self):
        # Hàm tải danh sách lên Treeview
        self.cursor.execute("SELECT * FROM Muon_tra ORDER BY ma_muon_tra")
        rows = self.cursor.fetchall()
        
        converted_rows = []
        for row in rows:
            row = list(row)
            ngay_tra = row[4]  # Cột ngày trả
            ngay_tra_du_kien = row[5]  # Cột ngày trả dự kiến
            
            # Logic mới: Dựa vào ngay_tra để xác định trạng thái
            if ngay_tra is not None:
                # Đã có ngày trả → Đã trả
                row[-1] = "Đã trả"
            else:
                # Chưa có ngày trả → Kiểm tra quá hạn
                if isinstance(ngay_tra_du_kien, str):
                    ngay_tra_du_kien = datetime.strptime(ngay_tra_du_kien, '%Y-%m-%d').date()
                
                if ngay_tra_du_kien < date.today():
                    row[-1] = "Quá hạn"
                else:
                    row[-1] = "Chưa trả"
            
            converted_rows.append(row)
        
        self.update_treeview(converted_rows)

    def update_treeview(self, rows):
        # Cập nhật Treeview với màu highlight
        self.tree.delete(*self.tree.get_children())
        
        for row in rows:
            tags = ()
            if row[-1] == "Quá hạn":
                tags = ('overdue',)
            self.tree. insert('', "end", values=row, tags=tags)
        
        # Định nghĩa màu cho tag quá hạn
        self. tree.tag_configure('overdue', background='#ffcccc', foreground='#c62828')
            
    def chon_item(self, event):
        selected_item = self.tree.focus()
        values = self.tree.item(selected_item, 'values')
        if values:
            labels = [
                "Mã mượn trả:",
                "Mã sách:", 
                "Mã đọc giả:", 
                "Ngày mượn:",
                "Ngày trả:",
                "Ngày trả dự kiến:", 
                "Trạng thái:"
            ]
            
            for i, key in enumerate(labels):
                entry = self. entries[key]
                
                if key in ["Ngày mượn:", "Ngày trả:", "Ngày trả dự kiến:"]:
                    if i < len(values) and values[i]:
                        try:
                            entry.set_date(values[i])
                        except:
                            entry. set_date(date.today())
                    else:
                        entry.set_date(date.today())
                elif key == "Trạng thái:":
                    trang_thai_value = values[6]
                    # Nếu là "Quá hạn", set về "Chưa trả" vì Combobox không có "Quá hạn"
                    if trang_thai_value == "Quá hạn":
                        entry.set("Chưa trả")
                    else:
                        entry. set(trang_thai_value)
                else:
                    entry.delete(0, "end")
                    if i < len(values):
                        entry.insert(0, values[i])

    def them_muon_tra(self):
        try:
            # Lấy dữ liệu từ form
            ma_muon_tra_str = self.entries["Mã mượn trả:"].get(). strip()
            ma_sach_str = self.entries["Mã sách:"].get(). strip()
            ma_doc_gia_str = self.entries["Mã đọc giả:"].get().strip()
            ngay_muon = self.entries["Ngày mượn:"].get_date()
            ngay_tra_du_kien = self.entries["Ngày trả dự kiến:"].get_date()
            trang_thai_text = self.entries["Trạng thái:"].get()

            # Validation
            if not ma_muon_tra_str or not ma_sach_str or not ma_doc_gia_str:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
                return

            try:
                ma_muon_tra = int(ma_muon_tra_str)
                ma_sach = int(ma_sach_str)
                ma_doc_gia = int(ma_doc_gia_str)
            except ValueError:
                messagebox.showerror("Lỗi", "Mã phải là số nguyên!")
                return

            # Validate ngày trả dự kiến
            if ngay_tra_du_kien <= ngay_muon:
                messagebox.showerror("Lỗi", "Ngày trả dự kiến phải sau ngày mượn!")
                return

            # Xử lý trạng thái
            if trang_thai_text == "Đã trả":
                trang_thai = 1
                ngay_tra_entry = self.entries["Ngày trả:"].get()
                if not ngay_tra_entry:
                    messagebox.showwarning("Cảnh báo", "Vui lòng chọn ngày trả!")
                    return
                ngay_tra = self.entries["Ngày trả:"].get_date()
                
                # Validate ngày trả
                if ngay_tra < ngay_muon:
                    messagebox. showerror("Lỗi", "Ngày trả phải sau hoặc bằng ngày mượn!")
                    return
            else:  # "Chưa trả"
                trang_thai = 0
                ngay_tra = None  # Set NULL

            # Thêm vào database
            self.cursor.execute("""
                INSERT INTO Muon_tra (ma_muon_tra, ma_sach, ma_doc_gia, ngay_muon, ngay_tra, ngay_tra_du_kien, trang_thai)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (ma_muon_tra, ma_sach, ma_doc_gia, ngay_muon, ngay_tra, ngay_tra_du_kien, trang_thai))

            self.conn.commit()
            self.load_muon_tra()
            messagebox.showinfo("Thành công", "Thêm thông tin mượn sách thành công!")
            
        except mysql.connector.IntegrityError as e:
            if "Duplicate entry" in str(e):
                messagebox.showerror("Lỗi", "Mã mượn trả đã tồn tại!")
            elif "foreign key" in str(e). lower():
                messagebox.showerror("Lỗi", "Mã sách hoặc mã đọc giả không tồn tại!")
            else:
                messagebox.showerror("Lỗi", f"Lỗi database: {e}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thêm: {e}")

    def sua_muon_tra(self):
        try:
            ma_muon_tra = int(self.entries["Mã mượn trả:"]. get())
            ma_sach = int(self.entries["Mã sách:"].get())
            ma_doc_gia = int(self.entries["Mã đọc giả:"].get())
            ngay_muon = self.entries["Ngày mượn:"].get_date()
            ngay_tra_du_kien = self.entries["Ngày trả dự kiến:"].get_date()
            trang_thai_text = self.entries["Trạng thái:"].get()

            # Validate ngày trả dự kiến
            if ngay_tra_du_kien <= ngay_muon:
                messagebox.showerror("Lỗi", "Ngày trả dự kiến phải sau ngày mượn!")
                return

            # Xử lý trạng thái
            if trang_thai_text == "Đã trả":
                trang_thai = 1
                ngay_tra_entry = self.entries["Ngày trả:"].get()
                if not ngay_tra_entry:
                    messagebox.showwarning("Cảnh báo", "Vui lòng chọn ngày trả!")
                    return
                ngay_tra = self.entries["Ngày trả:"].get_date()
                
                if ngay_tra < ngay_muon:
                    messagebox.showerror("Lỗi", "Ngày trả phải sau hoặc bằng ngày mượn!")
                    return
            else:  # "Chưa trả"
                trang_thai = 0
                ngay_tra = None

            # Cập nhật database
            self. cursor.execute("""
                UPDATE Muon_tra 
                SET ma_sach = %s, ma_doc_gia = %s, ngay_muon = %s, 
                    ngay_tra = %s, ngay_tra_du_kien = %s, trang_thai = %s 
                WHERE ma_muon_tra = %s
            """, (ma_sach, ma_doc_gia, ngay_muon, ngay_tra, ngay_tra_du_kien, trang_thai, ma_muon_tra))
            
            self.conn.commit()
            self.load_muon_tra()
            messagebox.showinfo("Thành công", "Cập nhật thông tin thành công!")
            
        except Exception as e:
            messagebox. showerror("Lỗi", f"Không thể cập nhật: {e}")
        
    def xoa_muon_tra(self):
        try:
            ma_muon_tra = int(self.entries["Mã mượn trả:"]. get())
            confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa? ")
            if confirm:
                self.cursor.execute("DELETE FROM Muon_tra WHERE ma_muon_tra = %s", (ma_muon_tra,))
                self.conn.commit()
                self.load_muon_tra()
                messagebox.showinfo("Thành công", "Xóa thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa: {e}")
        
    def tim_kiem(self):
        keyword = self.entries["Tìm kiếm:"].get(). strip()
        if not keyword:
            self.load_muon_tra()
            return
        
        query = """
            SELECT 
                Muon_tra.ma_muon_tra,
                Muon_tra.ma_sach,
                Muon_tra.ma_doc_gia,
                Muon_tra. ngay_muon,
                Muon_tra.ngay_tra,
                Muon_tra.ngay_tra_du_kien,
                Muon_tra.trang_thai
            FROM Muon_tra
            INNER JOIN Doc_gia ON Muon_tra.ma_doc_gia = Doc_gia.ma_doc_gia
            INNER JOIN Sach ON Muon_tra.ma_sach = Sach.ma_sach
            WHERE Doc_gia.ten_doc_gia LIKE %s 
               OR Sach.ten_sach LIKE %s
               OR Muon_tra.ngay_muon LIKE %s
               OR Muon_tra.ma_muon_tra LIKE %s
        """
        self.cursor.execute(query, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
        rows = self.cursor.fetchall()
        
        converted_rows = []
        for row in rows:
            row = list(row)
            ngay_tra = row[4]
            ngay_tra_du_kien = row[5]
            
            # Áp dụng logic tương tự load_muon_tra
            if ngay_tra is not None:
                row[-1] = "Đã trả"
            else:
                if isinstance(ngay_tra_du_kien, str):
                    ngay_tra_du_kien = datetime.strptime(ngay_tra_du_kien, '%Y-%m-%d').date()
                
                if ngay_tra_du_kien < date.today():
                    row[-1] = "Quá hạn"
                else:
                    row[-1] = "Chưa trả"
            
            converted_rows.append(row)
        
        self.update_treeview(converted_rows)

    def tro_ve(self):
        try:
            self.cursor.close()
            self.conn.close()
        except:
            pass
        self.frame_borrow_manager.destroy()
        from main import LibraryManagementScreen
        LibraryManagementScreen(self.root)


if __name__ == "__main__":
    root = tk. Tk()
    app = BorrowManagerScreen(root)
    root.mainloop()