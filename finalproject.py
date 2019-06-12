## Final Project (finalproject)

## Text Modeling

import math

def clean_text(txt):
    """ takes a string of text txt as a parameter and returns a
        list containing the words in txt after it has been “cleaned”
    """
    newtxt = txt.lower()
    newtxt = newtxt.replace('.', '').replace(',', '').replace('!', '')\
             .replace('?', '').replace(':', '').replace(';', '')\
             .replace('"', '').replace('/', '').replace('-', '')\
             .replace('(', '').replace(')', '')
    return newtxt
##    for i in range(len(txt)):
##        if newtxt[i] in '.,!?:;"/-()':
##            newtxt = newtxt[:i] + newtxt[i+1:]
##    return newtxt
            
def stem(s):
    """ return the stem of s """
    if len(s) < 4:
        return s
    elif s[-2:] == 'er':
        if s[-4] == s[-3]:
            return s[:-3]
        else:
            return s[:-2]
    elif s[-3:] == 'ing':
        if len(s) > 5:
            if s[-5] == s[-4]:
                return s[:-4]
            else:
                return s[:-3]
        else:
            return s
    elif s[-2:] != 'ly':
        if s[-1] == 'y':
            return s[:-1]
        elif s[-3:] == 'ier':
            return s[:-3]
        elif s[-4:] == 'iers':
            return s[:-4]
        elif s[-3:] == 'ies':
            return s[:-3]
        elif s[-3:] == 'ied':
            return s[:-3]
        elif s[-2:] == 'ed':
            if s[-4] == s[-3]:
                return s[:-3]
            else:
                return s[:-2]
        elif s[-2:] == 'es':
            return s[:-2]
        elif s[-1] == 's':
            return s[:-1]
        elif s[-1] == 'e':
            return s[:-1]
        else:
            if len(s) > 3:
                return s[:4]
    elif s[-2:] == 'ly':
            if s[-3] == 'i':
                return s[:-3]
            else:
                return s[:-2]
    else:
        return s

def compare_dictionaries(d1, d2):
    """ take two feature dictionaries d1 and d2 as inputs,
        and it should compute and return their log similarity score
    """
    score = 0
    total_list = [d1[i] for i in d1]
    total = sum(total_list)
    for i in d2:
        if i in d1:
            score += math.log(d1[i]/total) * d2[i]
        else:
            score += math.log(0.5/total) * d2[i]
    return round(score, 3)

class TextModel:
    """ text modeling
    """
    def __init__(self, model_name):
        """ constructor
        """
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.punctuation = {}

    def __repr__(self):
        """Return a string representation of the TextModel
        """
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths))\
              + '\n'
        s += '  number of punctuations: ' + str(len(self.punctuation))
        return s

    def add_string(self, s):
        """Analyzes the string txt and adds its pieces
           to all of the dictionaries in this text model.
        """
        new_s = s
        new_s = new_s.replace('?', '.').replace('!', '.')

        spacecount = 0
        spacelist = []

        for w in range(len(new_s)):
            if new_s[w] == '.':
                spacelist += [spacecount]
                spacecount = 0
            elif new_s[w] == ' ':
                if new_s[w-1] == ' ' and new_s[w+1] == ' ':
                    spacecount += 0
                else:
                    spacecount += 1
                
