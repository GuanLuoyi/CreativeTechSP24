# Your Decision Maker - What for Dinner?
The Dinner Decision Assistant Bot is a unique Discord application designed to simplify the daily dilemma of choosing what to have for dinner. Utilizing a decision-tree algorithm, this chatbot guides users through a series of questions, narrowing down the choices based on their preferences until a dinner suggestion is made. Whether you're craving Asian cuisine, pondering pasta, or considering a taco Tuesday, this bot makes the decision-making process engaging and straightforward.

## Features
Interactive Decision-Making: Engages users with a series of questions to determine their meal preference for the evening.
Diverse Cuisine Options: Offers suggestions from various cuisines including East Asian, Italian, Vietnamese, and more, ensuring a wide range of dining choices.
Feedback Learning: Incorporates user feedback to expand and refine the decision tree, enhancing the bot's suggestions over time.
User-Friendly Interface: Utilizes Discord's UI components like buttons and modals for a smooth and interactive experience.
Customizable: Allows for easy updates and additions to the decision tree to include new food categories and dining options.

## How It Works
Upon invoking the bot with a specific command (e.g., $whatfordinner), users are presented with an initial question related to their food preferences. Based on their responses, the bot navigates through a pre-defined decision tree, presenting further options or questions until a final suggestion is made. Users dissatisfied with the suggestion can provide feedback through a modal form, contributing to the bot's learning and adaptation.

## Technical Framework

Built on Discord's Python API, leveraging discord.py for bot interactions.
Implements a Node class structure to construct a dynamic decision tree.
Utilizes Discord's UI components, including Views, Buttons, and Modals, to create an interactive user experience.

## Decision Tree Structure

<img width="2490" alt="DecisionTree" src="https://github.com/GuanLuoyi/CreativeTechSP24/assets/95225808/80d45df8-fea2-4f0f-9f5c-fab70dca3067">

## Functions
### Create GuessOpition
```
class GuessOptionView(View):

  def __init__(self, node):
    super().__init__()
    self.node = node 
    for child in node.children:
      self.add_item(GuessButton(child))

  async def handleButtonPress(self, interaction, node):
    if not node.children:
      await interaction.response.send_message(content=node.value)
    else:
      await interaction.response.send_message(content=node.value,
                                              view=GuessOptionView(node))
```
###  Create GuessButton
```
class GuessButton(Button):

  def __init__(self, node):
    label = node.answer if node.answer else "Option"
    super().__init__(label=label, style=discord.ButtonStyle.secondary)
    self.node = node

  async def callback(self, interaction):
    if not self.node.children:
      view = WrongView(self.node)
      await interaction.response.send_message(content=self.node.value,
                                              view=view)
    else:
      view = GuessOptionView(self.node)
      await interaction.response.send_message(content=self.node.value,
                                              view=view)
```
### Create Wrongview
```
class WrongView(View):

  def __init__(self, node):
    super().__init__()
    self.node = node

  @discord.ui.button(label="Provide New Solution")
  async def buttonCallback(self, interaction, button):
    await interaction.response.send_modal(FeedbackModal(self.node))
```

### Create Feedback Modal
```
class FeedbackModal(Modal):

  def __init__(self, node):
    super().__init__(title="Feedback")
    self.node = node
    # Ensure labels are within Discord's character limit
    self.newChoice = TextInput(label="Your choice?")  # Shortened label
    self.newQuestion = TextInput(
        label="A question for your choice?")  # Shortened label
    self.newAnswerYes = TextInput(
        label="Answer leading to your choice?")  # Shortened label
    self.newAnswerNo = TextInput(
        label="Answer for the alternative?")  # Shortened label
    # Add items to the modal
    self.add_item(self.newChoice)
    self.add_item(self.newQuestion)
    self.add_item(self.newAnswerYes)
    self.add_item(self.newAnswerNo)

  async def on_submit(self, interaction):
    # Create new nodes based on feedback
    newNodeChoice = Node(self.newChoice.value, answer="Yes")  # New choice node
    newNodeAlternative = Node(self.node.value,
                              answer="No")  # Node for the previous choice
    # Update the current node to be a decision node with the new question
    self.node.value = self.newQuestion.value
    self.node.answer = ""  # Reset answer since it's now a question node
    self.node.children = [newNodeChoice, newNodeAlternative
                          ]  # Update children to reflect the new structure
    await interaction.response.send_message(
        f'Thank you for your feedback. Now you can choose between {self.newChoice.value} and {self.node.value}!'
    )
```


## Outcome


<img width="472" alt="Screenshot 2024-03-08 at 10 49 03 PM" src="https://github.com/GuanLuoyi/CreativeTechSP24/assets/95225808/bc94153b-c0d7-44d7-a065-c6f7167c5a24">

<img width="609" alt="Screenshot 2024-03-08 at 10 50 03 PM" src="https://github.com/GuanLuoyi/CreativeTechSP24/assets/95225808/872c6395-daa0-418f-8d07-1ff9add2174c">


