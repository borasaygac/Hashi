import os


def print_to_txt(n, model, num):
    output_folder = os.path.join(os.getcwd(), 'Solution')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_path = os.path.join(output_folder, f'sol{num}.txt')
        
    with open(output_path, 'w') as file:
        if model is None:
            file.write("No model!")
            return
        j = 0
        I = lambda i: (i // 4) // len(n[0])

        for i in range(0, len(model), 4):
            if n[I(i)][j].val != 0:
                file.write(f'{n[I(i)][j].val} ')
                print(f'{n[I(i)][j].val} ' , end=' ')
            else:
                chunk = model[i:i + 4]

                to_write = '0 '
                for c in chunk:
                    # if not (j > 0 and j < len(n[0])-1):
                    #     to_write = '~  '
                    if c > 0:
                        # print corresponding bridge symbol from {v1, v1, h1, h2}
                        to_write = chr(104 + ((c - i) // 3) * 14) + f"{((c + 1) % 2) + 1}"
                file.write(to_write)
                print(to_write, end=' ')

            j += 1
            if (((i // 4) + 1) % len(n[0])) == 0:
                file.write('\n')
                print('\n')
                j = 0
            else:
                file.write('  ')
                print('  ', end=' ')
