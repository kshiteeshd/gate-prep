"""PDS chapter 'Binary Trees, BST & AVL': extra generators, each with a worked explanation."""
import math

from content import g_pds as P
from content.kit import *

S = "PDS"
TR = "Trees & BST"
J = lambda a: " ".join(map(str, a))


def build(keys):
    t = P.BST()
    for k in keys:
        t.insert(k)
    return t.root


def delete(n, k):
    """Standard BST delete; a node with two children takes its in-order successor."""
    if n is None:
        return None
    if k < n[0]:
        n[1] = delete(n[1], k)
    elif k > n[0]:
        n[2] = delete(n[2], k)
    else:
        if n[1] is None:
            return n[2]
        if n[2] is None:
            return n[1]
        s = n[2]
        while s[1] is not None:
            s = s[1]
        n[0] = s[0]
        n[2] = delete(n[2], s[0])
    return n


def catalan(n):
    return math.comb(2 * n, n) // (n + 1)


@gen(S, TR, "Tree terminology", n=60, diff="easy")
def t_term(r):
    kind = r.choice(["perfect", "level", "nulls", "minh", "full", "kary", "complete", "shapes", "maxh"])
    if kind == "perfect":
        h = r.randint(2, 7)
        return nat(r, "How many nodes does a perfect binary tree of height %d have (a single node has height 0)?" % h, 2 ** (h + 1) - 1,
                   "Level k holds 2^k nodes, so the total is 2^0 + 2^1 + … + 2^%d = 2^%d − 1 = %d." % (h, h + 1, 2 ** (h + 1) - 1))
    if kind == "level":
        L = r.randint(3, 9)
        return nat(r, "What is the maximum number of nodes that can lie on level %d of a binary tree (the root is on level 0)?" % L, 2 ** L,
                   "Each node has at most two children, so the number of nodes at most doubles at every level: 2^%d = %d." % (L, 2 ** L))
    if kind == "nulls":
        n = r.randint(7, 40)
        return nat(r, "A binary tree has %d nodes, each stored with a left and a right pointer. How many of those pointers are NULL?" % n, n + 1,
                   "There are 2n = %d pointers. Every node except the root is pointed to by exactly one pointer, so n − 1 = %d are non-NULL. NULL pointers = 2n − (n − 1) = n + 1 = %d." % (2 * n, n - 1, n + 1))
    if kind == "minh":
        n = r.randint(10, 200)
        h = int(math.log2(n))
        return nat(r, "What is the minimum possible height (in edges) of a binary tree with %d nodes?" % n, h,
                   "A tree of height h holds at most 2^(h+1) − 1 nodes, so we need 2^(h+1) − 1 ≥ %d. The smallest such h is ⌊log2 %d⌋ = %d." % (n, n, h))
    if kind == "full":
        i = r.randint(5, 40)
        return nat(r, "A full binary tree (every node has 0 or 2 children) has %d internal nodes. How many leaves does it have?" % i, i + 1,
                   "In a full binary tree, leaves = internal nodes + 1. Reason: edges = 2·internal = (internal + leaves) − 1, so leaves = internal + 1 = %d." % (i + 1))
    if kind == "kary":
        k, i = r.randint(3, 5), r.randint(3, 15)
        return nat(r, "A full %d-ary tree has %d internal nodes. How many leaves does it have?" % (k, i), (k - 1) * i + 1,
                   "Edges = k·i = (i + L) − 1, so L = (k − 1)·i + 1 = %d·%d + 1 = %d." % (k - 1, i, (k - 1) * i + 1))
    if kind == "complete":
        n = r.randint(8, 99)
        return nat(r, "A complete binary tree stored as a heap has %d nodes. How many of them are internal nodes (have at least one child)?" % n, n // 2,
                   "Node i (1-indexed) has a child iff 2i ≤ n, i.e. i ≤ ⌊n/2⌋. So there are ⌊%d/2⌋ = %d internal nodes and %d leaves." % (n, n // 2, n - n // 2))
    if kind == "shapes":
        n = r.randint(3, 8)
        return nat(r, "How many structurally different binary trees can be formed with %d nodes?" % n, catalan(n),
                   "The count is the Catalan number C_n = C(2n, n)/(n + 1) = C(%d, %d)/%d = %d." % (2 * n, n, n + 1, catalan(n)))
    h = r.randint(3, 8)
    return nat(r, "What is the maximum height (in edges) of a binary tree with %d nodes?" % (h + 1), h,
               "The tallest tree is a chain in which every node has one child, so with n nodes the height is n − 1 = %d." % h)


@gen(S, TR, "Tree reconstruction", n=70, diff="medium", marks=2)
def t_recon(r):
    keys = r.sample(range(1, 40), r.randint(6, 8))
    root = build(keys)
    pre, ino, post = P.preorder(root), P.inorder(root), P.postorder(root)
    kind = r.choice(["pre_in_post", "post_in_pre", "pre_post_bst", "level"])
    if kind == "pre_in_post":
        return mcq(r, "A binary tree has pre-order traversal %s and in-order traversal %s. Its post-order traversal is" % (J(pre), J(ino)), J(post),
                   [J(pre[::-1]), J(ino[::-1]), J(list(reversed(post))), J(sorted(post, reverse=True))],
                   "The first pre-order key %d is the root. Its position in the in-order list splits the keys into the left part %s and the right part %s. Repeat on each part: the next pre-order key is that part's root. Reading left, right, root gives %s." % (pre[0], J(ino[:ino.index(pre[0])]) or "(none)", J(ino[ino.index(pre[0]) + 1:]) or "(none)", J(post)))
    if kind == "post_in_pre":
        return mcq(r, "A binary tree has post-order traversal %s and in-order traversal %s. Its pre-order traversal is" % (J(post), J(ino)), J(pre),
                   [J(post[::-1]), J(ino[::-1]), J(post), J(sorted(pre))],
                   "The LAST post-order key %d is the root. In the in-order list it splits the keys into left %s and right %s. The root of each part is the last post-order key belonging to it. Reading root, left, right gives %s." % (post[-1], J(ino[:ino.index(post[-1])]) or "(none)", J(ino[ino.index(post[-1]) + 1:]) or "(none)", J(pre)))
    if kind == "pre_post_bst":
        return mcq(r, "The pre-order traversal of a binary SEARCH tree is %s. Its post-order traversal is" % J(pre), J(post),
                   [J(pre[::-1]), J(ino), J(sorted(pre, reverse=True)), J(list(reversed(ino)))],
                   "For a BST the in-order traversal is the sorted order %s. Combine it with the given pre-order to rebuild the tree, then read left, right, root: %s." % (J(ino), J(post)))
    lv, q = [], [root]
    while q:
        n = q.pop(0)
        lv.append(n[0])
        q += [c for c in (n[1], n[2]) if c]
    return mcq(r, "Keys %s are inserted in this order into an empty BST. Its level-order traversal is" % J(keys), J(lv),
               [J(pre), J(post), J(ino), J(sorted(keys, reverse=True))],
               "Insert in the given order to build the tree; level-order visits the root, then its children left to right, then the next level, using a queue: %s." % J(lv))


@gen(S, TR, "BST deletion", n=70, diff="medium", marks=2)
def t_del(r):
    keys = r.sample(range(1, 60), r.randint(7, 9))
    root = build(keys)
    ino = P.inorder(root)
    two = [k for k in keys if (lambda n: n[1] is not None and n[2] is not None)(_find(root, k))]
    one = [k for k in keys if (lambda n: (n[1] is None) != (n[2] is None))(_find(root, k))]
    leaf = [k for k in keys if (lambda n: n[1] is None and n[2] is None)(_find(root, k))]
    kind = r.choice(["two", "two", "one", "leaf", "height"])
    pool = {"two": two, "one": one, "leaf": leaf, "height": two or leaf}[kind]
    if not pool:
        raise Skip()
    k = r.choice(pool)
    node = _find(root, k)
    succ = min(P.inorder(node[2])) if node[2] else None
    before = P.preorder(root)
    new = delete(build(keys), k)
    ks = J(keys)
    if kind == "height":
        return nat(r, "Keys %s are inserted into an empty BST. Then the key %d is deleted (a node with two children is replaced by its in-order successor). What is the height of the resulting tree (edges)?" % (ks, k), P.height(new),
                   "Build the tree (pre-order %s), delete %d%s and measure the longest root-to-leaf path in the result." % (J(before), k, " using successor %d" % succ if succ else ""))
    why = {"two": "%d has two children, so it is replaced by its in-order successor %d (the smallest key in its right subtree), and that successor node is then removed." % (k, succ if succ else 0),
           "one": "%d has exactly one child, so that child's subtree takes its place." % k,
           "leaf": "%d is a leaf, so it is simply removed." % k}[kind]
    ans = J(P.preorder(new))
    return mcq(r, "Keys %s are inserted in this order into an empty BST, then the key %d is deleted (a node with two children is replaced by its in-order successor). The pre-order traversal of the resulting tree is" % (ks, k), ans,
               [J(before), J(P.preorder(delete(build(keys), keys[0]))), J(P.inorder(new)), J(P.postorder(new))],
               "Original pre-order: %s. %s Pre-order afterwards: %s." % (J(before), why, ans))


def _find(n, k):
    while n and n[0] != k:
        n = n[1] if k < n[0] else n[2]
    return n


@gen(S, TR, "BST search and successor", n=70, diff="easy")
def t_succ(r):
    keys = r.sample(range(1, 60), r.randint(7, 10))
    root = build(keys)
    ino = P.inorder(root)
    ks = J(keys)
    kind = r.choice(["succ", "pred", "cmp", "min_right"])
    if kind in ("succ", "pred"):
        i = r.randint(1, len(ino) - 2)
        k = ino[i]
        ans = ino[i + 1] if kind == "succ" else ino[i - 1]
        name = "in-order successor" if kind == "succ" else "in-order predecessor"
        return nat(r, "Keys %s are inserted in this order into an empty BST. What is the %s of the key %d?" % (ks, name, k), ans,
                   "The in-order traversal of a BST is the sorted order %s. The key just %s %d in that list is %d." % (J(ino), "after" if kind == "succ" else "before", k, ans))
    if kind == "cmp":
        k = r.choice(keys)
        n, c, path = root, 0, []
        while n[0] != k:
            c += 1
            path.append(n[0])
            n = n[1] if k < n[0] else n[2]
        c += 1
        path.append(k)
        return nat(r, "Keys %s are inserted in this order into an empty BST. How many key comparisons (one per node visited) does a search for %d make?" % (ks, k), c,
                   "The search path is %s, which visits %d nodes, so %d comparisons." % (J(path), c, c))
    n = root
    if n[2] is None:
        raise Skip()
    m = n[2]
    while m[1]:
        m = m[1]
    return nat(r, "Keys %s are inserted in this order into an empty BST. What is the in-order successor of the ROOT?" % ks, m[0],
               "The root %d has a right subtree, so its successor is the leftmost node of that subtree: %d." % (root[0], m[0]))


_N = [1, 2, 4, 7, 12, 20, 33, 54, 88, 143]


@gen(S, TR, "AVL properties", n=60, diff="medium")
def t_avlp(r):
    kind = r.choice(["minn", "maxh", "maxn", "sorted"])
    if kind == "minn":
        h = r.randint(3, 8)
        return nat(r, "What is the minimum number of nodes in an AVL tree of height %d (a single node has height 0)?" % h, _N[h],
                   "N(h) = N(h−1) + N(h−2) + 1 (a root, one subtree of height h−1 and the thinnest allowed sibling of height h−2) with N(0) = 1, N(1) = 2: %s. So N(%d) = %d." % (", ".join(map(str, _N[:h + 1])), h, _N[h]))
    if kind == "maxh":
        n = r.randint(10, 120)
        h = max(i for i in range(len(_N)) if _N[i] <= n)
        return nat(r, "What is the maximum possible height of an AVL tree with %d nodes (a single node has height 0)?" % n, h,
                   "Sparsest AVL trees have N(h) = %s nodes for h = 0, 1, 2, …. The largest h with N(h) ≤ %d is %d." % (", ".join(map(str, _N)), n, h))
    if kind == "maxn":
        h = r.randint(2, 7)
        return nat(r, "What is the maximum number of nodes in an AVL tree of height %d (a single node has height 0)?" % h, 2 ** (h + 1) - 1,
                   "The fullest AVL tree is the perfect binary tree: 2^(h+1) − 1 = %d." % (2 ** (h + 1) - 1))
    n = r.choice([3, 7, 15, 31])
    keys = list(range(1, n + 1))
    rot, ht = P.avl_insert_rotations(keys)
    return nat(r, "The keys 1, 2, …, %d are inserted in increasing order into an empty AVL tree. How many rotations are performed in total (a double rotation counts as 2)?" % n, rot,
               "Each time the right spine becomes too long, a single left rotation fixes it. Simulating the %d insertions gives %d rotations and a perfect tree of height %d." % (n, rot, ht))
