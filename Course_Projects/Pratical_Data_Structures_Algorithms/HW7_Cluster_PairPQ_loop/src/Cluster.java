// import org.json.simple.JSONArray;
// import org.json.simple.JSONObject;
// import org.json.simple.parser.JSONParser;
// import org.json.simple.parser.ParseException;

// import java.io.FileNotFoundException;
// import java.io.FileReader;
// import java.io.IOException;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Comparator;
import java.lang.Math;

import edu.princeton.cs.algs4.MinPQ;
// import edu.princeton.cs.algs4.Point2D;


class ClusterPair{
    public final Comparator<ClusterPair> BYNEARESTDIST = new byNearestDist();
    public int Index_A;
    public int Index_B;
    public double nearest_dist;

    ClusterPair(int a,int b,double d){
        Index_A = a;
        Index_B = b;
        nearest_dist = d;
    }
    
    private class byNearestDist implements Comparator<ClusterPair>{
        public int compare(ClusterPair A,ClusterPair B){
            if(A.nearest_dist>B.nearest_dist) return 1;
            else return -1;
        }
    }
    
}

class Cluster {
    MinPQ<ClusterPair> ClusterPairPQ;
    ArrayList<Point2D> Points;
    ArrayList<Integer> Weights; 

    public List<double[]> cluster(List<int[]> p, int cluster_num) {
        ClusterPairPQ = new MinPQ<ClusterPair>(new ClusterPair(0, 0, 0).BYNEARESTDIST);
        Points = new ArrayList<Point2D>(); // all points including invalid, new centroids
        Weights = new ArrayList<Integer>();

        for(int i=0;i<p.size();i++){
            Points.add(new Point2D(p.get(i)[0],p.get(i)[1]));
            Weights.add(1);

            for(int j=i+1;j<p.size();j++){
                double dist = Math.sqrt(Math.pow(p.get(i)[0]-p.get(j)[0], 2)+Math.pow(p.get(i)[1]-p.get(j)[1], 2));
                ClusterPairPQ.insert(new ClusterPair(i, j,dist));
            }
        }
        // for(int w: Weights){
        //     System.out.println(w);
        // }

        // System.out.println("\n\nPoints: "+p.size());
        // System.out.println("\n\nInitial");
        // for(Point2D P : Points){
        //     if(P==null) continue;
        //     System.out.println(P.toString());
            
        // }
        
        // Clustering(ClusterPairPQ, p.size(), cluster_num);
        // displayPQ(ClusterPairPQ);
        
        int K = p.size();
        while(K>cluster_num){
            ClusterPair NearestPair = ClusterPairPQ.delMin();
            if(NearestPair!=null && (Points.get(NearestPair.Index_A)!=null && Points.get(NearestPair.Index_B)!=null)){ // both are valid
                K--;

                int C_Weight = Weights.get(NearestPair.Index_A) + Weights.get(NearestPair.Index_B);
                Point2D C_Point = new Point2D((Points.get(NearestPair.Index_A).x()*Weights.get(NearestPair.Index_A)+Points.get(NearestPair.Index_B).x()*Weights.get(NearestPair.Index_B))/(Weights.get(NearestPair.Index_A)+Weights.get(NearestPair.Index_B))
                ,(Points.get(NearestPair.Index_A).y()*Weights.get(NearestPair.Index_A)+Points.get(NearestPair.Index_B).y()*Weights.get(NearestPair.Index_B))/(Weights.get(NearestPair.Index_A)+Weights.get(NearestPair.Index_B)));
                
                // System.out.println("NearestPair.Index_A: "+NearestPair.Index_A);
                // System.out.println("NearestPair.Index_B: "+NearestPair.Index_B);
                // System.out.println("New Centroid: "+C_Point.toString());
                
                Points.set(NearestPair.Index_A, null);
                Points.set(NearestPair.Index_B, null);
                Weights.add(C_Weight);
                Points.add(C_Point);
                
                // System.out.println("Points size: "+Points.size());
                for(int i=0;i<Points.size()-1;i++){
                    if(Points.get(i)==null) continue;
                    double dist = Math.sqrt(Math.pow(Points.get(i).x()-C_Point.x(), 2)+Math.pow(Points.get(i).y()-C_Point.y(), 2));
                    ClusterPair NewPair = new ClusterPair(i, Points.size()-1, dist);
                    ClusterPairPQ.insert(NewPair);
                
                }
                
            }else{
                // System.out.println("Invalid, ignore: "+NearestPair.Index_A+" & "+NearestPair.Index_B);
                
            }

        }



        ArrayList<double[]> ans = new ArrayList<double[]>();
        MinPQ<Point2D> Centroids = new MinPQ<Point2D>(Point2D.X_then_Y_ORDER);
        // System.out.println("\n\n\n-----\nClustered Centroid: ");
        for(Point2D P : Points){
            if(P==null) ; //System.out.println("null");
            else{
                Centroids.insert(P);
            }
        }
        while(!Centroids.isEmpty()){
            Point2D P = Centroids.delMin();
            ans.add(new double[]{P.x(),P.y()});
            // System.out.println("( "+P.x()+" , "+P.y()+" )");
        }
        return ans;
    }
    
   
    // public void displayPQ(MinPQ<ClusterPair> PQ){
    //     System.out.println("-----\ndisplayPQ");
    //     for(ClusterPair E: PQ){
            
