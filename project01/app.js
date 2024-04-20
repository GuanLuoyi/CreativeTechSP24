import data from './api_key.json' assert { type: "json" };
const API_KEY = data.APIKey
const API_KEY2 = data.APIKey2
const API_KEY3 = data.APIKey3
const textGenerator = document.querySelector("#initTrigger")
const textSection = document.querySelector(".text-section");
const window = document.querySelector("body")
const poemButtonContainer = document.querySelector("#poem-button")
const poemOutput = document.querySelector("#poem-section");
const imgButtonContainer = document.querySelector("#img-button")
const imgOutput = document.querySelector("#img-section")


const getWords = async () => {
    textSection.innerHTML = '';
    let words = [];

    for (let i = 0; i < 5; i++) {
        try {
            const response = await fetch('https://api.api-ninjas.com/v1/randomword', {
                method: 'GET',
                headers: { 'X-Api-Key': API_KEY },
                contentType: 'application/json'
            });
            const data = await response.json();
            const word = data.word;
            const wordSpan = document.createElement('span');
            wordSpan.textContent = word;
            wordSpan.classList.add('word');

            const x = Math.random() * (window.clientWidth - wordSpan.clientWidth)/2;
            const y = Math.random() * (window.clientHeight - wordSpan.clientHeight)/2;

            wordSpan.style.position = "relative";
            wordSpan.style.left = `${x}px`;
            wordSpan.style.top = `${y}px`;
            wordSpan.style.padding = '0px';
            
            textSection.appendChild(wordSpan);
            words.push(word);
        } catch (error) {
            console.error('Error fetching random word:', error);
        }
    }
    console.log(words);
    poemButtonContainer.innerHTML = ''; 
    const poemButton = document.createElement('button');
    poemButton.textContent = "Generate Poem";
    poemButton.addEventListener('click', () => generatePoem(words));
    poemButtonContainer.appendChild(poemButton);
};

const generatePoem = async (words) => {
  const prompt = `Write a poem using these words: ${words.join(', ')}.`;
  
  const data = {
    model: "gpt-3.5-turbo",
    messages: [{
      role: "system",
      content: "You are a poet."
    },{
      role: "user",
      content: prompt
    }]
  };

  const options = {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${API_KEY2}`,
      'Content-Type': "application/json"
    },
    body: JSON.stringify(data)
  };

  try {
    const response = await fetch('https://api.openai.com/v1/chat/completions', options);
    if (!response.ok) {
      throw new Error(`Server responded with status ${response.status}`);
    }
    const resultData = await response.json();
    const message = resultData.choices[0].message.content; 
    poemOutput.textContent = message; 

    imgButtonContainer.innerHTML = ''; 
    const imgButton = document.createElement('button');
    imgButton.textContent = "Draw Poem";
    imgButton.addEventListener('click', () => generateImg(message));
    imgButtonContainer.appendChild(imgButton);

  } catch (error) {
    console.error('Error generating poem:', error);
    alert(`Error: ${error.message}`); 
  }
};

const generateImg = async (poem) => {
    // Clear the previous image
    imgOutput.innerHTML = '';

    // Use a Blob to handle the image data
    const options = {
        method: 'POST',
        headers: {
            "Authorization": `X-API-Key ${API_KEY3}`
        },
        body: new URLSearchParams({ 'prompt': poem })
    };

    try {
        const response = await fetch('https://api.computerender.com/generate', options);

        if (!response.ok) {
            throw new Error(`Server responded with status ${response.status}`);
        }

        const blob = await response.blob();
        const imageElement = document.createElement('img');
        imageElement.src = URL.createObjectURL(blob);
        imageElement.onload = () => URL.revokeObjectURL(imageElement.src); // Clean up the object URL after loading
        imgOutput.appendChild(imageElement); // Append the image to the imgOutput section

    } catch (error) {
        console.error('Error generating image:', error);
        alert(`Error: ${error.message}`);
    }
};

textGenerator.addEventListener('click', getWords)