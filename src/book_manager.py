import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from tkinter.font import Font
from database import get_db_connection
class BookManagerScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý sách")
        self.root.configure(bg="#babfbb")
        self.conn = get_db_connection()
        self.cursor = self.conn.cursor()
        self.create_gui()
        self.load_sach()

    def create_gui(self):
        # Giao diện nhập liệu
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.create_fonts()
        
        self.frame_book_manager = ttk.Frame(self.root)
        self.frame_book_manager.grid(row=0, column=0, sticky="nsew")
        # Nút trở về
        btn_back = ttk.Button(self.frame_book_manager, text="← Trở về", command=self.tro_ve)
        btn_back.grid(row=0, column=0, sticky="W", padx=10, pady=10)
        
        self.frame_inputs = ttk.Frame(self.frame_book_manager, padding=(10, 10))
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
        labels = ["Mã Sách:", "Tên Sách:", "Tác Giả:", "Thể Loại:", "Ngày Xuất Bản:", "Số Lượng:", "Tìm Kiếm:"]
        self.entries = {}

        for i, label in enumerate(labels):
            ttk.Label(self.frame_inputs, text=label, background=self.label_bg_color, font=self.label_font).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            if label == "Ngày Xuất Bản:":
                entry = DateEntry(self.frame_inputs, width=18, background="#dcdad5", foreground="white", date_pattern='yyyy-mm-dd')
            else:
                entry = ttk.Entry(self.frame_inputs)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[label] = entry

    def create_buttons(self):
        # Tạo các nút điều khiển
        frame_buttons = ttk.Frame(self.frame_inputs, padding=(10, 10))
        frame_buttons.grid(row=7, columnspan=2, pady=(10, 0))

        btn_names = [("Thêm", self.them_sach), ("Sửa", self.sua_sach), ("Xóa", self.xoa_sach), ("Tìm Kiếm", self.tim_kiem)]
        for idx, (text, command) in enumerate(btn_names):
            btn = ttk.Button(frame_buttons, text=text, command=command, style="TButton")
            btn.grid(row=0, column=idx, padx=5, pady=5, ipadx=10)

    def create_treeview(self):
        # Tạo Treeview để hiển thị danh sách sách
        columns = ("Mã Sách", "Tên Sách", "Tác Giả", "Thể Loại", "Ngày Xuất Bản", "Số Lượng")
        self.tree = ttk.Treeview(self.frame_book_manager, columns=columns, show="headings", height=15)
        self.tree.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Định nghĩa tiêu đề cột
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        # Liên kết sự kiện chọn dòng
        self.tree.bind('<<TreeviewSelect>>', self.chon_item)

    def load_sach(self):
        # Hàm tải danh sách sách lên Treeview
        self.cursor.execute("SELECT * FROM Sach")
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
                if key == "Tìm Kiếm:":  # Bỏ qua ô Tìm Kiếm
                    continue
                self.entries[key].delete(0, "end")
                if key == "Ngày Xuất Bản:":
                    self.entries[key].set_date(values[i])
                else:
                    self.entries[key].insert(0, values[i])

    def them_sach(self):
        try:
            # Lấy dữ liệu từ giao diện
            ma_sach = (self.entries["Mã Sách:"].get())
            ten_sach = self.entries["Tên Sách:"].get()
            tac_gia = self.entries["Tác Giả:"].get()
            the_loai = self.entries["Thể Loại:"].get()
            ngay_xuat_ban = self.entries["Ngày Xuất Bản:"].get_date()
            so_luong = (self.entries["Số Lượng:"].get())

            if not ten_sach or not ma_sach or not tac_gia or not the_loai or not so_luong or not ngay_xuat_ban:
                messagebox.showerror("Lỗi!", "Các trường dữ liệu không được để trống!")
                return
            
            # Thêm sách vào cơ sở dữ liệu
            self.cursor.execute("INSERT INTO Sach (ma_sach, ten_sach, tac_gia, the_loai, ngay_xuat_ban, so_luong) VALUES (%s, %s, %s, %s, %s, %s)",
                                (ma_sach, ten_sach, tac_gia, the_loai, ngay_xuat_ban, so_luong))
            self.conn.commit()
            self.load_sach()
            messagebox.showinfo("Thành công", "Thêm sách thành công.")
        except mysql.connector.IntegrityError:
            messagebox.showerror("Lỗi", "Mã sách đã tồn tại!")

    def sua_sach(self):
        try:
            selected_item = self.tree.focus()
            old_values = self.tree.item(selected_item, 'values')
            if not old_values:
                messagebox.showerror("Lỗi", "Vui lòng chọn sách cần sửa.")
                return
            
            old_ma_sach = int(old_values[0])
            new_ma_sach = int(self.entries["Mã Sách:"].get())
            ma_sach = (self.entries["Mã Sách:"].get())
            ten_sach = self.entries["Tên Sách:"].get()
            tac_gia = self.entries["Tác Giả:"].get()
            the_loai = self.entries["Thể Loại:"].get()
            ngay_xuat_ban = self.entries["Ngày Xuất Bản:"].get_date()
            so_luong = (self.entries["Số Lượng:"].get())

            if not ten_sach or not tac_gia or not the_loai or not so_luong or not ngay_xuat_ban:
                messagebox.showerror("Lỗi!", "Các trường dữ liệu không được để trống!")
                return
            # Nếu mã sách thay đổi, kiểm tra trùng lặp
            if new_ma_sach != old_ma_sach:
                self.cursor.execute("SELECT COUNT(*) FROM Sach WHERE ma_sach = %s", (new_ma_sach,))
                if self.cursor.fetchone()[0] > 0:
                    messagebox.showerror("Lỗi", "Mã sách đã tồn tại!")
                    return
            self.cursor.execute("UPDATE Sach SET ma_sach = %s, ten_sach = %s, tac_gia = %s, the_loai = %s, ngay_xuat_ban = %s, so_luong = %s WHERE ma_sach = %s",
                            (new_ma_sach, ten_sach, tac_gia, the_loai, ngay_xuat_ban, so_luong, old_ma_sach))
            self.conn.commit()
            self.load_sach()
            messagebox.showinfo("Thành công", "Sửa sách thành công.")
        except mysql.connector.IntegrityError :
            messagebox.showerror("Lỗi", f"Mã sách không tồn tại!")

    def xoa_sach(self):  # xóa sách theo mã
        ma_sach = (self.entries["Mã Sách:"].get())
        answer = messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa sách với mã {ma_sach}?")
        if not answer:
            return
        self.cursor.execute("DELETE FROM Sach WHERE ma_sach = %s", (ma_sach,))
        self.conn.commit()
        self.load_sach()
        # Xóa dữ liệu trên các entry
        for key, entry in self.entries.items():
            if key == "Ngày Xuất Bản:":
                entry.set_date("")
            else:
                entry.delete(0, "end")
        messagebox.showinfo("Thành công", "Xóa sách thành công.")

    def tim_kiem(self):
        # Tìm kiếm sách theo tên hoặc thể loại
        keyword = self.entries["Tìm Kiếm:"].get()
        self.cursor.execute("SELECT * FROM Sach WHERE ten_sach LIKE %s OR the_loai LIKE %s", 
                            (f"%{keyword}%", f"%{keyword}%"))
        rows = self.cursor.fetchall()
        self.update_treeview(rows)

    def tro_ve(self):
        self.frame_book_manager.destroy()
        # Xóa các widget hiện tại của màn hình quản lý sách
        # for widget in self.frame_book_manager.winfo_children():
        #     widget.grid_forget()

        # Quay lại màn hình chính
        from main import LibraryManagementScreen  # Nhập trong hàm để tránh vòng nhập
        main_screen = LibraryManagementScreen(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = BookManagerScreen(root)
    root.mainloop()
