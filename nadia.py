
def grid():


    scores = {'player 1': [], 'player 2': []}


    squares = {'ul':0,'um':2,'ur':4,
               'ml':0,'mm':2,'mr':4,
               'll':0,'lm':2,'lr':4}

    top,mid,bot = ['   ',' | ','   ',' | ','   '],['   ',' | ','   ',' | ','   '],['   ',' | ','   ',' | ','   ']
    break1,break2 = ['-------------------------------'],['-------------------------------']

    print('\n', top, '\n', break1, '\n', mid, '\n', break2, '\n', bot)

    player1 = 'O'
    player2 = 'X'
    for i in range(10):
        if i % 2 == 0:
            choice = input('noughts choose ')
            print(choice)
            if 'u' in choice:
                top[squares[choice]] = ' O '
            elif 'm' in choice:
                mid[squares[choice]] = ' O '
            else:
                bot[squares[choice]] = ' O '
        else:
            choice = input('crosses choose ')
            print(choice)
            if 'u' in choice:
                top[squares[choice]] = ' X '
            elif 'm' in choice:
                mid[squares[choice]] = ' X '
            else:
                bot[squares[choice]] = ' X '


        print('\n',top,'\n',break1,'\n',mid,'\n',break2,'\n',bot)
        print(top[0])

        if (top[0] == ' X ' and top[2] == ' X ' and top[4] == ' X ')\
                or (top[0] == ' X ' and mid[2] == ' X ' and bot[4] == ' X ')\
                or (top[0] == ' X ' and mid[0] == ' X ' and bot[0] == ' X ')\
                or (top[2] == ' X ' and mid[2] == ' X ' and bot[2] == ' X ')\
                or (top[4] == ' X ' and mid[4] == ' X ' and bot[4] == ' X ')\
                or top[4] == ' X ' and mid[2] == ' X ' and bot[0] == ' X ':
            print('CROSSES WINS')
        elif (top[0] == ' O ' and top[2] == ' O ' and top[4] == ' O ')\
                or (top[0] == ' O ' and mid[2] == ' O ' and bot[4] == ' O ')\
                or (top[0] == ' O ' and mid[0] == ' O ' and bot[0] == ' O ')\
                or (top[2] == ' O ' and mid[2] == ' O ' and bot[2] == ' O ')\
                or (top[4] == ' O ' and mid[4] == ' O ' and bot[4] == ' O ')\
                or top[4] == ' O ' and mid[2] == ' O ' and bot[0] == ' O ':
            print('NOUGHTS WINS')




grid()






