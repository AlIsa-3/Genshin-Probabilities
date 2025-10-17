import java.util.Random;
import java.util.Scanner;

public class Simulation {


    // Define Simulation Parameters
    public int wish_count;
    public int target_5_star_count;
    public int current_pity;
    public int banner_pity;
    public int simulation_count;
    public int CR_score;
    public boolean isGuaranteed;
    

    private boolean soft_pity(){

        int soft_pity_value = banner_pity - current_pity;
        Random rng = new Random(System.currentTimeMillis());
        
        int true_weight = 6 * (1 + 16 - soft_pity_value);

        if (soft_pity_value <= 16){
            // Weighted Random
            int soft_pity_int = rng.nextInt(101);
            return soft_pity_int <= true_weight;
        }
        else{
            // If the selected integer is a specific value --> got a 5-star
            int chosen_int = rng.nextInt(1000);
            return chosen_int == 6;
        }
    }

    private boolean capturing_radiance(){
        if (CR_score == 3){
            CR_score = 1;
            return true;
        }
        else{
            CR_score += 1;
            return false;
        }
    }

    private boolean fifty_fifty(){
        Random rng = new Random(System.currentTimeMillis());
        int num = rng.nextInt(2);

        boolean choice = (num == 1);

        if (choice == false){
            // Try capturing radiance
            choice = capturing_radiance();
        }

        return choice;
    }


    private boolean five_star(){
        boolean isLimited;

        // Reset Pity
        current_pity = 0;

        if (isGuaranteed){
            
            isGuaranteed = false;
            isLimited = true;
        }
        else{
            isLimited = fifty_fifty();
            isGuaranteed = !isLimited;
        }
        return isLimited;
    }


    private boolean one_wish(){
        boolean isLimited = false;

        // Check if reached pity or soft pity
        if (current_pity == banner_pity | soft_pity()){
            return five_star();
        }
        else{
            current_pity += 1;
            return isLimited;
        }

    }

    private boolean one_run(){
        int limited_count = 0;
        for (int i = 0; i < wish_count; i++){

            limited_count += (one_wish()) ? 1 : 0;

        }
        return limited_count >= target_5_star_count;
    }


    private double simulation(){

        int original_CR_score = CR_score;
        int original_current_pity = current_pity;
        boolean original_isGuaranteed = isGuaranteed;
        
        double successes = 0;

        for (int i = 0; i<simulation_count; i++){

            successes += (one_run()) ? 1 : 0;

            CR_score = original_CR_score;
            current_pity = original_current_pity;
            isGuaranteed = original_isGuaranteed;

        }
        return successes / simulation_count;
    }


    private void display_results(double probability){

        String outputString = "The probability of getting %d limited 5-stars in %d wishes is approximately %.2f%% (Calculated using %d simulations)";

        outputString = String.format(outputString,target_5_star_count,wish_count,probability*100,simulation_count);

        System.out.println(outputString);

    }

    private Simulation(){
        try (Scanner input = new Scanner(System.in)) {
            System.out.print("Enter the number of wishes: ");
            wish_count = Integer.parseInt(input.nextLine());
            
            System.out.print("Enter the target number of limited 5-stars: ");
            target_5_star_count = Integer.parseInt(input.nextLine());
            
            System.out.print("Enter the current pity: ");
            current_pity = Integer.parseInt(input.nextLine());
            
            System.out.print("Enter the banner pity: ");
            banner_pity = Integer.parseInt(input.nextLine());
            
            System.out.print("Is it Guaranteed, Y/N: ");
            isGuaranteed = ("Y".equals(input.nextLine().toUpperCase()));
            
            
            System.out.print("How many simulations: ");
            simulation_count = Integer.parseInt(input.nextLine());
        }

        
    }

    private Simulation(String[] args){

            wish_count = Integer.parseInt(args[0]);
            target_5_star_count = Integer.parseInt(args[1]);
            current_pity = Integer.parseInt(args[2]);
            banner_pity = Integer.parseInt(args[3]);
            isGuaranteed = ("Y".equals(args[4].toUpperCase()));
            simulation_count = Integer.parseInt(args[5]);


        }

    private void run(){

        double probability = simulation();
        display_results(probability);


        
    }
    
    public static void main(String[] args) {
        Simulation sim;

        if (args.length < 6){  
            sim = new Simulation();
        }
        else{
            sim = new Simulation(args);
        }

        sim.run();
    }
}
