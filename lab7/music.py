import pygame
import os

pygame.init()
pygame.mixer.init()

music_folder = r"C:\Users\omega\Desktop\lab2\lab7\musics"
playlist = [os.path.join(music_folder, song) for song in os.listdir(music_folder) if song.endswith(".mp3")]


screen = pygame.display.set_mode((1000, 670))
pygame.display.set_caption("My Music Player")
clock = pygame.time.Clock()


background = pygame.image.load(os.path.join("music-eelements", "background.jpg"))
font = pygame.font.Font(None, 36)


playb = pygame.image.load(os.path.join("music-eelements", "play.png"))
pauseb = pygame.image.load(os.path.join("music-eelements", "pause.png"))
nextb = pygame.image.load(os.path.join("music-eelements", "next.png"))
prevb = pygame.image.load(os.path.join("music-eelements", "back.png"))

index = 0
aplay = False
pygame.mixer.music.load(playlist[index])
pygame.mixer.music.play()
aplay = True


running = True
while running:
    screen.blit(background, (0, 0))  

    
    bg = pygame.Surface((500, 200))
    bg.fill((255, 255, 255))
    screen.blit(bg, (155, 500))
    text = font.render(os.path.basename(playlist[index]), True, (20, 50, 50))
    screen.blit(text, (365, 520))

    
    playb_resized = pygame.transform.scale(playb, (70, 70))
    pauseb_resized = pygame.transform.scale(pauseb, (70, 70))
    nextb_resized = pygame.transform.scale(nextb, (70, 70))
    prevb_resized = pygame.transform.scale(prevb, (75, 75))

    if aplay:
        screen.blit(pauseb_resized, (370, 590))
    else:
        screen.blit(playb_resized, (370, 590))

    screen.blit(nextb_resized, (460, 587))
    screen.blit(prevb_resized, (273, 585))

    pygame.display.flip()

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  
                if aplay:
                    pygame.mixer.music.pause()
                    aplay = False
                else:
                    pygame.mixer.music.unpause()
                    aplay = True
            elif event.key == pygame.K_RIGHT:  
                index = (index + 1) % len(playlist)
                pygame.mixer.music.load(playlist[index])
                pygame.mixer.music.play()
                aplay = True
            elif event.key == pygame.K_LEFT:  
                index = (index - 1) % len(playlist)
                pygame.mixer.music.load(playlist[index])
                pygame.mixer.music.play()
                aplay = True

pygame.quit()