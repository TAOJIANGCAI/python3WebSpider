import os


def get_dirname():
    return os.path.dirname(os.path.realpath(__file__))


def get_dirname2():
    return os.getcwd()


print(get_dirname())
print(get_dirname2())

# 1，os.path.dirname(os.path.realpath(__file__)) 和 os.getcwd()都是返回当前模块所在的绝对路径
# E:\pyProject\test\plist
# E:\pyProject\test\plist

# 2， get_dirname()和get_dirname2()方法在别的模块中被调用时：假如get_dirname()和get_dirname2()都在A模块中，在B模块中被调用
# os.path.dirname(os.path.realpath(__file__))获取的是A模块所在的路径，而os.getcwd()获取的是B模块所在的路径

# E:\pyProject\test\plist
# E:\pyProject\test\plist\TestDir
