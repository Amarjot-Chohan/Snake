from tkinter import *
import random
from sky import sky_gif
from amar_head import amar_head_png
from bonus_icons import bonus_icons
import mysql.connector
from datetime import datetime
import webbrowser
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# width and height must be a multiple of the speed.
WIDTH = 500
HEIGHT = 400
HIGHEST_SCORE = 0
SPEED = 10
TRIES = 0

class Apple():
    def __init__(self):
        self.apple_y = (random.randint(20, HEIGHT/10)) * 10
        self.apple_x = (random.randint(20, WIDTH/10)) * 10
        # bonus will be out of view for the majority of play
        self.bonus_y = HEIGHT + 50
        self.bonus_x = WIDTH + 50

    def create_new_Apple(self):
        self.apple_y = (random.randint(20, HEIGHT/10)) * 10
        self.apple_x = (random.randint(20, WIDTH/10)) * 10
        self.create_bonus()

    def create_bonus(self):
        random_int = random.randint(1, 3)
        if random_int == 2:
            self.bonus_y = (random.randint(20, HEIGHT/10)) * 10
            self.bonus_x = (random.randint(20, WIDTH/10)) * 10
        else:
            # out of view
            self.bonus_y = HEIGHT + 50
            self.bonus_x = WIDTH + 50

class Snake():
    def __init__(self):
        self.snake_x = [10, 11, 12]
        self.snake_y = [10, 10, 10]
        self.snake_body_cords = []
        self.length = 3
        self.key = "s"
        self.direction = "s"

    def grow(self):
        self.length += 1
        self.snake_x.append(10)
        self.snake_y.append(10)

    def getKey(self, event):
        event = event.char.lower()
        if event== "w" or event == "d" or event == "s" or event == "a" or event == " ":
            self.key = event

    def move(self, speed=SPEED):
        direction = 1
        for i in range(self.length -1 , 0, -1):
            self.snake_x[i] = self.snake_x[i - 1]
            self.snake_y[i] = self.snake_y[i - 1]

        if self.key == "s":
            # if user tries to go in the opposite direction
            if self.direction =="w":
                self.key = "w"
                self.snake_y[0] -= speed * direction
            else:
                self.snake_y[0] += speed * direction
        elif self.key == "w":
            # if user tries to go in the opposite direction
            if self.direction == "s":
                self.key = "s"
                self.snake_y[0] += speed * direction
            else:
                self.snake_y[0] -= speed * direction
        elif self.key == "d":
            # if user tries to go in the opposite direction
            if self.direction == "a":
                self.key = "a"
                self.snake_x[0] -= speed * direction
            else:
                self.snake_x[0] += speed * direction
        elif self.key == "a":
            # if user tries to go in the opposite direction
            if self.direction == "d":
                self.key = "d"
                self.snake_x[0] += speed * direction
            else:
                self.snake_x[0] -= speed * direction

        self.direction = self.key


