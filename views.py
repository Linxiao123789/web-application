from flask import render_template, flash, redirect, session, url_for, request, g
from flask_admin.contrib.sqla import ModelView
import datetime
from app import app, db, admin
from sqlalchemy import true, false

from .models import  Task

from .forms import  TaskForm


admin.add_view(ModelView(Task, db.session))

@app.route("/")

def getAlltask():
    tasks = Task.query.all()
    return render_template('index.html',
                           title='ToDoList',
                           tasks=tasks)




@app.route('/create_task', methods=['GET','POST'])
def create_task():
    form = TaskForm()
    flash('Errors="%s"' %
          (form.errors))
    if form.validate_on_submit():
        t = Task(date=form.date.data, title=form.title.data, description=form.description.data, status=form.status.data)
        db.session.add(t)
        db.session.commit()
        return redirect('/')

    return render_template('create_task.html',
                           title='Create Task',
                           form=form)


"""Display all completed tasks"""
@app.route('/completed_task', methods=['GET'])
def getAllcompleted_task():
    completed_tasks = Task.query.filter_by(status=True).all()
    return render_template('completed_list.html',
                           title='All completed tasks',
                           completed_tasks=completed_tasks)

"""Display all uncompleted tasks"""
@app.route('/uncompleted_task', methods=['GET'])
def getAlluncompleted_task():
    uncompleted_tasks = Task.query.filter_by(status=False).all()
    return render_template('uncompleted_list.html',
                           title='All uncompleted tasks',
                           uncompleted_tasks=uncompleted_tasks)

"""Display all recent tasks"""
@app.route('/recent_task', methods=['GET'])
def getAllrecent_task():
    recentdays = []
    """get the following seven days"""
    for i in range(7):
        recentday = ((datetime.date.today() + datetime.timedelta(days=i)))
        recentdays.append(recentday)
    alltasks = Task.query.all()
    tasks = []
    for task in alltasks:
        for recentday in recentdays:
            if task.date == recentday:
                tasks.append(task)


    return render_template('recent_task.html',
                           title='All recent tasks',
                           recent_tasks=tasks)

"""Edit a specific task"""
@app.route('/edit/<id>', methods=['GET','POST'])
def edit_task(id):
    task = Task.query.get(id)
    form = TaskForm(obj=task)
    flash('Errors="%s"' %
          (form.errors))
    if form.validate_on_submit():
        t = task
        t.date = form.date.data
        t.title = form.title.data
        t.description = form.description.data

        db.session.commit()
        return redirect('/')

    return render_template('edit_task.html',
                           title='Edit Task',
                           form=form)


"""Delete useless task"""
@app.route('/delete/<id>', methods=['GET'])
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/')

"""Mark task as complete"""
@app.route('/finish/<id>', methods=['GET'])
def finish_task(id):
    task = Task.query.get(id)
    task.status = True
    db.session.commit()
    return redirect('/')
