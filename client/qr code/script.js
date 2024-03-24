async function generateQRCode() {
    const data = document.getElementById("data").value;
    const version = document.getElementById("version").value;
    const errorCorrection = document.getElementById("errorCorrection").value;
    const boxSize = document.getElementById("boxSize").value;
    const border = document.getElementById("border").value;

    const payload = {
        data: data,
        version: parseInt(version),
        error_correction: errorCorrection,
        box_size: parseInt(boxSize),
        border: parseInt(border)
    };

    try {
        const response = await fetch("http://localhost:8000/api/qrcode/generate/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        const result = await response.json();
        document.getElementById("generateMessage").innerText = result.message;
        document.getElementById("qrImage").src = result.download_link;
        document.getElementById("qrImage").style.display = "block";
        document.getElementById("downloadLink").href = result.download_link;
        document.getElementById("downloadLink").style.display = "block";
    } catch (error) {
        console.error("Error generating QR code:", error);
    }
}

function showFileName() {
    const fileInput = document.getElementById("qrImageFile");
    const fileName = fileInput.files[0] ? fileInput.files[0].name : "Enter the image here";
    const label = document.getElementById("fileLabel");
    label.innerText = fileName;
}

async function readQRCode() {
    const fileInput = document.getElementById("qrImageFile");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select an image file.");
        return;
    }

    const formData = new FormData();
    formData.append("image", file);

    try {
        const response = await fetch("http://localhost:8000/api/qrcode/read/", {
            method: "POST",
            body: formData
        });

        const result = await response.json();
        document.getElementById("readMessage").innerText = `Decoded Data: ${result.qr_data[0].data}, Type: ${result.qr_data[0].type}`;
    } catch (error) {
        console.error("Error reading QR code:", error);
    }
}

function dragOver(event) {
    event.preventDefault();
    document.getElementById("fileDropArea").classList.add('dragging');
    document.getElementById("fileLabel").innerText = "Drop the image here";
}

function dragEnd(event) {
    event.preventDefault();
    document.getElementById("fileDropArea").classList.remove('dragging');
    document.getElementById("fileLabel").innerText = "Enter the image here";
}

function dragLeave(event) {
    event.preventDefault();
    document.getElementById("fileDropArea").classList.remove('dragging');
    document.getElementById("fileLabel").innerText = "Enter the image here";
}

function drop(event) {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    const fileInput = document.getElementById("qrImageFile");
    fileInput.files = event.dataTransfer.files;
    showFileName();
    document.getElementById("fileDropArea").classList.remove('dragging');

    const imageSrc = file ? URL.createObjectURL(file) : "";
    const imageName = file ? file.name : "Enter the image here";

    const imgPreview = `<img src="${imageSrc}" alt="${imageName}" style="max-width: 100%; height: auto;">`;
    document.getElementById("imagePreview").innerHTML = imgPreview;
    document.getElementById("fileLabel").innerText = "";
}



// Attach events
document.addEventListener("DOMContentLoaded", function () {
    let fileDropArea = document.getElementById("fileDropArea");
    fileDropArea.addEventListener("click", function () {
        document.getElementById("qrImageFile").click();
    });
    fileDropArea.addEventListener("dragover", dragOver);
    fileDropArea.addEventListener("dragleave", dragLeave);
    fileDropArea.addEventListener("drop", drop);
});

