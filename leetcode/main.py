# test example
from typing import List


test_examples = [
    [[0,0,1,1,1,1,2,3,3]]
]
test_answer = [
  [1,1,2,2,3]
]
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        index_slow = 0
        index_fast = 0
        middle_num = 0
        while index_fast < len(nums):
            if nums[index_slow] == nums[index_fast]  and index_fast -index_slow <2:
                # 相同，且距离小于 2
                index_fast += 1
            elif nums[index_slow] == nums[index_fast]  and index_fast -index_slow ==2:
                # 相同，距离大于等于2
                index_slow += 1
                index_fast += 1
            elif nums[index_slow] != nums[index_fast]  and index_fast -index_slow <2:
                # 不同，且距离小于2
                index_slow += 1
                nums[index_slow] = nums[index_fast]
            else:
                # 不同，且距离大于等于2
                if nums[index_fast] > nums[index_slow]:
                    index_slow += 2
                    nums[index_slow]= nums[index_fast]
                    index_fast += 1
                else:
                    index_fast += 1
        return index_slow + 1
        
Keyway = Solution.removeDuplicates

if __name__ =="__main__":
    s = Solution()
    for example, answer in zip(test_examples, test_answer):
        assert Keyway(s,*example) == answer,f"Input: {example}, Output: {Keyway(s,*example)} with args:{example}, Expected: {answer}"