    //         System.out.println("\nIndex A: "+E.Index_A);
    //         System.out.println("Index B: "+E.Index_B);
    //         System.out.println("Nearest Dist: "+E.nearest_dist);
    //         System.out.println("Valid: "+(Points.get(E.Index_A)!=null && Points.get(E.Index_B)!=null));
    //         System.out.println(" ");
    //     }
    //     System.out.println("-----\n");

    // }

    public static void main(String[] args) {
        // test t = new test(args);

        // List<double[]> out = new Cluster().cluster(new ArrayList<int[]>(){{
        //     add(new int[]{5,105});
        //     add(new int[]{6,105});
        //     add(new int[]{5,106});
        //     add(new int[]{4,105});


        //     add(new int[]{5,5});
        //     add(new int[]{6,5});
        //     add(new int[]{5,6});
        //     add(new int[]{4,5});
        //     add(new int[]{5,4});

        //     add(new int[]{105,5});

        //     add(new int[]{105,105});
        // }}, 4);
        // for(double[] o: out)
        //     System.out.println(Arrays.toString(o));

    }
}


// class test{
//     public test(String[] args){
//         Cluster sol = new Cluster();
//         JSONParser jsonParser = new JSONParser();
//         try (FileReader reader = new FileReader("C:\\Users\\BERLIN CHEN\\Desktop\\2022PDSA\\HW7_Cluster_PairPQ_loop\\test.json")){
//             JSONArray all = (JSONArray) jsonParser.parse(reader);
//             for(Object CaseInList : all){
//                 JSONArray a = (JSONArray) CaseInList;
//                 int q_cnt = 0, wa = 0,ac = 0;
//                 for (Object o : a) {
//                     q_cnt++;
//                     JSONObject person = (JSONObject) o;
//                     JSONArray point = (JSONArray) person.get("points");
//                     Long clusterNumber = (Long) person.get("cluster_num");
//                     JSONArray arg_ans = (JSONArray) person.get("answer");
//                     int points_x[] = new int[point.size()];
//                     int points_y[] = new int[point.size()];
//                     double Answer_x[] = new double[arg_ans.size()];
//                     double Answer_y[] = new double[arg_ans.size()];
//                     List<double[]> ansClus = new ArrayList<double[]>();
//                     ArrayList<int[]> pointList = new ArrayList<int[]>();
//                     for(int i=0;i<clusterNumber;i++){
//                         String ansStr = arg_ans.get(i).toString();
//                         ansStr = ansStr.replace("[","");ansStr = ansStr.replace("]","");
//                         String[] parts = ansStr.split(",");
//                         Answer_x[i] = Double.parseDouble(parts[0]);
//                         Answer_y[i] = Double.parseDouble(parts[1]);
//                     }
//                     for(int i=0;i< point.size();i++){
//                         String ansStr = point.get(i).toString();
//                         ansStr = ansStr.replace("[","");ansStr = ansStr.replace("]","");
//                         String[] parts = ansStr.split(",");
//                         pointList.add(new int[]{Integer.parseInt(parts[0]),Integer.parseInt(parts[1])});
//                     }
//                     ansClus = sol.cluster(pointList,Integer.parseInt(clusterNumber.toString()));
//                     if(ansClus.size()!=clusterNumber){
//                         wa++;
//                         System.out.println(q_cnt+": WA");
//                         break;
//                     } else{
//                         for(int i=0;i<clusterNumber;i++){
//                             if(ansClus.get(i)[0]!=Answer_x[i] || ansClus.get(i)[1]!=Answer_y[i]){
//                                 wa++;
//                                 System.out.println(q_cnt+": WA");
//                                 break;
//                             }
//                         }
//                         System.out.println(q_cnt+": AC");
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

