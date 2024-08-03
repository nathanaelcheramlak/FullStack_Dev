const restart_button = document.getElementById("restart-btn");
const winmsg = document.getElementById("win-msg");
const choice_x = document.getElementById("X");
const choice_o = document.getElementById("O");
const cells = document.getElementsByClassName("cell");
let active_player = "X";
let game_over = false;

function checkWinnings() {
  const winningCombos = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ];

  for (let combo of winningCombos) {
    let one = cells[combo[0]].innerHTML;
    let two = cells[combo[1]].innerHTML;
    let three = cells[combo[2]].innerHTML;

    if (one && one === two && one === three) {
      winmsg.innerHTML = `${active_player} has Won!`;
      game_over = true;
      return true;
    }
  }

  // Check Draw
  let isDraw = true;
  for (let cell of cells) {
    if (cell.innerHTML === "") {
      return false;
    }
  }

  if (isDraw) {
    winmsg.innerHTML = "Draw!";
    return true;
  }

  return false;
}

function addLetter(e) {
  if (game_over) return;

  const cell = e.target;
  if (cell.innerHTML !== "") return;

  cell.innerHTML = active_player;

  if (checkWinnings()) return;
  if (active_player === "X") {
    active_player = "O";
    choice_o.classList.add("active-choice");
    choice_x.classList.remove("active-choice");
  } else {
    active_player = "X";
    choice_x.classList.add("active-choice");
    choice_o.classList.remove("active-choice");
  }
}

function restartGame() {
  winmsg.innerHTML = "Playing";
  game_over = false;
  active_player = "X";
  for (let cell of cells) {
    cell.innerHTML = "";
  }
}

function addListener() {
  for (let cell of cells) {
    cell.addEventListener("click", addLetter);
  }
}

restart_button.addEventListener("click", restartGame);
addListener();
