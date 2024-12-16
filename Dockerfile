# Gunakan Python 3.9 Slim sebagai base image
FROM python:3.9-slim

# Non-buffering mode untuk Python
ENV PYTHONUNBUFFERED True

# Tentukan direktori kerja di dalam container
ENV APP_HOME /app
WORKDIR $APP_HOME

# Salin file dependencies terlebih dahulu untuk caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file ke dalam container
COPY . .

# Buat folder uploads agar tidak error saat digunakan
RUN mkdir -p uploads

# Expose port 8080 untuk Cloud Run
EXPOSE 8080

# Jalankan aplikasi Flask menggunakan Gunicorn
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8080", "app:app"]
