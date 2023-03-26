#include<vector>
//Definition for a binary tree node.
struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
};

//递归遍历v1.0
//本质为先序遍历，即先拿到当前节点来比较，然后遍历左节点和右节点数据
class Solution {
public:
    bool isSameTree(TreeNode* p, TreeNode* q) {
        bool res = true;//乐观思想，认为两棵树相同
        isSameTreeInternal(p, q, res);
        return res;
        
    }
    void isSameTreeInternal(TreeNode* p, TreeNode* q, bool& res) {
        if (res == false) return; //遵循上边乐观思想，所以如果遇到false则认为不是相同的树
        if (p == nullptr && q == nullptr) return;
        if (p == nullptr || q == nullptr) {
            res = false;
            return;//遇到false即异常，不用继续递归了直接返回false
        } else {
            if (p->val != q->val) {//同理，遇到不相等即为非相同树，不用递归直接返回
                res = false;
                return;
            } else {
                isSameTreeInternal(p->left, q->left, res);
                isSameTreeInternal(p->right, q->right, res);
            }
        }
    }
};

//递归遍历v2.0 看了别人代码做了优化
//本质为先序遍历，即先拿到当前节点来比较，然后遍历左节点和右节点数据
class Solution {
public:
    bool isSameTree(TreeNode* p, TreeNode* q) {
        if (p == nullptr && q == nullptr) return true;
        if (p == nullptr || q == nullptr) return false;
        if (p->val != q->val) return false;
        return isSameTree(p->left, q->left) && isSameTree(p->right, q->right);
    }
};