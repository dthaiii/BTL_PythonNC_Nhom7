import tkinter as tk
from tkinter import ttk
from book_manager import BookManagerScreen  # Import class từ file book_manager.py
from reader_manager import ReaderManagerScreen  # Import class từ file reader_manager.py
from borrow_manager import BorrowManagerScreen  # Import class từ file borrow_manager.py
from library_statistics import LibraryStatisticsScreen # Import class từ file library_statistics.py
from database import initialize_database

class LibraryManagementScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý thư viện")
        self.root.geometry("1200x800")
        self.create_styles()
         # Khởi tạo cơ sở dữ liệu
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        initialize_database()
        self.create_dashboard()
    def create_styles(self):
        # Định nghĩa style chung cho các nút
        style = ttk.Style()
        style.theme_use("clam")
        # Style cho Button
        style.configure(
            "TButton",
            font=("Arial", 12),
            padding=10,
            background="#7C7E7D",  # Màu nền chính
            foreground="white",  # Màu chữ
            borderwidth=0,
        )
        style.configure(
            "Green.TButton",
            background="#4CAF50",
            foreground="white",
            font=("Arial", 12, "bold"),
            padding=12,
        )
        style.configure(
            "Blue.TButton",
            background="#2196F3",
            foreground="white",
            font=("Arial", 12, "bold"),
            padding=12,
        )
        style.configure(
            "Yellow.TButton",
            background="#3B69FF",
            foreground="white",
            font=("Arial", 12, "bold"),
            padding=12,
        )
        style.configure(
            "Red.TButton",
            background="#FF0404",
            foreground="white",
            font=("Arial", 12, "bold"),
            padding=12,
        )        
        style.map(
            "TButton",
            background=[
                ("active", "#A2A6A4"),  # Màu khi nhấn
                ("hover", "#A2A6A4"),  # Màu khi di chuột
            ],
            foreground=[
                ("disabled", "gray"),
            ],
        )

        # Style cho Label
        style.configure(
            "Title.TLabel",
            font=("Arial", 40, "bold"),
            foreground="#111111",
            padding=12,
        )
        style.configure(
            "Shadow.TButton",
            relief="raised",
            borderwidth=4,
        )

    def create_dashboard(self):
        # Màn hình Dashboard
        self.dashboard_frame = ttk.Frame(self.root, padding=(20, 40))
        self.dashboard_frame.grid(row=0, column=0, sticky="nsew")
# Cấu hình grid cho dashboard_frame (3 hàng: tiêu đề, hàng nút, khoảng trống); 2 cột
        for i in range(4):
            self.dashboard_frame.rowconfigure(i, weight=1)
        for j in range(2):
            self.dashboard_frame.columnconfigure(j, weight=1)
        # Tiêu đề Dashboard
        dashboard_title = ttk.Label(
            self.dashboard_frame,
            text="Quản lý thư viện",
            style="Title.TLabel",
            anchor="center",
        )
        dashboard_title.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="ew")

        # Nút "Quản lý sách"
        self.book_management_button = self.create_button(
            self.dashboard_frame, "Quản lý sách", self.book_manager, 1, 0
        )
        self.book_management_button.config(style="Green.TButton")

        # Nút "Quản lý độc giả"
        self.reader_management_button = self.create_button(
            self.dashboard_frame, "Quản lý độc giả", self.manage_readers, 1, 1
        )
        self.reader_management_button.config(style="Blue.TButton")

        # Nút "Quản lý mượn trả"
        self.borrow_management_button = self.create_button(
            self.dashboard_frame, "Quản lý mượn trả", self.manage_borrows, 2, 0
        )
        self.borrow_management_button.config(style="Yellow.TButton")
        # Nút "Thống kê"
        self.report_button = self.create_button(
            self.dashboard_frame, "Thống kê", self.generate_report, 2, 1
        )
        self.report_button.config(style="Red.TButton")
# khoảng trắng dưới cùng để nút luôn ở giữa khi scale cửa sổ
        space_label = ttk.Label(self.dashboard_frame, text="")
        space_label.grid(row=3, column=0, columnspan=2, sticky="nsew")

        # Thêm lưới căn chỉnh tự động
        self.dashboard_frame.columnconfigure(0, weight=1)
        self.dashboard_frame.columnconfigure(1, weight=1)

    def create_button(self, parent, text, command, row, col):
        """Tạo một nút với hiệu ứng di chuột."""
        button = ttk.Button(parent, text=text, command=command, style="TButton")
        button.grid(row=row, column=col, padx=40, pady=20, sticky="ew")

        # Thêm hiệu ứng khi di chuột
        button.bind("<Enter>", lambda e: button.state(["hover"]))
        button.bind("<Leave>", lambda e: button.state(["!hover"]))
        return button
    def book_manager(self):
        self.dashboard_frame.destroy()
        # # Ẩn các widget hiện tại của main screen
        # for widget in self.dashboard_frame.winfo_children():
        #     widget.grid_forget()

        # # Khởi tạo màn hình quản lý sách và hiển thị nó
        self.book_manager_screen = BookManagerScreen(self.root)
    def manage_readers(self):
        self.dashboard_frame.destroy()
        
        #  # Ẩn các widget hiện tại của main screen
        # for widget in self.dashboard_frame.winfo_children():
        #     widget.grid_forget()

        # Khởi tạo màn hình quản lý sách và hiển thị nó
        reader_manager_screen = ReaderManagerScreen(self.root)
    def manage_borrows(self):
        self.dashboard_frame.destroy()
        
        #  # Ẩn các widget hiện tại của main screen
        # for widget in self.dashboard_frame.winfo_children():
        #     widget.grid_forget()

        # Khởi tạo màn hình quản lý sách và hiển thị nó
        borrow_manager_screen = BorrowManagerScreen(self.root)
    def generate_report(self):
        self.dashboard_frame.destroy()
        
        # for widget in self.dashboard_frame.winfo_children():
        #     widget.grid_forget()

        # Khởi tạo màn hình quản lý sách và hiển thị nó
        self.statics_manager_screen = LibraryStatisticsScreen(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementScreen(root)
    root.mainloop()
