class node:
    def __init__(self,data):
        self.next=None
        self.data=data
    def insert_beg(self,data):
        begg=node(data)
        if self.head is None:
            print('Linked list is empty')
        else:
            begg.next=head
            head=begg

l1=node(1)
l1.insert_beg(2)
print(l1)
