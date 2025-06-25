from deepmultilingualpunctuation import PunctuationModel

model = PunctuationModel()
with open('../recording.txt', 'r', encoding='utf-8') as f:
    text = f.read()

result = model.restore_punctuation(text)
print(result)