/******************************************************************************
 *  Compilation:  javac Point2D.java
 *  Execution:    java Point2D x0 y0 n
 *  Dependencies: StdDraw.java StdRandom.java
 *
 *  Immutable point data type for points in the plane.
 *
 ******************************************************************************/



/**
 *  The {@code Point} class is an immutable data type to encapsulate a
 *  two-dimensional point with real-value coordinates.
 *  <p>
 *  Note: in order to deal with the difference behavior of double and
 *  Double with respect to -0.0 and +0.0, the Point2D constructor converts
 *  any coordinates that are -0.0 to +0.0.
 *  <p>
 *  For additional documentation,
 *  see <a href="https://algs4.cs.princeton.edu/12oop">Section 1.2</a> of
 *  <i>Algorithms, 4th Edition</i> by Robert Sedgewick and Kevin Wayne.
 *
 *  @author Robert Sedgewick
 *  @author Kevin Wayne
 */
class Point2D implements Comparable<Point2D> {

    /**
     * Compares two points by x-coordinate.
     */
    // public static final Comparator<Point2D> X_ORDER = new XOrder();

    // /**
    //  * Compares two points by y-coordinate.
    //  */
    // public static final Comparator<Point2D> Y_ORDER = new YOrder();

    // /**
    //  * Compares two points by polar radius.
    //  */
    // public static final Comparator<Point2D> R_ORDER = new ROrder();

    public static final Comparator<Point2D> X_then_Y_ORDER = new ByXthenY();

    private final double x;    // x coordinate
    private final double y;    // y coordinate

    /**
     * Initializes a new point (x, y).
     * @param x the x-coordinate
     * @param y the y-coordinate
     * @throws IllegalArgumentException if either {@code x} or {@code y}
     *    is {@code Double.NaN}, {@code Double.POSITIVE_INFINITY} or
     *    {@code Double.NEGATIVE_INFINITY}
     */
    public Point2D(double x, double y) {
        if (Double.isInfinite(x) || Double.isInfinite(y))
            throw new IllegalArgumentException("Coordinates must be finite");
        if (Double.isNaN(x) || Double.isNaN(y))
            throw new IllegalArgumentException("Coordinates cannot be NaN");
        if (x == 0.0) this.x = 0.0;  // convert -0.0 to +0.0
        else          this.x = x;

        if (y == 0.0) this.y = 0.0;  // convert -0.0 to +0.0
        else          this.y = y;
    }

    /**
     * Returns the x-coordinate.
     * @return the x-coordinate
     */
    public double x() {
        return x;
    }

    /**
     * Returns the y-coordinate.
     * @return the y-coordinate
     */
    public double y() {
        return y;
    }

    /**
     * Returns the polar radius of this point.
     * @return the polar radius of this point in polar coordiantes: sqrt(x*x + y*y)
     */
    public double r() {
        return Math.sqrt(x*x + y*y);
    }

    /**
     * Returns the angle of this point in polar coordinates.
     * @return the angle (in radians) of this point in polar coordiantes (between –&pi; and &pi;)
     */
    public double theta() {
        return Math.atan2(y, x);
    }

    /**
     * Returns the angle between this point and that point.
     * @return the angle in radians (between –&pi; and &pi;) between this point and that point (0 if equal)
     */
    private double angleTo(Point2D that) {
        double dx = that.x - this.x;
        double dy = that.y - this.y;
        return Math.atan2(dy, dx);
    }

    /**
     * Returns true if a→b→c is a counterclockwise turn.
     * @param a first point
     * @param b second point
     * @param c third point
     * @return { -1, 0, +1 } if a→b→c is a { clockwise, collinear; counterclocwise } turn.
     */
    public static int ccw(Point2D a, Point2D b, Point2D c) {
        double area2 = (b.x-a.x)*(c.y-a.y) - (b.y-a.y)*(c.x-a.x);
        if      (area2 < 0) return -1;
        else if (area2 > 0) return +1;
        else                return  0;
    }

