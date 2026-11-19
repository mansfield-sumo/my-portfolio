#include<stdio.h>
#include<time.h>     // Needed for date/time

// Helper function to clear the keyboard memory
void clear_buffer() {
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
}

int main(void){

    int admin_pin = 2026;
    int entered_pin;
    int rate_choice;           
    float tax_rate = 0.15;

    // Variables to track daily totals
    float daily_total_revenue = 0.0;
    float daily_total_tax = 0.0;

    // --- 1. ADMIN LOGIN GATE ---
    printf("=== SYSTEM LOCKED ===\n");
    printf("Enter 4-digit Administrator PIN to unlock device: ");
    scanf("%d", &entered_pin);
    clear_buffer(); 
    
    if (entered_pin != admin_pin) {
        printf("\nACCESS DENIED: Incorrect PIN. Security incident logged.\n");
        printf("Terminal shutting down...\n");
        return 0; 
    }

    printf("\nAccess Granted! Welcome, Supervisor.\n");
    
    // --- 2. CHOICE MENU ---
    printf("Current tax rate is: %.2f (%.0f%%)\n", tax_rate, tax_rate * 100);
    printf("Do you want to change the tax rate for today?\n");
    printf("1. Yes, enter a new rate\n");
    printf("2. No, skip and use current rate\n");
    printf("Enter choice (1 or 2): ");
    scanf("%d", &rate_choice);
    clear_buffer(); 

    if (rate_choice == 1) {
        printf("\nEnter today's Official tax rate (eg. 0.18 for 18%% tax): ");
        scanf("%f", &tax_rate);
        clear_buffer(); 
        printf("Tax rate successfully updated to %.2f.\n", tax_rate);
    } 
    else {
        printf("\nSkipping. Keeping the current rate of %.2f (%.0f%%).\n", tax_rate, tax_rate * 100);
    }

    printf("\n--- SYSTEM READY FOR SHIPMENTS ---\n");

    // Append to file (keep old receipts)
    FILE *receipt_file = fopen("receipts.txt", "a");
    if (receipt_file == NULL) {
        printf("Error: Could not open receipts.txt for writing.\n");
        return 1; 
    }

    int keep_running = 1; 
    int merchant_count = 1;

    // --- 3. MAIN LOOP ---
    while (keep_running == 1) {
        
        int merchant_id;
        char merchant_name[100];       
        char contact_number[20];       
        
        int bags_of_rice = 0; 
        float price_per_bag_lrd = 0.0;
        float current_tax_rate = tax_rate; 

        printf("\n===FREEPORT OF MONROVIA: LIVE TAX TERMINAL (Merchant #%d)===\n", merchant_count);
        
        printf("Enter Merchant ID (numbers only): ");
        scanf("%d", &merchant_id);
        clear_buffer(); 
        
        printf("Enter Merchant Name: ");
        scanf("%[^\n]", merchant_name); 
        clear_buffer();
        
        printf("Enter Contact Number: ");
        scanf("%[^\n]", contact_number);
        clear_buffer();

        do {
            printf("Enter number of rice bags: ");
            scanf("%d", &bags_of_rice);
            clear_buffer();
            if (bags_of_rice <= 0) printf("Error: Bags must be greater than 0. Try again.\n");
        } while (bags_of_rice <= 0);

        do {
            printf("Enter price per bag in LRD: ");
            scanf("%f", &price_per_bag_lrd);
            clear_buffer();
            if (price_per_bag_lrd <= 0) printf("Error: Price must be greater than 0. Try again.\n");
        } while (price_per_bag_lrd <= 0);

        // --- 4. DECISION LOGIC ---
        if (bags_of_rice >= 10000){
           current_tax_rate = 0.08;                  
           printf("\nTier: Mega Shipment (8%% tax applied)\n");
        }
        else if (bags_of_rice >= 5000){
            current_tax_rate = 0.10;                 
            printf("\nTier: Bulk Shipment (10%% tax applied)\n");
        }
        else{
            printf("\nTier: Standard Shipment (Rate: %.0f%% tax applied)\n", current_tax_rate * 100);
        }

        // --- 5. CALCULATION ---
        float subtotal = bags_of_rice * price_per_bag_lrd;
        float total_tax = subtotal * current_tax_rate;
        float grand_total = subtotal + total_tax;

        // Add to daily totals
        daily_total_revenue += grand_total;
        daily_total_tax += total_tax;

        // --- 6. GET DATE/TIME (FEATURE 1) ---
        time_t current_time;
        struct tm *local_time;
        time(&current_time);
        local_time = localtime(&current_time);
        
        // Format: YYYY-MM-DD HH:MM:SS
        char time_str[50];
        strftime(time_str, sizeof(time_str), "%Y-%m-%d %H:%M:%S", local_time);

        // --- 7. PRINT REPORT TO SCREEN ---
        printf("=======================================================\n");
        printf("Date & Time   : %s\n", time_str);
        printf("Merchant ID   : %d\n", merchant_id);
        printf("Merchant Name : %s\n", merchant_name);
        printf("Contact No.   : %s\n", contact_number);
        printf("-------------------------------------------------------\n");
        printf("Base Subtotal : %.2f LRD\n", subtotal);
        printf("Government Tax: %.2f LRD\n", total_tax);
        printf("Grand Total   : %.2f LRD\n", grand_total);
        printf("=======================================================\n");
        printf("Clearance calculation Complete. Ready for payment.\n");

        // --- 8. SAVE REPORT TO FILE ---
        fprintf(receipt_file, "--- Merchant #%d ---\n", merchant_count);
        fprintf(receipt_file, "Date & Time: %s\n", time_str);
        fprintf(receipt_file, "ID: %d | Name: %s | Contact: %s\n", merchant_id, merchant_name, contact_number);
        fprintf(receipt_file, "Bags: %d | Price: %.2f | Tax Rate: %.2f\n", bags_of_rice, price_per_bag_lrd, current_tax_rate);
        fprintf(receipt_file, "Base Subtotal: %.2f LRD\n", subtotal);
        fprintf(receipt_file, "Government Tax: %.2f LRD\n", total_tax);
        fprintf(receipt_file, "Grand Total: %.2f LRD\n\n", grand_total);

        // Ask to continue
        printf("\nProcess another merchant? (1 for Yes, 0 for No): ");
        scanf("%d", &keep_running);
        clear_buffer(); 
        
        merchant_count++; 
    }

    fclose(receipt_file);

    // --- 9. PRINT DAILY REVENUE REPORT (FEATURE 2) ---
    printf("\n=======================================================\n");
    printf("             DAILY REVENUE SUMMARY REPORT             \n");
    printf("=======================================================\n");
    printf("Total Merchants Processed : %d\n", merchant_count - 1);
    printf("Total Tax Collected       : %.2f LRD\n", daily_total_tax);
    printf("Total Revenue (with tax)  : %.2f LRD\n", daily_total_revenue);
    printf("=======================================================\n");

    // --- 10. SEARCH RECEIPT (FEATURE 3) ---
    int search_choice;
    printf("\nDo you want to search for a specific Merchant ID in the file? (1 for Yes, 0 for No): ");
    scanf("%d", &search_choice);
    clear_buffer();

    if (search_choice == 1) {
        int search_id;
        printf("Enter Merchant ID to search: ");
        scanf("%d", &search_id);
        clear_buffer();

        // Reopen file for reading
        FILE *search_file = fopen("receipts.txt", "r");
        if (search_file == NULL) {
            printf("Error: Could not open receipts.txt.\n");
        } else {
            char line[256];
            int found = 0;
            printf("\n--- SEARCH RESULTS FOR ID %d ---\n", search_id);
            
            // Read line by line
            while (fgets(line, sizeof(line), search_file) != NULL) {
                // Check if the line contains "ID: <search_id> |"
                char target[20];
                sprintf(target, "ID: %d ", search_id); 
                
                if (strstr(line, target) != NULL) {
                    found = 1;
                    // Print the matching ID line and the next 4 lines
                    printf("%s", line);
                    for(int i = 0; i < 4; i++) {
                        if (fgets(line, sizeof(line), search_file) != NULL) {
                            printf("%s", line);
                        }
                    }
                    printf("\n");
                }
            }
            
            if (!found) {
                printf("No receipts found for Merchant ID %d.\n", search_id);
            }
            
            fclose(search_file);
        }
    }

    printf("\nAll transactions saved to receipts.txt. System shutting down...\n");
    printf("\nPress Enter to exit...");
    getchar(); 
   
    return 0;
}