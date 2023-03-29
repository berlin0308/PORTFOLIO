import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import java.util.Arrays;
import java.util.Comparator;
import java.util.PriorityQueue;
import java.lang.Math;

import edu.princeton.cs.algs4.MinPQ;
import edu.princeton.cs.algs4.Point2D;
import edu.princeton.cs.algs4.Stack;


class EachCluster{
    public final Comparator<EachCluster> BYNEARESTDIST = new byNearestDist();
    public int Index;
    public List<Integer> NearestIndex;

    public Point2D Centroid;
    public List<Point2D> NearestCluster;
    double nearest_dist;
    int weight;

    EachCluster(int i,List<Integer> n, Point2D C, List<Point2D> N,double d,int w){
        Index = i;
        NearestIndex = n;
        Centroid = C;
        NearestCluster = N;
        nearest_dist = d;
        weight = w;
    }
    
    private class byNearestDist implements Comparator<EachCluster>{
        public int compare(EachCluster A,EachCluster B){
            if(A.nearest_dist>B.nearest_dist) return 1;
            else return -1;
        }
    }
    
}

class Cluster {

    ArrayList<Point2D> AllPoints = new ArrayList<Point2D>(); // all points including invalid, new centroids (invalid Points are set axis INFINITY)
    MinPQ<EachCluster> ClusterPQ = new MinPQ<EachCluster>(new EachCluster(0,new ArrayList<>(),null, AllPoints, 0, 0).BYNEARESTDIST);
    List<int[]> points;
    int ValidClusterNum =0;

    public List<double[]> cluster(List<int[]> p, int cluster_num) {
        ValidClusterNum = p.size();
        points = p;
        /* Record nearest points and dist of each point */
        int self_index=0;
        for(int[] i: points) {
            AllPoints.add(new Point2D(i[0], i[1]));
            EachCluster C = UpdateNearest(self_index,0, i,new double[]{});
            ClusterPQ.insert(C);
            self_index++;
            
        }
        
        System.out.println("\nSameMinDistCount: "+SameMinDistCount());
        // displayPQ();
        while(ValidClusterNum>cluster_num){
            // System.out.println("\n"+ValidClusterNum+" Clusters remain\n");
            
            /* Update all clusters' nearest*/
            Stack<EachCluster> ToBeUpdated = new Stack<EachCluster>();
            while(!ClusterPQ.isEmpty()){
                EachCluster E =  ClusterPQ.delMin();
                int w = E.weight;
                E = UpdateNearest(E.Index, 1,new int[]{}, new double[]{E.Centroid.x(),E.Centroid.y()});
                E.weight = w;
                ToBeUpdated.push(E);
            }
            while(!ToBeUpdated.isEmpty()){
                ClusterPQ.insert(ToBeUpdated.pop());
            }
            
            System.out.println("\n1111111111111111111");

            List<EachCluster> nearestPoints = new ArrayList<EachCluster>();
            double min_dist = ClusterPQ.min().nearest_dist;
            for(EachCluster E: ClusterPQ){
                if(E.nearest_dist==min_dist) nearestPoints.add(E);
                else break;
            }
            for(int i=0;i<nearestPoints.size();i++){
                for(int j=0;j<nearestPoints.size();j++){
                    for(int k: nearestPoints.get(i).NearestIndex){
                        for(int l:nearestPoints.get(j).NearestIndex){
                            if(k==nearestPoints.get(j).Index && l==nearestPoints.get(i).Index && !ClusterPQ.isEmpty()){
                                EachCluster A = ClusterPQ.delMin();
                                EachCluster B = ClusterPQ.delMin();
                                AllPoints.set(A.Index, null);
                                AllPoints.set(B.Index, null);
                                
                                double NewCentroid_x = (A.Centroid.x()*A.weight+B.Centroid.x()*B.weight)/(A.weight+B.weight);
                                double NewCentroid_y = (A.Centroid.y()*A.weight+B.Centroid.y()*B.weight)/(A.weight+B.weight);
                                
                                System.out.println("\nNew Centroid: ("+NewCentroid_x+", "+NewCentroid_y+")\n");
                                EachCluster C = UpdateNearest(AllPoints.size(),1,new int[]{}, new double[]{NewCentroid_x,NewCentroid_y});
                                C.weight = A.weight+B.weight;
                                ValidClusterNum--;
                                ClusterPQ.insert(C);
                                AllPoints.add(new Point2D(NewCentroid_x, NewCentroid_y));
                                break;
                            }

                        }
                    }
                }
            }
        

        //     if(SameMinDistCount()==2){
        //         displayPQ();
        //         displayAllPoints();
        //         EachCluster A = ClusterPQ.delMin();
        //         EachCluster B = ClusterPQ.delMin();
        //         AllPoints.set(A.Index, null);
        //         AllPoints.set(B.Index, null);
                
        //         double NewCentroid_x = (A.Centroid.x()*A.weight+B.Centroid.x()*B.weight)/(A.weight+B.weight);
        //         double NewCentroid_y = (A.Centroid.y()*A.weight+B.Centroid.y()*B.weight)/(A.weight+B.weight);
                
        //         System.out.println("\nNew Centroid: ("+NewCentroid_x+", "+NewCentroid_y+")\n");
        //         EachCluster C = UpdateNearest(AllPoints.size(),1,new int[]{}, new double[]{NewCentroid_x,NewCentroid_y});
        //         C.weight = A.weight+B.weight;
        //         ValidClusterNum--;
        //         ClusterPQ.insert(C);
        //         AllPoints.add(new Point2D(NewCentroid_x, NewCentroid_y));

        //     }else{
                

        //     }
        }
        
        ArrayList<double[]> ans = new ArrayList<double[]>();
        for(Point2D P : AllPoints){
            if(P==null) System.out.print("null");
            else ans.add(new double[]{P.x(), P.y()});
        }
        // ans.add(new double[]{0, 1.5});
        // ans.add(new double[]{3, 1.5});
        return ans;
    }
    
    
    public EachCluster UpdateNearest(int self_index,int option,int[] i,double[] d){
        List<Point2D> nearest = new ArrayList<Point2D>(); // nearest points of a point
        List<Integer> nearest_index = new ArrayList<Integer>(); // nearest points of a point
        double min_dist = Double.POSITIVE_INFINITY; // nearest distance
        EachCluster C = new EachCluster(self_index,nearest_index ,new Point2D(0,0), nearest, min_dist, 1) ;


        if(option==0){ // initialize, from points

            for(int[] j: points){
                if(i[0]==j[0] && i[1]==j[1]) continue; // point itself
    
                double dist = Math.sqrt(Math.pow(i[0]-j[0], 2)+Math.pow(i[1]-j[1], 2));
                if(dist<min_dist && dist!=0){
                    min_dist = dist;
                }
            }
    
            int index=0;
            for(int[] k:points){
                double dist = Math.sqrt(Math.pow(i[0]-k[0], 2)+Math.pow(i[1]-k[1], 2));
                if(dist==min_dist){
                    nearest.add(new Point2D(k[0], k[1]));
                    nearest_index.add(index);
                }
                index++;
            }
            
            C = new EachCluster(self_index,nearest_index ,new Point2D(i[0], i[1]), nearest, min_dist, 1);
        }
        else if(option==1){ // new, from AllPoints
            for(Point2D j: AllPoints){
                if(j==null) continue; // invalid
                if(d[0]==j.x() && d[1]==j.y()) continue; // point itself
                
                double dist = Math.sqrt(Math.pow(d[0]-j.x(), 2)+Math.pow(d[1]-j.y(), 2));
                if(dist<min_dist && dist!=0){
                    min_dist = dist;
                }
            }
            
            int index=0;
            for(Point2D k:AllPoints){
                if(k==null) continue; // invalid
                double dist = Math.sqrt(Math.pow(d[0]-k.x(), 2)+Math.pow(d[1]-k.y(), 2));
                if(dist==min_dist){
                    nearest.add(k);
                    nearest_index.add(index);
                }
                index++;
            }
            C = new EachCluster(self_index,nearest_index ,new Point2D(d[0], d[1]), nearest, min_dist, 1);
        }
        // System.out.println("\nSelf index: "+self_index);
        // System.out.println("Self Point: "+Arrays.toString(i));
        // System.out.println("Nearest index: "+nearest_index.toString());
        // System.out.println("Nearest Points: "+nearest.toString());
        // System.out.println("Nearest Dist: "+min_dist);
        
        return C;
    }

