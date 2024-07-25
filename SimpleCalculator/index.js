function clearDisplay() {
  document.getElementById("display").value = "";
}
function append(number) {
  if (number === "N") {
    document.getElementById("display").value = "Created by: Nathanael";
    return;
  }
  document.getElementById("display").value += number;
}
function equate() {
  document.getElementById("display").value = eval(
    document.getElementById("display").value
  );
}
