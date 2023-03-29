//use one WQUUF to avoid backwash
import edu.princeton.cs.algs4.Merge;
import edu.princeton.cs.algs4.Point2D;
import edu.princeton.cs.algs4.WeightedQuickUnionUF;
import java.util.*;
class Percolation {  
    private boolean[] open; //blocked: false, open: true
    private boolean[] connectTop;
    private boolean[] connectBottom;
    private int N; //create N-by-N grid
    private WeightedQuickUnionUF uf; 
    private boolean percolateFlag;
    List<Point2D> PercoPoints;
    List<Integer> OpenPoints_id;
    private boolean RECORDED;
  
    public Percolation(int N)  {             // create N-by-N grid, with all sites blocked
        if (N <= 0) {
            throw new IllegalArgumentException("N must be bigger than 0");
        } 
         this.N = N;
         uf = new WeightedQuickUnionUF(N*N);
         open = new boolean[N*N];  
         connectTop = new boolean[N*N];  
         connectBottom = new boolean[N*N];  
      
         for (int i = 0; i < N*N; i++) {
             open[i] = false;
             connectTop[i] = false;
             connectBottom[i] = false;
         } 
         percolateFlag = false;
         PercoPoints = new ArrayList<>();
         OpenPoints_id = new ArrayList<>();
         RECORDED = false;
        }
     
    public void open(int i, int j)  {        // open site (row i, column j) if it is not open already
        i++;
        j++;
        validateIJ(i, j); 
        int index = xyTo1D(i, j);
        OpenPoints_id.add(index);
        open[index] = true;  //open
        boolean top = false;
        boolean bottom = false;
       
        if (i < N && open[index+N]) {
            if (connectTop[uf.find(index+N)] || connectTop[uf.find(index)] ) {   
                 top = true;
            }
            if (connectBottom[uf.find(index+N)] || connectBottom[uf.find(index)] ) {   
                 bottom = true;
            }
             uf.union(index, index+N);
        }
        if (i > 1 && open[index-N]) {
            if (connectTop[uf.find(index-N)] || connectTop[uf.find(index)] ) {   
                 top = true;
            }
            if (connectBottom[uf.find(index-N)] || connectBottom[uf.find(index)] ) {   
                 bottom = true;
            }
             uf.union(index, index-N);
        }
        if (j < N && open[index+1]) {
            if (connectTop[uf.find(index+1)] || connectTop[uf.find(index)] ) {   
                 top = true;
            }
            if (connectBottom[uf.find(index+1)] || connectBottom[uf.find(index)] ) {   
                 bottom = true;
            }
             uf.union(index, index+1);
        }
        if (j > 1 && open[index-1]) {
            if (connectTop[uf.find(index-1)] || connectTop[uf.find(index)] ) {   
                 top = true;
            }
            if (connectBottom[uf.find(index-1)] || connectBottom[uf.find(index)] ) {   
                 bottom = true;
            }
             uf.union(index, index-1);
        }
        if(i == 1) {
            top = true;
        }
        if(i == N){
            bottom = true;
        }
        connectTop[uf.find(index)] = top;
        connectBottom[uf.find(index)] = bottom;
        if( connectTop[uf.find(index)] &&  connectBottom[uf.find(index)]) {
            percolateFlag = true;
        }

        if(!RECORDED){
            if(percolateFlag){
               for(int id : OpenPoints_id){
                  if(uf.find(id)==uf.find(xyTo1D(i, j))){
                     int x = (id)/N;
                     int y = (id)%N;
                     Point2D point = new Point2D(x, y);
                     PercoPoints.add(point);
                     RECORDED = true;
                  }
               }
            }
   
         }
    }
    
    private int xyTo1D(int i, int j) {
        validateIJ(i, j);
        return j + (i-1) * N -1;
    }
    
    private void validateIJ(int i, int j) {
        if (!(i >= 1 && i <= N && j >= 1 && j <= N)) {
            throw new IndexOutOfBoundsException("Index is not betwwen 1 and N");
        }
    }
    
    public boolean isOpen(int i, int j) {     // is site (row i, column j) open?
      i++;
      j++;
        validateIJ(i, j);
        return open[xyTo1D(i, j)];
    }
    
    /*A full site is an open site that can be connected to an open site in the top row 
     * via a chain of neighboring (left, right, up, down) open sites. 
    */
    public boolean isFull(int i, int j) {    // is site (row i, column j) full?
      i++;
      j++;
      validateIJ(i, j);
        return connectTop[uf.find(xyTo1D(i, j))];
    }
    
    /* Introduce 2 virtual sites (and connections to top and bottom). 
     * Percolates iff virtual top site is connected to virtual bottom site.
     */
    public boolean percolates()  {           // does the system percolate? 
        return percolateFlag;
    }
    
    public Point2D[] PercolatedRegion()     // return the array of the sites of the percolated region in order (using Point2D default compare.to) 
    {                                        // This function should always return the content of the percolated region AT THE MOMENT when percolation just happened.
       // List to Array 
       Point2D[] PercoPointsArray = new Point2D[PercoPoints.size()];
       PercoPoints.toArray(PercoPointsArray);
 
       // Arrays.sort(PercoPointsArray,Point2D.Y_ORDER);
       Merge.sort(PercoPointsArray);
 
       return PercoPointsArray;
    }

    

   public static void main(String[] args) {
    //   Percolation s = new Percolation(3);
    //     s.open(1,1);
    //     System.out.println(s.isFull(1, 1));
    //     System.out.println(s.percolates());
    //     s.open(0,1);
    //     s.open(2,0);
    //     System.out.println(s.isFull(1, 1));
    //     System.out.println(s.isFull(0, 1));
    //     System.out.println(s.isFull(2, 0));
    //     System.out.println(s.percolates());
    //     s.open(2,1);
    //     System.out.println(s.isFull(1, 1));
    //     System.out.println(s.isFull(0, 1));
    //     System.out.println(s.isFull(2, 0));
    //     System.out.println(s.isFull(2, 1));
    //     System.out.println(s.percolates());
    //     Point2D[] pr = s.PercolatedRegion();
    //     for (int i = 0; i < pr.length; i++) {
    //        System.out.println("("+(int)pr[i].x() + "," + (int)pr[i].y()+")");
    //     }

   }
}