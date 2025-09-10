document.addEventListener('DOMContentLoaded', () => {
    const taskInput = document.getElementById('task-text');
    const addTaskBtn = document.getElementById('add-task-btn');
    const taskList = document.getElementById('task-list');

    // Load tasks from local storage
    let tasks = JSON.parse(localStorage.getItem('tasks')) || [];

    const saveTasks = () => {
        localStorage.setItem('tasks', JSON.stringify(tasks));
    };

    const renderTasks = () => {
        taskList.innerHTML = '';
        tasks.forEach((task, index) => {
            const listItem = document.createElement('li');
            listItem.classList.add('task-item');
            if (task.completed) {
                listItem.classList.add('completed');
            }

            listItem.innerHTML = `
                <span class="task-text">${task.text}</span>
                <div class="actions">
                    <button class="complete-btn" data-index="${index}" aria-label="Mark task as complete">
                        &#10003; <!-- Checkmark icon -->
                    </button>
                    <button class="delete-btn" data-index="${index}" aria-label="Delete task">
                        &#10006; <!-- X icon -->
                    </button>
                </div>
            `;
            taskList.appendChild(listItem);
        });
    };

    const addTask = () => {
        const taskText = taskInput.value.trim();
        if (taskText !== '') {
            tasks.push({ text: taskText, completed: false });
            taskInput.value = '';
            saveTasks();
            renderTasks();
        }
    };

    const toggleComplete = (index) => {
        tasks[index].completed = !tasks[index].completed;
        saveTasks();
        renderTasks();
    };

    const deleteTask = (index) => {
        tasks.splice(index, 1);
        saveTasks();
        renderTasks();
    };

    addTaskBtn.addEventListener('click', addTask);

    taskInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            addTask();
        }
    });

    taskList.addEventListener('click', (event) => {
        const target = event.target;
        if (target.classList.contains('complete-btn')) {
            const index = target.dataset.index;
            toggleComplete(index);
        } else if (target.classList.contains('delete-btn')) {
            const index = target.dataset.index;
            deleteTask(index);
        }
    });

    renderTasks();
});
