# GROUP-NAME - lab NUMBER - variant NUMBER

This is an example project which demonstrates project structure and necessary
CI checks. It is not the best structure for real-world projects, but good
enough for educational purposes.

## Project structure

- `BinaryTree.py` -- implementation of `BinaryTreeNode` class.

- `BinaryTree_test.py` -- unit and PBT tests for `BinaryTreeNode`

## Features

- PBT: `test_add_commutative`

## Contribution

- Lu Bin (1476683166@qq.com) -- All work.
- Wang Yining (351432511@qq.com) -- All work.

## Changelog
- 26.05.2024 - 7
  - Update README.
- 24.05.2024 - 6
  - fix bugs in code.
- 17.05.2024 - 5
  - fix bugs in code.
- 10.05.2024 - 4
  - Implement PBT test.
- 05.05.2024 - 3
  - Implement unit test.
- 29.03.2022 - 2
  - Add test coverage.
- 29.03.2022 - 1
  - Update README.
- 29.05.2024 - 0
  - Initial

## Design notes
- 1. Variable programming allows the value of variables to change while the code is running, 
    making programming more intuitive and achieving higher performance. However, 
    in a multi-threaded or concurrent environment, 
    variable states can easily lead to race conditions and data inconsistency issues.
    In immutable programming, once a variable is assigned a value, 
    it cannot be changed. Each modification requires a new data structure, 
    which is more suitable for multi-threaded or concurrent environments, 
    and there is no need to worry about data race conditions. 
    However, every time the data is modified, a new copy will be created, 
    which may cause more memory consumption and garbage collection pressure. 
    At the same time, it is necessary to change the programming idea when programming, which is more cumbersome.

- 2. In immutable programming, all objects cannot be changed after they are created, 
    and each change requires the generation of a new data structure. 
    Therefore, the copy() function is used repeatedly in the code to build a new data 
    structure based on the original data structure to ensure that the original structure will not change.

- 3. When implementing a Binary Tree based set, special conditions are sometimes overlooked. 
    For example, if the implemented function fails to handle empty inputs. 
    Due to the nature of property-based testing (PBT), automatically generated inputs may not include empty inputs. 
    Consequently, the test may pass, giving the impression that the function is problem-free. 
    However, when we manually introduce marginal conditions such as empty lists or empty trees, the test will fail.
