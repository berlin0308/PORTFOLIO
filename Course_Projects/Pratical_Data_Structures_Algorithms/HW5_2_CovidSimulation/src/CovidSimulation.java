// import java.io.FileNotFoundException;
// import java.io.FileReader;
// import java.io.IOException;

// import org.json.simple.JSONArray;
// import org.json.simple.JSONObject;
// import org.json.simple.parser.JSONParser;
// import org.json.simple.parser.ParseException;

import edu.princeton.cs.algs4.MinPQ;
import java.util.Arrays;
import java.util.Comparator;

class Event {
    public int EventDate;
    public String EventType;
    public int[] info;
    public int Attack_City;
    public int NumOfTraveller;
    public int FromCity;
    public int ToCity;
    public int ArriveDate;
    public int Travelers_Recovery;
    public int PRIORITY;

    Event(int Date, String Type, int[] Info){
        EventType=Type;
        EventDate=Date;
        info=Info;
        if(EventType=="VirusAttack"){
            PRIORITY = 3;
            Attack_City = info[0];
        }
        if(EventType=="TravelDepart"){
            PRIORITY = 1;
            NumOfTraveller = info[0];
            FromCity = info[1];
            ToCity = info[2];
            ArriveDate = info[3];
        }
        if(EventType=="TravelArrive"){
            PRIORITY = 2;
            NumOfTraveller = info[0];
            ToCity = info[1];
            Travelers_Recovery = info[2];
        }
    }

    public final Comparator<Event> BYDATE = new byDate();
    private class byDate implements Comparator<Event>{
        public int compare(Event A,Event B){
            if(A.EventDate>B.EventDate) return +1;
            else if(A.EventDate<B.EventDate) return -1;
            else{
                if(A.PRIORITY>B.PRIORITY) return -1;
                else return +1;
            }
        }
    }
    
}


class CovidSimulation {
    private MinPQ<Event> CovidEventPQ;
    int[] City_Population;
    int[] City_RecoveryDate;
    int[] City_MaxRecoveryDate;
    private int day;
    
    public CovidSimulation(int[] Num_Of_Citizen) {
        City_Population = Num_Of_Citizen;
        City_RecoveryDate = new int[Num_Of_Citizen.length];
        Arrays.fill(City_RecoveryDate,0);
        City_MaxRecoveryDate = new int[Num_Of_Citizen.length];
        Arrays.fill(City_MaxRecoveryDate,0);
        Event A = new Event(0, null, null);
        CovidEventPQ = new MinPQ<Event>(A.BYDATE);
        day=1;
    }

    public void virusAttackPlan(int city, int date){
        Event E = new Event(date, "VirusAttack", new int[]{city});
        CovidEventPQ.insert(E);
    }
    
    public void TravelPlan(int NumberOfTraveller, int FromCity, int ToCity, int DateOfDeparture, int DateOfArrival){
        Event E = new Event(DateOfDeparture, "TravelDepart", new int[]{NumberOfTraveller,FromCity,ToCity,DateOfArrival});
        CovidEventPQ.insert(E);
        
    }

