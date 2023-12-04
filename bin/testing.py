obj = open("test", 'w')
obj.write("test")
obj.close()
obj = open("test", 'r')
print(obj.read())
obj.close