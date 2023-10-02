# This class makes the nodes for the tree
class Node:
    def __init__(self, freq, symbol, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right
        self.bin = ''
    def __lt__(self, other):
        return self.freq < other.freq

# This function takes a list of tuples, that consists of frequency(freq) and the corresponding character (chars).
# This outputs a tree, consisting of nodes where the freq and chars are sent to the function above to make the node.
def build_huffman_tree(tuples):
    freq = []
    chars = []
    for i in tuples:
        freq.append(i[1])
        chars.append(i[0])
    nodes = [Node(freq[i], chars[i]) for i in range(len(chars))]
    while len(nodes) > 1:
        nodes.sort(key=lambda x: x.freq)
        left, right = nodes[:2]
        left.bin = '0'
        right.bin = '1'
        new_node = Node(left.freq + right.freq, left.symbol + right.symbol, left, right)
        nodes = [new_node] + nodes[2:]
    return nodes[0]

# This takes the encoded tree, and outputs each character with their corresponding binary string, or "bin"
def printout(node, val=''):
    new_val = val + node.bin
    if node.left:
        printout(node.left, new_val)
    if node.right:
        printout(node.right, new_val)
    if not node.left and not node.right:
        print(f"{node.symbol} : {new_val}")

# This is more simple
# This takes a string, or list of chars, and returns a dictionary where each character is in .keys(), 
# and their corresponding frequency is in .values().
def dict_counter(string):
    count_dict = {}
    for i in string:
        if i not in count_dict:
            count_dict[i] = 1
        else:
            count_dict[i] = count_dict[i]+1
    return count_dict

# This is also simple and just sorts the dictionary from least frequent to most frequent.
def dict_sorter(dictionary):
    sort_dict = sorted(dictionary.items(), key=lambda item:item[1])
    print(sort_dict)
    return sort_dict

# This takes in the string I want encoded and encodes it, so it is ready for the def printout() function.
# This could´ve also been called def main()
def encoder(string):
    counted_dict = dict_counter(string)
    sorted_dict = dict_sorter(counted_dict)
    return build_huffman_tree(sorted_dict)

string = "adadaddadavcvcbasgfnasbcbavscbascascasc"
printout(encoder(string))