    public int CityWithTheMostPatient(int date){
        
        int N = City_Population.length;
   
        // System.out.print("\n\n--------\nCityWithTheMostPatient() called!!!\n");
        // System.out.print("\ndate:");
        // System.out.println(date);
        // System.out.print("\nFrom Day: ");
        // System.out.println(day);
        // System.out.print("City_Population: ");
        // System.out.println(Arrays.toString(City_Population));
        // System.out.print("City_RecoveryDate: ");
        // System.out.println(Arrays.toString(City_RecoveryDate));
        // System.out.print("City_MaxRecoveryDate: ");
        // System.out.println(Arrays.toString(City_MaxRecoveryDate));
        // System.out.println(CovidEventPQ.size());
        // System.out.print("\n--------\n\n");
        
        // displayEventPQ();
        /* Process the Events of each day */
        while(day<=date){
            
            // for(int i=0;i<N;i++){
            //     if(City_RecoveryDate[i]==day)
            //         City_RecoveryDate[i]=0;
            // }

            while(CovidEventPQ.size()>0 && CovidEventPQ.min().EventDate==day){ // if the Event happens on this day
                Event thisEvent = CovidEventPQ.delMin();
                // System.out.print("\nProcess Event - ");
                // System.out.println(thisEvent.EventType);
                if(thisEvent.EventType=="VirusAttack"){
                    if(City_RecoveryDate[thisEvent.Attack_City]<=day){ // the City is not infected
                        City_RecoveryDate[thisEvent.Attack_City]=day+4;
                        City_MaxRecoveryDate[thisEvent.Attack_City]=day+7;
                    }
                }
                if(thisEvent.EventType=="TravelDepart"){
                    // Travellers leave
                    City_Population[thisEvent.FromCity] -= thisEvent.NumOfTraveller;
                    
                    // Record the info of the travellers, insert an Event of "TravelArrive" 
                    Event E = new Event(thisEvent.ArriveDate, "TravelArrive"
                    ,new int[]{thisEvent.NumOfTraveller,thisEvent.ToCity,City_RecoveryDate[thisEvent.FromCity]});
                    CovidEventPQ.insert(E);
                }
                
                if(thisEvent.EventType=="TravelArrive"){
                    // Travellers arrive
                    City_Population[thisEvent.ToCity] += thisEvent.NumOfTraveller;
                    if(thisEvent.Travelers_Recovery>day){ // arrived travellers is infected at that time
                        
                        if(City_RecoveryDate[thisEvent.ToCity]>day){ // the City is infected
                            
                            if(thisEvent.Travelers_Recovery>City_RecoveryDate[thisEvent.ToCity]){ // extend the Recovery Date by the arrived travellers
                                if(thisEvent.Travelers_Recovery<=City_MaxRecoveryDate[thisEvent.ToCity]){ // not beyond the max-7-day
                                    City_RecoveryDate[thisEvent.ToCity] = thisEvent.Travelers_Recovery;    
                                }
                                else{
                                    City_RecoveryDate[thisEvent.ToCity] = City_MaxRecoveryDate[thisEvent.ToCity];    
                                }

                                // City_RecoveryDate[thisEvent.ToCity] = Math.min(thisEvent.Travelers_Recovery,City_MaxRecoveryDate[thisEvent.ToCity]);
                                // System.out.println(City_MaxRecoveryDate[thisEvent.ToCity]);
                            }
                        }
                        else{ // the City is not infected
                            City_RecoveryDate[thisEvent.ToCity] = day+4;
                            City_MaxRecoveryDate[thisEvent.ToCity] = day+7;
                        }
                    }
                }
            }

            // /* The day ends */
            // System.out.print("\nDay: ");
            // System.out.println(day);
            // System.out.print("City_Population: ");
            // System.out.println(Arrays.toString(City_Population));
            // System.out.print("City_RecoveryDate: ");
            // System.out.println(Arrays.toString(City_RecoveryDate));
            // System.out.print("City_MaxRecoveryDate: ");
            // System.out.println(Arrays.toString(City_MaxRecoveryDate));
            
            day++;
            
        }
        
        // System.out.print("-------------\nEnd at Day: ");
        // System.out.println(day);
        // System.out.print("City_Population: ");
        // System.out.println(Arrays.toString(City_Population));
        // System.out.print("City_RecoveryDate: ");
        // System.out.println(Arrays.toString(City_RecoveryDate));
        // System.out.print("-------------\n");

        /* Find the City with most patients */
        int CityWithTheMostPatient=-1;
        int MaxPatient=0;
        for(int i=0;i<N;i++){
            if(City_RecoveryDate[i]>date){ // infected
                if(City_Population[i]>MaxPatient){
                    MaxPatient = City_Population[i];
                    CityWithTheMostPatient = i;
                }
                else if(City_Population[i]==MaxPatient){
                    if(i>CityWithTheMostPatient){
                        CityWithTheMostPatient = i;
                    }
                }
            }
        }
        // System.out.print("CityWithTheMostPatient: ");
        // System.out.println(CityWithTheMostPatient);
        // System.out.print("MaxPatient: ");
        // System.out.println(MaxPatient);
        // System.out.println("\n\n");


        return CityWithTheMostPatient;
    }

