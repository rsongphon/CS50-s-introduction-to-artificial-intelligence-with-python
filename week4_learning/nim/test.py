action = set()
for row_pile , pile in enumerate([2, 1, 0, 0]):
    for num_object in range(1, pile+1):
        action.add((row_pile,num_object))

print(action)