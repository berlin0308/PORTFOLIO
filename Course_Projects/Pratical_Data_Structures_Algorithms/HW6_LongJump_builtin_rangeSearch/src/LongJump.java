// import org.json.simple.JSONArray;
// import org.json.simple.JSONObject;
// import org.json.simple.parser.JSONParser;
// import org.json.simple.parser.ParseException;

// import java.io.FileNotFoundException;
// import java.io.FileReader;
// import java.io.IOException;

import java.util.NoSuchElementException;

// import edu.princeton.cs.algs4.BST;
import edu.princeton.cs.algs4.Queue;

class LongJump {

    public BST<Integer,Integer> PlayerDistanceBST;
    
    public LongJump(int[] playerList){
        PlayerDistanceBST = new BST<Integer,Integer>();
        for(int p:playerList){
            PlayerDistanceBST.put(p, p);
        }
    }

    // Add new player in the competition with different distance
    public void addPlayer(int distance) {
        PlayerDistanceBST.put(distance, distance);
    }
    // return the winners total distance in range[from, to]
    public int winnerDistances(int from, int to) {
        // System.out.print("\nwinnerDistances:");
        int Sum =0;
        for(int i:PlayerDistanceBST.rangeSearch(from, to)){
            Sum += i;
        }

        return Sum;
    }

    public void displayBST(){

        System.out.print("\nBST:");
        for(int a:PlayerDistanceBST.keys()){
            System.out.print(a);
            System.out.print(' ');
        }
        System.out.println('\n');
    }
    public static void main(String[] args) {
        // test t = new test(args);
        // LongJump solution = new LongJump(new int[]{2,5,6});
        // System.out.println(solution.winnerDistances(3,10));
        // solution.addPlayer(10);
        // solution.addPlayer(8);
        // solution.addPlayer(13);
        // System.out.println(solution.winnerDistances(3,10));
        // solution.displayBST();
        // LongJump solution = new LongJump(new int[]{5,6,2,8,7,11,10,12});
        // solution.displayBST();
    }
}


class BST<Key extends Comparable<Key>, Value> {
    private Node root;             // root of BST


    private class Node {
        private final Key key;       // sorted by key
        private Value val;           // associated data
        private Node left, right;    // left and right subtrees
        private int size;            // number of nodes in subtree
        private int Dist;

        public Node(Key key, Value val, int size, int dist) {
            this.key = key;
            this.val = val;
            this.size = size;
            this.Dist = dist;
        }
    }
    public BST() {
    }
    public void put(Key key, Value val) {
        // if (key == null) throw new IllegalArgumentException("first argument to put() is null");
        // if (val == null) {
        //     delete(key);
        //     return;
        // }
        root = put(root, key, val);
        // assert check();
    }

    private Node put(Node x, Key key, Value val) {
        if (x == null) return new Node(key, val, 1,1);
        int cmp = key.compareTo(x.key);
        if      (cmp < 0) x.left  = put(x.left,  key, val);
        else if (cmp > 0) x.right = put(x.right, key, val);
        else              x.val   = val;
        x.size = 1 + size(x.left) + size(x.right);
        x.Dist = x.Dist + getDist(x.left) + getDist(x.right);
        return x;
    }

    
    // return number of key-value pairs in BST rooted at x
    private int size(Node x) {
        if (x == null) return 0;
        else return x.size;
    }

    private int getDist(Node x) {
        if (x == null) return 0;
        else return x.Dist;
    }

    

    int size() {
        return size(root);
    }

    int getDist() {
        return getDist(root);
    }
    public boolean isEmpty() {
        return size() == 0;
    }
    
    public Key floor(Key key) {
        if (key == null) throw new IllegalArgumentException("argument to floor() is null");
        if (isEmpty()) throw new NoSuchElementException("called floor() with empty symbol table");
        Node x = floor(root, key);
        if (x == null) return null;
        else return x.key;
    }

    private Node floor(Node x, Key key) {
        if (x == null) return null;
        int cmp = key.compareTo(x.key);
        if (cmp == 0) return x;
        if (cmp <  0) return floor(x.left, key);
        Node t = floor(x.right, key);
        if (t != null) return t;
        else return x;
    }

