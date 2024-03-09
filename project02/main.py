import os
import discord
from discord.ui import View, Button, Modal, TextInput
from keep_alive import keep_alive

keep_alive()


## 1. Create Class Node
class Node:

  def __init__(self, value, answer="", children=[]):
    self.value = value
    self.answer = answer
    self.children = children


### 2. Create Decision Tree
# East Asian Cuisine
dontwantNode = Node('Sorry I cannot help.', answer='No')
spicySichuanNode = Node(
    'Let’s go to Sichuan Impression for some spicy dishes!', answer='No')
beijingRoastDuckNode = Node('Let’s go to Bistro Na’s for Beijing Roast Duck!',
                            answer='Yes')
sushiNode = Node('Let’s go to Sushi Stop for California Rolls!', answer='Yes')
sashimiUdonNode = Node('Let’s go to Osawa for delicious Sashimi and Udon!',
                       answer='No')
friedChickenNode = Node(
    'Let’s go to BBQ Chicken for Garlic Soy Fried Chicken!', answer='Yes')
galbiJjimNode = Node('Let’s go to Sun Nong Dan for Galbi Jjim!', answer='No')

# Vietnamese and Thai Cuisine
phoNode = Node(
    'Let’s go to Phở Bánh Mì Chè Cali for their Special Combination Pho!',
    answer='Yes')
padThaiNode = Node('Let’s go to Ruin Pair for Pad Thai!', answer='Yes')

# Italian Cuisine
pizzaNode = Node(
    'Let’s go to L\'Antica Pizzeria Da Michele for Margherita Pizza!',
    answer='Yes')
risottoNode = Node('Let’s go to Maccheroni Republic for Nero Risotto!',
                   answer='Yes')

## Define nodes for choosing a type of cuisine or dish
# East Asian Choices
chineseNode = Node('Do you wanna try Beijing Roast Duck?',
                   answer='Chinese',
                   children=[beijingRoastDuckNode, spicySichuanNode])
japaneseNode = Node('Do you wanna have some sushi?',
                    answer='Japanese',
                    children=[sushiNode, sashimiUdonNode])
koreanNode = Node('Do you wanna have some korean fried chicken?',
                  answer='Korean',
                  children=[friedChickenNode, galbiJjimNode])
eastAsianNode = Node('Pick one from the List',
                     answer='Yes',
                     children=[chineseNode, japaneseNode, koreanNode])

# Vietnamese Pho and Pad Thai
padThaiQuestionNode = Node('How about Pad Thai?',
                           answer='No',
                           children=[padThaiNode, dontwantNode])
vietnamPhoNode = Node('How about Vietnam Pho?',
                      answer='No',
                      children=[phoNode, padThaiQuestionNode])

# Taco Tuesday
tacoBellNode = Node('Let’s go to Taco Bell for Taco!', answer='Yes')
noTacoNode = Node('Not eating taco on Tuesday is unforgivable.', answer='No')
tacoTuesdayNode = Node('How about a taco Tuesday!',
                       answer='Yes',
                       children=[tacoBellNode, noTacoNode])

# Italian Cuisine Choices
risottoQuestionNode = Node('How about Risotto?',
                           answer='No',
                           children=[risottoNode, dontwantNode])
pizzaQuestionNode = Node('How about Pizza?',
                         answer='Yes',
                         children=[pizzaNode, risottoQuestionNode])
innoutNode = Node('I guess IN-N-OUT is your favorite!', answer='Yes')
americanNode = Node('how about american food?',
                    answer='No',
                    children=[innoutNode, dontwantNode])
italianNode = Node('Do you want to try something Italian?',
                   answer='No',
                   children=[pizzaQuestionNode, americanNode])

asianCuisineNode = Node('Do you want to Try something in East Asia?',
                        answer='Yes',
                        children=[eastAsianNode, vietnamPhoNode])
asianCuisineNode1 = Node('Are you in the mood for Asian cuisine?',
                         answer='No',
                         children=[asianCuisineNode, italianNode])

## Define the root node
root = Node('Is today Tuesday?', children=[tacoTuesdayNode, asianCuisineNode1])


## 3. Create GuessOpition
class GuessOptionView(View):

  def __init__(self, node):
    super().__init__()
    self.node = node  # 当前节点
    for child in node.children:
      self.add_item(GuessButton(child))

  async def handleButtonPress(self, interaction, node):
    # 判断是否有子节点，无子节点表示到达了决策树的叶节点，即最终建议
    if not node.children:
      # 为最终建议的节点创建消息
      await interaction.response.send_message(content=node.value)
    else:
      # 如果有子节点，继续展示下一层的问题或选项
      await interaction.response.send_message(content=node.value,
                                              view=GuessOptionView(node))


## 4. Create GuessButton
class GuessButton(Button):

  def __init__(self, node):
    label = node.answer if node.answer else "Option"
    super().__init__(label=label, style=discord.ButtonStyle.secondary)
    self.node = node

  async def callback(self, interaction):
    if not self.node.children:
      # 当到达叶子节点时，发送节点的 value 并提供一个 WrongView 来收集反馈
      view = WrongView(self.node)
      await interaction.response.send_message(content=self.node.value,
                                              view=view)
    else:
      # 如果有子节点，创建一个新的视图，并用子节点填充
      view = GuessOptionView(self.node)
      await interaction.response.send_message(content=self.node.value,
                                              view=view)


## 5. Create WrongView
class WrongView(View):

  def __init__(self, node):
    super().__init__()
    self.node = node

  @discord.ui.button(label="Provide New Solution")
  async def buttonCallback(self, interaction, button):
    await interaction.response.send_modal(FeedbackModal(self.node))


## 6. Create Feedback Modal
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


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$whatfordinner'):
    await message.channel.send(content=root.value, view=GuessOptionView(root))


token = os.getenv("DISCORD_BOT_SECRET")
client.run(token)
