
// import org.json.simple.JSONArray;
// import org.json.simple.JSONObject;
// import org.json.simple.parser.JSONParser;
// import org.json.simple.parser.ParseException;

// import java.io.FileNotFoundException;
// import java.io.FileReader;
// import java.io.IOException;

import java.util.NoSuchElementException;
import edu.princeton.cs.algs4.Queue;

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
 * 
 * 11/13 13:30-17:00
 * rangeDistSum()
 * left/right subtree Dist
 * Dist-Recursive hybrid
 * AutoLab 100.0
 * 
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
        // LongJump solution = new LongJump(new int[]{3,2,4,8,6,5,7,11,10,9,13,12});
        // solution.displayBST();
        
        // System.out.println(solution.winnerDistances(6,12));
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
        root = put(root, key, val);
    }

    private Node put(Node x, Key key, int val) {
        if (x == null) return new Node(key, val, 1,val);
        int cmp = key.compareTo(x.key);
        if      (cmp < 0) x.left  = put(x.left,  key, val);
        else if (cmp > 0) x.right = put(x.right, key, val);
        else              x.val   = val;
        x.size = 1 + size(x.left) + size(x.right);
        x.Dist = x.val+ getDist(x.left) + getDist(x.right);
        return x;
    }

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
    
    public int rangeDistSum(int A,int B){
        return rangeDistSum(root, A, B, B);
    }

    private int rangeDistSum(Node root,int A,int B,int upper){
        if(root!=null)
        {
            // System.out.print("current root: ");
            // System.out.println(root.val);
            // System.out.print("upper: ");
            // System.out.println(upper);
        }
        if(root==null) return 0;
        if(root.val<A) return rangeDistSum(root.right, A, B,root.val);
        else if(root.val>B) return rangeDistSum(root.left, A, B,root.val);
        else{
            if(upper<root.val && upper > A && root.val < B){
                // System.out.print("\n--Dist approach--\n");
                if(root.left!=null){
                    // System.out.print("left tree root: ");
                    // System.out.println(root.left.val);
                    // System.out.print("left tree Dist: ");
                    // System.out.println(root.left.Dist);
                    return root.val + root.left.Dist + rangeDistSum(root.right, A, B,root.val);
                }
                else{
                    return root.val + rangeDistSum(root.right, A, B,root.val);
                }
            }else if(upper>root.val && upper < B && root.val > A){
                // System.out.print("\n--Dist approach--\n");
                if(root.right!=null){
                    // System.out.print("right tree root: ");
                    // System.out.println(root.right.val);
                    // System.out.print("right tree Dist: ");
                    // System.out.println(root.right.Dist);
                    return root.val + root.right.Dist + rangeDistSum(root.left, A, B,root.val);
                }
                else{
                    return root.val + rangeDistSum(root.left, A, B,root.val);
                }

            }else{
                // System.out.println("\n--Recursive Search approach--\n");
                return root.val + rangeDistSum(root.left, A, B,root.val) + rangeDistSum(root.right, A, B,root.val);
            }
        }
    }
}

// class test{
//     public test(String[] args) {
//         LongJump g;
//         JSONParser jsonParser = new JSONParser();
//         try (FileReader reader = new FileReader("C:\\Users\\BERLIN CHEN\\Desktop\\2022PDSA\\HW6_LongJump_Dist_Rec\\LongJump.json")) {
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