    public Key ceiling(Key key) {
        if (key == null) throw new IllegalArgumentException("argument to ceiling() is null");
        if (isEmpty()) throw new NoSuchElementException("called ceiling() with empty symbol table");
        Node x = ceiling(root, key);
        if (x == null) return null;
        else return x.key;
    }

    private Node ceiling(Node x, Key key) {
        if (x == null) return null;
        int cmp = key.compareTo(x.key);
        if (cmp == 0) return x;
        if (cmp < 0) {
            Node t = ceiling(x.left, key);
            if (t != null) return t;
            else return x;
        }
        return ceiling(x.right, key);
    }
    public Iterable<Key> keys() {
        return rangeSearch(min(), max());
    }

    Key min() {
        if (isEmpty()) throw new NoSuchElementException("called min() with empty symbol table");
        return min(root).key;
    }

    private Node min(Node x) {
        if (x.left == null) return x;
        else                return min(x.left);
    }

    public Key max() {
        if (isEmpty()) throw new NoSuchElementException("called max() with empty symbol table");
        return max(root).key;
    }

    private Node max(Node x) {
        if (x.right == null) return x;
        else                 return max(x.right);
    }


    public Iterable<Key> rangeSearch(Key lo, Key hi) {
        if (lo == null) throw new IllegalArgumentException("first argument to keys() is null");
        if (hi == null) throw new IllegalArgumentException("second argument to keys() is null");

        Queue<Key> queue = new Queue<Key>();
        keys(root, queue, lo, hi);
        return queue;
    }

    private void keys(Node x, Queue<Key> queue, Key lo, Key hi) {
        if (x == null) return;
        int cmplo = lo.compareTo(x.key);
        int cmphi = hi.compareTo(x.key);
        if (cmplo < 0) keys(x.left, queue, lo, hi);
        if (cmplo <= 0 && cmphi >= 0) queue.enqueue(x.key);
        if (cmphi > 0) keys(x.right, queue, lo, hi);
    }

}

// class test{
//     public test(String[] args) {
//         LongJump g;
//         JSONParser jsonParser = new JSONParser();
//         try (FileReader reader = new FileReader("C:\\Users\\BERLIN CHEN\\Desktop\\2022PDSA\\HW6_LongJump\\LongJump.json")) {
//             JSONArray all = (JSONArray) jsonParser.parse(reader);
//             int count = 0;
//             for (Object CaseInList : all) {
//                 count++;
//                 JSONArray a = (JSONArray) CaseInList;
//                 int testSize = 0;
//                 int waSize = 0;
//                 System.out.print("Case ");
//                 System.out.println(count);
//                 //Board Setup
//                 JSONObject argsSetting = (JSONObject) a.get(0);
//                 a.remove(0);

//                 JSONArray argSettingArr = (JSONArray) argsSetting.get("args");

//                 int[] arr=new int[argSettingArr.size()];
//                 for(int k=0;k<argSettingArr.size();k++) {
//                     arr[k] = (int)(long) argSettingArr.get(k);
//                 }
//                 g = new LongJump(arr);

//                 for (Object o : a) {
//                     JSONObject person = (JSONObject) o;

//                     String func = person.get("func").toString();
//                     JSONArray arg = (JSONArray) person.get("args");

//                     switch (func) {
//                         case "addPlayer" : g.addPlayer(Integer.parseInt(arg.get(0).toString()));
//                         case "winnerDistances" : {
//                             testSize++;
//                             Integer t_ans = (int)(long)person.get("answer");
//                             Integer r_ans = g.winnerDistances(Integer.parseInt(arg.get(0).toString()),Integer.parseInt(arg.get(1).toString()));
//                             if (t_ans.equals(r_ans)) {
//                                 System.out.println("winnerDistances : AC");
//                             } else {
//                                 waSize++;
//                                 System.out.println("winnerDistances : WA");
//                                 System.out.println("Your answer : "+r_ans);
//                                 System.out.println("True answer : "+t_ans);
//                             }
//                         }
//                     }

//                 }
//                 System.out.println("Score: " + (testSize - waSize) + " / " + testSize + " ");
//             }
//         } catch (FileNotFoundException e) {
//             e.printStackTrace();
//         } catch (IOException e) {
//             e.printStackTrace();
//         } catch (ParseException e) {
//             e.printStackTrace();
//         }
//     }
// }