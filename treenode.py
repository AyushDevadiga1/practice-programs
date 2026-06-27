class TreeNode:
    print(" Tree Node initialized") # Once the import is cached by the importing module this print statement wont be executed again 
    def __init__(self,left,right,val):
        self.left = left
        self.right = right
        self.val = val