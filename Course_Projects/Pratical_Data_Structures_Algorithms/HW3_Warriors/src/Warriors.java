import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import java.util.Arrays;
import java.util.List;
import java.util.Comparator;

class EachWarrior{
    private int Strength;
    private int Range;
    private int Index;
    public EachWarrior(int str,int rng, int i){
        Strength=str;
        Range=rng;
        Index=i;
    }
    public int getStrength(){
        return Strength;
    }
    public int getIndex(){
        return Index;
    }
    public int getRange(){
        return Range;
    }
}

class Warriors {
    
    static EachWarrior[] WarriorsInfo;
    static int[] AttackBound; 

    public int[] warriors(int[] strength, int[] range) {
        int N = strength.length;
        // read attributes of each Warrior
        WarriorsInfo = new EachWarrior[N];
        for(int i=0;i<N;i++){
            EachWarrior E = new EachWarrior(strength[i],range[i],i);
            WarriorsInfo[i] = E;
        }
        // sort the array by strength
        List<EachWarrior> WarriorsInfoList = Arrays.asList(WarriorsInfo);
        WarriorsInfoList.sort(Comparator.comparing(EachWarrior::getStrength).thenComparing(EachWarrior::getIndex));
        
        AttackBound = new int[2*N];

        showWarriorsInfo();
        int bound_lower;
        int bound_upper;
        for(int i=0;i<N;i++){
            int pos_i = WarriorsInfo[i].getIndex();
            bound_lower = 0;
            bound_upper = N-1;

            for(int j=i+1;j<N;j++){ // Warriors with higher Strength than this 
                int pos_j = WarriorsInfo[j].getIndex();
                //System.out.println(pos_j);
                
                if(pos_j>pos_i && pos_j<=bound_upper){
                    bound_upper=pos_j-1;
                }
                if(pos_j<pos_i && pos_j>=bound_lower){
                    bound_lower=pos_j+1;
                }
            } 
            
            try{
                if(WarriorsInfo[i-1].getStrength()==WarriorsInfo[i].getStrength()){
                    int pos_j = WarriorsInfo[i-1].getIndex()+1;
                    // if(pos_j>pos_i && pos_j<bound_upper) bound_upper=pos_j;
                    if(pos_j<=pos_i && pos_j>bound_lower) bound_lower=pos_j;
                }
                
            }catch(Exception e){
            // System.out.println(e);
            }

            try{
                if(WarriorsInfo[i+1].getStrength()==WarriorsInfo[i].getStrength()){
                    int pos_j = WarriorsInfo[i+1].getIndex()-1;
                    if(pos_j>=pos_i && pos_j<bound_upper) bound_upper=pos_j;
                    // if(pos_j<pos_i && pos_j>bound_lower) bound_lower=pos_j;
                }
                
            }catch(Exception e){
                //System.out.println(e);
            }

            // System.out.println("--------");
            // System.out.println(bound_upper);
            // System.out.println(bound_lower);
            
            // find upper bound
            int bound_max = Math.min(bound_upper, pos_i+WarriorsInfo[i].getRange());
            
            // find lower bound
            int bound_min = Math.max(bound_lower, pos_i-WarriorsInfo[i].getRange());
            
            // System.out.println(pos_i+WarriorsInfo[i].getRange());
            // System.out.println(pos_i-WarriorsInfo[i].getRange());
            
            // System.out.println(bound_max);
            // System.out.println(bound_min);
            
            AttackBound[pos_i*2] = bound_min;
            AttackBound[pos_i*2+1] = bound_max;
    }
        //showAttackBound();
        
        return AttackBound; // complete the code by returning an int[]
    }


    public static void showWarriorsInfo(){
        System.out.println("Strength / Index / Range");
        for(EachWarrior E : WarriorsInfo){
            System.out.print(E.getStrength());
            System.out.print("  /  ");
            System.out.print(E.getIndex());
            System.out.print("  /  ");
            System.out.println(E.getRange());
            
        }
    }

    public static void showAttackBound(){
        for(int i=0;i<AttackBound.length;i++){
            System.out.print(AttackBound[i]);
            System.out.print(' ');
        }
        System.out.println("-------");
    }
    public static void main(String[] args) {
        test t = new test(args);
    }
}

class test{
    public test(String[] args){
        Warriors sol = new Warriors();
        JSONParser jsonParser = new JSONParser();
        try (FileReader reader = new FileReader("C:\\Users\\BERLIN CHEN\\Desktop\\2022PDSA\\HW3_Warriors\\warriors.json")){
            JSONArray all = (JSONArray) jsonParser.parse(reader);
            for(Object CaseInList : all){
                JSONArray a = (JSONArray) CaseInList;
                int q_cnt = 0, wa = 0,ac = 0;
                for (Object o : a) {
                    q_cnt++;
                    JSONObject person = (JSONObject) o;
                    JSONArray arg_str = (JSONArray) person.get("strength");
                    JSONArray arg_rng = (JSONArray) person.get("attack_range");
                    JSONArray arg_ans = (JSONArray) person.get("answer");
                    int STH[] = new int[arg_str.size()];
                    int RNG[] = new int[arg_str.size()];
                    int Answer[] = new int[arg_ans.size()];
                    int Answer_W[] = new int[arg_ans.size()];
                    for(int i=0;i<arg_ans.size();i++){
                        Answer[i]=(Integer.parseInt(arg_ans.get(i).toString()));
                        if(i<arg_str.size()){
                            STH[i]=(Integer.parseInt(arg_str.get(i).toString()));
                            RNG[i]=(Integer.parseInt(arg_rng.get(i).toString()));
                        }
                    }
                    Answer_W = sol.warriors(STH,RNG);
                    for(int i=0;i<arg_ans.size();i++){
                        if(Answer_W[i]==Answer[i]){
                            if(i==arg_ans.size()-1){
                                System.out.println(q_cnt+": AC");
                            }
                        }else {
                            wa++;
                            System.out.println(q_cnt+": WA");
                            break;
                        }
                    }

                }
                System.out.println("Score: "+(q_cnt-wa)+"/"+q_cnt);

            }
        }catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (ParseException e) {
            e.printStackTrace();
        }
    }
}