from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

# Load attendance data
df = pd.read_csv('merged_output.csv',encoding='latin1')

@app.route('/')
def home():
    return render_template('search.html')

@app.route('/summary', methods=['POST'])
def summary():
    student_id = request.form['student_id']
    student_data = df[df['student_uni_id'] == int(student_id)]

    if student_data.empty:
        return f"No data found for Student ID: {student_id}"
    """
    # Aggregate values
    columns_to_sum = [
        'total classes conducted',
        'total classes attended'
    ]
    summary_data = student_data[columns_to_sum].sum().to_dict()

    # Total average attendance percentage
    attendance_percentage = round(student_data['attendance_percentage'].mean(), 2)
    """
    # Prepare course attendance breakdown
    courses = student_data[['student_name','counselorname','coursecode','coursename', 'totalclassesconducted','totalclassesattended','attendance_percentage']].to_dict('records')
    #name = student_data[['student_name']].to_dict('records')
    #councelor = student_data[['counselorname']].to_dict('records')
    return render_template('result.html',
                           student_id=student_id,
                            courses=courses
                           )

if __name__ == '__main__':
    app.run(debug=True)