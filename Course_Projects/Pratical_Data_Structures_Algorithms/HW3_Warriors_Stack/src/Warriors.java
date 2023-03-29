// import java.io.FileNotFoundException;
// import java.io.FileReader;
// import java.io.IOException;

// import org.json.simple.JSONArray;
// import org.json.simple.JSONObject;
// import org.json.simple.parser.JSONParser;
// import org.json.simple.parser.ParseException;

import edu.princeton.cs.algs4.Stack;
import java.util.Arrays;

class Warriors {
    
    static int[] AttackBound; 

    public int[] warriors(int[] strength, int[] range) {
        int N = strength.length;
       
        AttackBound = new int[2*N];

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
        Warriors sol = new Warriors();
        System.out.println(Arrays.toString(
            sol.warriors(new int[] {11, 13, 11, 7, 15},
            new int[] { 1,  8,  1, 7,  2})));
            // test t= new test(args);
        }
    
    
        // public void showWarriorsInfo(){
        //     System.out.println(" Index / Strength / Range");
        //     for(EachWarrior E : WarriorsInfo){
        //         System.out.print(E.getIndex());
        //         System.out.print("  /  ");
        //         System.out.print(E.getStrength());
        //         System.out.print("  /  ");
        //         System.out.println(E.getRange());
        //     }
        // }
    
        // public void showAttackBound(){
        //     for(int i=0;i<AttackBound.length;i++){
        //         System.out.print(AttackBound[i]);
        //         System.out.print(' ');
        //     }
        //     System.out.println("-------");
        // }
    }
    
// class test{
//     public test(String[] args){
//         Warriors sol = new Warriors();
//         JSONParser jsonParser = new JSONParser();
//         try (FileReader reader = new FileReader("C:\\Users\\BERLIN CHEN\\Desktop\\2022PDSA\\HW3_Warriors\\warriors.json")){
//             JSONArray all = (JSONArray) jsonParser.parse(reader);
//             for(Object CaseInList : all){
//                 JSONArray a = (JSONArray) CaseInList;
//                 int q_cnt = 0, wa = 0,ac = 0;
//                 for (Object o : a) {
//                     q_cnt++;
//                     JSONObject person = (JSONObject) o;
//                     JSONArray arg_str = (JSONArray) person.get("strength");
//                     JSONArray arg_rng = (JSONArray) person.get("attack_range");
//                     JSONArray arg_ans = (JSONArray) person.get("answer");
//                     int STH[] = new int[arg_str.size()];
//                     int RNG[] = new int[arg_str.size()];
//                     int Answer[] = new int[arg_ans.size()];
//                     int Answer_W[] = new int[arg_ans.size()];
//                     for(int i=0;i<arg_ans.size();i++){
//                         Answer[i]=(Integer.parseInt(arg_ans.get(i).toString()));
//                         if(i<arg_str.size()){
//                             STH[i]=(Integer.parseInt(arg_str.get(i).toString()));
//                             RNG[i]=(Integer.parseInt(arg_rng.get(i).toString()));
//                         }
//                     }
//                     Answer_W = sol.warriors(STH,RNG);
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