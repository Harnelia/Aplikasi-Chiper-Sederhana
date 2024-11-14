from flask import Flask, render_template, request, redirect, url_for  
from typing import List, Tuple  

app = Flask(__name__)

def create_rail_fence(text: str, rails: int) -> List[List[str]]:
    """Fungsi untuk membuat matriks rail fence dengan pola zigzag"""
    # Membuat matriks kosong dengan ukuran rails x panjang teks
    fence = [['' for _ in range(len(text))] for _ in range(rails)]
    row, step = 0, 1  # Inisialisasi posisi baris dan arah pergerakan
    
    # Mengisi matriks dengan tanda '*' untuk menandai jalur zigzag
    for col in range(len(text)):
        fence[row][col] = '*'  # Tandai posisi yang akan diisi karakter
        # Logika untuk bergerak zigzag
        if row == 0:  # Jika di baris pertama, bergerak ke bawah
            step = 1
        elif row == rails - 1:  # Jika di baris terakhir, bergerak ke atas
            step = -1
        row += step  # Pindah ke baris berikutnya
    
    return fence

def create_rail_fence_visualization(fence: List[List[str]]) -> str:
    """Fungsi untuk membuat visualisasi HTML dari rail fence"""
    visualization_html = '<div class="rail-fence">'
    # Membuat representasi visual matriks dalam bentuk HTML
    for row in fence:
        visualization_html += '<div class="rail-row">'
        for cell in row:
            if cell and cell != '*':  # Jika sel berisi karakter
                display_char = '-' if cell == ' ' else cell
                visualization_html += f'<div class="rail-cell filled">{display_char}</div>'
            else:  # Jika sel kosong
                visualization_html += '<div class="rail-cell empty"></div>'
        visualization_html += '</div>'
    visualization_html += '</div>' 
    return visualization_html

def encrypt(text: str, rails: int) -> Tuple[str, str, str]:
    """Fungsi untuk melakukan enkripsi teks"""
    fence = create_rail_fence(text, rails)  # Buat matriks rail fence
    row, step = 0, 1
    
    # Mengisi matriks dengan karakter teks input
    for col in range(len(text)):
        fence[row][col] = text[col]
        if row == 0:
            step = 1
        elif row == rails - 1:
            step = -1
        row += step
    
    # Membuat visualisasi dan hasil enkripsi
    visualization = create_rail_fence_visualization(fence)
    # Gabungkan karakter dari setiap baris untuk mendapatkan teks terenkripsi
    ciphertext = ''.join(''.join(row).replace('*', '').replace(' ', '-') for row in fence)
    
    return text, ciphertext, visualization

def decrypt(text: str, rails: int) -> Tuple[str, str, str]:
    """Fungsi untuk melakukan dekripsi teks"""
    fence = create_rail_fence(text, rails)
    idx = 0
    
    # Mengisi matriks secara baris per baris
    for row in range(rails):
        for col in range(len(text)):
            if fence[row][col] == '*' and idx < len(text):
                fence[row][col] = text[idx]
                idx += 1
    
    visualization = create_rail_fence_visualization(fence)
    
    # ikuti pola zig zag
    plaintext = ''
    row, step = 0, 1
    for col in range(len(text)):
        char = fence[row][col].replace('-', ' ')
        plaintext += char
        if row == 0:
            step = 1
        elif row == rails - 1:
            step = -1
        row += step
    
    return plaintext, text, visualization


@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/rail-fence', methods=['GET', 'POST'])
def rail_fence():
    text = request.form.get('text', '')
    rails = int(request.form.get('rail', 3))
    action = request.form.get('action', '')
    
    plaintext, ciphertext, visualization = '', '', ''
    result_label = "Hasil"
   
    if action == 'encrypt' and text:  
        plaintext, ciphertext, visualization = encrypt(text, rails)
        result_label = "Hasil Enkripsi"
    elif action == 'decrypt' and text:  
        plaintext, ciphertext, visualization = decrypt(text, rails)
        result_label = "Hasil Dekripsi"
    elif action == 'reset':  # Jika aksi reset
        text = ''
        rails = 3
        result_label = "Hasil"
    
    # Render template dengan data hasil
    return render_template('index.html',
                         text=text,
                         rail=rails,
                         plaintext=plaintext,
                         ciphertext=ciphertext,
                         visualization=visualization,
                         result_label=result_label,
                         action=action)


if __name__ == '__main__':
    app.run(debug=True)