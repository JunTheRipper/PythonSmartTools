# task: 剪贴板处理长段的PDF复制文本，尝试拼接文本重新放入剪贴板上
'''
tool: text exanger 文本转换器
@Input: 长段的文本 exampleFile.txt 来自于剪贴板
@Output: 文本转换重写入exampleFile.txt中并且自动复制到剪贴板上
'''
import pyperclip


class TextChanger:
    def __init__(self):
        self.string = pyperclip.paste()
        self.out_string = None

    def exangerText(self):
        list_string = list(self.string)
        for i in range(len(self.string)):
            if self.string[i] == '\n' or self.string[i] == '\r':
                if self.string[i-1] != '.':
                    list_string[i] = ' '
        self.out_string = ''.join(list_string)
        print(self.out_string)

    def print_all(self):
        print(self.string)


if __name__ == '__main__':
    exampleFile = TextChanger()
    exampleFile.exanger_text()
    # exampleFile.printAll()
    pyperclip.copy(exampleFile.out_string)
    spam = pyperclip.paste()

    # print(spam)
    print("Pyperclip solved.................")