    /**
     * Returns twice the signed area of the triangle a-b-c.
     * @param a first point
     * @param b second point
     * @param c third point
     * @return twice the signed area of the triangle a-b-c
     */
    public static double area2(Point2D a, Point2D b, Point2D c) {
        return (b.x-a.x)*(c.y-a.y) - (b.y-a.y)*(c.x-a.x);
    }

    /**
     * Returns the Euclidean distance between this point and that point.
     * @param that the other point
     * @return the Euclidean distance between this point and that point
     */
    public double distanceTo(Point2D that) {
        double dx = this.x - that.x;
        double dy = this.y - that.y;
        return Math.sqrt(dx*dx + dy*dy);
    }

    /**
     * Returns the square of the Euclidean distance between this point and that point.
     * @param that the other point
     * @return the square of the Euclidean distance between this point and that point
     */
    public double distanceSquaredTo(Point2D that) {
        double dx = this.x - that.x;
        double dy = this.y - that.y;
        return dx*dx + dy*dy;
    }

    /**
     * Compares two points by y-coordinate, breaking ties by x-coordinate.
     * Formally, the invoking point (x0, y0) is less than the argument point (x1, y1)
     * if and only if either {@code y0 < y1} or if {@code y0 == y1} and {@code x0 < x1}.
     *
     * @param  that the other point
     * @return the value {@code 0} if this string is equal to the argument
     *         string (precisely when {@code equals()} returns {@code true});
     *         a negative integer if this point is less than the argument
     *         point; and a positive integer if this point is greater than the
     *         argument point
     */
    public int compareTo(Point2D that) {
        if (this.y < that.y) return -1;
        if (this.y > that.y) return +1;
        if (this.x < that.x) return -1;
        if (this.x > that.x) return +1;
        return 0;
    }

    /**
     * Compares two points by polar angle (between 0 and 2&pi;) with respect to this point.
     *
     * @return the comparator
     */
    public Comparator<Point2D> polarOrder() {
        return new PolarOrder();
    }

    /**
     * Compares two points by atan2() angle (between –&pi; and &pi;) with respect to this point.
     *
     * @return the comparator
     */
    public Comparator<Point2D> atan2Order() {
        return new Atan2Order();
    }

    /**
     * Compares two points by distance to this point.
     *
     * @return the comparator
     */
    public Comparator<Point2D> distanceToOrder() {
        return new DistanceToOrder();
    }

    private static class ByXthenY implements Comparator<Point2D> {
        public int compare(Point2D p, Point2D q) {
            if (p.x < q.x) return -1;
            if (p.x > q.x) return +1;
            if (p.y < q.y) return -1;
            return +1;
        }
    }

    // compare points according to their x-coordinate
    private static class XOrder implements Comparator<Point2D> {
        public int compare(Point2D p, Point2D q) {
            if (p.x < q.x) return -1;
            if (p.x > q.x) return +1;
            return 0;
        }
    }

    // compare points according to their y-coordinate
    private static class YOrder implements Comparator<Point2D> {
        public int compare(Point2D p, Point2D q) {
            if (p.y < q.y) return -1;
            if (p.y > q.y) return +1;
            return 0;
        }
    }

    // compare points according to their polar radius
    private static class ROrder implements Comparator<Point2D> {
        public int compare(Point2D p, Point2D q) {
            double delta = (p.x*p.x + p.y*p.y) - (q.x*q.x + q.y*q.y);
            if (delta < 0) return -1;
            if (delta > 0) return +1;
            return 0;
        }
    }

    // compare other points relative to atan2 angle (bewteen -pi/2 and pi/2) they make with this Point
    private class Atan2Order implements Comparator<Point2D> {
        public int compare(Point2D q1, Point2D q2) {
            double angle1 = angleTo(q1);
            double angle2 = angleTo(q2);
            if      (angle1 < angle2) return -1;
            else if (angle1 > angle2) return +1;
            else                      return  0;
        }
    }

