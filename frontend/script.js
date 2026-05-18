async function analyzeFile() {
  const fileInput = document.getElementById("fileInput");
  const output = document.getElementById("output");

  if (!fileInput.files.length) {
    alert("Please select a file.");
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  output.textContent = "Analyzing...";

  const response = await fetch("http://127.0.0.1:8001/analyze", {
    method: "POST",
    body: formData,
  });

  const data = await response.json();
  output.textContent = JSON.stringify(data, null, 2);
}