    public void displayEventPQ(){
        MinPQ<Event> Events = new MinPQ<Event>();
        Events = CovidEventPQ;

        while(Events.size()!=0){
            Event Min = Events.delMin();
            System.out.print(Min.EventDate);
            System.out.print(" ");
            System.out.print(Min.EventType);
            System.out.print(" ");
            System.out.println(Arrays.toString(Min.info));
        }
    }
  
    public static void main(String[] args) {
        // test t = new test(args);
        // CovidSimulation sol = new CovidSimulation(new int[] {10, 100, 15, 25, 10, 13});
        
        // sol.virusAttackPlan(0, 1);
        // sol.virusAttackPlan(4, 3);
        // sol.TravelPlan(3, 0, 3, 3, 4);
        // sol.TravelPlan(3, 4, 0, 3, 4); 
        
        // System.out.println(sol.CityWithTheMostPatient(2));
        // // output = 0
        
        // sol.virusAttackPlan(5, 5);
        // sol.TravelPlan(1, 5, 0, 5, 6); 
       
        // System.out.println(sol.CityWithTheMostPatient(4));
        // // output = 3
        // System.out.println(sol.CityWithTheMostPatient(8));
        // // output = 5
        
        //day 1:{10, 100, 15, 25, 10, 13}
        //infectedList:{1, 0, 0, 0, 0, 0}
        //day 2：{10, 100, 15, 25, 10, 13}
        //infectedList:{1, 0, 0, 0, 0, 0}
        //day 3：{7, 100, 15, 25, 7, 13}
        //infectedList:{1, 0, 0, 0, 1, 0}
        //day 4：{10, 100, 15, 28, 7, 13}
        //infectedList:{1, 0, 0, 1, 1, 0}
        //day 5：{10, 100, 15, 28, 7, 12}
        //infectedList:{1, 0, 0, 1, 1, 1}
        //day 6：{11, 100, 15, 28, 7, 12}
        //infectedList:{1, 0, 0, 1, 1, 1}
        //day 7：{11, 100, 15, 28, 7, 12}
        //infectedList:{1, 0, 0, 1, 0, 1}
        //day 8：{11, 100, 15, 28, 7, 12}
        //infectedList:{0, 0, 0, 0, 0, 1}

        //----virus and recovery test----
    //4 days recover for attack
        // CovidSimulation sol = new CovidSimulation(new int[] {5, 5, 5, 5, 5});
        // sol.virusAttackPlan(1, 1);
        
        //MaxRecoveryDate     |     NumOfCitizen
        //1： MostPatient: 1
        //0, 5, 0, 0, 0,  |  5, 5, 5, 5, 5,
        //
        //2： MostPatient: 1
        //0, 5, 0, 0, 0,  |  5, 5, 5, 5, 5,
        //
        //3： MostPatient: 1
        //0, 5, 0, 0, 0,  |  5, 5, 5, 5, 5,
        //
        //4： MostPatient: 1
        //0, 5, 0, 0, 0,  |  5, 5, 5, 5, 5,
        //
        //5： MostPatient: -1
        //0, 0, 0, 0, 0,  |  5, 5, 5, 5, 5,
        //pass
    //4 days recover for in coming infected traveller.
        // CovidSimulation sol = new CovidSimulation(new int[] {5, 5, 5, 5, 5});
        // sol.virusAttackPlan(1, 1);
        // sol.TravelPlan(1, 1, 2, 2, 3);
        //MaxRecoveryDate     |     NumOfCitizen
        //1： MostPatient: 1
        //0, 5, 0, 0, 0,  |  5, 5, 5, 5, 5,
        //
        //2： MostPatient: 1
        //0, 5, 0, 0, 0,  |  5, 4, 5, 5, 5,
        //
        //3： MostPatient: 2
        //0, 5, 7, 0, 0,  |  5, 4, 6, 5, 5,
        //
        //4： MostPatient: 2
        //0, 5, 7, 0, 0,  |  5, 4, 6, 5, 5,
        //
        //5： MostPatient: 2
        //0, 0, 7, 0, 0,  |  5, 4, 6, 5, 5,
        //
        //6： MostPatient: 2
        //0, 0, 7, 0, 0,  |  5, 4, 6, 5, 5,
        //
        //7： MostPatient: -1
        //0, 0, 0, 0, 0,  |  5, 4, 6, 5, 5,
        //pass
        //infected city: in coming with more recent virus
        // CovidSimulation sol = new CovidSimulation(new int[] {5, 5, 5, 5, 5});
        // sol.virusAttackPlan(1, 1);
        // sol.virusAttackPlan(2, 2);
        // sol.TravelPlan(1, 2, 1, 2, 3);
        //MaxRecoveryDate     |     NumOfCitizen
        //1： MostPatient: 1
        //0, 5, 0, 0, 0,  |  5, 5, 5, 5, 5,
        //
        //2： MostPatient: 1
        //0, 5, 6, 0, 0,  |  5, 5, 4, 5, 5,
        //
        //3： MostPatient: 1
        //0, 6, 6, 0, 0,  |  5, 6, 4, 5, 5,
        //
        //4： MostPatient: 1
        //0, 6, 6, 0, 0,  |  5, 6, 4, 5, 5,
        //
        //5： MostPatient: 1
        //0, 6, 6, 0, 0,  |  5, 6, 4, 5, 5,
        //
        //6： MostPatient: -1
        //0, 0, 0, 0, 0,  |  5, 6, 4, 5, 5,
        //pass
        //infected city: in coming less recent
        // CovidSimulation sol = new CovidSimulation(new int[] {5, 5, 5, 5, 5});
        // sol.virusAttackPlan(1, 1);
        // sol.virusAttackPlan(2, 2);
        // sol.TravelPlan(1, 1, 2, 2, 3);
        //MaxRecoveryDate     |     NumOfCitizen
        //1： MostPatient: 1
        //0, 5, 0, 0, 0,  |  5, 5, 5, 5, 5,
        //
        //2： MostPatient: 2
        //0, 5, 6, 0, 0,  |  5, 4, 5, 5, 5,
        //
        //3： MostPatient: 2
        //0, 5, 6, 0, 0,  |  5, 4, 6, 5, 5,
        //
        //4： MostPatient: 2
        //0, 5, 6, 0, 0,  |  5, 4, 6, 5, 5,
        //
        //5： MostPatient: 2
        //0, 0, 6, 0, 0,  |  5, 4, 6, 5, 5,
        //
        //6： MostPatient: -1
        //0, 0, 0, 0, 0,  |  5, 4, 6, 5, 5,
        //pass
        //infected city: in coming same recovery
        // CovidSimulation sol = new CovidSimulation(new int[] {5, 5, 5, 5, 5});
        // sol.virusAttackPlan(1, 1);
        // sol.virusAttackPlan(2, 1);
        // sol.TravelPlan(1, 1, 2, 2, 3);
        //MaxRecoveryDate     |     NumOfCitizen
        //1： MostPatient: 2
        //0, 5, 5, 0, 0,  |  5, 5, 5, 5, 5,
        //
        //2： MostPatient: 2
        //0, 5, 5, 0, 0,  |  5, 4, 5, 5, 5,
        //
        //3： MostPatient: 2
        //0, 5, 5, 0, 0,  |  5, 4, 6, 5, 5,
        //
        //4： MostPatient: 2
        //0, 5, 5, 0, 0,  |  5, 4, 6, 5, 5,
        //
        //5： MostPatient: -1
        //0, 0, 0, 0, 0,  |  5, 4, 6, 5, 5,
        //pass
        //infected city: 7day max recovery
        // CovidSimulation sol = new CovidSimulation(new int[] {5, 5, 5, 5, 5});
        // sol.virusAttackPlan(1, 1);
        // sol.virusAttackPlan(2, 3);
        // sol.virusAttackPlan(3, 5);
        // sol.TravelPlan(1, 2, 1, 3, 4);
        // sol.TravelPlan(1, 3, 1, 5, 6);
        //MaxRecoveryDate     |     NumOfCitizen
        //1： MostPatient: 1
        //0, 5, 0, 0, 0,  |  5, 5, 5, 5, 5,
        //
        //2： MostPatient: 1
        //0, 5, 0, 0, 0,  |  5, 5, 5, 5, 5,
        //
        //3： MostPatient: 1
        //0, 5, 7, 0, 0,  |  5, 5, 4, 5, 5,
        //
        //4： MostPatient: 1
        //0, 7, 7, 0, 0,  |  5, 6, 4, 5, 5,
        //
        //5： MostPatient: 1
        //0, 7, 7, 9, 0,  |  5, 6, 4, 4, 5,
        //
        //6： MostPatient: 1
        //0, 8, 7, 9, 0,  |  5, 7, 4, 4, 5,
        //
        //7： MostPatient: 1
        //0, 8, 0, 9, 0,  |  5, 7, 4, 4, 5,
        //
        //8： MostPatient: 3
        //0, 0, 0, 9, 0,  |  5, 7, 4, 4, 5,
        //
        //9： MostPatient: -1
        //0, 0, 0, 0, 0,  |  5, 7, 4, 4, 5,
        //pass
    //infected city: 8th day infected (infected after recovery)
        // CovidSimulation sol = new CovidSimulation(new int[] {5, 5, 5, 5, 5});
        // sol.virusAttackPlan(1, 1);
        // sol.virusAttackPlan(2, 3);
        // sol.virusAttackPlan(3, 5);
        // sol.virusAttackPlan(1, 8);
        // sol.TravelPlan(1, 2, 1, 3, 4);
        // sol.TravelPlan(1, 3, 1, 5, 6);
        // System.out.println(sol.CityWithTheMostPatient(6));
        // System.out.println(sol.CityWithTheMostPatient(7));
        // System.out.println(sol.CityWithTheMostPatient(8));
        // System.out.println(sol.CityWithTheMostPatient(9));
        // System.out.println(sol.CityWithTheMostPatient(10));
        // System.out.println(sol.CityWithTheMostPatient(11));
        // System.out.println(sol.CityWithTheMostPatient(12));
        //MaxRecoveryDate     |     NumOfCitizen
        //1： MostPatient: 1
        //0, 5, 0, 0, 0,  |  5, 5, 5, 5, 5,
        //
        //2： MostPatient: 1
        //0, 5, 0, 0, 0,  |  5, 5, 5, 5, 5,
        //
        //3： MostPatient: 1
        //0, 5, 7, 0, 0,  |  5, 5, 4, 5, 5,
        //
        //4： MostPatient: 1
        //0, 7, 7, 0, 0,  |  5, 6, 4, 5, 5,
        //
        //5： MostPatient: 1
        //0, 7, 7, 9, 0,  |  5, 6, 4, 4, 5,
        //
        //6： MostPatient: 1
        //0, 8, 7, 9, 0,  |  5, 7, 4, 4, 5,
        //
        //7： MostPatient: 1
        //0, 8, 0, 9, 0,  |  5, 7, 4, 4, 5,
        //
        //8： MostPatient: 1
        //0, 12, 0, 9, 0,  |  5, 7, 4, 4, 5,
        //
        //9： MostPatient: 1
        //0, 12, 0, 0, 0,  |  5, 7, 4, 4, 5,
        //
        //10： MostPatient: 1
        //0, 12, 0, 0, 0,  |  5, 7, 4, 4, 5,
        //
        //11： MostPatient: 1
        //0, 12, 0, 0, 0,  |  5, 7, 4, 4, 5,
        //
        //12： MostPatient: -1
        //0, 0, 0, 0, 0,  |  5, 7, 4, 4, 5,
        //pass.
    //virus attack infected city, no effect test.
    // CovidSimulation sol = new CovidSimulation(new int[] {5, 5, 5, 5, 5});
    // sol.virusAttackPlan(1, 1);
    // for(int i=1;i<5;i++){
        //     sol.virusAttackPlan(1, i);
        // }
        // System.out.println(sol.CityWithTheMostPatient(5));
        //MaxRecoveryDate     |     NumOfCitizen
        //1： MostPatient: 1
        //0, 5, 0, 0, 0,  |  5, 5, 5, 5, 5,
        //
        //2： MostPatient: 1
        //0, 5, 0, 0, 0,  |  5, 5, 5, 5, 5,
        //
        //3： MostPatient: 1
        //0, 5, 0, 0, 0,  |  5, 5, 5, 5, 5,
        //
        //4： MostPatient: 1
        //0, 5, 0, 0, 0,  |  5, 5, 5, 5, 5,
        //
        //5： MostPatient: -1
        //0, 0, 0, 0, 0,  |  5, 5, 5, 5, 5,
        //pass
        
        //----travel test----
        //infected before departure.
        // CovidSimulation sol = new CovidSimulation(new int[] {5, 5, 5, 5, 5});
        // sol.virusAttackPlan(1, 1);
        // sol.virusAttackPlan(2, 2);
        // sol.TravelPlan(1, 2, 1, 2, 3);
        //MaxRecoveryDate     |     NumOfCitizen
        //1： MostPatient: 1
        //0, 5, 0, 0, 0,  |  5, 5, 5, 5, 5,
        //
        //2： MostPatient: 1
        //0, 5, 6, 0, 0,  |  5, 5, 4, 5, 5,
        //
        //3： MostPatient: 1
        //0, 6, 6, 0, 0,  |  5, 6, 4, 5, 5,
        //
        //4： MostPatient: 1
        //0, 6, 6, 0, 0,  |  5, 6, 4, 5, 5,
        //
        //5： MostPatient: 1
        //0, 6, 6, 0, 0,  |  5, 6, 4, 5, 5,
        //
        //6： MostPatient: -1
        //0, 0, 0, 0, 0,  |  5, 6, 4, 5, 5,
        //pass
    //Recover before arrival
        // CovidSimulation sol = new CovidSimulation(new int[] {5, 5, 5, 5, 5});
        // sol.virusAttackPlan(1, 1);
        // sol.TravelPlan(1, 1, 2, 1, 5);
        //MaxRecoveryDate     |     NumOfCitizen
        //1： MostPatient: 1
        //0, 5, 0, 0, 0,  |  5, 4, 5, 5, 5,
        //
        //2： MostPatient: 1
        //0, 5, 0, 0, 0,  |  5, 4, 5, 5, 5,
        //
        //3： MostPatient: 1
        //0, 5, 0, 0, 0,  |  5, 4, 5, 5, 5,
        //
        //4： MostPatient: 1
        //0, 5, 0, 0, 0,  |  5, 4, 5, 5, 5,
        //
        //5： MostPatient: -1
        //0, 0, 0, 0, 0,  |  5, 4, 6, 5, 5,
        //pass
        //traveller not part of any city
        // CovidSimulation sol = new CovidSimulation(new int[] {5, 5, 5, 5, 5});
        // sol.virusAttackPlan(1, 1);
        // sol.TravelPlan(1, 1, 2, 1, 5);
        //MaxRecoveryDate     |     NumOfCitizen
        //1： MostPatient: 1
        //0, 5, 0, 0, 0,  |  5, 4, 5, 5, 5,
        //
        //2： MostPatient: 1
        //0, 5, 0, 0, 0,  |  5, 4, 5, 5, 5,
        //
        //3： MostPatient: 1
        //0, 5, 0, 0, 0,  |  5, 4, 5, 5, 5,
        //
        //4： MostPatient: 1
        //0, 5, 0, 0, 0,  |  5, 4, 5, 5, 5,
        //
        //5： MostPatient: -1
        //0, 0, 0, 0, 0,  |  5, 4, 6, 5, 5,
        //pass
        //travel after recover
        // CovidSimulation sol = new CovidSimulation(new int[] {5, 5, 5, 5, 5});
        // sol.virusAttackPlan(1, 1);
        // sol.TravelPlan(1, 1, 2, 5, 6);
        //MaxRecoveryDate     |     NumOfCitizen
        //1： MostPatient: 1
        //0, 5, 0, 0, 0,  |  5, 5, 5, 5, 5,
        //
        //2： MostPatient: 1
        //0, 5, 0, 0, 0,  |  5, 5, 5, 5, 5,
        //
        //3： MostPatient: 1
        //0, 5, 0, 0, 0,  |  5, 5, 5, 5, 5,
        //
        //4： MostPatient: 1
        //0, 5, 0, 0, 0,  |  5, 5, 5, 5, 5,
        //
        //5： MostPatient: -1
        //0, 0, 0, 0, 0,  |  5, 4, 5, 5, 5,
        //
        //6： MostPatient: -1
        //0, 0, 0, 0, 0,  |  5, 4, 6, 5, 5,
    //MostPatient:
        // CovidSimulation sol = new CovidSimulation(new int[] {11,9, 8, 20, 1});
        // sol.virusAttackPlan(1, 1);
        // sol.virusAttackPlan(2, 2);
        // sol.virusAttackPlan(3, 3);
        // sol.virusAttackPlan(4, 4);
        // sol.virusAttackPlan(0, 5);
        //MaxRecoveryDate     |     NumOfCitizen
        //1： MostPatient: 1
        //0, 5, 0, 0, 0,  |  11, 9, 8, 20, 1,
        //
        //2： MostPatient: 1
        //0, 5, 6, 0, 0,  |  11, 9, 8, 20, 1,
        //
        //3： MostPatient: 3
        //0, 5, 6, 7, 0,  |  11, 9, 8, 20, 1,
        //
        //4： MostPatient: 3
        //0, 5, 6, 7, 8,  |  11, 9, 8, 20, 1,
        //
        //5： MostPatient: 3
        //9, 0, 6, 7, 8,  |  11, 9, 8, 20, 1,
        //
        //6： MostPatient: 3
        //9, 0, 0, 7, 8,  |  11, 9, 8, 20, 1,
        //
        //7： MostPatient: 0
        //9, 0, 0, 0, 8,  |  11, 9, 8, 20, 1,
        //
        //8： MostPatient: 0
        //9, 0, 0, 0, 0,  |  11, 9, 8, 20, 1,
        //
        //9： MostPatient: -1
        //0, 0, 0, 0, 0,  |  11, 9, 8, 20, 1,
        //pass
    //MostPatient multiple same most patient:
        // CovidSimulation sol = new CovidSimulation(new int[] {11,11, 11, 11, 11});
        // sol.virusAttackPlan(0, 1);
        // sol.virusAttackPlan(1, 2);
        // sol.virusAttackPlan(2, 3);
        // sol.virusAttackPlan(3, 4);
        // sol.virusAttackPlan(4, 5);
        // System.out.println(sol.CityWithTheMostPatient(1));
        // System.out.println(sol.CityWithTheMostPatient(2));
        // System.out.println(sol.CityWithTheMostPatient(3));
        // System.out.println(sol.CityWithTheMostPatient(4));
        // System.out.println(sol.CityWithTheMostPatient(5));
        // System.out.println(sol.CityWithTheMostPatient(6));
        // System.out.println(sol.CityWithTheMostPatient(7));
        // System.out.println(sol.CityWithTheMostPatient(8));
        // System.out.println(sol.CityWithTheMostPatient(9));
        //MaxRecoveryDate     |     NumOfCitizen
        //1： MostPatient: 0
        //5, 0, 0, 0, 0,  |  11, 11, 11, 11, 11,
        //
        //2： MostPatient: 1
        //5, 6, 0, 0, 0,  |  11, 11, 11, 11, 11,
        //
        //3： MostPatient: 2
        //5, 6, 7, 0, 0,  |  11, 11, 11, 11, 11,
        //
        //4： MostPatient: 3
        //5, 6, 7, 8, 0,  |  11, 11, 11, 11, 11,
        //
        //5： MostPatient: 4
        //0, 6, 7, 8, 9,  |  11, 11, 11, 11, 11,
        //
        //6： MostPatient: 4
        //0, 0, 7, 8, 9,  |  11, 11, 11, 11, 11,
        //
        //7： MostPatient: 4
        //0, 0, 0, 8, 9,  |  11, 11, 11, 11, 11,
        //
        //8： MostPatient: 4
        //0, 0, 0, 0, 9,  |  11, 11, 11, 11, 11,
        //
        //9： MostPatient: -1
        //0, 0, 0, 0, 0,  |  11, 11, 11, 11, 11,
        //pass
    }
}

