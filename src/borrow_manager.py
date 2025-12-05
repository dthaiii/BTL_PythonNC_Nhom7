import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from tkcalendar import DateEntry
from datetime import datetime, date
from tkinter.font import Font
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
            self.style = ttk.Style()
            self.style.theme_use('clam')
            self.create_fonts()
            
            self.frame_borrow_manager = ttk.Frame(self.root)
            self.frame_borrow_manager.grid(row=0, column=0, sticky="nsew")
              # Nút trở về
            btn_back = ttk.Button(self.frame_borrow_manager, text="← Trở về", command=self.tro_ve)
            btn_back.grid(row=0, column=0, sticky="W", padx=10, pady=10)
            
            self.frame_inputs = ttk.Frame(self.frame_borrow_manager, padding=(10, 10))
            self.frame_inputs.grid(row=1, column=0, sticky="W")
            
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
        labels = ["Mã mượn trả:","Mã sách:", "Mã đọc giả:", "Ngày mượn:","Ngày trả:","Ngày trả dự kiến:", "Trạng thái:", "Tìm kiếm:"]
        self.entries = {}

        for i, label in enumerate(labels):
            ttk.Label(self.frame_inputs, text=label, background=self.label_bg_color, font=self.label_font).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            if label in ["Ngày mượn:", "Ngày trả:", "Ngày trả dự kiến:"]:
                entry = DateEntry(self.frame_inputs, width=18, background="darkblue", foreground="white", date_pattern='yyyy-mm-dd')
            elif label == "Trạng thái:":
                entry = ttk.Combobox(self.frame_inputs, values=["Chưa trả", "Đã trả"], state="readonly", width=18)
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
        # Tạo Treeview để hiển thị danh sách sách
        columns = ("Mã mượn trả","Mã Sách", "Mã đọc giả", "Ngày mượn","Ngày trả","Ngày trả dự kiến", "Trạng thái")
        self.tree = ttk.Treeview(self.frame_borrow_manager, columns=columns, show="headings", height=15)
        self.tree.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Định nghĩa tiêu đề cột
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        # Liên kết sự kiện chọn dòng
        self.tree.bind('<<TreeviewSelect>>', self.chon_item)
    def get_trang_thai_text(self, trang_thai_bit, ngay_tra, ngay_tra_du_kien):
        """
        Chuyển đổi trạng thái từ bit và kiểm tra quá hạn
        
        Args:
            trang_thai_bit: 0 (chưa trả) hoặc 1 (đã trả)
            ngay_tra: Ngày trả thực tế (có thể None)
            ngay_tra_du_kien: Ngày trả dự kiến
            
        Returns:
            str: "Chưa trả", "Đã trả", hoặc "Quá hạn"
        """
        if trang_thai_bit == 1:  # Đã trả
            return "Đã trả"
        
        # Chưa trả - kiểm tra quá hạn
        if ngay_tra_du_kien:
            if isinstance(ngay_tra_du_kien, str):
                ngay_tra_du_kien = datetime.strptime(ngay_tra_du_kien, '%Y-%m-%d').date()
            
            if ngay_tra_du_kien < date.today():
                return "Quá hạn"
        
        return "Chưa trả"

    def get_trang_thai_bit(self, trang_thai_text):
        """
        Chuyển đổi text trạng thái sang bit cho database
        
        Args:
            trang_thai_text: "Chưa trả", "Đã trả", hoặc "Quá hạn"
            
        Returns:
            int: 0 (chưa trả/quá hạn) hoặc 1 (đã trả)
        """
        if trang_thai_text == "Đã trả":
            return 1
        else:  # "Chưa trả" hoặc "Quá hạn"
            return 0

    def load_muon_tra(self):
        # Hàm tải danh sách sách lên Treeview
        self.cursor.execute("SELECT * FROM Muon_tra ORDER BY ma_muon_tra DESC")
        rows = self.cursor.fetchall()
        # Chuyển trạng thái 0/1 thành "Chưa trả"/"Đã trả"
        converted_rows = []
        for row in rows:
            row = list(row)
            if row[-1] == 1:
                row[-1] = "Đã trả"
            elif row[-1] == 0:
                ngay_tra_du_kien = row[5]
                if isinstance(ngay_tra_du_kien, str):
                    ngay_tra_du_kien = datetime.strptime(ngay_tra_du_kien, '%Y-%m-%d').date()
                if ngay_tra_du_kien < date.today():
                    row[-1] = "Quá hạn"
                else:
                    row[-1] = "Chưa trả"
            converted_rows.append(row)
        self.update_treeview(converted_rows)

    def update_treeview(self, rows):
        # Cập nhật Treeview
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            tags = ()
            if row[-1] == "Quá hạn":
                tags = ("overdue",)
            self.tree.insert('', "end", values=row, tags=tags)
            
    def chon_item(self, event):
        selected_item = self.tree.focus()
        values = self.tree.item(selected_item, 'values')
        if values:
            self.clear_form()
            # Fill dữ liệu vào form
            self.entries["Mã mượn trả:"].insert(0, values[0])
            self.entries["Mã sách:"].insert(0, values[1])
            self.entries["Mã đọc giả:"].insert(0, values[2])
            
            # Set ngày mượn
            if values[3]:
                self.entries["Ngày mượn:"].set_date(values[3])
            
            # Set ngày trả (có thể null)
            if values[4]:
                self.entries["Ngày trả:"].set_date(values[4])
            
            # Set ngày trả dự kiến
            if values[5]:
                self.entries["Ngày trả dự kiến:"].set_date(values[5])
            # # Set trạng thái
            # trang_thai = self.entries["Trạng thái:"].set(values[6])
            # if trang_thai


    def validate_dates(self, ngay_muon, ngay_tra, ngay_tra_du_kien):
        """
        Validate logic ngày tháng
        
        Returns:
            tuple: (success: bool, error_message: str)
        """
        # Convert to date objects if needed
        if isinstance(ngay_muon, str):
            ngay_muon = datetime.strptime(ngay_muon, '%Y-%m-%d').date()
        if isinstance(ngay_tra_du_kien, str):
            ngay_tra_du_kien = datetime.strptime(ngay_tra_du_kien, '%Y-%m-%d').date()
        if ngay_tra and isinstance(ngay_tra, str):
            ngay_tra = datetime.strptime(ngay_tra, '%Y-%m-%d').date()
        
        # 1. Ngày trả dự kiến phải sau ngày mượn
        if ngay_tra_du_kien <= ngay_muon:
            return False, "Ngày trả dự kiến phải sau ngày mượn!"
        
        # 2. Nếu có ngày trả, phải sau hoặc bằng ngày mượn
        if ngay_tra and ngay_tra < ngay_muon:
            return False, "Ngày trả phải sau hoặc bằng ngày mượn!"
        
        return True, ""

    def them_muon_tra(self):
        try:
            # Lấy dữ liệu từ giao diện
            ma_muon_tra = (self.entries["Mã mượn trả:"].get())
            ma_sach = (self.entries["Mã sách:"].get())
            ma_doc_gia = (self.entries["Mã đọc giả:"].get())
            ngay_muon = self.entries["Ngày mượn:"].get_date()

            ngay_tra = self.entries["Ngày trả:"].get()  # Có thể rỗng nếu chưa trả
            ngay_tra = self.entries["Ngày trả:"].get_date() if ngay_tra else None
            ngay_tra_du_kien = self.entries["Ngày trả dự kiến:"].get_date()
            trang_thai_text = self.entries["Trạng thái:"].get()
            if not ma_muon_tra:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập Mã mượn trả!")
                self.entries["Mã mượn trả:"].focus()
                return
            
            if not ma_sach:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập Mã sách!")
                self.entries["Mã sách:"].focus()
                return
            
            if not ma_doc_gia:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập Mã đọc giả!")
                self.entries["Mã đọc giả:"].focus()
                return
            # Validate logic ngày tháng
            is_valid, error_msg = self.validate_dates(ngay_muon, ngay_tra, ngay_tra_du_kien)
            if not is_valid:
                messagebox.showerror("Lỗi!", error_msg)
                return
            # Lấy trạng thái từ ô nhập, mặc định là 0 nếu rỗng
            trang_thai = self.get_trang_thai_bit(trang_thai_text)
            
            # Thêm thông tin mượn/trả vào bảng Muon_tra
            self.cursor.execute("""
                INSERT INTO Muon_tra (ma_muon_tra, ma_sach, ma_doc_gia, ngay_muon, ngay_tra, ngay_tra_du_kien, trang_thai)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (ma_muon_tra, ma_sach, ma_doc_gia, ngay_muon, ngay_tra, ngay_tra_du_kien, trang_thai))

            self.conn.commit()
            self.load_muon_tra()
            messagebox.showinfo("Thành công", "Thêm thông tin mượn sách thành công.")
            self.clear_form()
        except mysql.connector.IntegrityError:
            messagebox.showerror("Lỗi!", "Sai mã đọc giả hoặc mã sách!")
        except Exception as e:
            messagebox.showerror("Lỗi!", str(e))
        

    def sua_muon_tra(self):
        ma_muon_tra = int(self.entries["Mã mượn trả:"].get())  # Mã mượn trả
        ma_sach = int(self.entries["Mã sách:"].get())  # Mã sách
        ma_doc_gia = int(self.entries["Mã đọc giả:"].get())  # Mã độc giả
        ngay_muon = self.entries["Ngày mượn:"].get_date()  # Ngày mượn
        ngay_tra = self.entries["Ngày trả:"].get_date() if self.entries["Ngày trả:"].get() else None  # Ngày trả
        ngay_tra_du_kien = self.entries["Ngày trả dự kiến:"].get_date()  # Ngày trả dự kiến
        trang_thai_text = self.entries["Trạng thái:"].get()  # Trạng thái: 0 - chưa trả, 1 - đã trả
        trang_thai = int(trang_thai_text) if trang_thai_text in ["0", "1"] else 0

        # Validate logic ngày tháng
        success, error_msg = self.validate_dates(ngay_muon, ngay_tra, ngay_tra_du_kien)
        if not success:
            messagebox.showerror("Lỗi", error_msg)
            return

        # Kiểm tra dữ liệu bắt buộc
        if not ma_sach or not ma_doc_gia or not ngay_muon or not ngay_tra_du_kien:
            raise ValueError("Vui lòng nhập đầy đủ thông tin cần sửa!")
        trang_thai = self.get_trang_thai_bit(trang_thai_text)


        self.cursor.execute("""
                UPDATE Muon_tra 
                SET ma_sach = %s, ma_doc_gia = %s, ngay_muon = %s, 
                    ngay_tra = %s, ngay_tra_du_kien = %s, trang_thai = %s 
                WHERE ma_muon_tra = %s
            """, (ma_sach, ma_doc_gia, ngay_muon, ngay_tra, ngay_tra_du_kien, trang_thai, ma_muon_tra))
        self.conn.commit()
        self.load_muon_tra()
        messagebox.showinfo("Thành công", "Cập nhật thông tin mượn/trả thành công.")
        
    def xoa_muon_tra(self):
        ma_muon_tra = int(self.entries["Mã mượn trả:"].get())
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa đơn mượn trả này không?")
        if confirm:
            self.cursor.execute("DELETE FROM Muon_tra WHERE ma_muon_tra = %s", (ma_muon_tra,))
            self.conn.commit()
            self.load_muon_tra()
            messagebox.showinfo("Thành công", "Xóa đơn mượn trả thành công.")
        
    def tim_kiem(self):
        keyword = self.entries["Tìm kiếm:"].get()
        if not keyword.strip():
            self.load_muon_tra()
            return
        # Truy vấn tìm kiếm với JOIN giữa Muon_tra và Doc_gia
        # Tìm kiếm theo tên đọc giả hoặc ngày mượn, 
        query = """
            SELECT 
                Muon_tra.ma_muon_tra,
                Sach.ten_sach,
                Doc_gia.ten_doc_gia,
                Muon_tra.ngay_muon,
                Muon_tra.ngay_tra,
                Muon_tra.ngay_tra_du_kien,
                Muon_tra.trang_thai
            FROM Muon_tra
            INNER JOIN Doc_gia ON Muon_tra.ma_doc_gia = Doc_gia.ma_doc_gia
            INNER JOIN Sach ON Muon_tra.ma_sach = Sach.ma_sach
            WHERE Doc_gia.ten_doc_gia LIKE %s 
            OR Muon_tra.ngay_muon LIKE %s
            OR Sach.ten_sach LIKE %s
            OR Muon_tra.ma_muon_tra LIKE %s
            OR Muon_tra.ngay_muon LIKE %s
        """
        self.cursor.execute(query, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
        rows = self.cursor.fetchall()
        converted_rows = []
        for row in rows:
            row = list(row)
            trang_thai_text = self.get_trang_thai_text(row[-1], row[4], row[5])
            row[-1] = trang_thai_text
            converted_rows.append(row)
        self.update_treeview(converted_rows)
    def clear_form(self):
        """Xóa form nhập liệu"""
        for key, entry in self.entries.items():
            if key == "Tìm kiếm:":
                continue
            
            if isinstance(entry, DateEntry):
                entry.set_date(date.today())
            elif isinstance(entry, ttk.Combobox):
                entry.set("Chưa trả")
            else:
                entry.delete(0, tk.END)
    def tro_ve(self):
        self.frame_borrow_manager.destroy()
        # # Xóa các widget hiện tại của màn hình quản lý sách
        # for widget in self.frame_borrow_manager.winfo_children():
        #     widget.grid_forget()

        # Quay lại màn hình chính
        from main import LibraryManagementScreen  # Nhập trong hàm để tránh vòng nhập
        main_screen = LibraryManagementScreen(self.root)


if __name__ == "__main__":
    root = tk.Tk()
    app = BorrowManagerScreen(root)
    root.mainloop()
