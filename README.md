# GROUP-NAME - lab NUMBER - variant NUMBER

This is an example project which demonstrates project structure and necessary
CI checks. It is not the best structure for real-world projects, but good
enough for educational purposes.

## Project structure

- `BinaryTree.py` -- implementation of `BinaryTree` class and `BinaryTreeNode` class.

- `BinaryTree_test.py` -- unit and PBT tests for `BinaryTree`

## Features

- PBT: `test_add_commutative`

## Contribution

- Lu Bin (1476683166@qq.com) -- All work.
- Wang Yining (351432511@qq.com) -- All work.

## Changelog
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

- 3. When implementing a Binary Tree based set, special conditions are sometimes overlooked. 
    For example, if the implemented function fails to handle empty inputs. 
    Due to the nature of property-based testing (PBT), automatically generated inputs may not include empty inputs. 
    Consequently, the test may pass, giving the impression that the function is problem-free. 
    However, when we manually introduce marginal conditions such as empty lists or empty trees, the test will fail.