// class test {
//     public test(String[] args) {
//         CovidSimulation g;
//         JSONParser jsonParser = new JSONParser();
//         try (FileReader reader = new FileReader("C:\\Users\\BERLIN CHEN\\Desktop\\2022PDSA\\HW5_2_CovidSimulation\\test_data.json")){
//             JSONArray all = (JSONArray) jsonParser.parse(reader);
//             int waSize = 0;
//             int count = 0;
//             for(Object CaseInList : all){
//                 JSONArray a = (JSONArray) CaseInList;
//                 //Board Setup
//                 JSONObject argsSetting = (JSONObject) a.get(0);
//                 a.remove(0);

//                 JSONArray argSettingArr = (JSONArray) argsSetting.get("args");
//                 int citySetting[] = new int[argSettingArr.size()];
//                 for(int i=0;i<argSettingArr.size();i++){
//                     citySetting[i]=(Integer.parseInt(argSettingArr.get(i).toString()));
//                 }
//                 g = new CovidSimulation(citySetting);

//                 for (Object o : a)
//                 {
//                     JSONObject person = (JSONObject) o;
//                     String func =  person.get("func").toString();
//                     JSONArray arg = (JSONArray) person.get("args");

//                     switch(func){
//                         case "virusPlan":
//                             g.virusAttackPlan(Integer.parseInt(arg.get(0).toString()),
//                                     Integer.parseInt(arg.get(1).toString()));
//                             break;
//                         case "TravelPlan":
//                             g.TravelPlan(Integer.parseInt(arg.get(0).toString()),Integer.parseInt(arg.get(1).toString()),Integer.parseInt(arg.get(2).toString()),
//                                     Integer.parseInt(arg.get(3).toString()),Integer.parseInt(arg.get(4).toString()));
//                             break;

//                         case "CityMax":
//                             count++;
//                             int ans_sol = g.CityWithTheMostPatient(Integer.parseInt(arg.get(0).toString()));
//                             Long answer = (Long) person.get("answer");
//                             int ans = Integer.parseInt(answer.toString());
//                             if(ans_sol==ans){
//                                 System.out.println(count+": AC");
//                             }else{
//                                 waSize++;
//                                 System.out.println(count+": WA");
//                             }
//                     }

//                 }
//             }
//             System.out.println("Score: " + (count-waSize) + " / " + count + " ");
//         }catch (FileNotFoundException e) {
//             e.printStackTrace();
//         } catch (IOException e) {
//             e.printStackTrace();
//         } catch (ParseException e) {
//             e.printStackTrace();
//         }
//     }

// }