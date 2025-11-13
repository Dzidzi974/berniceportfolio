from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='.', static_url_path='')
app.secret_key = 'your-secret-key-here'

# Configuration
UPLOAD_FOLDER = '.'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    # Use your existing images
    profile_image = 'profile.jpg'
    
    project_images = {
        'paySwift': 'fintech.png',           # Your PaySwift image
        'canadianSpending': 'hsehold.jpg',    # Use hsehold.jpg for Canadian project
        'streamflix': 'movies.png',       # Your Streamflix image  
        'tastyBites': 'food.png'        # Your Tasty Bites image
    }
    
    return render_template('index.html', 
                         profile_image=profile_image,
                         project_images=project_images)

@app.route('/upload_profile', methods=['POST'])
def upload_profile():
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        # Save as profile.jpg (overwrite existing)
        filename = 'profile.jpg'
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Profile image uploaded successfully!', 'success')
    else:
        flash('Invalid file type. Please upload PNG, JPG, or JPEG.', 'error')
    
    return redirect(url_for('index'))

@app.route('/upload_project', methods=['POST'])
def upload_project():
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    project_name = request.form.get('project_name')
    
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    if not project_name:
        flash('Please select a project', 'error')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        # Map project names to your existing filenames
        filename_map = {
            'paySwift': 'fintech.png',
            'canadianSpending': 'canada.jpg', 
            'streamflix': 'movies.png',
            'tastyBites': 'food.png'
        }
        
        filename = filename_map.get(project_name, f"{project_name}.jpg")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash(f'Project image for {project_name} uploaded successfully!', 'success')
    else:
        flash('Invalid file type. Please upload PNG, JPG, or JPEG.', 'error')
    
    return redirect(url_for('index'))

@app.route('/download/<project_name>')
def download_project(project_name):
    # Map project names to your actual PDF files - UPDATED WITH CORRECT FILENAMES
    pdf_files = {
        'PaySwift': 'PaySwiftDashboard.pdf',
        'CanadianSpending': 'CanadianSpending.pdf',  # Fixed - using your exact filename
        'Streamflix': 'STREAMFLIX.pdf',
        'TastyBites': 'Tasty Bites Performance.pdf'
    }
    
    pdf_filename = pdf_files.get(project_name)
    if pdf_filename and os.path.exists(pdf_filename):
        return send_from_directory('.', pdf_filename, as_attachment=True)
    else:
        flash(f'PDF file not found: {pdf_filename}', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)