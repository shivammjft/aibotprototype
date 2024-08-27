import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [popupVisible, setPopupVisible] = useState(false);

  const [formData, setFormData] = useState({
    email: "",
    company_name: "",
    chatbot_name: "",
    base_link: "",
    deployment_link: "",
  });

  const [focus, setFocus] = useState({
    email: false,
    company_name: false,
    chatbot_name: false,
    base_link: false,
    deployment_link: false,
  });

  useEffect(() => {
    const inputs = document.querySelectorAll(".input");

    function focusFunc(e) {
      let parent = e.target.parentNode;
      parent.classList.add("focus");
    }

    function blurFunc(e) {
      let parent = e.target.parentNode;
      if (e.target.value === "") {
        parent.classList.remove("focus");
      }
    }

    inputs.forEach((input) => {
      input.addEventListener("focus", focusFunc);
      input.addEventListener("blur", blurFunc);
    });

    return () => {
      inputs.forEach((input) => {
        input.removeEventListener("focus", focusFunc);
        input.removeEventListener("blur", blurFunc);
      });
    };
  }, []);

  function snackbarShow() {
    var x = document.getElementById("snackbar");
    x.className = "show";
    setTimeout(function () {
      x.className = x.className.replace("show", "");
    }, 3000);
  }

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    axios
      .post("http://localhost:8000/init_company/", JSON.stringify(formData), {
        headers: {
          "Content-Type": "application/json",
        },
      })
      .then((response) => {
        console.log("Success response:", response.data);
        snackbarShow();
        setFormData({
          email: "",
          company_name: "",
          chatbot_name: "",
          base_link: "",
          deployment_link: "",
        });
      })
      .catch((error) => {
        console.error("Error submitting to FastAPI:", error);
      });
  };

  return (
    <>
      <div className="App">
        <div className="overlay" id="overlay"></div>
        <div className="logo-container">
          <img
            src="logo.png"
            alt="Jellyfish Technologies Logo"
            className="logo"
          />
        </div>
        <div className="container">
          <span className="big-circle"></span>
          <img src="img/shape.png" className="square" alt="" />
          <div className="form">
            <div className="contact-info">
              <h3 className="title">Let's get in touch</h3>
              <p className="text">
                Jellyfish Technologies is your go-to partner for innovative
                chatbot solutions and custom software development. With over 13
                years of experience and 4000+ successful projects, we empower
                businesses with cutting-edge technology.
              </p>

              <div className="info">
                <div className="information">
                  <i className="fas fa-map-marker-alt"></i> &nbsp; &nbsp;
                  <p>
                    D5 3rd floor, Logix Infotech Park, D Block, Sector 59,
                    Noida, Uttar Pradesh 201301
                  </p>
                </div>
                <div className="information">
                  <i className="fas fa-envelope"></i> &nbsp; &nbsp;
                  <p>contact@jellyfishtechnologies.com</p>
                </div>
              </div>

              <div className="social-media">
                <p>Connect with us :</p>
                <div className="social-icons">
                  <a href="https://www.facebook.com/teamjft/?locale=hi_IN&_rdr">
                    <i className="fab fa-facebook-f"></i>
                  </a>
                  <a href="https://x.com/teamjft?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor">
                    <i className="fab fa-twitter"></i>
                  </a>
                  <a href="https://www.instagram.com/teamjft/?hl=en">
                    <i className="fab fa-instagram"></i>
                  </a>
                  <a href="https://www.linkedin.com/company/teamjft">
                    <i className="fab fa-linkedin-in"></i>
                  </a>
                </div>
              </div>
            </div>

            <div className="contact-form">
              <span className="circle one"></span>
              <span className="circle two"></span>
              <form id="contact-form" onSubmit={handleSubmit}>
                <h3 className="title">Contact us</h3>
                <div className="input-container">
                  <input
                    type="email"
                    name="email"
                    className={`input ${focus.email ? "focus" : ""}`}
                    value={formData.email}
                    onChange={handleChange}
                    required
                  />
                  <label htmlFor="email">Your Email</label>
                  <span>Enter Your Email</span>
                </div>

                <div className="input-container textarea">
                  <textarea
                    name="company_name"
                    className={`input ${focus.company_name ? "focus" : ""}`}
                    value={formData.company_name}
                    onChange={handleChange}
                    required
                  ></textarea>
                  <label htmlFor="company_name">Company Name</label>
                  <span>Enter Your Company Name</span>
                </div>
                <div className="input-container">
                  <input
                    type="text"
                    name="chatbot_name"
                    className={`input ${focus.chatbot_name ? "focus" : ""}`}
                    value={formData.chatbot_name}
                    onChange={handleChange}
                    required
                  />
                  <label htmlFor="chatbot_name">Chatbot Name</label>
                  <span>Enter Your Chatbot Name</span>
                </div>
                <div className="input-container">
                  <input
                    type="url"
                    name="base_link"
                    className={`input ${focus.base_link ? "focus" : ""}`}
                    value={formData.base_link}
                    onChange={handleChange}
                    required
                  />
                  <label htmlFor="base_link">Source URL</label>
                  <span>Enter Your Source URL</span>
                </div>
                <div className="input-container">
                  <input
                    type="url"
                    name="deployment_link"
                    className={`input ${focus.deployment_link ? "focus" : ""}`}
                    value={formData.deployment_link}
                    onChange={handleChange}
                    required
                  />
                  <label htmlFor="deployment_link">Deployment Location</label>
                  <span>Enter Your Deployment Location</span>
                </div>
                <input type="submit" value="Send" className="btn" />
              </form>
            </div>
          </div>
        </div>
      </div>
      <div id="snackbar">
        Thank you for your response. We appreciate your patience as we proceed
        with training your bot. We will send you an email with further details
        once the training process is complete. Please keep an eye on your inbox
        for updates.
      </div>
    </>
  );
}

const Popup = ({ message, onClose }) => {
  return (
    <div className="popup-overlay">
      <div className="popup-content">
        <p>{message}</p>
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
};

export default App;
