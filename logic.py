import requests
import json
import pygame
import resourcegame

API_BASE_URL = "https://app.volsu.ru/maze"
session = requests.Session()

DIALOG_WIDTH = 400
DIALOG_HEIGHT = 200
DIALOG_COLOR = (240, 240, 240)
TEXT_COLOR = (0, 0, 0)
BUTTON_COLOR = (180, 180, 180)


def coord_coeff():
    coord_coeff = [
        [(-1, -1), (0, -1), (1, -1)],
        [(-1, 0), (0, 0), (1, 0)],
        [(-1, 1), (0, 1), (1, 1)],
    ]
    return coord_coeff


def init_coord(coords):
    if reset_game() == False:
        raise Exception("Ошибка соединения")
    response = session.get(f"{API_BASE_URL}/player/look")
    if response.status_code == 200:
        data = json.loads(response.text)
        coeff_cord = coord_coeff()

        for y in range(3):
            for x in range(3):
                coords[coeff_cord[y][x]] = data[y * 3 + x]
    else:
        print(f"Ошибка запроса {response.status_code}")


def reset_game():
    response = session.delete(f"{API_BASE_URL}/player/dead")
    if response.status_code == 200:
        return True
    else:
        return False


def move_up(player_coord, coords, screen):
    current_cell = player_coord
    next_cell = (current_cell[0], current_cell[1] - 1)

    if coords.get(next_cell) != None:
        code_cell = coords.get(next_cell)

        if code_cell == 0:
            response = session.post(f"{API_BASE_URL}/player/move/up")
            if response.status_code == 200:
                player_coord[1] -= 1
                data = json.loads(response.text)

                coords[(player_coord[0] - 1, player_coord[1] - 1)] = data[0]
                coords[(player_coord[0], player_coord[1] - 1)] = data[1]
                coords[(player_coord[0] + 1, player_coord[1] - 1)] = data[2]
            else:
                print(response.text)
        # door
        if 10 <= code_cell <= 99:
            key = show_dialog(screen, "Введите ключ")
            door_response = session.post(f"{API_BASE_URL}/player/move/up?key={key}")
            if door_response.status_code == 200:
                print(door_response.text)
                player_coord[1] -= 1
                data = json.loads(door_response.text)

                coords[(player_coord[0] - 1, player_coord[1] - 1)] = data[0]
                coords[(player_coord[0], player_coord[1] - 1)] = data[1]
                coords[(player_coord[0] + 1, player_coord[1] - 1)] = data[2]
                show_dialog(screen, "Успешно пройдена дверь")
            else:
                show_dialog(screen, door_response.text)
        # teleport
        elif 100 <= code_cell <= 999:
            key_response = session.post(f"{API_BASE_URL}/player/move/up?teleport=true")
            if key_response.status_code == 200:
                teleport(player_coord, coords)
                coeff_coord = coord_coeff()
                data = json.loads(key_response.text)
                for y in range(3):
                    for x in range(3):
                        coords[coeff_coord[y][x]] = data[y * 3 + x]
        # key
        elif code_cell >= 1000:
            key_info = session.get(f"{API_BASE_URL}/info/block/{code_cell}")
            isWalk = False
            key_data = json.loads(key_info.text)
            if isinstance(key_data, dict) and "params" in key_data:
                if "walkable" in key_data["params"]:
                    isWalk = True

            isFinish = False
            if isinstance(key_data, dict) and "description" in key_data:
                if "(финиш)" in key_data["description"]:
                    isFinish = True
            if key_info.status_code == 200:
                answer = show_dialog(screen, f"\n{key_info.text}")
                print(key_info.text)
                if len(answer) > 0:
                    key_response = session.post(
                        f"{API_BASE_URL}/player/move/up?answer={answer}"
                    )
                    if key_response.status_code == 200:
                        data_answer = json.loads(key_response.text)
                        print(key_response.text)
                        if isinstance(data_answer, dict) and "reward" in data_answer:
                            show_dialog(screen, "Ответ : " + data_answer["reward"])
                            print(data_answer["reward"])
                    else:
                        show_dialog(screen, "Вы начинаете заново")
                        return

                if isWalk == True or isFinish == True:
                    move_response = session.post(f"{API_BASE_URL}/player/move/up")
                    data = json.loads(move_response.text)

                    if isFinish == True:
                        resourcegame.Finish = True
                        print(data)
                        show_dialog(screen, data["message"])
                        return

                    player_coord[1] -= 1

                    coords[(player_coord[0] - 1, player_coord[1] - 1)] = data[0]
                    coords[(player_coord[0], player_coord[1] - 1)] = data[1]
                    coords[(player_coord[0] + 1, player_coord[1] - 1)] = data[2]


