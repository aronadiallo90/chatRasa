
    let lastButtons = [];

    function appendMessage(text, sender) {
        let chatBox = document.getElementById("chat-box");
        let messageDiv = document.createElement("div");
        messageDiv.classList.add("message", sender === "bot" ? "bot-message" : "user-message");
        messageDiv.innerText = text;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function appendButtons(buttons) {
        let chatBox = document.getElementById("chat-box");
        let buttonContainer = document.createElement("div");
        buttonContainer.classList.add("button-container");

        buttons.forEach(button => {
            let buttonElement = document.createElement("button");
            buttonElement.classList.add("chat-button");
            buttonElement.innerText = button.title;
            buttonElement.onclick = () => {
                disableButtons();
                sendMessage(button.payload);
            };
            buttonContainer.appendChild(buttonElement);
        });

        lastButtons = buttonContainer;
        chatBox.appendChild(buttonContainer);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function disableButtons() {
        if (lastButtons) {
            Array.from(lastButtons.children).forEach(btn => btn.disabled = true);
        }
    }

    function sendMessage(payload) {
        fetch("http://localhost:5005/webhooks/rest/webhook", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ sender: "user", message: payload })
        })
        .then(response => response.json())
        .then(data => {
            let foundButtons = false;
            data.forEach(res => {
                if (res.text) appendMessage(res.text, "bot");
                if (res.buttons) {
                    foundButtons = true;
                    appendButtons(res.buttons);
                }
            });
            if (!foundButtons) appendButtons([{ title: "Retour", payload: "/go_back" }]);
        })
        .catch(error => console.error("Erreur:", error));
    }

    function sendUserMessage() {
        let userInput = document.getElementById("user-input").value.trim();
        if (userInput === "") return;
        appendMessage(userInput, "user");
        sendMessage(userInput);
        document.getElementById("user-input").value = "";
    }

    function restartChat() {
        document.getElementById("chat-box").innerHTML = "";
        sendMessage("/greet");
    }

    function fermerChat() {
        document.getElementById("chat-container").style.display = "none";
        document.getElementById("open-chat-icon").style.display = "flex";
    }

    function ouvrirChat() {
        document.getElementById("chat-container").style.display = "flex";
        document.getElementById("open-chat-icon").style.display = "none";
    }

    window.onload = () => sendMessage("/greet");
