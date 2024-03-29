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

//二叉搜索树（Binary Search Tree，简称 BST）是一种很常用的的二叉树。它的定义是：一个二叉树中，任意节点的值要大于左子树所有节点的值，且要小于右边子树的所有节点的值。

//递归方法v1.0 注意！！！是错误版本，只比较了单层上下级的值
//本质为先序遍历
class Solution {
public:
    bool isValidBST(TreeNode* root) {
        if (root == nullptr) return true;
        if (root->left != nullptr && root->val < root->left->val) return false;
        if (root->right != nullptr && root->val > root->right->val) return false;
        return isValidBST(root->left) && isValidBST(root->right);
    }
};

//v1.0有错误是因为只比较了单层上下级的值，但是BST定义是任意节点的值要大于左子树所有节点的值，且要小于右边子树的所有节点的值
//因此新方法为，中序遍历，对每个节点，获取其左子树和右子树的所有值进行比较。也就是做了2层中序遍历

class Solution {
public:
    bool isValidBST(TreeNode* root) {
        if (root == nullptr) return true;
        std::vector<int> left_tree_values;
        std::vector<int> right_tree_values;
        getTreeValue(root->left, left_tree_values);
        getTreeValue(root->right, right_tree_values);
        for (const auto& i : left_tree_values) {
            if (root->val <= i) return false;
        }
        for (const auto& i : right_tree_values) {
            if (root->val >= i) return false;
        }
        return isValidBST(root->left) && isValidBST(root->right);
    }
    void getTreeValue(TreeNode* root, std::vector<int>& res) {//中序遍历获取所有值
        if (root == nullptr) return;
        res.emplace_back(root->val);
        getTreeValue(root->left, res);
        getTreeValue(root->right, res);
    }
};

//v2.0 看labuladuo答案：https://github.com/shichangzhi/fucking-algorithm-book/blob/main/%E7%AC%AC3%E7%AB%A0-%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84%E7%B3%BB%E5%88%97/3.3-%E4%BA%8C%E5%8F%89%E6%90%9C%E7%B4%A2%E6%A0%91%E6%93%8D%E4%BD%9C%E9%9B%86%E9%94%A6.md
class Solution {
public:
    bool isValidBST(TreeNode* root) {
        return isValidBST(root, nullptr, nullptr);
    }
    bool isValidBST(TreeNode* root, TreeNode* min, TreeNode* max) {
        if (! root) return true;
        if (min && min->val >= root->val) return false;
        if (max && max->val <= root->val) return false;
        return isValidBST(root->left, min, root) && isValidBST(root->right, root, max);
    }
};