
// import java.io.FileNotFoundException;
// import java.io.FileReader;
// import java.io.IOException;

// import org.json.simple.JSONArray;
// import org.json.simple.JSONObject;
// import org.json.simple.parser.JSONParser;
// import org.json.simple.parser.ParseException;

import java.util.Arrays;
import java.util.Comparator;
import java.util.Stack;
import edu.princeton.cs.algs4.MinPQ;

class King{
    public final Comparator<King> BYSTRENGTH = new byStrength();
    // optional, for reference only  
    int Strength;
    int Range;
    int Index;
    King(int str,int rng, int i){
        Strength=str;
        Range=rng;
        Index=i;
    }
    private class byStrength implements Comparator<King>{
        public int compare(King A,King B){
            if(A.Strength>B.Strength) return +1;
            else if(A.Strength<B.Strength) return -1;
            else{
                if(A.Index<B.Index) return +1;
                else return -1;
            }
        }
    }
}
 
class Kings {

    private int N;
    King A = new King(1, 1, 1);
    private MinPQ<King> KingPQ = new MinPQ<King>(A.BYSTRENGTH);

    public Kings(int[] strength, int[] range){

        N = strength.length;
        int[] AttackBound = warriors_AttackBound(strength, range);
        // for(int i=0;i<AttackBound.length;i++){
        //             System.out.print(AttackBound[i]);
        //             System.out.print(' ');
        // }

        boolean[] Survival = new boolean[N];
        Arrays.fill(Survival,true);
        for(int i=0;i<2*N;i+=2){
            int warriorIndex = i/2;
            int lower = AttackBound[i];
            int upper = AttackBound[i+1];
            for(int j=lower;j<=upper;j++){
                if(j!=warriorIndex){ // the warrior cannot attack itself
                    Survival[j] = false;
                }
            }
        }
        // System.out.println(Arrays.toString(Survival));

        for(int i=0;i<Survival.length;i++){
            if(Survival[i]){
                King newKing = new King(strength[i], range[i], i);
                KingPQ.insert(newKing);
            }
        }

    }
    public int[] topKKings(int k) {
        
        

        while(KingPQ.size()>k){
            KingPQ.delMin();
        }

        int[] topK = new int[Math.min(KingPQ.size(), k)]; 
        int count=1;
        for(King K: KingPQ){
            //System.out.println(K.Index);
            topK[Math.min(KingPQ.size(), k)-count] = K.Index;
            count++;
        }

        // System.out.println(Arrays.toString(topK));

        return topK;  
    }

    public static void displayKings(King[] Kings){
        System.out.println("\n\nIndex / Strength / Range");
        for(King K: Kings){
            System.out.print(K.Index);
            System.out.print("/");
            System.out.print(K.Strength);
            System.out.print("/");
            System.out.println(K.Range);
        }
    }

    public int[] warriors_AttackBound(int[] strength, int[] range) {
        int N = strength.length;
       
        int[] AttackBound = new int[2*N];

        Stack<Integer> forwardStack = new Stack<Integer>();
        int i = 0;
        int this_tail=0;
        int next_head=0;

        while(i<N){
            
            if(i==0){
                forwardStack.push(0);
            }
            else if(i==N-1){
                int end_index = forwardStack.peek();
                while(!forwardStack.isEmpty()){
                    int remain = forwardStack.pop();
                    int upper_bound = Math.min(end_index, remain+range[remain]);
                    AttackBound[2*remain+1] = upper_bound;
                }
                break;
            }

            try{
                if(strength[i+1] < strength[i]){
                    forwardStack.push(i+1);
                    i++;
                }
                else{
                    this_tail = i;
                    next_head = i+1;
                    AttackBound[2*this_tail+1] = this_tail;
                    int last_Strength;
                    while(!forwardStack.isEmpty()){
                        int CD_Index = forwardStack.peek();
                        last_Strength = strength[CD_Index];
                        if(strength[next_head] >= last_Strength){
                            int upper_bound = Math.min(this_tail, CD_Index+range[CD_Index]);
                            AttackBound[2*CD_Index+1] = upper_bound;
                            forwardStack.pop();
                        }
                        else{
                            break;
                        }
                    }
                    forwardStack.push(next_head);
                    i = next_head;
                }
            }catch(Exception e){
                i++;
            }
            
        }

        
        Stack<Integer> InverseStack = new Stack<Integer>();
        int j = N-1;
        int this_head=j;
        int prev_tail=j;

        while(j>=0){
            
            if(j==N-1){
                InverseStack.push(N-1);
            }
            else if(j==0){
                int end_index = InverseStack.peek();
                while(!InverseStack.isEmpty()){
                    int remain = InverseStack.pop();
                    int lower_bound = Math.max(end_index, remain-range[remain]);
                    AttackBound[2*remain] = lower_bound;
                }
                break;
            }

            try{
                if(strength[j-1] <  strength[j]){
                    InverseStack.push(j-1);
                    j--;
                }
                else{
                    this_head = j;
                    prev_tail = j-1;
                    AttackBound[2*this_head] = this_head;
                    int last_Strength;
                    while(!InverseStack.isEmpty()){
                        int CD_Index = InverseStack.peek();
                        last_Strength = strength[CD_Index];
                        if(strength[prev_tail] >= last_Strength){
                            int lower_bound = Math.max(this_head, CD_Index-range[CD_Index]);
                            AttackBound[2*CD_Index] = lower_bound;
                            InverseStack.pop();
                        }
                        else{
                            break;
                        }
                    }
                    InverseStack.push(prev_tail);
                    j = prev_tail;
                }
            }catch(Exception e){
                j--;
            }
        }
        return AttackBound;
    }

