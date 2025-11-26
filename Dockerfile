# Sử dụng Python slim base image
FROM python:3.10-slim

# Cài đặt các công cụ cần thiết
RUN apt-get update && apt-get install -y \
    python3-tk \
    xvfb \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Sao chép file yêu cầu vào container
COPY requirements.txt .

# Cài đặt các thư viện Python cần thiết
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn vào container
COPY . /app
WORKDIR /app

# Thiết lập biến môi trường để Tkinter hoạt động với Xvfb
ENV DISPLAY=:99

# Chạy ứng dụng Tkinter thông qua Xvfb
CMD ["xvfb-run", "python", "main.py"]
