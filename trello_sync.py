from trello import TrelloClient
import asyncio
from joplin_api import JoplinApiSync

# Consts
JOPLIN_TOKEN = ''
TRELLO_API_KEY = ''
TRELLO_API_SECRET = ''
TRELLO_TOKEN = ''
TRELLO_TOKEN_SECRET = ''

TRELLO_BOARD_ID = 'xxx'
JOPLIN_TMP_NOTEBOOK = 'XX_TRELLO'

joplin = JoplinApiSync(token=JOPLIN_TOKEN)

client = TrelloClient(
    api_key=TRELLO_API_KEY,
    api_secret=TRELLO_API_SECRET,
    token=TRELLO_TOKEN,
    token_secret=TRELLO_TOKEN_SECRET
)


def create_notebook(title, parent_id=None):
    if parent_id:
        res = joplin.create_folder(folder=title, parent_id=parent_id)
    else:
        res = joplin.create_folder(folder=title)
    
    return res.json()['id']
    
def new_note(notebook_id, data):
    #kwargs = {'tags': 'tag1, tag2'}
    joplin.create_note(title=data['name'], body=data['body'], parent_id=notebook_id, tags=data['tags'])


def get_my_board():
    all_boards = client.list_boards()
    index = 0
    for i in all_boards:
        if TRELLO_BOARD_ID in i.url:
                break
        index += 1
    board = all_boards[index]
    print(board.name)
    return board

def main():
    root_folder = create_notebook(JOPLIN_TMP_NOTEBOOK)
    board = get_my_board()

    lists = board.list_lists()
    for my_list in lists:
        notebook_id = create_notebook(my_list.name, root_folder)
        for card in my_list.list_cards():
            print(card.name)

            body = "# %s \n\n[link](%s) \n \n  %s  \n \n" % (card.name, card.url, card.description)
            
            for attach in card.attachments:
                body += "\n<img src='%s' width=400px/>\n" % attach["url"]
            
            labels = ['trello', 'Travel', my_list.name]
            if card.labels:
                for label in card.labels:
                    labels.append(label.name)
                
            data = {
                "body": body,
                "name": card.name,
                "tags": ",".join(labels)
            }
            
            
            new_note(notebook_id, data)

if __name__ == '__main__':
    main()
