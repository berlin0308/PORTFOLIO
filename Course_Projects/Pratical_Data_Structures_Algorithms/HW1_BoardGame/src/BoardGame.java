import edu.princeton.cs.algs4.WeightedQuickUnionUF;
import java.util.*;

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
        //Arrays.fill(Board,null);
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
        /* char opposite = ' ';
        if(getStoneType(x, y)=='O')
            opposite = 'X';
        else if(getStoneType(x, y)=='X')
            opposite = 'O';
 */
        char type = getStoneType(x, y); 
        int member_x;
        int member_y;
        for(int id=0;id<x_max*y_max;id++){
            if(Board[id]==type){
            
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
    }
    public static void main(String args[]){ 
        /* BoardGame g = new BoardGame(3,3); 
        g.showBoardGame();

        g.putStone(new int[]{1}, new int[]{1}, 'O');
        System.out.println(g.surrounded(1, 1));
        System.out.println(g.countConnectedRegions());
        g.showBoardGame();

        g.putStone(new int[]{0,1,1}, new int[]{1,0,2}, 'X');
        System.out.println(g.surrounded(1, 1));
        System.out.println(g.countConnectedRegions());
        g.showBoardGame();
        

        g.putStone(new int[]{2},new int[]{1}, 'X');
        System.out.println(g.surrounded(1, 1));
        System.out.println(g.surrounded(2, 1)); 
        System.out.println(g.countConnectedRegions()); 
        g.showBoardGame();


        g.putStone(new int[]{2}, new int[]{0}, 'O');
        System.out.println(g.surrounded(2, 0)); 
        System.out.println(g.countConnectedRegions());
        g.showBoardGame(); */
  
    }
}