    // compare other points relative to polar angle (between 0 and 2pi) they make with this Point
    private class PolarOrder implements Comparator<Point2D> {
        public int compare(Point2D q1, Point2D q2) {
            double dx1 = q1.x - x;
            double dy1 = q1.y - y;
            double dx2 = q2.x - x;
            double dy2 = q2.y - y;

            if      (dy1 >= 0 && dy2 < 0) return -1;    // q1 above; q2 below
            else if (dy2 >= 0 && dy1 < 0) return +1;    // q1 below; q2 above
            else if (dy1 == 0 && dy2 == 0) {            // 3-collinear and horizontal
                if      (dx1 >= 0 && dx2 < 0) return -1;
                else if (dx2 >= 0 && dx1 < 0) return +1;
                else                          return  0;
            }
            else return -ccw(Point2D.this, q1, q2);     // both above or below

            // Note: ccw() recomputes dx1, dy1, dx2, and dy2
        }
    }

    // compare points according to their distance to this point
    private class DistanceToOrder implements Comparator<Point2D> {
        public int compare(Point2D p, Point2D q) {
            double dist1 = distanceSquaredTo(p);
            double dist2 = distanceSquaredTo(q);
            if      (dist1 < dist2) return -1;
            else if (dist1 > dist2) return +1;
            else                    return  0;
        }
    }


    /**
     * Compares this point to the specified point.
     *
     * @param  other the other point
     * @return {@code true} if this point equals {@code other};
     *         {@code false} otherwise
     */
    @Override
    public boolean equals(Object other) {
        if (other == this) return true;
        if (other == null) return false;
        if (other.getClass() != this.getClass()) return false;
        Point2D that = (Point2D) other;
        return this.x == that.x && this.y == that.y;
    }

    /**
     * Return a string representation of this point.
     * @return a string representation of this point in the format (x, y)
     */
    @Override
    public String toString() {
        return "(" + x + ", " + y + ")";
    }

    /**
     * Returns an integer hash code for this point.
     * @return an integer hash code for this point
     */
    @Override
    public int hashCode() {
        int hashX = ((Double) x).hashCode();
        int hashY = ((Double) y).hashCode();
        return 31*hashX + hashY;
    }

    // /**
    //  * Plot this point using standard draw.
    //  */
    // public void draw() {
    //     StdDraw.point(x, y);
    // }

    // /**
    //  * Plot a line from this point to that point using standard draw.
    //  * @param that the other point
    //  */
    // public void drawTo(Point2D that) {
    //     StdDraw.line(this.x, this.y, that.x, that.y);
    // }


    // /**
    //  * Unit tests the point data type.
    //  *
    //  * @param args the command-line arguments
    //  */
    // public static void main(String[] args) {
    //     int x0 = Integer.parseInt(args[0]);
    //     int y0 = Integer.parseInt(args[1]);
    //     int n = Integer.parseInt(args[2]);

    //     StdDraw.setCanvasSize(800, 800);
    //     StdDraw.setXscale(0, 100);
    //     StdDraw.setYscale(0, 100);
    //     StdDraw.setPenRadius(0.005);
    //     StdDraw.enableDoubleBuffering();

    //     Point2D[] points = new Point2D[n];
    //     for (int i = 0; i < n; i++) {
    //         int x = StdRandom.uniformInt(100);
    //         int y = StdRandom.uniformInt(100);
    //         points[i] = new Point2D(x, y);
    //         points[i].draw();
    //     }

    //     // draw p = (x0, x1) in red
    //     Point2D p = new Point2D(x0, y0);
    //     StdDraw.setPenColor(StdDraw.RED);
    //     StdDraw.setPenRadius(0.02);
    //     p.draw();


    //     // draw line segments from p to each point, one at a time, in polar order
    //     StdDraw.setPenRadius();
    //     StdDraw.setPenColor(StdDraw.BLUE);
    //     Arrays.sort(points, p.polarOrder());
    //     for (int i = 0; i < n; i++) {
    //         p.drawTo(points[i]);
    //         StdDraw.show();
    //         StdDraw.pause(100);
    //     }
    // }
}

/******************************************************************************
 *  Copyright 2002-2022, Robert Sedgewick and Kevin Wayne.
 *
 *  This file is part of algs4.jar, which accompanies the textbook
 *
 *      Algorithms, 4th edition by Robert Sedgewick and Kevin Wayne,
 *      Addison-Wesley Professional, 2011, ISBN 0-321-57351-X.
 *      http://algs4.cs.princeton.edu
 *
 *
 *  algs4.jar is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  algs4.jar is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with algs4.jar.  If not, see http://www.gnu.org/licenses.
 ******************************************************************************/
