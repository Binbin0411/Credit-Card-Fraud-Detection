document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");
    const fileInput = document.querySelector("input[type='file']");
    const button = document.querySelector("button");

    // Kiểm tra các phần tử có tồn tại
    if (!form || !fileInput || !button) {
        return;
    }

    // Khi chọn file
    fileInput.addEventListener("change", function () {

        if (this.files.length > 0) {

            const file = this.files[0];

            // Chỉ cho phép file CSV
            if (!file.name.toLowerCase().endsWith(".csv")) {

                alert("Please select a CSV file!");

                this.value = "";

                button.textContent = "Analyze File";

                return;
            }

            // Hiển thị tên file
            button.textContent = "Analyze: " + file.name;
        }

    });

    // Khi bấm Analyze
    form.addEventListener("submit", function () {

        if (fileInput.files.length === 0) {

            alert("Please choose a CSV file!");

            return false;
        }

        button.disabled = true;

        button.textContent = "Analyzing...";

    });

});