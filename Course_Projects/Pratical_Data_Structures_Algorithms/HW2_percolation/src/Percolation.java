import edu.princeton.cs.algs4.Merge;
import edu.princeton.cs.algs4.Point2D;
import edu.princeton.cs.algs4.WeightedQuickUnionUF;
import java.util.*;


class Percolation {

   private int size;
   private int top_id;
   private int bottom_id;
   WeightedQuickUnionUF PointsUF;
   private boolean[][] OpenPoints;
   List<Integer> OpenPoints_id;
   List<Integer> OpenButtomPoints_id;
   List<Point2D> PercoPoints;
   private boolean RECORDED = false;

   //  private static class Node {
   //      private Point2D site;
   //      private Node next;
   //  }
   
   public Percolation(int N)               // create N-by-N grid, with all sites blocked
   {
      size = N;
      top_id = 0;
      bottom_id = size*size+1;
      PointsUF = new WeightedQuickUnionUF(size*size+2); // [0][0] -> id:1
      OpenPoints = new boolean[size][size];
      OpenPoints_id = new ArrayList<>();
      OpenButtomPoints_id = new ArrayList<>();
      PercoPoints = new ArrayList<>();
   }
   public void open(int i, int j)          // open site (row i, column j) if it is not open already
   {
      OpenPoints[i][j] = true;
      int open_id = i*size+j+1;
      OpenPoints_id.add(open_id);

      if(i==0) // top virtual node
         PointsUF.union(open_id, top_id);

      if(i==size-1) // buttom points
         OpenButtomPoints_id.add(open_id);
         
      try{
         if(i!=0 && isOpen(i-1, j)){ // up
            PointsUF.union(UF_index(i, j),UF_index(i-1, j));
         }
         if(i!=size-1 && isOpen(i+1, j)){ // down
            PointsUF.union(UF_index(i, j),UF_index(i+1, j));
         }
         if(j!=0 && isOpen(i, j-1)){ // left
            PointsUF.union(UF_index(i, j),UF_index(i, j-1));
         }
         if(j!=size-1 && isOpen(i, j+1)){ // right
            PointsUF.union(UF_index(i, j),UF_index(i, j+1));
         }
      }catch(Exception e){
         System.out.print(e);
      }

      for(int id : OpenButtomPoints_id){
         if(PointsUF.find(top_id)==PointsUF.find(id))
            PointsUF.union(id, bottom_id);
      }
      
      if(!RECORDED){
         if(percolates()){
            for(int id : OpenPoints_id){
               if(PointsUF.find(id)==PointsUF.find(top_id)){
                  int x = (id-1)/size;
                  int y = (id-1)%size;
                  Point2D point = new Point2D(x, y);
                  PercoPoints.add(point);
                  RECORDED = true;

               }
            }
         }

      }
      

      // if(isFull(i,j) && !RECORDED){
      //    Point2D fullpoint = new Point2D(i, j);
      //    PercoPoints.add(fullpoint);
      //    if(percolates()){
      //       RECORDED = true;
      //    }
      // }

   }
      
   public boolean isOpen(int i, int j)     // is site (row i, column j) open?
   {
      return OpenPoints[i][j];
   }
   
   public boolean isFull(int i, int j)     // is site (row i, column j) full?
   {
      return PointsUF.find(top_id)==PointsUF.find(UF_index(i, j));
   }
   
   public boolean percolates()             // does the system percolate?
   {
      return PointsUF.find(top_id)==PointsUF.find(bottom_id);
   }
   

   public Point2D[] PercolatedRegion()     // return the array of the sites of the percolated region in order (using Point2D default compare.to) 
   {                                        // This function should always return the content of the percolated region AT THE MOMENT when percolation just happened.
      // List to Array 
      Point2D[] PercoPointsArray = new Point2D[PercoPoints.size()];
      PercoPoints.toArray(PercoPointsArray);
      Merge.sort(PercoPointsArray);

      return PercoPointsArray;
   }

   public void showBoard(){

      System.out.print('\n'); 
      for(int i=0;i<size;i++){
          for(int j=0;j<size;j++){
              if(OpenPoints[i][j]==true)
                  System.out.print('O'); 
              else
                  System.out.print('.');
              System.out.print(' '); 
          }
          System.out.print('\n'); 
      }
  }

  public int UF_index(int i,int j){
      return i*size+j+1;
  }
 
   
   public static void main(String[] args) {
      // Percolation s = new Percolation(3);
      // s.open(1,1);
      // System.out.println(s.isFull(1, 1));
      // System.out.println(s.percolates());
      // s.open(0,1);
      // s.open(2,0);
      // System.out.println(s.isFull(1, 1));
      // System.out.println(s.isFull(0, 1));
      // System.out.println(s.isFull(2, 0));
      // System.out.println(s.percolates());
      // s.open(2,1);
      // System.out.println(s.isFull(1, 1));
      // System.out.println(s.isFull(0, 1));
      // System.out.println(s.isFull(2, 0));
      // System.out.println(s.isFull(2, 1));
      // System.out.println(s.percolates());

      // Point2D[] pr = s.PercolatedRegion();
      // for (int i = 0; i < pr.length; i++) {
      //    System.out.println("("+(int)pr[i].x() + "," + (int)pr[i].y()+")");
      // }

   }
}