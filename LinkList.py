from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        if self.head:
            new_node.next = self.head
            self.head = new_node
        else:
            self.head = new_node
            self.tail = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head:
            self.tail.next = new_node
            self.tail = new_node
        else:
            self.tail = new_node
            self.head = new_node

    def search(self, data):
        current_node = self.head
        while current_node:
            if current_node.data == data:
                return True
            current_node = current_node.next
        return False

    def printLinkedList(self):
        movies = []
        current_node = self.head
        while current_node:
            movies.append(current_node.data)
            current_node = current_node.next
        return movies

    def remove_beginning(self):
        if not self.head:
            return None
        removed_data = self.head.data
        self.head = self.head.next
        if not self.head:
            self.tail = None
        return removed_data

    def remove_at_end(self):
        if not self.head:
            return None
        if self.head == self.tail:
            removed_data = self.head.data
            self.head = None
            self.tail = None
            return removed_data
        current_node = self.head
        while current_node.next != self.tail:
            current_node = current_node.next
        removed_data = self.tail.data
        self.tail = current_node
        self.tail.next = None
        return removed_data

    def remove_at(self, data):
        if not self.head:
            return None
        if self.head.data == data:
            return self.remove_beginning()
        current_node = self.head
        while current_node.next and current_node.next.data != data:
            current_node = current_node.next
        if not current_node.next:
            return None
        removed_data = current_node.next.data
        if current_node.next == self.tail:
            self.tail = current_node
        current_node.next = current_node.next.next
        return removed_data


movie_list = LinkedList()

@app.route('/')
def home():
    return render_template('index.html', movies=movie_list.printLinkedList())

@app.route('/movies')
def movies():
    return render_template('linklistindex.html')


@app.route('/add_beginning', methods=['POST'])
def add_beginning():
    movie = request.form['movie']
    if movie_list.search(movie):
        return jsonify({"error": "This movie already exists in the list.", "movies": movie_list.printLinkedList()}), 400
    movie_list.insert_at_beginning(movie)
    return jsonify({"movies": movie_list.printLinkedList()})

@app.route('/add_end', methods=['POST'])
def add_end():
    movie = request.form['movie']
    if movie_list.search(movie):
        return jsonify({"error": "This movie already exists in the list.", "movies": movie_list.printLinkedList()}), 400
    movie_list.insert_at_end(movie)
    return jsonify({"movies": movie_list.printLinkedList()})

@app.route('/remove_beginning', methods=['POST'])
def remove_beginning():
    if not movie_list.printLinkedList():
        return jsonify({"error": "Cannot remove from beginning. The list is empty.", "movies": []}), 400
    removed = movie_list.remove_beginning()
    return jsonify({"removed": removed, "movies": movie_list.printLinkedList()})

@app.route('/remove_end', methods=['POST'])
def remove_end():
    if not movie_list.printLinkedList():
        return jsonify({"error": "Cannot remove from end. The list is empty.", "movies": []}), 400
    removed = movie_list.remove_at_end()
    return jsonify({"removed": removed, "movies": movie_list.printLinkedList()})

@app.route('/remove_movie', methods=['POST'])
def remove_movie():
    movie = request.form['movie']
    if not movie_list.search(movie):
        return jsonify({"error": "Movie not found in the list.", "movies": movie_list.printLinkedList()}), 404
    removed = movie_list.remove_at(movie)
    return jsonify({"removed": removed, "movies": movie_list.printLinkedList()})

@app.route('/search_movie', methods=['POST'])
def search_movie():
    movie = request.form['movie']
    found = movie_list.search(movie)
    return jsonify({"found": found})

if __name__ == '__main__':
    app.run(debug=True)