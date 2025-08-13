# Makefile untuk proyek Python di Windows
#
# Untuk menjalankan, pastikan kamu berada di root direktori proyek
# dan terminal mendukung "make" (misal: Git Bash, MSYS2).
#
# Catatan: Perintah di sini menggunakan syntax Command Prompt/Batch.

.PHONY: setup install run

# =========================================================================
# Variabel
# =========================================================================

# Nama folder virtual environment
VENV_FOLDER = .venv

# Jalur ke Python interpreter di virtual environment
VENV_PYTHON = $(VENV_FOLDER)\Scripts\python.exe

# Jalur ke skrip aktivasi
VENV_ACTIVATE = $(VENV_FOLDER)\Scripts\activate.bat

# =========================================================================
# Perintah (Recipes)
# =========================================================================

# Perintah untuk menyiapkan proyek:
# 1. Membuat virtual environment
# 2. Menginstal semua dependensi dari requirements.txt
setup:
	@echo "--- Membuat virtual environment ---"
	python -m venv $(VENV_FOLDER)
	@echo "--- Menginstal dependensi dari requirements.txt ---"
	$(VENV_FOLDER)\Scripts\pip install -r requirements.txt
	@echo "--- Proyek siap! ---"

# Perintah untuk menginstal dependensi baru
# Berguna jika kamu menambahkan pustaka baru ke requirements.txt
install:
	@echo "--- Menginstal dependensi dari requirements.txt ---"
	$(VENV_FOLDER)\Scripts\pip install -r requirements.txt
	@echo "--- Dependensi berhasil diinstal ---"

# Perintah untuk menjalankan skrip Python utama (misal: main.py)
# Ganti "main.py" dengan nama skrip utama kamu
run:
	@echo "--- Menjalankan skrip utama ---"
	@$(VENV_PYTHON) main.py

# Perintah untuk membersihkan proyek: menghapus virtual environment
clean:
	@echo "--- Menghapus virtual environment ---"
	-rd /s /q $(VENV_FOLDER)
	@echo "--- Selesai ---"