class Main_Game():
    def __init__(self, root):
        if hasattr(self, 'canvas'):
            self.canvas.destroy()
        self.username = ''
        self.score = 0
        self.root = root
        self.root.title("snake")
        self.a1 = Apple()
        self.s1 = Snake()
        self.canvas = Canvas(self.root, height=HEIGHT, width=WIDTH)
        self.username_entry = Entry(self.canvas)
        self.canvas.pack()
        self.draw_on_canvas()
        self.root.bind('<KeyPress>', self.s1.getKey)
        self.play()

    def draw_on_canvas(self):
        # x1,y1,x2,y2
        self.background = PhotoImage(data=sky_gif)
        self.canvas.create_image(0, 0, image=self.background)
        self.canvas.create_text((30,10), text=' Score '+ str(self.score), fill="white")

        # bonus items
        index = random.randint(0, 3)
        random_bonus_icoon = list(bonus_icons.values())[index]
        self.bonus = PhotoImage(data=random_bonus_icoon)
        self.canvas.create_image((self.a1.bonus_x), (self.a1.bonus_y), image=self.bonus)

        # apple and snake body
        self.img = PhotoImage(data=amar_head_png)
        self.canvas.create_image((self.a1.apple_x), (self.a1.apple_y), image=self.img)

        self.s1.snake_body_cords = []
        for i in range(self.s1.length-1, 1, -1):
            self.s1.snake_body_cords.append((self.s1.snake_x[i], self.s1.snake_y[i]))
            self.canvas.create_image((self.s1.snake_x[i]), (self.s1.snake_y[i]), image=self.img)


    def play(self):
        self.canvas.after(200, self.play)
        self.canvas.delete(ALL)
        self.draw_on_canvas()
        if not self.check_lost():
            self.s1.move()
        else:
            self.play_again()
        self.eat_apple()
        self.rebound()

    def play_again(self):
        canvas = self.canvas
        global HIGHEST_SCORE

        if self.score > HIGHEST_SCORE:
            HIGHEST_SCORE = self.score

        canvas.create_text((WIDTH / 2, HEIGHT / 2 - 100), text='GAME OVER', font=("Purisa", 42), fill="red")
        canvas.create_text((WIDTH / 2, HEIGHT / 2 - 50), text='Score : '+ str(self.score), font=("Purisa", 28), fill="red")
        canvas.create_text((WIDTH / 2, HEIGHT / 2 - 10), text='High Score : ' + str(HIGHEST_SCORE), font=("Purisa", 28),
                                fill="red")

        restart = Button(canvas, text="Try Again?", command=lambda: self.new_game())
        restart.place(x=WIDTH/2-30, y=HEIGHT/2+30)

        self.root.overrideredirect(True)
        canvas.create_text((WIDTH/2-120, HEIGHT/2+65), text='Enter name: ', font=("Purisa", 24), fill="red")
        self.username_entry.place(x=WIDTH/2-50, y=HEIGHT/2+55)

        exit = Button(canvas, text="Submit & Exit", command=lambda: self.add_to_db())
        exit.place(x=WIDTH/2-40, y=HEIGHT/2+90)

        comment = Button(canvas, text="Post comment on YouTube", command=lambda: self.comment())
        comment.place(x=WIDTH/2-70, y=HEIGHT/2+120)

        like = Button(canvas, text="Like on YouTube", command=lambda: self.like())
        like.place(x=WIDTH/2-40, y=HEIGHT/2+150)

    def new_game(self):
        self.__init__(self.root)

    def check_lost(self):
        for x,y in self.s1.snake_body_cords:
            if x == self.s1.snake_x[0]:
                if y == self.s1.snake_y[0]:
                    print(x,y)
                    print('cords', self.s1.snake_body_cords)
                    return True
        return False

    def eat_apple(self):
        if abs(self.a1.apple_x - self.s1.snake_x[0]) < 20 and abs(self.s1.snake_y[0] - self.a1.apple_y) < 25:
            self.score+=1
            self.a1.create_new_Apple()
            self.s1.grow()

        if abs(self.a1.bonus_x - self.s1.snake_x[0]) < 20 and abs(self.s1.snake_y[0] - self.a1.bonus_y) < 20:
            self.score += 10
            self.a1.create_bonus()
            self.s1.grow()

    def rebound(self):
        if self.s1.snake_x[0] == 0:
            self.s1.snake_x[0] = WIDTH
        elif self.s1.snake_x[0] == WIDTH:
            self.s1.snake_x[0] = 0
        elif self.s1.snake_y[0] == 0:
            self.s1.snake_y[0] = HEIGHT
        elif self.s1.snake_y[0] == HEIGHT:
            self.s1.snake_y[0] = 0

    def add_to_db(self):
        self.username = self.username_entry.get()
        if self.username and HIGHEST_SCORE:
            username = self.username
            try:
                db = mysql.connector.connect(
                    host="localhost",
                    user='root',
                    password='',
                    db="test",
                )
                cursor = db.cursor()

                date = datetime.today().strftime('%Y-%m-%d')
                savequery = "INSERT INTO leaderboard (Username, Score, Date) VALUES ('"\
                            + str(username) + "','" + str(HIGHEST_SCORE) + "','" + date +\
                            "')"
                try:
                    cursor.execute(savequery)
                    db.commit()
                    print("Query Excecuted successfully")
                except Exception as e:
                    db.rollback()
                    print("Error occured", e)
            except Exception as e:
                print("Could not connect to the database", e)

        webbrowser.open_new(r"https://a7528625f8f6.ngrok.io/snake/snake.php")

    def connect_to_youtube(self):
        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"
        scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        return youtube

    def like(self):
        youtube = self.connect_to_youtube()
        youtube.videos().rate(rating='like', id='m5s_dgkZvq8')

    def comment(self):
        youtube = self.connect_to_youtube()
        channel_id = 'UC0bh3ylMOUYA6Xwcb8S9dxA'
        video_id = 'm5s_dgkZvq8'
        text = "I (", self.username, ") disappointed myself and Amarjot scoring just ,", HIGHEST_SCORE
        insert_result = youtube.commentThreads().insert(
            part="snippet",
            body=dict(
                snippet=dict(
                    channelId=channel_id,
                    videoId=video_id,
                    topLevelComment=dict(
                        snippet=dict(
                            textOriginal=text)
                    )
                )
            )
        ).execute()

        comment = insert_result["snippet"]["topLevelComment"]
        author = comment["snippet"]["authorDisplayName"]
        text = comment["snippet"]["textDisplay"]
        print("Inserted comment for %s: %s" % (author, text))

root = Tk()
m1 = Main_Game(root)
root.mainloop()