    public static void main(String[] args) {

        /* Comparator test
        King A = new King(10,0,1);
        King B = new King(9,0,0);
        King[] KingAB = new King[] {A,B};
        Arrays.sort(KingAB,A.BYSTRENGTH);
        System.out.print("The smaller one: ");
        System.out.println(KingAB[0].Index);
         */

        // Kings sol = new Kings(new int[] {15, 3, 26, 2, 5, 19, 12, 8}
        //                                , new int[] { 1, 6, 1, 3, 2, 0, 1, 5});
        // System.out.println(Arrays.toString(sol.topKKings(3)));
        // In this case, the kings are [0, 2, 4, 5, 6] (without sorting, only by the order of ascending indices)
        // Output: [2, 5, 0]

        // test t = new test(args);

    }
}

// class test{
//     public test(String[] args){
//         Kings sol;
//         JSONParser jsonParser = new JSONParser();
//         try (FileReader reader = new FileReader("C:\\Users\\BERLIN CHEN\\Desktop\\2022PDSA\\HW5_1_TopKKings\\testcase.json")){
//             JSONArray all = (JSONArray) jsonParser.parse(reader);
//             for(Object CaseInList : all){
//                 JSONArray a = (JSONArray) CaseInList;
//                 int q_cnt = 0, wa = 0,ac = 0;
//                 for (Object o : a) {
//                     q_cnt++;
//                     JSONObject person = (JSONObject) o;
//                     JSONArray arg_str = (JSONArray) person.get("strength");
//                     JSONArray arg_rng = (JSONArray) person.get("attack_range");
//                     Long arg_k = (Long) person.get("k");
//                     JSONArray arg_ans = (JSONArray) person.get("answer");
//                     int STH[] = new int[arg_str.size()];
//                     int RNG[] = new int[arg_str.size()];
//                     int k = Integer.parseInt(arg_k.toString());

//                     int Answer[] = new int[arg_ans.size()];
//                     int Answer_W[] = new int[arg_ans.size()];
//                     for(int i=0;i<arg_ans.size();i++){
//                         Answer[i]=(Integer.parseInt(arg_ans.get(i).toString()));
//                     }
//                     for(int i=0;i<arg_str.size();i++){
//                         STH[i]=(Integer.parseInt(arg_str.get(i).toString()));
//                         RNG[i]=(Integer.parseInt(arg_rng.get(i).toString()));
//                     }
//                     sol = new Kings(STH,RNG);
//                     Answer_W = sol.topKKings(k);
//                     for(int i=0;i<arg_ans.size();i++){
//                         if(Answer_W[i]==Answer[i]){
//                             if(i==arg_ans.size()-1){
//                                 System.out.println(q_cnt+": AC");
//                             }
//                         }else {
//                             wa++;
//                             System.out.println(q_cnt+": WA");
//                             break;
//                         }
//                     }

//                 }
//                 System.out.println("Score: "+(q_cnt-wa)+"/"+q_cnt);

//             }
//         }catch (FileNotFoundException e) {
//             e.printStackTrace();
//         } catch (IOException e) {
//             e.printStackTrace();
//         } catch (ParseException e) {
//             e.printStackTrace();
//         }
//     }
// }