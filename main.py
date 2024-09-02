import requests
from collections import deque
from colorama import Fore

def get_article_neighbors(article):
    url = f"https://en.wikipedia.org/w/api.php?action=parse&page={article}&format=json&prop=links"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error: code {response.status_code}")
        exit(-1)

    data = response.json()
    if 'error' in data:
        print(f"Error: {data['error']['code']}. {data['error']['info']}")
        exit(-1)
    
    neighbors = []

    links = data['parse']['links']
    for link in links:
        if link['ns'] == 0 and 'exists' in link:
            neighbors.append(link['*'])
    
    return neighbors

def get_article_from_user(prompt):
    while True:
        article = input(prompt)

        url = f"https://en.wikipedia.org/w/api.php?action=parse&page={article}&format=json&prop=links"
        response = requests.get(url)

        if response.status_code != 200 or 'error' in response.json():
            print("invalid article")
            continue
        return article

def get_endpoint_articles():
    
    start_article = get_article_from_user(prompt=f"{Fore.WHITE}Enter {Fore.GREEN}starting {Fore.WHITE}article name: ")
    end_article = get_article_from_user(prompt=f"{Fore.WHITE}Enter {Fore.RED}ending {Fore.WHITE}article name: ")

    return start_article, end_article


def get_path(predecessors, final_article):
    path = [final_article]
    while predecessors[final_article] != None:
        final_article = predecessors[final_article]
        path.append(final_article)
    path.reverse()
    return path

def bfs_wiki_game_solver(starting_article, ending_article):
    queue = deque([starting_article])

    predecessors = {starting_article: None}

    while queue:
        current_article = queue.popleft()

        if current_article.lower() == ending_article.lower():
            path = get_path(predecessors, ending_article)
            return path
        
        neighbors = get_article_neighbors(current_article)
        for neighbor in neighbors:
            if neighbor not in predecessors:
                predecessors[neighbor] = current_article
                queue.append(neighbor)

    return None



def main():

    print('\n') # add white space
    start_article, end_article = get_endpoint_articles()
    
    path = bfs_wiki_game_solver(start_article, end_article)

    if path:
        path[0] = Fore.GREEN + path[0] + Fore.WHITE
        path[-1] = Fore.RED + path[-1] + Fore.WHITE

        print(f"{Fore.WHITE}the shortest path is: " + " -> ".join(path))
    else:
        print(f"{Fore.RED}no path found{Fore.WHITE}")

    print('\n') # add white space


if __name__ == "__main__":
    main()