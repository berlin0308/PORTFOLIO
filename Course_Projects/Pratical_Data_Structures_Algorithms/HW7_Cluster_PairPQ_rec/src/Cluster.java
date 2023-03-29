import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Comparator;
import java.lang.Math;

import edu.princeton.cs.algs4.MinPQ;
import edu.princeton.cs.algs4.Point2D;


class Centroid{

    public final Comparator<ClusterPair> BYXTHENY = new byXthenY();
    public double X;
    public double Y;
    Centroid(double x,double y){
        X = x;
        Y = y;
    }
    private class byXthenY implements Comparator<ClusterPair>{
        public int compare(ClusterPair A,ClusterPair B){
            if(A.nearest_dist>B.nearest_dist) return 1;
            else return -1;
        }
    }
}


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
    MinPQ<ClusterPair> ClusterPairPQ = new MinPQ<ClusterPair>(new ClusterPair(0, 0, 0).BYNEARESTDIST);
    ArrayList<Point2D> Points;
    ArrayList<Integer> Weights; 
    List<int[]> points;
    int ValidClusterNum;

    public List<double[]> cluster(List<int[]> p, int cluster_num) {
        ClusterPairPQ = new MinPQ<ClusterPair>(new ClusterPair(0, 0, 0).BYNEARESTDIST);
        Points = new ArrayList<Point2D>(); // all points including invalid, new centroids
        Weights = new ArrayList<Integer>();
        ValidClusterNum = p.size();
        points = p;
        for(int i=0;i<p.size();i++){
            Points.add(new Point2D(p.get(i)[0],p.get(i)[1]));
            Weights.add(1);

            for(int j=i+1;j<p.size();j++){
                double dist = Math.sqrt(Math.pow(p.get(i)[0]-p.get(j)[0], 2)+Math.pow(p.get(i)[1]-p.get(j)[1], 2));
                if(dist<Double.POSITIVE_INFINITY){
                    ClusterPairPQ.insert(new ClusterPair(i, j,dist));
                }
            }
        }
        // for(int w: Weights){
        //     System.out.println(w);
        // }

        System.out.println("\n\nPoints: "+p.size());
        // System.out.println("\n\nInitial");
        // for(Point2D P : Points){
        //     if(P==null) continue;
        //     System.out.println(P.toString());
            
        // }
        
        Clustering(ClusterPairPQ, p.size(), cluster_num);
        // displayPQ(ClusterPairPQ);
        

        ArrayList<double[]> ans = new ArrayList<double[]>();
        MinPQ<Point2D> Centroids = new MinPQ<Point2D>(Point2D.X_ORDER);
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
            System.out.println("( "+P.x()+" , "+P.y()+" )");
        }
        return ans;
    }
    
    private void Clustering(MinPQ<ClusterPair> Pairs, int K, int finalClusterNum){
        // System.out.println("K: "+K);
        // System.out.println("target: "+finalClusterNum);
        // System.out.println("Valid: "+ValidClusterNum);
        
        
        if(K<=finalClusterNum) return ;
        // if(ValidClusterNum<=finalClusterNum) return ;
        if(Pairs.isEmpty()) return ;

        try{
            ClusterPair NearestPair = Pairs.delMin();
            if(NearestPair!=null && (Points.get(NearestPair.Index_A)!=null && Points.get(NearestPair.Index_B)!=null)){ // both are valid
                // K--;
                // ValidClusterNum--;

                int C_Weight = Weights.get(NearestPair.Index_A) + Weights.get(NearestPair.Index_B);
                Point2D C_Point = new Point2D((Points.get(NearestPair.Index_A).x()*Weights.get(NearestPair.Index_A)+Points.get(NearestPair.Index_B).x()*Weights.get(NearestPair.Index_B))/(Weights.get(NearestPair.Index_A)+Weights.get(NearestPair.Index_B))
                ,(Points.get(NearestPair.Index_A).y()*Weights.get(NearestPair.Index_A)+Points.get(NearestPair.Index_B).y()*Weights.get(NearestPair.Index_B))/(Weights.get(NearestPair.Index_A)+Weights.get(NearestPair.Index_B)));
                
                // System.out.println("NearestPair.Index_A: "+NearestPair.Index_A);
                // System.out.println("NearestPair.Index_B: "+NearestPair.Index_B);
                System.out.println("New Centroid: "+C_Point.toString());
                
                Points.set(NearestPair.Index_A, null);
                Points.set(NearestPair.Index_B, null);
                Weights.add(C_Weight);
                Points.add(C_Point);
                
                // System.out.println("Points size: "+Points.size());
                for(int i=0;i<Points.size()-1;i++){
                    if(Points.get(i)==null) continue;
                    double dist = Math.sqrt(Math.pow(Points.get(i).x()-C_Point.x(), 2)+Math.pow(Points.get(i).y()-C_Point.y(), 2));
                    if(dist<Double.POSITIVE_INFINITY){

                        ClusterPair NewPair = new ClusterPair(i, Points.size()-1, dist);
                        Pairs.insert(NewPair);
                    }
                }
                
                Clustering(Pairs, K-1, finalClusterNum);
                
            }else{
                // System.out.println("Invalid, ignore: "+NearestPair.Index_A+" & "+NearestPair.Index_B);
                Clustering(Pairs, K, finalClusterNum);
                
            }

        }catch(Exception e){
            System.out.println(e);
        }
        
    }


    public void displayPQ(MinPQ<ClusterPair> PQ){
        System.out.println("-----\ndisplayPQ");
        for(ClusterPair E: PQ){
            
            System.out.println("\nIndex A: "+E.Index_A);
            System.out.println("Index B: "+E.Index_B);
            System.out.println("Nearest Dist: "+E.nearest_dist);
            System.out.println("Valid: "+(Points.get(E.Index_A)!=null && Points.get(E.Index_B)!=null));
            System.out.println(" ");
        }
        System.out.println("-----\n");

    }

    public static void main(String[] args) {
        test t = new test(args);

        
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


class test{
    public test(String[] args){
        Cluster sol = new Cluster();
        JSONParser jsonParser = new JSONParser();
        try (FileReader reader = new FileReader("C:\\Users\\BERLIN CHEN\\Desktop\\2022PDSA\\HW7_Cluster_PairPQ\\test.json")){
            JSONArray all = (JSONArray) jsonParser.parse(reader);
            for(Object CaseInList : all){
                JSONArray a = (JSONArray) CaseInList;
                int q_cnt = 0, wa = 0,ac = 0;
                for (Object o : a) {
                    q_cnt++;
                    JSONObject person = (JSONObject) o;
                    JSONArray point = (JSONArray) person.get("points");
                    Long clusterNumber = (Long) person.get("cluster_num");
                    JSONArray arg_ans = (JSONArray) person.get("answer");
                    int points_x[] = new int[point.size()];
                    int points_y[] = new int[point.size()];
                    double Answer_x[] = new double[arg_ans.size()];
                    double Answer_y[] = new double[arg_ans.size()];
                    List<double[]> ansClus = new ArrayList<double[]>();
                    ArrayList<int[]> pointList = new ArrayList<int[]>();
                    for(int i=0;i<clusterNumber;i++){
                        String ansStr = arg_ans.get(i).toString();
                        ansStr = ansStr.replace("[","");ansStr = ansStr.replace("]","");
                        String[] parts = ansStr.split(",");
                        Answer_x[i] = Double.parseDouble(parts[0]);
                        Answer_y[i] = Double.parseDouble(parts[1]);
                    }
                    for(int i=0;i< point.size();i++){
                        String ansStr = point.get(i).toString();
                        ansStr = ansStr.replace("[","");ansStr = ansStr.replace("]","");
                        String[] parts = ansStr.split(",");
                        pointList.add(new int[]{Integer.parseInt(parts[0]),Integer.parseInt(parts[1])});
                    }
                    ansClus = sol.cluster(pointList,Integer.parseInt(clusterNumber.toString()));
                    if(ansClus.size()!=clusterNumber){
                        wa++;
                        System.out.println(q_cnt+": WA");
                        break;
                    } else{
                        for(int i=0;i<clusterNumber;i++){
                            if(ansClus.get(i)[0]!=Answer_x[i] || ansClus.get(i)[1]!=Answer_y[i]){
                                wa++;
                                System.out.println(q_cnt+": WA");
                                break;
                            }
                        }
                        System.out.println(q_cnt+": AC");
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