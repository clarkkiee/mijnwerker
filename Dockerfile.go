# --- Tahap 1: Build tahap pertama untuk mengkompilasi aplikasi Go ---
FROM golang:1.23-alpine AS builder

# Tetapkan direktori kerja
WORKDIR /app/processors

# Salin go.mod dan go.sum untuk mengelola dependensi
COPY processors/go.mod processors/go.sum ./

# Unduh semua dependensi
RUN go mod download

# Salin seluruh kode sumber aplikasi Go
COPY processors .

# Kompilasi aplikasi Go ke dalam biner statik
RUN CGO_ENABLED=0 go build -o main .

# --- Tahap 2: Tahap akhir untuk membuat image yang sangat kecil ---
FROM alpine:latest

# Tetapkan direktori kerja
WORKDIR /app/processors

# Salin biner yang sudah dikompilasi dari tahap 'builder'
COPY --from=builder /app/processors/main .

# Atur user non-root untuk keamanan
RUN adduser -D nonroot
USER nonroot

# Perintah default untuk menjalankan aplikasi
CMD [ "./main" ]