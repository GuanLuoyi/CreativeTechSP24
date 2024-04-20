# WWW as a Rube Goldberg machine: Infinite Monkey Theorem
## Overview
In recent years on China's social media platform "Weibo," a phenomenon known as "zombie literature" has emerged. This is essentially social media bots randomly extracting text from the internet to generate paragraphs. The mechanically constructed text, through chaotic fetching and ordering, inadvertently creates poetry. This connects with the Infinite Monkey Theorem, where if you give a monkey a typewriter and enough time, it will inevitably type out a Shakespearean sonnet. The disorderly and chaotic text, through random combinations, generates poetry, akin to a rose of poetry blooming from the cyber junk. This application visualizes this concept by generating random words, composing poetry from these words, and finally rendering images inspired by the poetry.


https://github.com/GuanLuoyi/CreativeTechSP24/assets/95225808/6e941d1f-e8e8-47bd-8f79-6517e1915bdf

## Usage
### Generating Words
·Click the "Capture Cyber Sections" button to initiate the random word generation process.  
·The generated words will be displayed in the .text-section of the webpage.
#### API: Random Word API: To generate random words.
### Generating Poem
·After the random words appear, click the "Generate Poem" button that emerges within the #poem-button section.  
·A poem incorporating the random words will be displayed in the #poem-section.
#### API: OpenAI API: For creating poems using GPT-3.5 model.
### Rendering Image
·Once the poem is generated, a "Draw Poem" button will appear in the #img-button section.  
·Clicking this button triggers the image generation process, calling the external API with the poem as the prompt.  
·The rendered image will be centered and displayed in the #img-section.
#### API: Computerender API: To render images based on text prompts.
