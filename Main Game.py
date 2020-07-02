from pygame import *
font.init()

sc = display.set_mode((800, 600))
score = 0
best_score = 0
file = open('data.txt', 'r')

display.update()
while 1:
    for even in event.get():
        if even.type == QUIT:
            exit()
        elif even.type == MOUSEBUTTONDOWN:
            score += 1

    file = open('data.txt', 'r')

    if score >= int(file.read()):
        file.close()
        file = open('data.txt', 'w')
        file.write(str(score))
        best_score = score
        file.close()
    else:
        file = open('data.txt', 'r')
        best_score = file.read()
        file.close()

    font1 = font.Font(None, 36)
    text1 = font1.render(str(score), 1, (255, 255, 255))
    font2 = font.Font(None, 36)
    text2 = font2.render(str(best_score), 1, (255, 255, 255))

    sc.fill((0, 0, 0))
    sc.blit(text1, (50, 50))
    sc.blit(text2, (50, 100))
    time.delay(17)
    display.update()
