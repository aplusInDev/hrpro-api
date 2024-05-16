from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from datetime import datetime, date, timedelta


app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}}, supports_credentials=True)

    
@app.route('/upload', methods=['POST'])
def upload_file2():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file:
        df = pd.read_excel(file, skiprows=3, usecols="B:E", names=["name", "start", "end", "absent"])
        df['duration'] = df.apply(lambda row: str(timedelta(seconds=(datetime.combine(date.min, row['end']) - 
                                                                     datetime.combine(date.min, row['start'])).total_seconds()))
                                                                     if row['absent'] else None,
                                  axis=1)
        for col in df.columns:
            df[col] = df[col].astype(str)
        df['absent'] = df['absent'].apply(lambda x: 'No' if x == "nan" else 'Yes')
        print(df)
        return jsonify(df.to_dict(orient='records')), 200


if __name__ == '__main__':
    app.run(debug=True, port=5001)