def move_down(player_coord, coords, screen):
    current_cell = player_coord
    next_cell = (current_cell[0], current_cell[1] + 1)

    if coords.get(next_cell) != None:
        code_cell = coords.get(next_cell)

        if code_cell == 0:
            response = session.post(f"{API_BASE_URL}/player/move/down")
            if response.status_code == 200:
                player_coord[1] += 1
                data = json.loads(response.text)

                coords[(player_coord[0] - 1, player_coord[1] + 1)] = data[6]
                coords[(player_coord[0], player_coord[1] + 1)] = data[7]
                coords[(player_coord[0] + 1, player_coord[1] + 1)] = data[8]
            else:
                print(response.text)
        # door
        if 10 <= code_cell <= 99:
            key = show_dialog(screen, "Введите ключ")
            door_response = session.post(f"{API_BASE_URL}/player/move/down?key={key}")
            if door_response.status_code == 200:
                print(door_response.text)
                player_coord[1] += 1
                data = json.loads(door_response.text)

                coords[(player_coord[0] - 1, player_coord[1] + 1)] = data[6]
                coords[(player_coord[0], player_coord[1] + 1)] = data[7]
                coords[(player_coord[0] + 1, player_coord[1] + 1)] = data[8]
                show_dialog(screen, "Успешно пройдена дверь")
            else:
                show_dialog(screen, door_response.text)
        # teleport
        elif 100 <= code_cell <= 999:
            key_response = session.post(
                f"{API_BASE_URL}/player/move/down?teleport=true"
            )
            if key_response.status_code == 200:
                teleport(player_coord, coords)
                coeff_coord = coord_coeff()
                data = json.loads(key_response.text)
                for y in range(3):
                    for x in range(3):
                        coords[coeff_coord[y][x]] = data[y * 3 + x]
        # key
        elif code_cell >= 1000:
            key_info = session.get(f"{API_BASE_URL}/info/block/{code_cell}")

            isWalk = False
            key_data = json.loads(key_info.text)
            if isinstance(key_data, dict) and "params" in key_data:
                if "walkable" in key_data["params"]:
                    isWalk = True

            isFinish = False
            if isinstance(key_data, dict) and "description" in key_data:
                if "(финиш)" in key_data["description"]:
                    isFinish = True
            if key_info.status_code == 200:
                answer = show_dialog(screen, f"\n{key_info.text}")
                print(key_info.text)
                if len(answer) > 0:
                    key_response = session.post(
                        f"{API_BASE_URL}/player/move/down?answer={answer}"
                    )
                    if key_response.status_code == 200:
                        data_answer = json.loads(key_response.text)
                        print(key_response.text)
                        if isinstance(data_answer, dict) and "reward" in data_answer:
                            show_dialog(screen, "Ответ : " + data_answer["reward"])
                            print(data_answer["reward"])
                    else:
                        show_dialog(screen, "Вы начинаете заново")
                        return

                if isWalk == True or isFinish == True:
                    move_response = session.post(f"{API_BASE_URL}/player/move/down")
                    data = json.loads(move_response.text)

                    if isFinish == True:
                        resourcegame.Finish = True
                        print(data)
                        show_dialog(screen, data["message"])
                        return

                    player_coord[1] += 1

                    coords[(player_coord[0] - 1, player_coord[1] + 1)] = data[6]
                    coords[(player_coord[0], player_coord[1] + 1)] = data[7]
                    coords[(player_coord[0] + 1, player_coord[1] + 1)] = data[8]