##        senlen_list = new_s.split('.')
##        for i in range(len(senlen_list)):
##            num_words = senlen_list[i].split(' ')
        
        for l in spacelist:
            if l not in self.sentence_lengths:
                self.sentence_lengths[l] = 1
            else:
                self.sentence_lengths[l] += 1
        # Add code to clean the text and split it into a list of words.
        # *Hint:* Call one of the functions you have already written!
        clean = clean_text(s)
        word_list = clean.split(' ')
        # Template for updating the words dictionary.
        for w in word_list:
            # Update self.words to reflect w
            if w not in self.words:
            # either add a new key-value pair for w
                self.words[w] = 1
            # or update the existing key-value pair.
            else:
                self.words[w] += 1
        # Add code to update other feature dictionaries.

        len_list = clean_text(s).split(' ')

        for l in len_list:
            if len(l) not in self.word_lengths:
                self.word_lengths[len(l)] = 1
            else:
                self.word_lengths[len(l)] += 1

        for i in word_list:
            if stem(i) not in self.stems:
                self.stems[stem(i)] = 1
            else:
                self.stems[stem(i)] += 1

        punc_s = ''
        for i in s:
            if i in '.!?,\'":/;{}[]()-':
                punc_s += i
        for i in punc_s:
            if i not in self.punctuation:
                self.punctuation[i] = 1
            else:
                self.punctuation[i] += 1
            
    def add_file(self, filename):
        """ adds all of the text in the file identified by filename to
            the model. It should not explicitly return a value
        """
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        text = f.read()
        self.add_string(text)

    def save_model(self):
        """ saves the TextModel object self by writing its various
            feature dictionaries to files
        """
        w = open(str(self.name) + '_' + 'words', 'w')
        wl = open(str(self.name) + '_' + 'word_lengths', 'w')
        st = open(str(self.name) + '_' + 'stems', 'w')
        sl = open(str(self.name) + '_' + 'sentence_lengths', 'w')
        punc = open(str(self.name) + '_' + 'punctuation', 'w')
        w.write(str(self.words))
        wl.write(str(self.word_lengths))
        st.write(str(self.stems))
        sl.write(str(self.sentence_lengths))
        punc.write(str(self.punctuation))
        w.close()
        wl.close()
        st.close()
        sl.close()
        punc.close()

    def read_model(self):
        """ reads the stored dictionaries for the called TextModel object
            from their files and assigns them to the attributes of the
            called TextModel
        """
        w = open(str(self.name) + '_' + 'words', 'r')
        w_str = w.read()
        w.close()
        w_dict = dict(eval(w_str))
        self.words = w_dict
        
        wl = open(str(self.name) + '_' + 'word_lengths', 'r')
        wl_str = wl.read()
        wl.close()
        wl_dict = dict(eval(wl_str))
        self.word_lengths = wl_dict

        st = open(str(self.name) + '_' + 'stems', 'r')
        st_str = st.read()
        st.close()
        st_dict = dict(eval(st_str))
        self.stems = st_dict

        sl = open(str(self.name) + '_' + 'sentence_lengths', 'r')
        sl_str = sl.read()
        sl.close()
        sl_dict = dict(eval(sl_str))
        self.sentence_lengths = sl_dict

        punc = open(str(self.name) + '_' + 'punctuation', 'r')
        punc_str = punc.read()
        punc.close()
        punc_dict = dict(eval(punc_str))
        self.punctuation = punc_dict

    def similarity_scores(self, other):
        """ computes and returns a list of log similarity scores measuring
            the similarity of self and other – one score for each type of
            feature (words, word lengths, stems, sentence lengths, and
            your additional feature)
        """
        # words
        word_score = compare_dictionaries(other.words, self.words)

        # word_lengths
        word_lengths_score = compare_dictionaries(other.word_lengths, \
                                                  self.word_lengths)

        # stems
        stems_score = compare_dictionaries(other.stems, self.stems)

        # sentence lengths
        sentence_lengths_score = compare_dictionaries(other.sentence_lengths\
                                                      , self.sentence_lengths)

        # punctuation
        punctuation_score = compare_dictionaries(other.punctuation\
                                                 , self.punctuation)

        return [word_score, word_lengths_score, stems_score, \
                sentence_lengths_score, punctuation_score]
    

    def classify(self, source1, source2):
        """ compares the called TextModel object (self) to two other
            “source” TextModel objects (source1 and source2) and
            determines which of these other TextModels is the more
            likely source of the called TextModel
        """
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)

        print('scores for ' + source1.name + ': ' + str(scores1))
        print('scores for ' + source2.name + ': ' + str(scores2))

        weighted_sum1 = 10*scores1[0] + 7*scores1[1] + 4*scores1[2] + \
                        6*scores1[3] + 7*scores1[4]
        weighted_sum2 = 10*scores2[0] + 7*scores2[1] + 4*scores2[2] + \
                        6*scores2[3] + 7*scores2[4]

        if weighted_sum1 > weighted_sum2:
            return_name = source1.name
        else:
            return_name = source2.name

        print(self.name + ' is more likely to have come from ' + \
              return_name)


def sample_file_write(filename):
    """A function that demonstrates how to write a
       Python dictionary to an easily-readable file.
    """
    d = {'test': 1, 'foo': 42}   # Create a sample dictionary.
    f = open(filename, 'w')      # Open file for writing.
    f.write(str(d))              # Writes the dictionary to the file.
    f.close()                    # Close the file.

def sample_file_read(filename):
    """A function that demonstrates how to read a
       Python dictionary from a file.
    """
    f = open(filename, 'r')    # Open for reading.
    d_str = f.read()           # Read in a string that represents a dict.
    f.close()

    d = dict(eval(d_str))      # Convert the string to a dictionary.

    print("Inside the newly-read dictionary, d, we have:")
    print(d)


def test():
    """ initial testing """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)

def run_tests():
    """ testing different text models against shakespeare and J.K. Rowling
    """
    source1 = TextModel('William Shakespeare')
    source1.add_file('shakespeare.txt')

    source2 = TextModel('J.K. Rowling')
    source2.add_file('harrypotter.txt')

    new1 = TextModel('Harry Potter and the Deathly Hallows')
    new1.add_file('harrypottertest.txt')
    new1.classify(source1, source2)
    print()

    new2 = TextModel("The Winter's Tale by Shakespeare")
    new2.add_file('shakespearetest.txt')
    new2.classify(source1, source2)
    print()

    new3 = TextModel('wr120')
    new3.add_file('test1.txt')
    new3.classify(source1, source2)
    print()

    new4 = TextModel('Moby Dick by Herman Melville')
    new4.add_file('mobydick.txt')
    new4.classify(source1, source2)
