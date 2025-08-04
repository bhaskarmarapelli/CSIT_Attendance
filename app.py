from flask import Flask, request, render_template, redirect, url_for, flash
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for flashing messages

# Load attendance data
df = pd.read_csv('attendance31july.csv')

@app.route('/')
def home():
    return render_template('search.html')

@app.route('/report', methods=['POST'])
def summary():
    student_id = request.form['student_id']
    try:
        student_data = df[df['student_uni_id'] == int(student_id)]
    except ValueError:
        flash(f"Invalid ID format: '{student_id}'", 'danger')
        return redirect(url_for('home'))

    if student_data.empty:
        flash(f"No data found for Student ID: {student_id} Retry with other number", 'warning')
        return redirect(url_for('home'))

    name = student_data['student_name'].iloc[0]
    cgpa = student_data['cgpa'].iloc[0]
    backlogs = student_data['backlogs'].iloc[0]
    councelorname = student_data['counselorname'].iloc[0]
    councelorcontact = student_data['counselorcontact'].iloc[0]
    courses = student_data[[
        'coursecode',
        'coursename',
        'totalclassesconducted',
        'totalclassesattended',
        'attendance_percentage'
    ]].to_dict('records')


    if 'notdeclaredcourses' in student_data.columns:
        notdeclaredcourses = student_data['notdeclaredcourses'].iloc[0]
        notdeclaredcoursessplit = notdeclaredcourses.split("||")

    else:
        notdeclaredcoursessplit = 'Not Available'




    if 'backlogdetails' in student_data.columns:
        backlogdetails = student_data['backlogdetails'].iloc[0]
        backlogdetailssplit = backlogdetails.split("||")

    else:
        backlogdetailssplit = 'No Backlogs'

    return render_template('result.html',
                           student_id=student_id,
                           name=name,
                           cgpa=cgpa,
                           backlogs=backlogs,
                           councelorname=councelorname,
                           courses=courses,
                           councelorcontact=councelorcontact,
                           notdeclaredcoursessplit=notdeclaredcoursessplit,
                           backlogdetailssplit=backlogdetailssplit)

@app.route('/all_reports')
def all_reports():
    all_students = []

    for _, student_data in df.groupby('student_uni_id'):
        student_info = {
            'student_id': student_data['student_uni_id'].iloc[0],
            'name': student_data['student_name'].iloc[0],
            'cgpa': student_data['cgpa'].iloc[0],
            'Postal_Address': student_data['Postal_Address'].iloc[0],
            'phone': student_data['phone'].iloc[0],

            'backlogs': student_data['backlogs'].iloc[0],
            'councelorname': student_data['counselorname'].iloc[0],
            'councelorcontact': student_data['counselorcontact'].iloc[0],
            'courses': student_data[[
                'coursecode',
                'coursename',
                'totalclassesconducted',
                'totalclassesattended',
                'attendance_percentage'
            ]].to_dict('records'),
            'notdeclaredcoursessplit': student_data['notdeclaredcourses'].iloc[0].split("||") if 'notdeclaredcourses' in student_data.columns and pd.notna(student_data['notdeclaredcourses'].iloc[0]) else 'Not Available',

            'backlogdetailssplit': student_data['backlogdetails'].iloc[0].split(
                "||") if 'backlogdetails' in student_data.columns and pd.notna(
                student_data['backlogdetails'].iloc[0]) else 'No Backlogs'
        }
        all_students.append(student_info)

    return render_template('all_results.html', all_students=all_students)



if __name__ == '__main__':
    app.run(debug=True)