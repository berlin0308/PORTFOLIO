import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

import edu.princeton.cs.algs4.WeightedQuickUnionUF;
import java.util.*;
 
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

class BoardGame {

    private char[] Board;
    private int x_max;
    private int y_max;
    WeightedQuickUnionUF uf;

    public BoardGame(int h, int w) // create a board of size h*w
    {
        x_max = h;
        y_max = w;
        Board = new char[h*w];
        //Arrays.fill(Board,' ');
        uf = new WeightedQuickUnionUF(h*w);
    }

    public void putStone(int[] x, int[] y, char stoneType) // put stones of the specified type on the board according to the coordinates
    {
        for(int i=0;i<x.length;i++){
            int X = x[i];
            int Y =y[i];
            Board[X*y_max+Y] = stoneType; // change the stone on the Board
            try{
                if(Board[(X-1)*y_max+Y]==stoneType){
                    uf.union(X*y_max+Y,(X-1)*y_max+Y);
                }
            }catch(Exception ArrayIndexOutOfBoundsException){
                }

            try{
                if(Board[(X+1)*y_max+Y]==stoneType){
                    uf.union(X*y_max+Y,(X+1)*y_max+Y);
                }
            }catch(Exception ArrayIndexOutOfBoundsException){
            }
            
            try{
            if(Board[(X)*y_max+(Y-1)]==stoneType){
                uf.union(X*y_max+Y,(X)*y_max+(Y-1));
            }
            }catch(Exception ArrayIndexOutOfBoundsException){
            }

            try{
            if(Board[(X)*y_max+(Y+1)]==stoneType){
                uf.union(X*y_max+Y,(X)*y_max+(Y+1));
            }
            }catch(Exception ArrayIndexOutOfBoundsException){    
            }
        }
    }
    public boolean surrounded(int x, int y) // Answer if the stone and its connected stones are surrounded by another type of stones
    {
        boolean Surrounded = true;
        int union_root = uf.find(x*y_max+y);
        char type = getStoneType(x, y); 

        /* char opposite = ' ';
        if(getStoneType(x, y)=='O')
            opposite = 'X';
        else if(getStoneType(x, y)=='X')
            opposite = 'O';
 */
        int member_x;
        int member_y;
        for(int id=0;id<x_max*y_max;id++){
        if(Board[id]!=type)
            break;
        if(uf.find(id)==union_root){ // for union members
         //System.out.println("id:"+id);
        try{
             member_x = id/y_max;
             member_y = id%y_max;
             //System.out.println("x,y: "+member_x+","+member_y);

             if(member_x==0 || member_x==x_max-1 || member_y==0 || member_y==y_max-1){
                 Surrounded = false;
                 break;
             }
             if(getStoneType(member_x-1, member_y)=='\u0000' || getStoneType(member_x+1, member_y)=='\u0000'
             || getStoneType(member_x, member_y-1)=='\u0000' || getStoneType(member_x, member_y+1)=='\u0000'){ 
                 Surrounded = false;
                 break;
             }

         }catch(Exception ArrayIndexOutOfBoundsException){
             //System.out.print("\n\nException!!!\n\n"); 
             Surrounded = false;
             break;
         }
    }

   }
        //System.out.println("If ("+x+","+y+") Surrounded:"+Surrounded);
        return Surrounded;
    }
    
    public char getStoneType(int x, int y) // Get the type of the stone at (x,y)
    {
        return Board[x*y_max+y];
    }
    
    public int countConnectedRegions() // Get the number of connected regions in the board, including both types of the stones
    {
        List<Integer> rootList = new ArrayList<>();
        for(int id=0;id<x_max*y_max;id++){
            if(Board[id]=='O'||Board[id]=='X'){
                if(!rootList.contains(uf.find(id)))
                    rootList.add(uf.find(id));
            }
        }
        return rootList.size();
    }

    public void showBoardGame(){

        System.out.println(""); 
        for(int i=0;i<x_max;i++){
            for(int j=0;j<y_max;j++){
                if(Board[i*y_max+j]!='O' && Board[i*y_max+j]!='X')
                System.out.print("."); 
                else
                System.out.print(Board[i*y_max+j]); 
                
                System.out.print(" "); 
            }
            System.out.print("\n"); 
        }
        System.out.println(""); 
    }



    public static void test(String[] args){
        BoardGame g;
        JSONParser jsonParser = new JSONParser();
        try (FileReader reader = new FileReader("C:\\Users\\BERLIN CHEN\\Desktop\\2022PDSA\\HW1_BoardGame_TestCode\\BoardGame.json")){ //args[0])){
            JSONArray all = (JSONArray) jsonParser.parse(reader);
            int count = 0;
            for(Object CaseInList : all){
                count++;
                JSONArray a = (JSONArray) CaseInList;
                int testSize = 0; int waSize = 0;
                System.out.print("Case ");
                System.out.println(count);
                //Board Setup
                JSONObject argsSeting = (JSONObject) a.get(0);
                a.remove(0);

                JSONArray argSettingArr = (JSONArray) argsSeting.get("args");
                g = new BoardGame(
                        Integer.parseInt(argSettingArr.get(0).toString())
                        ,Integer.parseInt(argSettingArr.get(1).toString()));

                for (Object o : a)
                {
                    JSONObject person = (JSONObject) o;

                    String func =  person.get("func").toString();
                    JSONArray arg = (JSONArray) person.get("args");


                    g.showBoardGame();
                    switch(func){
                        case "putStone":
                            int xArray[] = JSONArraytoIntArray((JSONArray) arg.get(0));
                            int yArray[] = JSONArraytoIntArray((JSONArray) arg.get(1));
                            String stonetype =  (String) arg.get(2);

                            g.putStone(xArray,yArray,stonetype.charAt(0));
                            break;
                        case "surrounded":
                            Boolean answer = (Boolean) person.get("answer");
                            testSize++;
                            System.out.print(testSize + ": " + func + " / ");
                            Boolean ans = g.surrounded(
                                    Integer.parseInt(arg.get(0).toString()),
                                    Integer.parseInt(arg.get(1).toString())
                            );
                            if(ans==answer){
                                System.out.println("AC");
                            }else{
                                waSize++;
                                System.out.println("WA");
                            }
                            break;
                        case "countConnectedRegions":
                            testSize++;
                            int ans2 = Integer.parseInt(arg.get(0).toString());
                            int ansCR = g.countConnectedRegions();
                            System.out.print(testSize + ": " + func + " / ");
                            if(ans2==ansCR){
                                System.out.println("AC");
                            }else{
                                waSize++;
                                System.out.println("WA");
                            }
                    }

                }
                System.out.println("Score: " + (testSize-waSize) + " / " + testSize + " ");
            }
        }catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (ParseException e) {
            e.printStackTrace();
        }
    }

    public static int[] JSONArraytoIntArray(JSONArray x){
        int sizeLim = x.size();
        int MyInt[] = new int[sizeLim];
        for(int i=0;i<sizeLim;i++){
            MyInt[i]= Integer.parseInt(x.get(i).toString());
        }
        return MyInt;
    }

    public static void main(String[] args) {//mian
        test(args);
    }

}
