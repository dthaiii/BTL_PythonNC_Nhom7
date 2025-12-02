import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from tkinter.font import Font
from database import get_db_connection
class ReaderManagerScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý đọc giả")
        self.root.configure(bg="#babfbb")
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()
        self.create_gui()
        self.load_doc_gia()


    def create_gui(self):
        # Giao diện nhập liệu
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.create_fonts()
        
        self.frame_reader_manager = ttk.Frame(self.root)
        self.frame_reader_manager.grid(row=0, column=0, sticky="nsew")
          # Nút trở về
        btn_back = ttk.Button(self.frame_reader_manager, text="← Trở về", command=self.tro_ve)
        btn_back.grid(row=0, column=0, sticky="W", padx=10, pady=10)
            
        self.frame_inputs = ttk.Frame(self.frame_reader_manager, padding=(10, 10))
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
        labels = ["Mã đọc giả:", "Tên đọc giả:", "Ngày sinh:", "Email:", "Số điện thoại:", "Tìm kiếm"]
        self.entries = {}

        for i, label in enumerate(labels):
            ttk.Label(self.frame_inputs, text=label, background=self.label_bg_color, font=self.label_font).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            if label == "Ngày sinh:":
                entry = DateEntry(self.frame_inputs, width=18, background="darkblue", foreground="white", date_pattern='yyyy-mm-dd')
            else:
                entry = ttk.Entry(self.frame_inputs)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[label] = entry

    def create_buttons(self):
        # Tạo các nút điều khiển
        frame_buttons = ttk.Frame(self.frame_inputs, padding=(10, 10))
        frame_buttons.grid(row=7, columnspan=2, pady=(10, 0))

        btn_names = [("Thêm", self.them_doc_gia), ("Sửa", self.sua_doc_gia), ("Xóa", self.xoa_doc_gia), ("Tìm Kiếm", self.tim_kiem)]
        for idx, (text, command) in enumerate(btn_names):
            btn = ttk.Button(frame_buttons, text=text, command=command, style="TButton")
            btn.grid(row=0, column=idx, padx=5, pady=5, ipadx=10)

    def create_treeview(self):
        # Tạo Treeview để hiển thị danh sách đọc giả
        columns = ("Mã đọc giả", "Tên đọc giả", "Ngày sinh", "Email", "Số điện thoại")
        self.tree = ttk.Treeview(self.frame_reader_manager, columns=columns, show="headings", height=15)
        self.tree.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Định nghĩa tiêu đề cột
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        # Liên kết sự kiện chọn dòng
        self.tree.bind('<<TreeviewSelect>>', self.chon_item)

    def load_doc_gia(self):
        # Hàm tải danh sách đọc giả lên Treeview
        self.cursor.execute("SELECT * FROM Doc_gia")
        rows = self.cursor.fetchall()
        self.update_treeview(rows)

    def update_treeview(self, rows):
        # Cập nhật Treeview
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert('', "end", values=row)

    def chon_item(self, event):
        selected_item = self.tree.focus()
        values = self.tree.item(selected_item, 'values')
        if values:
            for i, key in enumerate(self.entries.keys()):
                if key == "Tìm kiếm":  # Bỏ qua ô Tìm Kiếm
                    continue
                self.entries[key].delete(0, "end")
                if key == "Ngày sinh:":
                    self.entries[key].set_date(values[i],)
                else:
                    self.entries[key].insert(0, values[i])

    def them_doc_gia(self):
        try:
            # Lấy dữ liệu từ giao diện
            ma_doc_gia = int(self.entries["Mã đọc giả:"].get())
            ten_doc_gia = self.entries["Tên đọc giả:"].get()
            ngay_sinh = self.entries["Ngày sinh:"].get_date()
            email = self.entries["Email:"].get()
            sdt = self.entries["Số điện thoại:"].get()
            if not ten_doc_gia:
                raise ValueError("Tên đọc giả không được để trống.")
            
            # Thêm đọc giả vào cơ sở dữ liệu
            self.cursor.execute("INSERT INTO doc_gia (ma_doc_gia, ten_doc_gia, ngay_sinh, email, sdt) VALUES (%s, %s, %s, %s, %s)",
                                (ma_doc_gia, ten_doc_gia, ngay_sinh, email, sdt))
            self.conn.commit()
            self.load_doc_gia()
            messagebox.showinfo("Thành công", "Thêm đọc giả thành công.")
        except mysql.connector.IntegrityError:
            messagebox.showerror("Lỗi", "Mã đọc giả đã tồn tại.")

    def sua_doc_gia(self):
        try:
            selected_item = self.tree.focus()
            old_values = self.tree.item(selected_item, 'values')
            if not old_values:
                messagebox.showerror("Lỗi", "Vui lòng chọn đọc giả cần sửa.")
                return

            old_ma_doc_gia = int(old_values[0])
            new_ma_doc_gia = int(self.entries["Mã đọc giả:"].get())
            ten_doc_gia = self.entries["Tên đọc giả:"].get()
            ngay_sinh = self.entries["Ngày sinh:"].get_date()
            email = self.entries["Email:"].get()
            sdt = self.entries["Số điện thoại:"].get()
            if not ten_doc_gia:
                raise ValueError("Tên đọc giả không được để trống.")

            # Nếu mã đọc giả thay đổi, kiểm tra trùng lặp
            if new_ma_doc_gia != old_ma_doc_gia:
                self.cursor.execute("SELECT COUNT(*) FROM doc_gia WHERE ma_doc_gia = %s", (new_ma_doc_gia,))
                if self.cursor.fetchone()[0] > 0:
                    messagebox.showerror("Lỗi", "Mã đọc giả mới đã tồn tại.")
                    return

            # Cập nhật thông tin đọc giả, bao gồm cả mã đọc giả
            self.cursor.execute(
                "UPDATE doc_gia SET ma_doc_gia = %s, ten_doc_gia = %s, ngay_sinh = %s, email = %s, sdt = %s WHERE ma_doc_gia = %s",
                (new_ma_doc_gia, ten_doc_gia, ngay_sinh, email, sdt, old_ma_doc_gia)
            )
            self.conn.commit()
            self.load_doc_gia()
            messagebox.showinfo("Thành công", "Sửa đọc giả thành công.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Sửa đọc giả thất bại: {e}")

    def xoa_doc_gia(self):
        ma_doc_gia = int(self.entries["Mã đọc giả:"].get())
        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa đọc giả có mã {ma_doc_gia}?")
        if confirm:
            self.cursor.execute("DELETE FROM Doc_gia WHERE ma_doc_gia = %s", (ma_doc_gia,))
            self.conn.commit()
            self.load_doc_gia()
            messagebox.showinfo("Thành công", "Xóa đọc giả thành công.")

    def tim_kiem(self):
        keyword = self.entries["Tìm kiếm"].get()
        self.cursor.execute("SELECT * FROM Doc_gia WHERE ten_doc_gia LIKE %s OR email LIKE %s",
                            (f"%{keyword}%", f"%{keyword}%"))
        rows = self.cursor.fetchall()
        self.update_treeview(rows)

    def tro_ve(self):
        self.frame_reader_manager.destroy()
        # Xóa các widget hiện tại của màn hình quản lý sách
        # for widget in self.frame_reader_manager.winfo_children():
        #     widget.grid_forget()

        # Quay lại màn hình chính
        from main import LibraryManagementScreen  # Nhập trong hàm để tránh vòng nhập
        main_screen = LibraryManagementScreen(self.root)


if __name__ == "__main__":
    root = tk.Tk()
    app = ReaderManagerScreen(root)
    root.mainloop()
