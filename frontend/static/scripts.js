// -----------------------------------------------------------------------------
// 1) Define arrays of background images for each chatbot
// -----------------------------------------------------------------------------
const clothingImages = [
    'static/images/clothing1.jpg',
    'static/images/clothing2.jpg',
    'static/images/clothing3.jpg'
];
const techImages = [
    'static/images/tech1.jpg',
    'static/images/tech2.jpg',
    'static/images/tech3.jpg'
];
const travelImages = [
    'static/images/travel1.jpg',
    'static/images/travel2.jpg',
    'static/images/travel3.jpg'
];

// -----------------------------------------------------------------------------
// 2) Variables for slideshow state
// -----------------------------------------------------------------------------
let currentChatbotType = 'clothing'; // default
let currentImageIndex = 0;
let slideshowInterval = null;

const bgImage1 = document.getElementById('bgImage1');
const bgImage2 = document.getElementById('bgImage2');
let showingImage1 = true;

// -----------------------------------------------------------------------------
// 3) Background Slideshow Logic
// -----------------------------------------------------------------------------
function startSlideshow(type) {
    if (slideshowInterval) {
        clearInterval(slideshowInterval);
    }
    currentImageIndex = 0;
    showingImage1 = true;

    const images = getImagesForType(type);
    bgImage1.style.backgroundImage = `url('${images[0]}')`;
    bgImage1.classList.add('active');
    bgImage2.classList.remove('active');

    slideshowInterval = setInterval(() => {
        currentImageIndex = (currentImageIndex + 1) % images.length;
        crossfadeToNextImage(images[currentImageIndex]);
    }, 5000);
}

function getImagesForType(type) {
    if (type === 'clothing') return clothingImages;
    if (type === 'tech') return techImages;
    if (type === 'travel') return travelImages;
    return [];
}

function crossfadeToNextImage(newImageUrl) {
    if (showingImage1) {
        bgImage2.style.backgroundImage = `url('${newImageUrl}')`;
        bgImage2.classList.add('active');
        bgImage1.classList.remove('active');
        showingImage1 = false;
    } else {
        bgImage1.style.backgroundImage = `url('${newImageUrl}')`;
        bgImage1.classList.add('active');
        bgImage2.classList.remove('active');
        showingImage1 = true;
    }
}

// -----------------------------------------------------------------------------
// 4) Chatbot Logic
// -----------------------------------------------------------------------------
function loadChatbot(type) {
    currentChatbotType = type;
    startSlideshow(type);

    // Clear out the #chatbotDisplay
    const display = document.getElementById('chatbotDisplay');
    display.innerHTML = '';

    // Create the chat interface
    const chatInterface = document.createElement('div');
    chatInterface.style.display = 'flex';
    chatInterface.style.flexDirection = 'column';
    chatInterface.innerHTML = `
        <div id="chatArea"></div>
        <div style="display:flex; align-items:center;">
            <input type="text" id="userInput" placeholder="Ask me anything..." onkeypress="checkEnter(event)" style="flex:1;"/>
            <button onclick="sendMessage()">Send</button>
        </div>
    `;
    display.appendChild(chatInterface);

    // Greet the user
    displayChatMessage('system', `Hello! I am the ${type} Assistant. How can I help you today?`);
}


function getCurrentChatbotType() {
    return currentChatbotType;
}

function displayChatMessage(sender, message) {
    const chatArea = document.getElementById('chatArea');
    if (!chatArea) return;

    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(sender === 'user' ? 'user-message' : 'system-message');
    messageDiv.textContent = message;
    chatArea.appendChild(messageDiv);

    // Trigger reflow to enable transition, then add 'visible' class
    void messageDiv.offsetWidth;
    messageDiv.classList.add('visible');

    chatArea.scrollTop = chatArea.scrollHeight;
}


function sendMessage() {
    const input = document.getElementById('userInput');
    if (!input) return;

    const userInput = input.value.trim();
    const chatbotType = getCurrentChatbotType();

    if (userInput) {
        input.value = '';
        displayChatMessage('user', userInput);

        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_input: userInput,
                chatbot_type: chatbotType
            })
        })
        .then(response => response.json())
        .then(data => {
            displayChatMessage('system', data.response);
        })
        .catch(err => console.error('Error:', err));
    }
}





function checkEnter(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}
