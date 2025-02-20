from flask import jsonify, request
from app import app, db
from app import Task, Milestone, Document, Attendance, User
from datetime import datetime
import os

# Task Management APIs
@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'due_date': task.due_date.strftime('%Y-%m-%d'),
        'priority': task.priority,
        'status': task.status
    })

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d') if 'due_date' in data else task.due_date
    task.priority = data.get('priority', task.priority)
    task.status = data.get('status', task.status)
    
    db.session.commit()
    return jsonify({'message': 'Task updated successfully'})

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'})

@app.route('/api/tasks/<int:task_id>/status', methods=['PUT'])
def update_task_status(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    task.status = data.get('status', 'completed')
    db.session.commit()
    return jsonify({'message': 'Task status updated successfully'})

# Milestone Management APIs
@app.route('/api/milestones/<int:milestone_id>', methods=['GET'])
def get_milestone(milestone_id):
    milestone = Milestone.query.get_or_404(milestone_id)
    return jsonify({
        'id': milestone.id,
        'title': milestone.title,
        'description': milestone.description,
        'date': milestone.date.strftime('%Y-%m-%d')
    })

@app.route('/api/milestones/<int:milestone_id>', methods=['PUT'])
def update_milestone(milestone_id):
    milestone = Milestone.query.get_or_404(milestone_id)
    data = request.get_json()
    
    milestone.title = data.get('title', milestone.title)
    milestone.description = data.get('description', milestone.description)
    milestone.date = datetime.strptime(data['date'], '%Y-%m-%d') if 'date' in data else milestone.date
    
    db.session.commit()
    return jsonify({'message': 'Milestone updated successfully'})

@app.route('/api/milestones/<int:milestone_id>', methods=['DELETE'])
def delete_milestone(milestone_id):
    milestone = Milestone.query.get_or_404(milestone_id)
    db.session.delete(milestone)
    db.session.commit()
    return jsonify({'message': 'Milestone deleted successfully'})

# Document Management APIs
@app.route('/api/documents/<int:document_id>', methods=['DELETE'])
def delete_document(document_id):
    document = Document.query.get_or_404(document_id)
    
    # Delete the actual file
    if document.file_path and os.path.exists(document.file_path):
        os.remove(document.file_path)
    
    db.session.delete(document)
    db.session.commit()
    return jsonify({'message': 'Document deleted successfully'})

# Attendance Management APIs
@app.route('/api/attendance', methods=['POST'])
def mark_attendance():
    data = request.get_json()
    
    # Check if attendance already exists for this date
    existing_attendance = Attendance.query.filter_by(
        employee_id=data['employee_id'],
        date=datetime.strptime(data['date'], '%Y-%m-%d').date()
    ).first()
    
    if existing_attendance:
        existing_attendance.status = data['status']
    else:
        new_attendance = Attendance(
            employee_id=data['employee_id'],
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            status=data['status']
        )
        db.session.add(new_attendance)
    
    db.session.commit()
    return jsonify({'message': 'Attendance marked successfully'})

@app.route('/api/attendance', methods=['GET'])
def get_attendance():
    employee_id = request.args.get('employee_id', type=int)
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    
    attendance_records = Attendance.query.filter(
        Attendance.employee_id == employee_id,
        db.extract('year', Attendance.date) == year,
        db.extract('month', Attendance.date) == month
    ).all()
    
    return jsonify([{
        'date': record.date.strftime('%Y-%m-%d'),
        'status': record.status
    } for record in attendance_records]) 