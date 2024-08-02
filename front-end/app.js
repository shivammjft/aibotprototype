const inputs = document.querySelectorAll(".input");

function focusFunc() {
  let parent = this.parentNode;
  parent.classList.add("focus");
}

function blurFunc() {
  let parent = this.parentNode;
  if (this.value == "") {
    parent.classList.remove("focus");
  }
}

inputs.forEach((input) => {
  input.addEventListener("focus", focusFunc);
  input.addEventListener("blur", blurFunc);
});

document
  .getElementById("contact-form")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the default form submission

    const formData = new FormData(this);

    const data = {
      company_name: formData.get("company_name"),
      email: formData.get("email"),
      base_link: formData.get("base_link"),
      deployment_link: formData.get("deployment_location"),
      chatbot_name: formData.get("chatbot_name"),
    };
    const fastapiUrl = "http://64.227.160.209/init_company/";

    fetch(fastapiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("FastAPI response:", data);
        // Optionally, handle the response from FastAPI here
        // Optionally reset the form
        document.getElementById("contact-form").reset();
      })
      .catch((error) => {
        console.error("Error submitting to FastAPI:", error);
        alert(
          "There was an error submitting the form. Please try again later."
        );
      });
  });
