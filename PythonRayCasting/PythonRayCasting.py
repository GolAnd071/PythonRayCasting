import pygame
import math

x, y, z, a, v, vv = 2000, 2000, 500, 0, 25, 0
wp, ap, sp, dp = False, False, False, False
mp, scoped, scoped2 = [False, False, False], False, False
fov = 60

screenHeight = 480
screenWidth = 640
screenDistance = screenWidth / 2 / math.tan(math.radians(fov / 2))
screenAngle = fov / screenWidth
screenCenter = screenHeight // 2
mapHeight = 16
mapWidth = 16
mapSize = 1000
mapRange = 16 * mapSize

pygame.init()

FPS = 60
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
map = ""
map += "################"
map += "#              #"
map += "#              #"
map += "#  ##          #"
map += "#  ##          #"
map += "#  #####       #"
map += "#  #####       #"
map += "#  #  #        #"
map += "#  # ##        #"
map += "#              #"
map += "#       ###    #"
map += "#       ###    #"
map += "#       ###    #"
map += "#              #"
map += "#              #"
map += "################"


def horizontalIntersection(inta):
    if math.sin(math.radians(inta)) == 0:
        return 1000000
    if math.sin(math.radians(inta)) > 0:
        inty = (y // mapSize) * mapSize - 1
        dy = -mapSize
    else:
        inty = (y // mapSize + 1) * mapSize
        dy = mapSize
    intx = int(x + (y - inty) / math.tan(math.radians(inta)))
    dx = -dy / math.tan(math.radians(inta))
    intx_, inty_ = int(intx) // mapSize, int(inty) // mapSize
    if intx_ < 0 or inty_ < 0 or intx_ >= mapWidth or inty_ >= mapHeight:
        return 1000000
    while map[intx_ + inty_ * mapWidth] != '#':
        intx += dx
        inty += dy
        intx_, inty_ = int(intx) // mapSize, int(inty) // mapSize
        if intx_ < 0 or inty_ < 0 or intx_ >= mapWidth or inty_ >= mapHeight:
            return 1000000
    return math.sqrt((intx - x) ** 2 + (inty - y) ** 2)


def verticalIntersection(inta):
    if math.cos(math.radians(inta)) == 0:
        return 1000000
    if math.cos(math.radians(inta)) > 0:
        intx = (x // mapSize + 1) * mapSize
        dx = mapSize
    else:
        intx = (x // mapSize) * mapSize - 1 
        dx = -mapSize
    inty = int(y + (x - intx) * math.tan(math.radians(inta)))
    dy = -dx * math.tan(math.radians(inta))
    intx_, inty_ = int(intx) // mapSize, int(inty) // mapSize
    if intx_ < 0 or inty_ < 0 or intx_ >= mapWidth or inty_ >= mapHeight:
        return 1000000
    while map[intx_ + inty_ * mapWidth] != '#':
        intx += dx
        inty += dy
        intx_, inty_ = int(intx) // mapSize, int(inty) // mapSize
        if intx_ < 0 or inty_ < 0 or intx_ >= mapWidth or inty_ >= mapHeight:
            return 1000000
    return math.sqrt((intx - x) ** 2 + (inty - y) ** 2)


def drawMap(surf):
    for i in range(mapWidth):
        for j in range(mapHeight):
            if map[i + j * mapWidth] == '#':
                pygame.draw.rect(surf, (255, 255, 255), (i * 8, j * 8, 8, 8))
            else:
                pygame.draw.rect(surf, (0, 0, 0), (i * 8, j * 8, 8, 8))
    pygame.draw.rect(surf, (255, 0, 0), (int(x) // (mapSize / 8), int(y) // (mapSize / 8), 2, 2))


def updateScreen(surf):
    intAngle = a - fov / 2
    surf.fill((0, 0, 0))
    for j in range(screenCenter):
        ceil = (mapSize - z) * screenDistance / abs(j - screenCenter)
        pygame.draw.line(
            surf,
            (
                max(0, int(250 * (1 - 1 / mapRange * ceil))),
                max(0, int(250 * (1 - 1 / mapRange * ceil))),
                max(0, int(250 * (1 - 1 / mapRange * ceil))),
            ),
            (0, j),
            (screenWidth, j)
        )
    for j in range(screenCenter + 1, screenHeight):
        floor = z * screenDistance / abs(j - screenCenter)
        pygame.draw.line(
            surf,
            (
                max(0, int(250 * (1 - 1 / mapRange * floor))),
                0,
                0,
            ),
            (0, j),
            (screenWidth, j)
        )
    for i in range(screenWidth):
        hIntersection = horizontalIntersection(intAngle)
        vIntersection = verticalIntersection(intAngle)
        dist = min(hIntersection, vIntersection) * math.cos(math.radians(intAngle - a))
        heig = mapSize / dist * screenDistance
        pygame.draw.line(
            surf,
            (
                0,
                0,
                max(0, int(250 * (1 - 1 / mapRange * dist))),
            ),
            (screenWidth - i - 1, max(0, 2 * screenCenter - heig) / 2),
            (screenWidth - i - 1, min(screenHeight * 2, 2 * screenCenter + heig) / 2)
        )
        intAngle += screenAngle 
    drawMap(surf)
    pygame.draw.line(surf, (0, 255, 0), (screenWidth // 2, screenHeight // 2 - 5), (screenWidth // 2, screenHeight // 2 + 5))
    pygame.draw.line(surf, (0, 255, 0), (screenWidth // 2 - 5, screenHeight // 2), (screenWidth // 2 + 5, screenHeight // 2))


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    updateScreen(screen)
    pygame.mouse.set_pos([screenWidth // 2, screenHeight // 2])
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                wp = True
            if event.key == pygame.K_s:
                sp = True
            if event.key == pygame.K_a:
                ap = True
            if event.key == pygame.K_d:
                dp = True
            if event.key == pygame.K_LCTRL:
                z = 200
                screenCenter -= screenHeight // 10
            if event.key == pygame.K_SPACE:
                if vv == 0:
                    vv = 10
            if event.key == pygame.K_ESCAPE:
                finished = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                wp = False
            if event.key == pygame.K_s:
                sp = False
            if event.key == pygame.K_a:
                ap = False
            if event.key == pygame.K_d:
                dp = False
            if event.key == pygame.K_LCTRL:
                z = 500
                screenCenter += screenHeight // 10
        if event.type == pygame.MOUSEBUTTONDOWN:
            mp = pygame.mouse.get_pressed(3)
            if mp[2] == True and scoped == True:
                scoped = False
                scoped2 = True
            elif mp[2] == True and scoped2 == True:
                scoped2 = False
            elif mp[2] == True:
                scoped = True
            if mp[0] == True:
                scoped = False
                scoped2 = False
    if wp:
        x += v * math.cos(math.radians(a))
        y -= v * math.sin(math.radians(a))
    if sp:
        x -= v * math.cos(math.radians(a))
        y += v * math.sin(math.radians(a))
    if ap:
        x -= v * math.sin(math.radians(a))
        y -= v * math.cos(math.radians(a))
    if dp:
        x += v * math.sin(math.radians(a))
        y += v * math.cos(math.radians(a))
    if scoped == True:
        pygame.draw.circle(screen, (0, 0, 0), (screenWidth // 2, screenHeight // 2), 450, width = 300)
        pygame.draw.line(screen, (0, 0, 0), (0, screenHeight // 2), (screenWidth, screenHeight // 2))
        pygame.draw.line(screen, (0, 0, 0), (screenWidth // 2, 0), (screenWidth // 2, screenHeight))
        fov = 30
        screenDistance = screenWidth / 2 / math.tan(math.radians(fov / 2))
        screenAngle = fov / screenWidth
    elif scoped2 == True:
        pygame.draw.circle(screen, (0, 0, 0), (screenWidth // 2, screenHeight // 2), 450, width = 300)
        pygame.draw.line(screen, (0, 0, 0), (0, screenHeight // 2), (screenWidth, screenHeight // 2))
        pygame.draw.line(screen, (0, 0, 0), (screenWidth // 2, 0), (screenWidth // 2, screenHeight))
        fov = 10
        screenDistance = screenWidth / 2 / math.tan(math.radians(fov / 2))
        screenAngle = fov / screenWidth
    else:
        fov = 60
        screenDistance = screenWidth / 2 / math.tan(math.radians(fov / 2))
        screenAngle = fov / screenWidth
    z = min(z + vv * 5, mapSize)
    if z > 500:
        vv -= 2
    if z < 500:
        z = 500
        screenCenter -= 10 * vv - 2
        vv = 0
    rel = pygame.mouse.get_pos()
    a -= rel[0] - screenWidth // 2
    screenCenter = max(min(screenHeight - 1, screenCenter - 5 * (-vv + rel[1] - screenHeight // 2)), 0)
    pygame.display.update()

pygame.quit()
