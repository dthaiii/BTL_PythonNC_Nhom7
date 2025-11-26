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
        self.root.geometry("800x600")
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
            background="#4CAF50",  # Màu nền chính
            foreground="white",  # Màu chữ
            borderwidth=0,
        )
        style.map(
            "TButton",
            background=[
                ("active", "#45a049"),  # Màu khi nhấn
                ("hover", "#5ECF60"),  # Màu khi di chuột
            ],
            foreground=[
                ("disabled", "gray"),
            ],
        )

        # Style cho Label
        style.configure(
            "Title.TLabel",
            font=("Arial", 18, "bold"),
            foreground="#333",
            padding=10,
        )

    def create_dashboard(self):
        # Màn hình Dashboard
        self.dashboard_frame = ttk.Frame(self.root, padding=20)
        self.dashboard_frame.grid(row=0, column=0, sticky="nsew")

        # Tiêu đề Dashboard
        dashboard_title = ttk.Label(
            self.dashboard_frame,
            text="Quản lý thư viện",
            style="Title.TLabel",
            anchor="center",
        )
        dashboard_title.grid(row=0, column=0, columnspan=2, pady=10)

        # Nút "Quản lý sách"
        self.book_management_button = self.create_button(
            self.dashboard_frame, "Quản lý Sách", self.book_manager, 1, 0
        )

        # Nút "Quản lý độc giả"
        self.reader_management_button = self.create_button(
            self.dashboard_frame, "Quản lý Độc giả", self.manage_readers, 1, 1
        )

        # Nút "Quản lý mượn sách"
        self.borrow_management_button = self.create_button(
            self.dashboard_frame, "Quản lý Mượn Sách", self.manage_borrows, 2, 0
        )

        # Nút "Thống kê"
        self.report_button = self.create_button(
            self.dashboard_frame, "Thống kê", self.generate_report, 2, 1
        )

        # Thêm lưới căn chỉnh tự động
        self.dashboard_frame.columnconfigure(0, weight=1)
        self.dashboard_frame.columnconfigure(1, weight=1)

    def create_button(self, parent, text, command, row, col):
        """Tạo một nút với hiệu ứng di chuột."""
        button = ttk.Button(parent, text=text, command=command, style="TButton")
        button.grid(row=row, column=col, padx=20, pady=10, sticky="ew")

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
