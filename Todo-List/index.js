document.getElementById("form").addEventListener("submit", function (e) {
  e.preventDefault();
  addTodo();
});

function addTodo() {
  const todo = document.getElementById("input").value;
  if (todo) {
    const li = document.createElement("li");
    const p = document.createElement("p");
    const div = document.createElement("div");
    const checkbox = document.createElement("input");
    const removeButton = document.createElement("button");

    p.textContent = todo;
    div.className = "todo";
    checkbox.type = "checkbox";
    checkbox.className = "todo-checkbox";
    removeButton.textContent = "Remove";
    removeButton.className = "remove-button";

    li.appendChild(p);
    div.appendChild(checkbox);
    div.appendChild(removeButton);
    li.appendChild(div);
    document.getElementById("todo-items").appendChild(li);

    removeButton.addEventListener("click", function () {
      li.remove();
      updateProgress();
      checkEmptyList();
    });

    checkbox.addEventListener("change", function () {
      if (checkbox.checked) {
        p.style.textDecoration = "line-through"; // Strike through the text
      } else {
        p.style.textDecoration = "none";
      }
      updateProgress();
    });

    document.getElementById("input").value = "";

    // Update progress and check if the list is empty
    updateProgress();
    checkEmptyList();
  }
}

document.getElementById("clear").addEventListener("click", function () {
  document.getElementById("todo-items").innerHTML = "";
  updateProgress();
  checkEmptyList();
});

function updateProgress() {
  const todoItems = document.querySelectorAll("#todo-items li");
  const completedTodos = document.querySelectorAll(
    "#todo-items li .todo-checkbox:checked"
  );
  const progress = todoItems.length
    ? Math.round((completedTodos.length / todoItems.length) * 100)
    : 0;

  document.getElementById("progress").textContent = `${progress}%`;
}

function checkEmptyList() {
  const todoItems = document.querySelectorAll("#todo-items li");
  const noTodosMessage = document.getElementById("no-todos");
  const progress = document.getElementById("progress-container");

  if (todoItems.length === 0) {
    noTodosMessage.style.display = "block";
    progress.style.display = "none";
  } else {
    noTodosMessage.style.display = "none";
    progress.style.display = "block";
  }
}

checkEmptyList();
