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
        for col in df.columns:
            df[col] = df[col].astype(str)
        # convert each row from str to datetime
        df['start'] = df['start'].apply(lambda x: datetime.strptime(x, '%H:%M:%S').time() if x != "nan" else "nan")
        df['end'] = df['end'].apply(lambda x: datetime.strptime(x, '%H:%M:%S').time() if x != "nan" else "nan")
        df['duration'] = df.apply(lambda row: str(
            timedelta(seconds=(datetime.combine(date.min, row['end']) -
                               datetime.combine(date.min, row['start'])).\
                                total_seconds()) if row['absent'] == 'False'
                                and row['start'] != "NaN"
                                and row['end'] != "NaN"
                                else '0:00:00'
                                ),
                        axis=1)
        for col in df.columns:
            df[col] = df[col].astype(str)
        print(df)
        df['absent'] = df['absent'].apply(lambda x: 'No' if x == "False" else 'Yes')
        return jsonify(df.to_dict(orient='records')), 200


if __name__ == '__main__':
    app.run(debug=True, port=5001)
