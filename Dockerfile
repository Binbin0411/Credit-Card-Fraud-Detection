# 1. Sử dụng Python image bản nhẹ
FROM python:3.10-slim

# 2. Thiết lập thư mục làm việc trong container
WORKDIR /app

# 3. Sao chép và cài đặt các thư viện phụ thuộc
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Sao chép toàn bộ mã nguồn vào container
COPY . .

# 5. Khai báo cổng (mặc định Render sử dụng biến môi trường $PORT, nếu không có sẽ dùng 5000)
ENV PORT=5000
EXPOSE $PORT

# 6. Khởi chạy ứng dụng Flask với Gunicorn hoặc trực tiếp qua Python
# Dùng sh -c để đọc biến môi trường $PORT do Render truyền vào
CMD ["sh", "-c", "python app.py --host=0.0.0.0 --port=$PORT"]