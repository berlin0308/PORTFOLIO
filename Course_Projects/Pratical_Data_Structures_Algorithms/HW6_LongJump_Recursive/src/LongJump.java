// import org.json.simple.JSONArray;
// import org.json.simple.JSONObject;
// import org.json.simple.parser.JSONParser;
// import org.json.simple.parser.ParseException;

// import java.io.FileNotFoundException;
// import java.io.FileReader;
// import java.io.IOException;

import java.util.NoSuchElementException;

// import edu.princeton.cs.algs4.BST;


/* 
 * 11/12 12:30-14:30
 * key_getDist(int key) completed
 * displayBST() key,Dist,size,root completed
 * 
 * 11/12 21:20-24:00
 * find_LCA()
 * only search the area under LCA
 * successfully run test code, test data
 * AutoLab 40.0
 */
class LongJump {

    public BST<Integer> PlayerDistanceBST;
    
    public LongJump(int[] playerList){
        PlayerDistanceBST = new BST<Integer>();
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
        // int A_key;
        // int B_key;
        // try{
        //     A_key = PlayerDistanceBST.floor_modified(from);
        // }catch(NullPointerException e){  // if A is not found, A_key = -1
        //     A_key = -1;
        // }
        // try{
        //     B_key = PlayerDistanceBST.ceiling_modified(to);
        // }catch(NullPointerException e){
        //     B_key = -1;
        // }
        // System.out.print("\nA key: ");
        // System.out.println(A_key);
        // System.out.print("Node A Dist: ");
        // System.out.println(PlayerDistanceBST.key_getDist(A_key));
        // System.out.print("\nB key: ");
        // System.out.println(B_key);
        // System.out.print("Node B Dist: ");
        // System.out.println(PlayerDistanceBST.key_getDist(B_key));
        
        // PlayerDistanceBST.DistSum=0;
        // PlayerDistanceBST.find_LCA(from, to);
        // displayBST();
        
        // PlayerDistanceBST.rangeSearch(from, to);
        // System.out.print("\n--------\nwinner Distances: ");
        // System.out.print(PlayerDistanceBST.DistSum);
        // System.out.print("\n--------\n");
        // return PlayerDistanceBST.DistSum;

        return PlayerDistanceBST.rangeDistSum(from, to);
    }

    public void displayBST(){

        // System.out.print("\n\n\nBST key:\n");
        // for(int a:PlayerDistanceBST.keys()){
        //     System.out.print(a);
        //     System.out.print(' ');
        // }
        // System.out.print("\n\nBST Dist:\n");
        // for(int a:PlayerDistanceBST.keys()){
        //     System.out.print(PlayerDistanceBST.key_getDist(a));
        //     System.out.print(' ');
        // }
        // System.out.print("\n\nBST size:\n");
        // for(int a:PlayerDistanceBST.keys()){
        //     System.out.print(PlayerDistanceBST.key_getSize(a));
        //     System.out.print(' ');
        // }
        System.out.print("\n\nBST root key: ");
        System.out.println(PlayerDistanceBST.root.val);
        System.out.print("BST root size: ");
        System.out.println(PlayerDistanceBST.size());

        if(PlayerDistanceBST.LCA!=null){

            System.out.print("\n\nBST LCA key: ");
            System.out.println(PlayerDistanceBST.LCA.val);
            System.out.print("BST LCA size: ");
            System.out.println(PlayerDistanceBST.size(PlayerDistanceBST.LCA));
        }

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
        
        // System.out.println(solution.winnerDistances(3,10));
        // solution.displayBST();
        
    }
}


class BST<Key extends Comparable<Key>> {
    public Node root;             // root of BST
    public Node LCA;
    public int DistSum=0;

    public class Node {
        public final Key key;       // sorted by key
        public int val;           // associated data
        private Node left, right;    // left and right subtrees
        private int size;            // number of nodes in subtree
        private int Dist;

        public Node(Key key, int val, int size, int dist) {
            this.key = key;
            this.val = val;
            this.size = size;
            this.Dist = dist;
        }
    }
    public BST() {
    }

    public void put(Key key, int val) {
        // if (key == null) throw new IllegalArgumentException("first argument to put() is null");
        // if (val == null) {
        //     delete(key);
        //     return;
        // }
        root = put(root, key, val);
        // assert check();
    }