    public int SameMinDistCount(){
        int count = 0;
        double min_dist = ClusterPQ.min().nearest_dist;
        for(EachCluster E: ClusterPQ){
            if(E.nearest_dist==min_dist) count++;
            else break;
        }
        return count;
    }

    public void displayAllPoints(){
        System.out.println("-----\ndisplayAllPoints");
        for(Point2D P:AllPoints){
            if(P==null) System.out.println("null");
            else System.out.println(P.toString());
        }
        System.out.println("-----\n");
    }

    public void displayPQ(){
        System.out.println("-----\ndisplayPQ");

        for(EachCluster E: ClusterPQ){
            
            System.out.println("\nSelf index: "+E.Index);
            System.out.println("Self Point: "+E.Centroid.toString());
            System.out.println("Nearest index: "+E.NearestIndex.toString());
            System.out.println("Nearest Points: "+E.NearestCluster.toString());
            System.out.println("Nearest Dist: "+E.nearest_dist);
            System.out.println(" ");
            
        }
        System.out.println("-----\n");

    }

    public static void main(String[] args) {
        // test t = new test(args);
        List<double[]> out = new Cluster().cluster(new ArrayList<int[]>(){{
            add(new int[]{0,1});
            add(new int[]{0,2});
            add(new int[]{3,1});
            add(new int[]{4,2});
        }}, 2);
        for(double[] o: out)
            System.out.println(Arrays.toString(o));

    }
}


class test{
    public test(String[] args){
        Cluster sol = new Cluster();
        JSONParser jsonParser = new JSONParser();
        try (FileReader reader = new FileReader("C:\\Users\\BERLIN CHEN\\Desktop\\2022PDSA\\HW7_Cluster\\test.json")){
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