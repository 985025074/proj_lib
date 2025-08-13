# sys.path
默认加入文件所在路径，sys.path.append(".") 执行终端pwd路径# sys.path
默认加入文件所在路径，sys.path.append(".") 执行终端pwd路径

# 类内修饰器 无法访问类变量：
```C
# test example
from typing import List


test_examples = [
    [[1,2,3,4],3]
]
test_answer = [
    [1,2,4]
]
class Solution:
    Keyway = None
    def is_keyway(func):
        Keyway = func
    @is_keyway
    def removeElement(self, nums: List[int], val: int) -> int:
        slow = 0
        for fast in range(len(nums)):
            if nums[fast] != val:
                nums[slow] = nums[fast]
                slow += 1
        return slow


if __name__ =="__main__":
    s = Solution()
    for example, answer in zip(test_examples, test_answer):
        assert s.Keyway(*example) == answer
```
 
