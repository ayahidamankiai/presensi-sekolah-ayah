from flask import Flask, request, jsonify, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Konfigurasi Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open("nama_peserta_kiai2").sheet1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/presensi', methods=['POST'])
def presensi():
    # Ambil data barcode dari request
    barcode = request.json.get('barcode')

    if not barcode:

        return jsonify({'status': 'error', 'message': 'Barcode tidak ditemukan'}), 400

    # Cari peserta di Google Sheet berdasarkan barcode
    all_records = sheet.get_all_records()
    for record in all_records:
        if str(record['ID']) == barcode:  # Misalkan kolom ID adalah barcode
            # Update kolom presensi (misalnya kolom "Hadir")
            row_number = all_records.index(record) + 2  # Baris dimulai dari 2 karena baris pertama adalah header
            sheet.update_cell(row_number, 3, 'Hadir')  # Kolom 3 adalah kolom "Hadir"
            return jsonify({'status': 'success', 'message': f'Presensi {record["Nama"]} berhasil dicatat'})

    return jsonify({'status': 'error', 'message': 'Peserta tidak ditemukan'}), 404

if __name__ == '__main__':
    app.run(debug=True)