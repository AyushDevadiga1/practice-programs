"""
import math_utils
        │
        ▼
1. Find file
        │
        ▼
2. Execute entire file
        │
        ▼
3. Store module in memory
        │
        ▼
4. Cache it
"""

import sys

# No matter hown much times I import later there would be no imports later as we have already cached the programme
from treenode import TreeNode
# from treenode import TreeNode
# from treenode import TreeNode
# from treenode import TreeNode
# from treenode import TreeNode
tree_1 = TreeNode(1,1,1)
print(type(tree_1))
# print(sys.modules) # At the end we can clearly see that our module cached

