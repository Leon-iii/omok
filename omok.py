import os
import keyboard as kb

HIGHLIGHT_1 = '\033[44;30m'
HIGHLIGHT_2 = '\033[41;30m'
HIGHLIGHT_BOTH = '\033[45;30m'
NORMAL = '\033[m'
#Console에서 커서 구현을 위한 하이라이팅 ASCII 확장 글자? 어쩌구. 나도 잘 모른다.

board = [[4 for col in range(15)] for row in range(15)]
board[0] = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2]
board[14] = [6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8]
for i in range(1, 14):
    board[i][0] = 3
    board[i][14] = 5
#좀 미개하지만, 보드 구현은 list comprehension과 부분적으로 치환해서 chars 리스트에 있는 글자들을 조합해서 Console에 출력하는 것으로 한다.

chars = ['┌', '┬', '┐', '├', '┼', '┤', '└', '┴', '┘', '●', '○']
#이게 출력될 보드의 Sprite들.

running = True
#게임이 진행 중인가?
to_play = 1
#X번 플레이어가 할 차례? (1 or 2)

cur1_r = 0
cur1_c = 0

cur2_r = 0
cur2_c = 0
#1, 2번 플레이어 커서 설정

os.system('color 07')

def print_board():
#화면 상태를 특수문자를 사용해 조립하여 콘솔에 출력해주는 함수.
    output = ''
    for row in range(15):
        for col in range(15):
            if cur1_r == row and cur1_c == col: output += HIGHLIGHT_1
            if cur2_r == row and cur2_c == col:
                output += HIGHLIGHT_2
                if cur1_r == cur2_r and cur1_c == cur2_c: output += HIGHLIGHT_BOTH
            output += chars[board[row][col]]

            if cur1_r == row and cur1_c == col: output += NORMAL
            if cur2_r == row and cur2_c == col:
                output += NORMAL
            if col != 14: output += '─'
            #마지막 줄이 아니면 중간에 일자 막대기 넣어서 비율 맞추기.
        output += "\n"
    os.system('cls')
    #Console 클리어
    print(output)
    #위에서 조립한 화면을 출력.
        
def check_for_streak(board:list, pos_r:int, pos_c:int):
#현재 좌표에서 4방향(가로, 세로, 대각 방향 2개)으로 연속된 돌이 몇개가 있는지 확인.

    directions = [[-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [1, 1], [-1, 1], [1, -1]]
    #탐색 대상이 되는 8방향.
    result = []

    for direc in directions:

        length = 0
        #이번 방향의 체인 길이
        for mult in range(1, 5):
            #direction에 mult만큼 곱해서 이동한 다음 현재 칸과 일치하는지 탐지.
            cur_r = pos_r + direc[0]*mult
            cur_c = pos_c + direc[1]*mult

            if cur_r < 0 or cur_r > 14 or cur_c < 0 or cur_c > 14: break
            #배열 크기 초과로 다음 방향으로 넘어감.
            if board[cur_r][cur_c] == board[pos_r][pos_c]: length += 1
            #시작 칸과 이 칸이 일치한다면 체인 길이에 1 추가.
            else: break
            #아니면 다음 방향으로.
        result.append(length)
        #결과 리스트에 현재 방향에 대한 탐지 결과를 추가.
    
    streak = 0
    for i in range(0, 8, 2):
        streak = max(streak, result[i]+result[i+1]+1)
    return streak
    #가장 길었던 체인의 갯수를 반환.

while running:

    print_board()
    event = str(kb.read_event())

    if 'up down' in event: cur1_r = max(cur1_r - 1, 0)
    if 'left down' in event: cur1_c = max(cur1_c - 1, 0)
    if 'down down' in event: cur1_r = min(cur1_r + 1, 14)
    if 'right down' in event: cur1_c = min(cur1_c + 1, 14)
    #플레이어 1 이동

    if 'right shift down' in event:
    #플레이어 1 착수
        if to_play == 1 and board[cur1_r][cur1_c] < 9:
            board[cur1_r][cur1_c] = 9

            streak = check_for_streak(board, cur1_r, cur1_c)
            if streak == 5: running = False
            #6목은 안된다. 무조건 5목.
            if running: to_play = 2
            #착수했는데도 오목이 완성이 안되면 다음 플레이어로 턴이 넘어감.

    if 'w down' in event: cur2_r = max(cur2_r - 1, 0)
    if 'a down' in event: cur2_c = max(cur2_c - 1, 0)
    if 's down' in event: cur2_r = min(cur2_r + 1, 14)
    if 'd down' in event: cur2_c = min(cur2_c + 1, 14)
    #플레이어 2 이동

    if 'z down' in event:
    #플레이어 2 착수
        if to_play == 2 and board[cur2_r][cur2_c] < 9:
            board[cur2_r][cur2_c] = 10

            streak = check_for_streak(board, cur2_r, cur2_c)
            if streak == 5: running = False
            #6목은 안된다. 무조건 5목.
            if running: to_play = 1
            #착수했는데도 오목이 완성이 안되면 다음 플레이어로 턴이 넘어감.

print_board()

if to_play == 1: print("Player 1(Blue) win")
else: print("Player 2(Red) win")