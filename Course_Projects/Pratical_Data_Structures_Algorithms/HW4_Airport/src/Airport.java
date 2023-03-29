import java.util.List;
import edu.princeton.cs.algs4.Point2D;
import java.lang.Math;
import java.util.*;

// import org.json.simple.JSONArray;
// import org.json.simple.JSONObject;
// import org.json.simple.parser.JSONParser;
// import org.json.simple.parser.ParseException;

// import java.io.FileNotFoundException;
// import java.io.FileReader;
// import java.io.IOException;



class Airport {
    
    public double airport(List<int[]> houses) {
        int N = houses.size();
        Point2D[] Points = new Point2D[N];
        for(int i=0;i<N;i++){
            double x = houses.get(i)[0];
            double y = houses.get(i)[1];
            Point2D p = new Point2D(x,y);
            Points[i] = p;
        }
        
        // Find convex hull point
        GrahamScan G = new GrahamScan(Points);
        Point2D[] Hull_Points = G.hull();

        // Find fringe lines of the convex hull
        // Record the average distances meanwhile
        double min_avg_distance = 0.0;
        for(int i=0;i<Hull_Points.length;i++){
            Point2D Point_A ;
            Point2D Point_B ;
            double Dist_Sum=0;
            try{
                Point_A = Hull_Points[i];
                Point_B = Hull_Points[i+1];
            }catch(Exception ArrayIndexOutOfBoundsException){
                Point_A = Hull_Points[i];
                Point_B = Hull_Points[0];
            }
            for(int j=0;j<N;j++){
                Dist_Sum += Math.abs((Point_B.y()-Point_A.y())*Points[j].x()+(Point_A.x()-Point_B.x())*Points[j].y()+
                (Point_B.x()*Point_A.y()-Point_A.x()*Point_B.y())) / Math.sqrt(Math.pow((Point_B.y()-Point_A.y()),2)+Math.pow((Point_A.x()-Point_B.x()),2));
            }
            Dist_Sum /= N;
            //System.out.println(i+" avg:"+Dist_Sum);

            if(i==0) min_avg_distance = Dist_Sum;
            min_avg_distance = Math.min(min_avg_distance,Dist_Sum);
        }
        return min_avg_distance; 
    }


    public static void main(String[] args) {

        // System.out.println(new Airport().airport(new ArrayList<int[]>(){{
        //     add(new int[]{0,0});
        //     add(new int[]{1,0});
        //     add(new int[]{0,1});
        //     add(new int[]{1,1});
        //     add(new int[]{2,2});
        // }}));

        //test t = new test(args);

    }
}


class GrahamScan {

    private Stack<Point2D> hull = new Stack<Point2D>();
    public GrahamScan(Point2D[] points) {
        if (points == null) throw new IllegalArgumentException("argument is null");
        if (points.length == 0) throw new IllegalArgumentException("array is of length 0");

        int n = points.length;
        Point2D[] a = new Point2D[n];
        for (int i = 0; i < n; i++) {
            if (points[i] == null)
                throw new IllegalArgumentException("points[" + i + "] is null");
            a[i] = points[i];
        }

        Arrays.sort(a);
        Arrays.sort(a, 1, n, a[0].polarOrder());

        hull.push(a[0]);       // a[0] is first extreme point

        // find index k1 of first point not equal to a[0]
        int k1;
        for (k1 = 1; k1 < n; k1++)
            if (!a[0].equals(a[k1])) break;
        if (k1 == n) return;        // all points equal

        // find index k2 of first point not collinear with a[0] and a[k1]
        int k2;
        for (k2 = k1+1; k2 < n; k2++)
            if (Point2D.ccw(a[0], a[k1], a[k2]) != 0) break;
        hull.push(a[k2-1]);    // a[k2-1] is second extreme point

        // Graham scan; note that a[n-1] is extreme point different from a[0]
        for (int i = k2; i < n; i++) {
            Point2D top = hull.pop();
            while (Point2D.ccw(hull.peek(), top, a[i]) <= 0) {
                top = hull.pop();
            }
            hull.push(top);
            hull.push(a[i]);
        }

        assert isConvex();
    }

    /**
     * Returns the extreme points on the convex hull in counterclockwise order.
     *
     * @return the extreme points on the convex hull in counterclockwise order
     */
    public Point2D[] hull() {
        // Stack<Point2D> s = new Stack<Point2D>();
        Point2D[] s = new Point2D[hull.size()];
        // for (Point2D p : hull) s.push(p);
        int c=0;
        for (Point2D p : hull){
            s[c] = p;
            c++;
        }
        return s;
    }

    // check that boundary of hull is strictly convex
    private boolean isConvex() {
        int n = hull.size();
        if (n <= 2) return true;

        Point2D[] points = new Point2D[n];
        int k = 0;
        for (Point2D p : hull()) {
            points[k++] = p;
        }

        for (int i = 0; i < n; i++) {
            if (Point2D.ccw(points[i], points[(i+1) % n], points[(i+2) % n]) <= 0) {
                return false;
            }
        }
        return true;
    }

   /**
     * Unit tests the {@code GrahamScan} data type.
     * Reads in an integer {@code n} and {@code n} points (specified by
     * their <em>x</em>- and <em>y</em>-coordinates) from standard input;
     * computes their convex hull; and prints out the points on the
     * convex hull to standard output.
     *
     * @param args the command-line arguments
     */

}

// class test{
//     public test(String[] args){
//         Airport sol = new Airport();
//         JSONParser jsonParser = new JSONParser();
//         try (FileReader reader = new FileReader("C:\\Users\\BERLIN CHEN\\Desktop\\2022PDSA\\HW4_Airport\\src\\airport.json")){
//             JSONArray all = (JSONArray) jsonParser.parse(reader);
//             for(Object CaseInList : all){
//                 JSONArray a = (JSONArray) CaseInList;
//                 int q_cnt = 0, wa = 0,ac = 0;
//                 for (Object o : a) {
//                     q_cnt++;
//                     JSONObject person = (JSONObject) o;
//                     JSONArray arg_hou = (JSONArray) person.get("houses");
//                     double Answer = (double) person.get("answer");
//                     ArrayList<int[]> HOU = new ArrayList<int[]>();
//                     double Answer_W = 0;
//                     for(int i=0;i<arg_hou.size();i++){
//                         String spl = arg_hou.get(i).toString();
//                         String fir = "";
//                         String sec = "";
//                         String[] two = new String[2];
//                         two = spl.split(",");
//                         fir = two[0].replace("[","");
//                         sec = two[1].replace("]","");
//                         int[] hou = new int[2];
//                         hou[0] = Integer.parseInt(fir);
//                         hou[1] = Integer.parseInt(sec);
//                         HOU.add(hou);
//                     }
//                     Answer_W = sol.airport(HOU);
//                     if(Math.abs(Answer_W-Answer)<1e-4){
//                         System.out.println(q_cnt+": AC");
//                     }
//                     else {
//                         wa++;
//                         System.out.println(q_cnt+": WA");
//                         System.out.println("your answer : "+Answer_W);
//                         System.out.println("true answer : "+Answer);
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