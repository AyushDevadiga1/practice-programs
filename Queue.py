#There can be two methods to use default queue:
#1 Using append(right) and pop(0)(left)
q1=[]
q1.append(4)
q1.append(3)
q1.append(23)
print(q1)
q1.pop(0)
print(q1)

#2 Using insert(0,item)(left) and pop(right)
q2=[]
q2.insert(0,4)
q2.insert(0,3)
q2.insert(0,33)
print(q2)
q2.pop()
print(q2)

#Using Collecions
import collections
q3=collections.deque()
q3.appendleft(2)
q3.appendleft(4)
print(q3)
q3.pop()
print(q3)
#Another combination is append and popleft

#Using Queue (includes syntax errors@-@)
import queue
q4=queue.Queue()
q4.put(34)
q4.put(54,block=True,timeout=None)
print(q4.queue)
q4.get()
print(q4.queue)