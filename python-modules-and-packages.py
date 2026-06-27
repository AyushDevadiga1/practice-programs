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

# from module import * pollutes the namespace, makes code harder to read, and can overwrite existing names.

"""
A package is simply a collection of related modules.

Example:

my_project/

    models/
        __init__.py
        linear.py
        tree.py

Folder + __init__.py -> Package

Basically a collection of the modules in one place

"""



"""
python -m models.tree

Basically it runs the the project from package level instead of module level
This is a better practice as there can be relative imports and these import may not be able to find the desired path .

Relative imports

↓

Only inside packages

Never standalone scripts


"""


"""
pyproject.toml stores direct dependencies, while poetry.lock stores the fully resolved dependency tree, making installations reproducible.
"""