import pygame, pygame_gui, bcrypt, sqlite3
from pygame.locals import *
import pygame_gui.elements.ui_image
from TinyEpicZombies.constants import WIDTH, HEIGHT, CARD_HEIGHT, CARD_WIDTH
import os

def createNewUser(username, password):
    flag = True
    salt = bcrypt.gensalt()
    password = hash(password, salt)
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    SQL = "INSERT INTO Users(username, password, salt) VALUES(?,?,?)"
    try:
        cursor.execute(SQL, (username, password, salt))
        connection.commit()
    except:
        flag = False

    connection.close()
    return flag

def hash(data, salt):
    bytes = data.encode('utf-8')
    hashedData = bcrypt.hashpw(bytes, salt) 
    return hashedData

# createNewUser("Toby", "password123")

def loginUser(username, password):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    SQL = "SELECT Salt FROM Users WHERE username = ?"
    try:
        salt = cursor.execute(SQL, (username,)).fetchone() # fetches the salt associated with the username
        password = hash(password, salt[0]) # using the salt, hashes the given password and stores it back in the password variable
        SQL = "SELECT ID FROM Users WHERE username = ? and password = ?" # performs a comparison between the stored username / hashed password and the given username / hashed password.
        result = cursor.execute(SQL, (username, password)).fetchone() # executes the above
    except:
        print("Invalid username or password")
        result = None
    connection.close()
    if result: # if there is a value in result, it will be the user ID of the user associated with the entered username (and password). 
        return result[0]
    else: # if there is NOT a value in result, the password must have been incorrect.
        return -1

pygame.init()

display = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# logged out screen elements:
loggedOut = pygame_gui.UIManager((WIDTH, HEIGHT))
startLoginButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH/2 - 120, HEIGHT/2 - 20), (100, 25)), text="Login", manager=loggedOut)
startSignupButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH/2 + 20, HEIGHT/2 - 20), (100, 25)), text="Signup", manager=loggedOut)
titleLabel = pygame_gui.elements.UILabel(pygame.Rect((WIDTH/2-65, 0), (200, 60)),text="Tiny Epic Zombies", manager=loggedOut)

# logged in screen elements
login_page = pygame_gui.UIManager((WIDTH, HEIGHT))
usernameInput = pygame_gui.elements.UITextEntryLine(pygame.Rect((50, 50), (100, 30)), manager=login_page)
passwordInput = pygame_gui.elements.UITextEntryLine(pygame.Rect((50, 100), (100, 30)), manager=login_page)
loginButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 150), (100, 25)), text="Login", manager=login_page)

# signup page elements
signup_page = pygame_gui.UIManager((WIDTH, HEIGHT))
signupUsernameInput = pygame_gui.elements.UITextEntryLine(pygame.Rect((50, 50), (100, 30)), manager = signup_page)
signupPasswordInput = pygame_gui.elements.UITextEntryLine(pygame.Rect((50, 100), (100, 30)), manager = signup_page)
signupButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 150), (100, 25)), text="Signup", manager=signup_page)

# main menu elements
mainMenu = pygame_gui.UIManager((WIDTH, HEIGHT))
welcomeLabel = pygame_gui.elements.UILabel(pygame.Rect((WIDTH/2, 50), (200, 100)),text="Welcome", manager=mainMenu)
logoutButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((150, 150), (100, 25)), text="Logout", manager=mainMenu)
startGameButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WIDTH/2, HEIGHT/2), (100, 25)), text="Start Game", manager=mainMenu)

# in game menu
gameboard = pygame_gui.UIManager((WIDTH, HEIGHT))
gameboardSurf = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "woodBackground.jpg"))
centralStore = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "stores", "centralStore.jpg"))
playingArea = pygame.Rect(0,0,3*WIDTH/4, HEIGHT)
pygame_gui.elements.ui_image.UIImage(relative_rect=pygame.Rect((0, 0), (WIDTH, HEIGHT)), image_surface=gameboardSurf, manager=gameboard)
pygame_gui.elements.ui_image.UIImage(relative_rect=pygame.Rect(((WIDTH-CARD_WIDTH)/2, (HEIGHT-CARD_HEIGHT)/2), (CARD_WIDTH, CARD_HEIGHT)), image_surface=centralStore, manager=gameboard)
exitGameButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 20), (100, 25)), text="Exit game", manager=gameboard)

manager = mainMenu

run = True
while run:
    time_delta = clock.tick(30)/1000

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == loginButton: # calls the login process
                id = loginUser(usernameInput.text, passwordInput.text)
                if id > -1:
                    manager = mainMenu
            if event.ui_element == signupButton: # calls the add new user process
                createNewUser(signupUsernameInput.text, signupPasswordInput.text)
                manager = login_page
            elif event.ui_element == logoutButton: # returns to login screen
                manager = loggedOut
            elif event.ui_element == startGameButton: # proceed to game board screen
                manager = gameboard
            elif event.ui_element == exitGameButton: # exit game to main menu
                manager = mainMenu
            elif event.ui_element == startLoginButton: # proceed to login page
                manager = login_page
            elif event.ui_element == startSignupButton: # proceed to signup page
                manager = signup_page
        
        manager.process_events(event)
    
    manager.update(time_delta)

    display.fill((0, 0, 0))

#    pygame.draw.rect(display, (255, 0, 0), (100, 100, 100, 100))

    manager.draw_ui(display)

    pygame.display.update()

pygame.quit()
