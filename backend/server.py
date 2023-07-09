from flask import Flask, request, jsonify
from flask_cors import CORS
from main import *

query_image = ''
radius = 0
knn = 0

app = Flask(__name__)
CORS(app, origins='http://localhost:5173')

@app.route("/knn-seq-range-search")
def knn_seq_range_search():
    result = knn_seq_range_search_exec(query_image, radius)
    picture_list = result[0]
    execution_time = result[1]
    formatted_pictures = [{"filename": filename, "score": score} for filename, score in picture_list]
    return {"pictures": formatted_pictures, "execution_time": execution_time}

@app.route("/knn-seq-knn-search")
def knn_seq_knn_search():
    result = knn_seq_knn_search_exec(query_image, knn)
    picture_list = result[0]
    execution_time = result[1]
    formatted_pictures = [{"filename": filename, "score": score} for filename, score in picture_list]
    return {"pictures": formatted_pictures, "execution_time": execution_time}

@app.route("/knn-rtree-range-search")
def knn_rtree_range_search():
    result = knn_rtree_range_search_exec(query_image, radius)
    picture_list = result[0]
    execution_time = result[1]
    formatted_pictures = [{"filename": filename, "score": score} for filename, score in picture_list]
    return {"pictures": formatted_pictures, "execution_time": execution_time}

@app.route("/knn-rtree-knn-search")
def knn_rtree_knn_search():
    result = knn_rtree_knn_search_exec(query_image, knn)
    picture_list = result[0]
    execution_time = result[1]
    formatted_pictures = [{"filename": filename, "score": score} for filename, score in picture_list]
    return {"pictures": formatted_pictures, "execution_time": execution_time}

@app.route("/knn-kdtree-knn-search")
def knn_kdtree_knn_search():
    result = knn_kdtree_knn_search_exec(query_image, knn)
    picture_list = result[0]
    execution_time = result[1]
    formatted_pictures = [{"filename": filename, "score": score} for filename, score in picture_list]
    return {"pictures": formatted_pictures, "execution_time": execution_time}

@app.route("/knn-kdtree-knn-search-live")
def knn_kdtree_knn_search_live():
    knn_kdtree_knn_search_live_exec()

@app.route('/send-input', methods=['POST'])
def send_input():
    global query_image, radius, knn

    if 'imageFile' not in request.files:
        return jsonify({'error': 'No file found'}), 400

    file = request.files['imageFile']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    file.save(os.path.join('./query_images', file.filename))
    query_image = os.path.join('./query_images', file.filename)
    
    if 'typeValue' not in request.form:
        return jsonify({'error': 'No valueType provided'}), 400
    
    valueType = request.form['typeValue']

    if 'numberValue' not in request.form:
        return jsonify({'error': 'No numberValue provided'}), 400
    
    value = request.form['numberValue']
    
    if valueType == 'knn':
        try:
            value = int(value)
        except ValueError:
            return jsonify({'error': 'Invalid knn value'}), 400
        knn = value
        return jsonify({'message': 'File uploaded successfully', 'query_image': query_image, 'knn': knn}), 200
    else:
        try:
            value = float(value)
        except ValueError:
            return jsonify({'error': 'Invalid radius value'}), 400
        radius = value
        return jsonify({'message': 'File uploaded successfully', 'query_image': query_image, 'radius': radius}), 200

if __name__ == "__main__":
    app.run(debug=True)