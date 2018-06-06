from collections import deque

class links:
    def __init__(self):
        self.unvisited = deque([])
        self.visited = []
        self.base_link = 'https://www.basketball-reference.com'

    def add_link(self, link, date_string):
        if(not link in self.visited):
            self.unvisited.append([self.base_link + link, date_string])
        
    def get_next_link(self):
        link, date_string = self.unvisited.popleft()
        self.visited.append(link)
        return link, date_string

    def has_links(self):
        return len(self.unvisited)

    def print_links(self):
        print(self.unvisited)