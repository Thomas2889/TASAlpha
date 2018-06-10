import time, random

class PCS:

    CW = {' help ':                     ['[c]help'],
          ' inspect / i ':              ['[c]inspected'],
          ' grab / take / pick up ':    ['[c]grabbed {}'],
          ' use ':                      ['[c]used {} with {}']}

    unknownMessages = ["What?", "I don't understand you.", "You don't make sense.", "Excuse me?", "Can you repeat?"]

    def what_next(self):
        choiceF = input(str("what next? "))

        result = '[w]'
        choiceF = choiceF.lower()
        choice = ' ' + choiceF + ' '

        for index in self.CW:
            for i in self.CW[index]:
                for indexS in index.split('/'):
                    if indexS in choice:
                        if index == ' inspect / i ':
                            result = self.inspect(self, choiceF, choice, index, i, indexS)
                        elif index == ' help ':
                            result = self.help(self, choiceF, choice, index, i, indexS)
                        if index == ' grab / take / pick up ':
                            result = self.grab(self, choiceF, choice, index, i, indexS)

                        if result != '[w]':
                            return result
                        else:
                            break

        return """[t]{}\nPlease do help to see a list of commands.""".format(random.choice(self.unknownMessages))

    @staticmethod
    def get_command_args(full, command):
        return (' '+full).replace(command, '')

    @staticmethod
    def check_args(choiceS, indexS):
        return len(choiceS) > 0 and not choiceS == ' ' + (indexS.replace(' ', ''))

    def inspect(self, choiceF, choice, index, i, indexS):

        if indexS == ' help ':
            print('------------------------Inspect------------------------')
            print('Inspect [item]')
            print('    [item]')
            print('       item is any item found in the room you are in')
            print('       (which can be found out by inspecting)')
            print()
            print('Inspect can also be shortened to i [item]. Inspect will')
            print('print information about the room you are currently in or')
            print('will print information about an item')


        choiceS = self.get_command_args(choiceF, indexS)
        if self.check_args(choiceS, indexS):
            return i + ' {}'.format(choiceS)
        else:
            return i


    def grab(self, choiceF, choice, index, i, indexS):

        if indexS == ' help ':
            print('------------------------Grab------------------------')
            print('Grab [item]')
            print('    [item]')
            print('       item is any item found in the room you are in')
            print('       (which can be found out by inspecting)')
            print()
            print('Grab can also be take or pick up. It will take an item')
            print('and put it in your inventory')

        choiceS = self.get_command_args(choiceF, indexS)
        if not self.check_args(choiceS, indexS):
            return '[w]'
        else:
            return i + ' {}'.format(choiceS)


    def use(self, choiceF, choice, index, i, indexS):
        choiceS = self.get_command_args(choiceF, indexS)

        if self.check_args(choiceS, indexS):

            if choiceS == 'help':

                print('-----------------------Use------------------------')
                print('Use [item1] with [item2]')
                print('    [item1]')
                print('        item1, in your inventory or in the world')
                print()
                print('    [item2]')
                print('        item2, in your inventory or in the world')
                print()
                print('Use two items together, something will happen if they')
                print('can be used together.')


    def help(self, choiceF, choice, index, i, indexS):
        choiceS = self.get_command_args(choiceF, indexS)

        if self.check_args(choiceS, indexS):

            if choiceS == 'help':

                print('------------------------Help------------------------')
                print('Help [command]')
                print('    [command]')
                print('        Command is any command found in the command list')
                print()
                print('Help prints a list of commands which can be used')

            elif choiceS == 'inspect':
                self.inspect(self, choiceF, choice, index, i, indexS)

            elif choiceS == 'grab':
                self.grab(self, choiceF, choice, index, i, indexS)

            else:
                print('Please pick a valid command')
                print()
                print('Do help [command] for more information')

        else:
            print('------------------------Help------------------------')
            print('Help [command]    - See a list of commands')
            print('Inspect [item]    - Inspect the room or an item')
            print('Grab [item]       - Take an item from the environment')
            print()
            print('Do help [command] for more information')

        return i


while True:
    print()
    print()
    print(PCS.what_next(PCS))