def move_left(player_coord, coords, screen):
    current_cell = player_coord
    next_cell = (current_cell[0] - 1, current_cell[1])

    if coords.get(next_cell) != None:
        code_cell = coords.get(next_cell)

        if code_cell == 0:
            response = session.post(f"{API_BASE_URL}/player/move/left")
            if response.status_code == 200:
                player_coord[0] -= 1
                data = json.loads(response.text)

                coords[(player_coord[0] - 1, player_coord[1] - 1)] = data[0]
                coords[(player_coord[0] - 1, player_coord[1])] = data[3]
                coords[(player_coord[0] - 1, player_coord[1] + 1)] = data[6]
            else:
                print(response.text)
        # door
        if 10 <= code_cell <= 99:
            key = show_dialog(screen, "Введите ключ")
            door_response = session.post(f"{API_BASE_URL}/player/move/left?key={key}")
            if door_response.status_code == 200:
                print(door_response.text)
                player_coord[0] -= 1
                data = json.loads(door_response.text)

                coords[(player_coord[0] - 1, player_coord[1] - 1)] = data[0]
                coords[(player_coord[0] - 1, player_coord[1])] = data[3]
                coords[(player_coord[0] - 1, player_coord[1] + 1)] = data[6]
                show_dialog(screen, "Успешно пройдена дверь")
            else:
                show_dialog(screen, door_response.text)
        # teleport
        elif 100 <= code_cell <= 999:
            key_response = session.post(
                f"{API_BASE_URL}/player/move/left?teleport=true"
            )
            if key_response.status_code == 200:
                teleport(player_coord, coords)
                coeff_coord = coord_coeff()
                data = json.loads(key_response.text)
                for y in range(3):
                    for x in range(3):
                        coords[coeff_coord[y][x]] = data[y * 3 + x]
        # key
        elif code_cell >= 1000:
            key_info = session.get(f"{API_BASE_URL}/info/block/{code_cell}")
            isWalk = False
            key_data = json.loads(key_info.text)
            if isinstance(key_data, dict) and "params" in key_data:
                if "walkable" in key_data["params"]:
                    isWalk = True

            isFinish = False
            if isinstance(key_data, dict) and "description" in key_data:
                if "(финиш)" in key_data["description"]:
                    isFinish = True

            if key_info.status_code == 200:
                answer = show_dialog(screen, f"\n{key_info.text}")
                print(key_info.text)
                if len(answer) > 0:
                    key_response = session.post(
                        f"{API_BASE_URL}/player/move/left?answer={answer}"
                    )
                    if key_response.status_code == 200:
                        print(key_response.text)
                        data_answer = json.loads(key_response.text)

                        if isinstance(data_answer, dict) and "reward" in data_answer:
                            show_dialog(screen, "Ответ : " + data_answer["reward"])
                            print(data_answer["reward"])
                    else:
                        show_dialog(screen, "Вы начинаете заново")
                        return
                if isWalk == True or isFinish == True:
                    move_response = session.post(f"{API_BASE_URL}/player/move/left")
                    data = json.loads(move_response.text)

                    if isFinish == True:
                        resourcegame.Finish = True
                        print(data)
                        show_dialog(screen, data["message"])
                        return

                    player_coord[0] -= 1

                    coords[(player_coord[0] - 1, player_coord[1] - 1)] = data[0]
                    coords[(player_coord[0] - 1, player_coord[1])] = data[3]
                    coords[(player_coord[0] - 1, player_coord[1] + 1)] = data[6]


