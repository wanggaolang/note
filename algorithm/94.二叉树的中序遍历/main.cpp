#include<vector>
using namespace std;
//Definition for a binary tree node.
struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
};

////////第1版////////
//递归方法
class Solution {
public:
    vector<int> inorderTraversal(TreeNode* root) {
        if (root == nullptr) return {};
        vector<int> res;
        res = inorderTraversal(root->left); //遍历左边所有节点获取值
        res.emplace_back(root->val); //获取中间节点数据
        vector<int> right_values = inorderTraversal(root->right); //遍历右边所有节点获取值
        res.insert(res.begin(), std::begin(right_values), std::end(right_values)); //将右边所有节点数据存入结果中
        return res;
    }
};

////////第2版////////
//递归方法
//由于1版的获取右边节点数据拿到后，还做了次遍历来转存数据不够优雅，该版是1版的改进
class Solution {
public:
    vector<int> inorderTraversal(TreeNode* root) {
        vector<int> res;
        inorderTraversalInternal(root, res);
        return res;
    }
    void inorderTraversalInternal(TreeNode* root, vector<int>& res) {
        if (root == nullptr) return;
        inorderTraversalInternal(root->left, res);
        res.emplace_back(root->val);
        inorderTraversalInternal(root->right, res);
    }
};

////////第3版////////
//非递归方法
//思想：首先手里是根节点，但是最先处理的应该是最左节点，也就是手里最先拿到的节点反而得留着，数据结构就是使用栈
//在整个遍历过程中，1）用栈记录向最左节点走过的所有节点（循环）；2）到最左节点后存入该节点数据并出栈（单次判断）；
// 3）如果最左节点右侧还有节点，则又走步骤1（一个大循环）
class Solution {
public:
    vector<int> inorderTraversal(TreeNode* root) {
        if (root == nullptr) return {};
        vector<int> res;
        TreeNode* flow_ptr = root;
        vector<TreeNode*> ptr_stack;
        do {
            while (flow_ptr != nullptr) {
                ptr_stack.emplace_back(flow_ptr);
                flow_ptr = flow_ptr->left;
            }//入栈左节点

            if (!ptr_stack.empty()) {
                //出栈最左节点
                auto most_left_ptr = ptr_stack.back();
                res.emplace_back(most_left_ptr->val);
                ptr_stack.pop_back();

                //如果最左节点右边还有节点，则用流动指针记录下这个节点，在下次循环中又执行入栈流程
                if (most_left_ptr->right != nullptr) {
                    flow_ptr = most_left_ptr->right;
                }
            }
        } while ((!ptr_stack.empty()) || (flow_ptr != nullptr));//注意这里还要判断flow_ptr不为空，有可能出现栈已经出完，但是还有右节点在flow_ptr中
        return res;
    }
};


////////重点知识////////
二叉树的遍历分为前、中、后序遍历以及层次遍历，其中前中后序遍历都指定根节点（中间节点）位置，如前序变为即中-左-右，后边遍历为左-右-中
要体会递归的思想，即只处理最小/最特殊的情况，把剩下所有复杂部分丢到函数本身做递归
注意第1版的2个vector做insert方法