from flask import Flask, render_template, request, redirect, url_for
import random
import string

app = Flask(__name__)

# Data storage (for simplicity, use a Python dictionary)
groups = {}

# Route to create a group and generate a code
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        group_name = request.form.get('group_name')
        if group_name:
            code = generate_code()
            groups[code] = {'name': group_name, 'tasks': [], 'members': [], 'announcements': []}
            return redirect(url_for('dashboard', code=code))
        else:
            return 'Invalid group name', 400
    return render_template('index.html')

# Function to generate a unique group code
def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# Route to join a group using a code
@app.route('/join-group', methods=['POST'])
def join_group():
    code = request.form.get('code')
    if code in groups:
        return redirect(url_for('dashboard', code=code))
    else:
        return 'Invalid code', 400

# Route for the dashboard
@app.route('/dashboard/<code>', methods=['GET', 'POST'])
def dashboard(code):
    if code in groups:
        group = groups[code]

        if request.method == 'POST':
            # Handle the form submission for marking a task as done
            task_index = int(request.form.get('task_index'))
            mark_task_as_done(group, task_index)

            # Handle the form submission for publishing an announcement
            announcement_text = request.form.get('announcement_input').strip()
            if announcement_text:
                group['announcements'].append(announcement_text)

        task_list = group.get('tasks', [])

        return render_template('dashboard.html', group=group, g_code=code)
    else:
        return 'Invalid code', 400

# Route for the task_list page
@app.route('/task_list/<code>', methods=['GET', 'POST'])
def task_list(code):
    if code in groups:
        group = groups[code]

        if request.method == 'POST':
            # Handle the form submission for adding tasks
            task_name = request.form.get('task_name')
            responsible_person = request.form.get('responsible_person')

            # Add the new task to the group
            group['tasks'].append({'name': task_name, 'responsible': responsible_person})

        return render_template('task_list.html', group=group)
    else:
        return 'Invalid code', 400

# Function to mark a task as done
def mark_task_as_done(group, task_index):
    tasks = group['tasks']
    if 0 <= task_index < len(tasks):
        # Move the completed task to the bottom
        completed_task = tasks.pop(task_index)
        tasks.append(completed_task)
        # Implement logic to highlight the next person or update as needed
        # You can also update other properties of the task, such as completion time
    else:
        return 'Invalid task index', 400

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
