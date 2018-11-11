from flask import Flask, request, render_template
import json

app = Flask(__name__)

class Node:
    def __init__(self, label=None, data=None):
        self.label = label
        self.data = data
        self.children = dict()
    
    def addChild(self, key, data=None):
        if not isinstance(key, Node):
            self.children[key] = Node(key, data)
        else:
            self.children[key.label] = key
    
    def __getitem__(self, key):
        return self.children[key]

class PrefixTree:
    def __init__(self):
        self.head = Node()
    
    def __getitem__(self, key):
        return self.head.children[key]
    
    def add(self, word):
        current_node = self.head
        word_finished = True
        for i in range(len(word)):
            if word[i] in current_node.children:
                current_node = current_node.children[word[i]]
            else:
                word_finished = False
                break
        if not word_finished: # создаём дочерние ноды для каждой новой буковки
            while i < len(word):
                current_node.addChild(word[i])
                current_node = current_node.children[word[i]]
                i += 1
        current_node.data = word # я решил сохранять в последней ячейке наше словцо, чтобы не бегать потом по дереву
    
    def check(self, word):
        if word == '':
            return False
        if word == None:
            raise ValueError('Trie.has_word requires a not-Null string')
        current_node = self.head
        exists = True
        for letter in word:
            if letter in current_node.children:
                current_node = current_node.children[letter]
            else:
                exists = False
                break
        if exists:
            if current_node.data == None:
                exists = False
        return exists
    
    def check_part(self, word):
        if word == '':
            return False
        if word == None:
            raise ValueError('Trie.has_word requires a not-Null string')
        current_node = self.head
        exists = True
        for letter in word:
            if letter in current_node.children:
                current_node = current_node.children[letter]
            else:
                exists = False
                break
        return exists
    
    def getTop10(self, prefix):
        prefix = prefix.lower()
        words = list()
        if prefix == None:
            raise ValueError('Requires not-Null prefix')
        top_node = self.head
        for letter in prefix:
            if letter in top_node.children:
                top_node = top_node.children[letter]
            else: # нет префикса
                return words
        if top_node == self.head:
            queue = [node for key, node in top_node.children.items()]
        else:
            queue = [top_node]
        while queue:
            current_node = queue.pop()
            if current_node.data != None: # вот тут-то нам и нужно сохраниение слова в последней ячейке
                words.append(current_node.data)
            queue = [node for key,node in current_node.children.items()] + queue
            
        nums = []
        for word in words:
            nums.append(int(word[len(word)-3:len(word)])) # рейтинг фильмов вычленяем в отдельный массив  
        for i in range(0, len(nums)): # сортируем оба массива по убыванию положения в топе
            flag = 0
            for j in range(0,len(nums)-1):
                if nums[j] > nums[j + 1]:
                    nums[j], nums[j + 1] = nums[j + 1], nums[j]
                    words[j], words[j + 1] = words[j + 1], words[j]
                    flag = 1
            if flag == 0:
                break
        result = []
        i = 0
        for word in words: # добавляем топ 10 либо все элементы (если их меньше 10)
            i += 1
            if i > 10:
                break
            result.append(words[i - 1][0:len(words[i - 1]) - 3])
        return result

def init_prefix_tree(filename, tr):
    file = open(filename, 'r')
    i = 1
    w = str()
    for volokno in file:
        w = '0'
        if i < 10:
            w += '0'
        w += str(i)
        if i > 99:
            w = str(i)
        clean_volokno = volokno.lower().replace('\xa0x', ' X').replace('ё', 'е')[:len(volokno)-1]
        clean_volokno += w
        tr.add(clean_volokno)
        i += 1

prefixtree = PrefixTree()

init_prefix_tree('top100.txt', prefixtree)

@app.route("/get_sudgest/<string>", methods=['GET', 'POST'])
def return_sudgest(string):
    list_ = prefixtree.getTop10(string)
    result = '<br><i>Топ фильмов по запросу</i> <b>' + string + '</b>:<br>'
    for item in list_:
        result += '<br>'
        result += item
    result += '<br>'
    return json.dumps(result, ensure_ascii = False)

@app.route("/")
def hello():
    return render_template("instruction.html")

if __name__ == "__main__":
    app.run()
