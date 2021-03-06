import markovify, random, sys

def cleanup_sentence(sentence):
  is_a_index = sentence.find(' is a ')
  sentence = sentence[:is_a_index].title() + sentence[is_a_index:]
  return sentence

def is_good_sentence(sentence):
  word_count = len(sentence.split())
  is_a_index = sentence.find(' is a ')
  # Make sure the format is: {Title} is a {description}
  if is_a_index == -1:
    return False

  # Make sure it's sufficiently long
  if word_count < 5:
    return False

  # Only keep titles that are under a few words
  title_length = len(sentence[:is_a_index].split())
  if title_length > 5:
    return False

  return True

def generate(num_sentences):
  with open('description.txt') as f:
    text = f.read()
  text_model = markovify.Text(text)
  best_sentences = []
  sentence_length = 140
  while True:
    sentence = text_model.make_short_sentence(sentence_length).capitalize()
    if is_good_sentence(sentence):
      sentence = cleanup_sentence(sentence)
      word_count = len(sentence.split())

      # For some short sentences, add another sentence
      if word_count < 11 and random.random() > 0.5:
        second_sentence = text_model.make_short_sentence(sentence_length - len(sentence)).capitalize()
        if second_sentence and second_sentence.find(' is a ') == -1:
          sentence += " " + second_sentence

      best_sentences.append(sentence)
      if len(best_sentences) == num_sentences:
        break;
  return best_sentences

def amazon_lambda_handler(event, context):
  return generate(5)

if __name__ == '__main__':
  print generate(1)[0]
