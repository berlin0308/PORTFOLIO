import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
import java.util.PriorityQueue;

class CovidSimulation {
    PriorityQueue<Event> pq = new PriorityQueue<>();;
    int index = 0;
    City[] city;
    int max_city;
    boolean max;

    class City
    {
        int citizen;
        int attacked_date;
        int recover_date;
        City(int num){
            citizen = num;
        }
    }
    class Event implements Comparable<Event>{
        private int Date;
        private int City_e;
        private int Number;
        private int Index;
        private int Plan;
        Event(int date, int city, int plan){
            Date = date;
            City_e = city;
            Plan = plan;
        }
        public int compareTo(Event o){
            if(this.Date > o.Date) return 1;
            else if(this.Date < o.Date) return -1;
            else {
                if(this.Plan < o.Plan) return -1;
                if(this.Plan > o.Plan) return 1;
                return 0;
            }
        }
    }

    public CovidSimulation(int[] Num_Of_Citizen) {
        int city_num = Num_Of_Citizen.length;
        city = new City[city_num];
        for(int i = 0 ;i < city_num ;i++) {
            city[i] = new City(Num_Of_Citizen[i]);
        }
    }
    public int CityWithTheMostPatient(int date){
        int[] recover_date  = new int[index];
        if(!pq.isEmpty()) {
            Event next = pq.peek();
            while (next.Date <= date) {
                Event now = pq.poll();
                if (now.Plan == 0) {
                    if(city[now.City_e].recover_date <= now.Date ) {
                        city[now.City_e].attacked_date = now.Date;
                        city[now.City_e].recover_date = now.Date + 4;
                    }
                }
                if (now.Plan == 2) {
                    if(now.Date < city[now.City_e].recover_date && now.Date >= city[now.City_e].attacked_date){
                        recover_date[now.Index] = city[now.City_e].recover_date;
                    }
                    city[now.City_e].citizen = city[now.City_e].citizen - now.Number;
                }
                if(now.Plan == 1){
                    if(recover_date[now.Index] > now.Date){
                        if(city[now.City_e].attacked_date == 0 || now.Date > city[now.City_e].recover_date){
                            city[now.City_e].recover_date = now.Date + 4;
                            city[now.City_e].attacked_date = now.Date;
                        }
                        else if(city[now.City_e].recover_date < recover_date[now.Index]){
                            city[now.City_e].recover_date = recover_date[now.Index];
                        }
                        if(city[now.City_e].recover_date - city[now.City_e].attacked_date > 7){
                            city[now.City_e].recover_date = city[now.City_e].attacked_date + 7;
                        }
                    }
                    city[now.City_e].citizen = city[now.City_e].citizen + now.Number;
                }
                if (pq.isEmpty()) {
                    break;
                }
                next = pq.peek();
            }
        }
//        max_city = 0;
        for(int i = 0;i < city.length ;i++){
            if(date >= city[i].attacked_date && date < city[i].recover_date){
                if(max == false){
                    max_city = i;
                }
                if(city[i].citizen >= city[max_city].citizen){
                    max_city = i;
                }
                max = true;
            }
        }
        if(max == false) return -1;
        max = false;
        return max_city;
    }
    public void virusAttackPlan(int city, int date){
        Event event = new Event(date,city,0);
        pq.add(event);
    }
    public void TravelPlan(int NumberOfTraveller, int FromCity, int ToCity, int DateOfDeparture, int DateOfArrival){
        Event leave_event = new Event(DateOfDeparture, FromCity, 2);
        Event arrive_event = new Event(DateOfArrival, ToCity, 1);
        leave_event.Number = NumberOfTraveller;
        arrive_event.Number = NumberOfTraveller;
        leave_event.Index = index;
        arrive_event.Index = index;
        pq.add(leave_event);
        pq.add(arrive_event);
        index++;
    }

    public static void main(String[] args){
        LongJump sol = new LongJump(new int[] {10, 100, 15, 25, 10, 13});
        
        sol.virusAttackPlan(0, 1);
        sol.virusAttackPlan(4, 3);
        sol.TravelPlan(3, 0, 3, 3, 4);
        sol.TravelPlan(3, 4, 0, 3, 4); 
        
        System.out.println(sol.CityWithTheMostPatient(10));
        System.out.println(sol.CityWithTheMostPatient(11));
        // test t = new test(args);
    }
}
class test {
    public test(String[] args) {
        LongJump g;
        JSONParser jsonParser = new JSONParser();
        try (FileReader reader = new FileReader(args[0])){
            JSONArray all = (JSONArray) jsonParser.parse(reader);
            int waSize = 0;
            int count = 0;
            for(Object CaseInList : all){
                JSONArray a = (JSONArray) CaseInList;
                //Board Setup
                JSONObject argsSetting = (JSONObject) a.get(0);
                a.remove(0);

                JSONArray argSettingArr = (JSONArray) argsSetting.get("args");
                int citySetting[] = new int[argSettingArr.size()];
                for(int i=0;i<argSettingArr.size();i++){
                    citySetting[i]=(Integer.parseInt(argSettingArr.get(i).toString()));
                }
                g = new LongJump(citySetting);

                for (Object o : a)
                {
                    JSONObject person = (JSONObject) o;
                    String func =  person.get("func").toString();
                    JSONArray arg = (JSONArray) person.get("args");

                    switch(func){
                        case "virusPlan":
                            g.virusAttackPlan(Integer.parseInt(arg.get(0).toString()),
                                    Integer.parseInt(arg.get(1).toString()));
                            break;
                        case "TravelPlan":
                            g.TravelPlan(Integer.parseInt(arg.get(0).toString()),Integer.parseInt(arg.get(1).toString()),Integer.parseInt(arg.get(2).toString()),
                                    Integer.parseInt(arg.get(3).toString()),Integer.parseInt(arg.get(4).toString()));
                            break;

                        case "CityMax":
                            count++;
                            int ans_sol = g.CityWithTheMostPatient(Integer.parseInt(arg.get(0).toString()));
                            Long answer = (Long) person.get("answer");
                            int ans = Integer.parseInt(answer.toString());
                            if(ans_sol==ans){
                                System.out.println(count+": AC");
                            }else{
                                waSize++;
                                System.out.println(count+": WA");
                            }
                    }

                }
            }
            System.out.println("Score: " + (count-waSize) + " / " + count + " ");
        }catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (ParseException e) {
            e.printStackTrace();
        }
    }

}