def move_right(player_coord, coords, screen):
    current_cell = player_coord
    next_cell = (current_cell[0] + 1, current_cell[1])

    if coords.get(next_cell) != None:
        code_cell = coords.get(next_cell)

        if code_cell == 0:
            response = session.post(f"{API_BASE_URL}/player/move/right")
            if response.status_code == 200:
                player_coord[0] += 1
                data = json.loads(response.text)

                coords[(player_coord[0] + 1, player_coord[1] - 1)] = data[2]
                coords[(player_coord[0] + 1, player_coord[1])] = data[5]
                coords[(player_coord[0] + 1, player_coord[1] + 1)] = data[8]
            else:
                print(response.text)
        # door
        if 10 <= code_cell <= 99:
            key = show_dialog(screen, "Введите ключ")
            door_response = session.post(f"{API_BASE_URL}/player/move/right?key={key}")
            if door_response.status_code == 200:
                print(door_response.text)
                player_coord[0] += 1
                data = json.loads(door_response.text)

                coords[(player_coord[0] + 1, player_coord[1] - 1)] = data[2]
                coords[(player_coord[0] + 1, player_coord[1])] = data[5]
                coords[(player_coord[0] + 1, player_coord[1] + 1)] = data[8]
                show_dialog(screen, "Успешно пройдена дверь")
            else:
                show_dialog(screen, door_response.text)
        # teleport
        elif 100 <= code_cell <= 999:
            key_response = session.post(
                f"{API_BASE_URL}/player/move/right?teleport=true"
            )
            if key_response.status_code == 200:
                teleport(player_coord, coords)
                coeff_coord = coord_coeff()
                data = json.loads(key_response.text)
                for y in range(3):
                    for x in range(3):
                        coords[coeff_coord[y][x]] = data[y * 3 + x]
        # key
        elif code_cell >= 1000:
            key_info = session.get(f"{API_BASE_URL}/info/block/{code_cell}")
            isWalk = False
            key_data = json.loads(key_info.text)
            if isinstance(key_data, dict) and "params" in key_data:
                if "walkable" in key_data["params"]:
                    isWalk = True

            isFinish = False
            if isinstance(key_data, dict) and "description" in key_data:
                if "(финиш)" in key_data["description"]:
                    isFinish = True

            print(key_data)

            if key_info.status_code == 200:
                answer = show_dialog(screen, f"\n{key_info.text}")
                print(key_info.text)
                if len(answer) > 0:
                    key_response = session.post(
                        f"{API_BASE_URL}/player/move/right?answer={answer}"
                    )
                    if key_response.status_code == 200:
                        data_answer = json.loads(key_response.text)
                        if isinstance(data_answer, dict) and "reward" in data_answer:
                            show_dialog(screen, "Ответ : " + data_answer["reward"])
                            print(data_answer["reward"])
                    else:
                        show_dialog(screen, "Вы начинаете заново")
                        return

                if isWalk == True or isFinish == True:
                    move_response = session.post(f"{API_BASE_URL}/player/move/right")
                    data = json.loads(move_response.text)

                    if isFinish == True:
                        resourcegame.Finish = True
                        print(data)
                        show_dialog(screen, data["message"])
                        return

                    player_coord[0] += 1

                    coords[(player_coord[0] + 1, player_coord[1] - 1)] = data[2]
                    coords[(player_coord[0] + 1, player_coord[1])] = data[5]
                    coords[(player_coord[0] + 1, player_coord[1] + 1)] = data[8]


def teleport(player_coord, coords):
    player_coord[0] = 0
    player_coord[1] = 0
    coords.clear()