    private Node put(Node x, Key key, int val) {
        if (x == null) return new Node(key, val, 1,val);
        int cmp = key.compareTo(x.key);
        if      (cmp < 0) x.left  = put(x.left,  key, val);
        else if (cmp > 0) x.right = put(x.right, key, val);
        else              x.val   = val;
        // x.size = 1 + size(x.left) + size(x.right);
        // x.Dist = x.val+ getDist(x.left) + getDist(x.right);
        return x;
    }

    
    // return number of key-int pairs in BST rooted at x
    public int size(Node x) {
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
    
    public Key floor_modified(Key key) {
        if (key == null) throw new IllegalArgumentException("argument to floor_modified() is null");
        if (isEmpty()) throw new NoSuchElementException("called floor_modified() with empty symbol table");
        Node x = floor_modified(root, key);
        if (x == null) return null;
        else return x.key;
    }

    private Node floor_modified(Node x, Key key) {
        if (x == null) return null;
        int cmp = key.compareTo(x.key);
        //if (cmp == 0) return x;
        if (cmp <=  0) return floor_modified(x.left, key);
        Node t = floor_modified(x.right, key);
        if (t != null) return t;
        else return x;
    }

    public Key ceiling_modified(Key key) {
        if (key == null) throw new IllegalArgumentException("argument to ceiling_modified() is null");
        if (isEmpty()) throw new NoSuchElementException("called ceiling_modified() with empty symbol table");
        Node x = ceiling_modified(root, key);
        if (x == null) return null;
        else return x.key;
    }

    private Node ceiling_modified(Node x, Key key) {
        if (x == null) return null;
        int cmp = key.compareTo(x.key);
        // if (cmp == 0) return x;
        if (cmp < 0) {
            Node t = ceiling_modified(x.left, key);
            if (t != null) return t;
            else return x;
        }
        return ceiling_modified(x.right, key);
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


    public void rangeSearch(Key lo, Key hi) {
        if (lo == null) throw new IllegalArgumentException("first argument to keys() is null");
        if (hi == null) throw new IllegalArgumentException("second argument to keys() is null");

        keys(LCA, lo, hi);
    }

    private void keys(Node x, Key lo, Key hi) {
        if (x == null) return;
        int cmplo = lo.compareTo(x.key);
        int cmphi = hi.compareTo(x.key);
        if (cmplo < 0) keys(x.left, lo, hi);
        if (cmplo <= 0 && cmphi >= 0){
            // System.out.print("key in the range is found: ");
            // System.out.println(x.key);
            DistSum += x.val;
        }
        if (cmphi > 0) keys(x.right, lo, hi);
    }

    public int get(Key key) {
        return get(root, key);
    }

    private int get(Node x, Key key) {
        if (x == null) return 0;
        int cmp = key.compareTo(x.key);
        if      (cmp < 0) return get(x.left, key);
        else if (cmp > 0) return get(x.right, key);
        else              return x.val;
    }

    public int key_getDist(Key key) {
        return key_getDist(root, key);
    }

    private int key_getDist(Node x, Key key) {
        if (x == null) return 0;
        int cmp = key.compareTo(x.key);
        if      (cmp < 0) return key_getDist(x.left, key);
        else if (cmp > 0) return key_getDist(x.right, key);
        else              return x.Dist;
    }

    public int key_getSize(Key key) {
        return key_getSize(root, key);
    }

    private int key_getSize(Node x, Key key) {
        if (x == null) return 0;
        int cmp = key.compareTo(x.key);
        if      (cmp < 0) return key_getSize(x.left, key);
        else if (cmp > 0) return key_getSize(x.right, key);
        else              return x.size;
    }

    public void find_LCA(int A_key,int B_key) {
        if (A_key == 0 || B_key == 0) throw new IllegalArgumentException("argument to floor_modified() is null");
        if (isEmpty()) throw new NoSuchElementException("called floor_modified() with empty symbol table");
        Node x = find_LCA(root, A_key, B_key);
        if (x == null) return;
        else{
            LCA = x;   
            // System.out.print("New LCA: ");
            // System.out.println(LCA.val);
            // return x.key;
        }
    }

    private Node find_LCA(Node root,int A_key,int B_key){
        if(root==null){
            return null;
        }
        if(A_key > root.val && B_key > root.val){
            return find_LCA(root.right, A_key, B_key);
        }
        else if(A_key < root.val && B_key < root.val){
            return find_LCA(root.left, A_key, B_key);
        }
        else{
            return root;
        }
    }

    public int rangeDistSum(int A,int B){
        return rangeDistSum(root, A, B);
    }

    private int rangeDistSum(Node root,int A,int B){
        
        if(root==null) return 0;
        if(root.val<A) return rangeDistSum(root.right, A, B);
        if(root.val>B) return rangeDistSum(root.left, A, B);
        return root.val + rangeDistSum(root.left, A, B) + rangeDistSum(root.right, A, B);
    }
}

// class test{
//     public test(String[] args) {
//         LongJump g;
//         JSONParser jsonParser = new JSONParser();
//         try (FileReader reader = new FileReader("C:\\Users\\BERLIN CHEN\\Desktop\\2022PDSA\\HW6_LongJump_recursive\\LongJump.json")) {
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
//                             break;
//                         case "winnerDistances" : {
//                             testSize++;
//                             Integer t_ans = (int)(long)person.get("answer");
//                             Integer r_ans = g.winnerDistances(Integer.parseInt(arg.get(0).toString()),
//                                     Integer.parseInt(arg.get(1).toString()));
//                             if (t_ans.equals(r_ans)) {
//                                 System.out.println("winnerDistances : AC");
//                             } else {
//                                 waSize++;
//                                 System.out.println("winnerDistances : WA");
//                                 System.out.println("Your answer : "+r_ans);
//                                 System.out.println("True answer : "+t_ans);
//                             }
//                             break;
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