def show_dialog(screen, message, default_text=""):
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 24)
    input_font = pygame.font.SysFont("Arial", 22)
    button_font = pygame.font.SysFont("Arial", 20, bold=True)

    # Параметры окна
    DIALOG_WIDTH = min(500, screen.get_width() - 40)
    DIALOG_HEIGHT = 300
    BORDER_RADIUS = 12
    SHADOW_OFFSET = 5
    ANIMATION_SPEED = 15

    # Цветовая схема
    COLORS = {
        "background": (240, 240, 245),
        "shadow": (0, 0, 0, 50),
        "title_bar": (70, 130, 180),
        "button": (100, 180, 100),
        "button_hover": (120, 200, 120),
        "input": (255, 255, 255),
        "input_border": (200, 200, 200),
        "text": (50, 50, 50),
        "text_light": (120, 120, 120),
    }

    # Разбиваем текст на строки
    def wrap_text(text, font, max_width):
        words = text.split(" ")
        lines = []
        current_line = []

        for word in words:
            test_line = " ".join(current_line + [word])
            width = font.size(test_line)[0]
            if width <= max_width:
                current_line.append(word)
            else:
                lines.append(" ".join(current_line))
                current_line = [word]

        lines.append(" ".join(current_line))
        return lines

    wrapped_text = wrap_text(message, font, DIALOG_WIDTH - 60)
    text_surfaces = [font.render(line, True, COLORS["text"]) for line in wrapped_text]

    # Параметры элементов
    dialog_rect = pygame.Rect(
        (screen.get_width() - DIALOG_WIDTH) // 2,
        (screen.get_height() - DIALOG_HEIGHT) // 2,
        DIALOG_WIDTH,
        DIALOG_HEIGHT,
    )

    input_rect = pygame.Rect(
        dialog_rect.x + 30, dialog_rect.y + DIALOG_HEIGHT - 90, DIALOG_WIDTH - 60, 40
    )

    button_rect = pygame.Rect(
        dialog_rect.x + DIALOG_WIDTH - 130, dialog_rect.y + DIALOG_HEIGHT - 40, 100, 35
    )

    # Анимация
    alpha_surface = pygame.Surface(
        (DIALOG_WIDTH + SHADOW_OFFSET * 2, DIALOG_HEIGHT + SHADOW_OFFSET * 2),
        pygame.SRCALPHA,
    )
    current_alpha = 0
    input_text = default_text
    input_active = False
    button_hover = False

    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(60) / 1000.0

        # Анимация появления
        if current_alpha < 200:
            current_alpha = min(200, current_alpha + ANIMATION_SPEED)
            alpha_surface.set_alpha(current_alpha)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    running = False
                elif input_rect.collidepoint(event.pos):
                    input_active = True
                else:
                    input_active = False

            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        running = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

        # Проверка наведения на кнопку
        mouse_pos = pygame.mouse.get_pos()
        button_hover = button_rect.collidepoint(mouse_pos)

        # Затемнение фона
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        # Тень
        shadow_rect = dialog_rect.move(SHADOW_OFFSET, SHADOW_OFFSET)
        pygame.draw.rect(
            alpha_surface,
            COLORS["shadow"],
            (0, 0, DIALOG_WIDTH + SHADOW_OFFSET * 2, DIALOG_HEIGHT + SHADOW_OFFSET * 2),
            border_radius=BORDER_RADIUS,
        )
        screen.blit(alpha_surface, shadow_rect)

        # Основное окно
        pygame.draw.rect(
            screen, COLORS["background"], dialog_rect, border_radius=BORDER_RADIUS
        )
        pygame.draw.rect(
            screen,
            COLORS["title_bar"],
            (dialog_rect.x, dialog_rect.y, DIALOG_WIDTH, 40),
            border_top_left_radius=BORDER_RADIUS,
            border_top_right_radius=BORDER_RADIUS,
        )

        # Заголовок
        title = font.render("Внимание", True, (255, 255, 255))
        screen.blit(title, (dialog_rect.x + 20, dialog_rect.y + 10))

        # Текст сообщения
        for i, text_surface in enumerate(text_surfaces):
            screen.blit(text_surface, (dialog_rect.x + 30, dialog_rect.y + 60 + i * 30))

        # Поле ввода
        pygame.draw.rect(screen, COLORS["input"], input_rect, border_radius=6)
        pygame.draw.rect(
            screen,
            COLORS["input_border"] if not input_active else (100, 180, 255),
            input_rect,
            2,
            border_radius=6,
        )

        input_surface = input_font.render(input_text, True, COLORS["text"])
        screen.blit(input_surface, (input_rect.x + 10, input_rect.y + 10))

        # Кнопка
        button_color = COLORS["button_hover"] if button_hover else COLORS["button"]
        pygame.draw.rect(screen, button_color, button_rect, border_radius=6)
        pygame.draw.rect(screen, (0, 0, 0, 30), button_rect, 2, border_radius=6)

        button_text = button_font.render("OK", True, (255, 255, 255))
        screen.blit(button_text, (button_rect.x + 35, button_rect.y + 8))

        pygame.display.flip()

    return input_text
